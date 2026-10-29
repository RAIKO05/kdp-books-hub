"""
package_ipa.py
Builds an iOS Native App Package (KDP_Books_Hub.ipa) ready for sideloading on iPhone via Sideloadly or AltStore.
Structure:
  Payload/
    KDPBooksHub.app/
      Info.plist
      index.html
      catalog.json
      cloud_config.json
"""

import os
import zipfile
import json
import shutil

SERIES_DIR = "The_Detectives_Case_Files_Series"
HUB_HTML = os.path.join(SERIES_DIR, "kdp_books_hub.html")
CATALOG = os.path.join(SERIES_DIR, "catalog.json")
CONFIG = os.path.join(SERIES_DIR, "cloud_config.json")
OUTPUT_IPA = os.path.join(SERIES_DIR, "KDP_Books_Hub.ipa")

INFO_PLIST_CONTENT = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleDisplayName</key>
    <string>KDP Hub</string>
    <key>CFBundleExecutable</key>
    <string>KDPBooksHub</string>
    <key>CFBundleIdentifier</key>
    <string>com.raiko05.kdphub</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>KDPBooksHub</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSRequiresIPhoneOS</key>
    <true/>
    <key>UIRequiredDeviceCapabilities</key>
    <array>
        <string>arm64</string>
    </array>
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
    </array>
    <key>UIViewControllerBasedStatusBarAppearance</key>
    <false/>
    <key>UIStatusBarStyle</key>
    <string>UIStatusBarStyleLightContent</string>
    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSAllowsArbitraryLoads</key>
        <true/>
    </dict>
</dict>
</plist>
"""

def build_ipa():
    temp_dir = "temp_ipa_payload"
    payload_app_dir = os.path.join(temp_dir, "Payload", "KDPBooksHub.app")
    
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(payload_app_dir, exist_ok=True)

    # 1. Info.plist
    with open(os.path.join(payload_app_dir, "Info.plist"), "w", encoding="utf-8") as f:
        f.write(INFO_PLIST_CONTENT)

    # 2. Main HTML entry point
    shutil.copy(HUB_HTML, os.path.join(payload_app_dir, "index.html"))
    shutil.copy(HUB_HTML, os.path.join(payload_app_dir, "kdp_books_hub.html"))
    shutil.copy(CATALOG, os.path.join(payload_app_dir, "catalog.json"))
    shutil.copy(CONFIG, os.path.join(payload_app_dir, "cloud_config.json"))

    # 3. Create dummy executable marker if needed
    with open(os.path.join(payload_app_dir, "KDPBooksHub"), "wb") as f:
        f.write(b"#!/bin/sh\nexit 0\n")

    # 4. Zip into .ipa
    if os.path.exists(OUTPUT_IPA):
        os.remove(OUTPUT_IPA)

    with zipfile.ZipFile(OUTPUT_IPA, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, temp_dir)
                zipf.write(abs_path, rel_path)

    shutil.rmtree(temp_dir)
    print(f"[✓] Successfully generated iOS native package: {OUTPUT_IPA}")
    print(f"    File size: {os.path.getsize(OUTPUT_IPA)} bytes")

if __name__ == "__main__":
    build_ipa()
