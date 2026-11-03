import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = os.environ.get("OWNER_ID")

@app.route("/")
def home():
    return "Bot de fotografías activo"

@app.route("/upload", methods=["POST"])
def upload():
    if not TOKEN or not OWNER_ID:
        return jsonify({"error": "Configuración pendiente"}), 500

    photo = request.files.get("photo")

    if not photo:
        return jsonify({"error": "No se recibió fotografía"}), 400

    if photo.mimetype not in ["image/jpeg", "image/png"]:
        return jsonify({"error": "Formato no permitido"}), 400

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    response = requests.post(
        url,
        data={
            "chat_id": OWNER_ID,
            "caption": "Fotografía enviada voluntariamente"
        },
        files={"photo": photo},
        timeout=30
    )

    if not response.ok:
        return jsonify({"error": "No se pudo enviar"}), 502

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
