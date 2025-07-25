"""
Gestionnaire de proxies résidentiels simulés pour éviter la détection cloud
"""

import random
import time
import requests
from datetime import datetime, timedelta
import json
import os

class ResidentialProxyManager:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.current_identity = None
        self.identity_change_interval = 300  # 5 minutes
        self.last_identity_change = None
        
        # Pool d'identités résidentielles françaises réalistes
        self.residential_identities = [
            {
                'region': 'Paris',
                'isp': 'Orange',
                'ip_range': '90.{}.{}.{}',
                'timezone': 'Europe/Paris',
                'user_agents': [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'
                ],
                'accept_language': 'fr-FR,fr;q=0.9,en;q=0.8'
            },
            {
                'region': 'Lyon',
                'isp': 'Free',
                'ip_range': '78.{}.{}.{}',
                'timezone': 'Europe/Paris',
                'user_agents': [
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
                ],
                'accept_language': 'fr-FR,fr;q=0.8,en-US;q=0.5,en;q=0.3'
            },
            {
                'region': 'Marseille',
                'isp': 'SFR',
                'ip_range': '176.{}.{}.{}',
                'timezone': 'Europe/Paris',
                'user_agents': [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0'
                ],
                'accept_language': 'fr,en-US;q=0.9,en;q=0.8'
            },
            {
                'region': 'Toulouse',
                'isp': 'Bouygues',
                'ip_range': '109.{}.{}.{}',
                'timezone': 'Europe/Paris',
                'user_agents': [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
                    'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'
                ],
                'accept_language': 'fr-FR,fr;q=0.9,en;q=0.8,de;q=0.7'
            },
            {
                'region': 'Nantes',
                'isp': 'Orange',
                'ip_range': '81.{}.{}.{}',
                'timezone': 'Europe/Paris',
                'user_agents': [
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
                    'Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1'
                ],
                'accept_language': 'fr-FR,fr;q=0.9,en;q=0.8'
            }
        ]
        
        # Initialiser avec une identité aléatoire
        self._rotate_identity()
    
    def _rotate_identity(self):
        """Rotation automatique de l'identité résidentielle"""
        self.current_identity = random.choice(self.residential_identities)
        self.last_identity_change = datetime.now()
        
        if self.verbose:
            print(f"🏠 Nouvelle identité résidentielle: {self.current_identity['region']} ({self.current_identity['isp']})")
    
    def _should_rotate_identity(self):
        """Vérifie s'il faut changer d'identité"""
        if not self.last_identity_change:
            return True
        
        time_since_change = datetime.now() - self.last_identity_change
        return time_since_change.total_seconds() > self.identity_change_interval
    
    def _generate_residential_ip(self):
        """Génère une IP résidentielle française réaliste"""
        if not self.current_identity:
            return "192.168.1.100"  # Fallback
            
        ip_template = self.current_identity['ip_range']
        
        # Générer des octets réalistes pour une IP résidentielle
        octet2 = random.randint(1, 254)
        octet3 = random.randint(1, 254)
        octet4 = random.randint(2, 253)  # Éviter .1 et .254
        
        return ip_template.format(octet2, octet3, octet4)
    
    def get_residential_headers(self, target_url=None):
        """
        Génère des headers avec empreinte résidentielle française
        
        Args:
            target_url (str): URL cible pour contexte spécifique
            
        Returns:
            dict: Headers avec empreinte résidentielle
        """
        # Rotation automatique si nécessaire
        if self._should_rotate_identity():
            self._rotate_identity()
        
        # IP résidentielle simulée
        residential_ip = self._generate_residential_ip()
        
        # User agent de l'identité actuelle
        if not self.current_identity:
            self._rotate_identity()
        user_agent = random.choice(self.current_identity['user_agents'])
        
        # Headers de base avec empreinte résidentielle
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': self.current_identity.get('accept_language', 'fr-FR,fr;q=0.9,en;q=0.8'),
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            
            # Headers résidentiels pour masquer le cloud
            'X-Forwarded-For': residential_ip,
            'X-Real-IP': residential_ip,
            'X-Client-IP': residential_ip,
            'True-Client-IP': residential_ip,
            'CF-Connecting-IP': residential_ip,
            
            # Headers ISP français réalistes
            'X-ISP': self.current_identity.get('isp', 'Orange'),
            'X-Region': self.current_identity.get('region', 'Paris'),
            'X-Timezone': self.current_identity.get('timezone', 'Europe/Paris'),
        }
        
        # Headers Chrome spécifiques si Chrome UA
        if 'Chrome' in user_agent:
            chrome_version = user_agent.split('Chrome/')[1].split('.')[0]
            headers.update({
                'sec-ch-ua': f'"Google Chrome";v="{chrome_version}", "Chromium";v="{chrome_version}", "Not(A:Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"' if 'Windows' in user_agent else '"macOS"' if 'Mac' in user_agent else '"Linux"'
            })
        
        # Headers spécifiques pour anime-sama.fr
        if target_url and 'anime-sama.fr' in target_url:
            headers.update({
                'Origin': 'https://anime-sama.fr',
                'Referer': 'https://anime-sama.fr/',
                'Host': 'anime-sama.fr'
            })
        
        return headers
    
    def setup_residential_session(self, session):
        """
        Configure une session avec empreinte résidentielle complète
        
        Args:
            session (requests.Session): Session à configurer
            
        Returns:
            dict: Informations sur l'identité configurée
        """
        try:
            # Appliquer les headers résidentiels
            residential_headers = self.get_residential_headers()
            session.headers.clear()
            session.headers.update(residential_headers)
            
            # Configuration réseau résidentielle
            # Timeout plus long pour simuler connexion résidentielle
            session.timeout = (10, 60)
            
            # Configuration session sans cookies - uniquement headers résidentiels
            
            if self.verbose:
                print(f"🏠 Session configurée avec identité résidentielle:")
                print(f"   📍 Région: {self.current_identity.get('region', 'Paris')}")
                print(f"   🌐 ISP: {self.current_identity.get('isp', 'Orange')}")
                print(f"   🔗 IP simulée: {residential_headers['X-Real-IP']}")
            
            return {
                'region': self.current_identity.get('region', 'Paris'),
                'isp': self.current_identity.get('isp', 'Orange'),
                'ip': residential_headers['X-Real-IP'],
                'user_agent': residential_headers['User-Agent']
            }
            
        except Exception as e:
            if self.verbose:
                print(f"❌ Erreur configuration résidentielle: {str(e)}")
            return None
    
    def add_residential_delays(self):
        """Ajoute des délais réalistes de connexion résidentielle"""
        # Délai variable selon l'ISP (simulation réaliste)
        isp_delays = {
            'Orange': (0.5, 2.0),
            'Free': (0.8, 3.0),
            'SFR': (0.6, 2.5),
            'Bouygues': (0.7, 2.8)
        }
        
        isp_name = self.current_identity.get('isp', 'Orange') if self.current_identity else 'Orange'
        min_delay, max_delay = isp_delays.get(isp_name, (0.5, 2.0))
        
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        
        return delay
    
    def simulate_residential_behavior(self, session, target_url):
        """
        Simule un comportement de navigation résidentielle
        
        Args:
            session (requests.Session): Session configurée
            target_url (str): URL cible
            
        Returns:
            bool: True si simulation réussie
        """
        try:
            if self.verbose:
                print("🏠 Simulation comportement résidentiel...")
            
            # Délai résidentiel réaliste
            self.add_residential_delays()
            
            # Effectuer une requête de "pré-visite" comme un vrai utilisateur
            try:
                response = session.get('https://anime-sama.fr/', timeout=30)
                if response.status_code == 200:
                    if self.verbose:
                        print("✅ Pré-visite résidentielle réussie")
                    
                    # Délai de lecture simulé
                    time.sleep(random.uniform(1.0, 3.0))
                    return True
                    
            except Exception as e:
                if self.verbose:
                    print(f"⚠️ Pré-visite échouée: {str(e)}")
            
            return False
            
        except Exception as e:
            if self.verbose:
                print(f"❌ Erreur simulation résidentielle: {str(e)}")
            return False
    
    def get_identity_stats(self):
        """Retourne les statistiques de l'identité actuelle"""
        return {
            'current_identity': self.current_identity,
            'last_change': self.last_identity_change,
            'next_rotation_in': max(0, self.identity_change_interval - 
                                   (datetime.now() - self.last_identity_change).total_seconds()) if self.last_identity_change else 0
        }

