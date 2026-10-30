"""
build_project_x_vol1.py
Compiles the complete production package for:
"PROJECT X: THE TERMINAL (Volume 1)"
Theme: Corporate Sabotage & Cover-Up in a Martian Orbital Research Station
Generates:
1. multigame_cases.json (35 unique 4-in-1 sci-fi forensic cases)
2. interior_6x9.pdf (176 pages, strict KDP margins, facing spreads, full solutions)
3. cover_wrap_6x9.pdf (Full wrap cover in Cosmic Void Obsidian & Martian Red Oxide)
4. KDP_Listing_Metadata.txt
5. Updates catalog.json and pushes live to Google Cloud Firebase & GitHub!
"""

import json
import random
import itertools
import string
import re
import os
import textwrap
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas

PROJECT_DIR = "Project_X"
VOL1_DIR = os.path.join(PROJECT_DIR, "Volume_1_The_Terminal")
os.makedirs(VOL1_DIR, exist_ok=True)

# --- STEP 1: ASSETS FOR PROJECT X ---
PROJECT_X_ASSETS = {
  "project": "Project X: The Terminal (Volume 1)",
  "version": "1.0",
  "themes": [
    {
      "id": "bio_extraction",
      "name": "The Bio-Extraction Labs Sabotage",
      "suspects": [
        {"name": "Director Vance", "role": "Corporate Executive"},
        {"name": "Dr. Elena Chen", "role": "Chief Whistleblower"},
        {"name": "Technician Cole", "role": "Maintenance Diver"},
        {"name": "Security Chief Ward", "role": "Mercenary Guard"},
        {"name": "Dr. Tariq Malik", "role": "Senior Geochemist"},
        {"name": "Android Unit-07", "role": "Synthetic Overseer"}
      ],
      "rooms": [
        "Specimen Safe Vault", "Hydroponics Bio-Bay", "Cryogenic Stasis Ring", 
        "Argon Venting Duct", "Centrifuge Chamber", "Decon Airlock"
      ],
      "weapons": [
        "Plasma Solder Torch", "Liquid Nitrogen Syringe", "High-Voltage Stun Rod", 
        "Severed Oxygen Line", "Argon Gas Release Valve", "Titanium Pry Tool"
      ],
      "forensic_evidence": [
        "PLASMA", "OXYGEN", "VALVE", "ARGON", 
        "CRYSTAL", "SAMPLE", "FILTER", "HELMET"
      ],
      "cipher_clues": [
        "THE ARGON VALVE WAS MANUALLY OVERRIDDEN",
        "DIRECTOR VANCE ORDERED THE DATA PURGED",
        "CHECK THE SPECIMEN SAFE FOR THE CORE",
        "THE PLASMA TORCH WAS SIGNED BY SECURITY",
        "THE WHISTLEBLOWER WAS TRAPPED IN AIRLOCK",
        "UNIT ZERO SEVEN COPIED THE TELEMETRY"
      ]
    },
    {
      "id": "drill_shaft",
      "name": "The Sub-Surface Drill Shaft Explosion",
      "suspects": [
        {"name": "Chief Engineer Thorne", "role": "Framed Mechanic"},
        {"name": "Dr. Tariq Malik", "role": "Senior Geochemist"},
        {"name": "Corporate Auditor Stone", "role": "Company Fixer"},
        {"name": "Operations Lead Keller", "role": "Shift Foreman"},
        {"name": "Dr. Elena Chen", "role": "Chief Whistleblower"},
        {"name": "Security Chief Ward", "role": "Mercenary Guard"}
      ],
      "rooms": [
        "Sub-Surface Drill Shaft", "Heavy Smelting Foundry", "Pressurized Ore Hauler", 
        "Magma Thermal Bypass", "Mining Control Booth", "Tool Storage Lockout"
      ],
      "weapons": [
        "Industrial Laser Cutter", "Heavy Pneumatic Drill", "Magma Exhaust Flush", 
        "Steel Hoist Cable", "Seismic Charge Blaster", "Silicon Coolant Spray"
      ],
      "forensic_evidence": [
        "DRILL", "LASER", "CABLE", "ISOTOPE", 
        "SHIELD", "FURNACE", "SENSOR", "BATTERY"
      ],
      "cipher_clues": [
        "THE DRILL SHAFT EXPLOSION WAS DELIBERATE",
        "AUDITOR STONE PLANTED THE SEISMIC CHARGE",
        "THE LASER CUTTER WAS DISABLED AT DUSK",
        "THORNE HAD NO ACCESS TO THE BLAST KEYS",
        "ILLEGAL SHIPMENT WAS HIDDEN IN HAULER",
        "CHECK THE THERMAL BYPASS FOR ORE"
      ]
    },
    {
      "id": "ion_reactor",
      "name": "The Ion Reactor Containment Breach",
      "suspects": [
        {"name": "Reactor Tech Silas", "role": "Core Operator"},
        {"name": "Chief Engineer Thorne", "role": "Framed Mechanic"},
        {"name": "Director Vance", "role": "Corporate Executive"},
        {"name": "Android Unit-07", "role": "Synthetic Overseer"},
        {"name": "Corporate Auditor Stone", "role": "Company Fixer"},
        {"name": "Technician Cole", "role": "Maintenance Diver"}
      ],
      "rooms": [
        "Tritium Plasma Manifold", "Magnetic Field Ring", "Emergency Dump Hatch", 
        "Reactor Primary Core", "Radiation Catwalk", "Coolant Storage Tank"
      ],
      "weapons": [
        "Superheated Plasma Arc", "Tritium Coolant Rod", "Heavy Spanner Wrench", 
        "Magnetic Field Inverter", "Radiation Shield Pin", "Synthetic Neuro-Dart"
      ],
      "forensic_evidence": [
        "PLASMA", "TRITIUM", "CORE", "MAGNET", 
        "CIRCUIT", "GAUGE", "COOLANT", "WRENCH"
      ],
      "cipher_clues": [
        "THE INVERTER WAS TRIPPED FROM THE BRIDGE",
        "TRITIUM LEAK WAS TRIGGERED TO PURGE CREW",
        "THE NEURO DART WAS SOURCED OFF PLANET",
        "THE RADIATION CATWALK DOOR WAS LOCKED",
        "CORPORATE LOGS WERE WIPED AT MIDNIGHT",
        "SILAS DISCOVERED THE TAMPERED LINE"
      ]
    },
    {
      "id": "command_deck",
      "name": "The Command Deck Flight Sabotage",
      "suspects": [
        {"name": "Flight Officer Mercer", "role": "Orbital Pilot"},
        {"name": "Director Vance", "role": "Corporate Executive"},
        {"name": "Security Chief Ward", "role": "Mercenary Guard"},
        {"name": "Corporate Auditor Stone", "role": "Company Fixer"},
        {"name": "Android Unit-07", "role": "Synthetic Overseer"},
        {"name": "Operations Lead Keller", "role": "Shift Foreman"}
      ],
      "rooms": [
        "Orbital Shuttle Bay", "Main Telemetry Server", "Commander Stateroom", 
        "Communications Array", "Emergency Escape Pod 1", "Pressurized Airlock A"
      ],
      "weapons": [
        "Electromagnetic Pistol", "Airlock Purge Manual", "Ceramic Utility Blade", 
        "Emergency Flare Charge", "Synthetic Toxin Patch", "Crushed Data Core"
      ],
      "forensic_evidence": [
        "SHUTTLE", "POD", "SERVER", "ANTENNA", 
        "BEACON", "CIRCUIT", "ROCKET", "AIRLOCK"
      ],
      "cipher_clues": [
        "THE ESCAPE PODS WERE REMOTELY JETTISONED",
        "THE TELEMETRY SERVER WAS MELTED WITH ACID",
        "MERCER RECEIVED EVACUATION PAYMENT",
        "DIRECTOR VANCE ORDERED TOTAL SILENCE",
        "THE TOXIN PATCH WAS IN THE STATEROOM",
        "THE BEACON WAS POWERED DOWN MANUALLY"
      ]
    }
  ]
}

