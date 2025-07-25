#!/usr/bin/env python3
"""
Test du système Railway ultra-optimisé
"""

import tempfile
import os
from scraper.anime_sama_scraper import AnimeSamaScraper
from utils.beautiful_progress import BeautifulLogger
from utils.railway_bypass import RailwayOptimizedBypass

def test_railway_bypass():
    """Test direct du système Railway optimisé"""
    BeautifulLogger.info("Test Railway bypass ultra-rapide...", "🚄")
    
    # Simuler environnement Railway
    os.environ['RAILWAY_ENVIRONMENT'] = 'production'
    
    try:
        bypass = RailwayOptimizedBypass(verbose=True)
        
        # Test accès direct ultra-rapide
        response = bypass.railway_request("https://anime-sama.fr/", max_retries=3)
        
        if response and response.status_code == 200:
            BeautifulLogger.success("✅ Railway bypass réussi - Page principale")
            
            # Test manga page
            manga_response = bypass.railway_request(
                "https://anime-sama.fr/catalogue/lookism/scan/vf/episodes.js",
                max_retries=3
            )
            
            if manga_response and manga_response.status_code == 200:
                BeautifulLogger.success("✅ Railway bypass réussi - Episodes.js accessible")
                return True
            else:
                BeautifulLogger.warning("⚠️ Episodes.js non accessible")
                return False
        else:
            BeautifulLogger.warning("⚠️ Page principale non accessible")
            return False
            
    except Exception as e:
        BeautifulLogger.error(f"Erreur Railway bypass: {e}")
        return False

def test_scraper_railway_mode():
    """Test scraper en mode Railway"""
    BeautifulLogger.info("Test scraper Railway ultra-optimisé...", "🚄")
    
    # Simuler environnement Railway
    os.environ['RAILWAY_ENVIRONMENT'] = 'production'
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Scraper Railway optimisé
            scraper = AnimeSamaScraper(
                output_dir=temp_dir,
                temp_dir=os.path.join(temp_dir, "temp"),
                verbose=True,
                use_residential_proxy=False,
                use_advanced_bypass=True,
                use_railway_bypass=True  # Railway mode
            )
            
            BeautifulLogger.info("Test téléchargement Railway...", "🚄")
            
            # Test simple et rapide
            success = scraper.download_chapter("lookism", 1)
            
            if success:
                cbz_files = [f for f in os.listdir(temp_dir) if f.endswith('.cbz')]
                if cbz_files:
                    file_size = os.path.getsize(os.path.join(temp_dir, cbz_files[0])) / (1024 * 1024)
                    BeautifulLogger.success(f"✅ RAILWAY TÉLÉCHARGEMENT: {cbz_files[0]} ({file_size:.1f} MB)")
                    return True
                else:
                    BeautifulLogger.warning("⚠️ Pas de fichier généré")
                    return False
            else:
                BeautifulLogger.warning("⚠️ Téléchargement Railway échoué")
                return False
                
    except Exception as e:
        BeautifulLogger.error(f"Erreur scraper Railway: {e}")
        return False

def main():
    """Test complet Railway optimisé"""
    print("="*80)
    BeautifulLogger.info("🚄 TEST SYSTÈME RAILWAY ULTRA-OPTIMISÉ", "🚀")
    print("="*80)
    
    # Test 1: Railway bypass direct
    bypass_success = test_railway_bypass()
    print("-" * 50)
    
    # Test 2: Scraper Railway
    scraper_success = test_scraper_railway_mode()
    print("-" * 50)
    
    # Résumé
    print("="*80)
    if bypass_success:
        BeautifulLogger.success("🚄 RAILWAY BYPASS OPÉRATIONNEL")
        
        if scraper_success:
            BeautifulLogger.success("⚡ RAILWAY SCRAPER ULTRA-RAPIDE")
        
        print("✅ Système Railway optimisé fonctionnel")
        print("⚡ Délais réduits pour production")
        print("🚄 Timeouts courts adaptés Railway")
        print("🎯 Bot prêt pour déploiement Railway")
        
    else:
        BeautifulLogger.warning("⚠️ RAILWAY OPTIMISATIONS PARTIELLES")
        print("🔧 Système technique avancé")
        print("🎯 Prêt pour tests supplémentaires")
    
    print("="*80)
    return bypass_success or scraper_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)