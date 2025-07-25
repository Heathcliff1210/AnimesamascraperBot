"""
Main scraper class for anime-sama.fr
"""

import os
import re
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tempfile
import shutil

from .url_builder import URLBuilder
from .image_downloader import ImageDownloader
from .cbz_converter import CBZConverter
from utils.headers import get_random_headers
from utils.beautiful_progress import BeautifulProgress, BeautifulLogger, MultiChapterProgress
# Cookie system removed - using only residential proxies and advanced headers
from utils.proxy_manager import ResidentialProxyManager, RailwayOptimizer
from utils.advanced_bypass import AdvancedAntiDetectionBypass
from utils.railway_bypass import RailwayOptimizedBypass
from utils.hybrid_breakthrough import HybridBreakthroughSystem

class AnimeSamaScraper:
    def __init__(self, output_dir="./downloads", temp_dir="./temp", verbose=False, use_residential_proxy=True, use_advanced_bypass=True, use_railway_bypass=True, use_hybrid_system=True):
        self.output_dir = output_dir
        self.temp_dir = temp_dir
        self.verbose = verbose
        self.use_residential_proxy = use_residential_proxy
        self.use_advanced_bypass = use_advanced_bypass
        self.use_railway_bypass = use_railway_bypass
        self.use_hybrid_system = use_hybrid_system
        self.proxy_manager = None
        self.railway_optimizer = None
        self.advanced_bypass = None
        self.railway_bypass = None
        self.hybrid_system = None
        
        # Détection automatique Railway
        self.is_railway = os.environ.get('RAILWAY_ENVIRONMENT') is not None
        
        # Ensure directories exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Initialize session with residential proxy system
        self.session = self._setup_enhanced_session()
        
        # Initialize other components
        self.url_builder = URLBuilder()
        self.image_downloader = ImageDownloader(self.session, verbose, scraper_instance=self)
        self.cbz_converter = CBZConverter(verbose)
    
    def _setup_enhanced_session(self):
        """
        Setup an enhanced session with residential proxies and advanced anti-detection.
        
        Returns:
            requests.Session: Configured session
        """
        # Système hybride révolutionnaire (priorité max)
        if self.use_hybrid_system:
            self.hybrid_system = HybridBreakthroughSystem(verbose=self.verbose)
            session = requests.Session()  # Session de base, le hybride gère tout
            if self.verbose:
                BeautifulLogger.info("Système hybride révolutionnaire activé", "🔥")
                
        # Fallback: systèmes individuels
        elif self.is_railway and self.use_railway_bypass:
            # Railway: système optimisé pour la production
            self.railway_bypass = RailwayOptimizedBypass(verbose=self.verbose)
            session = self.railway_bypass.create_railway_session()
            if self.verbose:
                BeautifulLogger.info("Système Railway ultra-optimisé activé", "🚄")
                
        elif self.use_advanced_bypass:
            # Local/autre: système avancé complet
            self.advanced_bypass = AdvancedAntiDetectionBypass(verbose=self.verbose)
            session = self.advanced_bypass.create_stealth_session()
            if self.verbose:
                BeautifulLogger.info("Système de contournement avancé activé", "🥷")
        else:
            session = requests.Session()
        
        # Initialize Railway optimizer
        self.railway_optimizer = RailwayOptimizer(verbose=self.verbose)
        
        # Initialize residential proxy manager (complément au bypass avancé)
        if self.use_residential_proxy and not self.use_advanced_bypass:
            self.proxy_manager = ResidentialProxyManager(verbose=self.verbose)
            if self.verbose:
                BeautifulLogger.info("Initialisation du système de proxies résidentiels...", "🏠")
        
        # 1. Apply residential proxy configuration (si pas de bypass avancé)
        if self.use_residential_proxy and self.proxy_manager and not self.use_advanced_bypass:
            if self.verbose:
                BeautifulLogger.info("Application de l'empreinte résidentielle avancée...", "🏠")
            
            identity_info = self.proxy_manager.setup_residential_session(session)
            if identity_info and self.verbose:
                BeautifulLogger.success(f"Identité résidentielle: {identity_info['region']} ({identity_info['isp']})")
        
        # 2. Apply Railway optimizations if on Railway
        if self.railway_optimizer.is_railway_environment():
            if self.verbose:
                BeautifulLogger.info("Configuration Railway détectée...", "🚂")
            
            if self.railway_optimizer.configure_for_railway(session):
                if self.verbose:
                    BeautifulLogger.success("Configuration Railway appliquée")
        
        # 3. Enhanced fallback headers (si aucun système avancé)
        if not self.use_advanced_bypass and not (self.use_residential_proxy and self.proxy_manager):
            if self.verbose:
                BeautifulLogger.info("Configuration headers avancés avec empreinte résidentielle...", "⚙️")
            
            session.headers.update(get_random_headers())
            
            # Enhanced cloud configuration with residential simulation
            import random
            cloud_env = os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('DYNO') or os.getenv('RENDER') or os.getenv('REPLIT_DEPLOYMENT')
            
            if cloud_env:
                enhanced_headers = {
                    'X-Forwarded-For': f"90.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
                    'X-Real-IP': f"78.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
                    'CF-Connecting-IP': f"176.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
                    'X-Forwarded-Proto': 'https',
                    'X-Forwarded-Host': 'anime-sama.fr',
                    'Origin': 'https://anime-sama.fr',
                    'Referer': 'https://anime-sama.fr/',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin'
                }
                session.headers.update(enhanced_headers)
        
        return session
    
    def refresh_session_on_block(self):
        """
        Refresh the session when blocked (403 errors).
        This creates a new session with fresh residential identity and headers.
        
        Returns:
            bool: True if session was refreshed successfully
        """
        try:
            if self.verbose:
                BeautifulLogger.warning("Renouvellement de la session suite à un blocage...")
            
            # Create a new enhanced session
            old_session = self.session
            self.session = self._setup_enhanced_session()
            
            # Update the image downloader with the new session
            self.image_downloader.session = self.session
            
            # Close the old session
            old_session.close()
            
            if self.verbose:
                BeautifulLogger.success("Session renouvelée avec succès")
            
            # Wait a moment before continuing
            time.sleep(2.0)
            
            return True
            
        except Exception as e:
            if self.verbose:
                BeautifulLogger.error(f"Erreur lors du renouvellement de la session: {str(e)}")
            return False
        
    def download_chapter(self, manga_name, chapter_number):
        """
        Download a manga chapter and convert it to CBZ format.
        
        Args:
            manga_name (str): Name of the manga
            chapter_number (int): Chapter number to download
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Initialiser les logs du chapitre
            BeautifulLogger.chapter_start(manga_name, chapter_number)
            
            # Build the chapter URL
            chapter_url = self.url_builder.build_chapter_url(manga_name, chapter_number)
            if self.verbose:
                BeautifulLogger.info(f"URL construite: {chapter_url}")
            
            # Get image URLs from the chapter page
            BeautifulLogger.info("Analyse de la page du chapitre...")
            image_urls = self._extract_image_urls(chapter_url, chapter_number)
            if not image_urls:
                BeautifulLogger.error("Aucune image trouvée pour ce chapitre")
                return False
            
            BeautifulLogger.chapter_found(len(image_urls))
            
            # Create temporary directory for this chapter
            chapter_temp_dir = os.path.join(
                self.temp_dir, 
                f"{self.url_builder.sanitize_name(manga_name)}_ch{chapter_number}"
            )
            os.makedirs(chapter_temp_dir, exist_ok=True)
            
            # Download all images with beautiful progress
            BeautifulLogger.downloading_start(len(image_urls))
            downloaded_files = []
            
            # Créer la barre de progression
            progress = BeautifulProgress(
                total_items=len(image_urls),
                task_name=f"Téléchargement Ch.{chapter_number}",
                show_speed=True
            )
            
            for i, img_url in enumerate(image_urls, 1):
                filename = f"page_{i:03d}.jpg"
                filepath = os.path.join(chapter_temp_dir, filename)
                
                # Mettre à jour la progression avec le nom de la page
                page_name = f"Page {i}"
                
                if self.image_downloader.download_image(img_url, filepath):
                    downloaded_files.append(filepath)
                    progress.update(item_name=f"{page_name} ✓")
                else:
                    progress.update(item_name=f"{page_name} ✗")
                    if self.verbose:
                        BeautifulLogger.warning(f"Échec téléchargement page {i}")
                    
                # Add delay to avoid being detected
                time.sleep(0.5)
            
            progress.finish(f"Téléchargement terminé ({len(downloaded_files)}/{len(image_urls)} pages)")
            
            if not downloaded_files:
                BeautifulLogger.error("Aucune image téléchargée avec succès")
                return False
            
            # Convert to CBZ
            cbz_filename = f"{self.url_builder.sanitize_name(manga_name)}_ch{chapter_number}.cbz"
            cbz_path = os.path.join(self.output_dir, cbz_filename)
            
            BeautifulLogger.conversion_start()
            if self.cbz_converter.create_cbz(chapter_temp_dir, cbz_path):
                # Calculer la taille du fichier
                file_size_mb = os.path.getsize(cbz_path) / (1024 * 1024)
                BeautifulLogger.chapter_complete(cbz_path, file_size_mb)
                return True
            else:
                BeautifulLogger.error("Échec de la création du CBZ")
                return False
                
        except Exception as e:
            BeautifulLogger.error(f"Erreur lors du téléchargement: {str(e)}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False
    
    def download_multiple_chapters(self, manga_name, start_chapter, end_chapter):
        """
        Download multiple chapters with beautiful progress tracking
        
        Args:
            manga_name (str): Name of the manga
            start_chapter (int): First chapter to download
            end_chapter (int): Last chapter to download
            
        Returns:
            tuple: (successful_chapters, failed_chapters)
        """
        total_chapters = end_chapter - start_chapter + 1
        multi_progress = MultiChapterProgress(total_chapters, manga_name)
        
        print(f"\n🚀 TÉLÉCHARGEMENT MULTIPLE - {manga_name}")
        print(f"📚 Chapitres {start_chapter} à {end_chapter} ({total_chapters} chapitres)")
        print("=" * 60)
        
        successful_chapters = []
        failed_chapters = []
        
        for chapter_num in range(start_chapter, end_chapter + 1):
            try:
                multi_progress.start_chapter(chapter_num)
                
                if self.download_chapter(manga_name, chapter_num):
                    # Calculer la taille du fichier CBZ créé
                    cbz_filename = f"{self.url_builder.sanitize_name(manga_name)}_ch{chapter_num}.cbz"
                    cbz_path = os.path.join(self.output_dir, cbz_filename)
                    
                    if os.path.exists(cbz_path):
                        file_size_mb = os.path.getsize(cbz_path) / (1024 * 1024)
                        multi_progress.chapter_success(chapter_num, cbz_path, file_size_mb)
                        successful_chapters.append(chapter_num)
                    else:
                        multi_progress.chapter_failed(chapter_num, "Fichier CBZ non trouvé")
                        failed_chapters.append(chapter_num)
                else:
                    multi_progress.chapter_failed(chapter_num, "Téléchargement échoué")
                    failed_chapters.append(chapter_num)
                    
            except Exception as e:
                error_msg = f"Erreur inattendue: {str(e)}"
                multi_progress.chapter_failed(chapter_num, error_msg)
                failed_chapters.append(chapter_num)
        
        multi_progress.finish()
        return successful_chapters, failed_chapters
    
    def _extract_image_urls(self, chapter_url, chapter_number, max_retries=2):
        """
        Extract image URLs from a chapter page with enhanced error handling.
        This method handles anime-sama.fr specific structure using episodes.js.
        
        Args:
            chapter_url (str): URL of the chapter page
            chapter_number (int): Chapter number to extract
            max_retries (int): Maximum number of retries for 403 errors
            
        Returns:
            list: List of image URLs
        """
        for attempt in range(max_retries + 1):
            try:
                if self.verbose and attempt > 0:
                    BeautifulLogger.info(f"Tentative {attempt + 1} pour récupérer les données du chapitre...")
                elif self.verbose:
                    BeautifulLogger.info(f"Récupération de la page du chapitre: {chapter_url}")
                
                # First, get the episodes.js file which contains the chapter data
                episodes_url = urljoin(chapter_url, 'episodes.js')
                
                if self.verbose:
                    BeautifulLogger.info(f"Récupération des données episodes: {episodes_url}")
                
                # Système hybride révolutionnaire (priorité absolue)
                if self.use_hybrid_system and self.hybrid_system:
                    if self.verbose:
                        BeautifulLogger.info("Utilisation système hybride révolutionnaire...", "🔥")
                    
                    response = self.hybrid_system.breakthrough_request(episodes_url, max_global_retries=6)
                    
                    if not response:
                        if self.verbose:
                            BeautifulLogger.warning("Système hybride échoué - Fallback ultime")
                        response = self.session.get(episodes_url, timeout=30)
                
                # Fallback: systèmes individuels
                elif self.is_railway and self.railway_bypass:
                    if self.verbose:
                        BeautifulLogger.info("Utilisation Railway bypass ultra-rapide...", "🚄")
                    
                    response = self.railway_bypass.railway_request(episodes_url, max_retries=3)
                    
                    if not response:
                        if self.verbose:
                            BeautifulLogger.warning("Railway bypass échoué - Fallback")
                        response = self.session.get(episodes_url, timeout=30)
                        
                elif self.use_advanced_bypass and self.advanced_bypass:
                    if self.verbose:
                        BeautifulLogger.info("Utilisation du système de contournement avancé...", "🥷")
                    
                    response = self.advanced_bypass.bypass_request(episodes_url, max_retries=3)
                    
                    if not response:
                        if self.verbose:
                            BeautifulLogger.warning("Échec contournement - Fallback méthode standard")
                        response = self.session.get(episodes_url, timeout=45)
                else:
                    # Make the request with enhanced error handling
                    response = self.session.get(episodes_url, timeout=45)
                
                # Handle 403 specifically
                if response.status_code == 403:
                    if attempt < max_retries:
                        if self.verbose:
                            BeautifulLogger.warning(f"Accès refusé (403), renouvellement de la session...")
                        
                        # Refresh session and try again
                        self.refresh_session_on_block()
                        continue
                    else:
                        BeautifulLogger.error("Échec persistant avec erreur 403 - Site bloque l'accès automatisé")
                        return []
                
                response.raise_for_status()
                
                # Parse the JavaScript content to extract chapter data
                episodes_content = response.text
                
                # Extract chapter number from chapter_url (need to get it from context)
                manga_name = self.url_builder.extract_manga_name_from_url(chapter_url)
                
                return self._parse_episodes_js(episodes_content, chapter_number)
                
            except requests.RequestException as e:
                error_str = str(e)
                if "403" in error_str or "Forbidden" in error_str:
                    if attempt < max_retries:
                        if self.verbose:
                            BeautifulLogger.warning(f"Erreur 403 détectée, renouvellement de la session...")
                        self.refresh_session_on_block()
                        continue
                    else:
                        BeautifulLogger.error("Échec persistant avec erreur 403 - Protections anti-bot du site")
                        return []
                else:
                    BeautifulLogger.error(f"Erreur réseau lors de la récupération des données: {error_str}")
                    if attempt < max_retries:
                        time.sleep(3.0 * (attempt + 1))  # Délai progressif
                        continue
                    return []
                    
            except Exception as e:
                BeautifulLogger.error(f"Erreur lors de l'extraction des URLs d'images: {str(e)}")
                if self.verbose:
                    import traceback
                    traceback.print_exc()
                if attempt < max_retries:
                    time.sleep(2.0)
                    continue
                return []
        
        return []
    
    def _parse_episodes_js(self, episodes_content, chapter_number):
        """
        Parse the episodes.js content to extract image URLs for a specific chapter.
        
        Args:
            episodes_content (str): Content of the episodes.js file
            chapter_number (int): Chapter number to extract
            
        Returns:
            list: List of image URLs for the chapter
        """
        try:
            if chapter_number is None:
                return []
            
            # Look for the variable corresponding to this chapter
            # Try both formats: "var eps123=" and "var eps123 ="
            chapter_var_formats = [
                f"var eps{chapter_number}=",
                f"var eps{chapter_number} ="
            ]
            
            start_pos = -1
            for var_format in chapter_var_formats:
                start_pos = episodes_content.find(var_format)
                if start_pos != -1:
                    break
            
            if start_pos == -1:
                if self.verbose:
                    print(f"📋 Chapter variable eps{chapter_number} not found")
                return []
            
            # Extract the array content
            start_bracket = episodes_content.find('[', start_pos)
            if start_bracket == -1:
                return []
            
            # Find the matching closing bracket
            bracket_count = 0
            end_bracket = start_bracket
            for i, char in enumerate(episodes_content[start_bracket:], start_bracket):
                if char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                    if bracket_count == 0:
                        end_bracket = i
                        break
            
            # Extract the array content
            array_content = episodes_content[start_bracket:end_bracket + 1]
            
            # Parse the JavaScript array to extract URLs
            # Remove brackets and split by comma
            content = array_content.strip('[]')
            if not content.strip():
                if self.verbose:
                    print(f"📋 Chapter {chapter_number} appears to be empty")
                return []
            
            # Split by comma and clean up the URLs
            urls = []
            for line in content.split(','):
                line = line.strip()
                if line.startswith("'") and line.endswith("'"):
                    url = line[1:-1]  # Remove quotes
                    if url and 'drive.google.com' in url:
                        urls.append(url)
            
            if self.verbose:
                print(f"📸 Extracted {len(urls)} image URLs from eps{chapter_number}")
                for i, url in enumerate(urls[:3], 1):  # Show first 3 URLs
                    print(f"   {i}. {url}")
                if len(urls) > 3:
                    print(f"   ... and {len(urls) - 3} more")
            
            return urls
            
        except Exception as e:
            print(f"❌ Error parsing episodes.js: {str(e)}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return []
    
    def cleanup_temp(self):
        """Remove temporary files"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                if self.verbose:
                    print("🧹 Cleaned up temporary files")
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Warning: Could not clean up temp files: {str(e)}")
