"""
build_lupin_and_poi_series.py
Builds the complete production suites for 2 brand-new blockbuster series:
1. THE LUPIN HEISTS (15 Volumes - Inspired by Netflix's LUPIN)
2. THE MACHINE PROTOCOLS (15 Volumes - Inspired by Netflix / CBS PERSON OF INTEREST)

Total: 30 New Volumes (Catalog expansion from 100 to 130 books).
Each volume contains:
- 176-Page Interior PDF (6" x 9" Trade Paperback)
- 12.646" x 9.250" Full-Wrap Luxury Vector Cover PDF (0.396" spine)
- High-Resolution Front Cover & Full Wrap PNG Previews
- KDP Listing Copy-Paste Metadata (Categories, 7 Backend Keywords, Blurb HTML)
- Interlocking 4-Stage Forensic Game Engine (Sudoku, Cipher, Logic Grid, Warrant)
- 100% Mathematically Verified Unique Logic Solutions
"""

import os
import json
import time
import textwrap
import pymupdf
from industrial_book_engine import build_interlocking_book
from luxury_cover_engine import generate_luxury_cover

ROOT_DIR = os.path.abspath(".")
CATALOG_PATH = os.path.join(ROOT_DIR, "catalog.json")

def render_cover_previews(cov_pdf_path, out_dir):
    if not os.path.exists(cov_pdf_path):
        return
    doc = pymupdf.open(cov_pdf_path)
    page = doc[0]
    rect = page.rect
    W, H = rect.width, rect.height

    # Full wrap preview
    wrap_pix = page.get_pixmap(dpi=100)
    wrap_pix.save(os.path.join(out_dir, "cover_wrap_preview.png"))

    # Exact front cover 6x9 crop
    x0 = (6.125 + 0.396) / 12.646 * W
    x1 = 12.521 / 12.646 * W
    y0 = 0.125 / 9.250 * H
    y1 = 9.125 / 9.250 * H
    front_pix = page.get_pixmap(clip=pymupdf.Rect(x0, y0, x1, y1), dpi=150)
    front_pix.save(os.path.join(out_dir, "cover_front_preview.png"))

# ==============================================================================
# THE LUPIN HEISTS: 15 VOLUMES
# ==============================================================================
LUPIN_VOLUMES = [
    (1, "The Queens Necklace at the Louvre", "The Lupin Heists: The Queen's Necklace at the Louvre", "#EF233C", "Midnight Indigo & Laser Crimson"),
    (2, "The Catacombs Phantom Vault", "The Catacombs Phantom Vault", "#D4AF37", "Subterranean Slate & Gilded Gold"),
    (3, "The Versailles Masquerade Gala", "The Versailles Masquerade Gala", "#8338EC", "Royal Velvet & Masquerade Amethyst"),
    (4, "The Montmartre Forgers Studio", "The Montmartre Forger's Studio", "#3A86FF", "Pigment Charcoal & Cobalt Blue"),
    (5, "The Musee dOrsay Clockwork Enigma", "The Musée d'Orsay Clockwork Enigma", "#FB5607", "Station Iron & Clockwork Amber"),
    (6, "The Palais Garnier Box Five Riddle", "The Palais Garnier Box Five Riddle", "#06D6A0", "Opera Crimson & Emerald Silk"),
    (7, "The French Riviera Casino Raid", "The French Riviera Casino Raid", "#FF006E", "Baccarat Green & Riviera Magenta"),
    (8, "The Saint-Germain Antique Safe", "The Saint-Germain Antique Safe", "#C9A227", "Hôtel Particulier Walnut & Antique Brass"),
    (9, "The Seine Midnight Barges", "The Seine Midnight Barges", "#1D3557", "River Fog Grey & Deep Pont-Neuf Navy"),
    (10, "The Luxembourg Gardens Syndicate", "The Luxembourg Gardens Syndicate", "#2A9D8F", "Senate Marble & Garden Malachite"),
    (11, "The Eiffel Tower Transmission Code", "The Eiffel Tower Transmission Code", "#E76F51", "Rivet Steel & Sunset Radio Coral"),
    (12, "The Chateau de Chantilly Cup", "The Château de Chantilly Cup", "#7F4F24", "Stallion Leather Russet & Gold Cup"),
    (13, "The Sorbonne Alchemical Manuscript", "The Sorbonne Alchemical Manuscript", "#6A0572", "Parchment Cream & Alchemical Purple"),
    (14, "The Place Vendome Jewel Vault", "The Place Vendôme Jewel Vault", "#0077B6", "Titanium Grey & Vendôme Sapphire"),
    (15, "The Elysee Sovereign Heist", "The Élysée Sovereign Heist", "#FFB703", "Imperial Sovereign Black & Tricolore Gold")
]

