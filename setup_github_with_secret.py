#!/usr/bin/env python3
"""
Script pour configurer l'origin GitHub avec le token depuis les secrets Replit
"""

import os
import subprocess

def setup_github_origin():
    # Récupérer le token depuis les secrets Replit
    github_token = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
    
    if not github_token:
        print("❌ ERREUR: Token GitHub non configuré!")
        print("📝 Ajoutez votre token dans les Secrets Replit:")
        print("   - Nom: GITHUB_PERSONAL_ACCESS_TOKEN")
        print("   - Valeur: [VOTRE_TOKEN_GITHUB]")
        return False
    
    # Construire l'URL avec le token
    repo_url = f"https://{github_token}@github.com/Heathcliff1210/AnimesamascraperBot.git"
    
    try:
        # Supprimer l'ancien remote s'il existe
        subprocess.run(['git', 'remote', 'remove', 'origin'], 
                      capture_output=True, check=False)
        
        # Ajouter le nouveau remote avec le token
        result = subprocess.run(['git', 'remote', 'add', 'origin', repo_url], 
                               capture_output=True, check=True, text=True)
        
        print("✅ Origin GitHub configuré avec succès!")
        
        # Vérifier la configuration
        result = subprocess.run(['git', 'remote', '-v'], 
                               capture_output=True, check=True, text=True)
        print("📋 Remote configuré:")
        print(result.stdout.replace(github_token, "***TOKEN***"))
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la configuration: {e}")
        return False

if __name__ == "__main__":
    setup_github_origin()