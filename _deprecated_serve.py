import time
import re
import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from src.interface import CSSKWInterface
import ssl


class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path[1:] == "favicon.ico":
            return
        if "~load~" in self.path:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # send the html file from build folder
            domain = self.path.split("~load~")[1]
            path = f"htmls/{domain}/generated_index.html"
            if not os.path.exists(path):
                self.wfile.write(b"error: generate first")
                return
            with open(f"htmls/{domain}/generated_index.html", "rb") as f:
                self.wfile.write(f.read())
        else:
            try:
                url = self.path[1:]
                css, kw = CSSKWInterface.get_fastest_way_css_kw(url)
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET")
                self.send_header("Access-Control-Allow-Header", "Content-Type")
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"css": css, "kw": kw}).encode())
                return
            except BrokenPipeError:
                print("clietn disconnected")
                self.send_response(500)
                return
            res = subprocess.run(["python3", "main.py", f"{url}"])
            if res.returncode != 0:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"error: can't generate")
                return

            self.send_response(201)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            domain = re.search("https?://(.*)", url).group(1)
            self.wfile.write(
                f"generated; go to /~load~{domain} to view the generated page".encode()
            )


httpd = HTTPServer(("0.0.0.0", 8000), Serv)
httpd.serve_forever()
