import time
import re
import os
import subprocess
from flask import Flask, request, jsonify
from script import get_css_palette, get_keywords_bs


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/~load~<domain>")
def load(domain):
    path = f"htmls/{domain}/generated_index.html"
    if not os.path.exists(path):
        return "error: generate first"
    with open(path, "rb") as f:
        return f.read()


@app.route("/<path:url>", methods=["GET"])
def generate(url):
    if not url:
        return "error: missing url parameter", 400

    css = get_css_palette(url)
    time.sleep(2)
    kw = get_keywords_bs(url)
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
    app.run(host="localhost", port=8000)
