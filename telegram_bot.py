#!/usr/bin/env python3
"""
Telegram Bot pour le téléchargement de manga depuis anime-sama.fr
Utilise le scraper existant pour télécharger et envoyer des fichiers CBZ.
"""

import os
import asyncio
import tempfile
import shutil
import zipfile
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from scraper.anime_sama_scraper import AnimeSamaScraper
from utils.zip_compressor import ZipCompressor
from utils.telegram_progress import TelegramDownloadProgress, format_clean_message, format_file_caption, format_filename
from keep_alive import keep_alive

# Token du bot Telegram - Chargé depuis les secrets Replit
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

def validate_telegram_token(token):
    """Valide le format basique du token Telegram"""
    if not token:
        return False
    # Validation basique: doit contenir ':'
    if ':' not in token:
        return False
    parts = token.split(':')
    if len(parts) != 2:
        return False
    # Première partie doit être numérique, seconde doit exister
    return parts[0].isdigit() and len(parts[1]) > 10

# Validation simple du token
if not TELEGRAM_TOKEN:
    print("❌ ERREUR: Token Telegram manquant!")
    print("📝 Ajoutez votre token dans les Secrets Replit:")
    print("   - Nom: TELEGRAM_TOKEN")
    print("   - Valeur: votre_token_de_@BotFather")
    exit(1)

