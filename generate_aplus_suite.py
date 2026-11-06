"""
generate_aplus_suite.py
Generates Amazon KDP A+ Content visual assets for all 7 series:
- Module 1: Hero Showcase Banner (970 x 600 px) with 3D Book Mockup & Value Props
- Module 2: Inside the Investigation Flow (970 x 600 px) with real page extractions
- Module 3: 4 Feature Spotlight Tiles (4 x 300 x 300 px) for Amazon 4-Image Grid
- Module 4: Manufacturing Quality & Specs Banner (970 x 300 px)
- Module 5: Collectible Series Lineup (970 x 600 px) with 5 volumes in 3D perspective
- A_Plus_Content_Copy_Guide.txt with headlines, bullets, and image alt text for KDP A+ builder
"""

import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pymupdf

OUTPUT_DIR = "Amazon_A_Plus_Content"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# System Fonts
FONT_TITLE = 'C:/Windows/Fonts/georgiab.ttf'
FONT_SERIF = 'C:/Windows/Fonts/georgia.ttf'
FONT_SANS_BOLD = 'C:/Windows/Fonts/arialbd.ttf'
FONT_SANS = 'C:/Windows/Fonts/arial.ttf'
FONT_MONO = 'C:/Windows/Fonts/consolab.ttf'

