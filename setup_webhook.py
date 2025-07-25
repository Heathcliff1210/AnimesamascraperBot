#!/usr/bin/env python3
"""
Script pour configurer automatiquement le webhook Telegram
"""

import os
import requests
import sys

def setup_webhook(webhook_url=None):
    """Configure le webhook Telegram"""
    
    # Obtenir le token
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        print("❌ TELEGRAM_TOKEN non trouvé dans les variables d'environnement")
        return False
    
    # URL par défaut si non fournie
    if not webhook_url:
        # Essayer de détecter l'URL du déploiement
        railway_url = os.getenv('RAILWAY_STATIC_URL')
        render_url = os.getenv('RENDER_EXTERNAL_URL')
        replit_url = os.getenv('REPL_URL')
        
        if railway_url:
            webhook_url = f"{railway_url}/webhook"
        elif render_url:
            webhook_url = f"{render_url}/webhook"
        elif replit_url:
            webhook_url = f"{replit_url}/webhook"
        else:
            print("❌ Impossible de détecter l'URL de déploiement")
            print("💡 Utilisez: python setup_webhook.py https://votre-url.railway.app")
            return False
    
    print(f"🔧 Configuration du webhook: {webhook_url}")
    
    # Configurer le webhook
    api_url = f"https://api.telegram.org/bot{token}/setWebhook"
    data = {
        'url': webhook_url,
        'allowed_updates': ['message', 'callback_query']
    }
    
    try:
        response = requests.post(api_url, data=data, timeout=30)
        result = response.json()
        
        if result.get('ok'):
            print("✅ Webhook configuré avec succès!")
            print(f"📡 URL: {webhook_url}")
            return True
        else:
            print(f"❌ Erreur: {result.get('description', 'Erreur inconnue')}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def get_webhook_info():
    """Affiche les informations du webhook actuel"""
    
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        print("❌ TELEGRAM_TOKEN non trouvé")
        return False
    
    api_url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
    
    try:
        response = requests.get(api_url, timeout=30)
        result = response.json()
        
        if result.get('ok'):
            info = result.get('result', {})
            print("📊 Informations du webhook:")
            print(f"   URL: {info.get('url', 'Non configuré')}")
            print(f"   Pending updates: {info.get('pending_update_count', 0)}")
            print(f"   Dernière erreur: {info.get('last_error_message', 'Aucune')}")
            return True
        else:
            print(f"❌ Erreur: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def delete_webhook():
    """Supprime le webhook (revient au polling)"""
    
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        print("❌ TELEGRAM_TOKEN non trouvé")
        return False
    
    api_url = f"https://api.telegram.org/bot{token}/deleteWebhook"
    
    try:
        response = requests.post(api_url, timeout=30)
        result = response.json()
        
        if result.get('ok'):
            print("✅ Webhook supprimé - Bot en mode polling")
            return True
        else:
            print(f"❌ Erreur: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "info":
            get_webhook_info()
        elif command == "delete":
            delete_webhook()
        elif command.startswith("http"):
            setup_webhook(command)
        else:
            print("❌ Commande inconnue")
            print("Usage:")
            print("  python setup_webhook.py                    # Auto-détection URL")
            print("  python setup_webhook.py https://mon-url    # URL spécifique")
            print("  python setup_webhook.py info               # Informations webhook")
            print("  python setup_webhook.py delete             # Supprimer webhook")
    else:
        setup_webhook()