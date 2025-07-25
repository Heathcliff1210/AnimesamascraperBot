"""
HTTP headers and user agent utilities for anti-detection
"""

import random

def get_random_headers():
    """
    Get a random set of HTTP headers to avoid detection.
    Enhanced for cloud deployment environments.
    
    Returns:
        dict: Dictionary of HTTP headers
    """
    # User agents plus récents et plus variés
    user_agents = [
        # Chrome récent
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        
        # Firefox récent
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0',
        'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
        
        # Safari récent
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
        
        # Edge récent
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
    ]
    
    accept_languages = [
        'fr-FR,fr;q=0.9,en;q=0.8,de;q=0.7',
        'en-US,en;q=0.9,fr;q=0.8,es;q=0.7',
        'fr,en-US;q=0.9,en;q=0.8,it;q=0.7',
        'fr-FR,fr;q=0.8,en-US;q=0.5,en;q=0.3',
        'en-GB,en;q=0.9,fr;q=0.8,de;q=0.7'
    ]
    
    # Headers plus réalistes pour éviter la détection cloud
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': random.choice(accept_languages),
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    
    return headers

def get_image_headers(referer_url=None):
    """
    Get headers specifically for image requests.
    
    Args:
        referer_url (str): URL to use as referer
        
    Returns:
        dict: Dictionary of HTTP headers for image requests
    """
    base_headers = get_random_headers()
    
    image_headers = {
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site'
    }
    
    if referer_url:
        image_headers['Referer'] = referer_url
    
    # Update base headers with image-specific ones
    base_headers.update(image_headers)
    
    return base_headers

def rotate_user_agent():
    """
    Get a new random user agent string.
    
    Returns:
        str: Random user agent string
    """
    return get_random_headers()['User-Agent']
