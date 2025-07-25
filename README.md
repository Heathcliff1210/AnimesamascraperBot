# Bot Telegram - Anime-Sama Manga Downloader

Ce bot Telegram vous permet de télécharger des chapitres de manga depuis anime-sama.fr directement dans votre chat.

## 🚀 Utilisation du Bot

### Commandes disponibles

#### `/start` ou `/help`
Affiche le message d'accueil et la liste des commandes disponibles.

#### `/scan <nom_manga> <chapitre>`
Télécharge un chapitre spécifique et l'envoie au format CBZ.

**Exemples :**
- `/scan blue lock 272`
- `/scan lookism 1`
- `/scan one piece 1095`

#### `/multiscan <nom_manga> <chapitre_debut> <chapitre_fin>`
Télécharge plusieurs chapitres d'affilée (maximum 20 chapitres).

**Exemples :**
- `/multiscan lookism 1 5`
- `/multiscan blue lock 270 275`

#### `/tome <nom_manga> <numéro_tome>`
Télécharge un tome complet (10 chapitres) dans un fichier ZIP.

**Logique des tomes :**
- Tome 1 = chapitres 1-10
- Tome 2 = chapitres 11-20
- Tome 3 = chapitres 21-30, etc.

**Exemples :**
- `/tome blue lock 1` (chapitres 1-10 en ZIP)
- `/tome lookism 3` (chapitres 21-30 en ZIP)

## 📋 Fonctionnalités

- ✅ Téléchargement de chapitres individuels
- ✅ Téléchargement multiple (jusqu'à 20 chapitres)
- ✅ Conversion automatique en format CBZ
- ✅ Validation de la taille des fichiers (limite 50 MB)
- ✅ Messages de progression en temps réel
- ✅ Gestion des erreurs avec feedback détaillé

## 🔧 Configuration Technique

### Prérequis
- Python 3.8+
- Bibliothèques : `python-telegram-bot`, `requests`, `beautifulsoup4`, `lxml`

### Structure du projet
```
.
├── telegram_bot.py          # Bot Telegram principal
├── main.py                 # Script en ligne de commande (original)
├── scraper/                # Modules de scraping
│   ├── anime_sama_scraper.py
│   ├── url_builder.py
│   ├── image_downloader.py
│   └── cbz_converter.py
└── utils/                  # Utilitaires
    ├── headers.py
    └── progress.py
```

### Démarrage du bot
```bash
python telegram_bot.py
```

## 📱 Comment trouver votre bot

1. Recherchez votre bot sur Telegram en utilisant le nom d'utilisateur fourni
2. Démarrez une conversation avec `/start`
3. Utilisez les commandes pour télécharger vos manga

## ⚠️ Limitations

- **Taille maximum :** 50 MB par fichier (limite Telegram)
- **Chapitres simultanés :** Maximum 20 chapitres avec `/multiscan`
- **Source :** Seuls les manga disponibles sur anime-sama.fr
- **Format :** Sortie uniquement en CBZ (compatible avec tous les lecteurs de BD)

## 🛠️ Résolution de problèmes

### "Aucun chapitre trouvé"
- Vérifiez l'orthographe du nom du manga
- Assurez-vous que le chapitre existe sur animate-sama.fr
- Essayez avec un nom plus simple (ex: "blue lock" au lieu de "Blue Lock")

### "Fichier trop volumineux"
- Le chapitre dépasse 50 MB
- Téléchargez-le individuellement ou utilisez la version ligne de commande

### Bot ne répond pas
- Vérifiez que le bot est en cours d'exécution
- Redémarrez le workflow si nécessaire

## 📄 Formats supportés

**Entrée :** Pages manga depuis anime-sama.fr
**Sortie :** Fichiers CBZ (ZIP contenant les images)

Les fichiers CBZ peuvent être lus avec :
- Tachiyomi (Android)
- CDisplayEx (Windows)
- Chunky Comic Reader (iOS)
- KOReader (Multi-plateforme)
- Et la plupart des lecteurs de BD numériques

## 🔒 Sécurité

- Le bot utilise un token sécurisé pour l'authentification
- Aucune donnée personnelle n'est stockée
- Les fichiers temporaires sont automatiquement supprimés après envoi