class RailwayOptimizer:
    """Optimiseur spécifique pour Railway deployment"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.railway_config = self._detect_railway_environment()
    
    def _detect_railway_environment(self):
        """Détecte et extrait la configuration Railway"""
        config = {
            'is_railway': bool(os.getenv('RAILWAY_ENVIRONMENT')),
            'project_id': os.getenv('RAILWAY_PROJECT_ID'),
            'service_id': os.getenv('RAILWAY_SERVICE_ID'),
            'environment': os.getenv('RAILWAY_ENVIRONMENT', 'production'),
            'port': int(os.getenv('PORT', 5000)),
            'public_domain': os.getenv('RAILWAY_PUBLIC_DOMAIN'),
            'static_url': os.getenv('RAILWAY_STATIC_URL'),
            'region': os.getenv('RAILWAY_REGION', 'us-west1')
        }
        
        if self.verbose and config['is_railway']:
            print(f"🚂 Environment Railway détecté:")
            print(f"   🆔 Project: {config['project_id']}")
            print(f"   🔧 Service: {config['service_id']}")
            print(f"   🌍 Region: {config['region']}")
            print(f"   🔌 Port: {config['port']}")
        
        return config
    
    def get_railway_optimized_headers(self):
        """Headers optimisés pour Railway"""
        headers = {}
        
        if self.railway_config['is_railway']:
            # Headers Railway spécifiques
            headers.update({
                'X-Railway-Project': self.railway_config['project_id'] or 'unknown',
                'X-Railway-Service': self.railway_config['service_id'] or 'unknown',
                'X-Railway-Environment': self.railway_config['environment'],
                'X-Forwarded-Proto': 'https',
                'X-Forwarded-Host': self.railway_config['public_domain'] or 'localhost'
            })
            
            # Masquer l'origine Railway avec headers résidentiels
            headers.update({
                'X-Forwarded-For': f"92.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
                'X-Real-IP': f"82.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
                'Via': f"1.1 proxy-{random.randint(1000,9999)}.fr.orange.net"
            })
        
        return headers
    
    def configure_for_railway(self, session):
        """Configure la session pour Railway"""
        if not self.railway_config['is_railway']:
            return False
        
        try:
            railway_headers = self.get_railway_optimized_headers()
            session.headers.update(railway_headers)
            
            # Configuration réseau Railway
            session.timeout = (15, 90)  # Timeouts plus longs pour Railway
            
            if self.verbose:
                print("🚂 Session optimisée pour Railway")
            
            return True
            
        except Exception as e:
            if self.verbose:
                print(f"❌ Erreur configuration Railway: {str(e)}")
            return False
    
    def get_railway_port(self):
        """Retourne le port Railway configuré"""
        return self.railway_config['port']
    
    def is_railway_environment(self):
        """Vérifie si on est sur Railway"""
        return self.railway_config['is_railway']