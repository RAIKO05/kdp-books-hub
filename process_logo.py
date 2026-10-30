"""
process_logo.py
Processes the user-provided "KDP HUB" logo into professional, Apple HIG-compliant app icons:
1. Trims and centers the logo with exact ~20% breathing room for the iOS squircle mask.
2. Generates all iOS and PWA icon resolutions (1024, 512, 192, 180, 167, 152, 120, 64, 32).
3. Creates a transparent PNG for the in-app navigation bar.
4. Generates PWA manifest.json.
5. Deploys assets across all project directories.
"""

import os
from PIL import Image

SRC_PATH = r"C:/Users/Aka.mouadd/.gemini/antigravity/brain/9cd31ca9-6dc1-4e61-b2f5-893e9a171765/.user_uploaded/media_1793322990465_edb4ff88.png"
SERIES_DIR = "The_Detectives_Case_Files_Series"
IOS_DIR = "ios_src"
os.makedirs(SERIES_DIR, exist_ok=True)
os.makedirs(IOS_DIR, exist_ok=True)

def generate_assets():
    print(f"[*] Loading source image from: {SRC_PATH}")
    src_img = Image.open(SRC_PATH).convert("RGBA")
    
    # Crop exact logo bbox: x=[300, 776], y=[345, 697]
    logo_crop = src_img.crop((300, 345, 776, 697))
    logo_w, logo_h = logo_crop.size

    # --- 1. Master 1024x1024 Solid Black Icon (Apple HIG compliant) ---
    # In Apple guidelines, the icon glyph should occupy ~60-65% of the canvas
    target_w = 640
    target_h = int(logo_h * (target_w / logo_w))
    logo_resized = logo_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)

    master_icon = Image.new("RGBA", (1024, 1024), (0, 0, 0, 255))
    offset_x = (1024 - target_w) // 2
    offset_y = (1024 - target_h) // 2
    master_icon.paste(logo_resized, (offset_x, offset_y), logo_resized)

    # --- 2. Transparent Header Logo ---
    transparent_logo = Image.new("RGBA", (logo_w, logo_h), (0, 0, 0, 0))
    for y in range(logo_h):
        for x in range(logo_w):
            r, g, b, _ = logo_crop.getpixel((x, y))
            alpha = max(r, g, b)
            if alpha > 12:
                transparent_logo.putpixel((x, y), (255, 255, 255, alpha))

    # Scale header logo to height 56px (for crisp 2x retina display at 28px height)
    hdr_h = 56
    hdr_w = int(logo_w * (hdr_h / logo_h))
    header_logo = transparent_logo.resize((hdr_w, hdr_h), Image.Resampling.LANCZOS)

    # --- 3. Generate All Resolutions ---
    sizes = {
        "app_icon_1024.png": 1024,
        "icon-512.png": 512,
        "icon-192.png": 192,
        "apple-touch-icon.png": 180,
        "apple-touch-icon-180x180.png": 180,
        "apple-touch-icon-167x167.png": 167,
        "apple-touch-icon-152x152.png": 152,
        "apple-touch-icon-120x120.png": 120,
        "favicon.png": 64,
        "favicon-32x32.png": 32,
        "AppIcon60x60@2x.png": 120,
        "AppIcon60x60@3x.png": 180,
        "AppIcon76x76@2x.png": 152,
        "AppIcon83.5x83.5@2x.png": 167
    }

    # Save to both root and SERIES_DIR
    target_dirs = [".", SERIES_DIR, IOS_DIR]
    for d in target_dirs:
        for fname, sz in sizes.items():
            resized = master_icon.resize((sz, sz), Image.Resampling.LANCZOS)
            # Remove alpha for Apple Touch Icon as iOS prefers RGB
            if "apple-touch-icon" in fname or "AppIcon" in fname:
                resized = resized.convert("RGB")
            out_path = os.path.join(d, fname)
            resized.save(out_path)

        # Save header logo
        header_logo.save(os.path.join(d, "logo_header.png"))

    # Also save favicon.ico
    master_icon.resize((32, 32), Image.Resampling.LANCZOS).convert("RGBA").save("favicon.ico")
    master_icon.resize((32, 32), Image.Resampling.LANCZOS).convert("RGBA").save(os.path.join(SERIES_DIR, "favicon.ico"))

    print("[✓] Generated all Apple HIG icon resolutions and transparent header logo!")

    # --- 4. Web App Manifest ---
    manifest_content = """{
  "name": "KDP Books Hub",
  "short_name": "KDP Hub",
  "description": "Multi-Book and Multi-Volume KDP Manager with Real-Time Cloud Sync",
  "start_url": "kdp_books_hub.html",
  "display": "standalone",
  "background_color": "#0D1117",
  "theme_color": "#0D1117",
  "orientation": "portrait",
  "icons": [
    {
      "src": "icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "apple-touch-icon.png",
      "sizes": "180x180",
      "type": "image/png"
    }
  ]
}
"""
    with open("manifest.json", "w", encoding="utf-8") as f:
        f.write(manifest_content)
    with open(os.path.join(SERIES_DIR, "manifest.json"), "w", encoding="utf-8") as f:
        f.write(manifest_content)
    print("[✓] Generated manifest.json in root and series directory.")

if __name__ == "__main__":
    generate_assets()
