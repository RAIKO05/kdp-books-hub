"""
luxury_cover_engine.py (v2.0 - Story-Specific Luxury Masterpiece Edition)
Generates 7 completely distinct architectural cover frameworks for the 7 series,
with bespoke, vector-precise central artwork tailored to each individual book's story!
"""

import math
import textwrap
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas

BLEED = 0.125 * inch
TRIM_W = 6.0 * inch
TRIM_H = 9.0 * inch
SPINE_W = (176 * 0.002252) * inch # 0.396"
TOTAL_W = BLEED + TRIM_W + SPINE_W + TRIM_W + BLEED
TOTAL_H = BLEED + TRIM_H + BLEED

# ==============================================================================
# VECTOR SHAPE HELPERS
# ==============================================================================

def draw_poly(c, points, fill=1, stroke=1):
    if not points: return
    p = c.beginPath()
    p.moveTo(points[0][0], points[0][1])
    for pt in points[1:]:
        p.lineTo(pt[0], pt[1])
    p.close()
    c.drawPath(p, fill=fill, stroke=stroke)

def draw_star(c, cx, cy, r_out, r_in, points=5, fill_color=colors.HexColor("#D4AF37")):
    c.saveState()
    c.setFillColor(fill_color)
    c.setStrokeColor(fill_color)
    p = c.beginPath()
    angle = -math.pi / 2
    step = math.pi / points
    for i in range(2 * points):
        r = r_out if i % 2 == 0 else r_in
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        if i == 0: p.moveTo(x, y)
        else: p.lineTo(x, y)
        angle += step
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()

def draw_gear(c, cx, cy, r_out, r_in, teeth=12, fill_col=None, stroke_col=colors.HexColor("#D4AF37")):
    c.saveState()
    if fill_col: c.setFillColor(fill_col)
    c.setStrokeColor(stroke_col)
    c.setLineWidth(1.2)
    p = c.beginPath()
    step = 2 * math.pi / teeth
    for i in range(teeth):
        a1 = i * step
        a2 = a1 + step * 0.25
        a3 = a1 + step * 0.50
        a4 = a1 + step * 0.75
        x1, y1 = cx + r_in * math.cos(a1), cy + r_in * math.sin(a1)
        x2, y2 = cx + r_out * math.cos(a2), cy + r_out * math.sin(a2)
        x3, y3 = cx + r_out * math.cos(a3), cy + r_out * math.sin(a3)
        x4, y4 = cx + r_in * math.cos(a4), cy + r_in * math.sin(a4)
        if i == 0: p.moveTo(x1, y1)
        else: p.lineTo(x1, y1)
        p.lineTo(x2, y2)
        p.lineTo(x3, y3)
        p.lineTo(x4, y4)
    p.close()
    c.drawPath(p, fill=1 if fill_col else 0, stroke=1)
    c.circle(cx, cy, r_in * 0.45, fill=0, stroke=1)
    c.restoreState()

# ==============================================================================
# 1. THE DETECTIVE'S CASE FILES (Victorian Noir & British Golden Age)
# ==============================================================================

def draw_detective_cover(c, b):
    title = b.get("title", "").upper()
    vol_num = b.get("vol_number", 1)
    accent = colors.HexColor(b.get("accent_hex", "#D4AF37"))
    gold = colors.HexColor("#E5C158")
    bg = colors.HexColor("#080D15")

    front_left = BLEED + TRIM_W + SPINE_W
    cf = front_left + (TRIM_W / 2.0)
    top_y = TOTAL_H - BLEED
    bot_y = BLEED

    c.setFillColor(bg)
    c.rect(0, 0, TOTAL_W, TOTAL_H, fill=1, stroke=0)

    # Victorian Double-Filigree Border
    m = 0.42 * inch
    c.setStrokeColor(gold)
    c.setLineWidth(2.0)
    c.rect(front_left + m, bot_y + m, TRIM_W - 2*m, TRIM_H - 2*m)
    c.setLineWidth(0.75)
    c.setStrokeColor(accent)
    c.rect(front_left + m + 5, bot_y + m + 5, TRIM_W - 2*m - 10, TRIM_H - 2*m - 10)

    # Victorian Corner Ornaments
    for cx_c, cy_c in [(front_left + m + 14, bot_y + m + 14),
                      (front_left + TRIM_W - m - 14, bot_y + m + 14),
                      (front_left + m + 14, top_y - m - 14),
                      (front_left + TRIM_W - m - 14, top_y - m - 14)]:
        c.setStrokeColor(gold)
        c.circle(cx_c, cy_c, 8, fill=0, stroke=1)
        draw_star(c, cx_c, cy_c, 5, 2.5, points=4, fill_color=gold)

    # Header Ribbon
    c.setFillColor(colors.HexColor("#121926"))
    c.setStrokeColor(gold)
    c.roundRect(cf - 2.1*inch, top_y - 0.95*inch, 4.2*inch, 0.32*inch, 4, fill=1, stroke=1)
    c.setFillColor(gold)
    c.setFont("Times-Bold", 8.5)
    c.drawCentredString(cf, top_y - 0.77*inch, f"★ THE DETECTIVE'S CASE FILES • VOLUME {vol_num:02d} ★")
    c.setFont("Times-Italic", 7)
    c.setFillColor(colors.HexColor("#C0CAD8"))
    c.drawCentredString(cf, top_y - 1.15*inch, "Authentic Golden Age Whodunit Dossiers • Scotland Yard Special Branch")

    # Title
    c.setFillColor(accent)
    c.setFont("Times-Bold", 25 if len(title) > 24 else 28)
    title_words = title.split()
    if len(title) > 20 and len(title_words) >= 2:
        mid = len(title_words) // 2
        c.drawCentredString(cf, top_y - 1.85*inch, " ".join(title_words[:mid]))
        c.drawCentredString(cf, top_y - 2.25*inch, " ".join(title_words[mid:]))
        sep_y = top_y - 2.50*inch
    else:
        c.drawCentredString(cf, top_y - 1.95*inch, title)
        sep_y = top_y - 2.30*inch

    c.setStrokeColor(gold)
    c.setLineWidth(1.0)
    c.line(cf - 1.8*inch, sep_y, cf - 0.3*inch, sep_y)
    draw_star(c, cf, sep_y, 6, 3, points=4, fill_color=gold)
    c.line(cf + 0.3*inch, sep_y, cf + 1.8*inch, sep_y)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.HexColor("#E2E8F0"))
    c.drawCentredString(cf, sep_y - 0.28*inch, "35 MULTI-GAME INTERLOCKING CRIME SCENES")

    # STORY-SPECIFIC CENTRAL ARTWORK
    art_y = sep_y - 1.8*inch
    c.saveState()
    c.setStrokeColor(gold)
    c.setLineWidth(1.5)
    c.circle(cf, art_y, 64, fill=0, stroke=1)
    c.setStrokeColor(accent)
    c.setLineWidth(0.75)
    c.circle(cf, art_y, 56, fill=0, stroke=1)

    if "AIRSHIP" in title:
        # Airship Zeppelin
        c.setFillColor(colors.HexColor("#1A2333"))
        c.setStrokeColor(gold)
        c.ellipse(cf - 44, art_y - 16, cf + 44, art_y + 16, fill=1, stroke=1)
        c.rect(cf - 15, art_y - 23, 30, 8, fill=1, stroke=1)
        draw_poly(c, [(cf - 44, art_y), (cf - 54, art_y + 14), (cf - 38, art_y)], fill=1, stroke=1)
        draw_poly(c, [(cf - 44, art_y), (cf - 54, art_y - 14), (cf - 38, art_y)], fill=1, stroke=1)
        draw_gear(c, cf + 20, art_y, 14, 9, teeth=8, stroke_col=gold)
    elif "VENETIAN" in title or "MASQUERADE" in title:
        # Venetian Mask
        c.setFillColor(colors.HexColor("#1E1624"))
        c.setStrokeColor(gold)
        p = c.beginPath()
        p.moveTo(cf - 40, art_y + 5)
        p.curveTo(cf - 20, art_y + 35, cf + 20, art_y + 35, cf + 40, art_y + 5)
        p.curveTo(cf + 25, art_y - 20, cf + 5, art_y - 15, cf, art_y - 5)
        p.curveTo(cf - 5, art_y - 15, cf - 25, art_y - 20, cf - 40, art_y + 5)
        p.close()
        c.drawPath(p, fill=1, stroke=1)
        c.setFillColor(colors.HexColor("#080D15"))
        c.ellipse(cf - 26, art_y + 5, cf - 10, art_y + 17, fill=1, stroke=1)
        c.ellipse(cf + 10, art_y + 5, cf + 26, art_y + 17, fill=1, stroke=1)
    elif "WHITECHAPEL" in title or "FOG" in title:
        # London Gaslamp on Cobblestones
        c.setFillColor(colors.HexColor("#1A202C"))
        c.setStrokeColor(gold)
        c.rect(cf - 3, art_y - 45, 6, 60, fill=1, stroke=1)
        draw_poly(c, [(cf - 18, art_y + 15), (cf + 18, art_y + 15), (cf + 12, art_y + 35), (cf - 12, art_y + 35)], fill=1, stroke=1)
        draw_poly(c, [(cf - 18, art_y + 15), (cf + 18, art_y + 15), (cf + 10, art_y - 5), (cf - 10, art_y - 5)], fill=1, stroke=1)
        c.setFillColor(gold)
        c.circle(cf, art_y + 12, 7, fill=1, stroke=0)
    elif "BALMORAL" in title or "CASTLE" in title:
        # Scottish Castle Turret & Crossed Swords
        c.setFillColor(colors.HexColor("#15222E"))
        c.setStrokeColor(gold)
        c.rect(cf - 25, art_y - 30, 50, 60, fill=1, stroke=1)
        # Battlements
        for bx in [-25, -9, 9]:
            c.rect(cf + bx, art_y + 30, 16, 12, fill=1, stroke=1)
        # Crossed Swords
        c.setLineWidth(2.0)
        c.line(cf - 35, art_y - 20, cf + 35, art_y + 20)
        c.line(cf - 35, art_y + 20, cf + 35, art_y - 20)
    elif "CLIFF" in title or "CORNISH" in title:
        # Lighthouse on Cliff
        c.setFillColor(colors.HexColor("#132338"))
        c.setStrokeColor(gold)
        draw_poly(c, [(cf - 15, art_y - 35), (cf + 15, art_y - 35), (cf + 8, art_y + 25), (cf - 8, art_y + 25)], fill=1, stroke=1)
        c.circle(cf, art_y + 32, 10, fill=1, stroke=1)
        c.setFillColor(gold)
        c.circle(cf, art_y + 32, 5, fill=1, stroke=0)
        # Beams
        c.setStrokeColor(gold)
        c.line(cf + 10, art_y + 32, cf + 50, art_y + 45)
        c.line(cf - 10, art_y + 32, cf - 50, art_y + 45)
    elif "CHALICE" in title or "OXFORD" in title:
        # Poisoned Chalice
        c.setFillColor(colors.HexColor("#221D15"))
        c.setStrokeColor(gold)
        c.setLineWidth(1.8)
        c.ellipse(cf - 24, art_y - 5, cf + 24, art_y + 25, fill=1, stroke=1)
        c.line(cf, art_y - 5, cf, art_y - 35)
        c.rect(cf - 20, art_y - 42, 40, 7, fill=1, stroke=1)
        # Vapor ring
        c.circle(cf, art_y + 32, 8, fill=0, stroke=1)
    elif "HOUND" in title or "DARTMOOR" in title:
        # Howling Hound Silhouette
        c.setFillColor(colors.HexColor("#221812"))
        c.setStrokeColor(gold)
        p = c.beginPath()
        p.moveTo(cf - 28, art_y - 25)
        p.lineTo(cf - 12, art_y)
        p.lineTo(cf - 8, art_y + 28)
        p.lineTo(cf + 12, art_y + 12)
        p.lineTo(cf + 24, art_y - 25)
        p.close()
        c.drawPath(p, fill=1, stroke=1)
        draw_star(c, cf + 28, art_y + 28, 8, 4, points=5, fill_color=gold)
    else:
        # Victorian Magnifying Glass & Pipe
        c.setFillColor(colors.HexColor("#101826"))
        c.setStrokeColor(gold)
        c.setLineWidth(2.0)
        c.circle(cf, art_y + 6, 26, fill=1, stroke=1)
        c.setStrokeColor(colors.white)
        c.setLineWidth(1.0)
        c.arc(cf - 18, art_y - 12, cf + 18, art_y + 24, 45, 80)
        c.setStrokeColor(gold)
        c.setLineWidth(4.0)
        c.line(cf + 18, art_y - 12, cf + 38, art_y - 32)
        c.circle(cf + 40, art_y - 34, 4, fill=1, stroke=1)

    c.restoreState()

    # Feature Box
    box_w = 4.6 * inch
    box_h = 1.05 * inch
    by = bot_y + 1.25 * inch
    c.setFillColor(colors.HexColor("#0F1724"))
    c.setStrokeColor(gold)
    c.roundRect(cf - box_w/2.0, by, box_w, box_h, 6, fill=1, stroke=1)
    c.setFillColor(gold)
    c.setFont("Times-Bold", 9)
    c.drawCentredString(cf, by + box_h - 0.22*inch, "THE INTERLOCKING EVIDENCE KEY SYSTEM")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.white)
    c.drawCentredString(cf, by + box_h - 0.42*inch, "Forensic Sudoku Keys  •  Passkey-Shifted Ciphers")
    c.drawCentredString(cf, by + box_h - 0.60*inch, "4x4 Alibi Deduction Matrices  •  Scotland Yard Warrants")
    c.setFont("Times-Italic", 7)
    c.setFillColor(accent)
    c.drawCentredString(cf, by + 0.16*inch, "★ 100% Mathematically Verified Unique Solutions ★")

    draw_spine_and_back(c, b, "The Detective's Case Files", accent, gold, bg)

