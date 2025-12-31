from flask import Flask, request, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)
IMG_DIR = "images"
os.makedirs(IMG_DIR, exist_ok=True)

@app.route("/")
def index():
    files = sorted(os.listdir(IMG_DIR), reverse=True)
    html = "<h2>ESP32-CAM Gallery</h2>"
    for f in files:
        html += f'<img src="/images/{f}" width="300"><br><br>'
    return html

@app.route("/upload", methods=["POST"])
def upload():
    if not request.data:
        return "No image", 400

    name = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    with open(os.path.join(IMG_DIR, name), "wb") as f:
        f.write(request.data)

    return "OK", 200

@app.route("/images/<name>")
def images(name):
    return send_from_directory(IMG_DIR, name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
