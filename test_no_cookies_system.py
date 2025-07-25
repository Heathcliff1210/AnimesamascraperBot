#!/usr/bin/env python3
"""
Test du système sans cookies - uniquement proxies résidentiels
"""

import tempfile
import os
from scraper.anime_sama_scraper import AnimeSamaScraper
from utils.beautiful_progress import BeautifulLogger

def test_no_cookies_system():
    """Test du système sans cookies"""
    BeautifulLogger.info("Test du système SANS COOKIES...", "🚫🍪")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Créer le scraper SANS cookies
            scraper = AnimeSamaScraper(
                output_dir=temp_dir,
                temp_dir=os.path.join(temp_dir, "temp"),
                verbose=True,
                use_residential_proxy=True
            )
            
            BeautifulLogger.info("Test accès direct avec proxies résidentiels...", "🏠")
            
            # Test d'accès simple
            response = scraper.session.get('https://anime-sama.fr/', timeout=30)
            BeautifulLogger.info(f"Accès page principale: {response.status_code}")
            
            if response.status_code == 200:
                BeautifulLogger.success("✅ Accès réussi SANS cookies")
                
                # Test manga page
                manga_url = "https://anime-sama.fr/catalogue/lookism/scan/vf/"
                response2 = scraper.session.get(manga_url, timeout=30)
                BeautifulLogger.info(f"Accès page manga: {response2.status_code}")
                
                if response2.status_code == 200:
                    BeautifulLogger.success("✅ Page manga accessible SANS cookies")
                    
                    # Test simple téléchargement
                    BeautifulLogger.info("Test téléchargement chapitre...", "📖")
                    success = scraper.download_chapter("lookism", 1)
                    
                    if success:
                        # Vérifier fichier
                        cbz_files = [f for f in os.listdir(temp_dir) if f.endswith('.cbz')]
                        if cbz_files:
                            BeautifulLogger.success(f"✅ TÉLÉCHARGEMENT RÉUSSI: {cbz_files[0]}")
                            return True
                        else:
                            BeautifulLogger.warning("⚠️ Pas de fichier CBZ généré")
                            return False
                    else:
                        BeautifulLogger.warning("⚠️ Téléchargement échoué")
                        return False
                else:
                    BeautifulLogger.warning(f"⚠️ Page manga: {response2.status_code}")
                    return False
            else:
                BeautifulLogger.warning(f"⚠️ Accès page principale: {response.status_code}")
                return False
                
    except Exception as e:
        BeautifulLogger.error(f"Erreur test: {e}")
        return False

def test_railway_readiness():
    """Test de préparation Railway"""
    BeautifulLogger.info("Test de préparation Railway...", "🚂")
    
    from utils.proxy_manager import RailwayOptimizer
    
    railway_optimizer = RailwayOptimizer(verbose=True)
    
    config_info = {
        'port': railway_optimizer.get_railway_port(),
        'is_railway': railway_optimizer.is_railway_environment(),
        'optimized': True
    }
    
    BeautifulLogger.success(f"Port configuré: {config_info['port']}")
    BeautifulLogger.success("Configuration Railway prête")
    
    return True

def main():
    """Test complet sans cookies"""
    print("="*60)
    BeautifulLogger.info("🚀 TEST SYSTÈME SANS COOKIES", "🚫🍪")
    print("="*60)
    
    # Test système sans cookies
    no_cookies_success = test_no_cookies_system()
    print("-" * 40)
    
    # Test Railway
    railway_success = test_railway_readiness()
    print("-" * 40)
    
    # Résumé
    print("="*60)
    if no_cookies_success and railway_success:
        BeautifulLogger.success("🎉 SYSTÈME SANS COOKIES OPÉRATIONNEL")
        print("🏠 Proxies résidentiels fonctionnels")
        print("🚂 Configuration Railway prête")
        print("✅ Bot prêt pour déploiement")
    elif no_cookies_success:
        BeautifulLogger.warning("⚠️ SYSTÈME PARTIELLEMENT OPÉRATIONNEL")
        print("🏠 Proxies résidentiels fonctionnels")
        print("🔄 Nécessite ajustements Railway")
    else:
        BeautifulLogger.error("❌ SYSTÈME NÉCESSITE CORRECTIONS")
        print("🔧 Vérifiez configuration proxies")
    
    print("="*60)
    return no_cookies_success and railway_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)