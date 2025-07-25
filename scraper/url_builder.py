"""
URL building utilities for anime-sama.fr
"""

import re
from urllib.parse import quote

class URLBuilder:
    BASE_URL = "https://anime-sama.fr"
    
    def build_chapter_url(self, manga_name, chapter_number):
        """
        Build a chapter URL in the format:
        https://anime-sama.fr/catalogue/{manga-name}/scan/vf/
        
        Args:
            manga_name (str): Name of the manga
            chapter_number (int): Chapter number
            
        Returns:
            str: Complete chapter URL
        """
        # Sanitize manga name for URL
        sanitized_name = self._sanitize_for_url(manga_name)
        
        # Build the base URL
        url = f"{self.BASE_URL}/catalogue/{sanitized_name}/scan/vf/"
        
        # Note: The chapter number might be handled by JavaScript on the page
        # or might need to be appended to the URL. We'll start with the base format
        # and let the scraper handle finding the specific chapter.
        
        return url
    
    def _sanitize_for_url(self, name):
        """
        Sanitize manga name for use in URL.
        Convert to lowercase, replace spaces with hyphens, remove special characters.
        
        Args:
            name (str): Original manga name
            
        Returns:
            str: Sanitized name suitable for URL
        """
        # Convert to lowercase
        name = name.lower()
        
        # Replace spaces and underscores with hyphens
        name = re.sub(r'[\s_]+', '-', name)
        
        # Remove special characters except hyphens and alphanumeric
        name = re.sub(r'[^a-z0-9\-]', '', name)
        
        # Remove multiple consecutive hyphens
        name = re.sub(r'-+', '-', name)
        
        # Remove leading/trailing hyphens
        name = name.strip('-')
        
        return name
    
    def sanitize_name(self, name):
        """
        Sanitize name for use as filename.
        
        Args:
            name (str): Original name
            
        Returns:
            str: Sanitized name suitable for filename
        """
        # Remove/replace characters that are invalid in filenames
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        
        # Replace spaces with underscores
        name = re.sub(r'\s+', '_', name)
        
        # Remove multiple consecutive underscores
        name = re.sub(r'_+', '_', name)
        
        # Remove leading/trailing underscores
        name = name.strip('_')
        
        return name
    
    def build_api_url(self, manga_name, chapter_number):
        """
        Build potential API URL for chapter data.
        This is speculative and might need adjustment based on actual API structure.
        
        Args:
            manga_name (str): Name of the manga
            chapter_number (int): Chapter number
            
        Returns:
            str: Potential API URL
        """
        sanitized_name = self._sanitize_for_url(manga_name)
        return f"{self.BASE_URL}/api/manga/{sanitized_name}/chapter/{chapter_number}"
    
    def extract_manga_name_from_url(self, url):
        """
        Extract manga name from anime-sama URL.
        
        Args:
            url (str): anime-sama URL
            
        Returns:
            str: Extracted manga name or None
        """
        pattern = r'/catalogue/([^/]+)/'
        match = re.search(pattern, url)
        if match:
            return match.group(1).replace('-', ' ')
        return None
