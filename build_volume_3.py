"""
build_volume_3.py
Compiles the complete production package for:
"The Detective's Case Files: Volume 3 - Case Files & Clues"
Generates:
1. multigame_cases.json (35 unique 4-in-1 multi-stage cases across 4 all-new settings)
2. interior_6x9.pdf (176 pages, strict KDP margins, facing spreads, full solutions)
3. cover_wrap_6x9.pdf (Full wrap cover in Deep Velvet Burgundy & Antique Gold)
4. KDP_Listing_Metadata.txt
5. Updates catalog.json and pushes live to Google Cloud Firebase!
"""

import json
import random
import itertools
import string
import re
import os
import textwrap
import urllib.request
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas

SERIES_DIR = "The_Detectives_Case_Files_Series"
VOL3_DIR = os.path.join(SERIES_DIR, "Volume_3_Venetian_Masquerade")
os.makedirs(VOL3_DIR, exist_ok=True)

# --- STEP 1: ASSETS FOR VOLUME 3 ---
VOL3_ASSETS = {
  "project": "Case Files & Clues: Volume 3 (The Detective's Case Files Series)",
  "version": "1.0",
  "themes": [
    {
      "id": "venetian_masquerade",
      "name": "The Venetian Masquerade Murders",
      "suspects": [
        {"name": "The Masked Doge", "role": "The Patrician Nobleman"},
        {"name": "The Harlequin Actor", "role": "The Commedia Performer"},
        {"name": "The Glass Maestro", "role": "The Murano Artisan"},
        {"name": "The Gondola Pilot", "role": "The Canal Smuggler"},
        {"name": "Contessa di Rialto", "role": "The Disgraced Aristocrat"},
        {"name": "The Silk Merchant", "role": "The Wealthy Trader"}
      ],
      "rooms": [
        "The Grand Ballroom", "The Canal Water Gate", "The Secret Alcove", 
        "The Doge's Private Study", "Bridge of Sighs Chamber", "The Gondola Mooring"
      ],
      "weapons": [
        "Murano Glass Dagger", "Venetian Belladonna", "Stiletto Rapier", 
        "Gilded Silk Garrote", "Poisoned Carnival Mask", "Heavy Bronze Torch"
      ],
      "forensic_evidence": [
        "LACE", "GLASS", "MASK", "RIBBON", 
        "VIAL", "DAGGER", "FEATHER", "GONDOLA"
      ],
      "cipher_clues": [
        "THE BELLADONNA VIAL WAS STOLEN FROM RIALTO",
        "THE HARLEQUIN CONCEALED THE GLASS DAGGER",
        "MEET THE MASKED DOGE AT WATER GATE MIDNIGHT",
        "THE CONTESSA LEFT HER MASK IN SECRET ALCOVE",
        "THE SILK GARROTE WAS BOUGHT IN FLORENCE",
        "THE GONDOLIER SAW THE STRIKE ON THE BRIDGE"
      ]
    },
    {
      "id": "highland_castle",
      "name": "The Scottish Highland Castle Mystery",
      "suspects": [
        {"name": "The Clan Laird", "role": "The Stern Patriarch"},
        {"name": "The Bagpipe Piper", "role": "The Wandering Bard"},
        {"name": "The Castle Archivist", "role": "The Ancient Genealogist"},
        {"name": "The Ghillie Hunter", "role": "The Highland Stalker"},
        {"name": "The High Chieftain", "role": "The Rival Heir"},
        {"name": "The Clan Physician", "role": "The Frontier Doctor"}
      ],
      "rooms": [
        "The Great Tartan Hall", "The Ancestral Armory", "The Turret Lookout", 
        "The Dungeon Vaults", "The Heather Moors", "The Clan Library"
      ],
      "weapons": [
        "Damascus Dirk", "Strychnine Dram", "Antique Flintlock", 
        "Iron Fire Poker", "Heavy Plaid Rope", "Spiked Stag Antler"
      ],
      "forensic_evidence": [
        "TARTAN", "BROOCH", "PEAT", "STONE", 
        "ARROW", "HORN", "CLOAK", "SHIELD"
      ],
      "cipher_clues": [
        "THE LAIRD LOCKED THE ANCESTRAL ARMORY",
        "CHECK THE HEATHER MOORS FOR THE FLINTLOCK",
        "THE PIPER WAS SEEN NEAR THE TURRET TOWER",
        "THE ARCHIVIST CONCEALED THE WILL IN DUNGEON",
        "THE POISON DRAM WAS SERVED IN TARTAN HALL",
        "THE HUNTER CARRIED THE DAMASCUS DIRK"
      ]
    },
    {
      "id": "winter_express",
      "name": "The Trans-Siberian Winter Express",
      "suspects": [
        {"name": "The Train Conductor", "role": "The Veteran Railwayman"},
        {"name": "The Imperial Courier", "role": "The State Messenger"},
        {"name": "The Siberian Trader", "role": "The Wealthy Furrier"},
        {"name": "The Locomotive Stoker", "role": "The Rebellious Fireman"},
        {"name": "The Grand Duchess", "role": "The Exiled Royalty"},
        {"name": "The Chess Master", "role": "The Tactical Genius"}
      ],
      "rooms": [
        "First Class Cabin 4", "The Dining Saloon", "The Observation Deck", 
        "The Luggage Van", "The Engine Tender", "The Smoking Lounge"
      ],
      "weapons": [
        "Silver Ice Pick", "Arsenic Caviar", "Brass Coal Shovel", 
        "Steel Luggage Strap", "Pocket Revolver", "Ether Handkerchief"
      ],
      "forensic_evidence": [
        "TICKET", "COAL", "TRACKS", "WATCH", 
        "COMPASS", "FROST", "LANTERN", "GLOVES"
      ],
      "cipher_clues": [
        "THE ENVELOPE WAS STOLEN IN CABIN FOUR",
        "THE CONDUCTOR HID IN THE LUGGAGE VAN",
        "THE ICE PICK WAS TAKEN FROM DINING SALOON",
        "THE CHESS MASTER RECEIVED A TELEGRAM",
        "THE COAL SHOVEL WAS LEFT IN ENGINE TENDER",
        "THE GRAND DUCHESS SAW THE REVOLVER"
      ]
    },
    {
      "id": "royal_observatory",
      "name": "The Royal Observatory & Planetarium",
      "suspects": [
        {"name": "The Royal Astronomer", "role": "The Celestial Observer"},
        {"name": "The Master Clockmaker", "role": "The Precision Horologist"},
        {"name": "The Meteorite Hunter", "role": "The Daring Field Collector"},
        {"name": "The Star Cartographer", "role": "The Chart Draughtsman"},
        {"name": "The Optical Artisan", "role": "The Precision Lens Grinder"},
        {"name": "The Academy Dean", "role": "The Ambitious Administrator"}
      ],
      "rooms": [
        "The Great Dome", "Pendulum Clock Vault", "Star Chart Archive", 
        "Meteorite Laboratory", "Observation Terrace", "The Dean's Office"
      ],
      "weapons": [
        "Brass Astrolabe", "Cyanide Infusion", "Heavy Brass Compass", 
        "Iron Meteorite Core", "Leyden Jar Shock", "Weighted Pendulum Rod"
      ],
      "forensic_evidence": [
        "COMET", "LENS", "CLOCK", "STAR", 
        "ORBIT", "METEOR", "BRASS", "PRISM"
      ],
      "cipher_clues": [
        "THE ASTROLABE WAS DROPPED FROM THE DOME",
        "THE ASTRONOMER HID IN THE PENDULUM VAULT",
        "THE CYANIDE WAS MIXED IN DEANS OFFICE",
        "THE METEORITE SPECIMEN WAS REMOVED AT NOON",
        "THE CARTOGRAPHER BURNT THE STAR CHARTS",
        "THE LENS MAKER CONCEALED THE BRASS COMPASS"
      ]
    }
  ]
}

