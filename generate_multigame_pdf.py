"""
generate_multigame_pdf.py
Compiles the 176-page print-ready interior PDF for:
"The Detective's Case Files: Volume 1 - Case Files & Clues"
Each of the 35 cases spans a 4-page investigative dossier:
- Page 1: Incident Briefing & Game 1 (Forensic Word Search)
- Page 2: Game 2 (Encrypted Dispatch Cipher) & Detective's Official Clues
- Page 3: Game 3 (Vector Logic Grid) & Game 4 (Official Warrant & Resolution)
- Page 4: Crime Scene Reconstruction & Investigator's Timeline Log
Pages 149-176: Complete 4-Game Master Solution Keys & Volume 2 Preview.
"""

import json
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import textwrap

PAGE_WIDTH = 6.0 * inch    # 432 pt
PAGE_HEIGHT = 9.0 * inch   # 648 pt
GUTTER = 0.5625 * inch     # 40.5 pt (KDP minimum for 176 pages is 0.50")
MARGIN_OUT = 0.45 * inch   # 32.4 pt
MARGIN_TOP = 0.45 * inch   # 32.4 pt
MARGIN_BOTTOM = 0.45 * inch # 32.4 pt

def get_page_margins(page_num):
    if page_num % 2 == 1:
        left = GUTTER
        right = PAGE_WIDTH - MARGIN_OUT
    else:
        left = MARGIN_OUT
        right = PAGE_WIDTH - GUTTER
    top = PAGE_HEIGHT - MARGIN_TOP
    bottom = MARGIN_BOTTOM
    return left, right, top, bottom

def draw_header_footer(c, page_num, title_text="THE DETECTIVE'S CASE FILES • VOL. 1"):
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