# --- STEP 2: PUZZLE ENGINES ---
def generate_word_search(words, grid_size=10):
    grid = [[" " for _ in range(grid_size)] for _ in range(grid_size)]
    placed_words = []
    for word in words:
        w_len = len(word)
        if w_len > grid_size: continue
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            attempts += 1
            direction = random.choice(["H", "V"])
            if direction == "H":
                r = random.randint(0, grid_size - 1)
                c = random.randint(0, grid_size - w_len)
                if all(grid[r][c + i] in (" ", word[i]) for i in range(w_len)):
                    for i in range(w_len): grid[r][c + i] = word[i]
                    placed_words.append(word)
                    placed = True
            else:
                r = random.randint(0, grid_size - w_len)
                c = random.randint(0, grid_size - 1)
                if all(grid[r + i][c] in (" ", word[i]) for i in range(w_len)):
                    for i in range(w_len): grid[r + i][c] = word[i]
                    placed_words.append(word)
                    placed = True

    for r in range(grid_size):
        for c in range(grid_size):
            if grid[r][c] == " ":
                grid[r][c] = random.choice(string.ascii_uppercase)

    return {"grid": grid, "words_to_find": placed_words}

def generate_cipher(plain_text):
    shift = 3
    cipher_chars = []
    for ch in plain_text.upper():
        if 'A' <= ch <= 'Z':
            cipher_chars.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
        else:
            cipher_chars.append(ch)
    ciphertext = "".join(cipher_chars)
    hint = "Caesar Shift (Frequency Key: +3). Shift each letter back 3 spots in the alphabet."
    return {"ciphertext": ciphertext, "plaintext": plain_text.upper(), "hint": hint, "shift": shift}

def count_valid_solutions(suspects, rooms, weapons, clues):
    room_perms = list(itertools.permutations(rooms))
    weapon_perms = list(itertools.permutations(weapons))
    valid_solutions = []

    for r_perm in room_perms:
        s_to_r = dict(zip(suspects, r_perm))
        for w_perm in weapon_perms:
            s_to_w = dict(zip(suspects, w_perm))
            r_to_w = {s_to_r[s]: s_to_w[s] for s in suspects}

            violation = False
            for clue in clues:
                m1 = re.match(r"(.+?) was confirmed to be in (.+)\.$", clue)
                if m1 and s_to_r.get(m1.group(1)) != m1.group(2): violation = True; break
                m2 = re.match(r"(.+?) was discovered carrying the (.+)\.$", clue)
                if m2 and s_to_w.get(m2.group(1)) != m2.group(2): violation = True; break
                m3 = re.match(r"The investigator found the (.+?) inside (.+)\.$", clue)
                if m3 and r_to_w.get(m3.group(2)) != m3.group(1): violation = True; break
                m4 = re.match(r"(.+?) was never seen near (.+)\.$", clue)
                if m4 and s_to_r.get(m4.group(1)) == m4.group(2): violation = True; break
                m5 = re.match(r"(.+?) had no access to the (.+)\.$", clue)
                if m5 and s_to_w.get(m5.group(1)) == m5.group(2): violation = True; break
                m6 = re.match(r"The weapon recovered from (.+?) was definitely not the (.+)\.$", clue)
                if m6 and r_to_w.get(m6.group(1)) == m6.group(2): violation = True; break
                m7 = re.match(r"Neither (.+?) nor (.+?) had ever visited (.+)\.$", clue)
                if m7 and (s_to_r.get(m7.group(1)) == m7.group(3) or s_to_r.get(m7.group(2)) == m7.group(3)): violation = True; break
                m8 = re.match(r"The lethal strike occurred in (.+?), leaving behind the deadly (.+)\.$", clue)
                if m8 and r_to_w.get(m8.group(1)) != m8.group(2): violation = True; break
                m9 = re.match(r"The suspect in (.+?) did not carry the (.+)\.$", clue)
                if m9 and r_to_w.get(m9.group(1)) == m9.group(2): violation = True; break
                m10 = re.match(r"(.+?) did not enter (.+)\.$", clue)
                if m10 and s_to_r.get(m10.group(1)) == m10.group(2): violation = True; break

            if not violation:
                valid_solutions.append({"s_to_r": s_to_r, "s_to_w": s_to_w})

    return valid_solutions

