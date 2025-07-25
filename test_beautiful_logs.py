#!/usr/bin/env python3
"""
Script de test pour démontrer les logs améliorés
"""

import time
import os
from utils.beautiful_progress import BeautifulProgress, BeautifulLogger, MultiChapterProgress


def demo_single_chapter():
    """Démonstration du téléchargement d'un chapitre unique"""
    BeautifulLogger.chapter_start("One Piece", 1095)
    
    # Simulation des étapes de téléchargement
    BeautifulLogger.info("Analyse de la page du chapitre...")
    time.sleep(0.5)
    
    BeautifulLogger.chapter_found(15)
    BeautifulLogger.downloading_start(15)
    
    # Simulation du téléchargement avec barre de progression
    progress = BeautifulProgress(
        total_items=15,
        task_name="Téléchargement Ch.1095",
        show_speed=True
    )
    
    for i in range(1, 16):
        page_name = f"Page {i}"
        # Simuler un téléchargement variable
        time.sleep(0.2 + (i % 3) * 0.1)  # Vitesse variable pour réalisme
        
        # Simuler un échec occasionnel
        if i == 7:
            progress.update(item_name=f"{page_name} ✗ (retry)")
            time.sleep(0.3)
        
        progress.update(item_name=f"{page_name} ✓")
    
    progress.finish("Téléchargement terminé (14/15 pages)")
    
    BeautifulLogger.conversion_start()
    time.sleep(0.8)
    
    BeautifulLogger.chapter_complete("/downloads/One_Piece_ch1095.cbz", 12.4)


def demo_multiple_chapters():
    """Démonstration du téléchargement multiple"""
    print("\n" + "="*60)
    
    multi_progress = MultiChapterProgress(3, "Demon Slayer")
    
    chapters = [201, 202, 203]
    page_counts = [18, 20, 16]
    
    for i, (chapter_num, pages) in enumerate(zip(chapters, page_counts)):
        multi_progress.start_chapter(chapter_num)
        
        # Simulation du téléchargement du chapitre
        progress = BeautifulProgress(
            total_items=pages,
            task_name=f"Ch.{chapter_num}",
            show_speed=True
        )
        
        success = True
        for page in range(1, pages + 1):
            time.sleep(0.1)
            if chapter_num == 202 and page == 15:  # Simuler un échec sur le chapitre 202
                progress.update(item_name=f"Page {page} ✗")
                success = False
                break
            else:
                progress.update(item_name=f"Page {page} ✓")
        
        if success:
            progress.finish()
            multi_progress.chapter_success(chapter_num, f"/downloads/Demon_Slayer_ch{chapter_num}.cbz", 8.2)
        else:
            multi_progress.chapter_failed(chapter_num, "Erreur réseau page 15")
    
    multi_progress.finish()


def demo_bot_startup():
    """Démonstration des logs de démarrage du bot"""
    print("\n" + "="*60)
    print("DÉMARRAGE DU BOT TELEGRAM")
    print("="*60)
    
    BeautifulLogger.info("Démarrage du serveur Flask...", "🌐")
    time.sleep(0.5)
    
    BeautifulLogger.info("Création de l'application Telegram...", "🔧")
    time.sleep(0.3)
    
    BeautifulLogger.success("Application Telegram créée avec succès")
    
    BeautifulLogger.info("Initialisation du bot...", "🤖")
    time.sleep(0.2)
    
    BeautifulLogger.info("Configuration des commandes...", "⚙️")
    time.sleep(0.4)
    
    BeautifulLogger.success("5 commandes configurées (/start, /help, /scan, /multiscan, /tome)")
    
    BeautifulLogger.success("Bot Telegram prêt !", "🚀")
    BeautifulLogger.info("Envoyez /start à votre bot pour commencer", "📱")
    
    BeautifulLogger.info("Démarrage en mode polling...", "🚀")
    BeautifulLogger.success("Bot actif - En attente des messages...")
    print("─" * 50)


if __name__ == "__main__":
    print("🎨 DÉMONSTRATION DES LOGS AMÉLIORÉS")
    print("="*60)
    
    print("\n1️⃣ Démarrage du bot:")
    demo_bot_startup()
    
    print("\n2️⃣ Téléchargement d'un chapitre:")
    demo_single_chapter()
    
    print("\n3️⃣ Téléchargement multiple:")
    demo_multiple_chapters()
    
    print("\n🎉 Démonstration terminée !")