# ==============================================================================
# 2. PROJECT X (Hard Sci-Fi / Cyberpunk Aerospace HUD)
# ==============================================================================

def draw_project_x_cover(c, b):
    title = b.get("title", "").upper()
    vol_num = b.get("vol_number", 1)
    accent = colors.HexColor(b.get("accent_hex", "#00F5D4"))
    amber = colors.HexColor("#FCA311")
    bg = colors.HexColor("#04060A")

    front_left = BLEED + TRIM_W + SPINE_W
    cf = front_left + (TRIM_W / 2.0)
    top_y = TOTAL_H - BLEED
    bot_y = BLEED

    c.setFillColor(bg)
    c.rect(0, 0, TOTAL_W, TOTAL_H, fill=1, stroke=0)

    # Aerospace HUD Chamfered Frame
    m = 0.40 * inch
    c.setStrokeColor(accent)
    c.setLineWidth(1.8)
    draw_poly(c, [
        (front_left + m + 18, bot_y + m),
        (front_left + TRIM_W - m - 18, bot_y + m),
        (front_left + TRIM_W - m, bot_y + m + 18),
        (front_left + TRIM_W - m, top_y - m - 18),
        (front_left + TRIM_W - m - 18, top_y - m),
        (front_left + m + 18, top_y - m),
        (front_left + m, top_y - m - 18),
        (front_left + m, bot_y + m + 18)
    ], fill=0, stroke=1)

    # Hazard Angled Chevrons
    c.setFillColor(amber)
    for x_ch in [front_left + m + 30, front_left + TRIM_W - m - 45]:
        c.rect(x_ch, top_y - m - 4, 15, 3, fill=1, stroke=0)

    c.setFont("Courier-Bold", 6.5)
    c.setFillColor(accent)
    c.drawString(front_left + m + 6, top_y - m - 14, "SEC: MARS-ARES-7 // ELEV: -4.2KM")
    c.drawRightString(front_left + TRIM_W - m - 6, top_y - m - 14, "CLEARANCE: ULTRA-0")

    # Header Tech Bracket
    c.setFillColor(colors.HexColor("#0D1520"))
    c.setStrokeColor(amber)
    c.rect(cf - 2.0*inch, top_y - 0.95*inch, 4.0*inch, 0.30*inch, fill=1, stroke=1)
    c.setFillColor(amber)
    c.setFont("Courier-Bold", 8.5)
    c.drawCentredString(cf, top_y - 0.77*inch, f"[ PROJECT X // FORENSIC DOSSIER // VOL. {vol_num:02d} ]")

    # Title
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 25 if len(title) > 24 else 28)
    title_words = title.split()
    if len(title) > 20 and len(title_words) >= 2:
        mid = len(title_words) // 2
        c.drawCentredString(cf, top_y - 1.75*inch, " ".join(title_words[:mid]))
        c.setFillColor(accent)
        c.drawCentredString(cf, top_y - 2.15*inch, " ".join(title_words[mid:]))
        sep_y = top_y - 2.45*inch
    else:
        c.drawCentredString(cf, top_y - 1.85*inch, title)
        sep_y = top_y - 2.25*inch

    c.setStrokeColor(accent)
    c.line(cf - 1.8*inch, sep_y, cf + 1.8*inch, sep_y)
    c.setFillColor(amber)
    c.circle(cf, sep_y, 4, fill=1, stroke=1)
    c.setFont("Courier", 8)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawCentredString(cf, sep_y - 0.22*inch, "CONTAINMENT BREACH INVESTIGATION PROTOCOL")

    # STORY-SPECIFIC CENTRAL ARTWORK
    art_y = sep_y - 1.75*inch
    c.saveState()
    c.setStrokeColor(colors.HexColor("#1A2D40"))
    c.circle(cf, art_y, 60, fill=0, stroke=1)
    c.circle(cf, art_y, 40, fill=0, stroke=1)
    c.setStrokeColor(accent)
    c.line(cf - 65, art_y, cf + 65, art_y)
    c.line(cf, art_y - 65, cf, art_y + 65)

    if "ELEVATOR" in title:
        # Space Elevator Tether Cable
        c.setStrokeColor(accent)
        c.setLineWidth(3.0)
        c.line(cf, art_y - 55, cf, art_y + 55)
        c.setStrokeColor(amber)
        c.circle(cf, art_y, 25, fill=0, stroke=1)
        c.rect(cf - 15, art_y - 6, 30, 12, fill=1, stroke=1)
    elif "CRYO" in title or "TITAN" in title:
        # Cryo Hexagon Matrix
        for r_hex in [16, 32]:
            p = c.beginPath()
            for k in range(6):
                ang = k * math.pi / 3
                x = cf + r_hex * math.cos(ang)
                y = art_y + r_hex * math.sin(ang)
                if k == 0: p.moveTo(x, y)
                else: p.lineTo(x, y)
            p.close()
            c.drawPath(p, fill=0, stroke=1)
    elif "BIO" in title or "GENETIC" in title:
        # Double Helix DNA
        c.setStrokeColor(accent)
        c.setLineWidth(2.0)
        for hx in range(-30, 31, 10):
            hy = 15 * math.sin(hx * 0.15)
            c.line(cf + hx, art_y + hy, cf + hx, art_y - hy)
            c.circle(cf + hx, art_y + hy, 3, fill=1, stroke=0)
            c.circle(cf + hx, art_y - hy, 3, fill=1, stroke=0)
    elif "NEXUS" in title or "AI" in title:
        # Cybernetic Core Brain
        draw_gear(c, cf, art_y, 35, 25, teeth=10, stroke_col=accent)
        c.setFillColor(amber)
        c.circle(cf, art_y, 14, fill=1, stroke=0)
    elif "SINGULARITY" in title or "OMEGA" in title:
        # Black Hole Event Horizon
        c.setFillColor(colors.black)
        c.setStrokeColor(amber)
        c.setLineWidth(3.0)
        c.circle(cf, art_y, 24, fill=1, stroke=1)
        c.setStrokeColor(accent)
        c.ellipse(cf - 55, art_y - 12, cf + 55, art_y + 12, fill=0, stroke=1)
    else:
        # Mars Sphere & Planetary Orbit
        c.setFillColor(colors.HexColor("#3D1010"))
        c.setStrokeColor(amber)
        c.circle(cf, art_y, 28, fill=1, stroke=1)
        c.setStrokeColor(accent)
        c.setLineWidth(1.2)
        c.ellipse(cf - 48, art_y - 18, cf + 48, art_y + 18, fill=0, stroke=1)
        c.setFillColor(accent)
        c.circle(cf + 42, art_y + 10, 4, fill=1, stroke=0)

    c.restoreState()

    # Tech Panel Box
    by = bot_y + 1.20 * inch
    c.setFillColor(colors.HexColor("#060C14"))
    c.setStrokeColor(accent)
    c.rect(cf - 2.2*inch, by, 4.4*inch, 1.05*inch, fill=1, stroke=1)
    c.setFillColor(accent)
    c.setFont("Courier-Bold", 8.5)
    c.drawCentredString(cf, by + 0.85*inch, "FORENSIC TELEMETRY & LOGIC SUBSYSTEM:")
    c.setFont("Courier", 7.5)
    c.setFillColor(colors.white)
    c.drawCentredString(cf, by + 0.65*inch, "Quantum Sudoku Keys  •  Decrypted Terminal Logs")
    c.drawCentredString(cf, by + 0.45*inch, "Airlock Elimination Matrix  •  Court-Martial Warrants")
    c.setFont("Courier-Bold", 7)
    c.setFillColor(amber)
    c.drawCentredString(cf, by + 0.20*inch, "[ 100% MATHEMATICALLY VERIFIED UNIQUE SOLUTIONS ]")

    draw_spine_and_back(c, b, "Project X", accent, amber, bg)

