"""
Système de progression et logs visuels améliorés pour le bot Telegram
"""

import sys
import time
import threading
from datetime import datetime, timedelta


class Colors:
    """Codes couleurs ANSI pour les logs"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Couleurs de base
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Couleurs de fond
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'
    BG_BLUE = '\033[104m'


class BeautifulProgress:
    """Affichage de progression avancé avec statistiques"""
    
    def __init__(self, total_items, task_name="Téléchargement", show_speed=True):
        self.total_items = total_items
        self.task_name = task_name
        self.show_speed = show_speed
        self.current_item = 0
        self.start_time = time.time()
        self.last_update_time = time.time()
        self.completed_times = []
        self.lock = threading.Lock()
        
    def update(self, increment=1, item_name=""):
        """Met à jour la progression"""
        with self.lock:
            self.current_item += increment
            current_time = time.time()
            self.completed_times.append(current_time)
            
            # Garder seulement les 10 derniers temps pour calculer la vitesse
            if len(self.completed_times) > 10:
                self.completed_times = self.completed_times[-10:]
            
            self._display_progress(item_name)
            self.last_update_time = current_time
    
    def _display_progress(self, item_name=""):
        """Affiche la barre de progression"""
        if self.total_items <= 0:
            return
            
        percentage = min(100, (self.current_item / self.total_items) * 100)
        
        # Barre de progression
        bar_length = 30
        filled_length = int(bar_length * percentage // 100)
        bar = '█' * filled_length + '▒' * (bar_length - filled_length)
        
        # Statistiques de temps
        elapsed_time = time.time() - self.start_time
        
        # Calcul ETA
        if self.current_item > 0:
            avg_time_per_item = elapsed_time / self.current_item
            remaining_items = self.total_items - self.current_item
            eta_seconds = avg_time_per_item * remaining_items
            eta = str(timedelta(seconds=int(eta_seconds)))
        else:
            eta = "calcul..."
        
        # Vitesse récente (basée sur les 10 derniers éléments)
        speed = ""
        if self.show_speed and len(self.completed_times) >= 2:
            recent_time = self.completed_times[-1] - self.completed_times[0]
            recent_items = len(self.completed_times) - 1
            if recent_time > 0:
                items_per_second = recent_items / recent_time
                speed = f" | ⚡ {items_per_second:.1f}/s"
        
        # Construction du message
        progress_line = (
            f"\r{Colors.CYAN}🚀 {self.task_name}{Colors.RESET} "
            f"{Colors.YELLOW}[{bar}]{Colors.RESET} "
            f"{Colors.BOLD}{percentage:.1f}%{Colors.RESET} "
            f"({self.current_item}/{self.total_items}) "
            f"{Colors.GREEN}| ETA: {eta}{Colors.RESET}"
            f"{Colors.MAGENTA}{speed}{Colors.RESET}"
        )
        
        if item_name:
            progress_line += f" | {Colors.DIM}{item_name}{Colors.RESET}"
        
        # Afficher et nettoyer la ligne
        print(progress_line, end='', flush=True)
        
        # Nouvelle ligne à la fin
        if self.current_item >= self.total_items:
            elapsed_str = str(timedelta(seconds=int(elapsed_time)))
            print(f"\n{Colors.GREEN}✅ {self.task_name} terminé en {elapsed_str}{Colors.RESET}")
    
    def finish(self, success_message="Terminé avec succès"):
        """Termine la progression avec un message de succès"""
        elapsed_time = time.time() - self.start_time
        elapsed_str = str(timedelta(seconds=int(elapsed_time)))
        
        print(f"\n{Colors.GREEN}✅ {success_message} en {elapsed_str}{Colors.RESET}")
        
        # Statistiques finales
        if self.current_item > 0:
            avg_time = elapsed_time / self.current_item
            print(f"{Colors.DIM}📊 Moyenne: {avg_time:.2f}s par élément{Colors.RESET}")


class BeautifulLogger:
    """Logger avec messages colorés et formatés"""
    
    @staticmethod
    def info(message, prefix="ℹ️"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} {Colors.BLUE}{prefix} {message}{Colors.RESET}")
    
    @staticmethod
    def success(message, prefix="✅"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} {Colors.GREEN}{prefix} {message}{Colors.RESET}")
    
    @staticmethod
    def warning(message, prefix="⚠️"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} {Colors.YELLOW}{prefix} {message}{Colors.RESET}")
    
    @staticmethod
    def error(message, prefix="❌"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} {Colors.RED}{prefix} {message}{Colors.RESET}")
    
    @staticmethod
    def chapter_start(manga_name, chapter_number):
        print(f"\n{Colors.CYAN}📖 CHAPITRE {chapter_number}{Colors.RESET}")
        print(f"{Colors.BOLD}📚 Manga: {manga_name}{Colors.RESET}")
        print("─" * 50)
    
    @staticmethod
    def chapter_found(page_count):
        print(f"{Colors.GREEN}🎯 {page_count} pages trouvées{Colors.RESET}")
    
    @staticmethod
    def downloading_start(page_count):
        print(f"{Colors.YELLOW}📥 Début du téléchargement de {page_count} images...{Colors.RESET}")
    
    @staticmethod
    def conversion_start():
        print(f"{Colors.MAGENTA}📦 Conversion en CBZ...{Colors.RESET}")
    
    @staticmethod
    def chapter_complete(cbz_path, file_size_mb):
        print(f"{Colors.GREEN}💾 CBZ créé: {cbz_path} ({file_size_mb:.1f} MB){Colors.RESET}")
        print("─" * 50)


class MultiChapterProgress:
    """Gestionnaire de progression pour plusieurs chapitres"""
    
    def __init__(self, total_chapters, manga_name):
        self.total_chapters = total_chapters
        self.manga_name = manga_name
        self.current_chapter = 0
        self.start_time = time.time()
        self.successful_downloads = []
        self.failed_downloads = []
        
    def start_chapter(self, chapter_number):
        """Démarre un nouveau chapitre"""
        self.current_chapter = chapter_number
        BeautifulLogger.chapter_start(self.manga_name, chapter_number)
        
        # Progression générale
        chapter_index = len(self.successful_downloads) + len(self.failed_downloads) + 1
        percentage = (chapter_index / self.total_chapters) * 100
        
        print(f"{Colors.CYAN}📊 Progression générale: {chapter_index}/{self.total_chapters} "
              f"({percentage:.1f}%){Colors.RESET}")
    
    def chapter_success(self, chapter_number, cbz_path, file_size_mb):
        """Marque un chapitre comme réussi"""
        self.successful_downloads.append(chapter_number)
        BeautifulLogger.chapter_complete(cbz_path, file_size_mb)
        
    def chapter_failed(self, chapter_number, error_message):
        """Marque un chapitre comme échoué"""
        self.failed_downloads.append(chapter_number)
        BeautifulLogger.error(f"Échec chapitre {chapter_number}: {error_message}")
    
    def finish(self):
        """Termine et affiche le résumé"""
        elapsed_time = time.time() - self.start_time
        elapsed_str = str(timedelta(seconds=int(elapsed_time)))
        
        print(f"\n{Colors.BOLD}📋 RÉSUMÉ FINAL{Colors.RESET}")
        print("=" * 50)
        print(f"{Colors.GREEN}✅ Réussis: {len(self.successful_downloads)} chapitres{Colors.RESET}")
        
        if self.failed_downloads:
            print(f"{Colors.RED}❌ Échecs: {len(self.failed_downloads)} chapitres "
                  f"({', '.join(map(str, self.failed_downloads))}){Colors.RESET}")
        
        success_rate = (len(self.successful_downloads) / self.total_chapters) * 100
        print(f"{Colors.CYAN}📊 Taux de réussite: {success_rate:.1f}%{Colors.RESET}")
        print(f"{Colors.DIM}⏱️ Temps total: {elapsed_str}{Colors.RESET}")
        print("=" * 50)