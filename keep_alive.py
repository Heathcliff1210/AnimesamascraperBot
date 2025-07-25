
from flask import Flask
from threading import Thread
import time

app = Flask('')

@app.route('/')
def home():
    return "🤖 Bot Telegram Anime-Sama est en ligne !"

@app.route('/health')
def health():
    import json
    return json.dumps({
        "status": "healthy",
        "service": "anime-sama-telegram-bot", 
        "timestamp": time.time()
    })

@app.route('/status')
def status():
    import json
    return json.dumps({
        "bot": "running",
        "platform": "replit",
        "version": "1.0.0"
    })

def run():
    try:
        # Port pour Railway (utilise la variable d'environnement PORT)
        import os
        port = int(os.getenv('PORT', 5000))
        print(f"🌐 Serveur Flask démarré sur le port {port}")
        app.run(host='0.0.0.0', port=port, use_reloader=False, debug=False)
    except OSError as e:
        if "Address already in use" in str(e):
            print("⚠️ Port déjà utilisé - tentative avec port alternatif")
            try:
                app.run(host='0.0.0.0', port=8080, use_reloader=False, debug=False)
            except:
                print("❌ Impossible de démarrer le serveur Flask")
        else:
            raise e

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
    # Attendre que le serveur soit prêt
    import time
    time.sleep(1)
