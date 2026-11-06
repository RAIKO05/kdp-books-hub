"""
serve_hub.py (v3.5 Multi-Threaded Edition)
High-performance local Wi-Fi and Cloudflare Tunnel server for KDP Books Hub.
Serves all 100 books, covers, PDFs, and metadata with concurrent requests support.
"""

import http.server
import socketserver
import socket
import os
import sys

PORT = 8080
DIRECTORY = "."

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

class HubHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Allow CORS from everywhere
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        
        # Cache control
        clean_path = self.path.split('?')[0]
        if clean_path.endswith(".html") or clean_path.endswith(".json") or clean_path == "/" or clean_path == "":
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
        elif clean_path.endswith(".pdf"):
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Disposition", "inline")
        elif clean_path.endswith(".png"):
            self.send_header("Content-Type", "image/png")
            self.send_header("Cache-Control", "public, max-age=3600")
        super().end_headers()

    def do_GET(self):
        # Redirect root to /index.html
        if self.path == "/" or self.path == "":
            self.send_response(302)
            self.send_header("Location", "/index.html")
            self.end_headers()
            return
        return super().do_GET()

    def do_HEAD(self):
        if self.path == "/" or self.path == "":
            self.send_response(302)
            self.send_header("Location", "/index.html")
            self.end_headers()
            return
        return super().do_HEAD()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

def run_server():
    local_ip = get_local_ip()
    url_local = f"http://{local_ip}:{PORT}/index.html"

    print("=" * 70)
    print("   KDP BOOKS HUB: MULTI-THREADED SERVER (100 BOOKS LIVE)")
    print("=" * 70)
    print(f"\n[+] Local Wi-Fi URL: {url_local}")
    print(f"[+] Localhost URL:  http://localhost:{PORT}/index.html")
    print("=" * 70)
    sys.stdout.flush()

    server = ThreadedHTTPServer(("", PORT), HubHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()

if __name__ == "__main__":
    run_server()
