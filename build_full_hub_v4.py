"""
build_full_hub_v4.py
Compiles the Master KDP Books Hub (v4.0) with:
1. 100-Book Catalog & High-Res 3D Cover Showcases
2. 1-Click Fast Publisher Stepper for Amazon KDP
3. KDP Publishing Status Tracker (Live / In Review / Unpublished) & ASIN Linker
4. Progress Dashboard & Filter Bar
5. Interactive Case #001 Playable Solver (Sudoku, Cipher, Logic Grid, Arrest Warrant)
6. Live Amazon Royalty & Revenue Projection Calculator
7. 1-Click Social Media & Video Script Generator (TikTok, Instagram, Reddit)
8. Amazon A+ Content Showcase Drawer (All 7 Series)
9. Native iOS IPA & Production ZIPs Downloads
10. Full Offline PWA Service Worker Integration
"""

import json
import os

with open('catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

SERIES_APLUS_MAP = {
    "The Detective's Case Files": "Amazon_A_Plus_Content/01_The_Detectives_Case_Files",
    "Project X": "Amazon_A_Plus_Content/02_Project_X",
    "The Ravencrest Chronicles": "Amazon_A_Plus_Content/03_The_Ravencrest_Chronicles",
    "The Bletchley Protocols": "Amazon_A_Plus_Content/04_The_Bletchley_Protocols",
    "Crypt of the Pharaohs": "Amazon_A_Plus_Content/05_Crypt_of_the_Pharaohs",
    "The Blackwood Asylum Files": "Amazon_A_Plus_Content/06_The_Blackwood_Asylum_Files",
    "The Grand Orient Express": "Amazon_A_Plus_Content/07_The_Grand_Orient_Express",
    "The Lupin Heists": "Amazon_A_Plus_Content/08_The_Lupin_Heists",
    "The Machine Protocols": "Amazon_A_Plus_Content/09_The_Machine_Protocols"
}

# Case 1 Interactive Solver Data
CASE_1_DATA = {
    "title": "Case #001: The Mystery of Library Gallery",
    "series": "The Detective's Case Files",
    "briefing": "Lord Harrington was discovered poisoned in the private Library Gallery of Blackwood Manor. The local constabulary has locked the estate grounds. Four suspects were observed fleeing the west wing. Can you recover the physical evidence, decode the dying cipher, dismantle the suspects' alibis, and sign the official arrest warrant?",
    "sudoku": {
        "puzzle": [
            [5, 3, 0, 0, 7, 0, 2, 4, 0],
            [0, 0, 0, 0, 4, 6, 0, 0, 9],
            [6, 0, 0, 0, 0, 2, 0, 8, 1],
            [1, 0, 0, 0, 0, 0, 0, 9, 0],
            [0, 9, 6, 0, 0, 0, 1, 2, 0],
            [7, 0, 5, 0, 0, 0, 4, 0, 3],
            [0, 0, 0, 8, 1, 4, 6, 0, 0],
            [4, 6, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 9, 5, 4]
        ],
        "solution": [
            [5, 3, 9, 1, 7, 8, 2, 4, 6],
            [2, 1, 8, 5, 4, 6, 7, 3, 9],
            [6, 4, 7, 3, 9, 2, 5, 8, 1],
            [1, 2, 4, 6, 3, 7, 8, 9, 5],
            [3, 9, 6, 4, 8, 5, 1, 2, 7],
            [7, 8, 5, 9, 2, 1, 4, 6, 3],
            [9, 5, 3, 8, 1, 4, 6, 7, 2],
            [4, 6, 2, 7, 5, 9, 3, 1, 8],
            [8, 7, 1, 2, 6, 3, 9, 5, 4]
        ],
        "key_cells": [
            {"label": "ALPHA", "r": 8, "c": 1, "digit": 7},
            {"label": "BETA", "r": 3, "c": 8, "digit": 5},
            {"label": "GAMMA", "r": 7, "c": 5, "digit": 9},
            {"label": "DELTA", "r": 4, "c": 4, "digit": 8}
        ],
        "key_code": "7598",
        "key_sum": 29,
        "shift": 3
    },
    "cipher": {
        "ciphertext": "WKH ZHDSRQ ZDV UHWULHYHG IURP WKH FULPH VFHQH DW WZLOLJKW (FDVH 7)",
        "plaintext": "THE WEAPON WAS RETRIEVED FROM THE CRIME SCENE AT TWILIGHT (CASE 7)",
        "shift": 3
    },
    "logic_grid": {
        "suspects": ["Lord Harrington", "Lady Beatrice", "Inspector Finch", "The Governess"],
        "rooms": ["Wine Cellar", "Billiard Room", "Library Gallery", "Study"],
        "weapons": ["Silken Dressing Cord", "Poisoned Snuffbox", "Heavy Brass Candlestick", "Ornate Letter Opener"],
        "clues": [
            "1. Lady Beatrice was confirmed to be in the Billiard Room.",
            "2. Inspector Finch was discovered carrying the Poisoned Snuffbox.",
            "3. The investigator found the Silken Dressing Cord inside the Study.",
            "4. Lord Harrington was never seen near the Wine Cellar.",
            "5. Lord Harrington had no access to the Silken Dressing Cord.",
            "6. The weapon recovered from the Billiard Room was definitely not the Poisoned Snuffbox.",
            "7. Neither Lord Harrington nor The Governess had ever visited the Billiard Room.",
            "8. The lethal strike occurred in the Library Gallery, leaving behind the Heavy Brass Candlestick."
        ]
    },
    "warrant_solution": {
        "culprit": "Lord Harrington",
        "room": "Library Gallery",
        "weapon": "Heavy Brass Candlestick"
    }
}

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>KDP Books Hub - 100-Book Catalog & Publishing Command Center</title>
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="KDP Hub">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
  <link rel="manifest" href="manifest.json">
  <style>
    :root {{
      --bg: #0D1117;
      --card-bg: #161B22;
      --border: #30363D;
      --accent: #E3B341;
      --accent-green: #2EA043;
      --accent-blue: #58A6FF;
      --accent-purple: #BC8CFF;
      --text: #F0F6FC;
      --text-muted: #8B949E;
      --danger: #F85149;
    }}
    * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
    body {{
      margin: 0;
      padding: 16px;
      padding-top: max(16px, env(safe-area-inset-top));
      padding-bottom: max(80px, env(safe-area-inset-bottom));
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .header-left {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .app-logo {{
      width: 40px;
      height: 40px;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.6);
      display: block;
    }}
    h1 {{
      font-size: 19px;
      margin: 0;
      color: var(--accent);
      letter-spacing: 0.5px;
      font-weight: 800;
    }}
    .header-actions {{
      display: flex;
      gap: 6px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .btn-header {{
      display: flex;
      align-items: center;
      gap: 5px;
      font-size: 11px;
      font-weight: 700;
      color: #FFF;
      background: #21262D;
      border: 1px solid var(--border);
      padding: 6px 10px;
      border-radius: 10px;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.15s ease;
    }}
    .btn-header:active {{
      transform: scale(0.97);
    }}
    .btn-pack {{
      background: linear-gradient(135deg, #1F6FEB, #238636);
      border-color: rgba(255, 255, 255, 0.15);
    }}
    .btn-game {{
      background: linear-gradient(135deg, #E3B341, #D90429);
      color: #000;
      border-color: #E3B341;
      font-weight: 800;
    }}
    .btn-calc {{
      background: rgba(46, 160, 67, 0.2);
      border-color: #2EA043;
      color: #3FB950;
    }}
    .cloud-status {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 600;
      color: var(--accent-blue);
      background: rgba(88, 166, 255, 0.12);
      padding: 6px 10px;
      border-radius: 10px;
      border: 1px solid rgba(88, 166, 255, 0.25);
      cursor: pointer;
    }}
    .cloud-dot {{
      width: 7px;
      height: 7px;
      background: var(--accent-green);
      border-radius: 50%;
      box-shadow: 0 0 6px var(--accent-green);
    }}

    /* Progress Banner */
    .progress-card {{
      background: #161B22;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 10px 14px;
      margin-bottom: 12px;
    }}
    .progress-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      margin-bottom: 6px;
    }}
    .progress-bar-bg {{
      width: 100%;
      height: 8px;
      background: #21262D;
      border-radius: 4px;
      overflow: hidden;
    }}
    .progress-bar-fill {{
      height: 100%;
      background: linear-gradient(90deg, #2EA043, #3FB950);
      width: 0%;
      transition: width 0.3s ease;
    }}
    .progress-filter-bar {{
      display: flex;
      gap: 6px;
      margin-top: 8px;
      overflow-x: auto;
      scrollbar-width: none;
    }}
    .progress-filter-bar::-webkit-scrollbar {{ display: none; }}
    .filter-chip {{
      font-size: 10px;
      font-weight: 700;
      padding: 4px 8px;
      border-radius: 6px;
      background: #21262D;
      border: 1px solid var(--border);
      color: var(--text-muted);
      cursor: pointer;
      white-space: nowrap;
    }}
    .filter-chip.active {{
      background: var(--accent);
      color: #000;
      border-color: var(--accent);
    }}

    /* Top Toolbar */
    .top-toolbar {{
      display: flex;
      gap: 8px;
      margin-bottom: 12px;
      align-items: center;
    }}
    .search-input {{
      flex: 1;
      background: #161B22;
      border: 1px solid var(--border);
      color: var(--text);
      padding: 9px 14px;
      border-radius: 10px;
      font-size: 13px;
      outline: none;
    }}
    .search-input:focus {{
      border-color: var(--accent);
    }}
    .catalog-badge {{
      font-size: 11px;
      font-weight: 800;
      padding: 8px 12px;
      border-radius: 10px;
      background: #21262D;
      border: 1px solid var(--border);
      color: var(--accent);
      white-space: nowrap;
    }}

    /* Series Pills Bar */
    .series-bar {{
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 8px;
      margin-bottom: 8px;
      scrollbar-width: none;
      -webkit-overflow-scrolling: touch;
    }}
    .series-bar::-webkit-scrollbar {{ display: none; }}
    .series-pill {{
      background: #21262D;
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      white-space: nowrap;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .series-pill.active {{
      background: var(--accent);
      color: #000;
      border-color: var(--accent);
      font-weight: 800;
      box-shadow: 0 2px 8px rgba(227, 179, 65, 0.4);
    }}

    /* Volume Tabs */
    .tab-bar {{
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding-bottom: 10px;
      margin-bottom: 14px;
      scrollbar-width: none;
      -webkit-overflow-scrolling: touch;
    }}
    .tab-bar::-webkit-scrollbar {{ display: none; }}
    .tab-btn {{
      background: #161B22;
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 7px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      white-space: nowrap;
      cursor: pointer;
    }}
    .tab-btn.active {{
      background: #238636;
      color: #FFF;
      border-color: #2EA043;
      font-weight: 700;
    }}

    /* Book Hero Card */
    .cover-showcase-card {{
      background: #161B22;
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 16px;
      margin-bottom: 16px;
      text-align: center;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }}
    .book-3d-wrap {{
      display: inline-block;
      margin: 10px auto 14px auto;
      cursor: pointer;
      perspective: 1000px;
      position: relative;
    }}
    .book-cover-img {{
      width: 175px;
      height: 262px;
      object-fit: cover;
      border-radius: 4px 10px 10px 4px;
      box-shadow: -4px 6px 20px rgba(0,0,0,0.8), 2px 2px 8px rgba(255,255,255,0.08) inset;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      background: #000;
    }}
    .book-cover-img:active {{
      transform: scale(0.98);
    }}
    .cover-tap-hint {{
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 14px;
    }}

    .badge-bar {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 6px;
      margin-bottom: 14px;
    }}
    .badge {{
      font-size: 10px;
      font-weight: 700;
      padding: 4px 9px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .badge-gold {{ background: rgba(227, 179, 65, 0.15); color: #E3B341; border: 1px solid rgba(227, 179, 65, 0.3); }}
    .badge-green {{ background: rgba(46, 160, 67, 0.15); color: #3FB950; border: 1px solid rgba(46, 160, 67, 0.3); }}
    .badge-blue {{ background: rgba(88, 166, 255, 0.15); color: #58A6FF; border: 1px solid rgba(88, 166, 255, 0.3); }}
    .badge-purple {{ background: rgba(188, 140, 255, 0.15); color: #BC8CFF; border: 1px solid rgba(188, 140, 255, 0.3); }}

    /* Status Control Card inside Book */
    .status-card {{
      background: #0D1117;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px 12px;
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .status-badge-wrap {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .status-select {{
      background: #161B22;
      color: #FFF;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 4px 8px;
      font-size: 11px;
      font-weight: 700;
      outline: none;
    }}

    /* Action Grid */
    .action-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 10px;
    }}
    .btn-pdf-interior, .btn-pdf-cover, .btn-quick-read, .btn-aplus-toggle, .btn-promo-toggle {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 12px 10px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 700;
      text-decoration: none;
      border: none;
      cursor: pointer;
      transition: transform 0.1s ease;
    }}
    .btn-pdf-interior {{
      background: #1F6FEB;
      color: #FFF;
      box-shadow: 0 2px 10px rgba(31, 111, 235, 0.4);
    }}
    .btn-pdf-cover {{
      background: #8957E5;
      color: #FFF;
      box-shadow: 0 2px 10px rgba(137, 87, 229, 0.4);
    }}
    .btn-quick-read {{
      width: 100%;
      background: #238636;
      color: #FFF;
      box-shadow: 0 2px 10px rgba(35, 134, 54, 0.4);
      margin-bottom: 8px;
    }}
    .btn-promo-toggle {{
      width: 100%;
      background: linear-gradient(135deg, #FF7B72, #D29922);
      color: #000;
      font-weight: 800;
      box-shadow: 0 2px 10px rgba(255, 123, 114, 0.3);
      margin-bottom: 8px;
    }}
    .btn-aplus-toggle {{
      width: 100%;
      background: linear-gradient(135deg, #D4AF37, #E76F51);
      color: #000;
      font-weight: 800;
      box-shadow: 0 2px 10px rgba(212, 175, 55, 0.4);
    }}

    /* Cards */
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px;
      margin-bottom: 12px;
    }}
    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}
    .label {{
      font-size: 11px;
      text-transform: uppercase;
      font-weight: 800;
      letter-spacing: 0.5px;
      color: var(--text-muted);
    }}
    .copy-btn {{
      background: #21262D;
      border: 1px solid var(--border);
      color: var(--accent-blue);
      font-size: 11px;
      font-weight: 600;
      padding: 4px 9px;
      border-radius: 6px;
      cursor: pointer;
    }}
    .copy-btn:active {{
      background: var(--accent-blue);
      color: #000;
    }}
    .val-box {{
      background: #0D1117;
      border: 1px solid #21262D;
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 13px;
      line-height: 1.5;
      color: var(--text);
      word-break: break-word;
    }}

    .kw-grid {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .kw-item {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #0D1117;
      border: 1px solid #21262D;
      border-radius: 6px;
      padding: 7px 10px;
      font-size: 12px;
    }}

    /* A+ Content Gallery */
    .aplus-drawer {{
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid var(--border);
      display: none;
    }}
    .aplus-drawer.open {{
      display: block;
    }}
    .aplus-preview-item {{
      margin-bottom: 14px;
      background: #0D1117;
      border: 1px solid var(--border);
      border-radius: 10px;
      overflow: hidden;
    }}
    .aplus-preview-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 12px;
      background: #161B22;
      font-size: 11px;
      font-weight: 700;
      color: var(--accent);
    }}
    .aplus-img-tag {{
      width: 100%;
      height: auto;
      display: block;
      cursor: pointer;
    }}
    .aplus-tiles-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      padding: 8px;
    }}
    .aplus-tile-img {{
      width: 100%;
      height: auto;
      border-radius: 6px;
      border: 1px solid var(--border);
      cursor: pointer;
    }}

    /* Modals */
    .reader-modal {{
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.94);
      backdrop-filter: blur(8px);
      z-index: 99999;
      flex-direction: column;
    }}
    .reader-modal.open {{ display: flex; }}
    .reader-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 16px;
      background: #161B22;
      border-bottom: 1px solid var(--border);
    }}
    .reader-title {{
      font-size: 13px;
      font-weight: 700;
      color: var(--accent);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 60%;
    }}
    .reader-actions {{
      display: flex;
      gap: 8px;
    }}
    .reader-close-btn {{
      background: #21262D;
      border: 1px solid var(--border);
      color: #FFF;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 8px;
      cursor: pointer;
    }}
    .reader-body {{
      flex: 1;
      width: 100%;
      height: 100%;
      overflow: auto;
      display: flex;
      justify-content: center;
      align-items: center;
      background: #000;
      -webkit-overflow-scrolling: touch;
    }}
    .reader-iframe {{
      width: 100%;
      height: 100%;
      border: none;
    }}
    .reader-img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
    }}

    /* Toast */
    .toast {{
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%) translateY(100px);
      background: #238636;
      color: #FFF;
      font-size: 12px;
      font-weight: 700;
      padding: 10px 20px;
      border-radius: 20px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.6);
      transition: transform 0.3s ease;
      z-index: 100000;
      pointer-events: none;
    }}
    .toast.show {{
      transform: translateX(-50%) translateY(0);
    }}

    /* Interactive Sudoku Grid */
    .sudoku-board {{
      display: grid;
      grid-template-columns: repeat(9, 1fr);
      gap: 1px;
      background: #30363D;
      border: 2px solid #E3B341;
      border-radius: 6px;
      overflow: hidden;
      max-width: 380px;
      margin: 12px auto;
    }}
    .sudoku-cell {{
      aspect-ratio: 1;
      background: #161B22;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      user-select: none;
    }}
    .sudoku-cell.fixed {{
      color: #F0F6FC;
      background: #0D1117;
    }}
    .sudoku-cell.key-cell {{
      background: rgba(227, 179, 65, 0.25) !important;
      color: #E3B341 !important;
      border: 1px solid #E3B341;
      box-shadow: inset 0 0 6px rgba(227, 179, 65, 0.4);
    }}
    .sudoku-cell.active-cell {{
      outline: 2px solid #58A6FF;
      z-index: 2;
    }}
    .sudoku-numpad {{
      display: flex;
      justify-content: center;
      gap: 6px;
      margin-top: 10px;
      flex-wrap: wrap;
    }}
    .num-btn {{
      width: 34px;
      height: 38px;
      background: #21262D;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #FFF;
      font-weight: 800;
      cursor: pointer;
    }}
    .num-btn:active {{
      background: var(--accent);
      color: #000;
    }}

    /* Logic Matrix */
    .logic-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
      margin: 10px 0;
    }}
    .logic-table th, .logic-table td {{
      border: 1px solid var(--border);
      padding: 6px 4px;
      text-align: center;
    }}
    .logic-table th {{
      background: #161B22;
      color: var(--accent);
      font-weight: 700;
    }}
    .matrix-toggle {{
      cursor: pointer;
      font-weight: 800;
      user-select: none;
    }}

    /* ZIP Items */
    .zip-item {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px;
      background: #0D1117;
      border: 1px solid var(--border);
      border-radius: 10px;
      margin-bottom: 8px;
    }}
    .zip-info {{
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}
    .zip-name {{ font-size: 13px; font-weight: 700; color: var(--text); }}
    .zip-sub {{ font-size: 11px; color: var(--text-muted); }}
    .zip-dl-btn {{
      background: #238636;
      color: #FFF;
      text-decoration: none;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
    }}
  </style>
</head>
<body>

  <header>
    <div class="header-left">
      <img src="logo_header.png" class="app-logo" alt="KDP Hub Logo">
      <div>
        <h1>KDP BOOKS HUB</h1>
        <div style="font-size:11px; color:var(--text-muted);" id="series-subtitle">130 Master Volumes &bull; 9 Flagship Series &bull; Production Ready</div>
      </div>
    </div>
    <div class="header-actions">
      <button class="btn-header btn-game" onclick="openGameModal()">🎮 Play Demo</button>
      <button class="btn-header btn-calc" onclick="openCalcModal()">💰 Calculator</button>
      <button class="btn-header btn-pack" onclick="openZipModal()">📦 Download Hub</button>
      <div class="cloud-status" onclick="refreshFromFirebase()">
        <div class="cloud-dot"></div>
        <span id="cloud-status-text">Cloud Sync (130)</span>
      </div>
    </div>
  </header>

  <!-- KDP PUBLISHING PROGRESS DASHBOARD -->
  <div class="progress-card">
    <div class="progress-header">
      <span style="font-weight:700; color:var(--text);" id="progress-text">📊 KDP Publishing Progress: 0 / 130 Live (0%)</span>
      <span style="font-size:11px; color:var(--accent);" id="projected-royalty-badge">Live Royalties: $0.00/mo</span>
    </div>
    <div class="progress-bar-bg">
      <div class="progress-bar-fill" id="progress-bar-fill"></div>
    </div>
    <div class="progress-filter-bar">
      <button class="filter-chip active" onclick="setStatusFilter('all')">All Books (130)</button>
      <button class="filter-chip" onclick="setStatusFilter('live')">🟢 Live on Amazon (<span id="count-live">0</span>)</button>
      <button class="filter-chip" onclick="setStatusFilter('in_review')">🟡 In Review (<span id="count-review">0</span>)</button>
      <button class="filter-chip" onclick="setStatusFilter('unpublished')">⚪ Unpublished (<span id="count-unpub">130</span>)</button>
    </div>
  </div>

  <div class="top-toolbar">
    <input type="text" id="search-box" class="search-input" placeholder="🔍 Search 130 books across 9 series..." oninput="handleSearch()">
    <div class="catalog-badge">130 BOOKS</div>
  </div>

  <!-- Series Selector Pills -->
  <div class="series-bar" id="series-bar"></div>

  <!-- Volume Tabs -->
  <div class="tab-bar" id="tab-container"></div>

  <!-- Main Content Container -->
  <div id="content-container"></div>

  <!-- In-App Reader Modal (PDF & Full Cover Wrap) -->
  <div class="reader-modal" id="reader-modal">
    <div class="reader-header">
      <div class="reader-title" id="reader-title">Document Viewer</div>
      <div class="reader-actions">
        <a id="reader-external-btn" href="#" target="_blank" class="reader-close-btn" style="text-decoration:none; background:#1F6FEB;">Full View ↗</a>
        <button class="reader-close-btn" onclick="closeReaderModal()">Close ✕</button>
      </div>
    </div>
    <div class="reader-body" id="reader-body"></div>
  </div>

  <!-- PLAYABLE CASE #001 SOLVER MODAL -->
  <div class="reader-modal" id="game-modal">
    <div class="reader-header">
      <div class="reader-title">🎮 Case #001: Playable Forensic Solver</div>
      <button class="reader-close-btn" onclick="closeGameModal()">Close ✕</button>
    </div>
    <div style="padding:16px; overflow-y:auto; flex:1; max-width:680px; margin:0 auto; width:100%;">
      <div style="background:#161B22; border:1px solid var(--border); border-radius:12px; padding:12px; margin-bottom:14px;">
        <div style="font-size:14px; font-weight:800; color:var(--accent); margin-bottom:4px;" id="game-case-title">The Mystery of Library Gallery</div>
        <div style="font-size:12px; color:var(--text-muted); line-height:1.4;" id="game-case-briefing">Lord Harrington was discovered poisoned in the private Library Gallery. Crack the 4 interlocking stages to indict the culprit!</div>
      </div>

      <!-- Stage Selector Tabs -->
      <div style="display:flex; gap:6px; margin-bottom:12px;">
        <button class="tab-btn active" id="game-tab-1" onclick="switchGameStage(1)">1. Sudoku Keys</button>
        <button class="tab-btn" id="game-tab-2" onclick="switchGameStage(2)">2. Decrypt Cipher</button>
        <button class="tab-btn" id="game-tab-3" onclick="switchGameStage(3)">3. Alibi Matrix</button>
        <button class="tab-btn" id="game-tab-4" onclick="switchGameStage(4)">4. Arrest Warrant</button>
      </div>

      <!-- STAGE 1: SUDOKU -->
      <div id="game-stage-1">
        <div style="font-size:12px; color:var(--text-muted); margin-bottom:6px;">
          Solve the 9x9 grid to unmask the <b>4 shaded Key Cells</b> (Alpha, Beta, Gamma, Delta).
        </div>
        <div id="sudoku-board" class="sudoku-board"></div>
        <div class="sudoku-numpad" id="sudoku-numpad">
          <button class="num-btn" onclick="enterSudokuNum(1)">1</button>
          <button class="num-btn" onclick="enterSudokuNum(2)">2</button>
          <button class="num-btn" onclick="enterSudokuNum(3)">3</button>
          <button class="num-btn" onclick="enterSudokuNum(4)">4</button>
          <button class="num-btn" onclick="enterSudokuNum(5)">5</button>
          <button class="num-btn" onclick="enterSudokuNum(6)">6</button>
          <button class="num-btn" onclick="enterSudokuNum(7)">7</button>
          <button class="num-btn" onclick="enterSudokuNum(8)">8</button>
          <button class="num-btn" onclick="enterSudokuNum(9)">9</button>
          <button class="num-btn" style="width:60px; color:var(--danger);" onclick="enterSudokuNum(0)">Clear</button>
          <button class="num-btn" style="width:110px; color:var(--accent);" onclick="revealSudokuKeys()">Reveal Keys</button>
        </div>
        <div style="background:#0D1117; border:1px solid var(--border); border-radius:8px; padding:10px; margin-top:12px; text-align:center;">
          <span style="font-size:11px; color:var(--text-muted);">EXTRACTED KEY CELLS:</span><br>
          <b style="font-size:16px; color:var(--accent); letter-spacing:3px;" id="game-key-code">? ? ? ?</b>
          <div style="font-size:11px; color:#3FB950; margin-top:4px;" id="game-key-status">Solve key cells to unlock Caesar cipher shift</div>
        </div>
      </div>

      <!-- STAGE 2: CIPHER -->
      <div id="game-stage-2" style="display:none;">
        <div style="font-size:12px; color:var(--text-muted); margin-bottom:10px;">
          Use your extracted passkey sum to decode the suspect's dying dispatch:
        </div>
        <div class="card">
          <div class="label" style="color:var(--danger);">Intercepted Encrypted Dispatch:</div>
          <div class="val-box" style="font-family:monospace; color:var(--danger);" id="game-ciphertext">WKH ZHDSRQ ZDV UHWULHYHG IURP WKH FULPH VFHQH DW WZLOLJKW (FDVH 7)</div>
        </div>
        <div style="display:flex; align-items:center; gap:10px; margin:14px 0;">
          <span style="font-size:12px; font-weight:700;">Caesar Shift:</span>
          <input type="range" id="cipher-shift-slider" min="0" max="25" value="0" style="flex:1;" oninput="updateCipherShift(this.value)">
          <span id="cipher-shift-label" style="font-size:14px; font-weight:800; color:var(--accent); width:30px;">+0</span>
          <button class="copy-btn" onclick="autoApplyKeyShift()">Apply Key Shift (+3)</button>
        </div>
        <div class="card">
          <div class="label" style="color:var(--accent-green);">Decrypted Plaintext:</div>
          <div class="val-box" style="font-family:monospace; color:#3FB950; font-weight:700;" id="game-plaintext">...</div>
        </div>
      </div>

      <!-- STAGE 3: LOGIC GRID -->
      <div id="game-stage-3" style="display:none;">
        <div style="font-size:12px; color:var(--text-muted); margin-bottom:8px;">
          Tap cells to toggle: <span style="color:#8B949E;">· (empty)</span> ➔ <span style="color:var(--danger);">✕ (eliminated)</span> ➔ <span style="color:#3FB950;">✓ (confirmed)</span>
        </div>
        <div style="overflow-x:auto;">
          <table class="logic-table" id="logic-matrix-table"></table>
        </div>
        <div class="card" style="margin-top:10px;">
          <div class="label">Forensic Witness Clues (100% Unique Solution):</div>
          <div style="font-size:11px; color:var(--text); line-height:1.5; margin-top:6px;" id="game-clues-list"></div>
        </div>
      </div>

      <!-- STAGE 4: ARREST WARRANT -->
      <div id="game-stage-4" style="display:none;">
        <div style="background:#161B22; border:2px solid var(--accent); border-radius:12px; padding:16px; text-align:center;">
          <div style="font-size:16px; font-weight:800; color:var(--accent); letter-spacing:1px; margin-bottom:4px;">OFFICIAL STATE ARREST WARRANT</div>
          <div style="font-size:11px; color:var(--text-muted); margin-bottom:14px;">Special Investigation Division &bull; Case Docket #001</div>

          <div style="text-align:left; display:flex; flex-direction:column; gap:10px; max-width:400px; margin:0 auto 16px auto;">
            <div>
              <label class="label">Perpetrator Indictment:</label>
              <select id="warrant-suspect-select" class="search-input" style="width:100%; margin-top:4px;"></select>
            </div>
            <div>
              <label class="label">Crime Scene Locus:</label>
              <select id="warrant-room-select" class="search-input" style="width:100%; margin-top:4px;"></select>
            </div>
            <div>
              <label class="label">Certified Murder Instrument:</label>
              <select id="warrant-weapon-select" class="search-input" style="width:100%; margin-top:4px;"></select>
            </div>
          </div>

          <button class="btn-header btn-game" style="margin:0 auto; padding:10px 24px; font-size:14px;" onclick="verifyArrestWarrant()">
            ⚖️ CERTIFY & EXECUTE WARRANT
          </button>

          <div id="warrant-result-box" style="margin-top:16px; display:none; padding:12px; border-radius:8px;"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- ROYALTY & REVENUE PROJECTION CALCULATOR MODAL -->
  <div class="reader-modal" id="calc-modal">
    <div class="reader-header">
      <div class="reader-title">💰 Amazon Royalty & Passive Income Calculator</div>
      <button class="reader-close-btn" onclick="closeCalcModal()">Close ✕</button>
    </div>
    <div style="padding:16px; overflow-y:auto; flex:1; max-width:600px; margin:0 auto; width:100%;">
      <div class="card" style="border-color:#2EA043; background:rgba(46,160,67,0.06);">
        <div style="font-size:13px; color:#3FB950; font-weight:700; margin-bottom:4px;">Publishing Empire Revenue Engine</div>
        <div style="font-size:11px; color:var(--text-muted);">Calculates exact Amazon KDP net author earnings after manufacturing print costs.</div>
      </div>

      <div class="card">
        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
          <span class="label">Published Titles:</span>
          <b style="color:var(--accent);" id="calc-books-val">30 Books</b>
        </div>
        <input type="range" id="calc-books-slider" min="1" max="130" value="30" style="width:100%;" oninput="recalculateRoyalties()">

        <div style="display:flex; justify-content:space-between; margin:14px 0 6px 0;">
          <span class="label">Avg Daily Sales Per Book:</span>
          <b style="color:var(--accent);" id="calc-sales-val">3 Copies / Day</b>
        </div>
        <input type="range" id="calc-sales-slider" min="0.5" max="15" step="0.5" value="3" style="width:100%;" oninput="recalculateRoyalties()">

        <div style="display:flex; justify-content:space-between; margin:14px 0 6px 0;">
          <span class="label">List Price (USD):</span>
          <b style="color:var(--accent);" id="calc-price-val">$12.99 ($4.68 Royalty)</b>
        </div>
        <input type="range" id="calc-price-slider" min="9.99" max="19.99" step="1" value="12.99" style="width:100%;" oninput="recalculateRoyalties()">
      </div>

      <!-- RESULTS METRIC CARDS -->
      <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; margin-bottom:12px;">
        <div class="card" style="text-align:center; padding:10px;">
          <div style="font-size:10px; color:var(--text-muted); font-weight:700;">DAILY PROFIT</div>
          <div style="font-size:16px; font-weight:800; color:#3FB950; margin-top:4px;" id="calc-daily-res">$351</div>
        </div>
        <div class="card" style="text-align:center; padding:10px; border-color:var(--accent);">
          <div style="font-size:10px; color:var(--text-muted); font-weight:700;">MONTHLY ROYALTY</div>
          <div style="font-size:17px; font-weight:800; color:var(--accent); margin-top:4px;" id="calc-monthly-res">$10,530</div>
        </div>
        <div class="card" style="text-align:center; padding:10px;">
          <div style="font-size:10px; color:var(--text-muted); font-weight:700;">ANNUAL INCOME</div>
          <div style="font-size:16px; font-weight:800; color:#58A6FF; margin-top:4px;" id="calc-annual-res">$128,115</div>
        </div>
      </div>

      <div class="card">
        <div class="label" style="margin-bottom:8px;">Milestone Tracker:</div>
        <div style="display:flex; flex-direction:column; gap:8px; font-size:11px;">
          <div>
            <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
              <span>🥉 $1,000 / month (Part-time Side Income)</span>
              <b id="ms-1-pct">100%</b>
            </div>
            <div class="progress-bar-bg"><div class="progress-bar-fill" id="ms-1-bar" style="width:100%;"></div></div>
          </div>
          <div>
            <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
              <span>🥈 $5,000 / month (Full-Time Income)</span>
              <b id="ms-2-pct">100%</b>
            </div>
            <div class="progress-bar-bg"><div class="progress-bar-fill" id="ms-2-bar" style="width:100%;"></div></div>
          </div>
          <div>
            <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
              <span>🥇 $10,000 / month (6-Figure Publishing Empire)</span>
              <b id="ms-3-pct">100%</b>
            </div>
            <div class="progress-bar-bg"><div class="progress-bar-fill" id="ms-3-bar" style="width:100%;"></div></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- PROMO KIT & SOCIAL MEDIA GENERATOR MODAL -->
  <div class="reader-modal" id="promo-modal">
    <div class="reader-header">
      <div class="reader-title" id="promo-modal-title">📣 Promo Kit & Social Media Generator</div>
      <button class="reader-close-btn" onclick="closePromoModal()">Close ✕</button>
    </div>
    <div style="padding:16px; overflow-y:auto; flex:1; max-width:600px; margin:0 auto; width:100%;">
      <!-- TikTok / Reels -->
      <div class="card">
        <div class="card-header">
          <span class="label" style="color:#FF7B72;">🎥 TikTok / Instagram Reels Video Script (15s)</span>
          <button class="copy-btn" onclick="copyText(document.getElementById('promo-tiktok-text').innerText)">📋 Copy</button>
        </div>
        <div class="val-box" id="promo-tiktok-text" style="font-size:12px; white-space:pre-wrap;"></div>
      </div>

      <!-- Instagram / Facebook -->
      <div class="card">
        <div class="card-header">
          <span class="label" style="color:#D29922;">📸 Instagram / Facebook Caption & Hashtags</span>
          <button class="copy-btn" onclick="copyText(document.getElementById('promo-ig-text').innerText)">📋 Copy</button>
        </div>
        <div class="val-box" id="promo-ig-text" style="font-size:12px; white-space:pre-wrap;"></div>
      </div>

      <!-- Reddit / Community -->
      <div class="card">
        <div class="card-header">
          <span class="label" style="color:#58A6FF;">💬 Reddit / Book Club Forum Post</span>
          <button class="copy-btn" onclick="copyText(document.getElementById('promo-reddit-text').innerText)">📋 Copy</button>
        </div>
        <div class="val-box" id="promo-reddit-text" style="font-size:12px; white-space:pre-wrap;"></div>
      </div>
    </div>
  </div>

  <!-- ZIP & IPA DOWNLOAD MODAL -->
  <div class="reader-modal" id="zip-modal">
    <div class="reader-header">
      <div class="reader-title">📦 KDP Production Release Packages & Native iOS App</div>
      <button class="reader-close-btn" onclick="closeZipModal()">Close ✕</button>
    </div>
    <div style="padding:16px; overflow-y:auto; flex:1; max-width:600px; margin:0 auto; width:100%;">
      <div style="font-size:12px; color:var(--text-muted); margin-bottom:12px;">
        Download complete print-ready interior PDFs, cover wraps, previews, metadata, Amazon A+ content, and native iOS apps:
      </div>

      <!-- NATIVE IOS IPA APP PACKAGE -->
      <div class="zip-item" style="border-color:#BC8CFF; background:rgba(188,140,255,0.12);">
        <div class="zip-info">
          <span class="zip-name" style="color:#BC8CFF;">📱 KDP Hub iOS Native App (.IPA)</span>
          <span class="zip-sub">Sideload on iPhone (Sideloadly / AltStore / Scarlet) • 959 KB</span>
        </div>
        <a href="KDP_Books_Hub.ipa" download class="zip-dl-btn" style="background:#BC8CFF; color:#000;">Download IPA</a>
      </div>

      <!-- 1-CLICK KDP AUTO-PUBLISHER EXTENSION -->
      <div class="zip-item" style="border-color:#58A6FF; background:rgba(88,166,255,0.12);">
        <div class="zip-info">
          <span class="zip-name" style="color:#58A6FF;">⚡ KDP Auto-Publisher Chrome Extension</span>
          <span class="zip-sub">1-Click Auto-Fill for Amazon KDP • Pre-Loaded with all 100 Books • 28.6 KB</span>
        </div>
        <a href="KDP_Production_Packages/KDP_100_Book_AutoPublisher_Chrome_Extension.zip" download class="zip-dl-btn" style="background:#58A6FF; color:#000;">Download Extension</a>
      </div>

      <!-- MASTER A+ CONTENT SUITE -->
      <div class="zip-item" style="border-color:#D4AF37; background:rgba(212,175,55,0.12);">
        <div class="zip-info">
          <span class="zip-name" style="color:#D4AF37;">🎨 Amazon A+ Content Master Suite</span>
          <span class="zip-sub">All 7 Series • 63 High-Res Graphics • Copy Guides • 2.92 MB</span>
        </div>
        <a href="KDP_Production_Packages/Amazon_A_Plus_Content_Master_Suite.zip" download class="zip-dl-btn" style="background:#D4AF37; color:#000;">Download A+</a>
      </div>

      <!-- MASTER 130-BOOK SUITE -->
      <div class="zip-item" style="border-color:var(--accent); background:rgba(227,179,65,0.08);">
        <div class="zip-info">
          <span class="zip-name" style="color:var(--accent);">🌟 Master 130-Book Catalog Suite</span>
          <span class="zip-sub">All 9 Series • 801 Files • 44.74 MB</span>
        </div>
        <a href="KDP_Production_Packages/Master_130_Book_Catalog_Full_Production_Suite.zip" download class="zip-dl-btn" style="background:var(--accent); color:#000;">Download All</a>
      </div>

      <div class="zip-item">
        <div class="zip-info">
          <span class="zip-name">🎩 The Lupin Heists (Parisian Gentleman Thief)</span>
          <span class="zip-sub">15 Volumes • 90 Files • 5.21 MB</span>
        </div>
        <a href="KDP_Production_Packages/The_Lupin_Heists_15_Volumes_KDP_Pack.zip" download class="zip-dl-btn">Download</a>
      </div>

      <div class="zip-item">
        <div class="zip-info">
          <span class="zip-name">👁️ The Machine Protocols (Mass-Surveillance AI)</span>
          <span class="zip-sub">15 Volumes • 90 Files • 5.23 MB</span>
        </div>
        <a href="KDP_Production_Packages/The_Machine_Protocols_15_Volumes_KDP_Pack.zip" download class="zip-dl-btn">Download</a>
      </div>

      <div class="zip-item">
        <div class="zip-info">
          <span class="zip-name">🕵️ The Detective's Case Files</span>
          <span class="zip-sub">15 Volumes • 108 Files • 5.63 MB</span>
        </div>
        <a href="KDP_Production_Packages/The_Detectives_Case_Files_15_Volumes_KDP_Pack.zip" download class="zip-dl-btn">Download</a>
      </div>

      <div class="zip-item">
        <div class="zip-info">
          <span class="zip-name">🚀 Project X (Sci-Fi Mars)</span>
          <span class="zip-sub">15 Volumes • 96 Files • 5.25 MB</span>
        </div>
        <a href="KDP_Production_Packages/Project_X_15_Volumes_KDP_Pack.zip" download class="zip-dl-btn">Download</a>
      </div>

      <div class="zip-item">
        <div class="zip-info">
          <span class="zip-name">🏰 The Ravencrest Chronicles</span>
          <span class="zip-sub">15 Volumes • 90 Files • 5.23 MB</span>
        </div>
        <a href="KDP_Production_Packages/The_Ravencrest_Chronicles_15_Volumes_KDP_Pack.zip" download class="zip-dl-btn">Download</a>
      </div>

      <div class="zip-item">
        <div class="zip-info">
          <span class="zip-name">📻 The Bletchley Protocols</span>
          <span class="zip-sub">15 Volumes • 90 Files • 5.16 MB</span>
        </div>
        <a href="KDP_Production_Packages/The_Bletchley_Protocols_15_Volumes_KDP_Pack.zip" download class="zip-dl-btn">Download</a>
      </div>

      <div class="zip-item">
        <div class="zip-info">
          <span class="zip-name">🏺 Crypt of the Pharaohs</span>
          <span class="zip-sub">15 Volumes • 90 Files • 4.84 MB</span>
        </div>
        <a href="KDP_Production_Packages/Crypt_of_the_Pharaohs_15_Volumes_KDP_Pack.zip" download class="zip-dl-btn">Download</a>
      </div>

      <div class="zip-item">
        <div class="zip-info">
          <span class="zip-name">🏥 The Blackwood Asylum Files</span>
          <span class="zip-sub">15 Volumes • 90 Files • 4.84 MB</span>
        </div>
        <a href="KDP_Production_Packages/The_Blackwood_Asylum_Files_15_Volumes_KDP_Pack.zip" download class="zip-dl-btn">Download</a>
      </div>

      <div class="zip-item">
        <div class="zip-info">
          <span class="zip-name">🚂 The Grand Orient Express</span>
          <span class="zip-sub">10 Volumes • 60 Files • 3.31 MB</span>
        </div>
        <a href="KDP_Production_Packages/The_Grand_Orient_Express_10_Volumes_KDP_Pack.zip" download class="zip-dl-btn">Download</a>
      </div>
    </div>
  </div>

  <div id="toast" class="toast">Copied to clipboard! ✓</div>

  <script>
    const INITIAL_CATALOG = {json.dumps(catalog)};
    const CASE_1_GAME = {json.dumps(CASE_1_DATA)};
    const SERIES_APLUS_MAP = {json.dumps(SERIES_APLUS_MAP)};

    const SERIES_ORDER = [
      "The Detective\'s Case Files",
      "The Lupin Heists",
      "The Machine Protocols",
      "Project X",
      "The Ravencrest Chronicles",
      "The Bletchley Protocols",
      "Crypt of the Pharaohs",
      "The Blackwood Asylum Files",
      "The Grand Orient Express"
    ];

    const firebaseEndpoint = "https://kdp-books-hub-26a1c-default-rtdb.europe-west1.firebasedatabase.app/";
    let currentCatalog = INITIAL_CATALOG;
    let activeSeries = localStorage.getItem('kdp_active_series_100') || SERIES_ORDER[0];
    let activeVolId = null;
    let searchQuery = "";
    let statusFilter = "all"; // 'all', 'live', 'in_review', 'unpublished'

    // Load saved publishing statuses
    let bookStatuses = JSON.parse(localStorage.getItem('kdp_publishing_statuses_v4') || "{{}}");
    let bookAsins = JSON.parse(localStorage.getItem('kdp_publishing_asins_v4') || "{{}}");

    function saveStatuses() {{
      localStorage.setItem('kdp_publishing_statuses_v4', JSON.stringify(bookStatuses));
      localStorage.setItem('kdp_publishing_asins_v4', JSON.stringify(bookAsins));
      updateProgressMetrics();
    }}

    function setBookStatus(id, val) {{
      bookStatuses[id] = val;
      saveStatuses();
      renderApp();
      showToast(`Updated status to ${{val.toUpperCase()}}! ✓`);
    }}

    function setBookAsin(id, asinVal) {{
      bookAsins[id] = asinVal.trim();
      saveStatuses();
      renderApp();
      showToast("Saved Amazon ASIN! ✓");
    }}

    function setStatusFilter(filt) {{
      statusFilter = filt;
      document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
      event.target.classList.add('active');
      renderApp();
    }}

    function updateProgressMetrics() {{
      let live = 0, inReview = 0, unpub = 0;
      currentCatalog.forEach(b => {{
        const st = bookStatuses[b.id] || 'unpublished';
        if (st === 'live') live++;
        else if (st === 'in_review') inReview++;
        else unpub++;
      }});

      document.getElementById('count-live').textContent = live;
      document.getElementById('count-review').textContent = inReview;
      document.getElementById('count-unpub').textContent = unpub;

      const pct = Math.round((live / currentCatalog.length) * 100);
      document.getElementById('progress-text').textContent = `📊 KDP Publishing Progress: ${{live}} / ${{currentCatalog.length}} Live (${{pct}}%)`;
      document.getElementById('progress-bar-fill').style.width = `${{pct}}%`;
      
      const liveMonthly = live * 3 * 30 * 4.68;
      document.getElementById('projected-royalty-badge').textContent = `Est. Live Royalties: $${{liveMonthly.toFixed(0)}}/mo`;
    }}

    function handleSearch() {{
      searchQuery = document.getElementById('search-box').value.trim().toLowerCase();
      renderApp();
    }}

    function getFilteredCatalog() {{
      let list = currentCatalog;
      if (searchQuery) {{
        list = list.filter(book => {{
          const titleMatch = (book.title || '').toLowerCase().includes(searchQuery);
          const seriesMatch = (book.series || '').toLowerCase().includes(searchQuery);
          const kwMatch = (book.keywords || []).some(k => k.toLowerCase().includes(searchQuery));
          return titleMatch || seriesMatch || kwMatch;
        }});
      }}
      if (statusFilter !== 'all') {{
        list = list.filter(b => {{
          const st = bookStatuses[b.id] || 'unpublished';
          return st === statusFilter;
        }});
      }}
      return list;
    }}

    function getVolumesForActiveSeries() {{
      const filtered = getFilteredCatalog();
      return filtered.filter(b => b.series === activeSeries);
    }}

    function toggleAplusDrawer(drawerId) {{
      const drawer = document.getElementById(drawerId);
      if (drawer) {{
        drawer.classList.toggle('open');
      }}
    }}

    function renderApp() {{
      const seriesBar = document.getElementById('series-bar');
      const tabContainer = document.getElementById('tab-container');
      const contentContainer = document.getElementById('content-container');

      seriesBar.innerHTML = '';
      const filtered = getFilteredCatalog();

      const presentSeries = SERIES_ORDER.filter(s => filtered.some(b => b.series === s));
      if (!presentSeries.includes(activeSeries) && presentSeries.length > 0) {{
        activeSeries = presentSeries[0];
      }}

      presentSeries.forEach(sName => {{
        const count = filtered.filter(b => b.series === sName).length;
        const pill = document.createElement('button');
        pill.className = `series-pill ${{sName === activeSeries ? 'active' : ''}}`;
        
        let icon = "📚";
        if (sName.includes("Detective")) icon = "🕵️";
        else if (sName.includes("Project X")) icon = "🚀";
        else if (sName.includes("Ravencrest")) icon = "🏰";
        else if (sName.includes("Bletchley")) icon = "📻";
        else if (sName.includes("Pharaoh")) icon = "🏺";
        else if (sName.includes("Asylum")) icon = "🏥";
        else if (sName.includes("Express")) icon = "🚂";

        pill.textContent = `${{icon}} ${{sName}} (${{count}})`;
        pill.onclick = () => {{
          activeSeries = sName;
          localStorage.setItem('kdp_active_series_100', activeSeries);
          const vols = getVolumesForActiveSeries();
          activeVolId = vols[0] ? vols[0].id : null;
          renderApp();
        }};
        seriesBar.appendChild(pill);
      }});

      document.getElementById('series-subtitle').textContent = `${{activeSeries}} (${{currentCatalog.filter(b => b.series === activeSeries).length}} Volumes)`;

      tabContainer.innerHTML = '';
      contentContainer.innerHTML = '';
      const vols = getVolumesForActiveSeries();

      if (vols.length === 0) {{
        contentContainer.innerHTML = `<div class="card" style="text-align:center; padding:30px; color:var(--text-muted);">No books found matching criteria.</div>`;
        return;
      }}

      if (!activeVolId || !vols.some(v => v.id === activeVolId)) {{
        activeVolId = vols[0].id;
      }}

      vols.forEach((book) => {{
        const btn = document.createElement('button');
        btn.className = `tab-btn ${{book.id === activeVolId ? 'active' : ''}}`;
        btn.textContent = book.tab_name || `Volume ${{book.vol_number}}`;
        btn.onclick = () => {{
          activeVolId = book.id;
          renderApp();
        }};
        tabContainer.appendChild(btn);

        if (book.id === activeVolId) {{
          const volDiv = document.createElement('div');

          const interiorPdf = book.pdf_interior_url;
          const coverPdf = book.pdf_cover_url;
          const frontImg = book.cover_img_url;
          const wrapImg = book.cover_wrap_img_url;
          const aplusDir = SERIES_APLUS_MAP[book.series] || "Amazon_A_Plus_Content/01_The_Detectives_Case_Files";
          const curStatus = bookStatuses[book.id] || "unpublished";
          const curAsin = bookAsins[book.id] || "";

          volDiv.innerHTML = `
            <!-- COVER & PDF SHOWCASE HERO CARD -->
            <div class="cover-showcase-card">
              <div class="book-3d-wrap" onclick="openImageModal('${{wrapImg}}?v=luxury_v3', '${{escapeQuotes(book.title)}} - Full Cover Wrap')">
                <img src="${{frontImg}}?v=luxury_v3" class="book-cover-img" alt="${{escapeHtml(book.title)}} Front Cover" onerror="this.onerror=null; this.src='app_icon_1024.png';">
              </div>
              <div class="cover-tap-hint">🔍 Tap cover image to inspect full wrap (Front, Spine & Back)</div>

              <!-- KDP PUBLISHING STATUS STRIP -->
              <div class="status-card">
                <div class="status-badge-wrap">
                  <span class="label">KDP Status:</span>
                  <select class="status-select" onchange="setBookStatus('${{book.id}}', this.value)">
                    <option value="unpublished" ${{curStatus==='unpublished'?'selected':''}}>⚪ Unpublished</option>
                    <option value="in_review" ${{curStatus==='in_review'?'selected':''}}>🟡 In Review on KDP</option>
                    <option value="live" ${{curStatus==='live'?'selected':''}}>🟢 Live on Amazon</option>
                  </select>
                </div>
                <div style="display:flex; align-items:center; gap:6px;">
                  <input type="text" placeholder="Amazon ASIN (e.g. B0D...)" value="${{curAsin}}" id="asin-input-${{book.id}}" class="search-input" style="width:120px; padding:4px 8px; font-size:11px;" onchange="setBookAsin('${{book.id}}', this.value)">
                  ${{curAsin ? `<a href="https://www.amazon.com/dp/${{curAsin}}" target="_blank" class="copy-btn" style="background:#2EA043; color:#FFF; text-decoration:none;">🛒 Amazon ↗</a>` : ''}}
                </div>
              </div>

              <div class="badge-bar">
                <span class="badge badge-gold">VOLUME ${{book.vol_number}}</span>
                <span class="badge badge-green">176 PAGES • 6" × 9"</span>
                <span class="badge badge-blue">PROFIT: $${{book.royalty_usd || '4.68'}}/SALE</span>
                <span class="badge badge-purple">100% UNIQUE LOGIC</span>
              </div>

              <!-- ONE-TAP PDF BUTTONS -->
              <div class="action-grid">
                <a href="${{interiorPdf}}" target="_blank" class="btn-pdf-interior">
                  📖 Interior PDF (176 Pgs)
                </a>
                <a href="${{coverPdf}}" target="_blank" class="btn-pdf-cover">
                  🎨 Cover Wrap PDF
                </a>
              </div>

              <button class="btn-quick-read" onclick="openPdfModal('${{interiorPdf}}', '${{escapeQuotes(book.title)}}')">
                👁️ In-App PDF Quick Reader
              </button>

              <button class="btn-promo-toggle" onclick="openPromoModal('${{book.id}}')">
                📣 1-Click Social Media & Promo Kit
              </button>

              <button class="btn-aplus-toggle" onclick="toggleAplusDrawer('aplus-drawer-${{book.id}}')">
                🎨 View Amazon A+ Content Graphics (5 Modules)
              </button>

              <!-- A+ CONTENT DRAWER -->
              <div class="aplus-drawer" id="aplus-drawer-${{book.id}}">
                <div style="font-size:12px; color:var(--text-muted); margin-bottom:10px; text-align:left;">
                  <b>Official Amazon A+ Content Graphics</b> ready to upload directly to Amazon KDP A+ Content Manager:
                </div>

                <!-- Module 1 -->
                <div class="aplus-preview-item">
                  <div class="aplus-preview-header">
                    <span>Module 1: Hero Showcase Banner (970 × 600)</span>
                    <a href="${{aplusDir}}/Module_1_Hero_Showcase_970x600.png" download class="copy-btn">Download</a>
                  </div>
                  <img src="${{aplusDir}}/Module_1_Hero_Showcase_970x600.png" class="aplus-img-tag" onclick="openImageModal('${{aplusDir}}/Module_1_Hero_Showcase_970x600.png', 'A+ Module 1: Hero Showcase')">
                </div>

                <!-- Module 2 -->
                <div class="aplus-preview-item">
                  <div class="aplus-preview-header">
                    <span>Module 2: Inside the Investigation (970 × 600)</span>
                    <a href="${{aplusDir}}/Module_2_Investigation_Flow_970x600.png" download class="copy-btn">Download</a>
                  </div>
                  <img src="${{aplusDir}}/Module_2_Investigation_Flow_970x600.png" class="aplus-img-tag" onclick="openImageModal('${{aplusDir}}/Module_2_Investigation_Flow_970x600.png', 'A+ Module 2: Investigation Flow')">
                </div>

                <!-- Module 3 -->
                <div class="aplus-preview-item">
                  <div class="aplus-preview-header">
                    <span>Module 3: Four Feature Tiles (4 × 300 × 300)</span>
                  </div>
                  <div class="aplus-tiles-grid">
                    <img src="${{aplusDir}}/Module_3_Feature_1_Sudoku_300x300.png" class="aplus-tile-img" onclick="openImageModal('${{aplusDir}}/Module_3_Feature_1_Sudoku_300x300.png', 'Feature 1: Forensic Sudoku')">
                    <img src="${{aplusDir}}/Module_3_Feature_2_Cipher_300x300.png" class="aplus-tile-img" onclick="openImageModal('${{aplusDir}}/Module_3_Feature_2_Cipher_300x300.png', 'Feature 2: Passkey Cipher')">
                    <img src="${{aplusDir}}/Module_3_Feature_3_LogicGrid_300x300.png" class="aplus-tile-img" onclick="openImageModal('${{aplusDir}}/Module_3_Feature_3_LogicGrid_300x300.png', 'Feature 3: Alibi Matrix')">
                    <img src="${{aplusDir}}/Module_3_Feature_4_ArrestWarrant_300x300.png" class="aplus-tile-img" onclick="openImageModal('${{aplusDir}}/Module_3_Feature_4_ArrestWarrant_300x300.png', 'Feature 4: Arrest Warrant')">
                  </div>
                </div>

                <!-- Module 4 -->
                <div class="aplus-preview-item">
                  <div class="aplus-preview-header">
                    <span>Module 4: Quality & Specs Banner (970 × 300)</span>
                    <a href="${{aplusDir}}/Module_4_Quality_Specs_Banner_970x300.png" download class="copy-btn">Download</a>
                  </div>
                  <img src="${{aplusDir}}/Module_4_Quality_Specs_Banner_970x300.png" class="aplus-img-tag" onclick="openImageModal('${{aplusDir}}/Module_4_Quality_Specs_Banner_970x300.png', 'A+ Module 4: Quality Specs')">
                </div>

                <!-- Module 5 -->
                <div class="aplus-preview-item">
                  <div class="aplus-preview-header">
                    <span>Module 5: Collectible Series Lineup (970 × 600)</span>
                    <a href="${{aplusDir}}/Module_5_Series_Lineup_970x600.png" download class="copy-btn">Download</a>
                  </div>
                  <img src="${{aplusDir}}/Module_5_Series_Lineup_970x600.png" class="aplus-img-tag" onclick="openImageModal('${{aplusDir}}/Module_5_Series_Lineup_970x600.png', 'A+ Module 5: Series Lineup')">
                </div>

                <div style="text-align:center; padding:10px 0;">
                  <a href="${{aplusDir}}/A_Plus_Content_Copy_Guide.txt" target="_blank" class="copy-btn" style="padding:8px 16px; font-size:12px; text-decoration:none; display:inline-block;">
                    📋 Open A+ Content Text & Copy Guide
                  </a>
                </div>
              </div>
            </div>

            <!-- 1-CLICK KDP FAST-PUBLISH WIZARD -->
            <div class="card" style="border-color: #238636; background: rgba(35, 134, 54, 0.06);">
              <div class="card-header">
                <span class="label" style="color:#3FB950;">⚡ 1-Click Fast Publisher Stepper</span>
                <span style="font-size:10px; color:var(--text-muted);">Copy directly into Amazon KDP</span>
              </div>
              <div style="display:grid; grid-template-columns: 1fr 1fr; gap:6px; margin-top:6px;">
                <button class="copy-btn" style="padding:8px; font-size:12px; text-align:left;" onclick="copyText('${{escapeQuotes(book.title)}}')">1️⃣ Copy Title</button>
                <button class="copy-btn" style="padding:8px; font-size:12px; text-align:left;" onclick="copyText('${{escapeQuotes(book.subtitle)}}')">2️⃣ Copy Subtitle</button>
                <button class="copy-btn" style="padding:8px; font-size:12px; text-align:left;" onclick="copyText('${{escapeQuotes(book.series)}} # ${{book.vol_number}}')">3️⃣ Copy Series Info</button>
                <button class="copy-btn" style="padding:8px; font-size:12px; text-align:left;" onclick="copyDesc('desc-box-${{book.id}}')">4️⃣ Copy HTML Desc</button>
                <button class="copy-btn" style="padding:8px; font-size:12px; text-align:left;" onclick="copyAllKeywords('${{escapeQuotes((book.keywords || []).join(', '))}}')">5️⃣ Copy 7 Keywords</button>
                <button class="copy-btn" style="padding:8px; font-size:12px; text-align:left;" onclick="copyText('$${{book.price_usd}}')">6️⃣ Copy Price ($${{book.price_usd}})</button>
              </div>
            </div>

            <!-- METADATA CARDS -->
            <div class="card">
              <div class="card-header">
                <span class="label">Book Title</span>
                <button class="copy-btn" onclick="copyText('${{escapeQuotes(book.title)}}')">📋 Copy</button>
              </div>
              <div class="val-box"><b>${{book.title}}</b></div>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="label">Subtitle</span>
                <button class="copy-btn" onclick="copyText('${{escapeQuotes(book.subtitle)}}')">📋 Copy</button>
              </div>
              <div class="val-box">${{book.subtitle}}</div>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="label">Pricing & Royalty Economics (US)</span>
                <button class="copy-btn" onclick="copyText('${{book.price_usd}}')">Copy $${{book.price_usd}}</button>
              </div>
              <div class="val-box">
                <b>List Price:</b> $${{book.price_usd}} USD &nbsp;|&nbsp; 
                <b>Print Cost:</b> $${{book.print_cost_usd || '3.11'}} &nbsp;|&nbsp; 
                <b style="color:#3FB950;">Author Royalty (60%):</b> $${{book.royalty_usd || '4.68'}} USD / sale
              </div>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="label">Print & Binding Specifications</span>
                <button class="copy-btn" onclick="copyText('6x9 in, 176 pages, Black and White, No Bleed, Matte finish')">📋 Copy Specs</button>
              </div>
              <div class="val-box">
                <b>Trim:</b> ${{book.trim || '6\" x 9\"'}} &nbsp;|&nbsp; 
                <b>Pages:</b> ${{book.pages || 176}} pages &nbsp;|&nbsp; 
                <b>Spine Width:</b> 0.396 in (10.06 mm)<br>
                <b>Interior:</b> B&W on White Paper &nbsp;|&nbsp; 
                <b>Bleed:</b> ${{book.bleed || 'No Bleed'}} &nbsp;|&nbsp; 
                <b>Cover Finish:</b> Matte
              </div>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="label">7 Backend Search Keywords</span>
                <button class="copy-btn" onclick="copyAllKeywords('${{escapeQuotes((book.keywords || []).join(', '))}}')">📋 Copy All 7</button>
              </div>
              <div class="kw-grid">
                ${{(book.keywords || []).map((kw, i) => `
                  <div class="kw-item">
                    <span><b>${{i+1}}.</b> ${{kw}}</span>
                    <button class="copy-btn" onclick="copyText('${{escapeQuotes(kw)}}')">Copy</button>
                  </div>
                `).join('')}}
              </div>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="label">Amazon KDP Categories</span>
                <button class="copy-btn" onclick="copyAllKeywords('${{escapeQuotes((book.categories || []).join('\\n'))}}')">📋 Copy</button>
              </div>
              <div class="val-box">
                ${{(book.categories || []).map(cat => `• ${{cat}}`).join('<br>')}}
              </div>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="label">Amazon HTML Description</span>
                <button class="copy-btn" onclick="copyDesc('desc-box-${{book.id}}')">📋 Copy HTML</button>
              </div>
              <div id="desc-box-${{book.id}}" class="val-box" style="font-size:11px; max-height:140px; overflow-y:auto; white-space:pre-wrap;">${{escapeHtml(book.description_html)}}</div>
            </div>
          `;
          contentContainer.appendChild(volDiv);
        }}
      }});

      updateProgressMetrics();
    }}

    function openPdfModal(pdfUrl, title) {{
      const modal = document.getElementById('reader-modal');
      const body = document.getElementById('reader-body');
      const titleElem = document.getElementById('reader-title');
      const extBtn = document.getElementById('reader-external-btn');

      titleElem.textContent = title;
      extBtn.href = pdfUrl;
      body.innerHTML = `<iframe class="reader-iframe" src="${{pdfUrl}}"></iframe>`;
      modal.classList.add('open');
    }}

    function openImageModal(imgUrl, title) {{
      const modal = document.getElementById('reader-modal');
      const body = document.getElementById('reader-body');
      const titleElem = document.getElementById('reader-title');
      const extBtn = document.getElementById('reader-external-btn');

      titleElem.textContent = title;
      extBtn.href = imgUrl;
      body.innerHTML = `<img src="${{imgUrl}}" class="reader-img" alt="Cover Wrap Preview">`;
      modal.classList.add('open');
    }}

    function closeReaderModal() {{
      const modal = document.getElementById('reader-modal');
      const body = document.getElementById('reader-body');
      modal.classList.remove('open');
      body.innerHTML = '';
    }}

    function openZipModal() {{
      document.getElementById('zip-modal').classList.add('open');
    }}

    function closeZipModal() {{
      document.getElementById('zip-modal').classList.remove('open');
    }}

    function openCalcModal() {{
      document.getElementById('calc-modal').classList.add('open');
      recalculateRoyalties();
    }}

    function closeCalcModal() {{
      document.getElementById('calc-modal').classList.remove('open');
    }}

    function recalculateRoyalties() {{
      const books = parseInt(document.getElementById('calc-books-slider').value);
      const salesPerDay = parseFloat(document.getElementById('calc-sales-slider').value);
      const price = parseFloat(document.getElementById('calc-price-slider').value);

      document.getElementById('calc-books-val').textContent = `${{books}} Books`;
      document.getElementById('calc-sales-val').textContent = `${{salesPerDay}} Copies / Day`;
      
      const royaltyPerBook = (price * 0.60) - 3.11;
      document.getElementById('calc-price-val').textContent = `$${{price.toFixed(2)}} ($${{royaltyPerBook.toFixed(2)}} Royalty)`;

      const daily = books * salesPerDay * royaltyPerBook;
      const monthly = daily * 30;
      const annual = daily * 365;

      document.getElementById('calc-daily-res').textContent = `$${{Math.round(daily).toLocaleString()}}`;
      document.getElementById('calc-monthly-res').textContent = `$${{Math.round(monthly).toLocaleString()}}`;
      document.getElementById('calc-annual-res').textContent = `$${{Math.round(annual).toLocaleString()}}`;

      // Milestones
      const m1 = Math.min(100, Math.round((monthly / 1000) * 100));
      const m2 = Math.min(100, Math.round((monthly / 5000) * 100));
      const m3 = Math.min(100, Math.round((monthly / 10000) * 100));

      document.getElementById('ms-1-pct').textContent = `${{m1}}%`;
      document.getElementById('ms-1-bar').style.width = `${{m1}}%`;
      document.getElementById('ms-2-pct').textContent = `${{m2}}%`;
      document.getElementById('ms-2-bar').style.width = `${{m2}}%`;
      document.getElementById('ms-3-pct').textContent = `${{m3}}%`;
      document.getElementById('ms-3-bar').style.width = `${{m3}}%`;
    }}

    // Promo Modal
    let promoCurrentBook = null;
    function openPromoModal(bookId) {{
      const book = currentCatalog.find(b => b.id === bookId) || currentCatalog[0];
      promoCurrentBook = book;
      document.getElementById('promo-modal-title').textContent = `📣 Promo Kit: ${{book.title}}`;

      // TikTok Script
      const tiktok = `[0:00 - 0:03] HOOK: "99% of people cannot solve this locked-room mystery before the police arrive. Can you?"\\n\\n[0:03 - 0:08] VISUAL: Flip to Page 9 of '${{book.title}}'. Point to the 4 shaded Sudoku key cells.\\n"Every murder case in this book is an interlocking 4-stage puzzle. First you solve the Sudoku to unmask 4 secret digits..."\\n\\n[0:08 - 0:12] "Then you sum the digits to decrypt the victim's dying cipher dispatch... which unlocks the alibi logic grid!"\\n\\n[0:12 - 0:15] CTA: "Get ${{book.title}} on Amazon today or test your detective IQ at the link in bio!"`;

      // Instagram Caption
      const ig = `Can you outthink the killer before emergency air runs out? 🕵️‍♂️✨\\n\\nWelcome to '${{book.title}}' — a brand new 4-stage interactive murder mystery experience featuring 35 interlocking case files.\\n\\n🔍 STAGE 1: Forensic Sudoku Keys\\n📻 STAGE 2: Intercepted Cipher Decryption\\n🧩 STAGE 3: Airtight Alibi Logic Grid (100% Unique Solution)\\n📜 STAGE 4: Official State Arrest Warrant\\n\\nNow available in 6" x 9" Trade Paperback on Amazon!\\n\\n#murdermystery #logicpuzzle #sudoku #cozycrime #detectivegames #whodunit #adultactivitybook #escapegame #puzzlebook #braingames #booksbooksbooks #bookstagram #amazonkdp #indieauthor`;

      // Reddit Post
      const reddit = `Title: I designed a 176-page 4-Stage Interlocking Murder Mystery Puzzle Book with verified zero-guesswork logic grids\\n\\nHey everyone! For fans of Golden Age mysteries (Agatha Christie, Sherlock Holmes) and deductive brain games, I just published '${{book.title}}'.\\n\\nUnlike isolated puzzle books, every single investigation connects 4 puzzles together: solving the 9x9 Sudoku reveals 4 shaded cells that give you the mathematical shift for the victim's dying cipher, which provides the proof needed to solve the alibi grid.\\n\\nAll 35 cases are constraint-solved to ensure exactly 1 unique solution. Available on Amazon in paperback!`;

      document.getElementById('promo-tiktok-text').innerText = tiktok;
      document.getElementById('promo-ig-text').innerText = ig;
      document.getElementById('promo-reddit-text').innerText = reddit;

      document.getElementById('promo-modal').classList.add('open');
    }}

    function closePromoModal() {{
      document.getElementById('promo-modal').classList.remove('open');
    }}

    // Playable Case Solver Game Logic
    let currentSudoku = [];
    let selectedCell = null;
    let logicGridState = {{}};

    function openGameModal() {{
      document.getElementById('game-modal').classList.add('open');
      initGame();
    }}

    function closeGameModal() {{
      document.getElementById('game-modal').classList.remove('open');
    }}

    function switchGameStage(stageNum) {{
      for (let s = 1; s <= 4; s++) {{
        document.getElementById(`game-stage-${{s}}`).style.display = s === stageNum ? 'block' : 'none';
        document.getElementById(`game-tab-${{s}}`).classList.toggle('active', s === stageNum);
      }}
    }}

    function initGame() {{
      // Reset Sudoku
      const puzzle = CASE_1_GAME.sudoku.puzzle;
      currentSudoku = JSON.parse(JSON.stringify(puzzle));
      renderSudokuBoard();

      // Init Warrant dropdowns
      const susSelect = document.getElementById('warrant-suspect-select');
      const roomSelect = document.getElementById('warrant-room-select');
      const weapSelect = document.getElementById('warrant-weapon-select');

      susSelect.innerHTML = CASE_1_GAME.logic_grid.suspects.map(s => `<option value="${{s}}">${{s}}</option>`).join('');
      roomSelect.innerHTML = CASE_1_GAME.logic_grid.rooms.map(r => `<option value="${{r}}">${{r}}</option>`).join('');
      weapSelect.innerHTML = CASE_1_GAME.logic_grid.weapons.map(w => `<option value="${{w}}">${{w}}</option>`).join('');

      // Render clues
      document.getElementById('game-clues-list').innerHTML = CASE_1_GAME.logic_grid.clues.map(c => `• ${{c}}`).join('<br>');

      // Init Logic table
      renderLogicMatrix();
    }}

    function renderSudokuBoard() {{
      const board = document.getElementById('sudoku-board');
      board.innerHTML = '';
      const keyCoords = CASE_1_GAME.sudoku.key_cells;

      for (let r = 0; r < 9; r++) {{
        for (let c = 0; c < 9; c++) {{
          const cell = document.createElement('div');
          const val = currentSudoku[r][c];
          const isFixed = CASE_1_GAME.sudoku.puzzle[r][c] !== 0;
          const keyMatch = keyCoords.find(k => k.r === r && k.c === c);

          cell.className = `sudoku-cell ${{isFixed ? 'fixed' : ''}} ${{keyMatch ? 'key-cell' : ''}}`;
          cell.textContent = val !== 0 ? val : '';
          
          if (!isFixed) {{
            cell.onclick = () => selectSudokuCell(r, c, cell);
          }}
          board.appendChild(cell);
        }}
      }}
      checkKeyProgress();
    }}

    function selectSudokuCell(r, c, cellElem) {{
      document.querySelectorAll('.sudoku-cell').forEach(c => c.classList.remove('active-cell'));
      cellElem.classList.add('active-cell');
      selectedCell = {{ r, c, elem: cellElem }};
    }}

    function enterSudokuNum(num) {{
      if (!selectedCell) {{
        showToast("Tap an empty cell first!");
        return;
      }}
      currentSudoku[selectedCell.r][selectedCell.c] = num;
      selectedCell.elem.textContent = num !== 0 ? num : '';
      checkKeyProgress();
    }}

    function revealSudokuKeys() {{
      CASE_1_GAME.sudoku.key_cells.forEach(k => {{
        currentSudoku[k.r][k.c] = k.digit;
      }});
      renderSudokuBoard();
      showToast("Revealed 4 Key Cells! (+3 shift unlocked) ✓");
    }}

    function checkKeyProgress() {{
      const keys = CASE_1_GAME.sudoku.key_cells;
      let solvedCount = 0;
      let digits = [];

      keys.forEach(k => {{
        const userVal = currentSudoku[k.r][k.c];
        if (userVal === k.digit) {{
          solvedCount++;
          digits.push(userVal);
        }} else {{
          digits.push('?');
        }}
      }});

      document.getElementById('game-key-code').textContent = digits.join(' ');
      if (solvedCount === 4) {{
        document.getElementById('game-key-status').innerHTML = `<b style="color:#3FB950;">ALL 4 KEYS UNLOCKED! Sum = 29 ➔ Shift = +3</b>`;
        autoApplyKeyShift();
      }}
    }}

    function updateCipherShift(shiftVal) {{
      document.getElementById('cipher-shift-label').textContent = `+${{shiftVal}}`;
      const ciphertext = CASE_1_GAME.cipher.ciphertext;
      let plaintext = "";
      const s = parseInt(shiftVal);

      for (let i = 0; i < ciphertext.length; i++) {{
        const ch = ciphertext[i];
        if (ch >= 'A' && ch <= 'Z') {{
          const code = ((ch.charCodeAt(0) - 65 - s + 26) % 26) + 65;
          plaintext += String.fromCharCode(code);
        }} else {{
          plaintext += ch;
        }}
      }}
      document.getElementById('game-plaintext').textContent = plaintext;
    }}

    function autoApplyKeyShift() {{
      document.getElementById('cipher-shift-slider').value = 3;
      updateCipherShift(3);
      showToast("Decoded Dying Dispatch! ✓");
    }}

    function renderLogicMatrix() {{
      const table = document.getElementById('logic-matrix-table');
      const suspects = CASE_1_GAME.logic_grid.suspects;
      const rooms = CASE_1_GAME.logic_grid.rooms;

      let html = '<tr><th>Suspect</th>';
      rooms.forEach(r => html += '<th>' + r.substring(0, 6) + '..</th>');
      html += '</tr>';

      suspects.forEach((s, rIdx) => {{
        html += `<tr><td style="font-weight:700; text-align:left;">${{s}}</td>`;
        rooms.forEach((rm, cIdx) => {{
          const key = `${{rIdx}}_${{cIdx}}`;
          const val = logicGridState[key] || '·';
          html += `<td class="matrix-toggle" onclick="toggleMatrixCell('${{key}}')">${{val}}</td>`;
        }});
        html += '</tr>';
      }});

      table.innerHTML = html;
    }}

    function toggleMatrixCell(key) {{
      const cur = logicGridState[key] || '·';
      if (cur === '·') logicGridState[key] = '<span style="color:var(--danger)">✕</span>';
      else if (cur.includes('✕')) logicGridState[key] = '<span style="color:#3FB950">✓</span>';
      else logicGridState[key] = '·';
      renderLogicMatrix();
    }}

    function verifyArrestWarrant() {{
      const sus = document.getElementById('warrant-suspect-select').value;
      const room = document.getElementById('warrant-room-select').value;
      const weap = document.getElementById('warrant-weapon-select').value;

      const sol = CASE_1_GAME.warrant_solution;
      const resBox = document.getElementById('warrant-result-box');
      resBox.style.display = 'block';

      if (sus === sol.culprit && room === sol.room && weap === sol.weapon) {{
        resBox.style.background = 'rgba(46, 160, 67, 0.2)';
        resBox.style.border = '1px solid #2EA043';
        resBox.innerHTML = `
          <div style="font-size:18px; font-weight:800; color:#3FB950;">🎉 CASE SOLVED • WARRANT CERTIFIED!</div>
          <div style="font-size:12px; color:#FFF; margin-top:6px;">
            You correctly identified <b>${{sus}}</b> who struck down the victim in the <b>${{room}}</b> using the <b>${{weap}}</b>!
          </div>
        `;
        showToast("MAGISTRATE WARRANT CERTIFIED! ✓");
      }} else {{
        resBox.style.background = 'rgba(248, 81, 73, 0.2)';
        resBox.style.border = '1px solid var(--danger)';
        resBox.innerHTML = `
          <div style="font-size:14px; font-weight:800; color:var(--danger);">⚠️ WARRANT REJECTED BY COURT</div>
          <div style="font-size:11px; color:#FFF; margin-top:4px;">
            The evidence does not substantiate this indictment. Review the dying cipher and re-check the logic grid alibis!
          </div>
        `;
      }}
    }}

    function escapeQuotes(str) {{
      return (str || '').replace(/'/g, "\\'").replace(/"/g, '&quot;');
    }}

    function escapeHtml(str) {{
      return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }}

    function showToast(msg) {{
      const toast = document.getElementById('toast');
      toast.textContent = msg || 'Copied to clipboard! ✓';
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 1600);
    }}

    function copyText(txt) {{
      navigator.clipboard.writeText(txt).then(() => showToast('Copied! ✓'));
    }}

    function copyAllKeywords(allKw) {{
      copyText(allKw);
    }}

    function copyDesc(elemId) {{
      const elem = document.getElementById(elemId);
      if (elem) {{
        copyText(elem.innerText);
      }}
    }}

    function refreshFromFirebase() {{
      const statusText = document.getElementById('cloud-status-text');
      statusText.textContent = "Syncing...";
      fetch(firebaseEndpoint + "catalog.json?t=" + Date.now())
        .then(res => res.json())
        .then(data => {{
          if (data && Array.isArray(data)) {{
            currentCatalog = data;
            statusText.textContent = `Cloud Sync (${{data.length}})`;
            showToast(`Synced ${{data.length}} books from Cloud! ✓`);
            renderApp();
          }} else {{
            statusText.textContent = "Cloud Sync (100)";
          }}
        }})
        .catch(err => {{
          console.error("Firebase sync error:", err);
          statusText.textContent = "Offline Ready (100)";
        }});
    }}

    // Register Service Worker for Full Offline PWA
    if ('serviceWorker' in navigator) {{
      window.addEventListener('load', () => {{
        navigator.serviceWorker.register('/sw.js').then((reg) => {{
          console.log('[KDP Hub] Service Worker registered offline support:', reg.scope);
        }}).catch((err) => {{
          console.log('[KDP Hub] Service Worker registration failed:', err);
        }});
      }});
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      renderApp();
      refreshFromFirebase();
    }});
  </script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('kdp_books_hub.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Successfully generated Master KDP Books Hub (v4.0)!')