# ==============================================================================
# 3. THE RAVENCREST CHRONICLES (Victorian Gothic / Occult Investigation)
# ==============================================================================

def draw_ravencrest_cover(c, b):
    title = b.get("title", "").upper()
    vol_num = b.get("vol_number", 1)
    accent = colors.HexColor(b.get("accent_hex", "#9D4EDD"))
    purple = colors.HexColor("#C77DFF")
    bg = colors.HexColor("#0A0610")

    front_left = BLEED + TRIM_W + SPINE_W
    cf = front_left + (TRIM_W / 2.0)
    top_y = TOTAL_H - BLEED
    bot_y = BLEED

    c.setFillColor(bg)
    c.rect(0, 0, TOTAL_W, TOTAL_H, fill=1, stroke=0)

    # Pointed Gothic Arch Frame
    m = 0.40 * inch
    c.setStrokeColor(accent)
    c.setLineWidth(2.0)
    p = c.beginPath()
    p.moveTo(front_left + m, bot_y + m)
    p.lineTo(front_left + m, top_y - m - 1.2*inch)
    p.curveTo(front_left + m + 0.4*inch, top_y - m - 0.3*inch, cf - 0.2*inch, top_y - m + 0.1*inch, cf, top_y - m + 0.2*inch)
    p.curveTo(cf + 0.2*inch, top_y - m + 0.1*inch, front_left + TRIM_W - m - 0.4*inch, top_y - m - 0.3*inch, front_left + TRIM_W - m, top_y - m - 1.2*inch)
    p.lineTo(front_left + TRIM_W - m, bot_y + m)
    p.close()
    c.drawPath(p, fill=0, stroke=1)

    c.setStrokeColor(purple)
    c.circle(cf, top_y - m - 0.1*inch, 12, fill=0, stroke=1)
    c.circle(cf, top_y - m - 0.1*inch, 6, fill=0, stroke=1)

    # Header
    c.setFont("Times-Bold", 8.5)
    c.setFillColor(purple)
    c.drawCentredString(cf, top_y - 0.85*inch, f"✦ THE RAVENCREST CHRONICLES • BOOK {vol_num:02d} ✦")
    c.setFont("Times-Italic", 7)
    c.setFillColor(colors.HexColor("#C4B5FD"))
    c.drawCentredString(cf, top_y - 1.05*inch, "Atmospheric Victorian Gothic Mystery & Occult Deductions")

    # Title
    c.setFillColor(colors.white)
    c.setFont("Times-Bold", 25 if len(title) > 24 else 28)
    title_words = title.split()
    if len(title) > 20 and len(title_words) >= 2:
        mid = len(title_words) // 2
        c.drawCentredString(cf, top_y - 1.80*inch, " ".join(title_words[:mid]))
        c.setFillColor(accent)
        c.drawCentredString(cf, top_y - 2.20*inch, " ".join(title_words[mid:]))
        sep_y = top_y - 2.45*inch
    else:
        c.drawCentredString(cf, top_y - 1.90*inch, title)
        sep_y = top_y - 2.25*inch

    c.setStrokeColor(accent)
    c.line(cf - 1.6*inch, sep_y, cf + 1.6*inch, sep_y)
    draw_star(c, cf, sep_y, 5, 2.5, points=8, fill_color=purple)

    # STORY-SPECIFIC CENTRAL ARTWORK
    art_y = sep_y - 1.70*inch
    c.saveState()
    c.setStrokeColor(purple)
    c.circle(cf, art_y, 56, fill=0, stroke=1)

    if "SEANCE" in title:
        # Seance Table & Spirit Planchette
        c.setFillColor(colors.HexColor("#1A0E2A"))
        c.setStrokeColor(purple)
        c.circle(cf, art_y, 35, fill=1, stroke=1)
        # Triangular planchette
        draw_poly(c, [(cf, art_y + 18), (cf - 16, art_y - 12), (cf + 16, art_y - 12)], fill=1, stroke=1)
        c.circle(cf, art_y - 2, 5, fill=0, stroke=1)
    elif "DOLL" in title or "CLOCKWORK" in title:
        # Clockwork Automaton Gear
        draw_gear(c, cf, art_y, 42, 28, teeth=12, stroke_col=purple)
        draw_star(c, cf, art_y, 14, 7, points=6, fill_color=accent)
    elif "GARGOYLE" in title or "CRYPT" in title:
        # Gargoyle Silhouette on Cathedral Parapet
        c.setFillColor(colors.HexColor("#1A0E2A"))
        c.setStrokeColor(purple)
        draw_poly(c, [(cf - 30, art_y - 30), (cf + 30, art_y - 30), (cf + 20, art_y - 10), (cf - 20, art_y - 10)], fill=1, stroke=1)
        # Gargoyle head & wings
        c.circle(cf, art_y + 10, 16, fill=1, stroke=1)
        draw_poly(c, [(cf - 16, art_y + 10), (cf - 36, art_y + 35), (cf - 10, art_y + 20)], fill=1, stroke=1)
        draw_poly(c, [(cf + 16, art_y + 10), (cf + 36, art_y + 35), (cf + 10, art_y + 20)], fill=1, stroke=1)
    else:
        # Spreading Raven Wings & Crescent Moon
        c.setFillColor(colors.HexColor("#1A0E2A"))
        c.setStrokeColor(purple)
        c.circle(cf - 14, art_y + 12, 16, fill=1, stroke=1)
        c.setFillColor(bg)
        c.circle(cf - 8, art_y + 14, 14, fill=1, stroke=0)
        # Raven Wings
        c.setStrokeColor(accent)
        c.setLineWidth(1.8)
        p = c.beginPath()
        p.moveTo(cf, art_y - 12)
        p.curveTo(cf - 20, art_y + 20, cf - 45, art_y + 10, cf - 48, art_y - 8)
        p.curveTo(cf - 30, art_y - 4, cf - 15, art_y - 10, cf, art_y - 12)
        p.curveTo(cf + 15, art_y - 10, cf + 30, art_y - 4, cf + 48, art_y - 8)
        p.curveTo(cf + 45, art_y + 10, cf + 20, art_y + 20, cf, art_y - 12)
        p.close()
        c.drawPath(p, fill=1, stroke=1)

    c.restoreState()

    # Feature Box
    by = bot_y + 1.25 * inch
    c.setFillColor(colors.HexColor("#120B1C"))
    c.setStrokeColor(accent)
    c.roundRect(cf - 2.2*inch, by, 4.4*inch, 1.05*inch, 6, fill=1, stroke=1)
    c.setFillColor(purple)
    c.setFont("Times-Bold", 9)
    c.drawCentredString(cf, by + 0.85*inch, "THE OCCULT EVIDENCE KEY INVESTIGATION:")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.white)
    c.drawCentredString(cf, by + 0.65*inch, "Ancestral Crypt Sudokus  •  Decrypted Seance Ciphers")
    c.drawCentredString(cf, by + 0.45*inch, "Alibi Deduction Matrices  •  Wills of Inheritance")
    c.setFont("Times-Italic", 7)
    c.setFillColor(accent)
    c.drawCentredString(cf, by + 0.18*inch, "★ 100% Mathematically Verified Unique Solutions ★")

    draw_spine_and_back(c, b, "The Ravencrest Chronicles", accent, purple, bg)

