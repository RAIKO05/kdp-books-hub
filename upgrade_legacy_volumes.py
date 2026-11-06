"""
upgrade_legacy_volumes.py
Upgrades the 4 legacy volumes to the advanced Interlocking Forensic Sudoku Mind Game System:
1. The_Detectives_Case_Files_Series / Volume 1 (Blackwood Files)
2. The_Detectives_Case_Files_Series / Volume 2 (Royal Airship Enigma)
3. The_Detectives_Case_Files_Series / Volume 3 (Venetian Masquerade)
4. Project_X / Volume 1 (The Terminal)
"""

import os
import json
import pymupdf
from industrial_book_engine import build_interlocking_book
from luxury_cover_engine import generate_luxury_cover
from build_mega_catalog_100 import generate_themes_for_volume

legacy_targets = [
    {
        "series": "The Detective's Case Files",
        "vol_num": 1,
        "title": "The Blackwood Manor Murders",
        "subtitle": "35 Multi-Game Murder Mystery Dossiers: Sudoku Keys, Ciphers, Alibi Logic Grids & State Arrest Warrants",
        "dir": "The_Detectives_Case_Files_Series/Volume_1_Blackwood_Files",
        "accent": "#D4AF37",
        "theme": "Midnight Noir & Gold"
    },
    {
        "series": "The Detective's Case Files",
        "vol_num": 2,
        "title": "The Royal Airship Enigma",
        "subtitle": "35 Multi-Game Murder Mystery Dossiers: Sudoku Keys, Ciphers, Alibi Logic Grids & State Arrest Warrants",
        "dir": "The_Detectives_Case_Files_Series/Volume_2_Royal_Airship_Enigma",
        "accent": "#2A9D8F",
        "theme": "Imperial Emerald & Gold"
    },
    {
        "series": "The Detective's Case Files",
        "vol_num": 3,
        "title": "The Venetian Masquerade",
        "subtitle": "35 Multi-Game Murder Mystery Dossiers: Sudoku Keys, Ciphers, Alibi Logic Grids & State Arrest Warrants",
        "dir": "The_Detectives_Case_Files_Series/Volume_3_Venetian_Masquerade",
        "accent": "#9D0208",
        "theme": "Deep Velvet Burgundy & Gold"
    },
    {
        "series": "Project X",
        "vol_num": 1,
        "title": "Project X: The Terminal",
        "subtitle": "35 Multi-Game Murder Mystery Dossiers: Sudoku Keys, Ciphers, Alibi Logic Grids & State Arrest Warrants",
        "dir": "Project_X/Volume_1_The_Terminal",
        "accent": "#D90429",
        "theme": "Cosmic Void & Martian Red Oxide"
    }
]

def upgrade():
    print("=" * 75)
    print("   UPGRADING LEGACY BOOKS TO INTERLOCKING FORENSIC SUDOKU SYSTEM")
    print("=" * 75)

    for item in legacy_targets:
        print(f"\n[*] Upgrading: {item['series']} - Vol {item['vol_num']}: {item['title']}...")
        themes = generate_themes_for_volume(item["series"], item["vol_num"], item["title"])
        
        # 1. Compile 176-page interior with Sudoku keys, ciphers & logic grids
        build_interlocking_book(
            series_name=item["series"],
            vol_num=item["vol_num"],
            book_title=item["title"],
            subtitle=item["subtitle"],
            themes=themes,
            out_dir=item["dir"],
            accent_hex=item["accent"],
            cover_theme=item["theme"]
        )

        # 2. Compile bespoke luxury cover wrap
        cov_pdf = os.path.join(item["dir"], "cover_wrap_6x9.pdf")
        generate_luxury_cover({
            "series": item["series"],
            "vol_number": item["vol_num"],
            "title": item["title"],
            "accent_hex": item["accent"]
        }, cov_pdf)

        # 3. Render 150 DPI previews
        doc = pymupdf.open(cov_pdf)
        page = doc[0]
        rect = page.rect
        W, H = rect.width, rect.height

        wrap_pix = page.get_pixmap(dpi=100)
        wrap_pix.save(os.path.join(item["dir"], "cover_wrap_preview.png"))

        x0 = (6.125 + 0.396) / 12.646 * W
        x1 = 12.521 / 12.646 * W
        y0 = 0.125 / 9.250 * H
        y1 = 9.125 / 9.250 * H
        front_pix = page.get_pixmap(clip=pymupdf.Rect(x0, y0, x1, y1), dpi=150)
        front_pix.save(os.path.join(item["dir"], "cover_front_preview.png"))
        doc.close()

        print(f"  [✓] Successfully upgraded {item['title']} to Sudoku Key Architecture!")

    print("\n[✓] All 4 legacy volumes successfully upgraded!")

if __name__ == "__main__":
    upgrade()
