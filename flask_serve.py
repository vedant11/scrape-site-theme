import os
import re
import subprocess

from flask import Flask, jsonify
from flask_cors import CORS

from src.interface import CSSKWInterface

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/favicon.ico")
def random_ico():
    data_url = "data:image/x-icon;base64,AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAAgAAAAAAAAAAAAAAAEAAAAAAAAAAEAAAAAAAAAAQAAAAAAEAAAAAAAB"
    return data_url


@app.route("/~load~<domain>")
def load(domain):
    path = f"htmls/{domain}/generated_index.html"
    if not os.path.exists(path):
        return "error: generate first"
    with open(path, "rb") as f:
        return f.read()


@app.route("/<path:url>", methods=["GET"])
def generate(url):
    if not url or not re.match(r"^https?://", url):
        return "error: invalid url", 400
    css, kw = CSSKWInterface.get_fastest_way_css_kw(url)
    return jsonify({"css": css, "kw": kw})


@app.route("/generate<url>", methods=["POST"])
def generate_post(url):
    if not url:
        return "error: missing url parameter", 400

    res = subprocess.run(["python3", "main.py", f"{url}"])
    if res.returncode != 0:
        return "error: can't generate", 400

    domain = re.search("https?://(.*)", url).group(1)
    return f"generated; go to /~load~{domain} to view the generated page"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
