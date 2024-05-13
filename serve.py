import re
import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from script import (
    generate_html_from_css_palette,
    get_webpage_ss,
    get_css_palette,
    get_print_keywords,
    get_keywords_bs,
)


class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
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
            url = self.path[1:]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # send makeshift json
            css = get_css_palette(url)
            kw = get_keywords_bs(url)
            self.wfile.write(json.dumps({"css": css, "kw": kw}))
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


httpd = HTTPServer(("localhost", 8000), Serv)
httpd.serve_forever()
