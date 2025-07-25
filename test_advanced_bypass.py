#!/usr/bin/env python3
"""
Test du système de contournement avancé anti-bot
"""

import tempfile
import os
from scraper.anime_sama_scraper import AnimeSamaScraper
from utils.beautiful_progress import BeautifulLogger
from utils.advanced_bypass import AdvancedAntiDetectionBypass

def test_advanced_bypass_direct():
    """Test direct du système de contournement avancé"""
    BeautifulLogger.info("Test direct du système de contournement avancé...", "🥷")
    
    try:
        bypass = AdvancedAntiDetectionBypass(verbose=True)
        
        # Test accès page principale
        response = bypass.bypass_request("https://anime-sama.fr/", max_retries=3)
        
        if response and response.status_code == 200:
            BeautifulLogger.success("✅ Contournement réussi - Page principale accessible")
            
            # Test page manga
            manga_response = bypass.bypass_request(
                "https://anime-sama.fr/catalogue/lookism/scan/vf/",
                max_retries=3
            )
            
            if manga_response and manga_response.status_code == 200:
                BeautifulLogger.success("✅ Contournement réussi - Page manga accessible")
                return True
            else:
                BeautifulLogger.warning("⚠️ Page manga non accessible")
                return False
        else:
            BeautifulLogger.warning("⚠️ Page principale non accessible")
            return False
            
    except Exception as e:
        BeautifulLogger.error(f"Erreur test bypass: {e}")
        return False

def test_scraper_with_bypass():
    """Test du scraper avec système de contournement"""
    BeautifulLogger.info("Test scraper avec contournement avancé...", "🎯")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Créer le scraper avec contournement avancé
            scraper = AnimeSamaScraper(
                output_dir=temp_dir,
                temp_dir=os.path.join(temp_dir, "temp"),
                verbose=True,
                use_residential_proxy=False,  # Désactiver proxies pour test pur
                use_advanced_bypass=True      # Activer contournement avancé
            )
            
            BeautifulLogger.info("Test téléchargement avec contournement...", "📖")
            
            # Test simple téléchargement
            success = scraper.download_chapter("lookism", 1)
            
            if success:
                # Vérifier fichier
                cbz_files = [f for f in os.listdir(temp_dir) if f.endswith('.cbz')]
                if cbz_files:
                    file_size = os.path.getsize(os.path.join(temp_dir, cbz_files[0])) / (1024 * 1024)
                    BeautifulLogger.success(f"✅ TÉLÉCHARGEMENT RÉUSSI: {cbz_files[0]} ({file_size:.1f} MB)")
                    return True
                else:
                    BeautifulLogger.warning("⚠️ Pas de fichier CBZ généré")
                    return False
            else:
                BeautifulLogger.warning("⚠️ Téléchargement échoué")
                return False
                
    except Exception as e:
        BeautifulLogger.error(f"Erreur test scraper: {e}")
        return False

def test_hybrid_system():
    """Test du système hybride (contournement + proxies)"""
    BeautifulLogger.info("Test système hybride complet...", "🚀")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Créer le scraper avec tous les systèmes
            scraper = AnimeSamaScraper(
                output_dir=temp_dir,
                temp_dir=os.path.join(temp_dir, "temp"),
                verbose=True,
                use_residential_proxy=True,   # Proxies résidentiels
                use_advanced_bypass=True      # + Contournement avancé
            )
            
            BeautifulLogger.info("Test système hybride complet...", "🔥")
            
            # Test téléchargement
            success = scraper.download_chapter("fairy tail", 1)
            
            if success:
                cbz_files = [f for f in os.listdir(temp_dir) if f.endswith('.cbz')]
                if cbz_files:
                    BeautifulLogger.success(f"✅ SYSTÈME HYBRIDE OPÉRATIONNEL: {cbz_files[0]}")
                    return True
                else:
                    BeautifulLogger.warning("⚠️ Pas de fichier CBZ généré")
                    return False
            else:
                BeautifulLogger.warning("⚠️ Téléchargement échoué")
                return False
                
    except Exception as e:
        BeautifulLogger.error(f"Erreur test hybride: {e}")
        return False

def main():
    """Test complet du système de contournement avancé"""
    print("="*80)
    BeautifulLogger.info("🥷 TEST SYSTÈME DE CONTOURNEMENT AVANCÉ", "🚀")
    print("="*80)
    
    # Test 1: Bypass direct
    bypass_success = test_advanced_bypass_direct()
    print("-" * 50)
    
    # Test 2: Scraper avec bypass
    scraper_success = test_scraper_with_bypass()
    print("-" * 50)
    
    # Test 3: Système hybride
    hybrid_success = test_hybrid_system()
    print("-" * 50)
    
    # Résumé
    print("="*80)
    if bypass_success:
        BeautifulLogger.success("🎉 CONTOURNEMENT AVANCÉ OPÉRATIONNEL")
        
        if scraper_success:
            BeautifulLogger.success("🎯 SCRAPER AVEC CONTOURNEMENT RÉUSSI")
        
        if hybrid_success:
            BeautifulLogger.success("🔥 SYSTÈME HYBRIDE PARFAIT")
        
        print("✅ Système de contournement fonctionnel")
        print("🥷 Protections anti-bot contournées")
        print("🚀 Bot prêt pour anime-sama.fr")
        
    else:
        BeautifulLogger.warning("⚠️ CONTOURNEMENT PARTIEL")
        print("🔧 Système technique avancé mais restrictions fortes")
        print("🎯 Architecture prête pour autres sources")
    
    print("="*80)
    return bypass_success or scraper_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)