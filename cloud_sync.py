"""
cloud_sync.py (v3.0 - Hybrid Cloud Sync Engine)
Simultaneously synchronizes KDP Books Hub across:
1. Google Cloud (Firebase Realtime Database) - Sub-second live updates
2. GitHub Cloud (Git repository / GitHub Pages / Raw CDN) - Permanent global redundancy
"""

import json
import urllib.request
import os
import subprocess

SERIES_DIR = "The_Detectives_Case_Files_Series"
CATALOG_PATH = os.path.join(SERIES_DIR, "catalog.json")
CONFIG_PATH = os.path.join(SERIES_DIR, "cloud_config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def sync_to_google_cloud(firebase_url):
    if not firebase_url:
        print("[!] No Google Cloud Firebase URL configured.")
        return False

    clean_url = firebase_url.rstrip("/")
    if not clean_url.endswith("/catalog.json"):
        clean_url += "/catalog.json"

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog_bytes = f.read().encode("utf-8")

    req = urllib.request.Request(
        clean_url,
        data=catalog_bytes,
        headers={"Content-Type": "application/json"},
        method="PUT"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                print(f"[✓] GOOGLE CLOUD: Synced to Firebase ({clean_url})")
                return True
    except Exception as e:
        print(f"[!] Google Cloud Sync failed: {e}")
        return False

def sync_to_github():
    # Check if a git remote origin exists
    try:
        result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
        if result.returncode != 0 or not result.stdout.strip():
            print("[i] GITHUB CLOUD: No git remote 'origin' configured yet.")
            print("    To enable auto-push to GitHub, connect a GitHub repository:")
            print("    git remote add origin https://github.com/<your-username>/<your-repo>.git")
            return False

        remote_url = result.stdout.strip()
        print(f"[*] GITHUB CLOUD: Pushing to {remote_url}...")
        
        # Stage files
        subprocess.run(["git", "add", "The_Detectives_Case_Files_Series/"], check=True)
        
        # Check if there are changes to commit
        status = subprocess.run(["git", "status", "--porcelain", "The_Detectives_Case_Files_Series/"], capture_output=True, text=True)
        if status.stdout.strip():
            subprocess.run(["git", "commit", "-m", "Hybrid Cloud auto-sync: KDP catalog update"], check=True)
        
        # Push to remote
        push = subprocess.run(["git", "push", "origin", "master"], capture_output=True, text=True)
        if push.returncode == 0:
            print("[✓] GITHUB CLOUD: Successfully pushed updates to GitHub!")
            return True
        else:
            print(f"[!] GitHub push failed: {push.stderr.strip()}")
            return False
    except Exception as e:
        print(f"[!] GitHub sync encountered an error: {e}")
        return False

def run_hybrid_sync():
    cfg = load_config()
    fb_url = cfg.get("firebase_url")
    
    print("=" * 65)
    print("      HYBRID CLOUD SYNCHRONIZER (GOOGLE CLOUD + GITHUB)")
    print("=" * 65)
    
    # 1. Google Cloud
    fb_success = sync_to_google_cloud(fb_url)
    
    # 2. GitHub Cloud
    gh_success = sync_to_github()
    
    print("=" * 65)
    if fb_success and gh_success:
        print("[✓] HYBRID SYNC: Both Google Cloud and GitHub Cloud updated!")
    elif fb_success:
        print("[✓] GOOGLE CLOUD SYNC: Active! (GitHub ready to connect)")
    elif gh_success:
        print("[✓] GITHUB CLOUD SYNC: Active! (Google Cloud offline)")
    else:
        print("[!] No clouds synchronized.")
    print("=" * 65)

if __name__ == "__main__":
    run_hybrid_sync()
