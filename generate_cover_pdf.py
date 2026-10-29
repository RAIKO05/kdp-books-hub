"""
generate_cover_pdf.py (v2.0 - Multi-Game Series Edition)
Compiles KDP full-wrap cover for:
Series: The Detective's Case Files (Volume 1)
Title: Case Files & Clues: Volume 1
Subtitle: 35 Multi-Game Murder Mystery Dossiers for Adults
Dimensions:
- Page count: 176 pages
- Spine: 176 * 0.002252 = 0.396 in (28.54 pt)
- Bleed: 0.125 in (9.0 pt)
- Total Width: 12.646 in (910.51 pt)
- Total Height: 9.25 in (666.0 pt)
"""

from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import textwrap

BLEED = 0.125 * inch
TRIM_W = 6.0 * inch
TRIM_H = 9.0 * inch
PAGE_COUNT = 176
SPINE_W = (PAGE_COUNT * 0.002252) * inch

TOTAL_W = BLEED + TRIM_W + SPINE_W + TRIM_W + BLEED  # 12.646 in
TOTAL_H = BLEED + TRIM_H + BLEED                    # 9.25 in

def create_cover_pdf(filename="cover_wrap_6x9.pdf"):
    c = canvas.Canvas(filename, pagesize=(TOTAL_W, TOTAL_H))

    back_left = BLEED
    back_right = BLEED + TRIM_W
    spine_left = back_right
    spine_right = spine_left + SPINE_W
    front_left = spine_right
    front_right = front_left + TRIM_W

    # Background Fill
    bg_color = colors.HexColor("#12171E")
    c.setFillColor(bg_color)
    c.rect(0, 0, TOTAL_W, TOTAL_H, fill=1, stroke=0)

    gold_accent = colors.HexColor("#C9A050")
    cream_text = colors.HexColor("#F4EEDB")
    crimson_badge = colors.HexColor("#8E1B1B")

    # -------------------------------------------------------------
    # FRONT COVER
    # -------------------------------------------------------------
    f_margin = 0.45 * inch
    c.setStrokeColor(gold_accent)
    c.setLineWidth(1.5)
    c.rect(front_left + f_margin, BLEED + f_margin, TRIM_W - (2 * f_margin), TRIM_H - (2 * f_margin))
    
    c.setLineWidth(0.5)
    c.rect(front_left + f_margin + 4, BLEED + f_margin + 4, TRIM_W - (2 * f_margin) - 8, TRIM_H - (2 * f_margin) - 8)

    center_front = front_left + (TRIM_W / 2.0)

    # Series Header Badge
    c.setFillColor(crimson_badge)
    c.setStrokeColor(gold_accent)
    c.setLineWidth(0.75)
    badge_w = 2.8 * inch
    badge_h = 0.28 * inch
    c.roundRect(center_front - (badge_w / 2.0), TOTAL_H - 1.25 * inch, badge_w, badge_h, 3, fill=1, stroke=1)
    
    c.setFillColor(cream_text)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(center_front, TOTAL_H - 1.15 * inch, "THE DETECTIVE'S CASE FILES • VOLUME 1")

    # Main Title
    c.setFillColor(gold_accent)
    c.setFont("Helvetica-Bold", 33)
    c.drawCentredString(center_front, TOTAL_H - 2.10 * inch, "CASE FILES")
    
    c.setFillColor(cream_text)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(center_front, TOTAL_H - 2.58 * inch, "& CLUES")

    # Divider Line
    c.setStrokeColor(gold_accent)
    c.setLineWidth(1.0)
    c.line(center_front - 1.6 * inch, TOTAL_H - 2.88 * inch, center_front + 1.6 * inch, TOTAL_H - 2.88 * inch)
    c.circle(center_front, TOTAL_H - 2.88 * inch, 3, fill=1, stroke=1)

    # Subtitle
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(cream_text)
    c.drawCentredString(center_front, TOTAL_H - 3.25 * inch, "35 MULTI-GAME MURDER MYSTERY")
    c.drawCentredString(center_front, TOTAL_H - 3.48 * inch, "DOSSIERS FOR ADULTS")

    # Center Graphic: Magnifying Glass & Shield
    c.saveState()
    c.setStrokeColor(gold_accent)
    c.setLineWidth(2.5)
    glass_cx = center_front
    glass_cy = TOTAL_H - 4.90 * inch
    c.circle(glass_cx, glass_cy, 36, fill=0, stroke=1)
    c.line(glass_cx + 25, glass_cy - 25, glass_cx + 52, glass_cy - 52)
    c.setLineWidth(0.5)
    c.setStrokeColor(cream_text)
    c.line(glass_cx - 20, glass_cy, glass_cx + 20, glass_cy)
    c.line(glass_cx, glass_cy - 20, glass_cx, glass_cy + 20)
    c.restoreState()

    # Multi-Game Feature Box
    c.setFillColor(colors.HexColor("#1A212B"))
    c.setStrokeColor(gold_accent)
    c.setLineWidth(0.75)
    hook_w = 4.6 * inch
    hook_h = 1.0 * inch
    c.rect(center_front - (hook_w / 2.0), TOTAL_H - 6.85 * inch, hook_w, hook_h, fill=1, stroke=1)

    c.setFillColor(cream_text)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(center_front, TOTAL_H - 6.15 * inch, "4 INTERLOCKING INVESTIGATIVE GAMES IN EVERY CASE:")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(gold_accent)
    c.drawCentredString(center_front, TOTAL_H - 6.35 * inch, "Forensic Word Hunts  •  Secret Ciphers & Cryptograms")
    c.drawCentredString(center_front, TOTAL_H - 6.52 * inch, "Alibi Logic Grids  •  Official Arrest Warrants")
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(cream_text)
    c.drawCentredString(center_front, TOTAL_H - 6.70 * inch, "★ 100% Mathematically Verified Unique Solutions ★")

    # Bottom Tag
    c.setFillColor(cream_text)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(center_front, BLEED + 0.85 * inch, "INTERACTIVE CRIME-SOLVER EXPERIENCE • COMPLETE SOLUTIONS")

    # -------------------------------------------------------------
    # SPINE
    # -------------------------------------------------------------
    c.setStrokeColor(colors.HexColor("#2C3440"))
    c.setLineWidth(0.5)
    c.line(spine_left, 0, spine_left, TOTAL_H)
    c.line(spine_right, 0, spine_right, TOTAL_H)

    c.saveState()
    c.translate(spine_left + (SPINE_W / 2.0), TOTAL_H / 2.0)
    c.rotate(270)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(cream_text)
    c.drawCentredString(0, -2.5, "THE DETECTIVE'S CASE FILES: VOL. 1  •  CASE FILES & CLUES")
    c.restoreState()

    # -------------------------------------------------------------
    # BACK COVER
    # -------------------------------------------------------------
    center_back = back_left + (TRIM_W / 2.0)
    c.setStrokeColor(gold_accent)
    c.setLineWidth(1.0)
    c.rect(back_left + f_margin, BLEED + f_margin, TRIM_W - (2 * f_margin), TRIM_H - (2 * f_margin))

    c.setFont("Helvetica-Bold", 13.5)
    c.setFillColor(gold_accent)
    c.drawCentredString(center_back, TOTAL_H - 1.25 * inch, "STEP INTO THE SHOES OF THE LEAD DETECTIVE")

    c.setFont("Helvetica", 8)
    c.setFillColor(cream_text)
    blurb = (
        "Welcome to The Detective's Case Files Series: Volume 1. "
        "Unlike ordinary puzzle books with repetitive grids, this enhanced edition "
        "immerses you in 35 comprehensive, multi-stage murder mysteries. "
        "Every single case challenges you to act as crime scene investigator, "
        "codebreaker, interrogator, and prosecutor.\n\n"
        "Can you uncover the hidden forensic evidence, crack the killer's encrypted cipher, "
        "disprove the suspects' alibis, and sign the official warrant before they escape justice?"
    )
    y_blurb = TOTAL_H - 1.62 * inch
    for para in blurb.split("\n\n"):
        for line in textwrap.wrap(para, width=54):
            c.drawString(back_left + f_margin + 18, y_blurb, line)
            y_blurb -= 11.5
        y_blurb -= 5

    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(gold_accent)
    c.drawString(back_left + f_margin + 18, y_blurb - 4, "THE 4-STAGE INVESTIGATION ANATOMY:")
    y_bullet = y_blurb - 18

    bullets = [
        ("STAGE 1: FORENSIC SWEEP", "10x10 word search scanning the crime scene for physical evidence."),
        ("STAGE 2: THE ENCRYPTED DISPATCH", "Decrypt the intercepted cipher to unlock a critical case clue."),
        ("STAGE 3: THE ALIBI MATRIX", "Airtight logic grids cross-referencing alibis, rooms, and weapons."),
        ("STAGE 4: THE OFFICIAL WARRANT", "Synthesize all proof and formally convict the true perpetrator.")
    ]

    for title_b, desc_b in bullets:
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(gold_accent)
        c.drawString(back_left + f_margin + 20, y_bullet, f"✔  {title_b}:")
        c.setFont("Helvetica", 7)
        c.setFillColor(cream_text)
        desc_wrapped = textwrap.wrap(desc_b, width=48)
        c.drawString(back_left + f_margin + 34, y_bullet - 9.5, desc_wrapped[0])
        y_bullet -= 22

    # Barcode Space
    bc_w = 2.0 * inch
    bc_h = 1.2 * inch
    bc_x = back_right - f_margin - bc_w - 6
    bc_y = BLEED + f_margin + 8

    c.setStrokeColor(colors.HexColor("#444C58"))
    c.setFillColor(colors.HexColor("#0D1116"))
    c.rect(bc_x, bc_y, bc_w, bc_h, fill=1, stroke=1)
    c.setFont("Helvetica", 6.5)
    c.setFillColor(colors.HexColor("#77808E"))
    c.drawCentredString(bc_x + (bc_w / 2.0), bc_y + (bc_h / 2.0) - 2, "[ Amazon KDP Barcode Zone ]")

    c.setFont("Helvetica", 7)
    c.setFillColor(cream_text)
    c.drawString(back_left + f_margin + 18, bc_y + 24, "GAMES & ACTIVITIES / MYSTERY PUZZLES")
    c.drawString(back_left + f_margin + 18, bc_y + 12, "Printed Independently • US $12.99")

    c.save()
    print(f"Successfully compiled multi-game series wrap cover: {filename}")

if __name__ == "__main__":
    create_cover_pdf()