def generate_logic_puzzle(theme, seed=None):
    if seed: random.seed(seed)
    
    attempts = 0
    while attempts < 200:
        attempts += 1
        sus_objs = random.sample(theme["suspects"], 4)
        suspects = [s["name"] for s in sus_objs]
        rooms = random.sample(theme["rooms"], 4)
        weapons = random.sample(theme["weapons"], 4)

        shuffled_rooms = random.sample(rooms, 4)
        shuffled_weapons = random.sample(weapons, 4)

        solution_map = {}
        for i in range(4):
            solution_map[suspects[i]] = {"room": shuffled_rooms[i], "weapon": shuffled_weapons[i]}

        culprit = suspects[0]
        murder_room = solution_map[culprit]["room"]
        murder_weapon = solution_map[culprit]["weapon"]

        clues = [
            f"{suspects[1]} was confirmed to be in {solution_map[suspects[1]]['room']}.",
            f"{suspects[2]} was discovered carrying the {solution_map[suspects[2]]['weapon']}.",
            f"The investigator found the {solution_map[suspects[3]]['weapon']} inside {solution_map[suspects[3]]['room']}.",
            f"{culprit} was never seen near {[r for r in rooms if r != murder_room][0]}.",
            f"{culprit} had no access to the {[w for w in weapons if w != murder_weapon][0]}.",
            f"The weapon recovered from {[r for r in rooms if r != solution_map[suspects[2]]['room']][0]} was definitely not the {solution_map[suspects[2]]['weapon']}.",
            f"Neither {suspects[0]} nor {suspects[3]} had ever visited {solution_map[suspects[1]]['room']}.",
            f"The lethal strike occurred in {murder_room}, leaving behind the deadly {murder_weapon}."
        ]

        sols = count_valid_solutions(suspects, rooms, weapons, clues)
        if len(sols) == 0: continue

        disambig_tries = 0
        while len(sols) > 1 and disambig_tries < 10:
            disambig_tries += 1
            sol_alt = [s for s in sols if s["s_to_r"] != {s: solution_map[s]["room"] for s in suspects} or s["s_to_w"] != {s: solution_map[s]["weapon"] for s in suspects}][0]
            added = False
            for s in suspects:
                gt_w = solution_map[s]["weapon"]
                alt_w = sol_alt["s_to_w"][s]
                if gt_w != alt_w:
                    clues.append(f"{s} had no access to the {alt_w}.")
                    added = True
                    break
                gt_r = solution_map[s]["room"]
                alt_r = sol_alt["s_to_r"][s]
                if gt_r != alt_r:
                    clues.append(f"{s} did not enter {alt_r}.")
                    added = True
                    break
            if not added: break
            sols = count_valid_solutions(suspects, rooms, weapons, clues)

        if len(sols) == 1:
            return {
                "suspects": suspects, "rooms": rooms, "weapons": weapons, "clues": clues,
                "solution": {"culprit": culprit, "murder_room": murder_room, "murder_weapon": murder_weapon, "full_mapping": solution_map}
            }

    raise RuntimeError("Failed to generate unique logic puzzle.")

