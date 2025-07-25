#!/usr/bin/env python3
"""
Système de contournement Railway ultra-avancé
Version finale avec toutes les techniques anti-détection pour production
"""

import requests
import time
import random
import os
import json
from utils.beautiful_progress import BeautifulLogger

class EnhancedRailwayBypass:
    """
    Contournement Railway de nouvelle génération
    Combine toutes les techniques pour maximiser les chances de succès
    """
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.session = None
        self.base_url = "https://anime-sama.fr"
        
        # Détection environnement Railway/Cloud
        self.is_railway = self._detect_cloud_environment()
        
        # Pool d'user agents ultra-récents
        self.modern_user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15'
        ]
        
        # Pools d'IPs résidentielles françaises par ISP
        self.french_ip_pools = {
            'orange': [(90, 0, 255), (81, 185, 255), (82, 250, 255)],
            'free': [(78, 192, 255), (78, 33, 255), (78, 245, 255)],
            'sfr': [(109, 190, 255), (109, 23, 255), (176, 161, 255)],
            'bouygues': [(109, 229, 255), (88, 127, 255), (77, 201, 255)]
        }
        
        self.current_isp = None
        self.request_count = 0
        self.last_ip_change = 0
        
    def _detect_cloud_environment(self):
        """Détection avancée de l'environnement cloud"""
        cloud_indicators = [
            'RAILWAY_ENVIRONMENT',
            'RENDER',
            'HEROKU_APP_NAME',
            'VERCEL',
            'NETLIFY',
            'PORT'  # Variable commune aux déploiements cloud
        ]
        
        for indicator in cloud_indicators:
            if os.environ.get(indicator):
                if self.verbose:
                    BeautifulLogger.info(f"☁️ Environnement cloud détecté: {indicator}")
                return True
        return False
    
    def _get_realistic_french_ip(self):
        """Génère une IP française réaliste selon ISP"""
        # Changer d'ISP toutes les 10 requêtes ou toutes les 5 minutes
        if (self.request_count % 10 == 0 or 
            time.time() - self.last_ip_change > 300):
            self.current_isp = random.choice(list(self.french_ip_pools.keys()))
            self.last_ip_change = time.time()
        
        if not self.current_isp:
            self.current_isp = 'orange'  # Default
        
        # Sélectionner une plage IP pour cet ISP
        ip_ranges = self.french_ip_pools[self.current_isp]
        base_range = random.choice(ip_ranges)
        
        # Générer IP dans cette plage
        ip = f"{base_range[0]}.{random.randint(1, base_range[1])}.{random.randint(1, 254)}.{random.randint(1, 254)}"
        return ip, self.current_isp
    
    def create_stealth_session(self):
        """Crée une session ultra-furtive avec empreinte résidentielle"""
        if self.verbose:
            BeautifulLogger.info("🥷 Création session furtive Railway...", "🔧")
        
        session = requests.Session()
        
        # User agent moderne aléatoire
        user_agent = random.choice(self.modern_user_agents)
        ip, isp = self._get_realistic_french_ip()
        
        # Headers de base ultra-réalistes
        base_headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Sec-GPC': '1'
        }
        
        # Headers Chrome/Edge spécifiques
        if 'Chrome' in user_agent:
            base_headers.update({
                'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"' if 'Windows' in user_agent else '"macOS"'
            })
        
        # Headers cloud spécifiques si détecté
        if self.is_railway:
            cloud_headers = {
                'X-Forwarded-For': ip,
                'X-Real-IP': ip,
                'X-Client-IP': ip,
                'CF-Connecting-IP': ip,
                'CF-IPCountry': 'FR',
                'CF-RAY': f"{random.randint(100000000000, 999999999999)}-CDG",
                'X-Forwarded-Proto': 'https',
                'X-Forwarded-Host': 'anime-sama.fr',
                'X-Original-Forwarded-For': ip,
                'True-Client-IP': ip,
                'X-Cluster-Client-IP': ip,
                'Via': f'1.1 {isp}-proxy-{random.randint(1000, 9999)}.fr'
            }
            base_headers.update(cloud_headers)
            
            if self.verbose:
                BeautifulLogger.info(f"🌍 IP simulée: {ip} ({isp.upper()})")
        
        session.headers.update(base_headers)
        self.session = session
        self.request_count += 1
        
        return session
    
    def railway_stealth_request(self, url, max_retries=7):
        """
        Requête furtive Railway avec stratégies multiples
        """
        strategies = [
            self._strategy_direct,
            self._strategy_with_navigation,
            self._strategy_with_delay,
            self._strategy_new_session,
            self._strategy_ultimate_stealth
        ]
        
        for attempt in range(max_retries):
            try:
                if self.verbose:
                    BeautifulLogger.info(f"🎯 Railway Attempt {attempt + 1}/{max_retries}", "🚄")
                
                # Sélectionner stratégie basée sur l'attempt
                strategy_index = min(attempt, len(strategies) - 1)
                strategy = strategies[strategy_index]
                
                # Créer/renouveler session si nécessaire
                if not self.session or attempt > 0:
                    self.create_stealth_session()
                
                # Exécuter stratégie
                response = strategy(url, attempt)
                
                if response and response.status_code == 200:
                    if self.verbose:
                        BeautifulLogger.success(f"✅ Railway bypass réussi (stratégie {strategy_index + 1})")
                    return response
                
                elif response and response.status_code == 403:
                    if self.verbose:
                        BeautifulLogger.warning(f"🚫 403 Forbidden - Changement complet d'identité...")
                    
                    # Forcer renouvellement complet
                    self.session = None
                    self._rotate_complete_identity()
                    time.sleep(random.uniform(3, 8))
                    continue
                
                elif response and response.status_code in [429, 503]:
                    if self.verbose:
                        BeautifulLogger.warning(f"⏳ Rate limit détecté - Pause prolongée...")
                    time.sleep(random.uniform(10, 20))
                    continue
                
                else:
                    if self.verbose and response:
                        BeautifulLogger.warning(f"⚠️ Status {response.status_code} - Retry...")
                    
                    # Délai progressif
                    wait_time = random.uniform(2, 5) + (attempt * 2)
                    time.sleep(wait_time)
                    continue
                    
            except requests.exceptions.Timeout:
                if self.verbose:
                    BeautifulLogger.warning("⏰ Timeout Railway - Session refresh...")
                self.session = None
                continue
                
            except Exception as e:
                if self.verbose:
                    BeautifulLogger.warning(f"❌ Erreur: {e}")
                continue
        
        if self.verbose:
            BeautifulLogger.error("💥 Railway bypass échoué après toutes tentatives")
        return None
    
    def _strategy_direct(self, url, attempt):
        """Stratégie 1: Requête directe optimisée"""
        return self.session.get(url, timeout=(15, 45), allow_redirects=True)
    
    def _strategy_with_navigation(self, url, attempt):
        """Stratégie 2: Navigation préalable"""
        # Visite page d'accueil
        home_response = self.session.get(self.base_url, timeout=(15, 45))
        if home_response.status_code == 200:
            time.sleep(random.uniform(1.5, 4))
            
            # Requête cible avec referer
            headers = {'Referer': self.base_url}
            return self.session.get(url, headers=headers, timeout=(15, 45))
        
        # Fallback
        return self.session.get(url, timeout=(15, 45))
    
    def _strategy_with_delay(self, url, attempt):
        """Stratégie 3: Avec délais réalistes"""
        # Navigation lente et réaliste
        time.sleep(random.uniform(2, 5))
        
        # Requête avec headers supplémentaires
        headers = {
            'Referer': self.base_url,
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        return self.session.get(url, headers=headers, timeout=(15, 45))
    
    def _strategy_new_session(self, url, attempt):
        """Stratégie 4: Nouvelle session complète"""
        self.create_stealth_session()
        time.sleep(random.uniform(1, 3))
        return self.session.get(url, timeout=(15, 45))
    
    def _strategy_ultimate_stealth(self, url, attempt):
        """Stratégie 5: Mode furtivité ultime"""
        # Nouvelle session avec rotation complète
        self.create_stealth_session()
        
        # Navigation ultra-réaliste
        try:
            # Étape 1: Page d'accueil
            home = self.session.get(self.base_url, timeout=(15, 45))
            time.sleep(random.uniform(2, 4))
            
            # Étape 2: Page catalogue (si possible)
            catalogue_url = f"{self.base_url}/catalogue/"
            catalogue = self.session.get(catalogue_url, 
                                       headers={'Referer': self.base_url}, 
                                       timeout=(15, 45))
            time.sleep(random.uniform(1.5, 3))
            
            # Étape 3: URL cible finale
            headers = {
                'Referer': catalogue_url if catalogue.status_code == 200 else self.base_url,
                'Cache-Control': 'max-age=0',
                'Sec-Fetch-Site': 'same-origin'
            }
            return self.session.get(url, headers=headers, timeout=(15, 45))
            
        except Exception:
            # Fallback ultime
            return self.session.get(url, timeout=(15, 45))
    
    def _rotate_complete_identity(self):
        """Rotation complète d'identité résidentielle"""
        # Forcer changement d'ISP
        self.current_isp = None
        self.last_ip_change = 0
        self.request_count = 0
        
        if self.verbose:
            BeautifulLogger.info("🔄 Rotation identité résidentielle complète")
    
    def get_enhanced_stats(self):
        """Statistiques détaillées du système"""
        return {
            'environment': 'Railway/Cloud' if self.is_railway else 'Local',
            'current_isp': self.current_isp or 'Aucun',
            'request_count': self.request_count,
            'session_active': self.session is not None,
            'available_strategies': 5
        }