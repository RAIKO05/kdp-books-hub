"""
sync_hub.py (v4.0 - Multi-Series & Bi-Directional Cloud Engine)
Generates the native-ready mobile app with:
- Multi-Book Series & Multi-Volume hierarchy
- In-App "Add New Book / Volume" modal with real-time cloud publishing
- Direct two-way sync with Google Cloud Firebase & GitHub Cloud
- 1-Tap Copy buttons optimized for mobile KDP copy-pasting
- iOS native PWA & IPA viewport compatibility
"""

import json
import os

SERIES_DIR = "The_Detectives_Case_Files_Series"
CATALOG_PATH = os.path.join(SERIES_DIR, "catalog.json")
CONFIG_PATH = os.path.join(SERIES_DIR, "cloud_config.json")
HTML_OUTPUT = os.path.join(SERIES_DIR, "kdp_books_hub.html")

def build_hub_html():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    firebase_url = ""
    github_url = ""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            firebase_url = cfg.get("firebase_url", "")
            github_url = cfg.get("github_url", "")

    catalog_json_str = json.dumps(catalog)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>KDP Books Hub</title>
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="KDP Hub">
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
    }}
    h1 {{
      font-size: 19px;
      margin: 0;
      color: var(--accent);
      letter-spacing: 0.5px;
    }}
    .cloud-status {{
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
    }}
    .cloud-dot {{
      width: 7px;
      height: 7px;
      background: var(--accent-blue);
      border-radius: 50%;
      box-shadow: 0 0 6px var(--accent-blue);
    }}
    
    /* Series Selector */
    .series-bar {{
      display: flex;
      gap: 8px;
      align-items: center;
      margin-bottom: 10px;
      overflow-x: auto;
      padding-bottom: 4px;
      -webkit-overflow-scrolling: touch;
    }}
    .series-bar::-webkit-scrollbar {{ display: none; }}
    .series-pill {{
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 600;
      background: #21262D;
      border: 1px solid var(--border);
      color: var(--text-muted);
      border-radius: 20px;
      white-space: nowrap;
      cursor: pointer;
    }}
    .series-pill.active {{
      background: rgba(227, 179, 65, 0.2);
      color: var(--accent);
      border-color: var(--accent);
    }}

    /* Volume Tabs */
    .tab-bar {{
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 8px;
      margin-bottom: 14px;
      -webkit-overflow-scrolling: touch;
    }}
    .tab-bar::-webkit-scrollbar {{ display: none; }}
    .tab-btn {{
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
    }}
    .tab-btn.active {{
      background: var(--accent);
      color: #000;
      border-color: var(--accent);
    }}
    .add-btn {{
      background: #238636;
      border: 1px solid #2ea043;
      color: #fff;
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
      font-weight: 700;
      text-transform: uppercase;
      color: var(--accent);
      letter-spacing: 0.5px;
    }}
    .copy-btn {{
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
    }}
    .copy-btn:active {{
      background: var(--accent-green);
      color: #fff;
    }}
    .val-box {{
      font-size: 13px;
      line-height: 1.4;
      color: var(--text);
      word-break: break-word;
      background: rgba(0,0,0,0.25);
      padding: 10px;
      border-radius: 8px;
      border: 1px solid rgba(255,255,255,0.06);
    }}
    .kw-grid {{
      display: grid;
      gap: 8px;
    }}
    .kw-item {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(0,0,0,0.25);
      padding: 8px 10px;
      border-radius: 8px;
      font-size: 12px;
    }}

    /* Toast */
    .toast {{
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
      z-index: 9999;
    }}
    .toast.show {{
      transform: translateX(-50%) translateY(0);
    }}

    /* Floating Action Button */
    .fab {{
      position: fixed;
      bottom: max(20px, env(safe-area-inset-bottom));
      right: 20px;
      width: 52px;
      height: 52px;
      border-radius: 26px;
      background: var(--accent);
      color: #000;
      font-size: 26px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 16px rgba(227, 179, 65, 0.4);
      cursor: pointer;
      border: none;
      font-weight: 700;
      z-index: 100;
    }}

    /* Modal Form */
    .modal-overlay {{
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0,0,0,0.75);
      z-index: 200;
      align-items: flex-end;
    }}
    .modal-overlay.open {{ display: flex; }}
    .modal-content {{
      background: #161B22;
      width: 100%;
      max-height: 85vh;
      border-top-left-radius: 20px;
      border-top-right-radius: 20px;
      padding: 20px;
      overflow-y: auto;
      border: 1px solid var(--border);
    }}
    .modal-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }}
    .modal-title {{
      font-size: 16px;
      font-weight: 700;
      color: var(--accent);
    }}
    .close-btn {{
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 22px;
      cursor: pointer;
    }}
    .form-group {{
      margin-bottom: 14px;
    }}
    .form-group label {{
      display: block;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-bottom: 6px;
    }}
    .form-control {{
      width: 100%;
      background: #0D1117;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px;
      font-size: 13px;
      color: var(--text);
      box-sizing: border-box;
      outline: none;
    }}
    .form-control:focus {{
      border-color: var(--accent);
    }}
    .submit-btn {{
      width: 100%;
      background: var(--accent-green);
      color: #fff;
      font-weight: 700;
      padding: 12px;
      font-size: 14px;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      margin-top: 10px;
    }}
  </style>
