"""
serve_hub.py
Launches a local Wi-Fi live sync server for your iPhone.
1. Detects your computer's local Wi-Fi IP address.
2. Serves kdp_books_hub.html and catalog.json.
3. Automatically updates your iPhone whenever books are added or modified!
"""

import http.server
import socketserver
import socket
import os

PORT = 8080
DIRECTORY = "The_Detectives_Case_Files_Series"

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

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run_server():
    local_ip = get_local_ip()
    url = f"http://{local_ip}:{PORT}/kdp_books_hub.html"

    print("=" * 65)
    print("       KDP BOOKS HUB: IPHONE AUTO-SYNC WI-FI SERVER")
    print("=" * 65)
    print(f"\n[+] Server is LIVE on your local Wi-Fi network!")
    print(f"\n[>] OPEN THIS LINK IN SAFARI ON YOUR IPHONE:")
    print(f"    --> {url} <--\n")
    print("=" * 65)
    print("HOW IT WORKS:")
    print("1. Make sure your iPhone is connected to the same Wi-Fi as this PC.")
    print("2. Open Safari on your iPhone and type the link above.")
    print("3. In Safari, tap Share -> 'Add to Home Screen'.")
    print("4. ANY TIME YOU ADD OR EDIT A BOOK, IT AUTO-SYNCS TO YOUR IPHONE!")
    print("=" * 65)
    print("\nPress Ctrl+C in this terminal to stop the server at any time.\n")

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run_server()
