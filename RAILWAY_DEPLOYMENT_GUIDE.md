# Guide de Déploiement Railway - AnimesamascraperBot

## Problème Identifié

Le bot fonctionne parfaitement en local mais rencontre des erreurs 403 Forbidden sur Railway due aux restrictions des datacenters cloud.

## Solutions Implémentées

### 1. Headers Anti-Détection Renforcés
- User agents plus récents (Chrome 122+, Firefox 123+)
- Headers modernes avec `sec-ch-ua` et `zstd` encoding
- Rotation automatique des en-têtes sur erreur 403

### 2. Configuration Cloud Spécifique
- Détection automatique de l'environnement Railway via `RAILWAY_ENVIRONMENT`
- Headers IP falsifiés (`X-Forwarded-For`, `X-Real-IP`, `CF-Connecting-IP`)
- Origin et Referer spécifiques à anime-sama.fr

### 3. Gestion d'Erreurs 403 Améliorée
- Retry avec rotation complète des headers
- Délais progressifs plus longs (3s+ pour erreurs 403)
- Maximum 5 tentatives au lieu de 3

### 4. Configuration Railway

**Fichier `railway.toml`** :
```toml
[build]
builder = "nixpacks"

[deploy]
healthcheckPath = "/"
healthcheckTimeout = 300
restartPolicyType = "always"

[env]
RAILWAY_ENVIRONMENT = "true"
PYTHONUNBUFFERED = "1"
PIP_NO_CACHE_DIR = "1"
```

**Variables d'environnement à configurer sur Railway** :
- `TELEGRAM_TOKEN` : Votre token de bot Telegram
- `RAILWAY_ENVIRONMENT` : `true` (pour activer les optimisations cloud)

## Instructions de Déploiement

### 1. Configuration Initiale
```bash
# Cloner le repository
git clone https://github.com/Heathcliff1210/AnimesamascraperBot.git
cd AnimesamascraperBot

# Installer Railway CLI
npm install -g @railway/cli

# Se connecter à Railway
railway login
```

### 2. Déploiement
```bash
# Créer un nouveau projet Railway
railway init

# Ajouter les variables d'environnement
railway variables set TELEGRAM_TOKEN=votre_token_ici
railway variables set RAILWAY_ENVIRONMENT=true

# Déployer
railway up
```

### 3. Configuration Webhook (OBLIGATOIRE)
Le bot fonctionne maintenant en mode webhook pour éviter les conflits. Après le déploiement :

**Option A - Configuration automatique :**
```bash
# Se connecter au shell Railway
railway shell

# Configurer le webhook automatiquement
python setup_webhook.py

# Ou spécifier l'URL manuellement
python setup_webhook.py https://votre-app.railway.app
```

**Option B - Configuration manuelle :**
1. Visitez `https://votre-app.railway.app/set_webhook`
2. Ou utilisez l'API Telegram directement :
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook" \
     -d "url=https://votre-app.railway.app/webhook"
```

### 4. Vérification
- Le bot devrait afficher "🌐 Environnement cloud détecté"
- Vérifiez le webhook : `python setup_webhook.py info`
- Testez avec `/start` sur Telegram
- Plus d'erreurs de conflit de polling

## Optimisations Supplémentaires

### Si les erreurs 403 persistent :

1. **Proxy Rotation** (pour versions futures) :
   - Intégrer des proxies rotatifs
   - Utiliser des services comme ProxyMesh ou Bright Data

2. **Rate Limiting Plus Agressif** :
   - Augmenter les délais entre requêtes
   - Implémenter un système de queue

3. **Fallback Strategies** :
   - Mode dégradé avec moins de pages
   - Retry avec différents user agents

## Monitoring

Surveiller ces métriques sur Railway :
- Taux d'erreurs 403/404
- Temps de réponse moyen
- Consommation mémoire/CPU
- Logs d'erreurs spécifiques

## Support

Si les problèmes persistent :
1. Vérifier les logs Railway pour les erreurs spécifiques
2. Tester manuellement les URLs dans un navigateur depuis Railway
3. Considérer l'utilisation d'un VPN ou proxy
4. Contacter le support Railway pour les restrictions réseau