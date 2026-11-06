"""
regenerate_all_100_covers.py
Recompiles all 100 book covers across the 7 series with bespoke architectural layouts,
series-specific typography, and story-tailored vector artwork!
"""

import os
import json
import time
import pymupdf
from luxury_cover_engine import generate_luxury_cover

CATALOG_PATH = "catalog.json"

def run_regenerate():
    print("=" * 75)
    print("   REGENERATING 100 BESPOKE LUXURY COVERS (STORY-SPECIFIC ARTWORK)")
    print("=" * 75)
    t0 = time.time()

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    print(f"Loaded {len(catalog)} books from catalog.json.")
    success_count = 0

    for idx, book in enumerate(catalog):
        series = book.get("series", "")
        vol_num = book.get("vol_number", 1)
        title = book.get("title", "")
        cov_pdf = book.get("pdf_cover_url")
        front_img = book.get("cover_img_url")
        wrap_img = book.get("cover_wrap_img_url")

        if not cov_pdf:
            print(f"[!] Warning: Missing pdf_cover_url for book {title}")
            continue

        book_dir = os.path.dirname(cov_pdf)
        os.makedirs(book_dir, exist_ok=True)

        # 1. Compile bespoke vector cover wrap PDF
        generate_luxury_cover(book, cov_pdf)

        # 2. Render high-res previews using PyMuPDF
        doc = pymupdf.open(cov_pdf)
        page = doc[0]
        rect = page.rect
        W, H = rect.width, rect.height

        # Full wrap preview
        if wrap_img:
            wrap_pix = page.get_pixmap(dpi=100)
            wrap_pix.save(wrap_img)

        # Exact front cover crop (6" x 9" ratio)
        if front_img:
            x0 = (6.125 + 0.396) / 12.646 * W
            x1 = 12.521 / 12.646 * W
            y0 = 0.125 / 9.250 * H
            y1 = 9.125 / 9.250 * H
            front_pix = page.get_pixmap(clip=pymupdf.Rect(x0, y0, x1, y1), dpi=150)
            front_pix.save(front_img)

        doc.close()
        success_count += 1
        if (idx + 1) % 10 == 0 or idx == len(catalog) - 1:
            print(f"  [✓] Processed {idx + 1}/{len(catalog)} covers ({series} - Vol {vol_num})")

    elapsed = round(time.time() - t0, 2)
    print("=" * 75)
    print(f"[SUCCESS] All {success_count} bespoke luxury covers recompiled and rendered in {elapsed}s!")
    print("=" * 75)

if __name__ == "__main__":
    run_regenerate()
