"""
sync_hub.py (v3.0 - Hybrid Cloud Sync Edition)
Generates the mobile app with real-time Dual-Engine Hybrid Auto-Sync:
- Primary: Google Cloud Firebase (Sub-second live streaming)
- Fallback: GitHub Cloud (Global Raw CDN & version control)
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
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>KDP Books Hub (Hybrid Cloud)</title>
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <style>
    :root {{
      --bg: #0D1117;
      --card-bg: #161B22;
      --border: #30363D;
      --accent: #E3B341;
      --accent-green: #2EA043;
      --accent-blue: #58A6FF;
      --text: #F0F6FC;
      --text-muted: #8B949E;
    }}
    * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
    body {{
      margin: 0;
      padding: 16px;
      padding-bottom: 70px;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      padding-top: 4px;
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
      padding: 10px 16px;
      font-size: 13px;
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
      background: rgba(0,0,0,0.2);
      padding: 10px;
      border-radius: 8px;
      border: 1px solid rgba(255,255,255,0.05);
    }}
    .kw-grid {{
      display: grid;
      gap: 8px;
    }}
    .kw-item {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(0,0,0,0.2);
      padding: 8px 10px;
      border-radius: 8px;
      font-size: 12px;
    }}
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
      box-shadow: 0 4px 12px rgba(0,0,0,0.4);
      transition: transform 0.25s ease-out;
      z-index: 9999;
    }}
    .toast.show {{
      transform: translateX(-50%) translateY(0);
    }}
  </style>
</head>
<body>
  <header>
    <div>
      <h1>KDP Books Hub</h1>
      <span style="font-size:11px; color:var(--text-muted);">The Detective's Case Files Series</span>
    </div>
    <div class="cloud-status" onclick="promptCloudUrl()">
      <div class="cloud-dot"></div>
      <span id="cloud-label">Hybrid: Syncing...</span>
    </div>
  </header>

  <div class="tab-bar" id="tab-container"></div>
  <div id="content-container"></div>

  <div id="toast" class="toast">Copied to clipboard! ✓</div>

  <script>
    const INITIAL_CATALOG = {catalog_json_str};
    let firebaseEndpoint = localStorage.getItem('kdp_firebase_url') || "{firebase_url}";
    let githubEndpoint = localStorage.getItem('kdp_github_url') || "{github_url}";

    let currentCatalog = JSON.parse(localStorage.getItem('kdp_catalog_cache') || 'null') || INITIAL_CATALOG;
    let activeVolId = currentCatalog[0] ? currentCatalog[0].id : null;

    function renderApp() {{
      const tabContainer = document.getElementById('tab-container');
      const contentContainer = document.getElementById('content-container');

      tabContainer.innerHTML = '';
      contentContainer.innerHTML = '';

      currentCatalog.forEach((book) => {{
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
                ${{book.keywords.map((kw, i) => `
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
                <b>Trim:</b> ${{book.trim}} | <b>Pages:</b> ${{book.pages}} | <b>Bleed:</b> ${{book.bleed}}<br>
                <b>Cover Theme:</b> ${{book.cover_palette}}<br>
                <b>Retail Price:</b> $${{book.price_usd}} USD | <b>Print Cost:</b> $${{book.print_cost_usd}} | <b>Your Royalty:</b> $${{book.royalty_usd}}
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
      setTimeout(() => toast.classList.remove('show'), 1500);
    }}

    function copyText(txt) {{
      navigator.clipboard.writeText(txt).then(() => showToast('Copied! ✓'));
    }}

    function copyDesc(elemId) {{
      const elem = document.getElementById(elemId);
      navigator.clipboard.writeText(elem.innerText).then(() => showToast('HTML Description Copied! ✓'));
    }}

    function promptCloudUrl() {{
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

    // DUAL-ENGINE HYBRID AUTO-SYNC: Polls Google Cloud with GitHub Cloud failover
    async function fetchCloudData() {{
      let data = null;
      let activeSource = "";

      // 1. Primary: Google Cloud Firebase (Sub-second live streaming)
      if (firebaseEndpoint) {{
        let targetUrl = firebaseEndpoint.replace(/\\/+$/, '');
        if (!targetUrl.endsWith('/catalog.json')) targetUrl += '/catalog.json';
        try {{
          const res = await fetch(targetUrl + '?t=' + Date.now());
          if (res.ok) {{
            data = await res.json();
            activeSource = githubEndpoint ? "Hybrid: Google ☁️ + GitHub 🐙" : "Google Cloud ☁️";
          }}
        }} catch(err) {{
          console.warn("Google Cloud connection failed, attempting GitHub fallback...", err);
        }}
      }}

      // 2. Secondary Failover: GitHub Cloud (Raw CDN / Gist)
      if (!data && githubEndpoint) {{
        try {{
          const res = await fetch(githubEndpoint + '?t=' + Date.now());
          if (res.ok) {{
            data = await res.json();
            activeSource = "GitHub Cloud 🐙";
          }}
        }} catch(err) {{
          console.warn("GitHub Cloud fallback failed...", err);
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

    // Trigger auto-sync when opening phone or unlocking screen
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

    print("Successfully built Dual-Engine Hybrid Cloud KDP Books Hub!")

if __name__ == "__main__":
    build_hub_html()