</head>
<body>
  <header>
    <div>
      <h1>KDP Books Hub</h1>
      <span id="series-subtitle" style="font-size:11px; color:var(--text-muted);">Multi-Book & Multi-Volume Organizer</span>
    </div>
    <div class="cloud-status" onclick="promptCloudSettings()">
      <div class="cloud-dot"></div>
      <span id="cloud-label">Hybrid: Syncing...</span>
    </div>
  </header>

  <!-- Series Navigation Pills -->
  <div class="series-bar" id="series-bar"></div>

  <!-- Volume Sub-Navigation Tabs -->
  <div class="tab-bar" id="tab-container"></div>

  <!-- Book Details Cards -->
  <div id="content-container"></div>

  <!-- Add Book FAB -->
  <button class="fab" onclick="openAddModal()">+</button>

  <!-- Toast Notification -->
  <div id="toast" class="toast">Copied to clipboard! ✓</div>

  <!-- Add Book / Volume Modal Sheet -->
  <div id="add-modal" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <span class="modal-title">➕ Add Book / New Volume</span>
        <button class="close-btn" onclick="closeAddModal()">×</button>
      </div>

      <div class="form-group">
        <label>Series / Project Name</label>
        <input type="text" id="m-series" class="form-control" list="series-options" placeholder="e.g. The Detective's Case Files">
        <datalist id="series-options"></datalist>
      </div>

      <div style="display:flex; gap:10px;">
        <div class="form-group" style="flex:1;">
          <label>Volume #</label>
          <input type="number" id="m-vol" class="form-control" placeholder="e.g. 4">
        </div>
        <div class="form-group" style="flex:2;">
          <label>Tab Label</label>
          <input type="text" id="m-tab" class="form-control" placeholder="e.g. Vol 4 (Highland)">
        </div>
      </div>

      <div class="form-group">
        <label>Full Book Title</label>
        <input type="text" id="m-title" class="form-control" placeholder="e.g. Case Files & Clues: Volume 4">
      </div>

      <div class="form-group">
        <label>Subtitle</label>
        <input type="text" id="m-subtitle" class="form-control" placeholder="e.g. 35 Murder Mystery Logic Puzzles...">
      </div>

      <div class="form-group">
        <label>7 Keywords (One per line or comma-separated)</label>
        <textarea id="m-keywords" class="form-control" rows="3" placeholder="Keyword 1&#10;Keyword 2&#10;Keyword 3..."></textarea>
      </div>

      <div class="form-group">
        <label>HTML Description</label>
        <textarea id="m-desc" class="form-control" rows="4" placeholder="<h2>Your Catchy Headline</h2>&#10;<p>Book summary...</p>"></textarea>
      </div>

      <div style="display:flex; gap:10px;">
        <div class="form-group" style="flex:1;">
          <label>List Price ($)</label>
          <input type="text" id="m-price" class="form-control" value="12.99">
        </div>
        <div class="form-group" style="flex:1;">
          <label>Print Cost ($)</label>
          <input type="text" id="m-print" class="form-control" value="3.11">
        </div>
        <div class="form-group" style="flex:1;">
          <label>Cover Palette</label>
          <input type="text" id="m-cover" class="form-control" value="Royal Sapphire & Gold">
        </div>
      </div>

      <button class="submit-btn" onclick="saveNewBook()">💾 Save & Push to Cloud (100% Sync)</button>
    </div>
  </div>

  <script>
    const INITIAL_CATALOG = {catalog_json_str};
    let firebaseEndpoint = localStorage.getItem('kdp_firebase_url') || "{firebase_url}";
    let githubEndpoint = localStorage.getItem('kdp_github_url') || "{github_url}";

    let currentCatalog = JSON.parse(localStorage.getItem('kdp_catalog_cache') || 'null') || INITIAL_CATALOG;
    
    // Series & Volume Selection State
    let activeSeries = localStorage.getItem('kdp_active_series') || (currentCatalog[0] ? (currentCatalog[0].series || "The Detective's Case Files") : "The Detective's Case Files");
    let activeVolId = null;

    function getSeriesList() {{
      const set = new Set();
      currentCatalog.forEach(b => set.add(b.series || "The Detective's Case Files"));
      return Array.from(set);
    }}

    function getVolumesForActiveSeries() {{
      return currentCatalog.filter(b => (b.series || "The Detective's Case Files") === activeSeries);
    }}

    function renderApp() {{
      const seriesBar = document.getElementById('series-bar');
      const tabContainer = document.getElementById('tab-container');
      const contentContainer = document.getElementById('content-container');
      const seriesList = getSeriesList();

      // Render Series Pills
      seriesBar.innerHTML = '';
      seriesList.forEach(sName => {{
        const pill = document.createElement('div');
        pill.className = `series-pill ${{sName === activeSeries ? 'active' : ''}}`;
        const count = currentCatalog.filter(b => (b.series || "The Detective's Case Files") === sName).length;
        pill.textContent = `${{sName}} (${{count}})`;
        pill.onclick = () => {{
          activeSeries = sName;
          localStorage.setItem('kdp_active_series', activeSeries);
          const vols = getVolumesForActiveSeries();
          activeVolId = vols[0] ? vols[0].id : null;
          renderApp();
        }};
        seriesBar.appendChild(pill);
      }});

      // Update Subtitle
      document.getElementById('series-subtitle').textContent = `${{activeSeries}}`;

      // Render Volume Tabs
      tabContainer.innerHTML = '';
      contentContainer.innerHTML = '';
      const vols = getVolumesForActiveSeries();

      if (!activeVolId && vols.length > 0) {{
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
          volDiv.innerHTML = `
            <div class="card">
              <div class="card-header">
                <span class="label">Book Title</span>
                <button class="copy-btn" onclick="copyText('${{escapeQuotes(book.title)}}')">📋 Copy</button>
              </div>
              <div class="val-box">${{book.title}}</div>
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
                <span class="label">7 Backend Keywords (Tap to Copy)</span>
              </div>
              <div class="kw-grid">
                ${{(book.keywords || []).map((kw, i) => `
                  <div class="kw-item">
                    <span>${{i+1}}. ${{kw}}</span>
                    <button class="copy-btn" onclick="copyText('${{escapeQuotes(kw)}}')">Copy</button>
                  </div>
                `).join('')}}
              </div>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="label">HTML Description</span>
                <button class="copy-btn" onclick="copyDesc('desc-box-${{book.id}}')">📋 Copy HTML</button>
              </div>
              <div id="desc-box-${{book.id}}" class="val-box" style="font-size:11px; max-height:110px; overflow-y:auto; white-space:pre-wrap;">${{escapeHtml(book.description_html)}}</div>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="label">Pricing & Print Specifications</span>
                <button class="copy-btn" onclick="copyText('${{book.price_usd}}')">Copy Price ($${{book.price_usd}})</button>
              </div>
              <div class="val-box">
                <b>Trim:</b> ${{book.trim || '6" x 9"'}} | <b>Pages:</b> ${{book.pages || 176}} | <b>Bleed:</b> ${{book.bleed || 'No Bleed'}}<br>
                <b>Cover Theme:</b> ${{book.cover_palette || 'Classic'}}<br>
                <b>Retail Price:</b> $${{book.price_usd}} USD | <b>Print Cost:</b> $${{book.print_cost_usd || '3.11'}} | <b>Your Royalty:</b> $${{book.royalty_usd || '4.68'}}
              </div>
            </div>
          `;
          contentContainer.appendChild(volDiv);
        }}
      }});
    }}

    function escapeQuotes(str) {{
      return (str || '').replace(/'/g, "\\\\'").replace(/"/g, '&quot;');
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

    function copyDesc(elemId) {{
      const elem = document.getElementById(elemId);
      navigator.clipboard.writeText(elem.innerText).then(() => showToast('HTML Description Copied! ✓'));
    }}

    function openAddModal() {{
      const modal = document.getElementById('add-modal');
      const datalist = document.getElementById('series-options');
      datalist.innerHTML = '';
      getSeriesList().forEach(s => {{
        const opt = document.createElement('option');
        opt.value = s;
        datalist.appendChild(opt);
      }});

      document.getElementById('m-series').value = activeSeries;
      const vols = getVolumesForActiveSeries();
      document.getElementById('m-vol').value = vols.length + 1;
      document.getElementById('m-tab').value = `Vol ${{vols.length + 1}}`;
      modal.classList.add('open');
    }}

    function closeAddModal() {{
      document.getElementById('add-modal').classList.remove('open');
    }}

    async function saveNewBook() {{
      const series = document.getElementById('m-series').value.trim() || "Independent Series";
      const volNum = parseInt(document.getElementById('m-vol').value.trim()) || 1;
      const tabName = document.getElementById('m-tab').value.trim() || `Volume ${{volNum}}`;
      const title = document.getElementById('m-title').value.trim();
      const subtitle = document.getElementById('m-subtitle').value.trim();
      const rawKw = document.getElementById('m-keywords').value.trim();
      const desc = document.getElementById('m-desc').value.trim();
      const price = document.getElementById('m-price').value.trim() || "12.99";
      const printCost = document.getElementById('m-print').value.trim() || "3.11";
      const cover = document.getElementById('m-cover').value.trim() || "Gold & Velvet";

      if (!title) {{
        alert("Please enter a Book Title.");
        return;
      }}

      const keywords = rawKw.split(/[\\r\\n,]+/).map(k => k.trim()).filter(k => k.length > 0);
      const royalty = ((parseFloat(price) * 0.60) - parseFloat(printCost)).toFixed(2);
      const bookId = `vol_${{Date.now()}}`;

      const newBook = {{
        id: bookId,
        vol_number: volNum,
        tab_name: tabName,
        title: title,
        subtitle: subtitle,
        series: series,
        price_usd: price,
        print_cost_usd: printCost,
        royalty_usd: royalty,
        trim: '6" x 9"',
        pages: 176,
        bleed: 'No Bleed',
        cover_palette: cover,
        keywords: keywords,
        categories: [
          "Crafts, Hobbies & Home > Crafts & Hobbies > Activity Books",
          "Humor & Entertainment > Puzzles & Games > Logic & Brain Teasers",
          "Mystery, Thriller & Suspense > Mystery > Traditional Detective"
        ],
        description_html: desc || `<p>${{subtitle}}</p>`
      }};

      currentCatalog.push(newBook);
      localStorage.setItem('kdp_catalog_cache', JSON.stringify(currentCatalog));
      activeSeries = series;
      activeVolId = bookId;
      closeAddModal();
      renderApp();
      showToast('Book Added Locally! Pushing to Cloud...');

      // 100% TWO-WAY SYNC: Push immediately to Google Cloud Firebase
      if (firebaseEndpoint) {{
        let targetUrl = firebaseEndpoint.replace(/\\/+$/, '');
        if (!targetUrl.endsWith('/catalog.json')) targetUrl += '/catalog.json';
        try {{
          const res = await fetch(targetUrl, {{
            method: 'PUT',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify(currentCatalog)
          }});
          if (res.ok) {{
            showToast('100% Synced to Google Cloud! ☁️✓');
          }}
        }} catch(e) {{
          console.error("Cloud push failed:", e);
        }}
      }}
    }}

    function promptCloudSettings() {{
      const choice = prompt("HYBRID CLOUD SETTINGS:\\nEnter '1' for Google Cloud (Firebase)\\nEnter '2' for GitHub Cloud (Raw CDN)", "1");
      if (choice === "1") {{
        const entered = prompt("Google Cloud Firebase Realtime Database URL:", firebaseEndpoint);
        if (entered !== null) {{
          firebaseEndpoint = entered.trim();
          localStorage.setItem('kdp_firebase_url', firebaseEndpoint);
          fetchCloudData();
        }}
      }} else if (choice === "2") {{
        const entered = prompt("GitHub Cloud Raw Catalog URL (raw.githubusercontent.com/...):", githubEndpoint);
        if (entered !== null) {{
          githubEndpoint = entered.trim();
          localStorage.setItem('kdp_github_url', githubEndpoint);
          fetchCloudData();
        }}
      }}
    }}

    // DUAL-ENGINE HYBRID AUTO-SYNC
    async function fetchCloudData() {{
      let data = null;
      let activeSource = "";

      // 1. Google Cloud Firebase
      if (firebaseEndpoint) {{
        let targetUrl = firebaseEndpoint.replace(/\\/+$/, '');
        if (!targetUrl.endsWith('/catalog.json')) targetUrl += '/catalog.json';
        try {{
          const res = await fetch(targetUrl + '?t=' + Date.now());
          if (res.ok) {{
            data = await res.json();
            activeSource = githubEndpoint ? "Hybrid: Google ☁️ + GitHub 🐙" : "Google Cloud ☁️";
          }}
        }} catch(e) {{
          console.warn("Google Cloud connection failed, attempting GitHub fallback...", e);
        }}
      }}

      // 2. GitHub Cloud Fallback
      if (!data && githubEndpoint) {{
        try {{
          const res = await fetch(githubEndpoint + '?t=' + Date.now());
          if (res.ok) {{
            data = await res.json();
            activeSource = "GitHub Cloud 🐙";
          }}
        }} catch(e) {{
          console.warn("GitHub Cloud fallback failed...", e);
        }}
      }}

      if (data && Array.isArray(data)) {{
        document.getElementById('cloud-label').textContent = activeSource;
        if (JSON.stringify(data) !== JSON.stringify(currentCatalog)) {{
          currentCatalog = data;
          localStorage.setItem('kdp_catalog_cache', JSON.stringify(data));
          renderApp();
          showToast(`Auto-synced from ${{activeSource}}!`);
        }}
      }} else if (!data && currentCatalog) {{
        document.getElementById('cloud-label').textContent = 'Offline (Cached)';
      }}
    }}

    window.addEventListener('pageshow', fetchCloudData);
    window.addEventListener('focus', fetchCloudData);
    setInterval(fetchCloudData, 5000);

    renderApp();
    fetchCloudData();
  </script>
</body>
</html>
"""

    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Successfully built Multi-Series & Two-Way Synced KDP Books Hub!")

if __name__ == "__main__":
    build_hub_html()
