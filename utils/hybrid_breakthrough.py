#!/usr/bin/env python3
"""
Système hybride révolutionnaire combinant toutes les techniques
Rotation automatique des méthodes selon l'environnement et les échecs
"""

import requests
import time
import random
import os
from utils.beautiful_progress import BeautifulLogger
from utils.advanced_bypass import AdvancedAntiDetectionBypass
from utils.railway_bypass import RailwayOptimizedBypass
from utils.railway_enhanced_bypass import EnhancedRailwayBypass
from utils.google_drive_downloader import GoogleDriveDownloader

class HybridBreakthroughSystem:
    """
    Système hybride qui combine et fait tourner toutes les techniques
    """
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.is_railway = os.environ.get('RAILWAY_ENVIRONMENT') is not None
        
        # Initialiser tous les systèmes
        self.advanced_bypass = AdvancedAntiDetectionBypass(verbose=verbose)
        self.railway_bypass = RailwayOptimizedBypass(verbose=verbose)
        
        # État des tentatives
        self.last_successful_method = None
        self.method_failures = {
            'advanced': 0,
            'railway': 0,
            'direct': 0,
            'gdrive': 0
        }
        
        # Session principale pour Google Drive
        self.current_session = None
        
        # Stratégies selon échecs
        self.current_strategy = 'auto'
        
    def breakthrough_request(self, url, max_global_retries=9):
        """
        Requête avec rotation automatique des techniques
        """
        if self.verbose:
            BeautifulLogger.info("Démarrage système hybride révolutionnaire...", "🔥")
        
        # Stratégies à tester dans l'ordre
        strategies = self._get_strategies_order()
        
        for global_attempt in range(max_global_retries):
            if self.verbose:
                BeautifulLogger.info(f"Tentative globale {global_attempt + 1}/{max_global_retries}", "🎯")
            
            for strategy in strategies:
                try:
                    if self.verbose:
                        BeautifulLogger.info(f"Test stratégie: {strategy}", "🧪")
                    
                    # Tentative avec stratégie spécifique
                    response = self._attempt_strategy(url, strategy)
                    
                    if response and response.status_code == 200:
                        if self.verbose:
                            BeautifulLogger.success(f"Stratégie {strategy} réussie !")
                        
                        # Marquer succès et garder la session pour Google Drive
                        self.last_successful_method = strategy
                        self.method_failures[strategy] = 0
                        self.current_session = self._get_session_from_strategy(strategy)
                        return response
                    
                    else:
                        # Marquer échec
                        self.method_failures[strategy] += 1
                        if self.verbose:
                            BeautifulLogger.warning(f"Stratégie {strategy} échouée")
                
                except Exception as e:
                    if self.verbose:
                        BeautifulLogger.warning(f"Erreur stratégie {strategy}: {e}")
                    self.method_failures[strategy] += 1
            
            # Délai entre cycles complets
            if global_attempt < max_global_retries - 1:
                delay = random.uniform(3, 8)
                if self.verbose:
                    BeautifulLogger.info(f"Rotation cycle - Délai: {delay:.1f}s")
                time.sleep(delay)
        
        if self.verbose:
            BeautifulLogger.error("Toutes les stratégies hybrides ont échoué")
        return None
    
    def _get_strategies_order(self):
        """
        Détermine l'ordre des stratégies selon l'environnement et l'historique
        """
        base_strategies = ['advanced', 'railway', 'direct']
        
        # Si Railway, prioriser Railway
        if self.is_railway:
            strategies = ['railway', 'advanced', 'direct']
        else:
            strategies = ['advanced', 'railway', 'direct']
        
        # Réorganiser selon les succès passés
        if self.last_successful_method:
            strategies.remove(self.last_successful_method)
            strategies.insert(0, self.last_successful_method)
        
        # Réorganiser selon les échecs
        strategies.sort(key=lambda x: self.method_failures.get(x, 0))
        
        return strategies
    
    def _attempt_strategy(self, url, strategy):
        """
        Tenter une stratégie spécifique
        """
        if strategy == 'advanced':
            return self._attempt_advanced(url)
        elif strategy == 'railway':
            return self._attempt_railway(url)
        elif strategy == 'direct':
            return self._attempt_direct(url)
        else:
            return None
    
    def _attempt_advanced(self, url):
        """
        Tentative avec système avancé
        """
        try:
            # Recréer session si nécessaire
            self.advanced_bypass.create_stealth_session()
            return self.advanced_bypass.bypass_request(url, max_retries=2)
        except Exception as e:
            if self.verbose:
                BeautifulLogger.warning(f"Erreur advanced: {e}")
            return None
    
    def _attempt_railway(self, url):
        """
        Tentative avec système Railway
        """
        try:
            # Recréer session Railway
            self.railway_bypass.create_railway_session()
            return self.railway_bypass.railway_request(url, max_retries=2)
        except Exception as e:
            if self.verbose:
                BeautifulLogger.warning(f"Erreur railway: {e}")
            return None
    
    def _attempt_direct(self, url):
        """
        Tentative directe simplifiée
        """
        try:
            session = requests.Session()
            
            # Headers simples mais efficaces
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
            }
            
            session.headers.update(headers)
            
            # Requête simple
            response = session.get(url, timeout=(10, 30))
            return response if response.status_code == 200 else None
            
        except Exception as e:
            if self.verbose:
                BeautifulLogger.warning(f"Erreur direct: {e}")
            return None
    
    def _get_session_from_strategy(self, strategy):
        """
        Récupérer la session depuis une stratégie spécifique
        """
        if strategy == 'advanced':
            return getattr(self.advanced_bypass, 'session', None)
        elif strategy == 'railway':
            return getattr(self.railway_bypass, 'session', None)
        elif strategy == 'direct':
            return None  # Session temporaire, pas gardée
        return None

    def get_enhanced_session_for_gdrive(self):
        """
        Obtenir une session optimisée pour Google Drive
        """
        # Utiliser la dernière session réussie ou en créer une nouvelle
        if self.current_session:
            return self.current_session
        
        # Si pas de session, utiliser la méthode la plus fiable
        if self.last_successful_method == 'advanced':
            self.advanced_bypass.create_stealth_session()
            return getattr(self.advanced_bypass, 'session', None)
        elif self.last_successful_method == 'railway':
            self.railway_bypass.create_railway_session()
            return getattr(self.railway_bypass, 'session', None)
        
        # Fallback: créer une session basique
        import requests
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        session.headers.update(headers)
        self.current_session = session
        return session

    def download_from_google_drive(self, drive_url, filepath, max_retries=5):
        """
        Téléchargement Google Drive intégré au système hybride
        """
        if self.verbose:
            BeautifulLogger.info("Téléchargement Google Drive avec système hybride", "🔗")
        
        # Obtenir une session optimisée
        session = self.get_enhanced_session_for_gdrive()
        if not session:
            if self.verbose:
                BeautifulLogger.error("Impossible de créer session pour Google Drive")
            return False
        
        # Créer le téléchargeur Google Drive avec la session hybride
        gdrive_downloader = GoogleDriveDownloader(session, self.verbose)
        
        # Tentative de téléchargement
        success = gdrive_downloader.download_from_google_drive(drive_url, filepath, max_retries)
        
        if success:
            self.method_failures['gdrive'] = 0
            if self.verbose:
                BeautifulLogger.success("Google Drive téléchargé via système hybride")
        else:
            self.method_failures['gdrive'] += 1
            if self.verbose:
                BeautifulLogger.error("Échec Google Drive avec système hybride")
        
        return success

    def get_stats(self):
        """
        Statistiques du système hybride
        """
        return {
            'last_successful': self.last_successful_method,
            'failures': self.method_failures.copy(),
            'environment': 'railway' if self.is_railway else 'local',
            'has_gdrive_session': self.current_session is not None
        }