# ==============================================================================
# THE MACHINE PROTOCOLS: 15 VOLUMES
# ==============================================================================
POI_VOLUMES = [
    (1, "The Wall Street Irrelevant", "The Machine Protocols: The Wall Street Irrelevant", "#00F5D4", "Carbon Black & Electric Cyan HUD"),
    (2, "The Subway Library Safehouse", "The Subway Library Safehouse", "#FFBE0B", "Subway Iron & Terminal Amber"),
    (3, "The Corrupt Precinct Syndicate", "The Corrupt Precinct Syndicate", "#FF0055", "Police Blue & Syndicate Crimson"),
    (4, "The Darknet Zero-Day Broker", "The Darknet Zero-Day Broker", "#7000FF", "Server Rack Black & Exploit Violet"),
    (5, "The Central Park Sniper Threat", "The Central Park Sniper Threat", "#05F140", "Night Camo & Night Vision Green"),
    (6, "The Decima Infiltration", "The Decima Infiltration", "#00BBF9", "Corporate Glass & Decima Cyan"),
    (7, "The Rikers Island Extraction", "The Rikers Island Extraction", "#F15BB5", "Prison Concrete & Neon Surveillance Pink"),
    (8, "The Grand Central Acoustic Wiretap", "The Grand Central Acoustic Wiretap", "#FF9F1C", "Station Travertine & Sensor Amber"),
    (9, "The Decommissioned Bunker Ambush", "The Decommissioned Bunker Ambush", "#2EC4B6", "Fallout Bunker Steel & Cold Cyan"),
    (10, "The Machine Failsafe Protocol", "The Machine Failsafe Protocol", "#E71D36", "Analog Copper & Core Failsafe Red"),
    (11, "The Brooklyn Navy Yard Smuggling", "The Brooklyn Navy Yard Smuggling", "#4361EE", "Gantry Steel & Harbor Cobalt"),
    (12, "The High-Frequency Trading Heist", "The High-Frequency Trading Heist", "#4CC9F0", "Fiber Optic Trench & Laser Cyan"),
    (13, "The Blacksite Hostage Extraction", "The Blacksite Hostage Extraction", "#F72585", "Off-The-Books Black & Ultraviolet"),
    (14, "The Autonomous Grid Meltdown", "The Autonomous Grid Meltdown", "#7209B7", "Traffic Grid Neon & Power Grid Purple"),
    (15, "The Samaritan Final Directive", "The Samaritan Final Directive", "#3A0CA3", "Totalitarian Obsidian & Deep Directive Blue")
]

