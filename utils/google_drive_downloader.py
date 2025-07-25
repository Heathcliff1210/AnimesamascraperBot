#!/usr/bin/env python3
"""
Module spécialisé pour le téléchargement d'images depuis Google Drive
Intégré au système hybride de contournement
"""

import re
import requests
import time
import random
from urllib.parse import urlparse, parse_qs
from utils.beautiful_progress import BeautifulLogger

class GoogleDriveDownloader:
    """
    Téléchargeur spécialisé pour les images stockées sur Google Drive
    """
    
    def __init__(self, session, verbose=False):
        self.session = session
        self.verbose = verbose
        
        # Headers spécialisés pour Google Drive
        self.gdrive_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
    
    def is_google_drive_url(self, url):
        """
        Vérifie si l'URL est une URL Google Drive
        """
        return 'drive.google.com' in url or 'docs.google.com' in url
    
    def extract_file_id(self, drive_url):
        """
        Extrait l'ID de fichier depuis une URL Google Drive
        Supporte plusieurs formats d'URLs
        """
        # Format 1: https://drive.google.com/file/d/FILE_ID/view
        match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', drive_url)
        if match:
            return match.group(1)
        
        # Format 2: https://drive.google.com/open?id=FILE_ID
        match = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', drive_url)
        if match:
            return match.group(1)
        
        # Format 3: https://docs.google.com/uc?id=FILE_ID
        match = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', drive_url)
        if match:
            return match.group(1)
        
        # Format 4: Direct ID dans l'URL
        parsed = urlparse(drive_url)
        if parsed.path:
            path_parts = parsed.path.strip('/').split('/')
            for part in path_parts:
                if len(part) > 20 and re.match(r'^[a-zA-Z0-9_-]+$', part):
                    return part
        
        if self.verbose:
            BeautifulLogger.warning(f"Impossible d'extraire l'ID de: {drive_url}")
        return None
    
    def build_direct_download_url(self, file_id):
        """
        Construit l'URL de téléchargement direct Google Drive
        """
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    
    def build_view_url(self, file_id):
        """
        Construit l'URL de visualisation Google Drive (fallback)
        """
        return f"https://drive.google.com/file/d/{file_id}/view"
    
    def download_from_google_drive(self, drive_url, filepath, max_retries=5):
        """
        Télécharge une image depuis Google Drive avec plusieurs stratégies
        
        Args:
            drive_url (str): URL Google Drive
            filepath (str): Chemin local pour sauvegarder
            max_retries (int): Nombre max de tentatives
            
        Returns:
            bool: True si succès, False sinon
        """
        if not self.is_google_drive_url(drive_url):
            if self.verbose:
                BeautifulLogger.warning(f"URL non Google Drive: {drive_url}")
            return False
        
        file_id = self.extract_file_id(drive_url)
        if not file_id:
            if self.verbose:
                BeautifulLogger.error(f"Impossible d'extraire l'ID de fichier: {drive_url}")
            return False
        
        if self.verbose:
            BeautifulLogger.info(f"Téléchargement GDrive ID: {file_id}")
        
        # Stratégies de téléchargement dans l'ordre de priorité
        strategies = [
            ('direct_download', self.build_direct_download_url(file_id)),
            ('view_page', self.build_view_url(file_id)),
            ('original_url', drive_url)
        ]
        
        for attempt in range(max_retries):
            for strategy_name, url in strategies:
                try:
                    if self.verbose and attempt > 0:
                        BeautifulLogger.info(f"Tentative {attempt + 1}: {strategy_name}")
                    
                    success = self._attempt_download_strategy(url, filepath, strategy_name, file_id)
                    if success:
                        if self.verbose:
                            BeautifulLogger.success(f"Téléchargé via {strategy_name}")
                        return True
                
                except Exception as e:
                    if self.verbose:
                        BeautifulLogger.warning(f"Erreur {strategy_name}: {str(e)}")
                    continue
            
            # Délai entre tentatives
            if attempt < max_retries - 1:
                delay = random.uniform(2, 5)
                if self.verbose:
                    BeautifulLogger.info(f"Délai avant nouvelle tentative: {delay:.1f}s")
                time.sleep(delay)
        
        if self.verbose:
            BeautifulLogger.error(f"Échec téléchargement Google Drive: {file_id}")
        return False
    
    def _attempt_download_strategy(self, url, filepath, strategy_name, file_id):
        """
        Tente une stratégie de téléchargement spécifique
        """
        # Préparer les headers pour cette stratégie
        headers = self.gdrive_headers.copy()
        
        if strategy_name == 'direct_download':
            # Headers pour téléchargement direct
            headers['Referer'] = f'https://drive.google.com/file/d/{file_id}/view'
            
        elif strategy_name == 'view_page':
            # D'abord obtenir la page de visualisation pour extraire l'URL directe
            return self._download_via_view_page(url, filepath, file_id)
        
        # Mise à jour temporaire des headers de session
        original_headers = self.session.headers.copy()
        self.session.headers.update(headers)
        
        try:
            response = self.session.get(url, stream=True, timeout=30)
            
            # Vérifier si c'est une redirection vers une page de confirmation
            if 'accounts.google.com' in response.url or 'warning' in response.text.lower():
                if self.verbose:
                    BeautifulLogger.warning("Redirection vers page de confirmation détectée")
                return False
            
            # Vérifier si c'est du contenu binaire (image)
            content_type = response.headers.get('Content-Type', '')
            if not (content_type.startswith('image/') or 'application/octet-stream' in content_type):
                # Peut-être une page HTML, essayer d'extraire l'URL directe
                if response.status_code == 200 and len(response.content) < 50000:  # Petite page
                    return self._extract_direct_url_from_html(response.text, filepath, file_id)
            
            if response.status_code == 200:
                # Écrire le contenu
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Vérifier que le fichier a une taille raisonnable
                import os
                file_size = os.path.getsize(filepath)
                if file_size > 500:  # Au moins 500 bytes pour une image
                    return True
                else:
                    if self.verbose:
                        BeautifulLogger.warning(f"Fichier trop petit: {file_size} bytes")
                    os.remove(filepath)
                    return False
            
            return False
            
        except Exception as e:
            if self.verbose:
                BeautifulLogger.warning(f"Erreur téléchargement: {str(e)}")
            return False
        finally:
            # Restaurer les headers originaux
            self.session.headers = original_headers
    
    def _download_via_view_page(self, view_url, filepath, file_id):
        """
        Télécharge en passant par la page de visualisation pour extraire l'URL directe
        """
        original_headers = self.session.headers.copy()
        try:
            # Obtenir la page de visualisation
            headers = self.gdrive_headers.copy()
            self.session.headers.update(headers)
            
            response = self.session.get(view_url, timeout=20)
            
            if response.status_code == 200:
                # Chercher l'URL directe dans le HTML
                direct_url = self._extract_direct_url_from_html(response.text, filepath, file_id)
                return direct_url
            
            return False
            
        except Exception as e:
            if self.verbose:
                BeautifulLogger.warning(f"Erreur page de visualisation: {str(e)}")
            return False
        finally:
            self.session.headers = original_headers
    
    def _extract_direct_url_from_html(self, html_content, filepath, file_id):
        """
        Extrait l'URL de téléchargement direct depuis le HTML de Google Drive
        """
        try:
            # Patterns pour trouver l'URL directe
            patterns = [
                r'"downloadUrl":"([^"]+)"',
                r'&export=download&id=' + re.escape(file_id) + r'[^"]*',
                r'https://drive\.google\.com/uc\?export=download&id=' + re.escape(file_id),
                r'"([^"]*uc\?export=download[^"]*' + re.escape(file_id) + '[^"]*)"'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, html_content)
                for match in matches:
                    if 'export=download' in match and file_id in match:
                        # Nettoyer l'URL
                        clean_url = match.replace('\\u003d', '=').replace('\\u0026', '&')
                        
                        if self.verbose:
                            BeautifulLogger.info(f"URL directe extraite: {clean_url[:100]}...")
                        
                        # Télécharger avec cette URL
                        return self._attempt_download_strategy(clean_url, filepath, 'extracted_url', file_id)
            
            # Si aucune URL trouvée, essayer avec l'URL de base
            base_download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            return self._attempt_download_strategy(base_download_url, filepath, 'base_download', file_id)
            
        except Exception as e:
            if self.verbose:
                BeautifulLogger.warning(f"Erreur extraction URL: {str(e)}")
            return False