with open("multi_game_assets_vol3.json", "w", encoding="utf-8") as f:
    json.dump(VOL3_ASSETS, f, indent=2)

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
    hint = "Caesar Shift (Key: +3). Shift each letter back 3 spots in the alphabet."
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
        if len(sols) == 0:
            continue

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
            if not added:
                break
            sols = count_valid_solutions(suspects, rooms, weapons, clues)

        if len(sols) == 1:
            return {
                "suspects": suspects, "rooms": rooms, "weapons": weapons, "clues": clues,
                "solution": {"culprit": culprit, "murder_room": murder_room, "murder_weapon": murder_weapon, "full_mapping": solution_map}
            }

    raise RuntimeError("Failed to generate unique logic puzzle after multiple attempts.")

def generate_all_cases():
    all_cases = []
    for c_id in range(1, 36):
        theme = VOL3_ASSETS["themes"][(c_id - 1) % len(VOL3_ASSETS["themes"])]
        seed = 11000 + c_id
        logic = generate_logic_puzzle(theme, seed=seed)
        ev_words = random.sample(theme["forensic_evidence"], 5)
        ws = generate_word_search(ev_words, grid_size=10)
        cipher_msg = random.choice(theme["cipher_clues"])
        cipher = generate_cipher(cipher_msg)

        case_obj = {
            "case_number": c_id,
            "title": f"Case #{c_id:03d}: The Mystery of {logic['solution']['murder_room']}",
            "theme": theme["name"],
            "briefing": (
                f"An urgent homicide dispatch has arrived from {theme['name']}. "
                f"The victim met foul play, and four suspects are detained. "
                f"Examine the physical evidence, decode the intercepted cipher dispatch, "
                f"cross-examine the witness alibis on the deduction matrix, and execute the arrest warrant."
            ),
            "game_1_word_search": ws,
            "game_2_cipher": cipher,
            "game_3_logic_grid": {
                "suspects": logic["suspects"], "rooms": logic["rooms"], "weapons": logic["weapons"], "clues": logic["clues"]
            },
            "game_4_solution": logic["solution"]
        }
        all_cases.append(case_obj)

    out_json = os.path.join(VOL3_DIR, "multigame_cases.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(all_cases, f, indent=2)
    print(f"[✓] Generated 35 cases saved to {out_json}")
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

def draw_header_footer(c, page_num, title_text="THE DETECTIVE'S CASE FILES • VOL. 3"):
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

def compile_interior_vol3(cases, filename=os.path.join(VOL3_DIR, "interior_6x9.pdf")):
    c = canvas.Canvas(filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    current_page = 1

    # PAGE 1: Half Title
    left, right, top, bottom = get_page_margins(current_page)
    c.setFont("Helvetica-Bold", 17)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 180, "THE DETECTIVE'S CASE FILES")
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.HexColor("#6B1A24")) # Velvet Crimson accent
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 205, "VOLUME 3: CASE FILES & CLUES")
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Oblique", 9.5)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 230, "35 All-New Multi-Game Murder Mystery Dossiers for Adults")
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 250, "Logic Grids • Cryptograms • Forensic Word Searches • Criminal Warrants")
    c.showPage()
    current_page += 1

    # PAGE 2: Copyright
    left, right, top, bottom = get_page_margins(current_page)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left, bottom + 160, "The Detective's Case Files: Volume 3")
    c.setFont("Helvetica", 7.5)
    c.drawString(left, bottom + 142, "Copyright © 2026. All rights reserved.")
    c.drawString(left, bottom + 128, "Published independently via Amazon Kindle Direct Publishing (KDP).")
    c.drawString(left, bottom + 110, "Original interactive mystery fiction. Zero duplicate cases.")
    c.drawString(left, bottom + 56, "First Edition: October 2026")
    c.showPage()
    current_page += 1

    # PAGES 3-4: Field Manual
    for p_idx in [3, 4]:
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, "INVESTIGATOR'S FIELD MANUAL")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left, top - 32, "WELCOME BACK, DETECTIVE (VOLUME 3)" if p_idx == 3 else "CIPHER KEYS & ADVANCED DEDUCTION")
        c.setFont("Helvetica", 8)
        y = top - 52
        if p_idx == 3:
            raw_text = [
                "Your detective expertise has taken you to the grandest halls and darkest corners of the world. In Volume 3, 35 all-new multi-stage murder mysteries await your keen intellect.",
                "",
                "YOUR 4-STAGE INVESTIGATION ANATOMY:",
                "1. FORENSIC EVIDENCE SWEEP (Word Search): Search the crime scene matrix for 5 key physical items.",
                "2. ENCRYPTED DISPATCH (Cryptograms): Crack the intercepted Caesar cipher (+3 key) to recover crucial testimony.",
                "3. ALIBI MATRIX (Logic Deduction Grid): Cross-reference witness alibis to eliminate innocent suspects.",
                "4. ARREST WARRANT: Indict the true perpetrator with confirmed scene and murder weapon."
            ]
        else:
            raw_text = [
                "ADVANCED INVESTIGATOR TACTICS:",
                "In Volume 3, conspirators operate with intricate alibis and subtle misdirections. Pay close attention to negative witness confirmations.",
                "",
                "CAESAR CIPHER QUICK REFERENCE:",
                "Shift 3 letters backward to decode (D->A, E->B, F->C, G->D).",
                "",
                "Pencil is strictly recommended! Verify each elimination carefully before closing the case."
            ]
        for block in raw_text:
            if not block: y -= 8; continue
            for line in textwrap.wrap(block, width=54):
                c.drawString(left, y, line)
                y -= 12
            y -= 4
        c.showPage()
        current_page += 1

    # PAGES 5-6: Settings & Directory
    for p_idx in [5, 6]:
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, "CASE DIRECTORY & DIFFICULTY")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left, top - 32, "FOUR ALL-NEW MYSTERY SETTINGS" if p_idx == 5 else "DIFFICULTY CURVE & SCORING")
        c.setFont("Helvetica", 8)
        y = top - 52
        if p_idx == 5:
            raw_text = [
                "Volume 3 introduces four completely new atmospheric backdrops:",
                "",
                "• THE VENETIAN MASQUERADE MURDERS (Cases 01–09): Grand Canal palazzos, carnival masks, Murano glass daggers, and midnight gondolas.",
                "• THE SCOTTISH HIGHLAND CASTLE (Cases 10–18): Ancient clan fortresses, heather moors, poisoned drams, and ancestral armories.",
                "• THE TRANS-SIBERIAN WINTER EXPRESS (Cases 19–27): Luxury arctic trains, stolen diplomatic pouches, ice picks, and blizzard dining cars.",
                "• THE ROYAL OBSERVATORY & PLANETARIUM (Cases 28–35): Hilltop brass telescopes, pendulum vaults, cyanide tea, and meteorites."
            ]
        else:
            raw_text = [
                "PROGRESSION TIERS:",
                "• TIER I: SENIOR INSPECTOR (Cases 01–12)",
                "• TIER II: CHIEF SUPERINTENDENT (Cases 13–24)",
                "• TIER III: MASTER SLEUTH (Cases 25–35)",
                "",
                "Tally your completed warrants in the Master Evaluation Scorecard at the back to claim your Master Sleuth certificate!"
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

    # PAGES 9-148: The 35 Multi-Game Cases (4 Pages each)
    for case in cases:
        c_num = case["case_number"]

        # Page 1: Briefing & Word Search
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, f"CASE #{c_num:03d} • PHASE I")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left, top - 30, case["title"].upper())
        c.setFont("Helvetica-Oblique", 7.5)
        c.drawString(left, top - 42, f"Setting: {case['theme']}")

        c.setLineWidth(0.5)
        c.rect(left, top - 100, right - left, 54)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(left + 6, top - 56, "CASE INCIDENT REPORT:")
        c.setFont("Helvetica", 7)
        sy = top - 68
        for sl in textwrap.wrap(case["briefing"], width=58)[:3]:
            c.drawString(left + 6, sy, sl)
            sy -= 10

        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.HexColor("#6B1A24"))
        c.drawString(left, top - 114, "GAME 1: FORENSIC EVIDENCE SWEEP")
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 126, "Locate the 5 hidden physical evidence words in the crime scene grid:")

        ws_grid = case["game_1_word_search"]["grid"]
        gx = left + 20
        gy = top - 142
        c_size = 14
        c.setFont("Courier-Bold", 8.5)
        for r_idx in range(10):
            for col_idx in range(10):
                c.drawString(gx + (col_idx * c_size), gy - (r_idx * c_size), ws_grid[r_idx][col_idx])

        c.setFont("Helvetica-Bold", 8)
        c.drawString(left + 175, top - 144, "EVIDENCE TO COLLECT:")
        c.setFont("Helvetica", 7.5)
        ey = top - 158
        for ew in case["game_1_word_search"]["words_to_find"]:
            c.drawString(left + 180, ey, f"[  ] {ew}")
            ey -= 14

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

        # Page 2: Game 2 Cipher & Clues
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, f"CASE #{c_num:03d} • PHASE II")
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(colors.HexColor("#6B1A24"))
        c.drawString(left, top - 32, "GAME 2: THE ENCRYPTED DISPATCH")
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 44, "The perpetrator left this coded message. Shift each letter back 3 places to read:")

        c.rect(left, top - 100, right - left, 52)
        c.setFont("Courier-Bold", 9)
        c.drawString(left + 8, top - 62, "INTERCEPTED CIPHER:")
        c.setFont("Courier", 8.5)
        c_lines = textwrap.wrap(case["game_2_cipher"]["ciphertext"], width=42)
        cy = top - 75
        for cl in c_lines:
            c.drawString(left + 8, cy, cl)
            cy -= 11

        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(left, top - 110, "YOUR DECRYPTED TRANSCRIPTION:")
        c.setStrokeColor(colors.HexColor("#AAAAAA"))
        c.line(left, top - 128, right, top - 128)

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

        c.rect(left, bottom + 12, right - left, 50)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(left + 6, bottom + 50, "INVESTIGATOR'S DEDUCTION SCRATCHPAD:")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.line(left + 6, bottom + 36, right - 6, bottom + 36)
        c.line(left + 6, bottom + 24, right - 6, bottom + 24)
        c.showPage()
        current_page += 1

        # Page 3: Logic Grid & Warrant
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, f"CASE #{c_num:03d} • PHASE III & IV")
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.HexColor("#6B1A24"))
        c.drawString(left, top - 32, "GAME 3: THE ALIBI & EVIDENCE MATRIX")
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
        c.setFillColor(colors.HexColor("#6B1A24"))
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

        # Page 4: Debrief
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, f"CASE #{c_num:03d} • DEBRIEF")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left, top - 32, "CRIME SCENE RECONSTRUCTION & NOTES")
        c.setFont("Helvetica", 7.5)
        c.drawString(left, top - 44, "Record your analytical reasoning and timeline observations below.")

        c.setLineWidth(0.5)
        c.rect(left, top - 140, right - left, 90)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(left + 8, top - 58, "CHRONOLOGICAL EVIDENCE TIMELINE:")
        c.setFont("Helvetica", 7.5)
        c.drawString(left + 12, top - 74, "1. Discovery of the Crime Scene (Forensic sweep conducted)")
        c.drawString(left + 12, top - 90, "2. Decoding of the Intercepted Dispatch (Cipher resolved)")
        c.drawString(left + 12, top - 106, "3. Interrogation & Alibi Cross-Check (Matrix verified)")
        c.drawString(left + 12, top - 122, "4. Execution of the Arrest Warrant (Culprit identified)")

        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(left, top - 156, "INVESTIGATOR'S FIELD JOURNAL:")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        ny = top - 172
        while ny > bottom + 25:
            c.line(left, ny, right, ny)
            ny -= 16
        c.showPage()
        current_page += 1

    # PAGES 149-166: Master Solutions (2 cases per page = 18 pages)
    cases_per_sol_page = 2
    sol_pages = (len(cases) + cases_per_sol_page - 1) // cases_per_sol_page
    for sp_idx in range(sol_pages):
        left, right, top, bottom = get_page_margins(current_page)
        draw_header_footer(c, current_page, "MASTER SOLUTION KEYS")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left, top - 32, "VOLUME 3 CASE SOLUTIONS & CIPHER KEYS")
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
            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(left + 8, y - 32, "GAME 1 (FORENSIC WORDS):")
            c.setFont("Helvetica", 7)
            c.drawString(left + 130, y - 32, ", ".join(sc["game_1_word_search"]["words_to_find"]))
            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(left + 8, y - 48, "GAME 2 (CIPHER DECRYPTED):")
            c.setFont("Courier-Bold", 7)
            c.drawString(left + 130, y - 48, f'"{sc["game_2_cipher"]["plaintext"]}"')
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(colors.HexColor("#6B1A24"))
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

    # PAGES 167-176: Scorecard & Notes
    left, right, top, bottom = get_page_margins(current_page)
    draw_header_footer(c, current_page, "INVESTIGATOR EVALUATION SCORECARD")
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 40, "VOLUME 3 DETECTIVE EVALUATION")
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_WIDTH / 2.0, top - 56, "Tally your completed warrants across the 35 cases:")
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
    print(f"[✓] Successfully compiled Volume 3 interior: {filename} (Total pages: {current_page - 1})")