# ==============================================================================
# THEME GENERATION FOR LUPIN & POI
# ==============================================================================
def get_lupin_themes(vol_num):
    sectors = [
        ("The Grand Louvre Midnight Gallery", "Assane The Phantom", "Curator Moreau", "Countess De Bellac", "Chief Guard Dubois", "The Master Restorer", "The Art Appraiser",
         "The Mona Lisa Vault", "Grand Gallery Parquet", "Apollo Gold Salon", "Under-Pyramid Sump", "Cour Carree Restorers Attic", "Antique Frame Vault",
         "Laser Cutter Pen", "Diamond Dust Chloroform", "Antique Gilded Stiletto", "Picture Hanging Cable", "Soporific Rose Perfume", "Disguise Latex Mask"),
        ("The Chateau de Versailles Masquerade", "The Cloaked Marquis", "Baroness Vance", "The Opera Virtuoso", "The French Minister", "The Sommelier Pierre", "Assane The Phantom",
         "Hall of Mirrors Parquet", "Kings Private Bedchamber", "Orangerie Citrus Terrace", "Fountain Hydraulic Vault", "Marble Courtyard Crypt", "Secret Servants Gallery",
         "Cyanide Truffle Flute", "Poisoned Pocket Watch", "Golden Chandelier Cord", "Antique Dueling Pistole", "Weighted Velvet Cape", "Venetian Glass Shard"),
        ("The Paris Catacombs Subterranean Vault", "The Catacomb Guide", "Chief Inspector Ganimard", "The Antiquarian Forger", "The Black Market Courier", "Curator Moreau", "Assane The Phantom",
         "The Ossuary Labyrinth", "Crypt of Chiseled Skulls", "Abandoned Metro Tunnel", "Subterranean Spring", "Smugglers Limestone Quarry", "Catacomb Well Alcove",
         "High-Voltage Taser Cane", "Mining Blasting Cap", "Heavy Iron Crowbar", "Piano Wire Strangle Cord", "Limestone Masonry Mallet", "Chloroform Soaked Linen"),
        ("The Monte Carlo Grand Prix Casino Vault", "The Monaco Magnate", "The Card Counter Lady", "Chief Security Officer", "The Superyacht Captain", "Assane The Phantom", "The Belgian Banker",
         "High-Stakes Baccarat Salon", "Underground Cash Vault", "Surveillance Control Bunker", "Rooftop Helipad Catwalk", "VIP Marina Balcony", "Grand Prix Garage Bay",
         "Electromagnetic EMP Pulse", "Serrated Glass Cutter", "Heavy Roulette Wheel Spindle", "Knockout Neuro-Gas", "Silenced Beretta 22", "Titanium Vault Pry Rod")
    ]
    cipher_sentences = [
        "THE STOLEN DIAMOND NECKLACE WAS CONCEALED IN THE FOUNTAIN DRAINAGE SUMP",
        "THE PHANTOM THIEF ESCAPED OVER THE ROOFTOPS IN THE AMBASSADORS VELVET DISGUISE",
        "THE FORGED MASTERPIECE WAS SWAPPED DURING THE MIDNIGHT FIREWORKS CELEBRATION",
        "THE SUBTERRANEAN VAULT PASSKEY WAS ENGRAVED ON THE INSIDE OF THE VINTAGE POCKET WATCH"
    ]
    themes = []
    for s_idx, sec in enumerate(sectors):
        themes.append({
            "id": f"lupin_sec_{s_idx+1}_v{vol_num}",
            "name": sec[0],
            "suspects": [{"name": s, "role": f"Suspect {idx+1}"} for idx, s in enumerate(sec[1:7])],
            "rooms": list(sec[7:13]),
            "weapons": list(sec[13:19]),
            "cipher_clues": [
                f"{cipher_sentences[0]} (CASE {s_idx*9 + 1})",
                f"{cipher_sentences[1]} (CASE {s_idx*9 + 4})",
                f"{cipher_sentences[2]} (CASE {s_idx*9 + 7})",
                f"{cipher_sentences[3]} (CASE {s_idx*9 + 8})"
            ]
        })
    return themes