# ==============================================================================
# 4. THE BLETCHLEY PROTOCOLS (Cold War Espionage & MI6)
# ==============================================================================

def draw_bletchley_cover(c, b):
    title = b.get("title", "").upper()
    vol_num = b.get("vol_number", 1)
    accent = colors.HexColor(b.get("accent_hex", "#C1121F"))
    khaki = colors.HexColor("#D4A373")
    bg = colors.HexColor("#111311")

    front_left = BLEED + TRIM_W + SPINE_W
    cf = front_left + (TRIM_W / 2.0)
    top_y = TOTAL_H - BLEED
    bot_y = BLEED

    c.setFillColor(bg)
    c.rect(0, 0, TOTAL_W, TOTAL_H, fill=1, stroke=0)

    # Dossier Tab & Border
    m = 0.42 * inch
    c.setStrokeColor(khaki)
    c.setLineWidth(1.5)
    c.rect(front_left + m, bot_y + m, TRIM_W - 2*m, TRIM_H - 2*m)

    # File Folder Tab
    c.setFillColor(colors.HexColor("#222622"))
    draw_poly(c, [
        (front_left + m + 20, top_y - m),
        (front_left + m + 35, top_y - m + 12),
        (front_left + m + 140, top_y - m + 12),
        (front_left + m + 155, top_y - m)
    ], fill=1, stroke=1)
    c.setFont("Courier-Bold", 6.5)
    c.setFillColor(khaki)
    c.drawString(front_left + m + 40, top_y - m + 3, f"FILE: MI6-HUT8-{vol_num:02d}")

    # Angled Rubber Stamp
    c.saveState()
    c.translate(cf, top_y - 1.10*inch)
    c.rotate(-8)
    c.setFillColor(colors.HexColor("#330A0A"))
    c.setStrokeColor(accent)
    c.setLineWidth(2.0)
    c.rect(-1.8*inch, -0.20*inch, 3.6*inch, 0.40*inch, fill=1, stroke=1)
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(0, -0.06*inch, "★ TOP SECRET // EYES ONLY ★")
    c.restoreState()

    # Title
    c.setFillColor(colors.white)
    c.setFont("Courier-Bold", 24 if len(title) > 24 else 26)
    title_words = title.split()
    if len(title) > 20 and len(title_words) >= 2:
        mid = len(title_words) // 2
        c.drawCentredString(cf, top_y - 1.95*inch, " ".join(title_words[:mid]))
        c.setFillColor(khaki)
        c.drawCentredString(cf, top_y - 2.30*inch, " ".join(title_words[mid:]))
        sep_y = top_y - 2.55*inch
    else:
        c.drawCentredString(cf, top_y - 2.00*inch, title)
        sep_y = top_y - 2.35*inch

    c.setFillColor(colors.black)
    c.rect(cf - 1.7*inch, sep_y, 3.4*inch, 4, fill=1, stroke=0)
    c.setFont("Courier", 8)
    c.setFillColor(khaki)
    c.drawCentredString(cf, sep_y - 0.20*inch, "DEPT: SIGNAL INTELLIGENCE • CIPHER CORPS")

    # STORY-SPECIFIC CENTRAL ARTWORK
    art_y = sep_y - 1.70*inch
    c.saveState()
    draw_gear(c, cf, art_y, 54, 40, teeth=16, stroke_col=khaki)
    draw_gear(c, cf, art_y, 36, 24, teeth=12, stroke_col=accent)
    c.circle(cf, art_y, 14, fill=0, stroke=1)

    c.setFillColor(colors.HexColor("#2B2820"))
    c.setStrokeColor(khaki)
    c.rect(cf - 2.2*inch, art_y - 10, 4.4*inch, 20, fill=1, stroke=1)
    c.setFont("Courier-Bold", 8)
    c.setFillColor(colors.HexColor("#E2E8F0"))
    c.drawCentredString(cf, art_y - 3, "••• W-Q-X-P-M-R ••• INTERCEPT VERIFIED •••")
    c.restoreState()

    # Feature Box
    by = bot_y + 1.25 * inch
    c.setFillColor(colors.HexColor("#1A1814"))
    c.setStrokeColor(khaki)
    c.rect(cf - 2.2*inch, by, 4.4*inch, 1.05*inch, fill=1, stroke=1)
    c.setFillColor(accent)
    c.setFont("Courier-Bold", 8.5)
    c.drawCentredString(cf, by + 0.85*inch, "MI6 DEDUCTIVE COUNTER-INTELLIGENCE:")
    c.setFont("Courier", 7.5)
    c.setFillColor(colors.white)
    c.drawCentredString(cf, by + 0.65*inch, "Enigma Sudoku Keys  •  Decrypted Diplomatic Telexes")
    c.drawCentredString(cf, by + 0.45*inch, "Double-Agent Grids  •  State Arrest Warrants")
    c.setFont("Courier-Bold", 7)
    c.setFillColor(khaki)
    c.drawCentredString(cf, by + 0.20*inch, "[ OFFICIAL ENIGMA CODE-BREAKING DOSSIER ]")

    draw_spine_and_back(c, b, "The Bletchley Protocols", accent, khaki, bg)

# ==============================================================================
# 5. CRYPT OF THE PHARAOHS (Egyptian Archaeology & Ancient Curses)
# ==============================================================================

