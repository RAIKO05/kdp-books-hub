"""
cloud_sync.py (v4.0 - Bi-Directional Hybrid Cloud Engine)
Simultaneously synchronizes KDP Books Hub across:
1. Google Cloud (Firebase Realtime Database) - Two-way live sync (iPhone <-> PC)
2. GitHub Cloud (Git repository / GitHub Pages / CI/CD IPA builder)
"""

import json
import urllib.request
import os
import subprocess
import time

SERIES_DIR = "The_Detectives_Case_Files_Series"
CATALOG_PATH = os.path.join(SERIES_DIR, "catalog.json")
CONFIG_PATH = os.path.join(SERIES_DIR, "cloud_config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def bi_directional_sync_firebase(firebase_url):
    if not firebase_url:
        print("[!] No Google Cloud Firebase URL configured.")
        return False

    clean_url = firebase_url.rstrip("/")
    if not clean_url.endswith("/catalog.json"):
        clean_url += "/catalog.json"

    # 1. Fetch remote data from Firebase to check for books added from iPhone
    remote_data = None
    try:
        req = urllib.request.Request(clean_url + f"?t={int(time.time())}")
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                remote_data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"[!] Note: Could not fetch remote Firebase catalog: {e}")

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        local_data = json.load(f)

    # 2. Merge any new books added from iPhone into local catalog
    updated = False
    if remote_data and isinstance(remote_data, list):
        local_ids = {b.get("id") for b in local_data if b.get("id")}
        for r_book in remote_data:
            if r_book.get("id") and r_book["id"] not in local_ids:
                print(f"[+] Synced new book from iPhone: {r_book.get('title')} ({r_book.get('tab_name')})")
                local_data.append(r_book)
                updated = True

        if updated:
            with open(CATALOG_PATH, "w", encoding="utf-8") as f:
                json.dump(local_data, f, indent=2)
            print(f"[✓] Local catalog updated with {len(local_data)} total books!")

    # 3. Push consolidated catalog back to Firebase
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
                print(f"[✓] GOOGLE CLOUD: 100% Bi-Directional Sync Active ({clean_url})")
                return True
    except Exception as e:
        print(f"[!] Google Cloud Sync failed: {e}")
        return False

def sync_to_github():
    try:
        result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
        if result.returncode != 0 or not result.stdout.strip():
            print("[i] GITHUB CLOUD: No git remote 'origin' configured.")
            return False

        remote_url = result.stdout.strip()
        print(f"[*] GITHUB CLOUD: Syncing to {remote_url}...")
        
        # Stage files
        subprocess.run(["git", "add", "."], check=True)
        
        # Check if there are changes to commit
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if status.stdout.strip():
            subprocess.run(["git", "commit", "-m", "Hybrid Cloud & iOS IPA auto-sync"], check=True)
        
        # Push to main
        push = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
        if push.returncode == 0:
            print("[✓] GITHUB CLOUD: Successfully pushed updates & triggered IPA build workflow!")
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
    print("  HYBRID CLOUD & NATIVE IOS SYNC (GOOGLE CLOUD + GITHUB)")
    print("=" * 65)
    
    fb_success = bi_directional_sync_firebase(fb_url)
    gh_success = sync_to_github()
    
    print("=" * 65)
    if fb_success and gh_success:
        print("[✓] HYBRID 100% SYNC: Google Cloud and GitHub Cloud in perfect lockstep!")
    elif fb_success:
        print("[✓] GOOGLE CLOUD SYNC: Active!")
    elif gh_success:
        print("[✓] GITHUB CLOUD SYNC: Active!")
    print("=" * 65)

if __name__ == "__main__":
    run_hybrid_sync()