def get_poi_themes(vol_num):
    sectors = [
        ("The Wall Street Dark Pool Trading Floor", "Analyst Harold", "Contractor Reese", "Detective Carter", "Officer Fusco", "Hedge Fund CEO Sterling", "Decima Operative Greer",
         "High-Frequency Trading Floor", "Sub-Level Server Farm", "Executive Penthouse Suite", "Fiber-Optic Cable Vault", "HVAC Cooling Tower", "Emergency Stairwell Landing",
         "Silenced SIG Sauer P226", "Acoustic Eavesdrop Laser", "Potassium Chloride Syringe", "High-Voltage Server Cable", "Stun Grenade Canister", "Zero-Day Memory Exploit"),
        ("The Decommissioned Subway Library", "The Mysterious Architect", "The Ex-Military Enforcer", "The Rogue Hacker Root", "The Corrupt Syndicate Boss", "Detective Carter", "Analyst Harold",
         "Abandoned Track Platform", "Vault Book Archives", "Analog Relay Switching Room", "Spiral Iron Catwalk", "Old Turnstile Vestibule", "Drainage Sump Pump Bay",
         "Tactical Combat Knife", "Acoustic Wiretap Transmitter", "Chloroform Extraction Mask", "Heavy Steel Railway Spike", "High-Yield Thermite Strip", "Tactical Taser Stunner"),
        ("The 8th Precinct Internal Affairs Bunker", "Captain Quinn", "Lieutenant Simmons", "Detective Carter", "Officer Fusco", "Contractor Reese", "The Undercover Fed",
         "Evidence Locker Vault", "Interrogation Room Three", "Records Microfiche Archives", "Captains Office", "Sally Port Garage Bay", "Rooftop Radio Transmitter Mast",
         "Untraceable 38 Snub Revolver", "Encrypted Radio Jammer", "Lethal Fentanyl Ampoule", "Heavy Police Baton", "Handcuff Chain Strangle", "Corrosive Acid Spray"),
        ("The Decima Cybernetics Supercomputer Vault", "Decima Operative Greer", "Rogue Hacker Root", "Analyst Harold", "The Ex-Military Enforcer", "The Cyber Mercenary", "The Double Agent",
         "AI Core Cold-Room", "Biometric Airlock Chamber", "Cryogenic Chiller Floor", "Satellite Uplink Dome", "Emergency Generator Bay", "Executive Cleanroom Chamber",
         "EMP Pulse Device", "Ceramic Non-Metallic Blade", "Cyanide Inhalation Mask", "High-Current Busbar Discharge", "Silenced Submachine Gun", "Sub-Dermal Neuro-Poison")
    ]
    cipher_sentences = [
        "THE SOCIAL SECURITY NUMBER BELONGS TO THE RETIRED MILITARY CODEBREAKER",
        "THE THREAT LEVEL REACHED MAXIMUM BEFORE THE SUBWAY TRAIN PULLED INTO THE STATION",
        "THE CORRUPT POLICE FRATERNITY PLANNED THE AMBUSH FROM THE UNMARKED SEDAN",
        "THE SATELLITE TELEMETRY FEED WAS INTERCEPTED THROUGH THE PUBLIC PAYPHONE RECEIVER"
    ]
    themes = []
    for s_idx, sec in enumerate(sectors):
        themes.append({
            "id": f"poi_sec_{s_idx+1}_v{vol_num}",
            "name": sec[0],
            "suspects": [{"name": s, "role": f"Suspect {idx+1}"} for idx, s in enumerate(sec[1:7])],
            "rooms": list(sec[7:13]),
            "weapons": list(sec[13:19]),
            "cipher_clues": [
                f"{cipher_sentences[0]} (CASE {s_idx*9 + 1})",
                f"{cipher_sentences[1]} (CASE {s_idx*9 + 4})",
                f"{cipher_sentences[2]} (CASE {s_idx*9 + 7})",
                f"{cipher_sentences[3]} (CASE {s_idx*9 + 8})"
            ]
        })
    return themes