def draw_pharaoh_cover(c, b):
    title = b.get("title", "").upper()
    vol_num = b.get("vol_number", 1)
    accent = colors.HexColor(b.get("accent_hex", "#EE964B"))
    lapis = colors.HexColor("#1E3A8A")
    gold = colors.HexColor("#FBBF24")
    bg = colors.HexColor("#0D0B08")

    front_left = BLEED + TRIM_W + SPINE_W
    cf = front_left + (TRIM_W / 2.0)
    top_y = TOTAL_H - BLEED
    bot_y = BLEED

    c.setFillColor(bg)
    c.rect(0, 0, TOTAL_W, TOTAL_H, fill=1, stroke=0)

    # Monumental Pylon Border
    m = 0.42 * inch
    c.setStrokeColor(gold)
    c.setLineWidth(2.2)
    c.rect(front_left + m, bot_y + m, TRIM_W - 2*m, TRIM_H - 2*m)

    # Winged Sun Disk Cornice
    c.setFillColor(lapis)
    c.setStrokeColor(gold)
    c.circle(cf, top_y - m - 4, 12, fill=1, stroke=1)
    c.setLineWidth(1.5)
    c.line(cf - 12, top_y - m - 4, cf - 1.2*inch, top_y - m - 4)
    c.line(cf + 12, top_y - m - 4, cf + 1.2*inch, top_y - m - 4)

    # Header Cartouche
    c.setFillColor(colors.HexColor("#1A140A"))
    c.roundRect(cf - 2.1*inch, top_y - 0.95*inch, 4.2*inch, 0.30*inch, 8, fill=1, stroke=1)
    c.setFillColor(gold)
    c.setFont("Times-Bold", 8.5)
    c.drawCentredString(cf, top_y - 0.77*inch, f"𓋹 CRYPT OF THE PHARAOHS • VOLUME {vol_num:02d} 𓋹")

    # Title
    c.setFillColor(colors.white)
    c.setFont("Times-Bold", 26 if len(title) > 24 else 28)
    title_words = title.split()
    if len(title) > 20 and len(title_words) >= 2:
        mid = len(title_words) // 2
        c.drawCentredString(cf, top_y - 1.80*inch, " ".join(title_words[:mid]))
        c.setFillColor(accent)
        c.drawCentredString(cf, top_y - 2.20*inch, " ".join(title_words[mid:]))
        sep_y = top_y - 2.45*inch
    else:
        c.drawCentredString(cf, top_y - 1.90*inch, title)
        sep_y = top_y - 2.25*inch

    c.setStrokeColor(gold)
    c.line(cf - 1.6*inch, sep_y, cf + 1.6*inch, sep_y)
    draw_star(c, cf, sep_y, 6, 3, points=4, fill_color=gold)

    # STORY-SPECIFIC CENTRAL ARTWORK
    art_y = sep_y - 1.70*inch
    c.saveState()
    # Golden Sun Disk
    c.setFillColor(gold)
    c.setStrokeColor(lapis)
    c.circle(cf, art_y + 36, 16, fill=1, stroke=1)

    # Scarab Body & Outstretched Wings
    c.setFillColor(lapis)
    c.setStrokeColor(gold)
    c.setLineWidth(1.5)
    c.ellipse(cf - 16, art_y - 16, cf + 16, art_y + 20, fill=1, stroke=1)
    p = c.beginPath()
    p.moveTo(cf - 16, art_y)
    p.curveTo(cf - 35, art_y + 30, cf - 60, art_y + 25, cf - 65, art_y - 10)
    p.curveTo(cf - 45, art_y - 5, cf - 25, art_y - 12, cf - 16, art_y - 16)
    p.close()
    c.drawPath(p, fill=1, stroke=1)

    p2 = c.beginPath()
    p2.moveTo(cf + 16, art_y)
    p2.curveTo(cf + 35, art_y + 30, cf + 60, art_y + 25, cf + 65, art_y - 10)
    p2.curveTo(cf + 45, art_y - 5, cf + 25, art_y - 12, cf + 16, art_y - 16)
    p2.close()
    c.drawPath(p2, fill=1, stroke=1)
    c.restoreState()

    # Feature Box
    by = bot_y + 1.25 * inch
    c.setFillColor(colors.HexColor("#1A140B"))
    c.setStrokeColor(gold)
    c.roundRect(cf - 2.2*inch, by, 4.4*inch, 1.05*inch, 6, fill=1, stroke=1)
    c.setFillColor(gold)
    c.setFont("Times-Bold", 9)
    c.drawCentredString(cf, by + 0.85*inch, "SACRED TOMB FORENSIC ARCHAEOLOGY:")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.white)
    c.drawCentredString(cf, by + 0.65*inch, "Scarab Sudoku Keys  •  Hieroglyphic Papyrus Ciphers")
    c.drawCentredString(cf, by + 0.45*inch, "Pharaoh's Alibi Matrix  •  Valley of Kings Warrants")
    c.setFont("Times-Italic", 7)
    c.setFillColor(accent)
    c.drawCentredString(cf, by + 0.18*inch, "★ 100% Mathematically Verified Unique Solutions ★")

    draw_spine_and_back(c, b, "Crypt of the Pharaohs", accent, gold, bg)

# ==============================================================================
# 6. THE BLACKWOOD ASYLUM FILES (Edwardian Psychological Thriller)
# ==============================================================================

def draw_asylum_cover(c, b):
    title = b.get("title", "").upper()
    vol_num = b.get("vol_number", 1)
    accent = colors.HexColor(b.get("accent_hex", "#008080"))
    crimson = colors.HexColor("#D90429")
    bg = colors.HexColor("#080D0E")

    front_left = BLEED + TRIM_W + SPINE_W
    cf = front_left + (TRIM_W / 2.0)
    top_y = TOTAL_H - BLEED
    bot_y = BLEED

    c.setFillColor(bg)
    c.rect(0, 0, TOTAL_W, TOTAL_H, fill=1, stroke=0)

    # Restraint Straps & Steel Bars Border
    m = 0.42 * inch
    c.setStrokeColor(accent)
    c.setLineWidth(2.0)
    c.rect(front_left + m, bot_y + m, TRIM_W - 2*m, TRIM_H - 2*m)
    c.setStrokeColor(colors.HexColor("#1A2D30"))
    c.setLineWidth(0.8)
    for bx in [front_left + m + 14, front_left + TRIM_W - m - 14]:
        c.line(bx, bot_y + m, bx, top_y - m)

    # Clinical Admission Header
    c.setFillColor(colors.HexColor("#0F1A1B"))
    c.setStrokeColor(accent)
    c.rect(cf - 2.1*inch, top_y - 0.95*inch, 4.2*inch, 0.30*inch, fill=1, stroke=1)
    c.setFillColor(accent)
    c.setFont("Courier-Bold", 8.5)
    c.drawCentredString(cf, top_y - 0.77*inch, f"[ BLACKWOOD SANITARIUM // WARD {vol_num:02d} RECORD ]")

    c.saveState()
    c.translate(cf + 1.2*inch, top_y - 1.25*inch)
    c.rotate(-12)
    c.setFillColor(crimson)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(0, 0, "[ CONFIDENTIAL // PATIENT ADMISSION ]")
    c.restoreState()

    # Title
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 25 if len(title) > 24 else 27)
    title_words = title.split()
    if len(title) > 20 and len(title_words) >= 2:
        mid = len(title_words) // 2
        c.drawCentredString(cf, top_y - 1.85*inch, " ".join(title_words[:mid]))
        c.setFillColor(accent)
        c.drawCentredString(cf, top_y - 2.25*inch, " ".join(title_words[mid:]))
        sep_y = top_y - 2.50*inch
    else:
        c.drawCentredString(cf, top_y - 1.95*inch, title)
        sep_y = top_y - 2.30*inch

    c.setStrokeColor(accent)
    c.line(cf - 1.6*inch, sep_y, cf + 1.6*inch, sep_y)
    c.setFont("Courier", 8)
    c.setFillColor(colors.HexColor("#8E9DA0"))
    c.drawCentredString(cf, sep_y - 0.20*inch, "LOCKED WARD ISOLATION INVESTIGATION")

    # STORY-SPECIFIC CENTRAL ARTWORK (Key Ring & Caduceus)
    art_y = sep_y - 1.70*inch
    c.saveState()
    c.setStrokeColor(accent)
    c.circle(cf, art_y, 56, fill=0, stroke=1)

    c.setFillColor(colors.HexColor("#1A2D30"))
    c.setStrokeColor(accent)
    c.circle(cf, art_y + 12, 18, fill=0, stroke=1)
    for k_ang in [-0.4, 0, 0.4]:
        c.saveState()
        c.translate(cf, art_y + 12)
        c.rotate(math.degrees(k_ang))
        c.setLineWidth(2.5)
        c.line(0, -18, 0, -48)
        c.rect(-6, -48, 6, 8, fill=1, stroke=1)
        c.restoreState()
    c.restoreState()

    # Feature Box
    by = bot_y + 1.25 * inch
    c.setFillColor(colors.HexColor("#0C1517"))
    c.setStrokeColor(accent)
    c.rect(cf - 2.2*inch, by, 4.4*inch, 1.05*inch, fill=1, stroke=1)
    c.setFillColor(accent)
    c.setFont("Courier-Bold", 8.5)
    c.drawCentredString(cf, by + 0.85*inch, "PSYCHIATRIC FORENSIC PROTOCOL:")
    c.setFont("Courier", 7.5)
    c.setFillColor(colors.white)
    c.drawCentredString(cf, by + 0.65*inch, "Isolation Sudoku Keys  •  Unreliable Inmate Ciphers")
    c.drawCentredString(cf, by + 0.45*inch, "Locked-Ward Alibi Grids  •  Superintendent Warrants")
    c.setFont("Courier-Bold", 7)
    c.setFillColor(crimson)
    c.drawCentredString(cf, by + 0.20*inch, "[ 100% MATHEMATICALLY VERIFIED UNIQUE SOLUTIONS ]")

    draw_spine_and_back(c, b, "The Blackwood Asylum Files", accent, crimson, bg)

# ==============================================================================
# 7. THE GRAND ORIENT EXPRESS (1920s Art Deco Luxury Railway)
# ==============================================================================