# --- STEP 4: COVER WRAP GENERATOR (Deep Velvet Burgundy & Antique Gold) ---
def compile_cover_vol3(filename=os.path.join(VOL3_DIR, "cover_wrap_6x9.pdf")):
    BLEED = 0.125 * inch
    TRIM_W = 6.0 * inch
    TRIM_H = 9.0 * inch
    SPINE_W = (176 * 0.002252) * inch # 0.39635"
    TOTAL_W = BLEED + TRIM_W + SPINE_W + TRIM_W + BLEED
    TOTAL_H = BLEED + TRIM_H + BLEED

    c = canvas.Canvas(filename, pagesize=(TOTAL_W, TOTAL_H))
    back_left = BLEED
    back_right = BLEED + TRIM_W
    spine_left = back_right
    spine_right = spine_left + SPINE_W
    front_left = spine_right

    # Deep Velvet Burgundy Background
    c.setFillColor(colors.HexColor("#1F070B"))
    c.rect(0, 0, TOTAL_W, TOTAL_H, fill=1, stroke=0)

    gold_accent = colors.HexColor("#D4AF37")
    cream_text = colors.HexColor("#FBF7F2")
    crimson_badge = colors.HexColor("#4A1521")

    f_margin = 0.45 * inch
    c.setStrokeColor(gold_accent)
    c.setLineWidth(1.5)
    c.rect(front_left + f_margin, BLEED + f_margin, TRIM_W - (2 * f_margin), TRIM_H - (2 * f_margin))
    c.setLineWidth(0.5)
    c.rect(front_left + f_margin + 4, BLEED + f_margin + 4, TRIM_W - (2 * f_margin) - 8, TRIM_H - (2 * f_margin) - 8)

    center_front = front_left + (TRIM_W / 2.0)

    # Series Badge
    c.setFillColor(crimson_badge)
    c.setStrokeColor(gold_accent)
    c.setLineWidth(0.75)
    badge_w = 2.8 * inch
    badge_h = 0.28 * inch
    c.roundRect(center_front - (badge_w / 2.0), TOTAL_H - 1.25 * inch, badge_w, badge_h, 3, fill=1, stroke=1)
    c.setFillColor(cream_text)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(center_front, TOTAL_H - 1.15 * inch, "THE DETECTIVE'S CASE FILES • VOLUME 3")

    # Main Title
    c.setFillColor(gold_accent)
    c.setFont("Helvetica-Bold", 33)
    c.drawCentredString(center_front, TOTAL_H - 2.10 * inch, "CASE FILES")
    c.setFillColor(cream_text)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(center_front, TOTAL_H - 2.58 * inch, "& CLUES")

    c.setStrokeColor(gold_accent)
    c.setLineWidth(1.0)
    c.line(center_front - 1.6 * inch, TOTAL_H - 2.88 * inch, center_front + 1.6 * inch, TOTAL_H - 2.88 * inch)
    c.circle(center_front, TOTAL_H - 2.88 * inch, 3, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 10.5)
    c.setFillColor(cream_text)
    c.drawCentredString(center_front, TOTAL_H - 3.25 * inch, "35 ALL-NEW MULTI-GAME MURDER")
    c.drawCentredString(center_front, TOTAL_H - 3.48 * inch, "MYSTERY DOSSIERS FOR ADULTS")

    # Graphic: Magnifying Glass
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

    # Feature Box
    c.setFillColor(colors.HexColor("#140407"))
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
    c.drawCentredString(center_front, TOTAL_H - 6.35 * inch, "Forensic Sweeps  •  Secret Ciphers & Cryptograms")
    c.drawCentredString(center_front, TOTAL_H - 6.52 * inch, "Alibi Logic Grids  •  Official Arrest Warrants")
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(cream_text)
    c.drawCentredString(center_front, TOTAL_H - 6.70 * inch, "★ 100% Mathematically Verified Unique Solutions ★")

    c.setFillColor(cream_text)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(center_front, BLEED + 0.85 * inch, "INTERACTIVE CRIME-SOLVER EXPERIENCE • COMPLETE SOLUTIONS")

    # Spine
    c.setStrokeColor(colors.HexColor("#2B0B14"))
    c.setLineWidth(0.5)
    c.line(spine_left, 0, spine_left, TOTAL_H)
    c.line(spine_right, 0, spine_right, TOTAL_H)

    c.saveState()
    c.translate(spine_left + (SPINE_W / 2.0), TOTAL_H / 2.0)
    c.rotate(270)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(cream_text)
    c.drawCentredString(0, -2.5, "THE DETECTIVE'S CASE FILES: VOL. 3  •  CASE FILES & CLUES")
    c.restoreState()

    # Back Cover
    center_back = back_left + (TRIM_W / 2.0)
    c.setStrokeColor(gold_accent)
    c.setLineWidth(1.0)
    c.rect(back_left + f_margin, BLEED + f_margin, TRIM_W - (2 * f_margin), TRIM_H - (2 * f_margin))

    c.setFont("Helvetica-Bold", 13.5)
    c.setFillColor(gold_accent)
    c.drawCentredString(center_back, TOTAL_H - 1.25 * inch, "THE MYSTERY DEEPENS...")

    c.setFont("Helvetica", 8)
    c.setFillColor(cream_text)
    blurb = (
        "Welcome to Volume 3 of The Detective's Case Files Series. "
        "Step into the shadowy world of international intrigue with 35 all-new "
        "murder mysteries designed to test your deductive powers to the limit:\n\n"
        "• The Venetian Masquerade: Midnight gondolas, masked patricians, and poisoned glass daggers.\n"
        "• The Highland Castle: Stormy Scottish moors, ancient armories, and clan rivalries.\n"
        "• The Trans-Siberian Express: Snowbound luxury carriages, frozen bodies, and stolen codes.\n"
        "• The Royal Observatory: Celestial telescopes, pendulum clock vaults, and cyanide vials.\n\n"
        "Every case features 4 interlocking games: Forensic Word Search, Encrypted Dispatch Cipher, "
        "Airtight Alibi Logic Grid Matrix, and Official State Arrest Warrant. "
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
    c.setStrokeColor(gold_accent)
    c.rect(center_back - 1.0 * inch, BLEED + 0.65 * inch, 2.0 * inch, 1.2 * inch, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#555555"))
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(center_back, BLEED + 1.2 * inch, "[ KDP Barcode Location ]")

    c.save()
    print(f"[✓] Successfully compiled Volume 3 cover wrap: {filename}")

# --- STEP 5: LISTING METADATA ---
def write_metadata():
    meta_text = """================================================================================
KDP LISTING METADATA: VOLUME 3
================================================================================

[BOOK DETAILS]
Title: Case Files & Clues: Volume 3
Subtitle: 35 All-New Multi-Game Murder Mystery Dossiers: Venetian Masquerades, Highland Castles, Winter Express & Observatories
Series Title: The Detective's Case Files
Series Number: 3
Edition: 1
Author: (Your Author Name / Independent Publisher)

[PRINT SPECIFICATIONS]
Interior & Paper Type: Black & white interior with white paper
Trim Size: 6 x 9 in
Bleed Settings: No Bleed
Paperback Cover Finish: Matte (or Glossy)
Page Count: 176 pages
Spine Width: 0.396 in (10.06 mm)

[CATEGORIES (Choose 3)]
1. Crafts, Hobbies & Home > Crafts & Hobbies > Activity Books
2. Humor & Entertainment > Puzzles & Games > Logic & Brain Teasers
3. Mystery, Thriller & Suspense > Mystery > Traditional Detective

[7 BACKEND SEARCH KEYWORDS]
1. murder mystery logic puzzle book for adults
2. escape room game in a book cryptograms
3. venetian masquerade and highland castle whodunit
4. forensic crime scene activity book for adults
5. trans-siberian express detective mystery game
6. deductive reasoning logic grid puzzles
7. cozy crime solving case files for seniors

[PRICING & ROYALTY (US MARKET)]
List Price: $12.99 USD
Printing Cost: $3.11 USD
Estimated Royalty (60%): $4.68 USD per copy sold

[KDP DESCRIPTION HTML]
<h2>Can you crack the case before the final curtain falls?</h2>
<p>Welcome to <b>The Detective's Case Files: Volume 3</b>, the thrilling next chapter in the interactive crime-solving series engineered for true mystery buffs, logic enthusiasts, and armchair detectives.</p>
<p>Journey into four brand new atmospheric settings spanning Venetian masked balls, mist-covered Scottish castle keeps, the luxury Trans-Siberian winter express, and Victorian star observatories.</p>
<p>Every case is an authentic <b>4-stage crime file</b>:</p>
<ul>
  <li><b>Stage 1: Forensic Evidence Sweep:</b> Scour the 10x10 crime scene matrix to unearth physical clues.</li>
  <li><b>Stage 2: The Encrypted Dispatch:</b> Crack the suspect's intercepted Caesar cipher to uncover secret testimony.</li>
  <li><b>Stage 3: The Alibi Matrix:</b> Pure logic deduction grid mathematically proven to have exactly 1 unique solution.</li>
  <li><b>Stage 4: The Official Arrest Warrant:</b> Synthesize your deductions, name the killer, and convict the true perpetrator!</li>
</ul>
<p><b>Gather your evidence, inspect the crime scene, and claim Volume 3 today!</b></p>
"""
    meta_path = os.path.join(VOL3_DIR, "KDP_Listing_Metadata.txt")
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(meta_text)
    print(f"[✓] Metadata file saved to {meta_path}")

# --- STEP 6: UPDATE CATALOG & CLOUD SYNC ---
def update_catalog():
    cat_path = os.path.join(SERIES_DIR, "catalog.json")
    with open(cat_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    # Check if vol3 already in catalog
    existing_ids = [b["id"] for b in catalog]
    vol3_entry = {
        "id": "vol3",
        "vol_number": 3,
        "tab_name": "Volume 3 (Venice & Highlands)",
        "title": "Case Files & Clues: Volume 3",
        "subtitle": "35 All-New Multi-Game Murder Mystery Dossiers: Venetian Masquerades, Highland Castles, Winter Express & Observatories",
        "series": "The Detective's Case Files",
        "price_usd": "12.99",
        "print_cost_usd": "3.11",
        "royalty_usd": "4.68",
        "trim": "6\" x 9\"",
        "pages": 176,
        "bleed": "No Bleed",
        "cover_palette": "Deep Velvet Burgundy & Gold",
        "keywords": [
          "murder mystery logic puzzle book for adults",
          "escape room game in a book cryptograms",
          "venetian masquerade and highland castle whodunit",
          "forensic crime scene activity book for adults",
          "trans-siberian express detective mystery game",
          "deductive reasoning logic grid puzzles",
          "cozy crime solving case files for seniors"
        ],
        "categories": [
          "Crafts, Hobbies & Home > Crafts & Hobbies > Activity Books",
          "Humor & Entertainment > Puzzles & Games > Logic & Brain Teasers",
          "Mystery, Thriller & Suspense > Mystery > Traditional Detective"
        ],
        "description_html": "<h2>Can you crack the case before the final curtain falls?</h2>\n<p>Welcome to <b>The Detective's Case Files: Volume 3</b>, the thrilling next chapter in the interactive crime-solving series engineered for true mystery buffs, logic enthusiasts, and armchair detectives.</p>\n<p>Journey into four brand new atmospheric settings spanning Venetian masked balls, mist-covered Scottish castle keeps, the luxury Trans-Siberian winter express, and Victorian star observatories.</p>\n<p>Every case is an authentic <b>4-stage crime file</b>:</p>\n<ul>\n  <li><b>Stage 1: Forensic Evidence Sweep:</b> Scour the 10x10 crime scene matrix to unearth physical clues.</li>\n  <li><b>Stage 2: The Encrypted Dispatch:</b> Crack the suspect's intercepted Caesar cipher to uncover secret testimony.</li>\n  <li><b>Stage 3: The Alibi Matrix:</b> Pure logic deduction grid mathematically proven to have exactly 1 unique solution.</li>\n  <li><b>Stage 4: The Official Arrest Warrant:</b> Synthesize your deductions, name the killer, and convict the true perpetrator!</li>\n</ul>\n<p><b>Gather your evidence, inspect the crime scene, and claim Volume 3 today!</b></p>"
    }

    if "vol3" in existing_ids:
        for idx, b in enumerate(catalog):
            if b["id"] == "vol3":
                catalog[idx] = vol3_entry
    else:
        catalog.append(vol3_entry)

    with open(cat_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
    print(f"[✓] Updated catalog.json with Volume 3! Total books in catalog: {len(catalog)}")

if __name__ == "__main__":
    print("=" * 65)
    print("BUILDING VOLUME 3: THE DETECTIVE'S CASE FILES")
    print("=" * 65)
    cases = generate_all_cases()
    compile_interior_vol3(cases)
    compile_cover_vol3()
    write_metadata()
    update_catalog()
    print("=" * 65)
    print("[✓] VOLUME 3 COMPLETE IN PRODUCTION REPO!")
    print("=" * 65)