def solve_linear_system(A, B):
    n = len(B)
    M = [A[i] + [B[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[max_row] = M[max_row], M[i]
        pivot = M[i][i]
        if abs(pivot) < 1e-10:
            pivot = 1e-10
        for j in range(i, n + 1):
            M[i][j] /= pivot
        for r in range(n):
            if r != i:
                factor = M[r][i]
                for j in range(i, n + 1):
                    M[r][j] -= factor * M[i][j]
    return [M[i][n] for i in range(n)]

def map_quad(src_img, dest_size, dest_pts):
    w, h = src_img.size
    src_pts = [(0, 0), (w, 0), (w, h), (0, h)]
    A = []
    B = []
    for (u, v), (x, y) in zip(src_pts, dest_pts):
        A.append([x, y, 1, 0, 0, 0, -x*u, -y*u])
        B.append(u)
        A.append([0, 0, 0, x, y, 1, -x*v, -y*v])
        B.append(v)
    coeffs = solve_linear_system(A, B)
    return src_img.transform(dest_size, Image.Transform.PERSPECTIVE, coeffs, Image.Resampling.BICUBIC)

def render_3d_book(cover_img, dest_size, center_x, center_y, scale=1.0, spine_color=(15,15,15)):
    """
    Renders an isometric 3D book mockup onto a transparent RGBA image.
    """
    img = Image.new('RGBA', dest_size, (0,0,0,0))
    w, h = cover_img.size
    
    bw = int(220 * scale)
    bh = int(330 * scale)
    spine_w = int(28 * scale)
    
    # Coordinates
    TL = (center_x - bw//2 + spine_w, center_y - bh//2)
    TR = (center_x + bw//2, center_y - bh//2 + 35)
    BR = (center_x + bw//2 - 25, center_y + bh//2 + 35)
    BL = (center_x - bw//2 + spine_w - 25, center_y + bh//2)
    
    # Shadow
    s_img = Image.new('RGBA', dest_size, (0,0,0,0))
    sdraw = ImageDraw.Draw(s_img)
    sdraw.polygon([
        (center_x - bw//2, center_y + bh//2 - 10),
        (center_x + bw//2 + 30, center_y + bh//2 + 25),
        (center_x + bw//2 - 10, center_y + bh//2 + 65),
        (center_x - bw//2 - 40, center_y + bh//2 + 30)
    ], fill=(0, 0, 0, 190))
    s_img = s_img.filter(ImageFilter.GaussianBlur(18 * scale))
    img.alpha_composite(s_img)
    
    # Spine quad
    draw = ImageDraw.Draw(img)
    SP_TL = (center_x - bw//2, center_y - bh//2 + 15)
    SP_TR = TL
    SP_BR = BL
    SP_BL = (center_x - bw//2 - 25, center_y + bh//2 + 15)
    draw.polygon([SP_TL, SP_TR, SP_BR, SP_BL], fill=spine_color)
    
    # Paper edge (bottom)
    draw.polygon([BL, BR, (BR[0]-6, BR[1]+14), (BL[0]-6, BL[1]+14)], fill=(235, 230, 218, 255))
    for off in range(2, 12, 2):
        draw.line([(BL[0]-off//2, BL[1]+off), (BR[0]-off//2, BR[1]+off)], fill=(200, 195, 180, 200), width=1)
        
    # Front cover mapped
    mapped_cover = map_quad(cover_img, dest_size, [TL, TR, BR, BL])
    img.alpha_composite(mapped_cover)
    
    # Subtle front gloss highlight
    gloss = Image.new('RGBA', dest_size, (0,0,0,0))
    gdraw = ImageDraw.Draw(gloss)
    gdraw.polygon([TL, (TL[0]+(TR[0]-TL[0])//3, TL[1]+(TR[1]-TL[1])//3),
                   (BL[0]+(BR[0]-BL[0])//4, BL[1]+(BR[1]-BL[1])//4), BL],
                  fill=(255, 255, 255, 30))
    gloss = gloss.filter(ImageFilter.GaussianBlur(4))
    img.alpha_composite(gloss)
    
    return img

def create_module_1_hero(series_name, book_vol_title, cover_path, theme, out_path):
    """
    Module 1: Standard Image Header with Text (970 x 600 px)
    Hero 3D book mockup + Brand positioning + 4 Pillars
    """
    w, h = 970, 600
    canvas = Image.new('RGBA', (w, h), theme['bg_color'])
    draw = ImageDraw.Draw(canvas)
    
    # Ambient radial gradient on book side
    glow_color = theme['accent_rgb']
    for r in range(450, 0, -25):
        alpha = int(45 * (1 - r/450.0))
        draw.ellipse([(200 - r, 300 - r), (200 + r, 300 + r)], fill=(*glow_color, alpha))
        
    # Subtle geometric tech / filigree frame on border
    draw.rectangle([8, 8, w-9, h-9], outline=(*glow_color, 70), width=1)
    draw.rectangle([14, 14, w-15, h-15], outline=(*glow_color, 40), width=1)
    
    # Render 3D Book on Left
    cover_raw = Image.open(cover_path).convert('RGBA')
    book_layer = render_3d_book(cover_raw, (w, h), center_x=225, center_y=285, scale=1.18, spine_color=theme['spine_color'])
    canvas.alpha_composite(book_layer)
    
    # Right Column Typography
    draw = ImageDraw.Draw(canvas)
    f_eyebrow = ImageFont.truetype(FONT_SANS_BOLD, 11)
    f_h1 = ImageFont.truetype(FONT_TITLE, 26)
    f_sub = ImageFont.truetype(FONT_SERIF, 15)
    f_pill_title = ImageFont.truetype(FONT_SANS_BOLD, 12)
    f_pill_desc = ImageFont.truetype(FONT_SANS, 12)
    f_footer = ImageFont.truetype(FONT_SANS_BOLD, 11)
    
    # Eyebrow Pill
    bx, by = 430, 50
    draw.rounded_rectangle([bx, by, bx + 360, by + 26], radius=6, fill=(*glow_color, 35), outline=(*glow_color, 160), width=1)
    draw.text((bx + 12, by + 6), f"{series_name.upper()} • VOLUME 1", fill=theme['accent_rgb'], font=f_eyebrow)
    
    # Headlines
    draw.text((bx, 90), "NOT JUST A PUZZLE BOOK.", fill=(255, 255, 255), font=f_h1)
    draw.text((bx, 125), theme['hero_subtitle_accent'], fill=theme['accent_rgb'], font=f_h1)
    
    draw.text((bx, 172), theme['hero_pitch_1'], fill=(210, 220, 235), font=f_sub)
    draw.text((bx, 195), theme['hero_pitch_2'], fill=(210, 220, 235), font=f_sub)
    
    # 4 Feature rows
    pillars = [
        ("STAGE I: FORENSIC SUDOKU", "Solve 9x9 grid to unmask 4 shaded Key Cells (Alpha, Beta, Gamma, Delta)."),
        ("STAGE II: PASSKEY CIPHER", "Sum the key digits to unlock the mathematical Caesar shift and decode dying words."),
        ("STAGE III: 100% UNIQUE LOGIC", "Eliminate suspects on the airtight alibi matrix. Verified 0 guesswork by solvers."),
        ("STAGE IV: STATE ARREST WARRANT", "Name the killer, certify the weapon, and indict the perpetrator.")
    ]
    
    py = 236
    for title, desc in pillars:
        draw.rounded_rectangle([bx, py + 2, bx + 8, py + 16], radius=2, fill=theme['accent_rgb'])
        draw.text((bx + 18, py), title, fill=(255, 255, 255), font=f_pill_title)
        draw.text((bx + 18, py + 18), desc, fill=(160, 175, 195), font=f_pill_desc)
        py += 56
        
    # Specs Footer Bar
    draw.rounded_rectangle([bx, 495, 930, 545], radius=8, fill=(20, 28, 45, 220), outline=(*glow_color, 90), width=1)
    draw.text((bx + 16, 511), "176 LARGE-FORMAT PAGES   •   6\" x 9\" TRADE PAPERBACK   •   SOLUTIONS INCLUDED", fill=theme['accent_rgb'], font=f_footer)
    
    canvas.save(out_path, format='PNG', quality=95)
    print(f"  [✓] Created Module 1: {os.path.basename(out_path)}")

def create_module_2_investigation_flow(pdf_path, theme, out_path):
    """
    Module 2: Inside the Investigation (970 x 600 px)
    Displays the 4 actual interior pages in an interlocking flow.
    """
    w, h = 970, 600
    canvas = Image.new('RGBA', (w, h), theme['bg_color'])
    draw = ImageDraw.Draw(canvas)
    
    # Header
    f_h1 = ImageFont.truetype(FONT_TITLE, 24)
    f_sub = ImageFont.truetype(FONT_SANS, 13)
    f_card_num = ImageFont.truetype(FONT_SANS_BOLD, 11)
    f_card_title = ImageFont.truetype(FONT_SANS_BOLD, 12)
    f_card_desc = ImageFont.truetype(FONT_SANS, 11)
    
    draw.text((40, 30), "THE 4-STAGE INTERLOCKING EVIDENCE SYSTEM", fill=(255, 255, 255), font=f_h1)
    draw.text((40, 62), "Every investigation is a continuous chain of forensic deduction — no isolated, repetitive puzzles.", fill=theme['accent_rgb'], font=f_sub)
    
    # Extract pages 9, 10, 11, 12 from PDF
    doc = pymupdf.open(pdf_path)
    page_imgs = []
    for p in range(8, 12):
        pix = doc[p].get_pixmap(dpi=150)
        p_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples).convert('RGBA')
        page_imgs.append(p_img)
    doc.close()
    
    stage_meta = [
        ("STAGE 1: SUDOKU", "Unmask 4 Key Cells", "Solve 9x9 grid to find shaded passkey cells."),
        ("STAGE 2: CIPHER", "Decode Dying Dispatch", "Sum of key cells unlocks Caesar shift."),
        ("STAGE 3: ALIBI MATRIX", "100% Unique Solution", "Pure deduction grid. Zero guesswork."),
        ("STAGE 4: ARREST WARRANT", "State Indictment", "Synthesize evidence to convict the killer.")
    ]
    
    # 4 Cards Layout
    card_w = 205
    card_h = 440
    gap = 25
    start_x = 40
    start_y = 105
    
    for i in range(4):
        cx = start_x + i * (card_w + gap)
        cy = start_y
        
        # Soft card shadow
        s_img = Image.new('RGBA', (w, h), (0,0,0,0))
        sdraw = ImageDraw.Draw(s_img)
        sdraw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=12, fill=(0, 0, 0, 160))
        s_img = s_img.filter(ImageFilter.GaussianBlur(12))
        canvas.alpha_composite(s_img)
        
        # Card Background
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=12, fill=(18, 24, 38, 255), outline=(*theme['accent_rgb'], 100), width=1)
        
        # Card Top Header Badge
        draw.rounded_rectangle([cx + 10, cy + 12, cx + card_w - 10, cy + 34], radius=6, fill=(*theme['accent_rgb'], 40), outline=(*theme['accent_rgb'], 140), width=1)
        draw.text((cx + 18, cy + 16), stage_meta[i][0], fill=theme['accent_rgb'], font=f_card_num)
        
        # Book Page Miniature with crisp border
        pw = card_w - 24
        ph = int(pw * 1.5)
        p_crop = page_imgs[i].resize((pw, ph), Image.Resampling.LANCZOS)
        
        # Add thin border to page thumbnail
        p_frame = Image.new('RGBA', (pw + 2, ph + 2), (200, 200, 200, 255))
        p_frame.paste(p_crop, (1, 1))
        canvas.paste(p_frame, (cx + 11, cy + 44))
        
        # Bottom Title & Description
        draw.text((cx + 12, cy + 44 + ph + 10), stage_meta[i][1], fill=(255, 255, 255), font=f_card_title)
        draw.text((cx + 12, cy + 44 + ph + 28), stage_meta[i][2], fill=(160, 175, 195), font=f_card_desc)
        
        # Connecting Arrow (between cards)
        if i < 3:
            arrow_x = cx + card_w + 5
            arrow_y = cy + card_h // 2
            draw.text((arrow_x, arrow_y - 10), "➔", fill=theme['accent_rgb'], font=ImageFont.truetype(FONT_TITLE, 18))
            
    # Bottom Instruction Pill
    draw.rounded_rectangle([start_x, 560, w - start_x, 586], radius=6, fill=(20, 28, 45, 255), outline=(*theme['accent_rgb'], 80))
    draw.text((start_x + 14, 566), "FLOW: Solve Grid ➔ Extract Shaded Numbers ➔ Sum Key Digits ➔ Decrypt Dispatch ➔ Eliminate Suspects ➔ Sign Warrant", fill=theme['accent_rgb'], font=f_card_desc)
    
    canvas.save(out_path, format='PNG', quality=95)
    print(f"  [✓] Created Module 2: {os.path.basename(out_path)}")

def create_module_3_tiles(pdf_path, theme, out_dir):
    """
    Module 3: Four 300 x 300 px Feature Tiles for Amazon 4-Image Grid
    """
    doc = pymupdf.open(pdf_path)
    pages = [doc[p].get_pixmap(dpi=150) for p in range(8, 12)]
    doc.close()
    
    tile_configs = [
        ("Module_3_Feature_1_Sudoku_300x300.png", "STAGE 1: FORENSIC SUDOKU", "Extract 4 Key Cells", 0, "Solve the 9x9 grid to unmask the 4 shaded key cells (Alpha, Beta, Gamma, Delta)."),
        ("Module_3_Feature_2_Cipher_300x300.png", "STAGE 2: PASSKEY CIPHER", "Decode Dying Dispatch", 1, "Sum of the 4 extracted key digits determines the Caesar shift formula."),
        ("Module_3_Feature_3_LogicGrid_300x300.png", "STAGE 3: ALIBI MATRIX", "100% Unique Solution", 2, "Airtight deduction grid verified with zero ambiguity and zero guessing."),
        ("Module_3_Feature_4_ArrestWarrant_300x300.png", "STAGE 4: ARREST WARRANT", "Official Indictment", 3, "Synthesize physical evidence, name the culprit, and close the case.")
    ]
    
    f_pill = ImageFont.truetype(FONT_SANS_BOLD, 9)
    f_title = ImageFont.truetype(FONT_TITLE, 13)
    f_desc = ImageFont.truetype(FONT_SANS, 10)
    
    for filename, eyebrow, title, page_idx, desc in tile_configs:
        out_p = os.path.join(out_dir, filename)
        tile = Image.new('RGBA', (300, 300), theme['bg_color'])
        draw = ImageDraw.Draw(tile)
        
        # Border
        draw.rectangle([4, 4, 295, 295], outline=(*theme['accent_rgb'], 90), width=1)
        
        # Header Eyebrow
        draw.rounded_rectangle([12, 12, 288, 30], radius=4, fill=(*theme['accent_rgb'], 35), outline=(*theme['accent_rgb'], 130), width=1)
        draw.text((18, 15), eyebrow, fill=theme['accent_rgb'], font=f_pill)
        
        # Page thumbnail
        pix = pages[page_idx]
        p_raw = Image.frombytes("RGB", [pix.width, pix.height], pix.samples).convert('RGBA')
        # Center-crop top section of page
        crop_box = (int(pix.width * 0.08), int(pix.height * 0.12), int(pix.width * 0.92), int(pix.height * 0.68))
        cropped = p_raw.crop(crop_box)
        thumb = cropped.resize((276, 170), Image.Resampling.LANCZOS)
        
        # Soft shadow behind thumbnail
        t_box = Image.new('RGBA', (300, 300), (0,0,0,0))
        tdraw = ImageDraw.Draw(t_box)
        tdraw.rectangle([12, 38, 288, 210], fill=(0, 0, 0, 160))
        t_box = t_box.filter(ImageFilter.GaussianBlur(6))
        tile.alpha_composite(t_box)
        
        tile.paste(thumb, (12, 38))
        draw = ImageDraw.Draw(tile)
        draw.rectangle([11, 37, 289, 209], outline=(*theme['accent_rgb'], 120), width=1)
        
        # Title and Description below
        draw.text((12, 218), title, fill=(255, 255, 255), font=f_title)
        
        # Wrap description
        words = desc.split(' ')
        lines = []
        cur = ""
        for w in words:
            if len(cur + " " + w) < 46:
                cur += (" " if cur else "") + w
            else:
                lines.append(cur)
                cur = w
        if cur: lines.append(cur)
        
        ty = 238
        for line in lines[:3]:
            draw.text((12, ty), line, fill=(160, 175, 195), font=f_desc)
            ty += 14
            
        tile.save(out_p, format='PNG', quality=95)
        print(f"  [✓] Created Tile: {filename}")

def create_module_4_specs_banner(series_name, theme, out_path):
    """
    Module 4: Premium Print & Publishing Standards Banner (970 x 300 px)
    """
    w, h = 970, 300
    canvas = Image.new('RGBA', (w, h), theme['bg_color'])
    draw = ImageDraw.Draw(canvas)
    
    # Outer frame
    draw.rectangle([8, 8, w-9, h-9], outline=(*theme['accent_rgb'], 80), width=1)
    draw.rectangle([14, 14, w-15, h-15], outline=(*theme['accent_rgb'], 40), width=1)
    
    f_h1 = ImageFont.truetype(FONT_TITLE, 22)
    f_sub = ImageFont.truetype(FONT_SANS, 12)
    f_badge_h = ImageFont.truetype(FONT_SANS_BOLD, 12)
    f_badge_p = ImageFont.truetype(FONT_SANS, 11)
    
    draw.text((40, 28), "PREMIUM MANUFACTURING & PRINTING SPECIFICATIONS", fill=(255, 255, 255), font=f_h1)
    draw.text((40, 58), f"Every volume in {series_name} is crafted to professional publishing standards.", fill=theme['accent_rgb'], font=f_sub)
    
    # 5 Feature Badges
    badges = [
        ("6\" x 9\" TRADE FORMAT", "Standard bookstore trim.", "Spacious grids designed for comfortable solving without eye strain."),
        ("176 CREAM PAGES", "High-opacity paper.", "Prevents ink bleed-through from gel pens, ballpoints, and pencils."),
        ("1 UNIQUE SOLUTION", "100% Deductive logic.", "Every grid verified by mathematical constraint solvers. Zero guessing."),
        ("FULL CASE DEBRIEFS", "Step-by-step solutions.", "Comprehensive evidence walkthroughs and magistrate notes in back."),
        ("LAY-FLAT BINDING", "Spine margin allowance.", "Generous gutter margins ensure grids stay flat while writing.")
    ]
    
    bw = 170
    bh = 175
    gap = 10
    start_x = 35
    start_y = 90
    
    for i, (b_title, b_sub, b_body) in enumerate(badges):
        bx = start_x + i * (bw + gap)
        by = start_y
        
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8, fill=(18, 25, 40, 255), outline=(*theme['accent_rgb'], 90), width=1)
        
        # Pill top
        draw.rounded_rectangle([bx + 8, by + 10, bx + bw - 8, by + 30], radius=4, fill=(*theme['accent_rgb'], 35), outline=(*theme['accent_rgb'], 120), width=1)
        draw.text((bx + 12, by + 14), b_title, fill=theme['accent_rgb'], font=ImageFont.truetype(FONT_SANS_BOLD, 9))
        
        draw.text((bx + 12, by + 38), b_sub, fill=(255, 255, 255), font=f_badge_h)
        
        # Word wrap
        words = b_body.split(' ')
        lines = []
        cur = ""
        for wrd in words:
            if len(cur + " " + wrd) < 22:
                cur += (" " if cur else "") + wrd
            else:
                lines.append(cur)
                cur = wrd
        if cur: lines.append(cur)
        
        ly = by + 60
        for line in lines[:6]:
            draw.text((bx + 12, ly), line, fill=(160, 175, 195), font=f_badge_p)
            ly += 16
            
    canvas.save(out_path, format='PNG', quality=95)
    print(f"  [✓] Created Module 4: {os.path.basename(out_path)}")

def create_module_5_series_lineup(series_name, volume_covers, theme, out_path):
    """
    Module 5: Collectible Series Lineup Banner (970 x 600 px)
    Renders 5 volumes fanned out in 3D with series comparison table below.
    """
    w, h = 970, 600
    canvas = Image.new('RGBA', (w, h), theme['bg_color'])
    draw = ImageDraw.Draw(canvas)
    
    # Outer frame
    draw.rectangle([8, 8, w-9, h-9], outline=(*theme['accent_rgb'], 70), width=1)
    
    f_h1 = ImageFont.truetype(FONT_TITLE, 24)
    f_sub = ImageFont.truetype(FONT_SANS, 13)
    f_vol_title = ImageFont.truetype(FONT_SANS_BOLD, 11)
    f_table_h = ImageFont.truetype(FONT_SANS_BOLD, 11)
    f_table_body = ImageFont.truetype(FONT_SANS, 11)
    
    draw.text((40, 25), f"BUILD YOUR COLLECTIBLE {series_name.upper()} LIBRARY", fill=(255, 255, 255), font=f_h1)
    draw.text((40, 58), "Each volume contains 35 brand-new, standalone forensic investigations. Collect them all!", fill=theme['accent_rgb'], font=f_sub)
    
    # Render 5 books in 3D lineup
    start_x = 115
    book_spacing = 180
    book_y = 230
    
    for i in range(min(5, len(volume_covers))):
        c_path, v_name = volume_covers[i]
        if os.path.exists(c_path):
            c_raw = Image.open(c_path).convert('RGBA')
            bl = render_3d_book(c_raw, (w, h), center_x=start_x + i * book_spacing, center_y=book_y, scale=0.72, spine_color=theme['spine_color'])
            canvas.alpha_composite(bl)
            
            # Volume Label under book
            draw = ImageDraw.Draw(canvas)
            draw.rounded_rectangle([start_x + i * book_spacing - 65, 375, start_x + i * book_spacing + 65, 396], radius=4, fill=(20, 28, 45, 255), outline=(*theme['accent_rgb'], 100), width=1)
            draw.text((start_x + i * book_spacing - 55, 380), f"VOL. {i+1}: {v_name[:12]}", fill=theme['accent_rgb'], font=f_vol_title)
            
    # Comparison Spec Matrix at Bottom
    table_y = 425
    table_w = 890
    table_h = 145
    draw.rounded_rectangle([40, table_y, 40 + table_w, table_y + table_h], radius=10, fill=(16, 22, 35, 255), outline=(*theme['accent_rgb'], 90), width=1)
    
    # Table Header Row
    draw.rounded_rectangle([40, table_y, 40 + table_w, table_y + 32], radius=10, fill=(25, 35, 55, 255))
    draw.line([(40, table_y + 32), (40 + table_w, table_y + 32)], fill=(*theme['accent_rgb'], 100), width=1)
    
    cols = ["VOLUME", "THEME / SETTING", "CASES", "CHALLENGES", "PAGE COUNT", "LIST PRICE"]
    col_x = [55, 170, 480, 570, 710, 830]
    
    for j, c in enumerate(cols):
        draw.text((col_x[j], table_y + 9), c, fill=theme['accent_rgb'], font=f_table_h)
        
    rows = [
        ("Volume 1", "Foundational Crime Dossiers & Manor Murders", "35 Cases", "140 Puzzles", "176 Pages", "$12.99"),
        ("Volume 2", "High-Stakes Expeditions & Transits", "35 Cases", "140 Puzzles", "176 Pages", "$12.99"),
        ("Volume 3", "Conspiracies, Masquerades & Heists", "35 Cases", "140 Puzzles", "176 Pages", "$12.99"),
        ("Volumes 4-15", "Complete 15-Book Full Season Library", "525 Cases", "2,100 Puzzles", "2,640 Pages", "$12.99 ea")
    ]
    
    ry = table_y + 38
    for r in rows:
        for j, val in enumerate(r):
            draw.text((col_x[j], ry), val, fill=(255, 255, 255) if j==0 else (175, 190, 210), font=f_table_body)
        ry += 26
        
    canvas.save(out_path, format='PNG', quality=95)
    print(f"  [✓] Created Module 5: {os.path.basename(out_path)}")

def create_aplus_copy_guide(series_name, theme, out_path):
    """
    Creates ready-to-paste text copy for Amazon KDP A+ Content Builder.
    """
    content = f"""================================================================================
AMAZON KDP A+ CONTENT COPY GUIDE: {series_name.upper()}
================================================================================

MODULE 1: Standard Image Header with Text (970 x 600 px)
--------------------------------------------------------------------------------
Image File: Module_1_Hero_Showcase_970x600.png
Image Alt-Text: {series_name} Volume 1 3D Book Mockup with Forensic Sudoku and Ciphers
Headline: Not Just a Puzzle Book. An Interlocking Crime Scene Investigation.
Body Text:
Step into {series_name}, where every investigation is an authentic 4-stage forensic case file. 
Unlike ordinary puzzle books that repeat the same isolated grids, every single deduction here 
is mathematically linked: solve the Sudoku grid to unlock the cipher passkey, decode the dying 
suspect dispatch, eliminate innocent alibis on the logic matrix, and indict the true perpetrator!

================================================================================
MODULE 2: Inside the Investigation (970 x 600 px)
--------------------------------------------------------------------------------
Image File: Module_2_Investigation_Flow_970x600.png
Image Alt-Text: The 4-Stage Interlocking Evidence System Diagram
Headline: The 4-Stage Interlocking Evidence Architecture
Body Text:
- Stage 1 (Forensic Sudoku): Solve the 9x9 grid to unmask 4 shaded Key Cells.
- Stage 2 (Passkey Cipher): Sum the key digits to unlock the Caesar shift and decode secret words.
- Stage 3 (Alibi Logic Matrix): 100% mathematically proven unique solution. Zero guessing.
- Stage 4 (State Arrest Warrant): Synthesize the physical evidence and sign the warrant!

================================================================================
MODULE 3: Four Image & Text Modules (4 x 300 x 300 px)
--------------------------------------------------------------------------------
Tile 1: Module_3_Feature_1_Sudoku_300x300.png
Alt-Text: Stage 1 Forensic Sudoku Key Cells
Headline: Stage 1: Forensic Sudoku Keys
Text: 9x9 grid concealing 4 shaded passkey cells (Alpha, Beta, Gamma, Delta).

Tile 2: Module_3_Feature_2_Cipher_300x300.png
Alt-Text: Stage 2 Passkey Cryptogram
Headline: Stage 2: Encrypted Dispatches
Text: Decrypt intercepted transmissions using the mathematical Sudoku key sum.

Tile 3: Module_3_Feature_3_LogicGrid_300x300.png
Alt-Text: Stage 3 Airtight Deduction Grid
Headline: Stage 3: Airtight Alibi Matrix
Text: Pure deductive logic mathematically verified to yield exactly 1 unique solution.

Tile 4: Module_3_Feature_4_ArrestWarrant_300x300.png
Alt-Text: Stage 4 Official State Arrest Warrant
Headline: Stage 4: Official Arrest Warrant
Text: Close the case file by naming the true culprit, murder weapon, and motive.

================================================================================
MODULE 4: Standard Technical Specifications Banner (970 x 300 px)
--------------------------------------------------------------------------------
Image File: Module_4_Quality_Specs_Banner_970x300.png
Image Alt-Text: Premium Quality Print Specifications 6x9 Trade Paperback 176 Pages
Headline: Engineered for Serious Puzzle Solvers & Mystery Buffs
Body Text:
Printed on 176 large-format, high-opacity cream pages inside a 6" x 9" trade paperback. 
Designed with generous gutter margins for flat-lay solving. Complete solutions and 
investigator debriefs included in the back of every volume.

================================================================================
MODULE 5: Collectible Series Lineup Banner (970 x 600 px)
--------------------------------------------------------------------------------
Image File: Module_5_Series_Lineup_970x600.png
Image Alt-Text: Complete {series_name} Multi-Volume Library Collection
Headline: Collect the Entire {series_name} Series
Body Text:
Continue your detective journey across all 15 collectible volumes. Each book contains 
35 brand-new, standalone crime investigations totaling 140 multi-game puzzles.
================================================================================
"""
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [✓] Created Copy Guide: {os.path.basename(out_path)}")

# 7 SERIES MASTER DEFINITIONS
SERIES_CONFIGS = [
    {
        "id": "01_The_Detectives_Case_Files",
        "name": "The Detective's Case Files",
        "hero_book": "The_Detectives_Case_Files_Series/Volume_1_Blackwood_Files",
        "theme": {
            "bg_color": (11, 19, 32, 255),
            "accent_rgb": (212, 175, 55), # Gold
            "spine_color": (18, 15, 12, 255),
            "hero_subtitle_accent": "AN INTERLOCKING CRIME SCENE.",
            "hero_pitch_1": "Step into 1920s London as a consulting detective. Crack 35 multi-stage",
            "hero_pitch_2": "investigations where every single puzzle is forensic evidence."
        },
        "lineup": [
            ("The_Detectives_Case_Files_Series/Volume_1_Blackwood_Files/cover_front_preview.png", "Blackwood Manor"),
            ("The_Detectives_Case_Files_Series/Volume_2_Royal_Airship_Enigma/cover_front_preview.png", "Royal Airship"),
            ("The_Detectives_Case_Files_Series/Volume_3_Venetian_Masquerade/cover_front_preview.png", "Venice Mask"),
            ("The_Detectives_Case_Files_Series/Volume_4_Fog_Over_Whitechapel/cover_front_preview.png", "Whitechapel Fog"),
            ("The_Detectives_Case_Files_Series/Volume_5_Balmoral_Castle_Conspiracy/cover_front_preview.png", "Balmoral Castle")
        ]
    },
    {
        "id": "02_Project_X",
        "name": "Project X",
        "hero_book": "Project_X/Volume_1_The_Terminal",
        "theme": {
            "bg_color": (8, 12, 20, 255),
            "accent_rgb": (252, 163, 17), # Neon Amber
            "spine_color": (20, 10, 5, 255),
            "hero_subtitle_accent": "CYBERPUNK SCI-FI DEDUCTION.",
            "hero_pitch_1": "Investigate corporate sabotage and lab containment breaches on Mars.",
            "hero_pitch_2": "35 interlocking space dossiers engineered for sci-fi sleuths."
        },
        "lineup": [
            ("Project_X/Volume_1_The_Terminal/cover_front_preview.png", "The Terminal"),
            ("Project_X/Volume_2_The_Sub-Terra_Core/cover_front_preview.png", "Sub-Terra Core"),
            ("Project_X/Volume_3_Orbital_Elevator_Sabotage/cover_front_preview.png", "Elevator Sabotage"),
            ("Project_X/Volume_4_Titan_Cryo_Breach/cover_front_preview.png", "Titan Breach"),
            ("Project_X/Volume_5_Bio_Synth_Catastrophe/cover_front_preview.png", "Bio-Synth Lab")
        ]
    },
    {
        "id": "03_The_Ravencrest_Chronicles",
        "name": "The Ravencrest Chronicles",
        "hero_book": "The_Ravencrest_Chronicles/Volume_1_The_Blackwood_Curse",
        "theme": {
            "bg_color": (16, 13, 22, 255),
            "accent_rgb": (157, 78, 221), # Amethyst Purple
            "spine_color": (18, 12, 25, 255),
            "hero_subtitle_accent": "VICTORIAN GOTHIC MANOR MYSTERY.",
            "hero_pitch_1": "Uncover dark seances, poisoned wills, and ancestral crypt curses.",
            "hero_pitch_2": "35 atmospheric gothic whodunits with interlocking key codes."
        },
        "lineup": [
            ("The_Ravencrest_Chronicles/Volume_1_The_Blackwood_Curse/cover_front_preview.png", "Blackwood Curse"),
            ("The_Ravencrest_Chronicles/Volume_2_Seance_at_Wyndcliff_Hall/cover_front_preview.png", "Wyndcliff Hall"),
            ("The_Ravencrest_Chronicles/Volume_3_Clockwork_Doll_of_Ravenswood/cover_front_preview.png", "Clockwork Doll"),
            ("The_Ravencrest_Chronicles/Volume_4_Portrait_of_Lady_Eleanor/cover_front_preview.png", "Lady Eleanor"),
            ("The_Ravencrest_Chronicles/Volume_5_Crypt_of_Screaming_Gargoyles/cover_front_preview.png", "Crypt Gargoyles")
        ]
    },
    {
        "id": "04_The_Bletchley_Protocols",
        "name": "The Bletchley Protocols",
        "hero_book": "The_Bletchley_Protocols/Volume_1_The_Enigma_Redux",
        "theme": {
            "bg_color": (14, 20, 26, 255),
            "accent_rgb": (46, 196, 182), # Enigma Teal
            "spine_color": (12, 18, 22, 255),
            "hero_subtitle_accent": "COLD WAR CODEBREAKING & ESPIONAGE.",
            "hero_pitch_1": "Intercept microdots, decode Enigma rotors, and expose MI6 moles.",
            "hero_pitch_2": "35 classified counter-intelligence investigations."
        },
        "lineup": [
            ("The_Bletchley_Protocols/Volume_1_The_Enigma_Redux/cover_front_preview.png", "Enigma Redux"),
            ("The_Bletchley_Protocols/Volume_2_The_Zimmermann_Shadow/cover_front_preview.png", "Zimmermann"),
            ("The_Bletchley_Protocols/Volume_3_The_Cables_of_Murmansk/cover_front_preview.png", "Murmansk Cables"),
            ("The_Bletchley_Protocols/Volume_4_The_Viennese_Intercept/cover_front_preview.png", "Viennese Intercept"),
            ("The_Bletchley_Protocols/Volume_5_The_Petrograd_Cipher/cover_front_preview.png", "Petrograd Cipher")
        ]
    },
    {
        "id": "05_Crypt_of_the_Pharaohs",
        "name": "Crypt of the Pharaohs",
        "hero_book": "Crypt_of_the_Pharaohs/Volume_1_Tomb_of_the_Golden_Scarab",
        "theme": {
            "bg_color": (15, 23, 34, 255),
            "accent_rgb": (233, 196, 106), # Pharaoh Gold
            "spine_color": (22, 18, 12, 255),
            "hero_subtitle_accent": "ANCIENT TOMBS & ARCHAEOLOGICAL CURSES.",
            "hero_pitch_1": "Expeditions into the Valley of the Kings, hieroglyphic ciphers,",
            "hero_pitch_2": "and 35 mysterious deaths in sealed burial chambers."
        },
        "lineup": [
            ("Crypt_of_the_Pharaohs/Volume_1_Tomb_of_the_Golden_Scarab/cover_front_preview.png", "Golden Scarab"),
            ("Crypt_of_the_Pharaohs/Volume_2_The_Curse_of_Nefertiti/cover_front_preview.png", "Nefertiti Curse"),
            ("Crypt_of_the_Pharaohs/Volume_3_Whispers_of_the_Sphinx/cover_front_preview.png", "Sphinx Whispers"),
            ("Crypt_of_the_Pharaohs/Volume_4_The_Hieroglyph_Code/cover_front_preview.png", "Hieroglyph Code"),
            ("Crypt_of_the_Pharaohs/Volume_5_Labyrinth_of_Anubis/cover_front_preview.png", "Anubis Labyrinth")
        ]
    },
    {
        "id": "06_The_Blackwood_Asylum_Files",
        "name": "The Blackwood Asylum Files",
        "hero_book": "The_Blackwood_Asylum_Files/Volume_1_Solitary_Confinement_Escape",
        "theme": {
            "bg_color": (19, 23, 26, 255),
            "accent_rgb": (230, 57, 70), # Sanitarium Red
            "spine_color": (25, 12, 15, 255),
            "hero_subtitle_accent": "EDWARDIAN PSYCHOLOGICAL THRILLERS.",
            "hero_pitch_1": "Locked isolation wards, phantom patients, and corrupt medical doctors.",
            "hero_pitch_2": "35 high-tension psychiatric mystery dossiers."
        },
        "lineup": [
            ("The_Blackwood_Asylum_Files/Volume_1_Solitary_Confinement_Escape/cover_front_preview.png", "Solitary Escape"),
            ("The_Blackwood_Asylum_Files/Volume_2_The_Lobotomy_Ward_Secret/cover_front_preview.png", "Lobotomy Ward"),
            ("The_Blackwood_Asylum_Files/Volume_3_Phantom_in_Ward_C/cover_front_preview.png", "Ward C Phantom"),
            ("The_Blackwood_Asylum_Files/Volume_4_The_Hydrotherapy_Chamber/cover_front_preview.png", "Hydrotherapy"),
            ("The_Blackwood_Asylum_Files/Volume_5_The_Director_s_Diary/cover_front_preview.png", "Director Diary")
        ]
    },
    {
        "id": "07_The_Grand_Orient_Express",
        "name": "The Grand Orient Express",
        "hero_book": "The_Grand_Orient_Express/Volume_1_Simplon_Tunnel_Stabbing",
        "theme": {
            "bg_color": (11, 29, 21, 255),
            "accent_rgb": (255, 183, 3), # Champagne Gold
            "spine_color": (12, 22, 16, 255),
            "hero_subtitle_accent": "CONTINENTAL LUXURY TRAIN HEISTS.",
            "hero_pitch_1": "First-class sleeper cabins, alpine blizzards, and poisoned banquets.",
            "hero_pitch_2": "35 elegant golden-age railway murder cases."
        },
        "lineup": [
            ("The_Grand_Orient_Express/Volume_1_Simplon_Tunnel_Stabbing/cover_front_preview.png", "Simplon Tunnel"),
            ("The_Grand_Orient_Express/Volume_2_The_Vienna_Sleeper_Car_Theft/cover_front_preview.png", "Vienna Sleeper"),
            ("The_Grand_Orient_Express/Volume_3_Balkan_Blizzard_Conspiracy/cover_front_preview.png", "Balkan Blizzard"),
            ("The_Grand_Orient_Express/Volume_4_Dining_Car_Poisoning/cover_front_preview.png", "Dining Car"),
            ("The_Grand_Orient_Express/Volume_5_The_Diplomatic_Pouch_Robbery/cover_front_preview.png", "Diplomat Pouch")
        ]
    },
    {
        "id": "08_The_Lupin_Heists",
        "name": "The Lupin Heists",
        "hero_book": "The_Lupin_Heists/Volume_01_The_Queens_Necklace_at_the_Louvre",
        "theme": {
            "bg_color": (6, 10, 23, 255),
            "accent_rgb": (239, 35, 60), # Laser Crimson & Gold
            "spine_color": (13, 22, 44, 255),
            "hero_subtitle_accent": "PARISIAN GENTLEMAN HEISTS.",
            "hero_pitch_1": "Louvre museum vaults, Versailles masquerades, and subterranean catacombs.",
            "hero_pitch_2": "35 high-stakes masterclass art theft and deduction dossiers."
        },
        "lineup": [
            ("The_Lupin_Heists/Volume_01_The_Queens_Necklace_at_the_Louvre/cover_front_preview.png", "Louvre Necklace"),
            ("The_Lupin_Heists/Volume_02_The_Catacombs_Phantom_Vault/cover_front_preview.png", "Catacombs Vault"),
            ("The_Lupin_Heists/Volume_03_The_Versailles_Masquerade_Gala/cover_front_preview.png", "Versailles Gala"),
            ("The_Lupin_Heists/Volume_04_The_Montmartre_Forgers_Studio/cover_front_preview.png", "Montmartre Forger"),
            ("The_Lupin_Heists/Volume_05_The_Musee_dOrsay_Clockwork_Enigma/cover_front_preview.png", "Musee dOrsay")
        ]
    },
    {
        "id": "09_The_Machine_Protocols",
        "name": "The Machine Protocols",
        "hero_book": "The_Machine_Protocols/Volume_01_The_Wall_Street_Irrelevant",
        "theme": {
            "bg_color": (8, 10, 14, 255),
            "accent_rgb": (0, 245, 212), # Electric Cyan HUD
            "spine_color": (14, 22, 34, 255),
            "hero_subtitle_accent": "MASS SURVEILLANCE A.I. THRILLERS.",
            "hero_pitch_1": "CCTV satellite tracking, intercepted wiretaps, and predictive crime prevention.",
            "hero_pitch_2": "35 tactical Person of Interest intelligence dossiers."
        },
        "lineup": [
            ("The_Machine_Protocols/Volume_01_The_Wall_Street_Irrelevant/cover_front_preview.png", "Wall St Irrelevant"),
            ("The_Machine_Protocols/Volume_02_The_Subway_Library_Safehouse/cover_front_preview.png", "Subway Safehouse"),
            ("The_Machine_Protocols/Volume_03_The_Corrupt_Precinct_Syndicate/cover_front_preview.png", "Precinct Syndicate"),
            ("The_Machine_Protocols/Volume_04_The_Darknet_Zero-Day_Broker/cover_front_preview.png", "Zero-Day Broker"),
            ("The_Machine_Protocols/Volume_05_The_Central_Park_Sniper_Threat/cover_front_preview.png", "Sniper Threat")
        ]
    }
]

def main():
    print("=" * 80)
    print("   GENERATING AMAZON KDP A+ CONTENT GRAPHICS SUITE (ALL 7 SERIES)")
    print("=" * 80)
    
    total_generated = 0
    
    for cfg in SERIES_CONFIGS:
        s_id = cfg['id']
        s_name = cfg['name']
        s_dir = os.path.join(OUTPUT_DIR, s_id)
        os.makedirs(s_dir, exist_ok=True)
        
        print(f"\n[*] Processing Series: {s_name} -> {s_dir}")
        
        cover_p = os.path.join(cfg['hero_book'], 'cover_front_preview.png')
        interior_p = os.path.join(cfg['hero_book'], 'interior_6x9.pdf')
        
        # 1. Module 1: Hero Showcase (970 x 600)
        m1_path = os.path.join(s_dir, "Module_1_Hero_Showcase_970x600.png")
        create_module_1_hero(s_name, "Volume 1", cover_p, cfg['theme'], m1_path)
        total_generated += 1
        
        # 2. Module 2: Investigation Flow (970 x 600)
        m2_path = os.path.join(s_dir, "Module_2_Investigation_Flow_970x600.png")
        create_module_2_investigation_flow(interior_p, cfg['theme'], m2_path)
        total_generated += 1
        
        # 3. Module 3: 4 Feature Spotlight Tiles (300 x 300)
        create_module_3_tiles(interior_p, cfg['theme'], s_dir)
        total_generated += 4
        
        # 4. Module 4: Quality & Specs Banner (970 x 300)
        m4_path = os.path.join(s_dir, "Module_4_Quality_Specs_Banner_970x300.png")
        create_module_4_specs_banner(s_name, cfg['theme'], m4_path)
        total_generated += 1
        
        # 5. Module 5: Collectible Series Lineup (970 x 600)
        m5_path = os.path.join(s_dir, "Module_5_Series_Lineup_970x600.png")
        create_module_5_series_lineup(s_name, cfg['lineup'], cfg['theme'], m5_path)
        total_generated += 1
        
        # 6. Copy Guide
        guide_path = os.path.join(s_dir, "A_Plus_Content_Copy_Guide.txt")
        create_aplus_copy_guide(s_name, cfg['theme'], guide_path)
        total_generated += 1
        
    print("\n" + "=" * 80)
    print(f"SUCCESS! Generated {total_generated} A+ Content Assets across all 7 Series!")
    print(f"Output directory: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 80)

if __name__ == "__main__":
    main()
