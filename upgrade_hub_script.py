import json
import os

with open('catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Series directory mapping
SERIES_APLUS_MAP = {
    "The Detective's Case Files": "Amazon_A_Plus_Content/01_The_Detectives_Case_Files",
    "Project X": "Amazon_A_Plus_Content/02_Project_X",
    "The Ravencrest Chronicles": "Amazon_A_Plus_Content/03_The_Ravencrest_Chronicles",
    "The Bletchley Protocols": "Amazon_A_Plus_Content/04_The_Bletchley_Protocols",
    "Crypt of the Pharaohs": "Amazon_A_Plus_Content/05_Crypt_of_the_Pharaohs",
    "The Blackwood Asylum Files": "Amazon_A_Plus_Content/06_The_Blackwood_Asylum_Files",
    "The Grand Orient Express": "Amazon_A_Plus_Content/07_The_Grand_Orient_Express"
}

html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>KDP Books Hub - 100-Book Catalog, Fast-Publish & Amazon A+ Content Suite</title>
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
      gap: 8px;
      align-items: center;
    }}
    .btn-pack {{
      display: flex;
      align-items: center;
      gap: 5px;
      font-size: 11px;
      font-weight: 700;
      color: #FFF;
      background: linear-gradient(135deg, #1F6FEB, #238636);
      padding: 6px 12px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.15);
      cursor: pointer;
      text-decoration: none;
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
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
      border-radius: 12px;
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

    /* Action Grid */
    .action-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 10px;
    }}
    .btn-pdf-interior, .btn-pdf-cover, .btn-quick-read, .btn-aplus-toggle {{
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
      background: rgba(0, 0, 0, 0.92);
      backdrop-filter: blur(8px);
      z-index: 9999;
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
      z-index: 10000;
      pointer-events: none;
    }}
    .toast.show {{
      transform: translateX(-50%) translateY(0);
    }}

    /* ZIP Packages Modal */
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
        <div style="font-size:11px; color:var(--text-muted);" id="series-subtitle">100 Master Volumes &bull; Production Ready</div>
      </div>
    </div>
    <div class="header-actions">
      <button class="btn-pack" onclick="openZipModal()">📦 Download ZIPs</button>
      <div class="cloud-status" onclick="refreshFromFirebase()">
        <div class="cloud-dot"></div>
        <span id="cloud-status-text">Cloud Sync (100)</span>
      </div>
    </div>
  </header>

  <div class="top-toolbar">
    <input type="text" id="search-box" class="search-input" placeholder="🔍 Search 100 books by title or keyword..." oninput="handleSearch()">
    <div class="catalog-badge">100 BOOKS</div>
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

  <!-- ZIP Download Modal -->
  <div class="reader-modal" id="zip-modal">
    <div class="reader-header">
      <div class="reader-title">📦 KDP Production Release Packages (.ZIP)</div>
      <button class="reader-close-btn" onclick="closeZipModal()">Close ✕</button>
    </div>
    <div style="padding:16px; overflow-y:auto; flex:1; max-width:600px; margin:0 auto; width:100%;">
      <div style="font-size:12px; color:var(--text-muted); margin-bottom:12px;">
        Download complete print-ready interior PDFs, cover wraps, previews, metadata, and Amazon A+ Content packages:
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

      <!-- MASTER 100-BOOK SUITE -->
      <div class="zip-item" style="border-color:var(--accent); background:rgba(227,179,65,0.08);">
        <div class="zip-info">
          <span class="zip-name" style="color:var(--accent);">🌟 Master 100-Book Catalog Suite</span>
          <span class="zip-sub">All 7 Series • 621 Files • 34.3 MB</span>
        </div>
        <a href="KDP_Production_Packages/Master_100_Book_Catalog_Full_Production_Suite.zip" download class="zip-dl-btn" style="background:var(--accent); color:#000;">Download All</a>
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

    const SERIES_ORDER = [
      "The Detective\'s Case Files",
      "Project X",
      "The Ravencrest Chronicles",
      "The Bletchley Protocols",
      "Crypt of the Pharaohs",
      "The Blackwood Asylum Files",
      "The Grand Orient Express"
    ];

    const SERIES_APLUS_MAP = {json.dumps(SERIES_APLUS_MAP)};

    const firebaseEndpoint = "https://kdp-books-hub-26a1c-default-rtdb.europe-west1.firebasedatabase.app/";
    let currentCatalog = INITIAL_CATALOG;
    let activeSeries = localStorage.getItem('kdp_active_series_100') || SERIES_ORDER[0];
    let activeVolId = null;
    let searchQuery = "";

    function handleSearch() {{
      searchQuery = document.getElementById('search-box').value.trim().toLowerCase();
      renderApp();
    }}

    function getFilteredCatalog() {{
      if (!searchQuery) return currentCatalog;
      return currentCatalog.filter(book => {{
        const titleMatch = (book.title || '').toLowerCase().includes(searchQuery);
        const seriesMatch = (book.series || '').toLowerCase().includes(searchQuery);
        const kwMatch = (book.keywords || []).some(k => k.toLowerCase().includes(searchQuery));
        return titleMatch || seriesMatch || kwMatch;
      }});
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

      // Render Series Bar
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

      // Update Subtitle
      document.getElementById('series-subtitle').textContent = `${{activeSeries}} (${{currentCatalog.filter(b => b.series === activeSeries).length}} Volumes)`;

      // Render Volume Tabs
      tabContainer.innerHTML = '';
      contentContainer.innerHTML = '';
      const vols = getVolumesForActiveSeries();

      if (vols.length === 0) {{
        contentContainer.innerHTML = `<div class="card" style="text-align:center; padding:30px; color:var(--text-muted);">No books found matching "${{escapeHtml(searchQuery)}}".</div>`;
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

          volDiv.innerHTML = `
            <!-- COVER & PDF SHOWCASE HERO CARD -->
            <div class="cover-showcase-card">
              <div class="book-3d-wrap" onclick="openImageModal('${{wrapImg}}?v=luxury_v3', '${{escapeQuotes(book.title)}} - Full Cover Wrap')">
                <img src="${{frontImg}}?v=luxury_v3" class="book-cover-img" alt="${{escapeHtml(book.title)}} Front Cover" onerror="this.onerror=null; this.src='app_icon_1024.png';">
              </div>
              <div class="cover-tap-hint">🔍 Tap cover image to inspect full wrap (Front, Spine & Back)</div>

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

                <!-- Copy Guide Download -->
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

    window.addEventListener('DOMContentLoaded', () => {{
      renderApp();
      refreshFromFirebase();
    }});
  </script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

with open('kdp_books_hub.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print('Successfully upgraded index.html and kdp_books_hub.html with Amazon A+ Content integration!')
