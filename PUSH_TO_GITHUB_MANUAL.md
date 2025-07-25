# 🚀 Instructions pour pousser vers GitHub

## ✅ Étapes à suivre manuellement

Votre token GitHub est déjà configuré dans les secrets Replit. Voici les commandes exactes à exécuter dans le terminal :

### 1. Nettoyer les verrous Git
```bash
rm -f .git/index.lock .git/config.lock
```

### 2. Configurer votre identité Git
```bash
git config --global user.name "Heathcliff1210"
git config --global user.email "votre-email@example.com"
```

### 3. Configurer l'origin avec votre token
```bash
git remote remove origin
git remote add origin https://$GITHUB_PERSONAL_ACCESS_TOKEN@github.com/Heathcliff1210/AnimesamascraperBot.git
```

### 4. Ajouter et commiter les fichiers
```bash
git add .
git commit -m "🤖 Bot Telegram AnimesamascraperBot complet

✅ Fonctionnalités:
- /start - Interface élégante avec boutons
- /scan - Téléchargement chapitre unique CBZ
- /multiscan - Téléchargement multiple (1-20 chapitres)
- /tome - Téléchargement tome complet (10 chapitres ZIP)

🔧 Technologies:
- Python 3.11 + Telegram Bot API
- BeautifulSoup4 pour scraping anime-sama.fr
- Support CBZ/ZIP automatique
- Interface Flask intégrée

🔐 Sécurité:
- Tokens stockés dans secrets Replit
- Pas de credentials exposés dans le code"
```

### 5. Pousser vers GitHub
```bash
git push -u origin main
```

## 📁 Ce qui sera poussé vers GitHub

- `telegram_bot.py` - Bot principal avec 4 commandes
- `main.py` - Script CLI original
- `scraper/` - Modules de scraping modulaires
- `utils/` - Utilitaires partagés
- `README.md` - Documentation utilisateur
- `requirements.txt` - Dépendances Python
- Tous les fichiers de configuration

## ✅ Vérification

Après le push, votre repository GitHub contiendra tout le code du bot fonctionnel prêt pour déploiement.

## 🆘 En cas de problème

Si vous rencontrez des erreurs, essayez ces commandes alternatives :

```bash
# Si la branche main n'existe pas
git branch -M main
git push -u origin main

# Ou avec force si nécessaire
git push -f origin main
```