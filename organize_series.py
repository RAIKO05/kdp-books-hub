"""
organize_series.py
Creates a structured, production-ready directory for the book series:
The_Detectives_Case_Files_Series/
  ├── Volume_1_Blackwood_Files/
  │     ├── interior_6x9.pdf
  │     ├── cover_wrap_6x9.pdf
  │     ├── multigame_cases.json
  │     └── KDP_Listing_Metadata.txt
  └── Volume_2_Royal_Airship_Enigma/
        ├── interior_6x9.pdf
        ├── cover_wrap_6x9.pdf
        ├── multigame_cases.json
        └── KDP_Listing_Metadata.txt
"""

import os
import shutil

BASE_DIR = "The_Detectives_Case_Files_Series"
VOL1_DIR = os.path.join(BASE_DIR, "Volume_1_Blackwood_Files")
VOL2_DIR = os.path.join(BASE_DIR, "Volume_2_Royal_Airship_Enigma")

os.makedirs(VOL1_DIR, exist_ok=True)
os.makedirs(VOL2_DIR, exist_ok=True)

# Copy Volume 1 Files
shutil.copy2("interior_6x9.pdf", os.path.join(VOL1_DIR, "interior_6x9.pdf"))
shutil.copy2("cover_wrap_6x9.pdf", os.path.join(VOL1_DIR, "cover_wrap_6x9.pdf"))
shutil.copy2("multigame_cases.json", os.path.join(VOL1_DIR, "multigame_cases.json"))

# Copy Volume 2 Files
shutil.copy2("interior_vol2_6x9.pdf", os.path.join(VOL2_DIR, "interior_6x9.pdf"))
shutil.copy2("cover_wrap_vol2_6x9.pdf", os.path.join(VOL2_DIR, "cover_wrap_6x9.pdf"))
shutil.copy2("multigame_cases_vol2.json", os.path.join(VOL2_DIR, "multigame_cases.json"))

# Volume 1 Metadata
vol1_meta = """================================================================================
KDP LISTING METADATA: THE DETECTIVE'S CASE FILES • VOLUME 1
================================================================================

[BOOK TITLE]: Case Files & Clues: Volume 1
[SUBTITLE]: 35 Multi-Game Murder Mystery Dossiers for Adults: Logic Grids, Ciphers, Forensic Sweeps & Arrest Warrants
[SERIES NAME]: The Detective's Case Files
[SERIES NUMBER]: 1
[AUTHOR NAME]: Enter your preferred pen name or real name (e.g. Mouad Zitouni)

[PRINT SETTINGS]:
- Trim Size: 6" x 9" (15.24 x 22.86 cm)
- Page Count: 176 Pages
- Interior: Black & white interior with white paper
- Bleed Settings: No bleed (for interior)
- Cover Finish: Matte

[PRICING]:
- List Price: $12.99 USD
- KDP Print Cost: $3.11 USD
- Royalty per Sale: $4.68 USD (60% standard distribution)

[CATEGORIES]:
1. Crafts, Hobbies & Home > Crafts & Hobbies > Activity Books
2. Humor & Entertainment > Puzzles & Games > Logic & Brain Teasers
3. Mystery, Thriller & Suspense > Mystery > Traditional Detective

[7 BACKEND KEYWORDS]:
1. murder mystery logic puzzles for adults
2. detective puzzle book crime solving games
3. whodunit logic grid brain teasers
4. forensic investigation case files book
5. cozy mystery mind games for seniors
6. escape room in a book cryptograms
7. crime scene activity book for adults

[BOOK DESCRIPTION (HTML)]:
<h2>Can you outthink the criminal mind?</h2>
<p>Welcome to <b>The Detective's Case Files: Volume 1</b>, an enhanced interactive crime-solving experience engineered for true mystery buffs, logic lovers, and armchair sleuths.</p>
<p>Unlike ordinary puzzle books that repeat the same grid on every page, every investigation in this volume is an immersive <b>4-stage case file</b>:</p>
<ul>
  <li><b>Stage 1: Forensic Evidence Sweep:</b> 10x10 crime scene word search to recover physical evidence.</li>
  <li><b>Stage 2: The Encrypted Dispatch:</b> Decrypt the killer's secret cipher message.</li>
  <li><b>Stage 3: The Alibi & Motive Matrix:</b> Airtight logic deduction grid verified to yield 1 unique solution.</li>
  <li><b>Stage 4: The Official Arrest Warrant:</b> Synthesize your evidence and indict the true perpetrator!</li>
</ul>
<p><b>Sharpen your pencil, assemble the evidence, and crack the case today!</b></p>
"""

with open(os.path.join(VOL1_DIR, "KDP_Listing_Metadata.txt"), "w", encoding="utf-8") as f:
    f.write(vol1_meta)

# Volume 2 Metadata
vol2_meta = """================================================================================
KDP LISTING METADATA: THE DETECTIVE'S CASE FILES • VOLUME 2
================================================================================

[BOOK TITLE]: Case Files & Clues: Volume 2
[SUBTITLE]: 35 All-New Multi-Game Murder Mystery Dossiers: Airships, Grand Operas, Botanical Gardens & Ancient Tombs
[SERIES NAME]: The Detective's Case Files
[SERIES NUMBER]: 2
[AUTHOR NAME]: Same author name used in Volume 1

[PRINT SETTINGS]:
- Trim Size: 6" x 9" (15.24 x 22.86 cm)
- Page Count: 176 Pages
- Interior: Black & white interior with white paper
- Bleed Settings: No bleed (for interior)
- Cover Finish: Matte

[PRICING]:
- List Price: $12.99 USD
- KDP Print Cost: $3.11 USD
- Royalty per Sale: $4.68 USD (60% standard distribution)

[CATEGORIES]:
1. Crafts, Hobbies & Home > Crafts & Hobbies > Activity Books
2. Humor & Entertainment > Puzzles & Games > Logic & Brain Teasers
3. Mystery, Thriller & Suspense > Mystery > Traditional Detective

[7 BACKEND KEYWORDS]:
1. adult murder mystery game in a book
2. 1920s detective logic puzzle book
3. airship and opera house crime dossiers
4. escape room activity book cryptograms
5. forensic investigation grid puzzles
6. deductive reasoning mystery games
7. cold case files activity book for adults

[BOOK DESCRIPTION (HTML)]:
<h2>The investigation continues...</h2>
<p>Welcome back, Inspector! <b>The Detective's Case Files: Volume 2</b> presents 35 all-new high-stakes investigations spanning transatlantic zeppelins, backstage opera murders, venomous botanical conservatories, and ancient Egyptian archaeological digs.</p>
<p>Every case is an authentic <b>4-stage crime file</b>:</p>
<ul>
  <li><b>Stage 1: Forensic Evidence Sweep:</b> Scour the crime scene matrix for physical clues.</li>
  <li><b>Stage 2: The Encrypted Dispatch:</b> Crack the suspect's coded message to reveal crucial testimony.</li>
  <li><b>Stage 3: The Alibi Matrix:</b> Pure logic deduction grid mathematically proven to have 1 unique solution.</li>
  <li><b>Stage 4: The Official Arrest Warrant:</b> Close the case and convict the true culprit!</li>
</ul>
<p><b>Continue your detective career—claim Volume 2 today!</b></p>
"""

with open(os.path.join(VOL2_DIR, "KDP_Listing_Metadata.txt"), "w", encoding="utf-8") as f:
    f.write(vol2_meta)

print("Successfully created master series directory structure!")
