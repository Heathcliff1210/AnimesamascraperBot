#!/usr/bin/env python3
"""
Module de progression en temps réel pour Telegram
Affiche des barres de progression qui se mettent à jour automatiquement
"""

import asyncio
import time
from typing import Optional

class TelegramProgressBar:
    """
    Barre de progression qui se met à jour automatiquement sur Telegram
    """
    
    def __init__(self, update, total_items: int, task_name: str = "Téléchargement", auto_update_interval: float = 2.0):
        self.update = update
        self.total_items = total_items
        self.task_name = task_name
        self.auto_update_interval = auto_update_interval
        
        self.current_progress = 0
        self.start_time = time.time()
        self.last_update_time = 0
        self.message = None
        self.current_item_name = ""
        self.is_complete = False
        
    async def initialize(self):
        """Initialise la barre de progression avec le premier message"""
        progress_text = self._generate_progress_text()
        self.message = await self.update.message.reply_text(
            progress_text,
            parse_mode='HTML'
        )
        self.last_update_time = time.time()
    
    async def update_progress(self, current: int, item_name: str = ""):
        """Met à jour la progression"""
        self.current_progress = current
        self.current_item_name = item_name
        
        # Mise à jour automatique si assez de temps s'est écoulé
        current_time = time.time()
        if current_time - self.last_update_time >= self.auto_update_interval:
            await self._update_message()
            self.last_update_time = current_time
    
    async def complete(self, final_message: str = ""):
        """Marque la progression comme terminée"""
        self.is_complete = True
        self.current_progress = self.total_items
        
        if final_message:
            self.current_item_name = final_message
        
        await self._update_message()
    
    async def _update_message(self):
        """Met à jour le message de progression"""
        if not self.message:
            return
            
        try:
            progress_text = self._generate_progress_text()
            await self.message.edit_text(
                progress_text,
                parse_mode='HTML'
            )
        except Exception:
            # Ignore les erreurs de mise à jour (message trop ancien, etc.)
            pass
    
    def _generate_progress_text(self) -> str:
        """Génère le texte de la barre de progression"""
        # Calcul du pourcentage
        percentage = (self.current_progress / self.total_items) * 100 if self.total_items > 0 else 0
        
        # Barre de progression visuelle
        filled_blocks = int(percentage / 5)  # 20 blocs max (100% / 5)
        progress_bar = "█" * filled_blocks + "░" * (20 - filled_blocks)
        
        # Calcul du temps
        elapsed_time = time.time() - self.start_time
        
        if self.current_progress > 0 and not self.is_complete:
            # Estimation du temps restant
            time_per_item = elapsed_time / self.current_progress
            remaining_items = self.total_items - self.current_progress
            eta_seconds = time_per_item * remaining_items
            eta_text = self._format_time(eta_seconds)
        else:
            eta_text = "Calcul..."
        
        # Formatage du temps écoulé
        elapsed_text = self._format_time(elapsed_time)
        
        # Statut actuel
        status_icon = "✅" if self.is_complete else "🔄"
        
        # Construction du message
        progress_text = f"""<b>{status_icon} {self.task_name}</b>

<code>[{progress_bar}]</code>
<b>{self.current_progress}/{self.total_items}</b> ({percentage:.1f}%)

⏱ <b>Temps écoulé:</b> {elapsed_text}
"""
        
        if not self.is_complete and self.current_progress > 0:
            progress_text += f"⏰ <b>Temps restant:</b> {eta_text}\n"
        
        if self.current_item_name:
            # Limiter la longueur du nom d'item pour éviter les messages trop longs
            item_display = self.current_item_name
            if len(item_display) > 50:
                item_display = item_display[:47] + "..."
            progress_text += f"\n📄 <b>Actuellement:</b> {item_display}"
        
        return progress_text
    
    def _format_time(self, seconds: float) -> str:
        """Formate le temps en format lisible"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            remaining_seconds = int(seconds % 60)
            return f"{minutes}m {remaining_seconds}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"

class TelegramDownloadProgress:
    """
    Gestionnaire de progression spécialisé pour les téléchargements de manga
    """
    
    def __init__(self, update, manga_name: str, chapter_range: str = ""):
        self.update = update
        self.manga_name = manga_name
        self.chapter_range = chapter_range
        self.phases = []
        self.current_phase = 0
        self.progress_bar = None
        
    async def start_download(self, total_images: int):
        """Démarre la progression de téléchargement"""
        task_name = f"📚 {self.manga_name}"
        if self.chapter_range:
            task_name += f" ({self.chapter_range})"
            
        self.progress_bar = TelegramProgressBar(
            self.update, 
            total_images, 
            task_name,
            auto_update_interval=1.5  # Mise à jour plus rapide pour téléchargements
        )
        await self.progress_bar.initialize()
    
    async def update_image_progress(self, current_image: int, image_name: str, success: bool = True):
        """Met à jour la progression d'image"""
        if not self.progress_bar:
            return
            
        status_icon = "✅" if success else "❌"
        item_name = f"{status_icon} {image_name}"
        
        await self.progress_bar.update_progress(current_image, item_name)
    
    async def complete_download(self, success_count: int, total_count: int, file_size_mb: float = 0):
        """Finalise la progression de téléchargement"""
        if not self.progress_bar:
            return
            
        if success_count == total_count:
            final_message = f"Téléchargement terminé - {file_size_mb:.1f} MB"
        else:
            final_message = f"Terminé avec {success_count}/{total_count} réussies"
            
        await self.progress_bar.complete(final_message)

def format_clean_message(text: str) -> str:
    """
    Nettoie un message Telegram en retirant les astérisques et en formatant proprement
    """
    # Remplacer les astérisques par du HTML bold
    text = text.replace('**', '')  # Retirer les doubles astérisques
    text = text.replace('*', '')   # Retirer les astérisques simples
    
    # Nettoyer les caractères spéciaux problématiques
    text = text.replace('`', '')   # Retirer les backticks
    
    return text

def format_file_caption(manga_name: str, chapter_info: str, file_size_mb: float, is_compressed: bool = False) -> str:
    """
    Formate proprement la légende d'un fichier manga
    """
    # Nettoyage des noms
    clean_manga = format_clean_message(manga_name)
    clean_chapter = format_clean_message(chapter_info)
    
    # Construction de la légende
    caption = f"📚 <b>{clean_manga}</b>\n"
    caption += f"📖 {clean_chapter}\n"
    
    if is_compressed:
        caption += f"📦 <b>Fichier compressé</b> ({file_size_mb:.1f} MB)\n"
    else:
        caption += f"📊 <b>Taille:</b> {file_size_mb:.1f} MB\n"
    
    caption += f"🎌 <i>Téléchargé depuis anime-sama.fr</i>"
    
    return caption

def format_filename(manga_name: str, chapter_info: str, extension: str = "cbz") -> str:
    """
    Formate proprement le nom de fichier
    """
    # Nettoyage et remplacement des caractères problématiques
    clean_manga = manga_name.replace(' ', '_').replace('*', '').replace('`', '')
    clean_chapter = chapter_info.replace(' ', '_').replace('*', '').replace('`', '')
    
    # Limitation de longueur pour éviter les noms trop longs
    if len(clean_manga) > 30:
        clean_manga = clean_manga[:27] + "..."
    
    return f"{clean_manga}_{clean_chapter}.{extension}"