def draw_orient_express_cover(c, b):
    title = b.get("title", "").upper()
    vol_num = b.get("vol_number", 1)
    accent = colors.HexColor(b.get("accent_hex", "#D4AF37"))
    gold = colors.HexColor("#F3C64F")
    bg = colors.HexColor("#060A14")

    front_left = BLEED + TRIM_W + SPINE_W
    cf = front_left + (TRIM_W / 2.0)
    top_y = TOTAL_H - BLEED
    bot_y = BLEED

    c.setFillColor(bg)
    c.rect(0, 0, TOTAL_W, TOTAL_H, fill=1, stroke=0)

    # 1920s Art Deco Stepped Chevron Border
    m = 0.42 * inch
    c.setStrokeColor(gold)
    c.setLineWidth(2.2)
    c.rect(front_left + m, bot_y + m, TRIM_W - 2*m, TRIM_H - 2*m)

    for cx_c, cy_c, sx, sy in [(front_left + m, bot_y + m, 1, 1),
                              (front_left + TRIM_W - m, bot_y + m, -1, 1),
                              (front_left + m, top_y - m, 1, -1),
                              (front_left + TRIM_W - m, top_y - m, -1, -1)]:
        c.setLineWidth(1.2)
        c.line(cx_c + sx*18, cy_c, cx_c, cy_c + sy*18)
        c.line(cx_c + sx*28, cy_c, cx_c, cy_c + sy*28)

    # Luxury Placard Header
    c.setFillColor(colors.HexColor("#101726"))
    c.setStrokeColor(gold)
    c.roundRect(cf - 2.2*inch, top_y - 0.95*inch, 4.4*inch, 0.32*inch, 4, fill=1, stroke=1)
    c.setFillColor(gold)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(cf, top_y - 0.77*inch, f"★ THE GRAND ORIENT EXPRESS • CARRIAGE {vol_num:02d} ★")
    c.setFont("Times-Italic", 7)
    c.setFillColor(colors.HexColor("#CBD5E1"))
    c.drawCentredString(cf, top_y - 1.15*inch, "Paris — Lausanne — Milano — Venezia — Wien — Istanbul")

    # Title
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 25 if len(title) > 24 else 27)
    title_words = title.split()
    if len(title) > 20 and len(title_words) >= 2:
        mid = len(title_words) // 2
        c.drawCentredString(cf, top_y - 1.80*inch, " ".join(title_words[:mid]))
        c.setFillColor(gold)
        c.drawCentredString(cf, top_y - 2.20*inch, " ".join(title_words[mid:]))
        sep_y = top_y - 2.45*inch
    else:
        c.drawCentredString(cf, top_y - 1.90*inch, title)
        sep_y = top_y - 2.25*inch

    c.setStrokeColor(gold)
    c.setLineWidth(1.5)
    c.line(cf - 1.8*inch, sep_y, cf + 1.8*inch, sep_y)
    draw_star(c, cf, sep_y, 6, 3, points=8, fill_color=gold)

    # STORY-SPECIFIC CENTRAL ARTWORK (Streamline Locomotive Front)
    art_y = sep_y - 1.70*inch
    c.saveState()
    c.setStrokeColor(colors.HexColor("#1A2436"))
    c.setLineWidth(0.8)
    for ray_idx in range(16):
        r_ang = ray_idx * math.pi / 8
        c.line(cf, art_y, cf + 62 * math.cos(r_ang), art_y + 62 * math.sin(r_ang))

    c.setStrokeColor(gold)
    c.setLineWidth(1.8)
    c.circle(cf, art_y, 56, fill=0, stroke=1)

    c.setFillColor(colors.HexColor("#0A111F"))
    c.setStrokeColor(gold)
    c.setLineWidth(1.4)
    c.circle(cf, art_y, 28, fill=1, stroke=1)
    draw_poly(c, [(cf - 24, art_y - 22), (cf + 24, art_y - 22), (cf, art_y - 40)], fill=1, stroke=1)
    c.setFillColor(gold)
    c.circle(cf, art_y + 6, 9, fill=1, stroke=1)
    c.restoreState()

    # Feature Box
    by = bot_y + 1.25 * inch
    c.setFillColor(colors.HexColor("#0D1424"))
    c.setStrokeColor(gold)
    c.roundRect(cf - 2.2*inch, by, 4.4*inch, 1.05*inch, 6, fill=1, stroke=1)
    c.setFillColor(gold)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(cf, by + 0.85*inch, "THE LUXURY CONTINENTAL TRANSIT SYSTEM:")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.white)
    c.drawCentredString(cf, by + 0.65*inch, "First-Class Sudoku Keys  •  Intercepted Wire Ciphers")
    c.drawCentredString(cf, by + 0.45*inch, "Salon Car Alibi Grids  •  State Arrest Warrants")
    c.setFont("Times-Italic", 7)
    c.setFillColor(gold)
    c.drawCentredString(cf, by + 0.18*inch, "★ 100% Mathematically Verified Unique Solutions ★")

    draw_spine_and_back(c, b, "The Grand Orient Express", accent, gold, bg)

# ==============================================================================
# SPINE & BACK COVER
# ==============================================================================