# ==============================================================================
# MAIN COMPILER PIPELINE
# ==============================================================================
def run():
    print("=" * 80)
    print("   PRODUCTION PIPELINE: BUILDING LUPIN & PERSON OF INTEREST SERIES")
    print("=" * 80)
    t_start = time.time()

    # Load existing catalog
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            catalog = json.load(f)
    else:
        catalog = []

    existing_ids = {b.get("id"): b for b in catalog}
    new_books_added = 0

    series_jobs = [
        {
            "series_name": "The Lupin Heists",
            "folder": "The_Lupin_Heists",
            "volumes": LUPIN_VOLUMES,
            "theme_func": get_lupin_themes,
            "category_base": [
                "Humor & Entertainment > Puzzles & Games > Logic & Brain Teasers",
                "Mystery, Thriller & Suspense > Mystery > Heist / Capers",
                "Crafts, Hobbies & Home > Crafts & Hobbies > Activity Books"
            ],
            "keywords": [
                "lupin heist mystery puzzle book for adults",
                "gentleman thief museum escape room in a book",
                "paris detective logic grid brain teasers",
                "forensic art theft case files activity book",
                "laser grid sudoku cryptogram crime puzzles",
                "cozy heist deductive reasoning games for adults",
                "interlocking evidence key mystery puzzle book"
            ],
            "subtitle_fmt": "35 High-Stakes Parisian Heist Dossiers: Laser Grid Sudoku, Coded Calling Cards, Security Alibi Logic Grids & French Gendarmerie Arrest Warrants",
            "desc_headline": "Can you outsmart the Louvre's security grids and pull off the perfect heist?"
        },
        {
            "series_name": "The Machine Protocols",
            "folder": "The_Machine_Protocols",
            "volumes": POI_VOLUMES,
            "theme_func": get_poi_themes,
            "category_base": [
                "Humor & Entertainment > Puzzles & Games > Logic & Brain Teasers",
                "Mystery, Thriller & Suspense > Thrillers > Technological / AI Thrillers",
                "Mystery, Thriller & Suspense > Mystery > Hard-Boiled / Detective"
            ],
            "keywords": [
                "person of interest crime mystery puzzle book",
                "mass surveillance ai logic grid puzzles for adults",
                "cyber thriller deductive reasoning brain teasers",
                "forensic wiretap cipher escape room in a book",
                "cctv tracking crime scene activity book",
                "fbi intelligence asset neutralization mind games",
                "interlocking evidence key predictive crime book"
            ],
            "subtitle_fmt": "35 Predictive AI Crime Dossiers: CCTV Satellite Sudoku, Wiretap Ciphers, Surveillance Suspect Logic Grids & Asset Neutralization Warrants",
            "desc_headline": "You are being watched. The Machine has dropped a new number. Can you stop the crime in time?"
        }
    ]

    for job in series_jobs:
        s_name = job["series_name"]
        folder_base = job["folder"]
        os.makedirs(folder_base, exist_ok=True)
        print(f"\n>>> PROCESSING SERIES: {s_name.upper()} ({len(job['volumes'])} Volumes)")

        for vol_tuple in job["volumes"]:
            vol_num, slug, title, accent_hex, cover_theme = vol_tuple
            clean_slug = slug.replace(" ", "_").replace("'", "").replace("&", "and").replace(":", "")
            vol_folder_name = f"Volume_{vol_num:02d}_{clean_slug}"
            book_dir = os.path.join(folder_base, vol_folder_name)
            os.makedirs(book_dir, exist_ok=True)

            book_id = f"{s_name.lower().replace(' ', '_')}_v{vol_num:02d}"
            tab_name = f"Vol {vol_num}: {slug}"
            subtitle = job["subtitle_fmt"]

            interior_path = os.path.join(book_dir, "interior_6x9.pdf")
            cover_path = os.path.join(book_dir, "cover_wrap_6x9.pdf")
            front_img_path = os.path.join(book_dir, "cover_front_preview.png")
            meta_path = os.path.join(book_dir, "KDP_Listing_Metadata.txt")

            t0 = time.time()
            themes = job["theme_func"](vol_num)

            # 1. Build 176-Page Interior PDF
            build_interlocking_book(
                series_name=s_name,
                vol_num=vol_num,
                book_title=title,
                subtitle=subtitle,
                themes=themes,
                out_dir=book_dir,
                accent_hex=accent_hex,
                cover_theme=cover_theme
            )

            # 2. Build Bespoke Luxury Wrap Cover PDF
            book_meta_dummy = {
                "series": s_name,
                "vol_number": vol_num,
                "title": title,
                "accent_hex": accent_hex
            }
            generate_luxury_cover(book_meta_dummy, cover_path)

            # 3. Render High-Resolution PNG Previews
            render_cover_previews(cover_path, book_dir)

            # 4. Generate KDP Listing Metadata Text
            meta_content = f"""================================================================================
KDP LISTING METADATA: {s_name.upper()} - VOLUME {vol_num}
================================================================================

[BOOK DETAILS]
Title: {s_name}: {title} (Volume {vol_num})
Subtitle: {subtitle}
Series Title: {s_name}
Series Number: {vol_num}
Edition: 1
Author: (Independent Publisher / Special Investigator)

[PRINT SPECIFICATIONS]
Interior & Paper Type: Black & white interior with white paper
Trim Size: 6 x 9 in
Bleed Settings: No Bleed
Paperback Cover Finish: Matte
Page Count: 176 pages
Spine Width: 0.396 in (10.06 mm)

[CATEGORIES (Choose 3)]
1. {job['category_base'][0]}
2. {job['category_base'][1]}
3. {job['category_base'][2]}

[7 BACKEND SEARCH KEYWORDS]
1. {job['keywords'][0]}
2. {job['keywords'][1]}
3. {job['keywords'][2]}
4. {job['keywords'][3]}
5. {job['keywords'][4]}
6. {job['keywords'][5]}
7. {job['keywords'][6]}

[PRICING & ROYALTY (US MARKET)]
List Price: $12.99 USD
Printing Cost: $3.11 USD
Estimated Royalty (60%): $4.68 USD per copy sold
"""
            with open(meta_path, "w", encoding="utf-8") as f_meta:
                f_meta.write(meta_content)

            # 5. Build Description HTML
            desc_html = f"""<h2>{job['desc_headline']}</h2>
<p>Welcome to <b>{title} (Volume {vol_num})</b>, an enhanced interactive crime-solving experience engineered for true mystery buffs, logic enthusiasts, and armchair detectives.</p>
<p>Unlike ordinary puzzle books that repeat the same isolated grids, every single investigation in this volume is an authentic <b>4-stage interlocking crime file</b>:</p>
<ul>
  <li><b>Stage 1: Forensic Sudoku:</b> Solve the 9x9 grid to unmask the 4 shaded Key Cells (Alpha, Beta, Gamma, Delta).</li>
  <li><b>Stage 2: Passkey-Shifted Cipher:</b> Sum the extracted digits to decrypt the victim's coded dying dispatch.</li>
  <li><b>Stage 3: Alibi Logic Grid:</b> Use the decrypted clue as elimination proof on the 4x4 deduction matrix (100% mathematically proven unique solution).</li>
  <li><b>Stage 4: Official State Arrest Warrant:</b> Name the perpetrator, certify the weapon, and secure the indictment!</li>
</ul>
<p><b>Gather your pencils, inspect the evidence, and crack the mystery today!</b></p>"""

            # 6. Assemble Catalog Entry
            rel_interior_pdf = f"{folder_base}/{vol_folder_name}/interior_6x9.pdf"
            rel_cover_pdf = f"{folder_base}/{vol_folder_name}/cover_wrap_6x9.pdf"
            rel_front_img = f"{folder_base}/{vol_folder_name}/cover_front_preview.png"
            rel_wrap_img = f"{folder_base}/{vol_folder_name}/cover_wrap_preview.png"

            entry = {
                "id": book_id,
                "vol_number": vol_num,
                "tab_name": tab_name,
                "title": title,
                "subtitle": subtitle,
                "series": s_name,
                "price_usd": 12.99,
                "print_cost_usd": 3.11,
                "royalty_usd": 4.68,
                "trim": "6 x 9 in",
                "pages": 176,
                "bleed": "No Bleed",
                "cover_palette": cover_theme,
                "keywords": job["keywords"],
                "categories": job["category_base"],
                "description_html": desc_html,
                "pdf_interior_url": rel_interior_pdf,
                "pdf_cover_url": rel_cover_pdf,
                "cover_img_url": rel_front_img,
                "cover_wrap_img_url": rel_wrap_img,
                "accent_hex": accent_hex
            }

            if book_id in existing_ids:
                # Update existing
                idx_found = next(i for i, b in enumerate(catalog) if b.get("id") == book_id)
                catalog[idx_found] = entry
            else:
                catalog.append(entry)
                new_books_added += 1

            dt = round(time.time() - t0, 2)
            print(f"  [✓] Vol {vol_num:02d}: {title} compiled in {dt}s")

    # Save updated catalog
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    total_time = round(time.time() - t_start, 2)
    print("\n" + "=" * 80)
    print(f"   PIPELINE COMPLETE IN {total_time}s!")
    print(f"   Added {new_books_added} new volumes. Total catalog size: {len(catalog)} books.")
    print("=" * 80)

if __name__ == "__main__":
    run()
