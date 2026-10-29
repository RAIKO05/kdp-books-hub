"""
generate_interior_pdf.py (v2.0)
Updated with strict margin safeguards:
1. Dynamic title wrapping & scaling to prevent overflow past margins.
2. Universal textwrap on all tutorial and briefing lines to honor the 0.55" gutter.
3. True facing spreads: Even page (Left) = Dossier; Odd page (Right) = Deduction Grid.
Total page count: exactly 176 pages.
"""

import json
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import textwrap

PAGE_WIDTH = 6.0 * inch    # 432 pt
PAGE_HEIGHT = 9.0 * inch   # 648 pt
GUTTER = 0.5625 * inch     # 40.5 pt (KDP minimum for 176 pages is 0.50")
MARGIN_OUT = 0.45 * inch   # 32.4 pt (KDP minimum is 0.25")
MARGIN_TOP = 0.45 * inch   # 32.4 pt
MARGIN_BOTTOM = 0.45 * inch # 32.4 pt

def get_page_margins(page_num):
    # Odd pages = Right-hand page: Gutter on Left, Margin on Right
    # Even pages = Left-hand page: Margin on Left, Gutter on Right
    if page_num % 2 == 1:
        left = GUTTER
        right = PAGE_WIDTH - MARGIN_OUT
    else:
        left = MARGIN_OUT
        right = PAGE_WIDTH - GUTTER
    top = PAGE_HEIGHT - MARGIN_TOP
    bottom = MARGIN_BOTTOM
    return left, right, top, bottom

def draw_header_footer(c, page_num, title_text="CASE FILES & CLUES"):
    left, right, top, bottom = get_page_margins(page_num)
    if page_num <= 2:
        return

    c.saveState()
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor("#555555"))

    c.setLineWidth(0.5)
    c.setStrokeColor(colors.HexColor("#AAAAAA"))
    c.line(left, top - 16, right, top - 16)
    
    if page_num % 2 == 1:
        c.drawRightString(right, top - 12, title_text)
    else:
        c.drawString(left, top - 12, title_text)

    # Footer
    c.setLineWidth(0.5)
    c.line(left, bottom + 16, right, bottom + 16)
    if page_num % 2 == 1:
        c.drawRightString(right, bottom + 6, str(page_num))
    else:
        c.drawString(left, bottom + 6, str(page_num))

    c.restoreState()

