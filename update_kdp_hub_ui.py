"""
update_kdp_hub_ui.py
Generates the next-generation KDP Books Hub with Cover Showcases, PDF Viewers,
and 100-Book Multi-Series Catalog Support.
"""

import os
import json

ROOT_DIR = os.path.abspath(".")
CATALOG_PATH = os.path.join(ROOT_DIR, "catalog.json")

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog_data = json.load(f)

print(f"Loaded {len(catalog_data)} books for KDP Hub UI.")

# Catalog JSON string for inline embedding
catalog_json_str = json.dumps(catalog_data)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>KDP Books Hub - 100-Book Catalog & PDF Reader</title>
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="KDP Hub">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
  <link rel="manifest" href="manifest.json">
  <style>
    :root {
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
    }
    * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
    body {
      margin: 0;
      padding: 16px;
      padding-top: max(16px, env(safe-area-inset-top));
      padding-bottom: max(80px, env(safe-area-inset-bottom));
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }
    .header-left {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .app-logo {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }
    h1 {
      font-size: 18px;
      margin: 0;
      color: var(--accent);
      letter-spacing: 0.5px;
      font-weight: 700;
    }
    .cloud-status {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 600;
      color: var(--accent-blue);
      background: rgba(88, 166, 255, 0.12);
      padding: 5px 10px;
      border-radius: 12px;
      border: 1px solid rgba(88, 166, 255, 0.25);
      cursor: pointer;
    }
    .cloud-dot {
      width: 7px;
      height: 7px;
      background: var(--accent-green);
      border-radius: 50%;
      box-shadow: 0 0 6px var(--accent-green);
    }

    /* Search & Stats Bar */
    .top-toolbar {
      display: flex;
      gap: 8px;
      margin-bottom: 12px;
      align-items: center;
    }
    .search-input {
      flex: 1;
      background: #161B22;
      border: 1px solid var(--border);
      color: var(--text);
      padding: 8px 12px;
      border-radius: 10px;
      font-size: 13px;
      outline: none;
    }
    .search-input:focus {
      border-color: var(--accent);
    }
    .catalog-badge {
      background: rgba(227, 179, 65, 0.15);
      color: var(--accent);
      border: 1px solid rgba(227, 179, 65, 0.3);
      padding: 6px 10px;
      border-radius: 10px;
      font-size: 11px;
      font-weight: 700;
      white-space: nowrap;
    }

    /* Series Selector */
    .series-bar {
      display: flex;
      gap: 8px;
      align-items: center;
      margin-bottom: 10px;
      overflow-x: auto;
      padding-bottom: 4px;
      -webkit-overflow-scrolling: touch;
    }
    .series-bar::-webkit-scrollbar { display: none; }
    .series-pill {
      padding: 7px 14px;
      font-size: 12px;
      font-weight: 600;
      background: #21262D;
      border: 1px solid var(--border);
      color: var(--text-muted);
      border-radius: 20px;
      white-space: nowrap;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s;
    }
    .series-pill.active {
      background: rgba(227, 179, 65, 0.2);
      color: var(--accent);
      border-color: var(--accent);
    }

    /* Volume Tabs */
    .tab-bar {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 8px;
      margin-bottom: 14px;
      -webkit-overflow-scrolling: touch;
    }
    .tab-bar::-webkit-scrollbar { display: none; }
    .tab-btn {
      white-space: nowrap;
      padding: 9px 14px;
      font-size: 12px;
      font-weight: 600;
      background: var(--card-bg);
      border: 1px solid var(--border);
      color: var(--text-muted);
      border-radius: 10px;
      cursor: pointer;
      text-align: center;
      transition: all 0.2s;
    }
    .tab-btn.active {
      background: var(--accent);
      color: #000;
      border-color: var(--accent);
      font-weight: 700;
    }

    /* Cards */
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px;
      margin-bottom: 12px;
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }
    .label {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--accent);
      letter-spacing: 0.5px;
    }
    .copy-btn {
      background: #21262D;
      border: 1px solid var(--border);
      color: var(--text);
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: background 0.15s;
    }
    .copy-btn:active {
      background: var(--accent-green);
      color: #fff;
    }
    .val-box {
      font-size: 13px;
      line-height: 1.45;
      color: var(--text);
      word-break: break-word;
      background: rgba(0,0,0,0.25);
      padding: 10px;
      border-radius: 8px;
      border: 1px solid rgba(255,255,255,0.06);
    }
    .kw-grid {
      display: grid;
      gap: 8px;
    }
    .kw-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(0,0,0,0.25);
      padding: 8px 10px;
      border-radius: 8px;
      font-size: 12px;
    }

    /* --- COVER & PDF SHOWCASE STYLES --- */
    .cover-showcase-card {
      background: linear-gradient(180deg, #161B22 0%, #0D1117 100%);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 16px;
      margin-bottom: 14px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    }
    .book-3d-wrap {
      perspective: 1000px;
      margin: 10px 0 16px 0;
      cursor: pointer;
    }
    .book-cover-img {
      width: 200px;
      height: 300px;
      object-fit: cover;
      border-radius: 8px;
      box-shadow: 0 12px 32px rgba(0,0,0,0.7), -4px 0 10px rgba(255,255,255,0.1) inset;
      border: 2px solid rgba(227, 179, 65, 0.4);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .book-cover-img:hover {
      transform: scale(1.03) rotateY(-5deg);
      box-shadow: 0 16px 40px rgba(227, 179, 65, 0.3);
    }
    .cover-tap-hint {
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 6px;
    }
    .badge-bar {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 6px;
      margin: 8px 0 14px 0;
    }
    .badge {
      font-size: 10px;
      font-weight: 700;
      padding: 4px 8px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.4px;
    }
    .badge-gold { background: rgba(227, 179, 65, 0.15); color: var(--accent); border: 1px solid rgba(227, 179, 65, 0.3); }
    .badge-green { background: rgba(46, 160, 67, 0.15); color: #3FB950; border: 1px solid rgba(46, 160, 67, 0.3); }
    .badge-blue { background: rgba(88, 166, 255, 0.15); color: var(--accent-blue); border: 1px solid rgba(88, 166, 255, 0.3); }
    .badge-purple { background: rgba(188, 140, 255, 0.15); color: var(--accent-purple); border: 1px solid rgba(188, 140, 255, 0.3); }

    /* PDF Action Buttons */
    .action-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 10px;
      width: 100%;
      margin-top: 6px;
    }
    @media (min-width: 480px) {
      .action-grid {
        grid-template-columns: 1fr 1fr;
      }
    }
    .btn-pdf-interior {
      background: linear-gradient(135deg, #1F6FEB 0%, #1158C7 100%);
      color: #FFFFFF;
      text-decoration: none;
      padding: 12px 14px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 4px 14px rgba(31, 111, 235, 0.35);
      border: 1px solid rgba(255, 255, 255, 0.15);
      transition: all 0.2s;
    }
    .btn-pdf-interior:active {
      transform: scale(0.98);
      background: #1158C7;
    }
    .btn-pdf-cover {
      background: linear-gradient(135deg, #E3B341 0%, #C9971D 100%);
      color: #000000;
      text-decoration: none;
      padding: 12px 14px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 4px 14px rgba(227, 179, 65, 0.35);
      border: 1px solid rgba(0, 0, 0, 0.1);
      transition: all 0.2s;
    }
    .btn-pdf-cover:active {
      transform: scale(0.98);
    }
    .btn-quick-read {
      background: #21262D;
      color: var(--text);
      border: 1px solid var(--accent-purple);
      padding: 10px 14px;
      border-radius: 10px;
      font-size: 12px;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      cursor: pointer;
      width: 100%;
      margin-top: 8px;
    }
    .btn-quick-read:active {
      background: rgba(188, 140, 255, 0.15);
    }

    /* Modal PDF Viewer & Image Viewer */
    .reader-modal {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.95);
      z-index: 10000;
      flex-direction: column;
    }
    .reader-modal.open {
      display: flex;
    }
    .reader-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 16px;
      background: #161B22;
      border-bottom: 1px solid var(--border);
    }
    .reader-title {
      font-size: 13px;
      font-weight: 700;
      color: var(--accent);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 65%;
    }
    .reader-actions {
      display: flex;
      gap: 8px;
    }
    .reader-close-btn {
      background: #21262D;
      border: 1px solid var(--border);
      color: #fff;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
    }
    .reader-body {
      flex: 1;
      width: 100%;
      height: 100%;
      overflow: auto;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #0B0E14;
    }
    .reader-iframe {
      width: 100%;
      height: 100%;
      border: none;
    }
    .reader-img {
      max-width: 95%;
      max-height: 90vh;
      object-fit: contain;
      box-shadow: 0 0 30px rgba(0,0,0,0.8);
      border-radius: 4px;
    }

    /* Toast */
    .toast {
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%) translateY(100px);
      background: #238636;
      color: #fff;
      padding: 10px 20px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
      transition: transform 0.25s ease-out;
      z-index: 10001;
    }
    .toast.show {
      transform: translateX(-50%) translateY(0);
    }
  </style>
</head>
<body>

  <header>
    <div class="header-left">
      <img src="logo_header.png" class="app-logo" alt="KDP Hub Logo">
      <div>
        <h1>KDP BOOKS HUB</h1>
        <div style="font-size:11px; color:var(--text-muted);" id="series-subtitle">The Detective's Case Files</div>
      </div>
    </div>
    <div class="cloud-status" onclick="refreshFromFirebase()">
      <div class="cloud-dot"></div>
      <span id="cloud-status-text">Cloud Sync (100)</span>
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
    <div class="reader-body" id="reader-body">
      <!-- Injected iframe or image -->
    </div>
  </div>

  <div id="toast" class="toast">Copied to clipboard! ✓</div>

  <script>
    const INITIAL_CATALOG = """ + catalog_json_str + """;
    let firebaseEndpoint = "https://kdp-books-hub-26a1c-default-rtdb.europe-west1.firebasedatabase.app/";
    let currentCatalog = JSON.parse(localStorage.getItem('kdp_catalog_cache_100') || 'null') || INITIAL_CATALOG;
    
    // Series & Volume Selection State
    let activeSeries = localStorage.getItem('kdp_active_series_100') || "The Detective's Case Files";
    let activeVolId = null;
    let searchQuery = "";

    function getSeriesList() {
      const set = new Set();
      currentCatalog.forEach(b => set.add(b.series || "The Detective's Case Files"));
      return Array.from(set);
    }

    function getVolumesForActiveSeries() {
      return currentCatalog.filter(b => {
        const matchesSeries = (b.series || "The Detective's Case Files") === activeSeries;
        if (!searchQuery) return matchesSeries;
        const q = searchQuery.toLowerCase();
        const matchesQuery = (b.title && b.title.toLowerCase().includes(q)) ||
                             (b.subtitle && b.subtitle.toLowerCase().includes(q)) ||
                             (b.keywords && b.keywords.some(k => k.toLowerCase().includes(q)));
        return matchesSeries && matchesQuery;
      });
    }

    function handleSearch() {
      searchQuery = document.getElementById('search-box').value.trim();
      renderApp();
    }

    function renderApp() {
      const seriesBar = document.getElementById('series-bar');
      const tabContainer = document.getElementById('tab-container');
      const contentContainer = document.getElementById('content-container');
      const seriesList = getSeriesList();

      // Render Series Pills
      seriesBar.innerHTML = '';
      seriesList.forEach(sName => {
        const pill = document.createElement('div');
        pill.className = `series-pill ${sName === activeSeries ? 'active' : ''}`;
        const count = currentCatalog.filter(b => (b.series || "The Detective's Case Files") === sName).length;
        
        let icon = "📚";
        if (sName.includes("Detective")) icon = "🕵️‍♂️";
        else if (sName.includes("Project X")) icon = "🚀";
        else if (sName.includes("Ravencrest")) icon = "🏰";
        else if (sName.includes("Bletchley")) icon = "📻";
        else if (sName.includes("Pharaoh")) icon = "🏺";
        else if (sName.includes("Asylum")) icon = "🏥";
        else if (sName.includes("Express")) icon = "🚂";

        pill.textContent = `${icon} ${sName} (${count})`;
        pill.onclick = () => {
          activeSeries = sName;
          localStorage.setItem('kdp_active_series_100', activeSeries);
          const vols = getVolumesForActiveSeries();
          activeVolId = vols[0] ? vols[0].id : null;
          renderApp();
        };
        seriesBar.appendChild(pill);
      });

      // Update Subtitle
      document.getElementById('series-subtitle').textContent = `${activeSeries} (${currentCatalog.filter(b => b.series === activeSeries).length} Volumes)`;

      // Render Volume Tabs
      tabContainer.innerHTML = '';
      contentContainer.innerHTML = '';
      const vols = getVolumesForActiveSeries();

      if (vols.length === 0) {
        contentContainer.innerHTML = `<div class="card" style="text-align:center; padding:30px; color:var(--text-muted);">No books found matching "${escapeHtml(searchQuery)}".</div>`;
        return;
      }

      if (!activeVolId || !vols.some(v => v.id === activeVolId)) {
        activeVolId = vols[0].id;
      }

      vols.forEach((book) => {
        const btn = document.createElement('button');
        btn.className = `tab-btn ${book.id === activeVolId ? 'active' : ''}`;
        btn.textContent = book.tab_name || `Volume ${book.vol_number}`;
        btn.onclick = () => {
          activeVolId = book.id;
          renderApp();
        };
        tabContainer.appendChild(btn);

        if (book.id === activeVolId) {
          const volDiv = document.createElement('div');

          // Fallback URLs
          const interiorPdf = book.pdf_interior_url || `${book.series}/${book.id}/interior_6x9.pdf`;
          const coverPdf = book.pdf_cover_url || `${book.series}/${book.id}/cover_wrap_6x9.pdf`;
          const frontImg = book.cover_img_url || `${book.series}/${book.id}/cover_front_preview.png`;
          const wrapImg = book.cover_wrap_img_url || `${book.series}/${book.id}/cover_wrap_preview.png`;

          volDiv.innerHTML = `
            <!-- COVER & PDF SHOWCASE HERO CARD -->
            <div class="cover-showcase-card">
              <div class="book-3d-wrap" onclick="openImageModal('${wrapImg}?v=luxury_v2', '${escapeQuotes(book.title)} - Full Cover Wrap')">
                <img src="${frontImg}?v=luxury_v2" class="book-cover-img" alt="${escapeHtml(book.title)} Front Cover" onerror="this.onerror=null; this.src='app_icon_1024.png';">
              </div>
              <div class="cover-tap-hint">🔍 Tap cover to view full-wrap cover (Front, Spine & Back)</div>

              <div class="badge-bar">
                <span class="badge badge-gold">VOLUME ${book.vol_number}</span>
                <span class="badge badge-green">176 PAGES • 6" × 9"</span>
                <span class="badge badge-blue">PROFIT: $${book.royalty_usd || '4.68'}/SALE</span>
                <span class="badge badge-purple">100% UNIQUE LOGIC</span>
              </div>

              <!-- ONE-TAP PDF BUTTONS -->
              <div class="action-grid">
                <a href="${interiorPdf}" target="_blank" class="btn-pdf-interior">
                  📖 Open Interior PDF (176 Pgs)
                </a>
                <a href="${coverPdf}" target="_blank" class="btn-pdf-cover">
                  🎨 View Cover Wrap PDF
                </a>
              </div>

              <button class="btn-quick-read" onclick="openPdfModal('${interiorPdf}', '${escapeQuotes(book.title)}')">
                👁️ In-App PDF Quick Reader
              </button>
            </div>

            <!-- METADATA CARDS -->
            <div class="card">
              <div class="card-header">
                <span class="label">Book Title</span>
                <button class="copy-btn" onclick="copyText('${escapeQuotes(book.title)}')">📋 Copy</button>
              </div>
              <div class="val-box">${book.title}</div>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="label">Subtitle</span>
                <button class="copy-btn" onclick="copyText('${escapeQuotes(book.subtitle)}')">📋 Copy</button>
              </div>
              <div class="val-box">${book.subtitle}</div>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="label">Pricing & Author Royalty</span>
                <button class="copy-btn" onclick="copyText('${book.price_usd}')">Copy Price ($${book.price_usd})</button>
              </div>
              <div class="val-box">
                <b>List Price:</b> $${book.price_usd} USD &nbsp;|&nbsp; 
                <b>KDP Print Cost:</b> $${book.print_cost_usd || '3.11'} &nbsp;|&nbsp; 
                <b style="color:#3FB950;">Your Royalty (60%):</b> $${book.royalty_usd || '4.68'} USD per copy
              </div>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="label">Print & Binding Specifications</span>
                <button class="copy-btn" onclick="copyText('6x9 in, 176 pages, Black and White, No Bleed, Matte')">📋 Copy Specs</button>
              </div>
              <div class="val-box">
                <b>Trim Size:</b> ${book.trim || '6" x 9"'} &nbsp;|&nbsp; 
                <b>Page Count:</b> ${book.pages || 176} pages &nbsp;|&nbsp; 
                <b>Spine Width:</b> 0.396 in (10.06 mm)<br>
                <b>Interior:</b> Black & White on White Paper &nbsp;|&nbsp; 
                <b>Bleed:</b> ${book.bleed || 'No Bleed'} &nbsp;|&nbsp; 
                <b>Cover Finish:</b> Matte
              </div>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="label">7 Backend Search Keywords</span>
                <button class="copy-btn" onclick="copyAllKeywords('${escapeQuotes((book.keywords || []).join(', '))}')">📋 Copy All 7</button>
              </div>
              <div class="kw-grid">
                ${(book.keywords || []).map((kw, i) => `
                  <div class="kw-item">
                    <span>${i+1}. ${kw}</span>
                    <button class="copy-btn" onclick="copyText('${escapeQuotes(kw)}')">Copy</button>
                  </div>
                `).join('')}
              </div>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="label">3 Amazon KDP Categories</span>
                <button class="copy-btn" onclick="copyAllKeywords('${escapeQuotes((book.categories || []).join('\\n'))}')">📋 Copy Categories</button>
              </div>
              <div class="val-box">
                ${(book.categories || []).map(cat => `• ${cat}`).join('<br>')}
              </div>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="label">HTML Product Description</span>
                <button class="copy-btn" onclick="copyDesc('desc-box-${book.id}')">📋 Copy HTML</button>
              </div>
              <div id="desc-box-${book.id}" class="val-box" style="font-size:11px; max-height:120px; overflow-y:auto; white-space:pre-wrap;">${escapeHtml(book.description_html)}</div>
            </div>
          `;
          contentContainer.appendChild(volDiv);
        }
      });
    }

    function openPdfModal(pdfUrl, title) {
      const modal = document.getElementById('reader-modal');
      const body = document.getElementById('reader-body');
      const titleElem = document.getElementById('reader-title');
      const extBtn = document.getElementById('reader-external-btn');

      titleElem.textContent = title;
      extBtn.href = pdfUrl;
      body.innerHTML = `<iframe class="reader-iframe" src="${pdfUrl}"></iframe>`;
      modal.classList.add('open');
    }

    function openImageModal(imgUrl, title) {
      const modal = document.getElementById('reader-modal');
      const body = document.getElementById('reader-body');
      const titleElem = document.getElementById('reader-title');
      const extBtn = document.getElementById('reader-external-btn');

      titleElem.textContent = title;
      extBtn.href = imgUrl;
      body.innerHTML = `<img src="${imgUrl}" class="reader-img" alt="Cover Wrap Preview">`;
      modal.classList.add('open');
    }

    function closeReaderModal() {
      const modal = document.getElementById('reader-modal');
      const body = document.getElementById('reader-body');
      modal.classList.remove('open');
      body.innerHTML = '';
    }

    function escapeQuotes(str) {
      return (str || '').replace(/'/g, "\\'").replace(/"/g, '&quot;');
    }

    function escapeHtml(str) {
      return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    function showToast(msg) {
      const toast = document.getElementById('toast');
      toast.textContent = msg || 'Copied to clipboard! ✓';
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 1600);
    }

    function copyText(txt) {
      navigator.clipboard.writeText(txt).then(() => showToast('Copied! ✓'));
    }

    function copyAllKeywords(allKw) {
      copyText(allKw);
    }

    function copyDesc(elemId) {
      const elem = document.getElementById(elemId);
      if (elem) {
        copyText(elem.innerText);
      }
    }

    function refreshFromFirebase() {
      const statusText = document.getElementById('cloud-status-text');
      statusText.textContent = "Syncing...";
      fetch(firebaseEndpoint + "catalog.json?t=" + Date.now())
        .then(res => res.json())
        .then(data => {
          if (data && Array.isArray(data)) {
            currentCatalog = data;
            localStorage.setItem('kdp_catalog_cache_100', JSON.stringify(data));
            statusText.textContent = `Cloud Sync (${data.length})`;
            showToast(`Synced ${data.length} books from Cloud! ✓`);
            renderApp();
          } else {
            statusText.textContent = "Sync Failed";
          }
        })
        .catch(err => {
          console.error("Firebase sync error:", err);
          statusText.textContent = "Offline Cache";
          showToast("Using local offline cache ✓");
        });
    }

    // Auto-fetch on boot
    window.addEventListener('DOMContentLoaded', () => {
      renderApp();
      refreshFromFirebase();
    });
  </script>
</body>
</html>
"""

# Write to root kdp_books_hub.html
root_hub_path = os.path.join(ROOT_DIR, "kdp_books_hub.html")
with open(root_hub_path, "w", encoding="utf-8") as f:
    f.write(html_template)

# Also write to The_Detectives_Case_Files_Series/kdp_books_hub.html
series_hub_path = os.path.join(ROOT_DIR, "The_Detectives_Case_Files_Series", "kdp_books_hub.html")
with open(series_hub_path, "w", encoding="utf-8") as f:
    f.write(html_template)

# Also update index.html to serve kdp_books_hub.html directly
index_path = os.path.join(ROOT_DIR, "index.html")
with open(index_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print("[✓] Upgraded KDP Books Hub UI successfully written to:")
print(f"    - {root_hub_path}")
print(f"    - {series_hub_path}")
print(f"    - {index_path}")
