"""
run_batch_publisher.py
Executes batch publication of flagship books using the industrial interlocking engine:
1. Project X (Volume 2: The Sub-Terra Core)
2. The Ravencrest Chronicles (Volume 1: The Blackwood Curse)
"""

import os
import json
from industrial_book_engine import build_interlocking_book

def run_batch():
    print("=" * 70)
    print("   INDUSTRIAL BATCH BOOK ENGINE: ADVANCED INTERLOCKING MIND GAMES")
    print("=" * 70)

    # --- BOOK 1: PROJECT X (VOLUME 2: THE SUB-TERRA CORE) ---
    px_themes = [
        {
            "id": "magma_shaft",
            "name": "The Magma Thermal Shaft",
            "suspects": [
                {"name": "Dr. Tariq Malik", "role": "Senior Geochemist"},
                {"name": "Operations Lead Keller", "role": "Shift Foreman"},
                {"name": "Security Chief Ward", "role": "Mercenary Guard"},
                {"name": "Reactor Tech Silas", "role": "Core Operator"},
                {"name": "Android Unit-07", "role": "Synthetic Overseer"},
                {"name": "Corporate Auditor Stone", "role": "Company Fixer"}
            ],
            "rooms": [
                "Magma Thermal Bypass", "Heavy Smelting Foundry", "Sub-Surface Drill Shaft",
                "Tool Storage Lockout", "Pressurized Ore Hauler", "Coolant Storage Tank"
            ],
            "weapons": [
                "Industrial Laser Cutter", "Heavy Pneumatic Drill", "Magma Exhaust Flush",
                "Steel Hoist Cable", "Seismic Charge Blaster", "Silicon Coolant Spray"
            ],
            "cipher_clues": [
                "THE SEISMIC CHARGE WAS DETONATED DELIBERATELY",
                "AUDITOR STONE ORDERED THE ORE SHIPMENT PURGED",
                "THORNE DISCOVERED THE TAMPERED HYDRAULIC LINE",
                "THE DRILL SHAFT LOCKOUT WAS OVERRIDDEN AT MIDNIGHT"
            ]
        },
        {
            "id": "quantum_core",
            "name": "The Quantum Supercomputer Core",
            "suspects": [
                {"name": "Director Vance", "role": "Corporate Executive"},
                {"name": "Flight Officer Mercer", "role": "Orbital Pilot"},
                {"name": "Android Unit-07", "role": "Synthetic Overseer"},
                {"name": "Dr. Elena Chen", "role": "Chief Whistleblower"},
                {"name": "Reactor Tech Silas", "role": "Core Operator"},
                {"name": "Security Chief Ward", "role": "Mercenary Guard"}
            ],
            "rooms": [
                "Quantum Server Chamber", "Sub-Zero Coolant Ring", "Neural Uplink Suite",
                "Emergency Memory Dump", "Fiber Optic Catwalk", "Main Terminal Bridge"
            ],
            "weapons": [
                "Supercooled Nitrogen Flush", "High-Voltage EMP Discharge", "Ceramic Stun Scalpel",
                "Severed Bus Cable", "Synthetic Neuro-Dart", "Crushed Silicon Processor"
            ],
            "cipher_clues": [
                "THE NEURAL UPLINK LOGS WERE DELETED AT 0300",
                "DIRECTOR VANCE AUTHORIZED THE MAINFRAME OVERHEAT",
                "UNIT ZERO SEVEN STORED THE EVIDENCE ON DRIVES",
                "THE COOLANT LINE WAS CUT WITH A CERAMIC BLADE"
            ]
        },
        {
            "id": "deep_borehole",
            "name": "The Deep Borehole Extraction Site",
            "suspects": [
                {"name": "Chief Engineer Thorne", "role": "Framed Mechanic"},
                {"name": "Technician Cole", "role": "Maintenance Diver"},
                {"name": "Corporate Auditor Stone", "role": "Company Fixer"},
                {"name": "Dr. Tariq Malik", "role": "Senior Geochemist"},
                {"name": "Operations Lead Keller", "role": "Shift Foreman"},
                {"name": "Security Chief Ward", "role": "Mercenary Guard"}
            ],
            "rooms": [
                "Borehole Pressure Sump", "Specimen Sorting Bay", "Ore Conveyor Lift",
                "Hydraulic Power Vault", "Sub-Surface Habitat B", "Aerosol Exhaust Vent"
            ],
            "weapons": [
                "Tungsten Core Drill Bit", "High-Pressure Hydraulic Ram", "Argon Venting Valve",
                "Heavy Steel Wrench", "Mining Blaster Detonator", "Carbon Composite Cable"
            ],
            "cipher_clues": [
                "THE BOREHOLE EXTRACTION WAS STRICTLY ILLEGAL",
                "THE TOXIC GAS WAS VENTED INTO HABITAT B",
                "STONE PLANTED THE DETONATOR IN THE POWER VAULT",
                "THE CONVEYOR LIFT WAS STOPPED TO TRAP THE CREW"
            ]
        },
        {
            "id": "command_bunker",
            "name": "The Sub-Surface Command Bunker",
            "suspects": [
                {"name": "Director Vance", "role": "Corporate Executive"},
                {"name": "Flight Officer Mercer", "role": "Orbital Pilot"},
                {"name": "Security Chief Ward", "role": "Mercenary Guard"},
                {"name": "Android Unit-07", "role": "Synthetic Overseer"},
                {"name": "Chief Engineer Thorne", "role": "Framed Mechanic"},
                {"name": "Dr. Elena Chen", "role": "Chief Whistleblower"}
            ],
            "rooms": [
                "Executive War Room", "Sub-Surface Comms Array", "Emergency Bunkers Vault",
                "Security Armory Cell", "Life Support Scrubber", "Airlock Primary Beta"
            ],
            "weapons": [
                "Electromagnetic Pistol", "Cyanide Capsule Infusion", "Airlock Decompress Switch",
                "Heavy Titanium Riot Club", "Thermal Laser Solder", "Severed Scrubber Fuse"
            ],
            "cipher_clues": [
                "THE AIRLOCK PURGE WAS INITIATED FROM WAR ROOM",
                "MERCER TOOK THE PAYMENT IN UNTRACEABLE CREDITS",
                "THE LIFE SUPPORT FUSE WAS PULLED DELIBERATELY",
                "THE ARMORY SURVEILLANCE FEED WAS DISCONNECTED"
            ]
        }
    ]

    out_px_v2 = os.path.join("Project_X", "Volume_2_The_Sub_Terra_Core")
    print("\n[*] Compiling Project X: Volume 2 (The Sub-Terra Core)...")
    build_interlocking_book(
        series_name="Project X",
        vol_num=2,
        book_title="The Sub-Terra Core",
        subtitle="35 Interlocking Sci-Fi Murder Mystery Logic Puzzles & Sudoku Key Solvers",
        themes=px_themes,
        out_dir=out_px_v2,
        accent_hex="#FCA311", # Neon Amber
        cover_theme="Cosmic Obsidian & Neon Amber"
    )

    # --- BOOK 2: THE RAVENCREST CHRONICLES (VOLUME 1: THE BLACKWOOD CURSE) ---
    rc_themes = [
        {
            "id": "ancestral_crypt",
            "name": "The Ancestral Crypt & Catacombs",
            "suspects": [
                {"name": "Lord Alistair Ravencrest", "role": "The Wealthy Patriarch"},
                {"name": "Madame Vane", "role": "The Cursed Medium"},
                {"name": "Butler Graves", "role": "The Somber Servant"},
                {"name": "Dr. Lucian Blackwood", "role": "The Sinister Physician"},
                {"name": "Clara Ravencrest", "role": "The Disinherited Niece"},
                {"name": "Archivist Thorne", "role": "The Crypt Historian"}
            ],
            "rooms": [
                "The Vault of Sarcophagi", "The Subterranean Ossuary", "The Family Mausoleum",
                "The Secret Catacomb Hall", "The Torched Chapel", "The Stone Reliquary"
            ],
            "weapons": [
                "Antique Silver Dagger", "Belladonna Laudanum", "Heavy Iron Candelabra",
                "Velvet Shroud Cord", "Poisoned Signet Ring", "Obsidian Ritual Blade"
            ],
            "cipher_clues": [
                "THE COFFIN WAS FORCED OPEN BEFORE MIDNIGHT",
                "MADAME VANE HID THE WILL IN THE OSSUARY",
                "THE BELLADONNA WAS POURED IN THE SACRAMENTAL WINE",
                "LORD ALISTAIR CONCEALED THE ANCIENT PARCHMENT"
            ]
        },
        {
            "id": "grand_library",
            "name": "The Ravencrest Grand Library",
            "suspects": [
                {"name": "Archivist Thorne", "role": "The Crypt Historian"},
                {"name": "Dr. Lucian Blackwood", "role": "The Sinister Physician"},
                {"name": "Clara Ravencrest", "role": "The Disinherited Niece"},
                {"name": "Lord Alistair Ravencrest", "role": "The Wealthy Patriarch"},
                {"name": "Butler Graves", "role": "The Somber Servant"},
                {"name": "Madame Vane", "role": "The Cursed Medium"}
            ],
            "rooms": [
                "The Occult Rare Book Vault", "The Spiral Gallery", "The Fireplace Study",
                "The Clockwork Globe Alcove", "The Conservatory Conservatory", "The Secret Bookcase Pass"
            ],
            "weapons": [
                "Wrought Iron Fire Poker", "Arsenic Ink Infusion", "Gilded Bookbinder Vice",
                "Heavy Brass Astrolabe", "Silk Dressing Cord", "Carved Bone Dagger"
            ],
            "cipher_clues": [
                "THE RARE OCCULT GRIMOIRE HAS BEEN STOLEN",
                "DR BLACKWOOD APPLIED THE ARSENIC TO THE PAGES",
                "THE FIRE POKER WAS RETRIEVED FROM THE STUDY",
                "CLARA ACCUSED HER UNCLE IN THE GALLERY"
            ]
        },
        {
            "id": "ruined_bell_tower",
            "name": "The Ruined Bell Tower & Cloister",
            "suspects": [
                {"name": "Butler Graves", "role": "The Somber Servant"},
                {"name": "Madame Vane", "role": "The Cursed Medium"},
                {"name": "Dr. Lucian Blackwood", "role": "The Sinister Physician"},
                {"name": "Archivist Thorne", "role": "The Crypt Historian"},
                {"name": "Clara Ravencrest", "role": "The Disinherited Niece"},
                {"name": "Lord Alistair Ravencrest", "role": "The Wealthy Patriarch"}
            ],
            "rooms": [
                "The Bell Belfry Loft", "The Storm Gutter Catwalk", "The Gargoyle Parapet",
                "The Overgrown Cloister", "The Abandoned Scullery", "The Tower Cellar Gate"
            ],
            "weapons": [
                "Weighted Bell Chime Rope", "Strychnine Brandy Flask", "Corroded Iron Spike",
                "Heavy Bronze Bell Clapper", "Cobblestone Mason Hammer", "Grave Digger Spade"
            ],
            "cipher_clues": [
                "THE VICTIM FELL FROM THE GARGOYLE PARAPET",
                "GRAVES WASHED THE BLOOD FROM THE BRONZE CLAPPER",
                "THE STRICHTNINE FLASK WAS BURIED IN CLOISTER",
                "MADAME VANE HELD A SEANCE IN THE BELFRY"
            ]
        },
        {
            "id": "apothecary_lab",
            "name": "The Victorian Apothecary Laboratory",
            "suspects": [
                {"name": "Dr. Lucian Blackwood", "role": "The Sinister Physician"},
                {"name": "Clara Ravencrest", "role": "The Disinherited Niece"},
                {"name": "Lord Alistair Ravencrest", "role": "The Wealthy Patriarch"},
                {"name": "Archivist Thorne", "role": "The Crypt Historian"},
                {"name": "Madame Vane", "role": "The Cursed Medium"},
                {"name": "Butler Graves", "role": "The Somber Servant"}
            ],
            "rooms": [
                "The Toxic Mortar Bench", "The Herb Drying Chamber", "The Leech Glass Aquarium",
                "The Distillation Furnace", "The Darkroom Chemical Bath", "The Cold Storage Cellar"
            ],
            "weapons": [
                "Cyanide Tincture Dropper", "Heavy Stone Mortar Pestle", "Silver Amputation Scalpel",
                "Chloroform Soaked Linen", "Serrated Botanical Shear", "Glass Acid Carboy"
            ],
            "cipher_clues": [
                "THE CYANIDE TINCTURE WAS EMPTIED IN CELLAR",
                "THE DOCTOR EXPERIMENTED WITH LETHAL SPORES",
                "CLARA ENTERED THE DISTILLATION ROOM AT DUSK",
                "THE SCALPEL WAS FOUND IN THE DRYING CHAMBER"
            ]
        }
    ]

    out_rc_v1 = os.path.join("The_Ravencrest_Chronicles", "Volume_1_The_Blackwood_Curse")
    print("\n[*] Compiling The Ravencrest Chronicles: Volume 1 (The Blackwood Curse)...")
    build_interlocking_book(
        series_name="The Ravencrest Chronicles",
        vol_num=1,
        book_title="The Blackwood Curse",
        subtitle="35 Gothic Murder Mystery Dossiers: Sudoku Keys, Ciphers & Deduction Grids",
        themes=rc_themes,
        out_dir=out_rc_v1,
        accent_hex="#9D4EDD", # Gothic Amethyst Purple
        cover_theme="Midnight Gothic Obsidian & Amethyst Purple"
    )

    # --- UPDATE CATALOG.JSON ---
    cat_path = os.path.join("The_Detectives_Case_Files_Series", "catalog.json")
    with open(cat_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    # Check and append Book 1: Project X Vol 2
    if not any(b.get("id") == "px_vol2" for b in catalog):
        catalog.append({
            "id": "px_vol2",
            "vol_number": 2,
            "tab_name": "Vol 2: Sub-Terra Core",
            "title": "Project X: The Sub-Terra Core",
            "subtitle": "35 Interlocking Sci-Fi Murder Mystery Logic Puzzles & Sudoku Key Solvers",
            "series": "Project X",
            "price_usd": "12.99",
            "print_cost_usd": "3.11",
            "royalty_usd": "4.68",
            "trim": '6" x 9"',
            "pages": 176,
            "bleed": "No Bleed",
            "cover_palette": "Cosmic Obsidian & Neon Amber",
            "keywords": [
                "interlocking sudoku logic puzzle book",
                "sci fi murder mystery mind games for adults",
                "space station corporate sabotage logic grid",
                "challenging hard logic puzzle book",
                "forensic crime escape room in a book",
                "adult brain teasers cryptograms",
                "cyberpunk detective mystery book"
            ],
            "categories": [
                "Humor & Entertainment > Puzzles & Games > Logic & Brain Teasers",
                "Science Fiction & Fantasy > Science Fiction > Space Exploration",
                "Crafts, Hobbies & Home > Crafts & Hobbies > Activity Books"
            ],
            "description_html": "<h2>Can you unlock the Sub-Terra Core before emergency oxygen expires?</h2>\n<p>Welcome to <b>Project X: Volume 2 - The Sub-Terra Core</b>, the next-generation interactive sci-fi deduction experience built with the revolutionary <b>Interlocking Evidence Key System</b>.</p>\n<p>Unlike repetitive puzzle books, every single investigation in this volume is a connected chain of forensic deduction:</p>\n<ul>\n  <li><b>Stage 1: Forensic Sudoku:</b> Solve the 9x9 grid to unmask the 4 shaded Key Cells.</li>\n  <li><b>Stage 2: Passkey-Shifted Cipher:</b> Use the extracted 4-digit code to decode the saboteur's dying transmission.</li>\n  <li><b>Stage 3: Alibi Logic Grid:</b> Use the decrypted message as proof to eliminate innocent crew on the deduction matrix.</li>\n  <li><b>Stage 4: State Arrest Warrant:</b> Indict the true corporate saboteur and convict the culprit!</li>\n</ul>\n<p><b>100% mathematically verified unique solutions. Claim Volume 2 today!</b></p>"
        })

    # Check and append Book 2: Ravencrest Chronicles Vol 1
    if not any(b.get("id") == "rc_vol1" for b in catalog):
        catalog.append({
            "id": "rc_vol1",
            "vol_number": 1,
            "tab_name": "Vol 1: Blackwood Curse",
            "title": "The Ravencrest Chronicles: The Blackwood Curse",
            "subtitle": "35 Gothic Murder Mystery Dossiers: Sudoku Keys, Ciphers & Deduction Grids",
            "series": "The Ravencrest Chronicles",
            "price_usd": "12.99",
            "print_cost_usd": "3.11",
            "royalty_usd": "4.68",
            "trim": '6" x 9"',
            "pages": 176,
            "bleed": "No Bleed",
            "cover_palette": "Midnight Gothic & Amethyst Purple",
            "keywords": [
                "gothic murder mystery puzzle book for adults",
                "sudoku escape room in a book whodunit",
                "victorian haunted manor logic grid puzzles",
                "dark academia deduction mystery book",
                "interlocking evidence key puzzle book",
                "cozy horror mind games for adults",
                "crime scene cold case files activity book"
            ],
            "categories": [
                "Humor & Entertainment > Puzzles & Games > Logic & Brain Teasers",
                "Mystery, Thriller & Suspense > Mystery > Hard-Boiled / Traditional Detective",
                "Crafts, Hobbies & Home > Crafts & Hobbies > Activity Books"
            ],
            "description_html": "<h2>Dark secrets lurk within the Ravencrest catacombs...</h2>\n<p>Welcome to <b>The Ravencrest Chronicles: Volume 1 - The Blackwood Curse</b>, an atmospheric gothic whodunit experience designed for true mystery lovers and serious puzzle solvers.</p>\n<p>Every case is an authentic <b>4-stage interlocking investigation</b>:</p>\n<ul>\n  <li><b>Stage 1: Forensic Sudoku:</b> Solve the grid to extract the 4 sacred Key Cells from the ancestral crypt.</li>\n  <li><b>Stage 2: Cryptic Cipher:</b> Decrypt the medium's intercepted seance message using the Sudoku key sum.</li>\n  <li><b>Stage 3: Alibi Deduction Matrix:</b> Pure logic grid mathematically proven to have 1 unique solution.</li>\n  <li><b>Stage 4: State Arrest Warrant:</b> Name the killer, expose the poisoned inheritance, and close the case!</li>\n</ul>\n<p><b>Step into the shadows of Ravencrest Manor—claim your dossier today!</b></p>"
        })

    with open(cat_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    print("\n[✓] Updated catalog.json with 2 brand new flagship books!")

if __name__ == "__main__":
    run_batch()