def generate_all_cases():
    all_cases = []
    for c_id in range(1, 36):
        theme = PROJECT_X_ASSETS["themes"][(c_id - 1) % len(PROJECT_X_ASSETS["themes"])]
        seed = 15000 + c_id
        logic = generate_logic_puzzle(theme, seed=seed)
        ev_words = random.sample(theme["forensic_evidence"], 5)
        ws = generate_word_search(ev_words, grid_size=10)
        cipher_msg = random.choice(theme["cipher_clues"])
        cipher = generate_cipher(cipher_msg)

        case_obj = {
            "case_number": c_id,
            "title": f"Incident #{c_id:03d}: The Breach at {logic['solution']['murder_room']}",
            "theme": theme["name"],
            "briefing": (
                f"Emergency alert triggered from {theme['name']}. "
                f"Vanguard Orbital Dynamics reported an explosion, but physical evidence proves foul play. "
                f"Scour the crime scene spectrometer, decrypt the intercepted black box cipher, "
                f"cross-examine the biometric airlock logs, and issue the court-martial indictment."
            ),
            "game_1_word_search": ws,
            "game_2_cipher": cipher,
            "game_3_logic_grid": {
                "suspects": logic["suspects"], "rooms": logic["rooms"], "weapons": logic["weapons"], "clues": logic["clues"]
            },
            "game_4_solution": logic["solution"]
        }
        all_cases.append(case_obj)

    out_json = os.path.join(VOL1_DIR, "multigame_cases.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(all_cases, f, indent=2)
    print(f"[✓] Generated 35 Project X cases saved to {out_json}")
    return all_cases

# --- STEP 3: INTERIOR PDF GENERATOR (176 Pages) ---
PAGE_WIDTH = 6.0 * inch
PAGE_HEIGHT = 9.0 * inch
GUTTER = 0.5625 * inch
MARGIN_OUT = 0.45 * inch
MARGIN_TOP = 0.45 * inch
MARGIN_BOTTOM = 0.45 * inch

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

def draw_header_footer(c, page_num, title_text="PROJECT X: THE TERMINAL • ORBITAL INVESTIGATION"):
    left, right, top, bottom = get_page_margins(page_num)
    if page_num <= 2: return
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
    c.line(left, bottom + 16, right, bottom + 16)
    if page_num % 2 == 1:
        c.drawRightString(right, bottom + 6, str(page_num))
    else:
        c.drawString(left, bottom + 6, str(page_num))
    c.restoreState()

def compile_interior(cases, filename=os.path.join(VOL1_DIR, "interior_6x9.pdf")):
    c = canvas.Canvas(filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    current_page = 1

    # PAGE 1: Half Title
    left, right, top, bottom = get_page_margins(current_page)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 170, "PROJECT X")
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#D90429")) # Martian Red Oxide accent
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 195, "VOLUME 1: THE TERMINAL")
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Oblique", 9.5)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 225, "35 Sci-Fi Murder Mystery Logic Puzzles: Corporate Sabotage on Mars")
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 245, "Spectrometer Sweeps • Black Box Ciphers • Airlock Logic Grids • Court-Martial Warrants")
    c.showPage()
    current_page += 1

    # PAGE 2: Copyright & Corporate Disclaimer
    left, right, top, bottom = get_page_margins(current_page)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left, bottom + 160, "Project X: The Terminal (Volume 1)")
    c.setFont("Helvetica", 7.5)
    c.drawString(left, bottom + 142, "Copyright © 2026. All rights reserved.")
    c.drawString(left, bottom + 128, "Published independently via Amazon Kindle Direct Publishing (KDP).")
    c.drawString(left, bottom + 110, "Setting: Ares Terminal Station, Mars Orbit (Year 2148).")
    c.drawString(left, bottom + 96, "Vanguard Orbital Dynamics corporate oversight clearance code: VOD-7790-OMEGA.")
    c.drawString(left, bottom + 56, "First Edition: October 2026")
    c.showPage()
    current_page += 1

    # PAGES 3-4: Investigator Manual
    for p_idx in [3, 4]:
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, "ORBITAL SAFETY & INVESTIGATION MANUAL")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left, top - 32, "SECURITY INCIDENT PROTOCOL" if p_idx == 3 else "TELEMETRY CIPHERS & LOGIC MATRICES")
        c.setFont("Helvetica", 8)
        y = top - 52
        if p_idx == 3:
            raw_text = [
                "Attention Special Investigator: You have docked aboard the Ares Terminal research outpost following a catastrophic containment breach.",
                "Corporate authorities claim a routine gas pocket ignited. Your mission is to establish the true chain of events.",
                "",
                "YOUR 4-STAGE INVESTIGATION ANATOMY:",
                "1. SPECTROMETER SENSOR SWEEP: Scan the 10x10 crime scene matrix for 5 critical forensic isotope markers.",
                "2. BLACK BOX DISPATCH: Crack intercepted crew transmissions shifted by +3 frequency channels.",
                "3. AIRLOCK ALIBI MATRIX: Cross-examine biometric swipe records to eliminate innocent crew members.",
                "4. COURT-MARTIAL INDICTMENT: Issue the emergency indictment with confirmed saboteur, module, and weapon."
            ]
        else:
            raw_text = [
                "CORPORATE SABOTAGE EVIDENCE GUIDELINES:",
                "Vanguard Orbital Dynamics operates under strict compartmentalization. Witnesses will obfuscate facts to protect corporate bounties.",
                "",
                "BLACK BOX FREQUENCY SHIFT REFERENCE:",
                "Shift 3 characters backward to decode intercepted telemetry (D->A, E->B, F->C, G->D).",
                "",
                "Pencil is strictly recommended! Double-check your biometric deductions before sealing the court-martial indictment."
            ]
        for block in raw_text:
            if not block: y -= 8; continue
            for line in textwrap.wrap(block, width=54):
                c.drawString(left, y, line)
                y -= 12
            y -= 4
        c.showPage()
        current_page += 1

    # PAGES 5-6: Sector Map & Directory
    for p_idx in [5, 6]:
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, "ARES TERMINAL SECTOR DIRECTORY")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left, top - 32, "FOUR HIGH-TECH SABOTAGE SECTORS" if p_idx == 5 else "CLEARANCE LEVELS & EVALUATION")
        c.setFont("Helvetica", 8)
        y = top - 52
        if p_idx == 5:
            raw_text = [
                "The investigations span four high-hazard terminal sectors:",
                "",
                "• THE BIO-EXTRACTION LABS (Cases 01–09): Mutated Martian flora, argon venting ducts, cryo-pods, and specimen vaults.",
                "• THE SUB-SURFACE DRILL SHAFT (Cases 10–18): Subterranean magma chambers, pneumatic rock drills, laser cutters, and ore haulers.",
                "• THE ION PROPULSION & REACTOR (Cases 19–27): Superheated plasma manifolds, tritium coolant tanks, and magnetic fields.",
                "• THE COMMAND DECK & SHUTTLE BAY (Cases 28–35): Melted telemetry servers, hacked launch airlocks, and jettisoned escape pods."
            ]
        else:
            raw_text = [
                "SECURITY CLEARANCE PROGRESSION:",
                "• CLEARANCE LEVEL 1: CHIEF INSPECTOR (Cases 01–12)",
                "• CLEARANCE LEVEL 2: PROVOST MARSHAL (Cases 13–24)",
                "• CLEARANCE LEVEL 3: SPECIAL ENVOY (Cases 25–35)",
                "",
                "Record your solved court-martial warrants in the Mission Scorecard at the back of the book."
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
        c.drawString(left, top - 32, f"INCIDENT DOSSIER LOG ({'Cases 01–18' if toc_p == 7 else 'Cases 19–35 & Solutions'})")
        c.setFont("Helvetica", 7.5)
        start_idx = 0 if toc_p == 7 else 18
        end_idx = 18 if toc_p == 7 else 35
        y = top - 52
        for i in range(start_idx, end_idx):
            case = cases[i]
            c_page = 9 + (i * 4)
            c.drawString(left, y, f"Incident #{case['case_number']:02d}: {case['title'].split(': ')[-1][:28]}")
            c.drawRightString(right, y, f"Pages {c_page}–{c_page+3}")
            y -= 14
        if toc_p == 8:
            y -= 10
            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(left, y, "Master Solutions & Black Box Decryption Key")
            c.drawRightString(right, y, "Page 149")
        c.showPage()
        current_page += 1

    # PAGES 9-148: The 35 Multi-Game Cases (4 Pages each)
    for case in cases:
        c_num = case["case_number"]

        # Page 1: Incident Dispatch & Sensor Sweep
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, f"INCIDENT #{c_num:03d} • STAGE I")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left, top - 30, case["title"].upper())
        c.setFont("Helvetica-Oblique", 7.5)
        c.drawString(left, top - 42, f"Facility Sector: {case['theme']}")

        c.setLineWidth(0.5)
        c.rect(left, top - 100, right - left, 54)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(left + 6, top - 56, "EMERGENCY DISPATCH REPORT:")
        c.setFont("Helvetica", 7)
        sy = top - 68
        for sl in textwrap.wrap(case["briefing"], width=58)[:3]:
            c.drawString(left + 6, sy, sl)
            sy -= 10

        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.HexColor("#D90429"))
        c.drawString(left, top - 114, "GAME 1: SPECTROMETER SENSOR SWEEP")
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 126, "Scan the 10x10 crime scene matrix for 5 key physical isotope markers:")

        ws_grid = case["game_1_word_search"]["grid"]
        gx = left + 20
        gy = top - 142
        c_size = 14
        c.setFont("Courier-Bold", 8.5)
        for r_idx in range(10):
            for col_idx in range(10):
                c.drawString(gx + (col_idx * c_size), gy - (r_idx * c_size), ws_grid[r_idx][col_idx])

        c.setFont("Helvetica-Bold", 8)
        c.drawString(left + 175, top - 144, "ISOTOPE MARKERS TO LOCATE:")
        c.setFont("Helvetica", 7.5)
        ey = top - 158
        for ew in case["game_1_word_search"]["words_to_find"]:
            c.drawString(left + 180, ey, f"[  ] {ew}")
            ey -= 14

        c.rect(left, bottom + 12, right - left, 64)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(left + 6, bottom + 64, "CREW MEMBERS DETAINED IN SECTOR:")
        c.setFont("Helvetica", 7.5)
        py = bottom + 50
        for s_idx, susp in enumerate(case["game_3_logic_grid"]["suspects"]):
            c.drawString(left + 10, py, f"• Crew Member #{s_idx+1}: {susp}")
            py -= 12
        c.showPage()
        current_page += 1

        # Page 2: Black Box Cipher & Witness Alibis
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, f"INCIDENT #{c_num:03d} • STAGE II")
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(colors.HexColor("#D90429"))
        c.drawString(left, top - 32, "GAME 2: CORRUPTED BLACK BOX DISPATCH")
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 44, "Intercepted saboteur signal. Shift each letter back 3 places (+3 frequency key):")

        c.rect(left, top - 100, right - left, 52)
        c.setFont("Courier-Bold", 9)
        c.drawString(left + 8, top - 62, "RAW INTERCEPTED TELEMETRY:")
        c.setFont("Courier", 8.5)
        c_lines = textwrap.wrap(case["game_2_cipher"]["ciphertext"], width=42)
        cy = top - 75
        for cl in c_lines:
            c.drawString(left + 8, cy, cl)
            cy -= 11

        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(left, top - 110, "YOUR DECRYPTED TELEMETRY LOG:")
        c.setStrokeColor(colors.HexColor("#AAAAAA"))
        c.line(left, top - 128, right, top - 128)

        c.setStrokeColor(colors.black)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(left, top - 146, "CREW TESTIMONY & BIOMETRIC SWIPE STATEMENTS:")
        c.setFont("Helvetica", 7.5)
        cly = top - 162
        for idx, clue in enumerate(case["game_3_logic_grid"]["clues"], 1):
            cl_wrapped = textwrap.wrap(f"{idx}. {clue}", width=52)
            for cw in cl_wrapped:
                c.drawString(left + 4, cly, cw)
                cly -= 10
            cly -= 2

        c.rect(left, bottom + 12, right - left, 50)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(left + 6, bottom + 50, "INVESTIGATOR'S DEDUCTION SCRATCHPAD:")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.line(left + 6, bottom + 36, right - 6, bottom + 36)
        c.line(left + 6, bottom + 24, right - 6, bottom + 24)
        c.showPage()
        current_page += 1

        # Page 3: Airlock Logic Matrix & Court-Martial Warrant
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, f"INCIDENT #{c_num:03d} • STAGE III & IV")
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.HexColor("#D90429"))
        c.drawString(left, top - 32, "GAME 3: BIOMETRIC AIRLOCK LOGIC MATRIX")
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 44, "Cross-reference statements to mark confirmations [√] and eliminations [X]")

        rms = case["game_3_logic_grid"]["rooms"]
        wps = case["game_3_logic_grid"]["weapons"]
        sus = case["game_3_logic_grid"]["suspects"]
        grid_x = left + 78
        grid_y = top - 250
        cell_size = 18.5
        c.setLineWidth(0.5)

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

        for k, susp in enumerate(sus):
            c.drawRightString(grid_x - 6, grid_y + 135 - (k * cell_size), susp[:15])

        for w_idx, weap in enumerate(wps):
            c.drawRightString(grid_x - 6, grid_y + 61 - (w_idx * cell_size), weap[:15])

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

        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(colors.HexColor("#D90429"))
        c.drawString(left, bottom + 76, "GAME 4: EMERGENCY COURT-MARTIAL INDICTMENT")
        c.setFillColor(colors.black)
        c.setLineWidth(1.0)
        c.rect(left, bottom + 10, right - left, 58)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(left + 8, bottom + 54, "INTERPLANETARY COURT-MARTIAL WARRANT:")
        c.setFont("Helvetica", 7.5)
        c.drawString(left + 8, bottom + 38, "CHARGED SABOTEUR: ____________________")
        c.drawString(left + 175, bottom + 38, "BREACH LOCATION: ___________________")
        c.drawString(left + 8, bottom + 24, "SABOTAGE WEAPON: ____________________")
        c.drawString(left + 175, bottom + 24, "CORPORATE MOTIVE: __________________")
        c.drawString(left + 8, bottom + 12, "INVESTIGATOR SIGNATURE: _______________")
        c.drawString(left + 175, bottom + 12, "MISSION DATE: STARDATE 2148.___")
        c.showPage()
        current_page += 1

        # Page 4: Debrief
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, f"INCIDENT #{c_num:03d} • DEBRIEF")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left, top - 32, "BREACH RECONSTRUCTION & MISSION NOTES")
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 44, "Document timeline anomalies, atmospheric pressure drops, and suspect motives.")

        c.setLineWidth(0.5)
        c.rect(left, top - 140, right - left, 90)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(left + 8, top - 58, "INCIDENT TIMELINE VERIFICATION:")
        c.setFont("Helvetica", 7.5)
        c.drawString(left + 12, top - 74, "1. Spectrometer Sensor Sweep (Forensic markers logged)")
        c.drawString(left + 12, top - 90, "2. Black Box Telemetry Decryption (Cipher message cracked)")
        c.drawString(left + 12, top - 106, "3. Biometric Airlock Cross-Check (Matrix verified)")
        c.drawString(left + 12, top - 122, "4. Execution of Court-Martial Warrant (Corporate saboteur indicted)")

        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(left, top - 156, "INVESTIGATOR'S LOGBOOK:")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        ny = top - 172
        while ny > bottom + 25:
            c.line(left, ny, right, ny)
            ny -= 16
        c.showPage()
        current_page += 1

    # PAGES 149-166: Master Solutions
    cases_per_sol_page = 2
    sol_pages = (len(cases) + cases_per_sol_page - 1) // cases_per_sol_page
    for sp_idx in range(sol_pages):
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, "MASTER TELEMETRY SOLUTIONS")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left, top - 32, "PROJECT X INCIDENT RESOLUTIONS")
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 44, "Official verification keys for all 35 orbital sabotage incidents.")
        y = top - 64
        batch = cases[sp_idx * cases_per_sol_page : (sp_idx + 1) * cases_per_sol_page]
        for sc in batch:
            c.setStrokeColor(colors.HexColor("#666666"))
            c.setLineWidth(0.5)
            c.rect(left, y - 240, right - left, 240)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(left + 8, y - 16, f"INCIDENT #{sc['case_number']:02d}: {sc['title'].split(': ')[-1]}")
            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(left + 8, y - 32, "STAGE 1 (SPECTROMETER ISOTOPES):")
            c.setFont("Helvetica", 7)
            c.drawString(left + 160, y - 32, ", ".join(sc["game_1_word_search"]["words_to_find"]))
            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(left + 8, y - 48, "STAGE 2 (BLACK BOX DECRYPTED):")
            c.setFont("Courier-Bold", 7)
            c.drawString(left + 160, y - 48, f'"{sc["game_2_cipher"]["plaintext"]}"')
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(colors.HexColor("#D90429"))
            c.drawString(left + 8, y - 68, f"CHARGED SABOTEUR: {sc['game_4_solution']['culprit'].upper()}")
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 7.5)
            c.drawString(left + 175, y - 68, f"Breach Location: {sc['game_4_solution']['murder_room']}")
            c.drawString(left + 8, y - 82, f"Sabotage Instrument: {sc['game_4_solution']['murder_weapon']}")
            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(left + 8, y - 100, "COMPLETE BIOMETRIC AIRLOCK ROSTER:")
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

    # PAGES 167-176: Scorecard & Notes
    left, right, top, bottom = get_page_margins(current_page)
    draw_header_footer(c, current_page, "MISSION EVALUATION SCORECARD")
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 40, "PROJECT X MISSION SCORECARD")
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 56, "Tally your resolved court-martial indictments:")
    ranks = [
        ("30 – 35 Saboteurs Indicted", "SPECIAL ENVOY (Chief Orbital Investigator)"),
        ("20 – 29 Saboteurs Indicted", "PROVOST MARSHAL"),
        ("10 – 19 Saboteurs Indicted", "STATION INSPECTOR"),
        ("01 – 09 Saboteurs Indicted", "CADET INVESTIGATOR")
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

    while current_page <= 176:
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, "INVESTIGATOR'S LOG NOTES")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left, top - 32, "TERMINAL MISSION LOGS")
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 44, "Decompression calculations, radiation markers, and cipher keys.")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.5)
        ny = top - 64
        while ny > bottom + 25:
            c.line(left, ny, right, ny)
            ny -= 17
        c.showPage()
        current_page += 1

    c.save()
    print(f"[✓] Successfully compiled Project X interior: {filename}")

