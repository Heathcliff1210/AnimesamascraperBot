"""
Image downloading utilities with anti-detection measures
Enhanced with Google Drive support
"""

import os
import time
import requests
from urllib.parse import urlparse
import random
from utils.google_drive_downloader import GoogleDriveDownloader

class ImageDownloader:
    def __init__(self, session, verbose=False, scraper_instance=None):
        self.session = session
        self.verbose = verbose
        self.scraper_instance = scraper_instance  # Reference to main scraper for session refresh
        self.download_delays = [0.3, 0.5, 0.7, 1.0]  # Random delays
        
        # Initialiser le téléchargeur Google Drive
        self.gdrive_downloader = GoogleDriveDownloader(session, verbose)
        
    def download_image(self, url, filepath, max_retries=5):
        """
        Download an image from URL to filepath.
        Enhanced with Google Drive support and cloud deployment environments.
        
        Args:
            url (str): Image URL (supports Google Drive)
            filepath (str): Local file path to save image
            max_retries (int): Maximum number of retry attempts
            
        Returns:
            bool: True if successful, False otherwise
        """
        import os
        
        # Vérifier si c'est une URL Google Drive
        if self.gdrive_downloader.is_google_drive_url(url):
            if self.verbose:
                print(f"   🔗 Détection Google Drive: {os.path.basename(filepath)}")
            
            # Utiliser le téléchargeur Google Drive spécialisé
            success = self.gdrive_downloader.download_from_google_drive(url, filepath, max_retries)
            
            if success:
                return True
            else:
                if self.verbose:
                    print(f"   ⚠️ Échec Google Drive, tentative téléchargement standard...")
                # Fallback vers téléchargement standard si GDrive échoue
        
        # Téléchargement standard pour URLs non-Google Drive ou fallback
        cloud_env = os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('DYNO') or os.getenv('RENDER')
        
        for attempt in range(max_retries):
            try:
                if self.verbose and attempt > 0:
                    print(f"   🔄 Retry attempt {attempt + 1} for {os.path.basename(filepath)}")
                
                # Add some randomization to headers for this request
                headers = self.session.headers.copy()
                headers['Referer'] = self._get_referer_from_url(url)
                
                # Headers supplémentaires pour éviter le blocage cloud
                if cloud_env:
                    headers.update({
                        'Cache-Control': 'no-cache',
                        'Pragma': 'no-cache',
                        'Sec-Fetch-Dest': 'image',
                        'Sec-Fetch-Mode': 'no-cors',
                        'Sec-Fetch-Site': 'cross-site'
                    })
                
                # Délai plus long pour les environnements cloud
                if attempt > 0:
                    delay = (1.5 if cloud_env else 0.5) * (attempt + 1)
                    if self.verbose:
                        print(f"   ⏳ Attente de {delay:.1f}s avant nouvelle tentative...")
                    time.sleep(delay)
                
                # Make the request
                response = self.session.get(
                    url, 
                    headers=headers,
                    timeout=45 if cloud_env else 30,
                    stream=True
                )
                response.raise_for_status()
                
                # Check if the response is actually an image
                content_type = response.headers.get('content-type', '')
                if not self._is_image_content_type(content_type):
                    if self.verbose:
                        print(f"   ⚠️  Warning: URL may not be an image: {content_type}")
                
                # Save the image
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Verify the file was created and has content
                if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                    if self.verbose:
                        file_size = os.path.getsize(filepath)
                        print(f"   ✅ Downloaded {os.path.basename(filepath)} ({file_size} bytes)")
                    return True
                else:
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    raise Exception("Downloaded file is empty")
                    
            except requests.RequestException as e:
                if self.verbose:
                    error_msg = str(e)
                    if "403" in error_msg or "Forbidden" in error_msg:
                        print(f"   🚫 Accès refusé (403) pour {os.path.basename(filepath)} - Rotation des headers...")
                        # Renouveler complètement les headers sur erreur 403
                        from utils.headers import get_random_headers
                        self.session.headers.update(get_random_headers())
                    else:
                        print(f"   ❌ Erreur réseau pour {os.path.basename(filepath)}: {error_msg}")
                
                if attempt < max_retries - 1:
                    # Handle 403 errors with session refresh
                    if "403" in str(e) or "Forbidden" in str(e):
                        if self.scraper_instance and hasattr(self.scraper_instance, 'refresh_session_on_block'):
                            if self.verbose:
                                print(f"   🔄 Erreur 403 détectée, renouvellement de la session...")
                            self.scraper_instance.refresh_session_on_block()
                            self.session = self.scraper_instance.session  # Update session reference
                            # Mettre à jour la session du téléchargeur Google Drive aussi
                            self.gdrive_downloader.session = self.session
                        delay = (3.0 if cloud_env else 2.0) * (attempt + 2)
                    else:
                        delay = random.choice(self.download_delays) * (attempt + 1)
                    
                    if self.verbose:
                        print(f"   ⏳ Nouvelle tentative dans {delay:.1f}s...")
                    time.sleep(delay)
                    continue
                    
            except Exception as e:
                if self.verbose:
                    print(f"   ❌ Error downloading {os.path.basename(filepath)}: {str(e)}")
                
                if attempt < max_retries - 1:
                    delay = random.choice(self.download_delays) * (attempt + 1)
                    time.sleep(delay)
                    continue
        
        return False
    
    def _get_referer_from_url(self, url):
        """
        Generate an appropriate referer header from the image URL.
        
        Args:
            url (str): Image URL
            
        Returns:
            str: Referer URL
        """
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    
    def _is_image_content_type(self, content_type):
        """
        Check if the content type indicates an image.
        
        Args:
            content_type (str): HTTP Content-Type header value
            
        Returns:
            bool: True if content type is an image
        """
        image_types = [
            'image/jpeg',
            'image/jpg', 
            'image/png',
            'image/gif',
            'image/webp',
            'image/bmp'
        ]
        
        return any(img_type in content_type.lower() for img_type in image_types)
    
    def verify_image_file(self, filepath):
        """
        Verify that a downloaded file is a valid image.
        
        Args:
            filepath (str): Path to the image file
            
        Returns:
            bool: True if file appears to be a valid image
        """
        try:
            if not os.path.exists(filepath):
                return False
            
            if os.path.getsize(filepath) == 0:
                return False
            
            # Read first few bytes to check for image signatures
            with open(filepath, 'rb') as f:
                header = f.read(16)
            
            # Check for common image file signatures
            signatures = {
                b'\xff\xd8\xff': 'JPEG',
                b'\x89PNG\r\n\x1a\n': 'PNG',
                b'GIF87a': 'GIF',
                b'GIF89a': 'GIF',
                b'RIFF': 'WEBP',  # WEBP files start with RIFF
                b'BM': 'BMP'
            }
            
            for sig, format_name in signatures.items():
                if header.startswith(sig):
                    return True
            
            # If no signature matches, it might still be a valid image
            # but we'll be less confident
            return True
            
        except Exception:
            return False