def draw_spine_and_back(c, b, series_name, accent, sec_color, bg):
    title = b.get("title", "").upper()
    vol_num = b.get("vol_number", 1)
    spine_left = BLEED + TRIM_W
    spine_center = spine_left + (SPINE_W / 2.0)
    back_left = BLEED
    center_back = back_left + (TRIM_W / 2.0)
    top_y = TOTAL_H - BLEED
    bot_y = BLEED
    m = 0.42 * inch

    # Spine
    c.saveState()
    c.translate(spine_center, TOTAL_H / 2.0)
    c.rotate(270)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.white)
    c.drawCentredString(0, -2.5, f"{series_name.upper()} (VOL. {vol_num})  •  {title}")
    c.restoreState()

    # Back Cover Border
    c.setStrokeColor(sec_color)
    c.setLineWidth(1.5)
    c.rect(back_left + m, bot_y + m, TRIM_W - 2*m, TRIM_H - 2*m)

    if "Lupin" in series_name:
        headline = "CRACK THE HIGH-STAKES HEIST EVIDENCE..."
        blurb = (
            f"Step into the dazzling, dangerous world of Parisian high society with {series_name}: Volume {vol_num}. "
            "Inspired by the legendary gentleman thief Arsène Lupin, every investigation challenges you with an "
            "authentic 4-stage interlocking forensic heist dossier:\n\n"
            "• Stage 1: Solve the Forensic Sudoku grid to reveal the four shaded Key Cells and bypass the infrared laser security grid.\n"
            "• Stage 2: Combine your security passkey digits to decrypt the phantom thief's calling card cipher left at the vault.\n"
            "• Stage 3: Cross-reference witness statements on the Gala Alibi Deduction Matrix (100% mathematically proven unique solution).\n"
            "• Stage 4: Unmask the master of disguise, certify the stolen artifact, and execute the French National Gendarmerie Warrant!\n\n"
            "Engineered with 100% mathematically proven unique solutions, zero ambiguous puzzles, "
            "and complete walk-through solutions. Gather your pencils, trust your intellect, and crack the Parisian heists today!"
        )
    elif "Machine" in series_name:
        headline = "YOU ARE BEING WATCHED. CAN YOU STOP THE THREAT?"
        blurb = (
            f"The government has a secret system: an artificial intelligence that monitors every camera, wiretap, and transaction in the city. "
            f"In {series_name}: Volume {vol_num}, you receive the latest classified intelligence drop:\n\n"
            "• Stage 1: Scan the metropolitan CCTV Satellite Grid with Forensic Sudoku to isolate the 4 GPS coordinate key cells.\n"
            "• Stage 2: Decrypt the intercepted payphone wiretap and audio telemetry using the Stage 1 numeric passkey.\n"
            "• Stage 3: Cross-reference suspects on the Surveillance Threat Matrix (100% mathematically proven unique solution) to identify the true perpetrator.\n"
            "• Stage 4: Authorize tactical intervention and execute the Asset Neutralization Warrant before the countdown hits zero!\n\n"
            "Engineered with 100% mathematically proven unique solutions, zero ambiguous puzzles, "
            "and complete walk-through solutions. Gather your pencils, trust your intellect, and intercept the crime in time!"
        )
    else:
        headline = "SOLVE THE INTERLOCKING EVIDENCE..."
        blurb = (
            f"Enter the gripping atmosphere of {series_name}: Volume {vol_num}. "
            "Unlike ordinary puzzle books that repeat disconnected grids, every single investigation in "
            "this volume is built upon the revolutionary Interlocking Evidence Key System:\n\n"
            "• Stage 1: Solve the Forensic Sudoku grid to extract the four shaded Key Cells.\n"
            "• Stage 2: Combine the extracted key digits into a security passkey to decrypt the dying witness dispatch.\n"
            "• Stage 3: Use the decrypted message as vital elimination proof to crack the 4x4 Alibi Deduction Matrix.\n"
            "• Stage 4: Synthesize your deductive evidence and execute the Official State Arrest Warrant.\n\n"
            "Engineered with 100% mathematically proven unique solutions, zero ambiguous puzzles, "
            "and complete walk-through solutions. Gather your pencils, trust your intellect, and solve the mystery!"
        )

    c.setFont("Helvetica-Bold", 12.5 if len(headline) > 35 else 13)
    c.setFillColor(sec_color)
    c.drawCentredString(center_back, top_y - 0.95*inch, headline)

    c.setFont("Helvetica", 7.8)
    c.setFillColor(colors.HexColor("#E2E8F0"))
    by = top_y - 1.35 * inch
    for p in blurb.split("\n\n"):
        for l in textwrap.wrap(p, width=44):
            c.drawString(back_left + m + 16, by, l)
            by -= 11.5
        by -= 6

    # Barcode Safe Box
    c.setFillColor(colors.white)
    c.setStrokeColor(sec_color)
    c.rect(center_back - 1.0 * inch, bot_y + 0.50 * inch, 2.0 * inch, 1.2 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#555555"))
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(center_back, bot_y + 1.05 * inch, "[ KDP Barcode Location ]")

# ==============================================================================
# 8. THE LUPIN HEISTS (Gentlemen of Paris & High-Stakes Museum Capers)
# ==============================================================================

def draw_lupin_cover(c, b):
    title = b.get("title", "").upper()
    vol_num = b.get("vol_number", 1)
    accent = colors.HexColor(b.get("accent_hex", "#EF233C")) # Laser Crimson / Ruby
    gold = colors.HexColor("#D4AF37") # Paris Belle Epoque Gold
    bg = colors.HexColor("#060A17") # Deep Midnight Indigo

    front_left = BLEED + TRIM_W + SPINE_W
    cf = front_left + (TRIM_W / 2.0)
    top_y = TOTAL_H - BLEED
    bot_y = BLEED

    c.setFillColor(bg)
    c.rect(0, 0, TOTAL_W, TOTAL_H, fill=1, stroke=0)

    # Belle Époque Ornate Frame
    m = 0.42 * inch
    c.setStrokeColor(gold)
    c.setLineWidth(1.8)
    c.rect(front_left + m, bot_y + m, TRIM_W - 2*m, TRIM_H - 2*m)

    c.setLineWidth(0.6)
    c.rect(front_left + m + 4, bot_y + m + 4, TRIM_W - 2*m - 8, TRIM_H - 2*m - 8)

    # Ornate Corner Flourishes
    for cx_c, cy_c, sx, sy in [(front_left + m, bot_y + m, 1, 1),
                              (front_left + TRIM_W - m, bot_y + m, -1, 1),
                              (front_left + m, top_y - m, 1, -1),
                              (front_left + TRIM_W - m, top_y - m, -1, -1)]:
        c.setLineWidth(1.2)
        c.line(cx_c + sx*18, cy_c, cx_c, cy_c + sy*18)
        c.line(cx_c + sx*28, cy_c, cx_c, cy_c + sy*28)
        draw_star(c, cx_c + sx*14, cy_c + sy*14, 4, 2, points=4, fill_color=gold)

    # Header Placard
    c.setFillColor(colors.HexColor("#0D162C"))
    c.setStrokeColor(gold)
    c.roundRect(cf - 2.3*inch, top_y - 0.95*inch, 4.6*inch, 0.32*inch, 4, fill=1, stroke=1)
    c.setFillColor(gold)
    c.setFont("Helvetica-Bold", 8.2)
    c.drawCentredString(cf, top_y - 0.77*inch, f"★ THE LUPIN HEISTS • GENTLEMEN OF PARIS (VOL. {vol_num:02d}) ★")
    c.setFont("Times-Italic", 7)
    c.setFillColor(colors.HexColor("#CBD5E1"))
    c.drawCentredString(cf, top_y - 1.15*inch, "High-Stakes Museum Thefts • Code of the Gentleman Thief")

    # Title
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24 if len(title) > 24 else 26)
    title_words = title.split()
    if len(title) > 20 and len(title_words) >= 2:
        mid = len(title_words) // 2
        c.drawCentredString(cf, top_y - 1.80*inch, " ".join(title_words[:mid]))
        c.setFillColor(gold)
        c.drawCentredString(cf, top_y - 2.20*inch, " ".join(title_words[mid:]))
        sep_y = top_y - 2.45*inch
    else:
        c.drawCentredString(cf, top_y - 1.90*inch, title)
        sep_y = top_y - 2.25*inch

    c.setStrokeColor(gold)
    c.setLineWidth(1.5)
    c.line(cf - 1.8*inch, sep_y, cf + 1.8*inch, sep_y)
    draw_star(c, cf, sep_y, 6, 3, points=8, fill_color=gold)

    # CENTRAL BESPOKE ARTWORK: Gentleman Thief Silhouette & Museum Laser Grid
    art_y = sep_y - 1.70*inch
    c.saveState()

    # Red Laser Security Beams Slicing Across
    c.setStrokeColor(accent)
    c.setLineWidth(1.2)
    c.line(cf - 70, art_y - 45, cf + 70, art_y + 35)
    c.line(cf - 65, art_y + 40, cf + 65, art_y - 40)
    c.setStrokeColor(colors.HexColor("#FFAAA6"))
    c.setLineWidth(0.5)
    c.line(cf - 70, art_y - 45, cf + 70, art_y + 35)
    c.line(cf - 65, art_y + 40, cf + 65, art_y - 40)

    # Outer Gilded Medal Ring
    c.setStrokeColor(gold)
    c.setLineWidth(1.8)
    c.circle(cf, art_y, 56, fill=0, stroke=1)
    c.setLineWidth(0.6)
    c.circle(cf, art_y, 50, fill=0, stroke=1)

    # Gentleman Thief Top Hat
    c.setFillColor(colors.HexColor("#080D1A"))
    c.setStrokeColor(gold)
    c.setLineWidth(1.5)
    # Brim
    draw_poly(c, [(cf - 36, art_y - 2), (cf + 36, art_y - 2), (cf + 32, art_y + 4), (cf - 32, art_y + 4)], fill=1, stroke=1)
    # Crown
    draw_poly(c, [(cf - 22, art_y + 4), (cf + 22, art_y + 4), (cf + 20, art_y + 36), (cf - 20, art_y + 36)], fill=1, stroke=1)
    # Hat ribbon in laser red
    c.setFillColor(accent)
    draw_poly(c, [(cf - 22, art_y + 6), (cf + 22, art_y + 6), (cf + 21, art_y + 12), (cf - 21, art_y + 12)], fill=1, stroke=0)

    # Monocle
    c.setStrokeColor(gold)
    c.setLineWidth(1.5)
    c.circle(cf + 12, art_y - 18, 9, fill=0, stroke=1)
    # Monocle chain
    p = c.beginPath()
    p.moveTo(cf + 21, art_y - 18)
    p.curveTo(cf + 28, art_y - 26, cf + 26, art_y - 34, cf + 16, art_y - 38)
    c.drawPath(p, fill=0, stroke=1)

    # Bow tie
    c.setFillColor(gold)
    draw_poly(c, [(cf - 14, art_y - 32), (cf - 2, art_y - 36), (cf - 14, art_y - 40)], fill=1, stroke=1)
    draw_poly(c, [(cf + 14, art_y - 32), (cf + 2, art_y - 36), (cf + 14, art_y - 40)], fill=1, stroke=1)
    c.circle(cf, art_y - 36, 3, fill=1, stroke=1)

    c.restoreState()

    # Feature Box
    by = bot_y + 1.25 * inch
    c.setFillColor(colors.HexColor("#0D162C"))
    c.setStrokeColor(gold)
    c.roundRect(cf - 2.2*inch, by, 4.4*inch, 1.05*inch, 6, fill=1, stroke=1)
    c.setFillColor(gold)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(cf, by + 0.85*inch, "THE 4-STAGE INTERLOCKING HEIST DOSSIER:")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.white)
    c.drawCentredString(cf, by + 0.65*inch, "Laser Grid Sudoku Keys  •  Gentleman Calling Card Ciphers")
    c.drawCentredString(cf, by + 0.45*inch, "Louvre & Gala Alibi Grids  •  Gendarmerie Arrest Warrants")
    c.setFont("Times-Italic", 7)
    c.setFillColor(accent)
    c.drawCentredString(cf, by + 0.18*inch, "★ 100% Mathematically Verified Unique Solutions ★")

    draw_spine_and_back(c, b, "The Lupin Heists", accent, gold, bg)


# ==============================================================================
# 9. THE MACHINE PROTOCOLS (Mass-Surveillance AI & Predictive Crime Prevention)
# ==============================================================================