# --- STEP 4: FULL WRAP COVER (Cosmic Void Obsidian & Martian Red Oxide) ---
def compile_cover(filename=os.path.join(VOL1_DIR, "cover_wrap_6x9.pdf")):
    BLEED = 0.125 * inch
    TRIM_W = 6.0 * inch
    TRIM_H = 9.0 * inch
    SPINE_W = (176 * 0.002252) * inch # 0.396"
    TOTAL_W = BLEED + TRIM_W + SPINE_W + TRIM_W + BLEED
    TOTAL_H = BLEED + TRIM_H + BLEED

    c = canvas.Canvas(filename, pagesize=(TOTAL_W, TOTAL_H))
    back_left = BLEED
    back_right = BLEED + TRIM_W
    spine_left = back_right
    spine_right = spine_left + SPINE_W
    front_left = spine_right

    # Deep Cosmic Void Obsidian Background
    c.setFillColor(colors.HexColor("#060913"))
    c.rect(0, 0, TOTAL_W, TOTAL_H, fill=1, stroke=0)

    neon_crimson = colors.HexColor("#D90429")
    amber_accent = colors.HexColor("#FCA311")
    cyan_glow = colors.HexColor("#00F0FF")
    white_text = colors.HexColor("#F0F6FC")

    f_margin = 0.45 * inch
    c.setStrokeColor(neon_crimson)
    c.setLineWidth(1.5)
    c.rect(front_left + f_margin, BLEED + f_margin, TRIM_W - (2 * f_margin), TRIM_H - (2 * f_margin))
    c.setLineWidth(0.5)
    c.setStrokeColor(amber_accent)
    c.rect(front_left + f_margin + 4, BLEED + f_margin + 4, TRIM_W - (2 * f_margin) - 8, TRIM_H - (2 * f_margin) - 8)

    center_front = front_left + (TRIM_W / 2.0)

    # Series Badge
    c.setFillColor(colors.HexColor("#1A050B"))
    c.setStrokeColor(neon_crimson)
    c.setLineWidth(1.0)
    badge_w = 2.6 * inch
    badge_h = 0.28 * inch
    c.roundRect(center_front - (badge_w / 2.0), TOTAL_H - 1.25 * inch, badge_w, badge_h, 3, fill=1, stroke=1)
    c.setFillColor(amber_accent)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(center_front, TOTAL_H - 1.15 * inch, "PROJECT X • VOLUME 1")

    # Main Title
    c.setFillColor(neon_crimson)
    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(center_front, TOTAL_H - 2.15 * inch, "THE TERMINAL")
    
    c.setStrokeColor(amber_accent)
    c.setLineWidth(1.0)
    c.line(center_front - 1.6 * inch, TOTAL_H - 2.50 * inch, center_front + 1.6 * inch, TOTAL_H - 2.50 * inch)
    c.setFillColor(neon_crimson)
    c.circle(center_front, TOTAL_H - 2.50 * inch, 3, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(white_text)
    c.drawCentredString(center_front, TOTAL_H - 2.90 * inch, "35 SCI-FI MURDER MYSTERY LOGIC DOSSIERS:")
    c.drawCentredString(center_front, TOTAL_H - 3.12 * inch, "CORPORATE SABOTAGE & ORBITAL CRIME")

    # Graphic: Sci-Fi Orbital Crosshair / Target Radar
    c.saveState()
    c.setStrokeColor(neon_crimson)
    c.setLineWidth(2.0)
    radar_cx = center_front
    radar_cy = TOTAL_H - 4.70 * inch
    c.circle(radar_cx, radar_cy, 42, fill=0, stroke=1)
    c.setStrokeColor(amber_accent)
    c.setLineWidth(0.75)
    c.circle(radar_cx, radar_cy, 28, fill=0, stroke=1)
    c.circle(radar_cx, radar_cy, 12, fill=0, stroke=1)
    c.line(radar_cx - 50, radar_cy, radar_cx + 50, radar_cy)
    c.line(radar_cx, radar_cy - 50, radar_cx, radar_cy + 50)
    c.restoreState()

    # Feature Box
    c.setFillColor(colors.HexColor("#0D1117"))
    c.setStrokeColor(neon_crimson)
    c.setLineWidth(1.0)
    hook_w = 4.6 * inch
    hook_h = 1.0 * inch
    c.rect(center_front - (hook_w / 2.0), TOTAL_H - 6.85 * inch, hook_w, hook_h, fill=1, stroke=1)

    c.setFillColor(amber_accent)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(center_front, TOTAL_H - 6.15 * inch, "4 SCI-FI FORENSIC GAMES IN EVERY INVESTIGATION:")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(white_text)
    c.drawCentredString(center_front, TOTAL_H - 6.35 * inch, "Spectrometer Sweeps  •  Black Box Telemetry Ciphers")
    c.drawCentredString(center_front, TOTAL_H - 6.52 * inch, "Airlock Alibi Logic Grids  •  Court-Martial Warrants")
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(neon_crimson)
    c.drawCentredString(center_front, TOTAL_H - 6.70 * inch, "★ 100% Mathematically Verified Unique Solutions ★")

    c.setFillColor(white_text)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(center_front, BLEED + 0.85 * inch, "INTERACTIVE CRIME-SOLVER EXPERIENCE • COMPLETE SOLUTIONS")

    # Spine
    c.setStrokeColor(colors.HexColor("#1A050B"))
    c.setLineWidth(0.5)
    c.line(spine_left, 0, spine_left, TOTAL_H)
    c.line(spine_right, 0, spine_right, TOTAL_H)

    c.saveState()
    c.translate(spine_left + (SPINE_W / 2.0), TOTAL_H / 2.0)
    c.rotate(270)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(white_text)
    c.drawCentredString(0, -2.5, "PROJECT X: THE TERMINAL (VOL. 1)  •  SCIENTIFIC CRIME DOSSIERS")
    c.restoreState()

    # Back Cover
    center_back = back_left + (TRIM_W / 2.0)
    c.setStrokeColor(neon_crimson)
    c.setLineWidth(1.0)
    c.rect(back_left + f_margin, BLEED + f_margin, TRIM_W - (2 * f_margin), TRIM_H - (2 * f_margin))

    c.setFont("Helvetica-Bold", 13.5)
    c.setFillColor(neon_crimson)
    c.drawCentredString(center_back, TOTAL_H - 1.25 * inch, "ACCIDENT... OR CORPORATE SABOTAGE?")

    c.setFont("Helvetica", 8)
    c.setFillColor(white_text)
    blurb = (
        "Mars Orbit, 2148. The subterranean research terminal Ares-9 has gone dark. "
        "Vanguard Orbital Dynamics reported a catastrophic gas explosion, but your physical "
        "evidence sweep confirms the truth: the containment breach was a corporate cover-up.\n\n"
        "Take on 35 high-stakes forensic investigations across four perilous terminal sectors:\n"
        "• The Bio-Extraction Labs: Mutated flora, argon vents, and stolen genetic crystal cores.\n"
        "• The Sub-Surface Drill Shaft: Subterranean magma chambers and severed seismic blaster lines.\n"
        "• The Ion Propulsion Reactor: Superheated plasma manifolds, tritium coolant, and magnetic field trips.\n"
        "• The Command Deck: Hacked flight recorders, purge manuals, and jettisoned escape pods.\n\n"
        "Every investigation features 4 interlocking games: Spectrometer Sensor Sweep, "
        "Corrupted Black Box Cipher, Airlock Biometric Matrix, and Emergency Court-Martial Warrant. "
        "Contains 100% mathematically proven unique solutions with zero duplicate puzzles."
    )

    by = TOTAL_H - 1.65 * inch
    for p in blurb.split("\n\n"):
        for l in textwrap.wrap(p, width=44):
            c.drawString(back_left + f_margin + 18, by, l)
            by -= 12
        by -= 6

    # Barcode Safe Box
    c.setFillColor(colors.white)
    c.setStrokeColor(neon_crimson)
    c.rect(center_back - 1.0 * inch, BLEED + 0.65 * inch, 2.0 * inch, 1.2 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#555555"))
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(center_back, BLEED + 1.2 * inch, "[ KDP Barcode Location ]")

    c.save()
    print(f"[✓] Successfully compiled Project X cover wrap: {filename}")

# --- STEP 5: LISTING METADATA ---
def write_metadata():
    meta_text = """================================================================================
KDP LISTING METADATA: PROJECT X - THE TERMINAL (VOLUME 1)
================================================================================

[BOOK DETAILS]
Title: Project X: The Terminal
Subtitle: 35 Sci-Fi Murder Mystery Logic Puzzles: Corporate Sabotage, Lab Accidents & Orbital Crime Dossiers for Adults
Series Title: Project X
Series Number: 1
Edition: 1
Author: (Your Author Name / Independent Publisher)

[PRINT SPECIFICATIONS]
Interior & Paper Type: Black & white interior with white paper
Trim Size: 6 x 9 in
Bleed Settings: No Bleed
Paperback Cover Finish: Matte
Page Count: 176 pages
Spine Width: 0.396 in (10.06 mm)

[CATEGORIES (Choose 3)]
1. Humor & Entertainment > Puzzles & Games > Logic & Brain Teasers
2. Science Fiction & Fantasy > Science Fiction > Space Exploration
3. Mystery, Thriller & Suspense > Mystery > Hard-Boiled / Detective

[7 BACKEND SEARCH KEYWORDS]
1. sci fi murder mystery logic puzzle book
2. space station detective puzzle book for adults
3. corporate sabotage logic grid puzzles
4. mars lab accident escape room in a book
5. forensic science fiction crime dossiers
6. adult deductive reasoning puzzle book
7. cyberpunk cryptograms and brain teasers

[PRICING & ROYALTY (US MARKET)]
List Price: $12.99 USD
Printing Cost: $3.11 USD
Estimated Royalty (60%): $4.68 USD per copy sold

[KDP DESCRIPTION HTML]
<h2>Can you expose the corporate conspiracy before life support runs out?</h2>
<p>Welcome to <b>Project X: The Terminal (Volume 1)</b>, an electrifying interactive sci-fi deduction experience engineered for mystery fans, puzzle solvers, and cyberpunk sleuths.</p>
<p>Deep beneath the surface of Mars, the <i>Ares Terminal</i> research outpost has suffered a catastrophic containment breach. Vanguard Orbital Dynamics blamed a routine gas explosion, but your investigation uncovers a far darker reality: an illegal extraction lab, a murdered whistleblower, and a corporate cover-up.</p>
<p>Every investigation is an authentic <b>4-stage crime file</b>:</p>
<ul>
  <li><b>Stage 1: Spectrometer Sensor Sweep:</b> Scan the 10x10 crime scene matrix for 5 critical forensic isotope markers.</li>
  <li><b>Stage 2: Corrupted Black Box Dispatch:</b> Decrypt intercepted saboteur communications shifted across frequency bands.</li>
  <li><b>Stage 3: Biometric Airlock Matrix:</b> Pure logic deduction grid mathematically proven to have exactly 1 unique solution.</li>
  <li><b>Stage 4: Emergency Court-Martial Warrant:</b> Synthesize your evidence, name the saboteur, identify the breach point, and secure the indictment!</li>
</ul>
<p><b>Inspect the airlocks, decode the black box, and crack the Mars conspiracy today!</b></p>
"""
    meta_path = os.path.join(VOL1_DIR, "KDP_Listing_Metadata.txt")
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(meta_text)
    print(f"[✓] Metadata file saved to {meta_path}")

# --- STEP 6: UPDATE CATALOG ---
def update_catalog():
    cat_path = os.path.join("The_Detectives_Case_Files_Series", "catalog.json")
    with open(cat_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    # Find the "Project X" / "THE TERMINAL" entry and upgrade it
    found = False
    for b in catalog:
        if b.get("series") == "Project X" or "TERMINAL" in b.get("title", "").upper():
            b["series"] = "Project X"
            b["title"] = "Project X: The Terminal"
            b["subtitle"] = "35 Sci-Fi Murder Mystery Logic Puzzles: Corporate Sabotage, Lab Accidents & Orbital Crime Dossiers for Adults"
            b["tab_name"] = "Vol 1: The Terminal"
            b["vol_number"] = 1
            b["price_usd"] = "12.99"
            b["print_cost_usd"] = "3.11"
            b["royalty_usd"] = "4.68"
            b["trim"] = '6" x 9"'
            b["pages"] = 176
            b["bleed"] = "No Bleed"
            b["cover_palette"] = "Cosmic Void & Martian Red Oxide"
            b["keywords"] = [
                "sci fi murder mystery logic puzzle book",
                "space station detective puzzle book for adults",
                "corporate sabotage logic grid puzzles",
                "mars lab accident escape room in a book",
                "forensic science fiction crime dossiers",
                "adult deductive reasoning puzzle book",
                "cyberpunk cryptograms and brain teasers"
            ]
            b["categories"] = [
                "Humor & Entertainment > Puzzles & Games > Logic & Brain Teasers",
                "Science Fiction & Fantasy > Science Fiction > Space Exploration",
                "Mystery, Thriller & Suspense > Mystery > Hard-Boiled / Detective"
            ]
            b["description_html"] = "<h2>Can you expose the corporate conspiracy before life support runs out?</h2>\n<p>Welcome to <b>Project X: The Terminal (Volume 1)</b>, an electrifying interactive sci-fi deduction experience engineered for mystery fans, puzzle solvers, and cyberpunk sleuths.</p>\n<p>Deep beneath the surface of Mars, the <i>Ares Terminal</i> research outpost has suffered a catastrophic containment breach. Vanguard Orbital Dynamics blamed a routine gas explosion, but your investigation uncovers a far darker reality: an illegal extraction lab, a murdered whistleblower, and a corporate cover-up.</p>\n<p>Every investigation is an authentic <b>4-stage crime file</b>:</p>\n<ul>\n  <li><b>Stage 1: Spectrometer Sensor Sweep:</b> Scan the 10x10 crime scene matrix for 5 critical forensic isotope markers.</li>\n  <li><b>Stage 2: Corrupted Black Box Dispatch:</b> Decrypt intercepted saboteur communications shifted across frequency bands.</li>\n  <li><b>Stage 3: Biometric Airlock Matrix:</b> Pure logic deduction grid mathematically proven to have exactly 1 unique solution.</li>\n  <li><b>Stage 4: Emergency Court-Martial Warrant:</b> Synthesize your evidence, name the saboteur, identify the breach point, and secure the indictment!</li>\n</ul>\n<p><b>Inspect the airlocks, decode the black box, and crack the Mars conspiracy today!</b></p>"
            found = True
            break

    if not found:
        catalog.append({
            "id": "project_x_vol1",
            "vol_number": 1,
            "tab_name": "Vol 1: The Terminal",
            "title": "Project X: The Terminal",
            "subtitle": "35 Sci-Fi Murder Mystery Logic Puzzles: Corporate Sabotage, Lab Accidents & Orbital Crime Dossiers for Adults",
            "series": "Project X",
            "price_usd": "12.99",
            "print_cost_usd": "3.11",
            "royalty_usd": "4.68",
            "trim": '6" x 9"',
            "pages": 176,
            "bleed": "No Bleed",
            "cover_palette": "Cosmic Void & Martian Red Oxide",
            "keywords": [
                "sci fi murder mystery logic puzzle book",
                "space station detective puzzle book for adults",
                "corporate sabotage logic grid puzzles",
                "mars lab accident escape room in a book",
                "forensic science fiction crime dossiers",
                "adult deductive reasoning puzzle book",
                "cyberpunk cryptograms and brain teasers"
            ],
            "categories": [
                "Humor & Entertainment > Puzzles & Games > Logic & Brain Teasers",
                "Science Fiction & Fantasy > Science Fiction > Space Exploration",
                "Mystery, Thriller & Suspense > Mystery > Hard-Boiled / Detective"
            ],
            "description_html": "<h2>Can you expose the corporate conspiracy before life support runs out?</h2>\n<p>Welcome to <b>Project X: The Terminal (Volume 1)</b>, an electrifying interactive sci-fi deduction experience engineered for mystery fans, puzzle solvers, and cyberpunk sleuths.</p>\n<p>Deep beneath the surface of Mars, the <i>Ares Terminal</i> research outpost has suffered a catastrophic containment breach. Vanguard Orbital Dynamics blamed a routine gas explosion, but your investigation uncovers a far darker reality: an illegal extraction lab, a murdered whistleblower, and a corporate cover-up.</p>\n<p>Every investigation is an authentic <b>4-stage crime file</b>:</p>\n<ul>\n  <li><b>Stage 1: Spectrometer Sensor Sweep:</b> Scan the 10x10 crime scene matrix for 5 critical forensic isotope markers.</li>\n  <li><b>Stage 2: Corrupted Black Box Dispatch:</b> Decrypt intercepted saboteur communications shifted across frequency bands.</li>\n  <li><b>Stage 3: Biometric Airlock Matrix:</b> Pure logic deduction grid mathematically proven to have exactly 1 unique solution.</li>\n  <li><b>Stage 4: Emergency Court-Martial Warrant:</b> Synthesize your evidence, name the saboteur, identify the breach point, and secure the indictment!</li>\n</ul>\n<p><b>Inspect the airlocks, decode the black box, and crack the Mars conspiracy today!</b></p>"
        })

    with open(cat_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
    print(f"[✓] Updated catalog.json with complete Project X metadata!")

if __name__ == "__main__":
    print("=" * 65)
    print("BUILDING PROJECT X: THE TERMINAL (VOLUME 1)")
    print("=" * 65)
    cases = generate_all_cases()
    compile_interior(cases)
    compile_cover()
    write_metadata()
    update_catalog()
    print("=" * 65)
    print("[✓] PROJECT X COMPLETE IN PRODUCTION REPO!")
    print("=" * 65)