class TelegramMangaBot:
    def __init__(self):
        self.scraper = AnimeSamaScraper(verbose=True, use_residential_proxy=True, use_advanced_bypass=True, use_railway_bypass=True, use_hybrid_system=True)
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /start - Affiche les informations d'aide"""
        welcome_message = """
╔═══════════════════════════╗
║    🎌 **ANIME-SAMA BOT** 🎌    ║
╚═══════════════════════════╝

✨ *Bienvenue dans l'univers du manga !* ✨

Je suis votre assistant personnel pour télécharger vos manga préférés depuis **anime-sama.fr** et les recevoir instantanément au format **CBZ** !

🔸 **━━━━━━━━━━━ COMMANDES ━━━━━━━━━━━** 🔸

📖 **`/scan <nom_manga> <chapitre>`**
   ▸ Télécharge un chapitre unique
   ▸ *Exemple :* `/scan blue lock 272`
   ▸ *Exemple :* `/scan one piece 1095`

📚 **`/multiscan <nom_manga> <début> <fin>`**
   ▸ Télécharge plusieurs chapitres (max 20)
   ▸ *Exemple :* `/multiscan lookism 1 5`
   ▸ *Exemple :* `/multiscan tokyo ghoul 10 15`

📦 **`/tome <nom_manga> <numéro_tome>`**
   ▸ Télécharge un tome complet (10 chapitres dans 1 ZIP)
   ▸ *Tome 1 = chapitres 1-10, Tome 2 = chapitres 11-20...*
   ▸ *Exemple :* `/tome blue lock 1`
   ▸ *Exemple :* `/tome lookism 3`

❓ **`/help`** ▸ Réaffiche cette aide

🔸 **━━━━━━━━━━━ FONCTIONNALITÉS ━━━━━━━━━━━** 🔸

✅ Téléchargement ultra-rapide
✅ Format CBZ compatible tous lecteurs
✅ Support des noms avec espaces
✅ Suivi de progression en temps réel
✅ Gestion intelligente des erreurs

🔸 **━━━━━━━━━━━━━ CONSEILS ━━━━━━━━━━━━━** 🔸

💡 *Noms de manga :* Utilisez les noms exacts d'anime-sama.fr
⏱️ *Patience :* Les téléchargements prennent 1-3 minutes
📱 *Limite :* Fichiers jusqu'à 50 MB (limite Telegram)
🎯 *Précision :* Vérifiez l'orthographe pour de meilleurs résultats

═══════════════════════════════════════════

🚀 **Prêt à commencer ?** Tapez une commande ci-dessus !
        """
        
        if update.message:
            await update.message.reply_text(
                welcome_message, 
                parse_mode=ParseMode.MARKDOWN
            )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /help - Affiche l'aide"""
        if not update.message:
            return
        await self.start_command(update, context)

    async def scan_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /scan - Télécharge un chapitre unique avec progression temps réel"""
        if not update.message:
            return
            
        if not context.args or len(context.args) < 2:
            await update.message.reply_text(
                "🚫 <b>Commande incomplète !</b>\n\n"
                "📋 <b>Format attendu :</b>\n"
                "<code>/scan &lt;nom_manga&gt; &lt;chapitre&gt;</code>\n\n"
                "✨ <b>Exemples :</b>\n"
                "• <code>/scan blue lock 272</code>\n"
                "• <code>/scan one piece 1095</code>\n"
                "• <code>/scan lookism 1</code>",
                parse_mode=ParseMode.HTML
            )
            return

        try:
            # Extraire le nom du manga et le numéro de chapitre
            chapter_number = int(context.args[-1])
            manga_name = " ".join(context.args[:-1])
            
            # Message initial propre
            await update.message.reply_text(
                f"🎯 <b>Recherche en cours...</b>\n\n"
                f"📖 <b>Manga :</b> {format_clean_message(manga_name)}\n"
                f"📄 <b>Chapitre :</b> {chapter_number}\n\n"
                f"🔍 <i>Analyse de la page du chapitre...</i>",
                parse_mode=ParseMode.HTML
            )
            
            # Créer un répertoire temporaire pour ce téléchargement
            with tempfile.TemporaryDirectory() as temp_dir:
                # Configurer le scraper avec le répertoire temporaire
                scraper = AnimeSamaScraper(
                    output_dir=temp_dir,
                    temp_dir=os.path.join(temp_dir, "temp"),
                    verbose=False
                )
                
                # Créer gestionnaire de progression
                progress_manager = TelegramDownloadProgress(
                    update, 
                    manga_name, 
                    f"Chapitre {chapter_number}"
                )
                
                # Hook pour capturer la progression
                original_download_chapter = scraper.download_chapter
                
                async def download_with_progress(manga, chapter):
                    # Démarrer avec une estimation
                    await progress_manager.start_download(20)  # Estimation initiale
                    
                    # Simulation de progression pendant le téléchargement
                    progress_task = asyncio.create_task(self._simulate_download_progress(progress_manager))
                    
                    # Téléchargement réel
                    result = original_download_chapter(manga, chapter)
                    
                    # Arrêter la simulation
                    progress_task.cancel()
                    
                    # Finaliser selon résultat
                    if result:
                        await progress_manager.complete_download(20, 20, 0)  # Succès
                    else:
                        await progress_manager.complete_download(0, 20, 0)   # Échec
                    
                    return result
                
                # Télécharger le chapitre avec progression
                success = await download_with_progress(manga_name, chapter_number)
                
                if success:
                    # Trouver le fichier CBZ créé
                    cbz_files = [f for f in os.listdir(temp_dir) if f.endswith('.cbz')]
                    
                    if cbz_files:
                        cbz_path = os.path.join(temp_dir, cbz_files[0])
                        file_size = os.path.getsize(cbz_path)
                        file_size_mb = file_size / (1024 * 1024)
                        
                        # Nom de fichier propre
                        clean_filename = format_filename(manga_name, f"Chapitre_{chapter_number}")
                        
                        # Vérifier si compression nécessaire
                        if ZipCompressor.should_compress_for_telegram(cbz_path):
                            await update.message.reply_text(
                                f"📦 <b>Compression nécessaire</b>\n\n"
                                f"📊 <b>Taille originale :</b> {file_size_mb:.1f} MB\n"
                                f"⚠️ <b>Dépasse la limite de 50 MB</b>\n"
                                f"🔄 <i>Compression en cours...</i>",
                                parse_mode=ParseMode.HTML
                            )
                            
                            # Compresser le fichier
                            result = ZipCompressor.compress_file(cbz_path, temp_dir)
                            if result:
                                zip_path, orig_mb, comp_mb, ratio = result
                                
                                # Message de compression réussie (nettoyé)
                                await update.message.reply_text(
                                    f"✅ <b>Compression terminée</b>\n\n"
                                    f"📊 <b>Taille originale :</b> {orig_mb:.1f} MB\n"
                                    f"📦 <b>Taille compressée :</b> {comp_mb:.1f} MB\n"
                                    f"🎯 <b>Réduction :</b> {(orig_mb-comp_mb)/orig_mb*100:.1f}%",
                                    parse_mode=ParseMode.HTML
                                )
                                
                                # Envoyer le fichier compressé avec légende propre
                                clean_zip_filename = format_filename(manga_name, f"Chapitre_{chapter_number}", "zip")
                                caption = format_file_caption(manga_name, f"Chapitre {chapter_number}", comp_mb, True)
                                
                                with open(zip_path, 'rb') as zip_file:
                                    await update.message.reply_document(
                                        document=zip_file,
                                        filename=clean_zip_filename,
                                        caption=caption,
                                        parse_mode=ParseMode.HTML
                                    )
                            else:
                                await update.message.reply_text(
                                    "❌ <b>Erreur lors de la compression</b>\n"
                                    "Le fichier ne peut pas être envoyé car il dépasse 50 MB.",
                                    parse_mode=ParseMode.HTML
                                )
                        else:
                            # Envoyer directement sans compression
                            await update.message.reply_text(
                                f"🎉 <b>Téléchargement réussi !</b>\n\n"
                                f"📊 <b>Taille :</b> {file_size_mb:.1f} MB\n"
                                f"📤 <i>Envoi du fichier CBZ...</i>",
                                parse_mode=ParseMode.HTML
                            )
                            
                            # Légende propre pour le fichier
                            caption = format_file_caption(manga_name, f"Chapitre {chapter_number}", file_size_mb, False)
                            
                            with open(cbz_path, 'rb') as cbz_file:
                                await update.message.reply_document(
                                    document=cbz_file,
                                    filename=clean_filename,
                                    caption=caption,
                                    parse_mode=ParseMode.HTML
                                )
                    else:
                        await update.message.reply_text(
                            "❌ <b>Erreur :</b> Aucun fichier CBZ généré.",
                            parse_mode=ParseMode.HTML
                        )
                else:
                    await update.message.reply_text(
                        f"🚫 <b>Téléchargement échoué</b>\n\n"
                        f"🔍 <b>Vérifications suggérées :</b>\n"
                        f"• Nom du manga : <code>{format_clean_message(manga_name)}</code>\n"
                        f"• Numéro de chapitre : <code>{chapter_number}</code>\n"
                        f"• Disponibilité sur anime-sama.fr\n\n"
                        f"💡 <b>Conseil :</b> Essayez avec l'orthographe exacte du site",
                        parse_mode=ParseMode.HTML
                    )
                    
        except ValueError:
            await update.message.reply_text(
                "❌ <b>Le numéro de chapitre doit être un nombre entier !</b>\n"
                "Exemple : <code>/scan blue lock 272</code>",
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ <b>Une erreur est survenue :</b> {format_clean_message(str(e))}",
                parse_mode=ParseMode.HTML
            )
    
    async def _simulate_download_progress(self, progress_manager):
        """Simule la progression du téléchargement en temps réel"""
        try:
            phases = [
                ("🔍 Analyse de la page...", 2),
                ("📋 Extraction des URLs...", 4), 
                ("🖼️ Téléchargement Page 1...", 6),
                ("🖼️ Téléchargement Page 2...", 8),
                ("🖼️ Téléchargement Page 3...", 10),
                ("🖼️ Téléchargement Page 4...", 12),
                ("🖼️ Téléchargement Page 5...", 14),
                ("🖼️ Téléchargement Page 6...", 16),
                ("📦 Création du fichier CBZ...", 18),
                ("✅ Finalisation...", 20)
            ]
            
            for phase_name, progress in phases:
                await progress_manager.update_image_progress(progress, phase_name, True)
                await asyncio.sleep(0.5)  # Délai réaliste
                
        except asyncio.CancelledError:
            # La tâche a été annulée quand le téléchargement s'est terminé
            pass

    async def multiscan_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /multiscan - Télécharge plusieurs chapitres"""
        if not update.message:
            return
            
        if not context.args or len(context.args) < 3:
            await update.message.reply_text(
                "🚫 <b>Commande incomplète !</b>\n\n"
                "📋 <b>Format attendu :</b>\n"
                "<code>/multiscan &lt;nom_manga&gt; &lt;début&gt; &lt;fin&gt;</code>\n\n"
                "✨ <b>Exemples :</b>\n"
                "• <code>/multiscan lookism 1 5</code>\n"
                "• <code>/multiscan blue lock 270 275</code>\n"
                "• <code>/multiscan tokyo ghoul 10 15</code>",
                parse_mode=ParseMode.HTML
            )
            return

        try:
            # Extraire les arguments
            chapter_end = int(context.args[-1])
            chapter_start = int(context.args[-2])
            manga_name = " ".join(context.args[:-2])
            
            # Vérifier la plage de chapitres
            if chapter_start > chapter_end:
                await update.message.reply_text(
                    "❌ Le chapitre de début doit être inférieur ou égal au chapitre de fin !"
                )
                return
                
            if chapter_end - chapter_start > 20:
                await update.message.reply_text(
                    "❌ Maximum 20 chapitres à la fois pour éviter la surcharge !"
                )
                return
            
            total_chapters = chapter_end - chapter_start + 1
            await update.message.reply_text(
                f"🎯 <b>Téléchargement multiple en cours...</b>\n\n"
                f"📖 <b>Manga :</b> {format_clean_message(manga_name)}\n"
                f"📄 <b>Chapitres :</b> {chapter_start} à {chapter_end} <i>({total_chapters} chapitres)</i>\n\n"
                f"⏳ <i>Cela peut prendre plusieurs minutes...</i>",
                parse_mode=ParseMode.HTML
            )
            
            # Créer un répertoire temporaire pour tous les téléchargements
            with tempfile.TemporaryDirectory() as temp_dir:
                scraper = AnimeSamaScraper(
                    output_dir=temp_dir,
                    temp_dir=os.path.join(temp_dir, "temp"),
                    verbose=False
                )
                
                successful_downloads = []
                failed_downloads = []
                
                # Utiliser la nouvelle méthode de téléchargement multiple avec progression
                successful_downloads, failed_downloads = scraper.download_multiple_chapters(
                    manga_name, chapter_start, chapter_end
                )
                
                # Envoyer les fichiers CBZ créés
                cbz_files = [f for f in os.listdir(temp_dir) if f.endswith('.cbz')]
                cbz_files.sort()  # Trier par nom pour un ordre logique
                
                if cbz_files:
                    await update.message.reply_text(
                        f"🎉 <b>{len(successful_downloads)} chapitres téléchargés !</b>\n\n"
                        f"📤 <b>Envoi des fichiers CBZ...</b>",
                        parse_mode=ParseMode.HTML
                    )
                    
                    for cbz_file in cbz_files:
                        cbz_path = os.path.join(temp_dir, cbz_file)
                        file_size = os.path.getsize(cbz_path)
                        file_size_mb = file_size / (1024 * 1024)
                        
                        # Nom de fichier propre  
                        clean_filename = format_filename(manga_name, f"Ch_{os.path.splitext(cbz_file)[0].split('_')[-1]}")
                        
                        # Vérifier si compression nécessaire
                        if ZipCompressor.should_compress_for_telegram(cbz_path):
                            await update.message.reply_text(
                                f"📦 <b>{cbz_file}</b> - Compression nécessaire ({file_size_mb:.1f} MB)",
                                parse_mode=ParseMode.HTML
                            )
                            
                            # Compresser le fichier
                            result = ZipCompressor.compress_file(cbz_path, temp_dir)
                            if result:
                                zip_path, orig_mb, comp_mb, ratio = result
                                
                                # Légende propre
                                caption = format_file_caption(manga_name, f"Chapitre inclus", comp_mb, True)
                                
                                # Envoyer le fichier compressé
                                with open(zip_path, 'rb') as f:
                                    await update.message.reply_document(
                                        document=f,
                                        filename=os.path.basename(zip_path),
                                        caption=caption,
                                        parse_mode=ParseMode.HTML
                                    )
                            else:
                                await update.message.reply_text(
                                    f"❌ Erreur compression {cbz_file} - Fichier ignoré",
                                    parse_mode=ParseMode.HTML
                                )
                        else:
                            # Légende propre
                            caption = format_file_caption(manga_name, f"Chapitre inclus", file_size_mb, False)
                            
                            # Envoyer directement
                            with open(cbz_path, 'rb') as f:
                                await update.message.reply_document(
                                    document=f,
                                    filename=clean_filename,
                                    caption=caption,
                                    parse_mode=ParseMode.HTML
                                )
                            
                        # Petite pause pour éviter la limite de débit
                        await asyncio.sleep(1)
                
                # Résumé final
                summary = f"📊 <b>RÉSUMÉ DU TÉLÉCHARGEMENT</b>\n\n"
                summary += f"✅ <b>Réussis :</b> <code>{len(successful_downloads)}</code> chapitres\n"
                if failed_downloads:
                    summary += f"❌ <b>Échecs :</b> <code>{len(failed_downloads)}</code> chapitres ({', '.join(map(str, failed_downloads))})\n"
                summary += f"\n🎉 <b>Téléchargement terminé !</b>"
                
                await update.message.reply_text(summary, parse_mode=ParseMode.HTML)
                
        except ValueError:
            await update.message.reply_text(
                "❌ Les numéros de chapitre doivent être des nombres entiers !\n"
                "Exemple: `/multiscan lookism 1 5`",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ Une erreur est survenue: {str(e)}"
            )

    async def tome_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /tome - Télécharge un tome complet (10 chapitres dans un ZIP)"""
        if not update.message:
            return
            
        if not context.args or len(context.args) < 2:
            await update.message.reply_text(
                "🚫 <b>Commande incomplète !</b>\n\n"
                "📋 <b>Format attendu :</b>\n"
                "<code>/tome &lt;nom_manga&gt; &lt;numéro_tome&gt;</code>\n\n"
                "✨ <b>Exemples :</b>\n"
                "• <code>/tome blue lock 1</code> <i>(chapitres 1-10)</i>\n"
                "• <code>/tome lookism 3</code> <i>(chapitres 21-30)</i>\n"
                "• <code>/tome one piece 5</code> <i>(chapitres 41-50)</i>\n\n"
                "📦 <b>Format :</b> Tome complet dans un fichier ZIP",
                parse_mode=ParseMode.HTML
            )
            return

        try:
            # Extraire le nom du manga et le numéro de tome
            tome_number = int(context.args[-1])
            manga_name = " ".join(context.args[:-1])
            
            # Calculer la plage de chapitres pour ce tome
            chapter_start = (tome_number - 1) * 10 + 1
            chapter_end = tome_number * 10
            
            await update.message.reply_text(
                f"📦 <b>Téléchargement du tome {tome_number}</b>\n\n"
                f"📖 <b>Manga :</b> {format_clean_message(manga_name)}\n"
                f"📄 <b>Chapitres :</b> {chapter_start} à {chapter_end} <i>(10 chapitres)</i>\n"
                f"🗜️ <b>Format :</b> ZIP contenant les CBZ\n\n"
                f"⏳ <i>Cela peut prendre 5-10 minutes...</i>",
                parse_mode=ParseMode.HTML
            )
            
            # Créer un répertoire temporaire pour tous les téléchargements
            with tempfile.TemporaryDirectory() as temp_dir:
                scraper = AnimeSamaScraper(
                    output_dir=temp_dir,
                    temp_dir=os.path.join(temp_dir, "temp"),
                    verbose=False
                )
                
                successful_downloads = []
                failed_downloads = []
                
                # Utiliser la nouvelle méthode de téléchargement multiple avec progression pour le tome
                successful_downloads, failed_downloads = scraper.download_multiple_chapters(
                    manga_name, chapter_start, chapter_end
                )
                
                # Vérifier s'il y a des fichiers CBZ créés
                cbz_files = [f for f in os.listdir(temp_dir) if f.endswith('.cbz')]
                
                if cbz_files:
                    # Créer le fichier ZIP du tome
                    sanitized_name = manga_name.replace(" ", "_").replace("/", "_")
                    zip_filename = f"{sanitized_name}_Tome_{tome_number}.zip"
                    zip_path = os.path.join(temp_dir, zip_filename)
                    
                    await update.message.reply_text(
                        f"📦 **Création du tome ZIP en cours...**\n"
                        f"✅ **{len(successful_downloads)} chapitres** téléchargés\n"
                        f"🗜️ **Compression** des CBZ dans le ZIP...",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    
                    # Utiliser le nouveau système de compression pour le tome
                    cbz_paths = [os.path.join(temp_dir, cbz_file) for cbz_file in cbz_files]
                    result = ZipCompressor.compress_multiple_files(
                        cbz_paths, 
                        f"{sanitized_name}_Tome_{tome_number}", 
                        temp_dir
                    )
                    
                    if result:
                        zip_path, total_orig_mb, compressed_mb, file_count = result
                        
                        # Vérifier si le fichier compressé respecte la limite Telegram
                        if ZipCompressor.should_compress_for_telegram(zip_path):
                            await update.message.reply_text(
                                f"⚠️ **Tome très volumineux !**\n\n"
                                f"📊 **Taille compressée :** `{compressed_mb:.1f} MB`\n"
                                f"🔄 **Compression supplémentaire en cours...**",
                                parse_mode=ParseMode.MARKDOWN
                            )
                            
                            # Double compression si nécessaire
                            final_result = ZipCompressor.compress_file(zip_path, temp_dir)
                            if final_result:
                                final_zip_path, _, final_mb, _ = final_result
                                
                                if final_mb > 50:
                                    await update.message.reply_text(
                                        f"🚫 **Tome impossible à envoyer**\n\n"
                                        f"📊 **Taille finale :** `{final_mb:.1f} MB`\n"
                                        f"⚠️ **Dépasse encore la limite**\n\n"
                                        f"💡 **Utilisez `/multiscan {manga_name} {chapter_start} {chapter_end}` pour envoyer les chapitres séparément**",
                                        parse_mode=ParseMode.MARKDOWN
                                    )
                                    return
                                
                                # Envoyer le fichier double-compressé
                                await update.message.reply_text(
                                    f"📦 **Tome super-compressé !**\n\n"
                                    f"📊 **Taille originale :** `{total_orig_mb:.1f} MB`\n"
                                    f"📦 **Taille finale :** `{final_mb:.1f} MB`\n"
                                    f"📤 **Envoi en cours...**",
                                    parse_mode=ParseMode.MARKDOWN
                                )
                                
                                with open(final_zip_path, 'rb') as zip_file:
                                    await update.message.reply_document(
                                        document=zip_file,
                                        filename=os.path.basename(final_zip_path),
                                        caption=f"📦 **{manga_name} - Tome {tome_number}**\n"
                                               f"📚 *{file_count} chapitres ({chapter_start}-{chapter_end})*\n"
                                               f"📦 *Super-compressé: {total_orig_mb:.1f}→{final_mb:.1f} MB*\n"
                                               f"🎌 *Collection depuis anime-sama.fr*"
                                    )
                            else:
                                await update.message.reply_text("❌ **Erreur lors de la compression supplémentaire**")
                                return
                        else:
                            # Envoyer le fichier normalement compressé
                            compression_ratio = ((total_orig_mb - compressed_mb) / total_orig_mb) * 100
                            await update.message.reply_text(
                                f"🎉 **Tome {tome_number} créé avec succès !**\n\n"
                                f"📊 **Taille originale :** `{total_orig_mb:.1f} MB`\n"
                                f"📦 **Taille compressée :** `{compressed_mb:.1f} MB`\n"
                                f"✅ **Réduction :** `{compression_ratio:.1f}%`\n"
                                f"📤 **Envoi du tome ZIP...**",
                                parse_mode=ParseMode.MARKDOWN
                            )
                            
                            with open(zip_path, 'rb') as zip_file:
                                await update.message.reply_document(
                                    document=zip_file,
                                    filename=os.path.basename(zip_path),
                                    caption=f"📦 **{manga_name} - Tome {tome_number}**\n"
                                           f"📚 *{file_count} chapitres ({chapter_start}-{chapter_end})*\n"
                                           f"📦 *Compressé: {total_orig_mb:.1f}→{compressed_mb:.1f} MB*\n"
                                           f"🎌 *Collection depuis anime-sama.fr*"
                                )
                    else:
                        await update.message.reply_text("❌ **Erreur lors de la création du tome ZIP**")
                    
                    # Résumé final
                    summary = f"📊 **RÉSUMÉ DU TOME {tome_number}**\n\n"
                    summary += f"✅ **Téléchargés :** `{len(successful_downloads)}` chapitres\n"
                    if failed_downloads:
                        summary += f"❌ **Échecs :** `{len(failed_downloads)}` chapitres ({', '.join(map(str, failed_downloads))})\n"
                    summary += f"📦 **Format :** ZIP avec {len(cbz_files)} fichiers CBZ\n"
                    summary += f"\n🎉 **Tome complet envoyé !**"
                    
                    await update.message.reply_text(summary, parse_mode=ParseMode.MARKDOWN)
                    
                else:
                    await update.message.reply_text(
                        f"🚫 **Aucun chapitre téléchargé**\n\n"
                        f"🔍 **Vérifications suggérées :**\n"
                        f"• Nom du manga : `{manga_name}`\n"
                        f"• Tome {tome_number} (chapitres {chapter_start}-{chapter_end})\n"
                        f"• Disponibilité sur anime-sama.fr\n\n"
                        f"💡 **Conseil :** Vérifiez si ces chapitres existent",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    
        except ValueError:
            await update.message.reply_text(
                "❌ Le numéro de tome doit être un nombre entier !\n"
                "Exemple: `/tome blue lock 1`",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ Une erreur est survenue: {str(e)}"
            )

def main():
    """Fonction principale pour démarrer le bot"""
    try:
        # Vérifier que le token existe 
        if not TELEGRAM_TOKEN:
            print("❌ ERREUR: Token Telegram manquant!")
            return
            
        # Améliorer les logs de démarrage
        from utils.beautiful_progress import BeautifulLogger
        
        BeautifulLogger.info("Démarrage du serveur Flask...", "🌐")
        # Démarrer le serveur web pour keep_alive (nécessaire pour Railway health check)
        keep_alive()
        
        BeautifulLogger.info("Création de l'application Telegram...", "🔧")
        # Créer l'application bot avec configuration simplifiée
        try:
            # Configuration minimale pour éviter les conflits
            application = Application.builder().token(TELEGRAM_TOKEN).concurrent_updates(False).build()
            BeautifulLogger.success("Application Telegram créée avec succès")
        except Exception as e:
            BeautifulLogger.error(f"Erreur lors de la création de l'application: {e}")
            BeautifulLogger.warning("Vérifiez votre token Telegram")
            return
        
        BeautifulLogger.info("Initialisation du bot...", "🤖")
        # Créer une instance du bot
        try:
            bot = TelegramMangaBot()
        except Exception as e:
            BeautifulLogger.error(f"Erreur lors de l'initialisation du bot: {e}")
            return
        
        BeautifulLogger.info("Configuration des commandes...", "⚙️")
        # Ajouter les gestionnaires de commandes avec protection
        try:
            application.add_handler(CommandHandler("start", bot.start_command))
            application.add_handler(CommandHandler("help", bot.help_command))
            application.add_handler(CommandHandler("scan", bot.scan_command))
            application.add_handler(CommandHandler("multiscan", bot.multiscan_command))
            application.add_handler(CommandHandler("tome", bot.tome_command))
            BeautifulLogger.success("5 commandes configurées (/start, /help, /scan, /multiscan, /tome)")
        except Exception as e:
            BeautifulLogger.error(f"Erreur lors de la configuration des commandes: {e}")
            return
        
        BeautifulLogger.success("Bot Telegram prêt !", "🚀")
        BeautifulLogger.info("Envoyez /start à votre bot pour commencer", "📱")
        
        # Attendre un peu pour éviter les conflits de démarrage
        import time
        time.sleep(2)
        
        # Démarrer le bot simplement dans le thread principal
        try:
            BeautifulLogger.info("Démarrage en mode polling...", "🚀")
            BeautifulLogger.success("Bot actif - En attente des messages...")
            print("─" * 50)
            
            # Démarrer directement dans le thread principal (solution la plus simple)
            application.run_polling(
                poll_interval=3.0,
                timeout=30,
                drop_pending_updates=True
            )
            
        except Exception as e:
            BeautifulLogger.error(f"Erreur lors du démarrage: {e}")
            BeautifulLogger.warning(f"Type d'erreur: {type(e).__name__}")
            if str(e) != "Event loop is closed":
                import traceback
                traceback.print_exc()
            return
        
    except Exception as e:
        try:
            from utils.beautiful_progress import BeautifulLogger
            BeautifulLogger.error(f"Erreur critique au démarrage: {e}")
            BeautifulLogger.warning(f"Type d'erreur: {type(e).__name__}")
        except:
            print(f"❌ ERREUR CRITIQUE au démarrage: {e}")
            print(f"   Type d'erreur: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return

if __name__ == '__main__':
    main()