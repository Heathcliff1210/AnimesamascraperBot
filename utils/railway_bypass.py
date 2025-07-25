#!/usr/bin/env python3
"""
Système de contournement spécialement optimisé pour Railway
Résout les problèmes de timeout et erreurs 403 en production
"""

import requests
import time
import random
import os
from utils.beautiful_progress import BeautifulLogger

class RailwayOptimizedBypass:
    """
    Contournement ultra-optimisé pour Railway production
    """
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.session = None
        self.base_url = "https://anime-sama.fr"
        
        # Configuration Railway détectée
        self.is_railway = os.environ.get('RAILWAY_ENVIRONMENT') is not None
        
        # User agents légers pour Railway
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'
        ]
        
    def create_railway_session(self):
        """
        Session optimisée Railway avec maximum d'efficacité
        """
        if self.verbose:
            BeautifulLogger.info("Session Railway ultra-rapide...", "🚄")
        
        session = requests.Session()
        
        # Headers ultra-légers et efficaces
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        
        # Headers Railway spécifiques pour contourner détection
        if self.is_railway:
            french_ip = self._get_french_ip()
            headers.update({
                'X-Forwarded-For': french_ip,
                'X-Real-IP': french_ip,
                'X-Client-IP': french_ip,
                'CF-Connecting-IP': french_ip,
                'CF-IPCountry': 'FR',
                'X-Forwarded-Proto': 'https',
                'X-Railway-Bypass': 'enabled',
            })
        
        session.headers.update(headers)
        
        self.session = session
        return session
    
    def _get_french_ip(self):
        """
        IP française aléatoire optimisée
        """
        # Plages françaises courantes
        ranges = [
            (90, 0, 255, 255),    # Orange
            (78, 192, 255, 255),  # Free  
            (81, 185, 220, 255),  # Mix
        ]
        
        r = random.choice(ranges)
        return f"{random.randint(r[0], r[0])}.{random.randint(r[1], r[2])}.{random.randint(1, 254)}.{random.randint(1, 254)}"
    
    def railway_request(self, url, max_retries=5):
        """
        Requête ultra-optimisée Railway avec gestion avancée 403
        """
        if not self.session:
            self.create_railway_session()
        
        for attempt in range(max_retries):
            try:
                if self.verbose:
                    BeautifulLogger.info(f"Railway attempt {attempt + 1}/{max_retries}...", "🚄")
                
                # Délai progressif entre tentatives
                if attempt > 0:
                    wait = random.uniform(2, 5) + (attempt * 1.5)
                    if self.verbose:
                        BeautifulLogger.info(f"Délai anti-détection: {wait:.1f}s")
                    time.sleep(wait)
                
                # Rotation avancée sur échec ou erreur 403
                if attempt > 0:
                    self._advanced_railway_rotate()
                
                # Navigation furtive pour Railway
                if attempt == 0:
                    # Premier essai : navigation directe
                    if self.session:
                        response = self.session.get(url, timeout=(10, 30), allow_redirects=True)
                    else:
                        continue
                else:
                    # Essais suivants : avec navigation préalable
                    response = self._stealth_railway_request(url)
                
                if self.verbose:
                    BeautifulLogger.info(f"Railway réponse: {response.status_code}")
                
                if response.status_code == 200:
                    if self.verbose:
                        BeautifulLogger.success("Railway bypass réussi !")
                    return response
                
                elif response.status_code == 403:
                    if self.verbose:
                        BeautifulLogger.warning("403 détecté - Rotation complète d'identité...")
                    # Rotation complète sur 403
                    self.create_railway_session()
                    continue
                
                elif response.status_code in [429, 503]:
                    if self.verbose:
                        BeautifulLogger.warning("Rate limit - Attente prolongée...")
                    time.sleep(random.uniform(8, 15))
                    continue
                
            except requests.exceptions.Timeout:
                if self.verbose:
                    BeautifulLogger.warning("Timeout Railway - Session refresh...")
                self.create_railway_session()
                continue
                
            except Exception as e:
                if self.verbose:
                    BeautifulLogger.warning(f"Erreur Railway: {e}")
                continue
        
        if self.verbose:
            BeautifulLogger.error("Railway bypass échoué après toutes tentatives")
        return None
    
    def _advanced_railway_rotate(self):
        """
        Rotation avancée d'identité pour Railway
        """
        if not self.session:
            return
            
        # Nouveau user agent
        self.session.headers['User-Agent'] = random.choice(self.user_agents)
        
        # Nouvelle IP française
        if self.is_railway:
            new_ip = self._get_french_ip()
            self.session.headers.update({
                'X-Forwarded-For': new_ip,
                'X-Real-IP': new_ip,
                'CF-Connecting-IP': new_ip,
                'X-Client-IP': new_ip,
            })
        
        # Headers anti-détection supplémentaires
        additional_headers = {
            'Cache-Control': random.choice(['no-cache', 'max-age=0', 'no-store']),
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': random.choice(['none', 'same-origin']),
            'DNT': '1',
        }
        self.session.headers.update(additional_headers)
        
        # Délai anti-détection
        time.sleep(random.uniform(1, 3))
    
    def _stealth_railway_request(self, url):
        """
        Requête furtive avec navigation préalable pour Railway
        """
        if not self.session:
            return None
            
        try:
            # Étape 1: Accès page principale pour établir session
            base_response = self.session.get(
                self.base_url,
                timeout=(10, 30),
                allow_redirects=True
            )
            
            if base_response.status_code == 200:
                # Délai réaliste entre navigation
                time.sleep(random.uniform(1, 3))
                
                # Étape 2: Accès URL cible avec referer
                headers = {'Referer': self.base_url}
                response = self.session.get(
                    url,
                    headers=headers,
                    timeout=(10, 30),
                    allow_redirects=True
                )
                return response
            else:
                # Fallback: requête directe
                return self.session.get(url, timeout=(10, 30), allow_redirects=True)
                
        except Exception:
            # Fallback: requête directe si session existe toujours
            try:
                return self.session.get(url, timeout=(10, 30), allow_redirects=True)
            except Exception:
                return None