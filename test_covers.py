import json
import os
import pymupdf
from luxury_cover_engine import generate_luxury_cover

with open('catalog.json', encoding='utf-8') as f:
    cat = json.load(f)

samples = {}
for b in cat:
    s = b['series']
    if s not in samples:
        samples[s] = b

os.makedirs('temp_cover_tests', exist_ok=True)

for s, b in samples.items():
    s_clean = s.replace(' ', '_').replace("'", '')
    out_pdf = f'temp_cover_tests/{s_clean}_cover.pdf'
    generate_luxury_cover(b, out_pdf)
    
    doc = pymupdf.open(out_pdf)
    page = doc[0]
    rect = page.rect
    W, H = rect.width, rect.height
    x0 = (6.125 + 0.396) / 12.646 * W
    x1 = 12.521 / 12.646 * W
    y0 = 0.125 / 9.250 * H
    y1 = 9.125 / 9.250 * H
    pix = page.get_pixmap(clip=pymupdf.Rect(x0, y0, x1, y1), dpi=150)
    out_img = f'temp_cover_tests/{s_clean}_front.png'
    pix.save(out_img)
    print(f'[✓] Compiled test cover for: {s} -> {out_img}')

print('All 7 sample covers compiled successfully!')