def create_interior_pdf(filename="interior_6x9.pdf"):
    with open("generated_cases.json", "r", encoding="utf-8") as f:
        cases = json.load(f)

    c = canvas.Canvas(filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    current_page = 1

    # PAGE 1: Half Title (Odd / Right)
    left, right, top, bottom = get_page_margins(current_page)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 200, "CASE FILES & CLUES")
    c.setFont("Helvetica-Oblique", 10.5)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 225, "70 Crime Scene Deduction Grids for Adults")
    c.showPage()
    current_page += 1

    # PAGE 2: Copyright & Originality (Even / Left)
    left, right, top, bottom = get_page_margins(current_page)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left, bottom + 160, "Case Files & Clues: 70 Crime Scene Deduction Grids for Adults")
    c.setFont("Helvetica", 7.5)
    c.drawString(left, bottom + 142, "Copyright © 2026. All rights reserved.")
    c.drawString(left, bottom + 128, "Published independently via Amazon Kindle Direct Publishing (KDP).")
    c.drawString(left, bottom + 110, "This is an original work of logic puzzle fiction. Names, characters,")
    c.drawString(left, bottom + 98, "places, and incidents are either products of the author's imagination")
    c.drawString(left, bottom + 86, "or used fictitiously. Any resemblance to actual persons or existing")
    c.drawString(left, bottom + 74, "trademarked publications is entirely coincidental.")
    c.drawString(left, bottom + 56, "First Edition: October 2026")
    c.showPage()
    current_page += 1

    # PAGES 3-4: How to Solve (Spread 3 Right, 4 Left)
    for tut_p in [3, 4]:
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, "HOW TO SOLVE A DEDUCTION GRID")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left, top - 32, "DETECTIVE'S BRIEFING: HOW TO SOLVE" if tut_p == 3 else "GRID MARKING & DEDUCTION TECHNIQUES")
        
        c.setFont("Helvetica", 8)
        y = top - 52
        if tut_p == 3:
            raw_text = [
                "Welcome, Inspector. Every case in this ledger presents an unsolved crime with four persons of interest, four locations, and four potential murder weapons.",
                "Your objective is to complete the case matrix using deductive reasoning alone.",
                "",
                "CORE PRINCIPLES OF DEDUCTION:",
                "1. ONE-TO-ONE MAPPING: Each suspect was in exactly one room and had access to exactly one piece of physical evidence or weapon.",
                "2. CROSSES (X) FOR ELIMINATION: Whenever a clue rules out a possibility, place an 'X' in the corresponding intersection on your grid.",
                "3. CHECKMARKS (√) FOR CONFIRMATIONS: When a clue establishes a definite link, place a '√' in that box.",
                "4. COMPLETE THE ROW & COLUMN: Once a '√' is confirmed, you must cross out all other boxes in that suspect's row and room's column, as no two suspects can share the same location.",
                "5. TRANSITIVE LINKS: If Suspect A is in Room 1, and the Candlestick was found in Room 1, then Suspect A unquestionably had the Candlestick."
            ]
        else:
            raw_text = [
                "ADVANCED SLEUTHING STRATEGIES:",
                "",
                "1. NEGATIVE LINKING: If Suspect B carried Weapon 2, and Clue 6 states that the weapon in the Conservatory was NOT Weapon 2, you immediately deduce that Suspect B was never in the Conservatory.",
                "",
                "2. MUTUAL EXCLUSION: Pay careful attention to 'Neither/Nor' statements. 'Neither Suspect A nor Suspect C visited Room 3' eliminates Room 3 for both individuals simultaneously.",
                "",
                "3. THE FINAL ACCUSATION: Each case concludes with an Official Accusation Box. The culprit is the sole individual linked by evidence to the designated crime scene and murder weapon.",
                "",
                "Pencil is recommended! Read each clue carefully, mark your findings methodically, and never guess. Every puzzle in this book is mathematically proven to have exactly one unique solution."
            ]

        for block in raw_text:
            if not block:
                y -= 8
                continue
            lines = textwrap.wrap(block, width=54)
            for line in lines:
                c.drawString(left, y, line)
                y -= 12
            y -= 4
        c.showPage()
        current_page += 1

    # PAGES 5-6: Categories & Difficulty Progression
    for guide_p in [5, 6]:
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, "THEMATIC CASE DIRECTORY")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left, top - 32, "THE FOUR INVESTIGATION SETTINGS" if guide_p == 5 else "DIFFICULTY TIERS & SCORING")
        c.setFont("Helvetica", 8)
        y = top - 52
        if guide_p == 5:
            raw_text = [
                "Your detective career spans four distinct atmospheric historical settings:",
                "",
                "• THE ENGLISH MANOR MURDERS (Cases 01–18):",
                "  Aristocratic intrigue, secluded country estates, poisoned tea, and family secrets.",
                "",
                "• THE MIDNIGHT EXPRESS MYSTERIES (Cases 19–36):",
                "  Continental passenger trains, sleeper cars, covert diplomats, and stolen jewels.",
                "",
                "• THE METROPOLITAN MUSEUM CRIMES (Cases 37–54):",
                "  Priceless antiquities, Renaissance galleries, art forgers, and dark conservation vaults.",
                "",
                "• THE COASTAL & LIGHTHOUSE CONSPIRACIES (Cases 55–70):",
                "  Foghorn towers, storm-battered islands, salvage captains, and sunken relics."
            ]
        else:
            raw_text = [
                "DIFFICULTY PROGRESSION:",
                "",
                "• TIER I: JUNIOR INVESTIGATOR (Cases 01–25)",
                "  Direct clues and clear negative eliminations. Ideal for warming up and mastering logic grid methodology.",
                "",
                "• TIER II: SENIOR INSPECTOR (Cases 26–50)",
                "  Introduces multi-step compound clues and subtle cross-category deductions.",
                "",
                "• TIER III: MASTER SLEUTH (Cases 51–70)",
                "  Requires deep chain-deductions. Every clue is tightly interconnected with zero margin for error.",
                "",
                "SOLVER SCORECARD:",
                "Keep score of your accuracy! Can you solve all 70 cases without consulting the Master Solution Key at the back of the book?"
            ]

        for block in raw_text:
            if not block:
                y -= 8
                continue
            lines = textwrap.wrap(block, width=54)
            for line in lines:
                c.drawString(left, y, line)
                y -= 12
            y -= 4
        c.showPage()
        current_page += 1

    # PAGES 7-8: Table of Contents
    for toc_p in [7, 8]:
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, "TABLE OF CONTENTS")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left, top - 32, f"CASE LOG ({'Cases 01–35' if toc_p == 7 else 'Cases 36–70 & Solutions'})")
        c.setFont("Helvetica", 7.5)
        
        start_idx = 0 if toc_p == 7 else 35
        end_idx = 35 if toc_p == 7 else 70
        y = top - 52
        for i in range(start_idx, end_idx):
            case = cases[i]
            c_page = 10 + (i * 2)
            c.drawString(left, y, f"Case #{case['case_number']:02d}: {case['title'].split(': ')[-1][:28]}")
            c.drawRightString(right, y, f"Page {c_page}")
            y -= 13.5

        if toc_p == 8:
            y -= 8
            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(left, y, "Master Solutions Key & Walkthroughs")
            c.drawRightString(right, y, "Page 150")

        c.showPage()
        current_page += 1

    # PAGE 9: Tier 1 Divider Page (Odd / Right) - Sets up Case 1 on Page 10 (Left)
    left, right, top, bottom = get_page_margins(current_page)
    draw_header_footer(c, current_page, "TIER I: JUNIOR INVESTIGATOR")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 180, "TIER I")
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 205, "JUNIOR INVESTIGATOR DOSSIERS")
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 230, "Cases 001 – 025")
    c.setLineWidth(0.5)
    c.line(left + 50, top - 250, right - 50, top - 250)
    c.setFont("Helvetica", 8)
    msg = textwrap.wrap("Sharpen your pencil and review your first 25 assignments. In this section, focus on establishing direct links and eliminating impossible intersections.", width=48)
    my = top - 275
    for ml in msg:
        c.drawCentredString(PAGE_WIDTH / 2.0, my, ml)
        my -= 14
    c.showPage()
    current_page += 1

    # PAGES 10-149: The 70 Cases (Even page = Left / Odd page = Right)
    for case in cases:
        c_num = case["case_number"]

        # --- EVEN PAGE (LEFT): Case Dossier & Clues ---
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, f"CASE #{c_num:03d} DOSSIER")

        # Dynamic title rendering to prevent margin overflow
        raw_title = case["title"].upper()
        c.setFont("Helvetica-Bold", 10.5)
        title_width = c.stringWidth(raw_title, "Helvetica-Bold", 10.5)
        max_title_w = right - left
        if title_width > max_title_w:
            t_lines = textwrap.wrap(raw_title, width=38)
            c.drawString(left, top - 30, t_lines[0])
            c.drawString(left, top - 42, t_lines[1])
            header_offset = 54
        else:
            c.drawString(left, top - 32, raw_title)
            header_offset = 44

        c.setFont("Helvetica-Oblique", 8)
        c.drawString(left, top - header_offset, f"Theme: {case['theme']}")

        # Incident briefing box
        box_top = top - header_offset - 10
        box_h = 50
        c.setLineWidth(0.5)
        c.setStrokeColor(colors.black)
        c.rect(left, box_top - box_h, right - left, box_h)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(left + 6, box_top - 12, "INCIDENT BRIEFING:")
        c.setFont("Helvetica", 7)
        story_lines = textwrap.wrap(case["briefing"], width=58)
        sy = box_top - 23
        for sl in story_lines[:3]:
            c.drawString(left + 6, sy, sl)
            sy -= 10

        # Roster summary
        y = box_top - box_h - 14
        c.setFont("Helvetica-Bold", 8)
        c.drawString(left, y, "PERSONS OF INTEREST:")
        c.drawString(left + 155, y, "LOCATIONS / EVIDENCE:")
        y -= 11
        c.setFont("Helvetica", 7.5)
        sus = case["categories"]["Suspects"]
        rms = case["categories"]["Rooms"]
        wps = case["categories"]["Weapons"]
        for i in range(4):
            c.drawString(left + 6, y, f"• {sus[i][:20]}")
            c.drawString(left + 160, y, f"• {rms[i][:20]}")
            c.drawString(left + 160, y - 44, f"• {wps[i][:20]}")
            y -= 11

        y -= 40
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(left, y, "DETECTIVE'S OFFICIAL CLUES:")
        y -= 13

        c.setFont("Helvetica", 7.5)
        for idx, clue in enumerate(case["clues"], 1):
            clue_wrapped = textwrap.wrap(f"{idx}. {clue}", width=52)
            for cw in clue_wrapped:
                c.drawString(left + 4, y, cw)
                y -= 10
            y -= 2

        c.showPage()
        current_page += 1

        # --- ODD PAGE (RIGHT): Deduction Grid & Accusation ---
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, f"CASE #{c_num:03d} DEDUCTION MATRIX")

        c.setFont("Helvetica-Bold", 11)
        c.drawString(left, top - 32, "DEDUCTION GRID")
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 44, "Mark confirmed links with [√] and eliminated links with [X]")

        # Grid positioning: strictly within printable width
        grid_x = left + 78
        grid_y = top - 265
        cell_size = 19
        c.setLineWidth(0.5)

        # Draw Rooms and Weapons column headers
        c.setFont("Helvetica", 6)
        for i, room in enumerate(rms):
            c.saveState()
            c.translate(grid_x + (i * cell_size) + 11, grid_y + 158)
            c.rotate(55)
            c.drawString(0, 0, room[:13])
            c.restoreState()

        for j, weap in enumerate(wps):
            c.saveState()
            c.translate(grid_x + ((4 + j) * cell_size) + 11, grid_y + 158)
            c.rotate(55)
            c.drawString(0, 0, weap[:13])
            c.restoreState()

        # Suspects row headers
        for k, susp in enumerate(sus):
            c.drawRightString(grid_x - 6, grid_y + 138 - (k * cell_size), susp[:15])

        # Weapons vertical row headers
        for w_idx, weap in enumerate(wps):
            c.drawRightString(grid_x - 6, grid_y + 62 - (w_idx * cell_size), weap[:15])

        # Grid lines: Suspects vs Rooms (4x4)
        c.setStrokeColor(colors.black)
        for r in range(5):
            thick = 1.0 if r in [0, 4] else 0.5
            c.setLineWidth(thick)
            c.line(grid_x, grid_y + 76 + (r * cell_size), grid_x + (4 * cell_size), grid_y + 76 + (r * cell_size))
        for col in range(5):
            thick = 1.0 if col in [0, 4] else 0.5
            c.setLineWidth(thick)
            c.line(grid_x + (col * cell_size), grid_y + 76, grid_x + (col * cell_size), grid_y + 152)

        # Grid lines: Suspects vs Weapons (4x4)
        for r in range(5):
            thick = 1.0 if r in [0, 4] else 0.5
            c.setLineWidth(thick)
            c.line(grid_x + (4 * cell_size), grid_y + 76 + (r * cell_size), grid_x + (8 * cell_size), grid_y + 76 + (r * cell_size))
        for col in range(5):
            thick = 1.0 if col in [0, 4] else 0.5
            c.setLineWidth(thick)
            c.line(grid_x + (4 * cell_size) + (col * cell_size), grid_y + 76, grid_x + (4 * cell_size) + (col * cell_size), grid_y + 152)

        # Grid lines: Weapons vs Rooms (4x4)
        for r in range(5):
            thick = 1.0 if r in [0, 4] else 0.5
            c.setLineWidth(thick)
            c.line(grid_x, grid_y + (r * cell_size), grid_x + (4 * cell_size), grid_y + (r * cell_size))
        for col in range(5):
            thick = 1.0 if col in [0, 4] else 0.5
            c.setLineWidth(thick)
            c.line(grid_x + (col * cell_size), grid_y, grid_x + (col * cell_size), grid_y + 76)

        # Notes area
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(left, bottom + 115, "DETECTIVE'S NOTES:")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.5)
        for nl in range(4):
            c.line(left, bottom + 100 - (nl * 14), right, bottom + 100 - (nl * 14))

        # Official Accusation Box
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.75)
        c.rect(left, bottom + 10, right - left, 44)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(left + 6, bottom + 40, "OFFICIAL CASE RESOLUTION (YOUR ACCUSATION):")
        c.setFont("Helvetica", 7)
        c.drawString(left + 6, bottom + 25, "THE CULPRIT: _______________________")
        c.drawString(left + 165, bottom + 25, "CRIME SCENE: _______________________")
        c.drawString(left + 6, bottom + 13, "LETHAL WEAPON: ____________________")
        c.drawString(left + 165, bottom + 13, "DATE SOLVED: ___/___/2026")

        c.showPage()
        current_page += 1

    # PAGES 150-174: Master Solution Key
    cases_per_sol_page = 3
    sol_pages = (len(cases) + cases_per_sol_page - 1) // cases_per_sol_page  # 24 pages (150-173)
    
    for sp_idx in range(sol_pages):
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, "MASTER SOLUTION KEY")

        c.setFont("Helvetica-Bold", 12)
        c.drawString(left, top - 32, "CASE SOLUTIONS & DEDUCTION PROOFS")
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 44, "Compare your deductions against the official case resolutions.")

        y = top - 64
        batch = cases[sp_idx * cases_per_sol_page : (sp_idx + 1) * cases_per_sol_page]
        for sc in batch:
            c.setStrokeColor(colors.HexColor("#777777"))
            c.setLineWidth(0.5)
            c.rect(left, y - 142, right - left, 142)

            c.setFont("Helvetica-Bold", 8.5)
            c.drawString(left + 6, y - 15, f"CASE #{sc['case_number']:02d}: {sc['title'].split(': ')[-1]}")
            
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(colors.HexColor("#9E1B1B"))
            c.drawString(left + 6, y - 30, f"CULPRIT: {sc['solution']['culprit'].upper()}")
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 7.5)
            c.drawString(left + 155, y - 30, f"Location: {sc['solution']['murder_room']}")
            c.drawString(left + 6, y - 44, f"Weapon: {sc['solution']['murder_weapon']}")

            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(left + 6, y - 58, "COMPLETE ASSIGNMENTS:")
            c.setFont("Helvetica", 7)
            ay = y - 71
            for s_name, s_data in sc["solution"]["full_mapping"].items():
                c.drawString(left + 10, ay, f"• {s_name}: {s_data['room']} | {s_data['weapon']}")
                ay -= 11

            c.setFont("Helvetica-Oblique", 6.5)
            c.drawString(left + 6, y - 132, "Deduction Proof: Unique mathematical solution verified by constraint satisfaction.")
            y -= 155

        c.showPage()
        current_page += 1

    # Remaining filler pages to reach exactly 176 pages (Detective notes)
    while current_page <= 176:
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, "DETECTIVE'S CASE NOTES")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left, top - 32, "INVESTIGATOR'S LOG & NOTES")
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 44, "Use this space for scratch deductions and case timings.")

        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.5)
        y = top - 64
        while y > bottom + 25:
            c.line(left, y, right, y)
            y -= 17

        c.showPage()
        current_page += 1

    c.save()
    print(f"Successfully generated {filename} with exactly {current_page - 1} pages!")

if __name__ == "__main__":
    create_interior_pdf()