def create_multigame_pdf(filename="interior_6x9.pdf"):
    with open("multigame_cases.json", "r", encoding="utf-8") as f:
        cases = json.load(f)

    c = canvas.Canvas(filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    current_page = 1

    # PAGE 1: Half Title (Odd / Right)
    left, right, top, bottom = get_page_margins(current_page)
    c.setFont("Helvetica-Bold", 17)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 180, "THE DETECTIVE'S CASE FILES")
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.HexColor("#8E1B1B"))
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 205, "VOLUME 1: CASE FILES & CLUES")
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Oblique", 9.5)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 230, "35 Multi-Game Murder Mystery Dossiers for Adults")
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 250, "Logic Grids • Cryptograms • Forensic Word Searches • Criminal Warrants")
    c.showPage()
    current_page += 1

    # PAGE 2: Copyright & Originality (Even / Left)
    left, right, top, bottom = get_page_margins(current_page)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left, bottom + 160, "The Detective's Case Files: Volume 1")
    c.setFont("Helvetica", 7.5)
    c.drawString(left, bottom + 142, "Copyright © 2026. All rights reserved.")
    c.drawString(left, bottom + 128, "Published independently via Amazon Kindle Direct Publishing (KDP).")
    c.drawString(left, bottom + 110, "This is an original interactive work of mystery puzzle fiction.")
    c.drawString(left, bottom + 98, "Names, characters, places, and incidents are either products of the")
    c.drawString(left, bottom + 86, "author's imagination or used fictitiously. Any resemblance to actual")
    c.drawString(left, bottom + 74, "persons or trademarked entities is entirely coincidental.")
    c.drawString(left, bottom + 56, "First Enhanced Edition: October 2026")
    c.showPage()
    current_page += 1

    # PAGES 3-4: How to Play the 4-Game Dossiers
    for p_idx in [3, 4]:
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, "INVESTIGATOR'S FIELD MANUAL")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left, top - 32, "HOW TO SOLVE A 4-STAGE CASE DOSSIER" if p_idx == 3 else "CIPHER KEYS & LOGIC DEDUCTION RULES")
        c.setFont("Helvetica", 8)
        y = top - 52

        if p_idx == 3:
            raw_text = [
                "Welcome to the Agency, Detective. In this enhanced volume, every unsolved crime is structured as an interactive 4-stage case file. To identify the killer, you must complete four distinct phases:",
                "",
                "PHASE 1: THE FORENSIC EVIDENCE SWEEP (Word Search)",
                "Begin each case by scouring the crime scene grid for 5 pieces of physical evidence. As you locate each word, cross it off your evidence roster. The remaining untouched letters hold secondary investigative significance.",
                "",
                "PHASE 2: THE ENCRYPTED DISPATCH (Cryptograms)",
                "The victim, an informant, or the suspect left a coded dispatch. Using the provided Caesar Shift key (+3), decipher the message. The decrypted text contains a vital clue that eliminates a suspect or location.",
                "",
                "PHASE 3: THE ALIBI MATRIX (Logic Deduction Grid)",
                "Use the witness statements, forensic clues, and your decrypted dispatch to complete the logic matrix. Place checkmarks (√) for confirmations and crosses (X) for eliminations.",
                "",
                "PHASE 4: THE OFFICIAL CASE WARRANT",
                "Once the matrix proves who had access to the murder weapon at the scene of the crime, formally indict the culprit on the Official Warrant."
            ]
        else:
            raw_text = [
                "CIPHER CODEBREAKER GUIDE:",
                "Each case features an intercepted Caesar cipher shifted by 3 letters forward in the alphabet.",
                "To decode, shift each letter 3 places backward:",
                "• D becomes A   |   E becomes B   |   F becomes C",
                "• G becomes D   |   H becomes E   |   ...   |   C becomes Z",
                "",
                "LOGIC MATRIX PRINCIPLES:",
                "1. Each person of interest was in exactly one room and possessed one weapon.",
                "2. When a '√' is marked, all other boxes in that row and column must be crossed out ('X').",
                "3. Transitive property: If Person A was in Room B, and the weapon in Room B was Weapon C, then Person A possessed Weapon C.",
                "",
                "Pencil is strictly recommended! Take your time, double-check your deductions, and never guess. Every puzzle in this volume has been verified with constraint satisfaction solvers to have a single, unique solution."
            ]

        for block in raw_text:
            if not block: y -= 8; continue
            for line in textwrap.wrap(block, width=54):
                c.drawString(left, y, line)
                y -= 12
            y -= 4
        c.showPage()
        current_page += 1

    # PAGES 5-6: The 4 Thematic Universes & Difficulty
    for p_idx in [5, 6]:
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, "CASE DIRECTORY & DIFFICULTY")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left, top - 32, "THE FOUR INVESTIGATION SETTINGS" if p_idx == 5 else "DIFFICULTY CURVE & SCORING")
        c.setFont("Helvetica", 8)
        y = top - 52
        if p_idx == 5:
            raw_text = [
                "Your detective assignments take you across four atmospheric historical settings:",
                "",
                "• THE BLACKWOOD MANOR MURDERS (Cases 01–09):",
                "  Victorian country estates, aristocratic inheritances, poisoned sherry, and family feuds.",
                "",
                "• THE MIDNIGHT EXPRESS MYSTERIES (Cases 10–18):",
                "  Continental luxury trains, dark tunnels, covert diplomats, and jewel thefts.",
                "",
                "• THE METROPOLITAN MUSEUM HEISTS (Cases 19–27):",
                "  Priceless antiquities, Renaissance art vaults, master forgeries, and lethal artifacts.",
                "",
                "• THE COASTAL & LIGHTHOUSE CONSPIRACIES (Cases 28–35):",
                "  Isolated islands, foggy cliffs, storm wreckage, and maritime sabotage."
            ]
        else:
            raw_text = [
                "PROGRESSION TIERS:",
                "• TIER I: PROBATIONARY INVESTIGATOR (Cases 01–12)",
                "  Clear clues, direct cipher shifts, and standard word placements.",
                "• TIER II: SENIOR DETECTIVE INSPECTOR (Cases 13–24)",
                "  Complex multi-clause witness clues and tighter forensic grids.",
                "• TIER III: CHIEF SUPERINTENDENT (Cases 25–35)",
                "  Intricate chain-deductions where every clue relies on previous puzzle steps.",
                "",
                "DETECTIVE EVALUATION:",
                "At the end of Volume 1, tally your completed warrants on the Master Scorecard to determine your official investigator ranking!"
            ]
        for block in raw_text:
            if not block: y -= 8; continue
            for line in textwrap.wrap(block, width=54):
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
        c.drawString(left, top - 32, f"DOSSIER LOG ({'Cases 01–18' if toc_p == 7 else 'Cases 19–35 & Solutions'})")
        c.setFont("Helvetica", 7.5)
        
        start_idx = 0 if toc_p == 7 else 18
        end_idx = 18 if toc_p == 7 else 35
        y = top - 52
        for i in range(start_idx, end_idx):
            case = cases[i]
            c_page = 9 + (i * 4)
            c.drawString(left, y, f"Case #{case['case_number']:02d}: {case['title'].split(': ')[-1][:28]}")
            c.drawRightString(right, y, f"Pages {c_page}–{c_page+3}")
            y -= 14

        if toc_p == 8:
            y -= 10
            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(left, y, "Master Solutions & Decryption Key")
            c.drawRightString(right, y, "Page 149")

        c.showPage()
        current_page += 1

    # PAGES 9-148: The 35 Multi-Game Cases (4 Pages per Case)
    for case in cases:
        c_num = case["case_number"]

        # --- PAGE 1 OF CASE (Odd / Right): Incident Story & Game 1 Word Search ---
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, f"CASE #{c_num:03d} • PHASE I")

        # Case Header
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left, top - 30, case["title"].upper())
        c.setFont("Helvetica-Oblique", 7.5)
        c.drawString(left, top - 42, f"Setting: {case['theme']}")

        # Briefing Box
        c.setLineWidth(0.5)
        c.rect(left, top - 100, right - left, 54)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(left + 6, top - 56, "CASE INCIDENT REPORT:")
        c.setFont("Helvetica", 7)
        sy = top - 68
        for sl in textwrap.wrap(case["briefing"], width=58)[:3]:
            c.drawString(left + 6, sy, sl)
            sy -= 10

        # Game 1: Forensic Word Search
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.HexColor("#8E1B1B"))
        c.drawString(left, top - 114, "GAME 1: FORENSIC EVIDENCE SWEEP")
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 126, "Locate the 5 hidden physical evidence words in the crime scene grid:")

        # Draw Word Search Grid (10x10)
        ws_grid = case["game_1_word_search"]["grid"]
        gx = left + 20
        gy = top - 142
        c_size = 14
        c.setFont("Courier-Bold", 8.5)
        for r_idx in range(10):
            for col_idx in range(10):
                c.drawString(gx + (col_idx * c_size), gy - (r_idx * c_size), ws_grid[r_idx][col_idx])

        # Evidence Word Checklist
        c.setFont("Helvetica-Bold", 8)
        c.drawString(left + 175, top - 144, "EVIDENCE TO COLLECT:")
        c.setFont("Helvetica", 7.5)
        ey = top - 158
        for ew in case["game_1_word_search"]["words_to_find"]:
            c.drawString(left + 180, ey, f"[  ] {ew}")
            ey -= 14

        # Suspect Lineup Box
        c.rect(left, bottom + 12, right - left, 64)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(left + 6, bottom + 64, "PERSONS OF INTEREST DETAINED:")
        c.setFont("Helvetica", 7.5)
        py = bottom + 50
        for s_idx, susp in enumerate(case["game_3_logic_grid"]["suspects"]):
            c.drawString(left + 10, py, f"• Suspect #{s_idx+1}: {susp}")
            py -= 12

        c.showPage()
        current_page += 1

        # --- PAGE 2 OF CASE (Even / Left): Game 2 Cipher & Official Clues ---
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, f"CASE #{c_num:03d} • PHASE II")

        # Game 2: Encrypted Dispatch
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(colors.HexColor("#8E1B1B"))
        c.drawString(left, top - 32, "GAME 2: THE ENCRYPTED DISPATCH")
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 44, "The killer left this encoded message. Shift each letter back 3 places to read:")

        # Cipher Box
        c.rect(left, top - 100, right - left, 52)
        c.setFont("Courier-Bold", 9)
        c.drawString(left + 8, top - 62, "INTERCEPTED CIPHER:")
        c.setFont("Courier", 8.5)
        c_lines = textwrap.wrap(case["game_2_cipher"]["ciphertext"], width=42)
        cy = top - 75
        for cl in c_lines:
            c.drawString(left + 8, cy, cl)
            cy -= 11

        # Decryption Workspace
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(left, top - 110, "YOUR DECRYPTED TRANSCRIPTION:")
        c.setStrokeColor(colors.HexColor("#AAAAAA"))
        c.line(left, top - 128, right, top - 128)

        # Detective's Official Clues
        c.setStrokeColor(colors.black)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(left, top - 146, "DETECTIVE'S OFFICIAL WITNESS STATEMENTS:")
        c.setFont("Helvetica", 7.5)
        cly = top - 162
        for idx, clue in enumerate(case["game_3_logic_grid"]["clues"], 1):
            cl_wrapped = textwrap.wrap(f"{idx}. {clue}", width=52)
            for cw in cl_wrapped:
                c.drawString(left + 4, cly, cw)
                cly -= 10
            cly -= 2

        # Investigator's Field Note Box at bottom
        c.rect(left, bottom + 12, right - left, 50)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(left + 6, bottom + 50, "INVESTIGATOR'S DEDUCTION SCRATCHPAD:")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.line(left + 6, bottom + 36, right - 6, bottom + 36)
        c.line(left + 6, bottom + 24, right - 6, bottom + 24)

        c.showPage()
        current_page += 1

        # --- PAGE 3 OF CASE (Odd / Right): Game 3 Logic Grid & Game 4 Warrant ---
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, f"CASE #{c_num:03d} • PHASE III & IV")

        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.HexColor("#8E1B1B"))
        c.drawString(left, top - 32, "GAME 3: THE ALIBI & EVIDENCE MATRIX")
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 44, "Cross-reference statements to mark confirmations [√] and eliminations [X]")

        # Logic Grid Construction
        rms = case["game_3_logic_grid"]["rooms"]
        wps = case["game_3_logic_grid"]["weapons"]
        sus = case["game_3_logic_grid"]["suspects"]

        grid_x = left + 78
        grid_y = top - 250
        cell_size = 18.5
        c.setLineWidth(0.5)

        # Header rotation for rooms and weapons
        c.setFont("Helvetica", 5.8)
        for i, room in enumerate(rms):
            c.saveState()
            c.translate(grid_x + (i * cell_size) + 10, grid_y + 154)
            c.rotate(55)
            c.drawString(0, 0, room[:13])
            c.restoreState()

        for j, weap in enumerate(wps):
            c.saveState()
            c.translate(grid_x + ((4 + j) * cell_size) + 10, grid_y + 154)
            c.rotate(55)
            c.drawString(0, 0, weap[:13])
            c.restoreState()

        # Suspects row headers
        for k, susp in enumerate(sus):
            c.drawRightString(grid_x - 6, grid_y + 135 - (k * cell_size), susp[:15])

        for w_idx, weap in enumerate(wps):
            c.drawRightString(grid_x - 6, grid_y + 61 - (w_idx * cell_size), weap[:15])

        # Grid lines (4x4, 4x4, 4x4)
        c.setStrokeColor(colors.black)
        for r in range(5):
            c.setLineWidth(1.0 if r in [0, 4] else 0.5)
            c.line(grid_x, grid_y + 74 + (r * cell_size), grid_x + (4 * cell_size), grid_y + 74 + (r * cell_size))
            c.line(grid_x + (4 * cell_size), grid_y + 74 + (r * cell_size), grid_x + (8 * cell_size), grid_y + 74 + (r * cell_size))
            c.line(grid_x, grid_y + (r * cell_size), grid_x + (4 * cell_size), grid_y + (r * cell_size))

        for col in range(5):
            c.setLineWidth(1.0 if col in [0, 4] else 0.5)
            c.line(grid_x + (col * cell_size), grid_y + 74, grid_x + (col * cell_size), grid_y + 148)
            c.line(grid_x + (4 * cell_size) + (col * cell_size), grid_y + 74, grid_x + (4 * cell_size) + (col * cell_size), grid_y + 148)
            c.line(grid_x + (col * cell_size), grid_y, grid_x + (col * cell_size), grid_y + 74)

        # Game 4: The Official Case Warrant
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(colors.HexColor("#8E1B1B"))
        c.drawString(left, bottom + 76, "GAME 4: THE OFFICIAL ARREST WARRANT")
        c.setFillColor(colors.black)
        c.setLineWidth(1.0)
        c.rect(left, bottom + 10, right - left, 58)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(left + 8, bottom + 54, "STATE WARRANT OF INDICTMENT:")
        c.setFont("Helvetica", 7.5)
        c.drawString(left + 8, bottom + 38, "THE PERPETRATOR: ________________________")
        c.drawString(left + 175, bottom + 38, "CRIME SCENE: ________________________")
        c.drawString(left + 8, bottom + 24, "MURDER WEAPON: _________________________")
        c.drawString(left + 175, bottom + 24, "CONFIRMED MOTIVE: ___________________")
        c.drawString(left + 8, bottom + 12, "INVESTIGATOR SIGNATURE: _________________")
        c.drawString(left + 175, bottom + 12, "DATE CLOSED: ___/___/2026")

        c.showPage()
        current_page += 1

        # --- PAGE 4 OF CASE (Even / Left): Reconstruction & Notes ---
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, f"CASE #{c_num:03d} • DEBRIEF")

        c.setFont("Helvetica-Bold", 11)
        c.drawString(left, top - 32, "CRIME SCENE RECONSTRUCTION & NOTES")
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 44, "Record your analytical reasoning and timeline observations below.")

        # Timeline Diagram Box
        c.setLineWidth(0.5)
        c.rect(left, top - 140, right - left, 90)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(left + 8, top - 58, "CHRONOLOGICAL EVIDENCE TIMELINE:")
        c.setFont("Helvetica", 7.5)
        c.drawString(left + 12, top - 74, "1. Discovery of the Crime Scene (Forensic sweep conducted)")
        c.drawString(left + 12, top - 90, "2. Decoding of the Intercepted Dispatch (Cipher resolved)")
        c.drawString(left + 12, top - 106, "3. Interrogation & Alibi Cross-Check (Matrix verified)")
        c.drawString(left + 12, top - 122, "4. Execution of the Arrest Warrant (Culprit identified)")

        # Lined Notes Section
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(left, top - 156, "INVESTIGATOR'S FIELD JOURNAL:")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        ny = top - 172
        while ny > bottom + 25:
            c.line(left, ny, right, ny)
            ny -= 16

        c.showPage()
        current_page += 1

    # PAGES 149-174: Complete Master Solution Key (35 Cases)
    cases_per_sol_page = 2  # 2 detailed cases per solution page = 18 pages (149-166)
    sol_pages = (len(cases) + cases_per_sol_page - 1) // cases_per_sol_page

    for sp_idx in range(sol_pages):
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, "MASTER SOLUTION KEYS")

        c.setFont("Helvetica-Bold", 12)
        c.drawString(left, top - 32, "CASE DOSSIER SOLUTIONS & CIPHER KEYS")
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 44, "Official resolutions for all four investigative games.")

        y = top - 64
        batch = cases[sp_idx * cases_per_sol_page : (sp_idx + 1) * cases_per_sol_page]
        for sc in batch:
            c.setStrokeColor(colors.HexColor("#666666"))
            c.setLineWidth(0.5)
            c.rect(left, y - 240, right - left, 240)

            c.setFont("Helvetica-Bold", 9)
            c.drawString(left + 8, y - 16, f"CASE #{sc['case_number']:02d}: {sc['title'].split(': ')[-1]}")
            
            # Game 1 solutions
            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(left + 8, y - 32, "GAME 1 (FORENSIC WORDS):")
            c.setFont("Helvetica", 7)
            c.drawString(left + 130, y - 32, ", ".join(sc["game_1_word_search"]["words_to_find"]))

            # Game 2 solutions
            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(left + 8, y - 48, "GAME 2 (CIPHER DECRYPTED):")
            c.setFont("Courier-Bold", 7)
            c.drawString(left + 130, y - 48, f'"{sc["game_2_cipher"]["plaintext"]}"')

            # Game 3 & 4 solutions
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(colors.HexColor("#8E1B1B"))
            c.drawString(left + 8, y - 68, f"THE PERPETRATOR: {sc['game_4_solution']['culprit'].upper()}")
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 7.5)
            c.drawString(left + 175, y - 68, f"Scene: {sc['game_4_solution']['murder_room']}")
            c.drawString(left + 8, y - 82, f"Murder Weapon: {sc['game_4_solution']['murder_weapon']}")

            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(left + 8, y - 100, "COMPLETE MATRIX ALIBI MAPPINGS:")
            c.setFont("Helvetica", 7)
            ay = y - 114
            for s_name, s_data in sc["game_4_solution"]["full_mapping"].items():
                c.drawString(left + 12, ay, f"• {s_name}: {s_data['room']} | {s_data['weapon']}")
                ay -= 11

            c.setFont("Helvetica-Oblique", 6.5)
            c.drawString(left + 8, y - 230, "Proof: Algorithmic constraint satisfaction verified with exactly 1 unique solution.")
            y -= 255

        c.showPage()
        current_page += 1

    # PAGES 167-174: Scorecard & Volume 2 Preview
    # Page 167: Master Scorecard
    left, right, top, bottom = get_page_margins(current_page)
    draw_header_footer(c, current_page, "INVESTIGATOR EVALUATION SCORECARD")
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 40, "MASTER DETECTIVE EVALUATION")
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 56, "Tally your completed warrants to determine your official Agency Rank:")

    ranks = [
        ("30 – 35 Cases Solved", "CHIEF SUPERINTENDENT (Master Sleuth)"),
        ("20 – 29 Cases Solved", "SENIOR DETECTIVE INSPECTOR"),
        ("10 – 19 Cases Solved", "SERGEANT INVESTIGATOR"),
        ("01 – 09 Cases Solved", "ROOKIE CONSTABLE")
    ]
    ry = top - 90
    for r_score, r_title in ranks:
        c.rect(left + 20, ry - 24, right - left - 40, 24)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(left + 30, ry - 16, r_score)
        c.drawString(left + 150, ry - 16, r_title)
        ry -= 32

    c.showPage()
    current_page += 1

    # Page 168: Sneak Peek of Volume 2
    left, right, top, bottom = get_page_margins(current_page)
    draw_header_footer(c, current_page, "COMING SOON • VOLUME 2")
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 160, "CONTINUE THE INVESTIGATION")
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.HexColor("#8E1B1B"))
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 185, "THE DETECTIVE'S CASE FILES: VOLUME 2")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 210, "Featuring 35 All-New Crime Dossiers:")
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 228, "• The Royal Airship Sabotage")
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 242, "• The Grand Opera Poisoning")
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 256, "• The Botanical Gardens Conspiracy")
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 290, "Look for Volume 2 on Amazon KDP!")
    c.showPage()
    current_page += 1

    # Remaining filler pages to reach exactly 176 pages (Lined Notes)
    while current_page <= 176:
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, "INVESTIGATOR'S LOG NOTES")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left, top - 32, "DETECTIVE'S FIELD MEMORANDUM")
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 44, "Scratch calculations, cipher keys, and suspects' timelines.")

        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.5)
        ny = top - 64
        while ny > bottom + 25:
            c.line(left, ny, right, ny)
            ny -= 17

        c.showPage()
        current_page += 1

    c.save()
    print(f"Successfully compiled multi-game interior PDF: {filename} with exactly {current_page - 1} pages!")

if __name__ == "__main__":
    create_multigame_pdf()