def draw_machine_protocols_cover(c, b):
    title = b.get("title", "").upper()
    vol_num = b.get("vol_number", 1)
    accent = colors.HexColor(b.get("accent_hex", "#00F5D4")) # Electric Cyan HUD
    yellow_target = colors.HexColor("#FFBE0B") # Yellow POI Bounding Box
    threat_red = colors.HexColor("#FF0055") # Threat Alert Red
    bg = colors.HexColor("#080A0E") # Deep Carbon Slate

    front_left = BLEED + TRIM_W + SPINE_W
    cf = front_left + (TRIM_W / 2.0)
    top_y = TOTAL_H - BLEED
    bot_y = BLEED

    c.setFillColor(bg)
    c.rect(0, 0, TOTAL_W, TOTAL_H, fill=1, stroke=0)

    # Tactical HUD Frame
    m = 0.42 * inch
    c.setStrokeColor(accent)
    c.setLineWidth(1.4)
    c.rect(front_left + m, bot_y + m, TRIM_W - 2*m, TRIM_H - 2*m)

    # Surveillance Crosshairs on Corners
    for cx_c, cy_c, sx, sy in [(front_left + m, bot_y + m, 1, 1),
                              (front_left + TRIM_W - m, bot_y + m, -1, 1),
                              (front_left + m, top_y - m, 1, -1),
                              (front_left + TRIM_W - m, top_y - m, -1, -1)]:
        c.setLineWidth(1.5)
        c.setStrokeColor(accent)
        c.line(cx_c, cy_c, cx_c + sx*15, cy_c)
        c.line(cx_c, cy_c, cx_c, cy_c + sy*15)
        c.setFillColor(threat_red)
        c.circle(cx_c + sx*8, cy_c + sy*8, 2, fill=1, stroke=0)

    # Top Telemetry Bar
    c.setFont("Courier-Bold", 6.5)
    c.setFillColor(accent)
    c.drawCentredString(cf, top_y - m + 6, f"REC ● 1080P // CAM-08 HUD // LAT 40.7128° N // LON 74.0060° W")

    # Header Placard
    c.setFillColor(colors.HexColor("#0E1622"))
    c.setStrokeColor(yellow_target)
    c.roundRect(cf - 2.3*inch, top_y - 0.95*inch, 4.6*inch, 0.32*inch, 3, fill=1, stroke=1)
    c.setFillColor(yellow_target)
    c.setFont("Helvetica-Bold", 8.2)
    c.drawCentredString(cf, top_y - 0.77*inch, f"[ CLASSIFIED // THREAT LEVEL 5 ] THE MACHINE PROTOCOLS • ASSET #{vol_num:03d}")
    c.setFont("Courier-Bold", 7)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawCentredString(cf, top_y - 1.15*inch, "MASS SURVEILLANCE A.I. • IRRELEVANT NUMBERS • PREDICTIVE CRIME")

    # Title
    c.setFillColor(colors.white)
    c.setFont("Courier-Bold", 24 if len(title) > 24 else 26)
    title_words = title.split()
    if len(title) > 20 and len(title_words) >= 2:
        mid = len(title_words) // 2
        c.drawCentredString(cf, top_y - 1.80*inch, " ".join(title_words[:mid]))
        c.setFillColor(accent)
        c.drawCentredString(cf, top_y - 2.20*inch, " ".join(title_words[mid:]))
        sep_y = top_y - 2.45*inch
    else:
        c.drawCentredString(cf, top_y - 1.90*inch, title)
        sep_y = top_y - 2.25*inch

    c.setStrokeColor(accent)
    c.setLineWidth(1.2)
    c.line(cf - 1.8*inch, sep_y, cf + 1.8*inch, sep_y)
    c.setFillColor(yellow_target)
    c.rect(cf - 8, sep_y - 3, 16, 6, fill=1, stroke=0)

    # CENTRAL BESPOKE ARTWORK: Surveillance HUD Targeting Reticle & Facial Bounding Box
    art_y = sep_y - 1.70*inch
    c.saveState()

    # Concentric HUD Radar Circles
    c.setStrokeColor(colors.HexColor("#1A2B3C"))
    c.setLineWidth(0.8)
    c.circle(cf, art_y, 62, fill=0, stroke=1)
    c.setStrokeColor(accent)
    c.setLineWidth(1.2)
    c.circle(cf, art_y, 48, fill=0, stroke=1)

    # Compass / Reticle ticks
    for deg in range(0, 360, 45):
        rad = math.radians(deg)
        c.line(cf + 48*math.cos(rad), art_y + 48*math.sin(rad), cf + 54*math.cos(rad), art_y + 54*math.sin(rad))

    # Yellow Person of Interest Bounding Box
    c.setStrokeColor(yellow_target)
    c.setLineWidth(2.0)
    bw, bh = 54, 54
    # Corner brackets for bounding box
    c.line(cf - bw/2, art_y + bh/2, cf - bw/2 + 12, art_y + bh/2)
    c.line(cf - bw/2, art_y + bh/2, cf - bw/2, art_y + bh/2 - 12)
    c.line(cf + bw/2, art_y + bh/2, cf + bw/2 - 12, art_y + bh/2)
    c.line(cf + bw/2, art_y + bh/2, cf + bw/2, art_y + bh/2 - 12)
    c.line(cf - bw/2, art_y - bh/2, cf - bw/2 + 12, art_y - bh/2)
    c.line(cf - bw/2, art_y - bh/2, cf - bw/2, art_y - bh/2 + 12)
    c.line(cf + bw/2, art_y - bh/2, cf + bw/2 - 12, art_y - bh/2)
    c.line(cf + bw/2, art_y - bh/2, cf + bw/2, art_y - bh/2 + 12)

    # Target Tag
    c.setFillColor(yellow_target)
    c.rect(cf - bw/2, art_y + bh/2 + 2, 60, 10, fill=1, stroke=0)
    c.setFillColor(colors.black)
    c.setFont("Courier-Bold", 6.5)
    c.drawString(cf - bw/2 + 2, art_y + bh/2 + 4, f"POI #{vol_num:03d} LOCKED")

    # Audio Waveform Pulse across center
    c.setStrokeColor(accent)
    c.setLineWidth(1.5)
    wave_pts = [
        (cf - 40, art_y), (cf - 30, art_y + 8), (cf - 20, art_y - 12),
        (cf - 10, art_y + 18), (cf, art_y - 20), (cf + 10, art_y + 16),
        (cf + 20, art_y - 10), (cf + 30, art_y + 6), (cf + 40, art_y)
    ]
    p_wave = c.beginPath()
    p_wave.moveTo(wave_pts[0][0], wave_pts[0][1])
    for pt in wave_pts[1:]:
        p_wave.lineTo(pt[0], pt[1])
    c.drawPath(p_wave, fill=0, stroke=1)

    # Red Target Bullseye Center
    c.setFillColor(threat_red)
    c.circle(cf, art_y, 4, fill=1, stroke=0)

    c.restoreState()

    # Feature Box
    by = bot_y + 1.25 * inch
    c.setFillColor(colors.HexColor("#0D1722"))
    c.setStrokeColor(accent)
    c.roundRect(cf - 2.2*inch, by, 4.4*inch, 1.05*inch, 6, fill=1, stroke=1)
    c.setFillColor(yellow_target)
    c.setFont("Courier-Bold", 8.5)
    c.drawCentredString(cf, by + 0.85*inch, "THE 4-STAGE SURVEILLANCE PROTOCOL:")
    c.setFont("Courier", 7.5)
    c.setFillColor(colors.white)
    c.drawCentredString(cf, by + 0.65*inch, "CCTV Satellite Sudoku  •  Intercepted Wiretap Ciphers")
    c.drawCentredString(cf, by + 0.45*inch, "Threat-Matrix Alibi Grids  •  Asset Neutralization Warrants")
    c.setFont("Courier-Oblique", 7)
    c.setFillColor(accent)
    c.drawCentredString(cf, by + 0.18*inch, "★ 100% Mathematically Verified Unique Solutions ★")

    draw_spine_and_back(c, b, "The Machine Protocols", threat_red, accent, bg)


# ==============================================================================
# MASTER ROUTER
# ==============================================================================

def generate_luxury_cover(book_data, out_path):
    c = canvas.Canvas(out_path, pagesize=(TOTAL_W, TOTAL_H))
    s_name = book_data.get("series", "")

    if "Detective" in s_name:
        draw_detective_cover(c, book_data)
    elif "Project X" in s_name:
        draw_project_x_cover(c, book_data)
    elif "Ravencrest" in s_name:
        draw_ravencrest_cover(c, book_data)
    elif "Bletchley" in s_name:
        draw_bletchley_cover(c, book_data)
    elif "Pharaoh" in s_name:
        draw_pharaoh_cover(c, book_data)
    elif "Asylum" in s_name:
        draw_asylum_cover(c, book_data)
    elif "Express" in s_name or "Orient" in s_name:
        draw_orient_express_cover(c, book_data)
    elif "Lupin" in s_name:
        draw_lupin_cover(c, book_data)
    elif "Machine" in s_name:
        draw_machine_protocols_cover(c, book_data)
    else:
        draw_detective_cover(c, book_data)

    c.save()
