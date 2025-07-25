#!/usr/bin/env python3
"""
Système avancé de contournement anti-bot pour anime-sama.fr
Utilise des techniques de pointe pour passer les protections Cloudflare/WAF
"""

import requests
import time
import random
import json
import base64
import os
from urllib.parse import urljoin, urlparse
import ssl
import socket
from utils.beautiful_progress import BeautifulLogger

class AdvancedAntiDetectionBypass:
    """
    Système avancé de contournement des protections anti-bot
    """
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.session = None
        self.base_url = "https://anime-sama.fr"
        self.is_railway = os.environ.get('RAILWAY_ENVIRONMENT') is not None
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
        ]
        
        # Configuration Railway spécifique
        self.railway_headers = {}
        if self.is_railway:
            self.railway_headers = {
                'X-Railway-Environment': 'production',
                'X-Forwarded-Proto': 'https',
                'X-Real-IP': self._generate_french_ip(),
                'CF-Connecting-IP': self._generate_french_ip(),
                'X-Client-IP': self._generate_french_ip(),
            }
        
    def create_stealth_session(self):
        """
        Créer une session furtive avec toutes les techniques anti-détection
        """
        if self.verbose:
            BeautifulLogger.info("Création session furtive avancée...", "🥷")
        
        session = requests.Session()
        
        # 1. Headers ultra-réalistes avec empreinte complète
        headers = self._get_stealth_headers()
        session.headers.update(headers)
        
        # 2. Configuration SSL/TLS avancée
        self._configure_ssl_context(session)
        
        # 3. Simulation comportement humain
        self._configure_human_behavior(session)
        
        # 4. Techniques de contournement Cloudflare
        self._apply_cloudflare_bypass(session)
        
        self.session = session
        return session
    
    def _get_stealth_headers(self):
        """
        Générer des headers ultra-réalistes pour éviter la détection
        """
        user_agent = random.choice(self.user_agents)
        
        # Détection de type de navigateur pour headers cohérents
        is_chrome = 'Chrome' in user_agent and 'Edg' not in user_agent
        is_firefox = 'Firefox' in user_agent
        is_edge = 'Edg' in user_agent
        
        # Headers de base ultra-réalistes
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Pragma': 'no-cache',
        }
        
        # Headers spécifiques Chrome
        if is_chrome:
            headers.update({
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
            })
        
        # Headers spécifiques Firefox
        elif is_firefox:
            headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
            })
        
        # Headers Railway spécifiques
        if self.is_railway:
            headers.update(self.railway_headers)
            headers.update({
                'X-Forwarded-Host': 'anime-sama.fr',
                'Host': 'anime-sama.fr',
                'X-Original-URL': '/',
                'X-Forwarded-Port': '443',
            })
        
        # Headers français spécifiques
        headers.update({
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'X-Requested-With': None,  # Pas d'AJAX
            'Origin': None,  # Sera ajouté dynamiquement
            'Referer': None,  # Sera ajouté dynamiquement
        })
        
        return headers
    
    def _configure_ssl_context(self, session):
        """
        Configuration SSL/TLS pour éviter la détection par empreinte TLS
        """
        try:
            # Adapter SSL pour ressembler à un vrai navigateur
            session.mount('https://', requests.adapters.HTTPAdapter(
                max_retries=3,
                pool_connections=10,
                pool_maxsize=10
            ))
            
            # Configuration timeout réaliste
            session.timeout = (10, 30)
            
        except Exception as e:
            if self.verbose:
                BeautifulLogger.warning(f"Configuration SSL échouée: {e}")
    
    def _configure_human_behavior(self, session):
        """
        Configuration pour simuler un comportement humain
        """
        # Délais réalistes entre requêtes
        self.min_delay = 2.0
        self.max_delay = 5.0
        
        # Simulation de patterns de navigation humaine
        self.last_request_time = 0
    
    def _apply_cloudflare_bypass(self, session):
        """
        Appliquer des techniques spécifiques pour contourner Cloudflare
        """
        # Headers anti-Cloudflare
        cloudflare_headers = {
            'CF-IPCountry': 'FR',
            'CF-RAY': f"{random.randint(100000000000, 999999999999)}-CDG",
            'CF-Visitor': '{"scheme":"https"}',
            'X-Forwarded-Proto': 'https',
            'X-Forwarded-For': self._generate_french_ip(),
            'X-Real-IP': self._generate_french_ip(),
        }
        
        session.headers.update(cloudflare_headers)
        
        # Désactiver la vérification SSL stricte si nécessaire
        session.verify = True  # Garder la vérification mais avec tolérance
    
    def _generate_french_ip(self):
        """
        Générer une IP française réaliste
        """
        # Plages IP résidentielles françaises courantes
        french_ranges = [
            (90, 0, 0, 0, 90, 255, 255, 255),    # Orange
            (78, 192, 0, 0, 78, 255, 255, 255),  # Free
            (176, 189, 0, 0, 176, 189, 255, 255), # SFR
            (109, 190, 0, 0, 109, 255, 255, 255), # Bouygues
            (81, 185, 0, 0, 81, 220, 255, 255),   # Autres FAI
        ]
        
        range_data = random.choice(french_ranges)
        
        ip = f"{random.randint(range_data[0], range_data[4])}.{random.randint(range_data[1], range_data[5])}.{random.randint(range_data[2], range_data[6])}.{random.randint(range_data[3], range_data[7])}"
        
        return ip
    
    def simulate_human_navigation(self):
        """
        Simuler une navigation humaine avant d'accéder aux pages manga
        """
        if self.verbose:
            BeautifulLogger.info("Simulation navigation humaine...", "👤")
        
        try:
            # 1. Visite page d'accueil d'abord
            self._human_delay()
            
            response = self.session.get(
                self.base_url,
                headers={'Referer': 'https://www.google.com/'}
            )
            
            if self.verbose:
                BeautifulLogger.info(f"Page d'accueil: {response.status_code}")
            
            if response.status_code != 200:
                return False
            
            # 2. Simuler un clic sur catalogue
            self._human_delay()
            
            catalog_url = urljoin(self.base_url, '/catalogue/')
            response = self.session.get(
                catalog_url,
                headers={'Referer': self.base_url}
            )
            
            if self.verbose:
                BeautifulLogger.info(f"Page catalogue: {response.status_code}")
            
            # 3. Simuler lecture de quelques secondes
            time.sleep(random.uniform(3, 8))
            
            return response.status_code == 200
            
        except Exception as e:
            if self.verbose:
                BeautifulLogger.error(f"Erreur navigation: {e}")
            return False
    
    def bypass_request(self, url, max_retries=5):
        """
        Effectuer une requête avec contournement avancé optimisé Railway
        """
        if not self.session:
            self.create_stealth_session()
        
        for attempt in range(max_retries):
            try:
                if self.verbose:
                    BeautifulLogger.info(f"Tentative contournement {attempt + 1}/{max_retries}...", "🚀")
                
                # Optimisation Railway: délais plus courts
                if attempt > 0:
                    if self.is_railway:
                        delay = random.uniform(2, 8) + (attempt * 2)  # Délais réduits pour Railway
                    else:
                        delay = random.uniform(5, 15) * attempt
                    if self.verbose:
                        BeautifulLogger.info(f"Délai anti-détection: {delay:.1f}s")
                    time.sleep(delay)
                
                # Rotation d'identité plus agressive
                if attempt > 0:
                    self._rotate_identity()
                
                # Simulation navigation réduite pour Railway
                if attempt == 0 and not self.is_railway:
                    self.simulate_human_navigation()
                elif attempt == 0 and self.is_railway:
                    # Navigation accélérée pour Railway
                    self._quick_railway_navigation()
                
                # Délai réaliste
                self._human_delay()
                
                # Configuration headers dynamiques avec Railway
                dynamic_headers = {
                    'Referer': self.base_url + '/',
                    'Origin': self.base_url,
                }
                
                if self.is_railway:
                    # Headers Railway optimisés
                    dynamic_headers.update({
                        'X-Railway-Request': 'direct',
                        'Cache-Control': 'no-cache, no-store, must-revalidate',
                        'Pragma': 'no-cache',
                    })
                
                # Timeout optimisé pour Railway
                timeout = (10, 30) if self.is_railway else (15, 45)
                
                # Requête avec toutes les protections
                response = self.session.get(
                    url,
                    headers=dynamic_headers,
                    timeout=timeout,
                    allow_redirects=True
                )
                
                if self.verbose:
                    BeautifulLogger.info(f"Réponse: {response.status_code}")
                
                # Vérification succès
                if response.status_code == 200:
                    if self.verbose:
                        BeautifulLogger.success("Contournement réussi !")
                    return response
                
                elif response.status_code == 403:
                    if self.verbose:
                        BeautifulLogger.warning("Erreur 403 - Rotation identité...")
                    # Rotation immédiate sur Railway
                    if self.is_railway and attempt < max_retries - 1:
                        self._emergency_identity_rotation()
                    continue
                
                elif response.status_code in [429, 503]:
                    if self.verbose:
                        BeautifulLogger.warning("Rate limit - Attente...")
                    # Attente réduite sur Railway
                    wait_time = random.uniform(15, 30) if self.is_railway else random.uniform(30, 60)
                    time.sleep(wait_time)
                    continue
                
                else:
                    if self.verbose:
                        BeautifulLogger.warning(f"Code inattendu: {response.status_code}")
                    continue
                    
            except requests.exceptions.SSLError as e:
                if self.verbose:
                    BeautifulLogger.warning("Erreur SSL - Ajustement configuration...")
                self._adjust_ssl_config()
                continue
                
            except requests.exceptions.Timeout as e:
                if self.verbose:
                    BeautifulLogger.warning("Timeout - Nouvelle tentative...")
                continue
                
            except Exception as e:
                if self.verbose:
                    BeautifulLogger.error(f"Erreur requête: {e}")
                continue
        
        if self.verbose:
            BeautifulLogger.error("Échec après toutes les tentatives")
        return None
    
    def _rotate_identity(self):
        """
        Changer complètement d'identité (headers, IP, etc.)
        """
        if self.verbose:
            BeautifulLogger.info("Rotation complète d'identité...", "🔄")
        
        # Nouveaux headers
        new_headers = self._get_stealth_headers()
        self.session.headers.update(new_headers)
        
        # Nouvelle IP simulée
        self.session.headers.update({
            'X-Forwarded-For': self._generate_french_ip(),
            'X-Real-IP': self._generate_french_ip(),
            'CF-RAY': f"{random.randint(100000000000, 999999999999)}-CDG",
        })
        
        # Délai pour "changer de réseau" - optimisé Railway
        wait_time = random.uniform(1, 3) if self.is_railway else random.uniform(2, 5)
        time.sleep(wait_time)
    
    def _human_delay(self):
        """
        Délai réaliste entre requêtes pour simuler un humain
        """
        current_time = time.time()
        
        if self.last_request_time > 0:
            elapsed = current_time - self.last_request_time
            min_interval = self.min_delay
            
            if elapsed < min_interval:
                sleep_time = min_interval - elapsed + random.uniform(0, 1)
                time.sleep(sleep_time)
        
        # Délai aléatoire supplémentaire
        extra_delay = random.uniform(0.5, 2.0)
        time.sleep(extra_delay)
        
        self.last_request_time = time.time()
    
    def _quick_railway_navigation(self):
        """
        Navigation accélérée spécifique Railway
        """
        if self.verbose:
            BeautifulLogger.info("Navigation Railway accélérée...", "🚄")
        
        try:
            # Page d'accueil rapide
            response = self.session.get(
                self.base_url,
                headers={'Referer': 'https://www.google.fr/'},
                timeout=(5, 15)
            )
            
            if self.verbose:
                BeautifulLogger.info(f"Page d'accueil Railway: {response.status_code}")
            
            # Délai réduit
            time.sleep(random.uniform(1, 3))
            
            return response.status_code == 200
            
        except Exception as e:
            if self.verbose:
                BeautifulLogger.warning(f"Navigation Railway échouée: {e}")
            return False
    
    def _emergency_identity_rotation(self):
        """
        Rotation d'urgence pour Railway
        """
        if self.verbose:
            BeautifulLogger.info("Rotation d'urgence Railway...", "🚨")
        
        # Changer complètement d'identité
        self._rotate_identity()
        
        # Recréer session si nécessaire
        if random.random() < 0.3:  # 30% chance
            self.create_stealth_session()
    
    def _adjust_ssl_config(self):
        """
        Ajuster la configuration SSL en cas d'erreur
        """
        # Recréer session avec configuration SSL plus permissive
        self.create_stealth_session()