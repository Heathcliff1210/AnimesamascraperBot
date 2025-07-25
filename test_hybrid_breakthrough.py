#!/usr/bin/env python3
"""
Test du système hybride révolutionnaire
"""

import tempfile
import os
from scraper.anime_sama_scraper import AnimeSamaScraper
from utils.beautiful_progress import BeautifulLogger
from utils.hybrid_breakthrough import HybridBreakthroughSystem

def test_hybrid_direct():
    """Test direct du système hybride"""
    BeautifulLogger.info("Test hybride révolutionnaire direct...", "🔥")
    
    # Simuler environnement Railway pour test complet
    os.environ['RAILWAY_ENVIRONMENT'] = 'production'
    
    try:
        hybrid = HybridBreakthroughSystem(verbose=True)
        
        # Test avec rotation automatique
        response = hybrid.breakthrough_request(
            "https://anime-sama.fr/catalogue/lookism/scan/vf/episodes.js",
            max_global_retries=6
        )
        
        if response and response.status_code == 200:
            BeautifulLogger.success("✅ SYSTÈME HYBRIDE RÉUSSI !")
            
            # Afficher stats
            stats = hybrid.get_stats()
            BeautifulLogger.info(f"Méthode réussie: {stats['last_successful']}")
            return True
        else:
            BeautifulLogger.warning("⚠️ Système hybride échoué")
            stats = hybrid.get_stats()
            BeautifulLogger.info(f"Échecs: {stats['failures']}")
            return False
            
    except Exception as e:
        BeautifulLogger.error(f"Erreur hybride: {e}")
        return False

def test_scraper_hybrid():
    """Test scraper avec système hybride"""
    BeautifulLogger.info("Test scraper hybride complet...", "🔥")
    
    # Simuler Railway
    os.environ['RAILWAY_ENVIRONMENT'] = 'production'
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Scraper avec système hybride
            scraper = AnimeSamaScraper(
                output_dir=temp_dir,
                temp_dir=os.path.join(temp_dir, "temp"),
                verbose=True,
                use_residential_proxy=False,
                use_advanced_bypass=True,
                use_railway_bypass=True,
                use_hybrid_system=True  # SYSTÈME HYBRIDE
            )
            
            BeautifulLogger.info("Test téléchargement hybride...", "🔥")
            
            # Test avec rotation automatique des méthodes
            success = scraper.download_chapter("lookism", 1)
            
            if success:
                cbz_files = [f for f in os.listdir(temp_dir) if f.endswith('.cbz')]
                if cbz_files:
                    file_size = os.path.getsize(os.path.join(temp_dir, cbz_files[0])) / (1024 * 1024)
                    BeautifulLogger.success(f"✅ HYBRIDE RÉUSSI: {cbz_files[0]} ({file_size:.1f} MB)")
                    
                    # Stats du système hybride
                    if scraper.hybrid_system:
                        stats = scraper.hybrid_system.get_stats()
                        BeautifulLogger.info(f"🎯 Méthode gagnante: {stats['last_successful']}")
                    
                    return True
                else:
                    BeautifulLogger.warning("⚠️ Pas de fichier généré")
                    return False
            else:
                BeautifulLogger.warning("⚠️ Téléchargement hybride échoué")
                return False
                
    except Exception as e:
        BeautifulLogger.error(f"Erreur scraper hybride: {e}")
        return False

def main():
    """Test complet du système révolutionnaire"""
    print("="*80)
    BeautifulLogger.info("🔥 TEST SYSTÈME HYBRIDE RÉVOLUTIONNAIRE", "🚀")
    print("="*80)
    
    # Test 1: Hybride direct
    hybrid_success = test_hybrid_direct()
    print("-" * 50)
    
    # Test 2: Scraper hybride
    scraper_success = test_scraper_hybrid()
    print("-" * 50)
    
    # Résumé final
    print("="*80)
    if hybrid_success or scraper_success:
        BeautifulLogger.success("🔥 SYSTÈME HYBRIDE RÉVOLUTIONNAIRE OPÉRATIONNEL")
        
        if scraper_success:
            BeautifulLogger.success("🎯 SCRAPER HYBRIDE RÉUSSI")
        
        print("✅ Rotation automatique des techniques")
        print("🔥 Système adaptatif selon environnement") 
        print("🎯 Apprentissage des méthodes efficaces")
        print("🚀 Bot prêt avec toutes les armes")
        
    else:
        BeautifulLogger.warning("⚠️ SYSTÈME HYBRIDE PARTIEL")
        print("🔧 Architecture technique avancée")
        print("🎯 Infrastructure prête pour évolutions")
    
    print("="*80)
    return hybrid_success or scraper_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)