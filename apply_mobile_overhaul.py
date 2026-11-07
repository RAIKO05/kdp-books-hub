import sys

print("Reading build_full_hub_v4.py...")
with open("build_full_hub_v4.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. CSS Injection
css_target = """    .zip-dl-btn {{
      background: #238636;
      color: #FFF;
      text-decoration: none;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
    }}
  </style>"""

css_replacement = """    .zip-dl-btn {{
      background: #238636;
      color: #FFF;
      text-decoration: none;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
    }}

    /* ==========================================================================
       MOBILE OPTIMIZATION (iPhone & Android Viewports)
       ========================================================================== */
    @media (max-width: 640px) {{
      body {{
        padding: 6px 8px;
        padding-top: max(6px, env(safe-area-inset-top));
        padding-bottom: max(75px, calc(58px + env(safe-area-inset-bottom)));
      }}

      /* Compact Header */
      header {{
        margin-bottom: 5px;
        align-items: center;
        flex-wrap: nowrap;
      }}
      .app-logo {{
        width: 30px;
        height: 30px;
        border-radius: 7px;
      }}
      h1 {{
        font-size: 15px;
        letter-spacing: 0.2px;
      }}
      #series-subtitle {{
        font-size: 9.5px !important;
      }}
      .header-actions {{
        display: none !important; /* Moved to fixed bottom navigation bar */
      }}
      .header-mobile-right {{
        display: flex !important;
        align-items: center;
        gap: 6px;
      }}

      /* Ultra-Compact Collapsible Publishing Progress Bar */
      .progress-card {{
        padding: 5px 8px;
        margin-bottom: 5px;
        border-radius: 8px;
      }}
      .progress-header {{
        font-size: 10.5px;
        margin-bottom: 3px;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }}
      .progress-bar-bg {{
        height: 4px;
      }}
      .progress-toggle-icon {{
        display: inline-block !important;
        font-size: 11px;
        color: var(--accent);
        margin-left: 4px;
      }}
      .progress-filter-bar {{
        display: none;
        margin-top: 5px;
        gap: 4px;
        overflow-x: auto;
        padding-bottom: 2px;
        -webkit-overflow-scrolling: touch;
      }}
      .progress-filter-bar.open {{
        display: flex !important;
      }}
      .filter-chip {{
        font-size: 9px;
        padding: 2.5px 6px;
        border-radius: 4px;
        white-space: nowrap;
        flex-shrink: 0;
      }}

      /* Slim Search Bar */
      .top-toolbar {{
        margin-bottom: 5px;
        gap: 5px;
      }}
      .search-input {{
        padding: 6px 9px;
        font-size: 12px;
        border-radius: 7px;
      }}
      .catalog-badge {{
        font-size: 9.5px;
        padding: 5px 8px;
        border-radius: 7px;
      }}

      /* Series Pills Bar */
      .series-bar {{
        gap: 4px;
        padding-bottom: 4px;
        margin-bottom: 5px;
      }}
      .series-pill {{
        padding: 4px 9px;
        font-size: 10.5px;
        border-radius: 14px;
        white-space: nowrap;
      }}
      .series-full-label {{
        display: none !important;
      }}
      .series-mobile-label {{
        display: inline !important;
      }}

      /* Hide Desktop Tabs on Mobile */
      .tab-bar {{
        display: none !important;
      }}

      /* Mobile Volume Stepper Bar */
      .mobile-vol-stepper {{
        display: flex !important;
        align-items: center;
        gap: 5px;
        margin-bottom: 6px;
      }}
      .stepper-btn {{
        background: #21262D;
        border: 1px solid var(--border);
        color: var(--text);
        width: 36px;
        height: 36px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: 700;
        cursor: pointer;
        flex-shrink: 0;
      }}
      .stepper-btn:active {{
        background: var(--accent);
        color: #000;
      }}
      .stepper-select {{
        flex: 1;
        background: #161B22;
        border: 1px solid #2EA043;
        color: #FFF;
        font-weight: 700;
        font-size: 11.5px;
        padding: 8px 8px;
        border-radius: 8px;
        outline: none;
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
      }}

      /* Book Showcase Card (Front and Center Above Fold) */
      .cover-showcase-card {{
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 12px;
      }}
      .book-title-header {{
        text-align: center;
        margin-bottom: 5px;
      }}
      .book-vol-tag {{
        font-size: 9.5px;
        font-weight: 800;
        color: var(--accent);
        letter-spacing: 0.5px;
        text-transform: uppercase;
      }}
      .book-main-title {{
        font-size: 15px;
        font-weight: 800;
        color: #FFF;
        margin-top: 1px;
        line-height: 1.25;
      }}
      .book-main-subtitle {{
        font-size: 10px;
        color: var(--text-muted);
        margin-top: 2px;
      }}
      .book-3d-wrap {{
        margin: 5px auto 7px auto;
      }}
      .book-cover-img {{
        width: 140px;
        height: 210px;
        border-radius: 4px 8px 8px 4px;
        box-shadow: -4px 6px 16px rgba(0,0,0,0.6), 0 0 12px rgba(227,179,65,0.25);
      }}
      .cover-tap-hint {{
        font-size: 9px;
        margin-bottom: 7px;
      }}

      .badge-bar {{
        gap: 3px;
        margin-bottom: 7px;
      }}
      .badge {{
        font-size: 8.5px;
        padding: 2.5px 5px;
      }}

      /* Compact Action Grid */
      .action-grid {{
        grid-template-columns: 1fr 1fr;
        gap: 5px;
        margin-bottom: 5px;
      }}
      .btn-pdf-interior, .btn-pdf-cover {{
        padding: 8px 5px;
        font-size: 11px;
        border-radius: 7px;
      }}
      .btn-quick-read, .btn-promo-toggle, .btn-aplus-toggle {{
        padding: 8px 8px;
        font-size: 11px;
        margin-bottom: 5px;
        border-radius: 7px;
      }}

      /* Status Strip */
      .status-card {{
        padding: 7px 9px;
        margin-bottom: 7px;
        flex-direction: column;
        align-items: stretch;
        gap: 5px;
      }}
      .status-badge-wrap {{
        justify-content: space-between;
      }}
      .status-select {{
        font-size: 10.5px;
        padding: 4px 6px;
      }}

      /* Fixed Mobile Bottom App Bar */
      .mobile-bottom-nav {{
        display: flex !important;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 56px;
        background: rgba(13, 17, 23, 0.95);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-top: 1px solid var(--border);
        justify-content: space-around;
        align-items: center;
        z-index: 999;
        padding-bottom: env(safe-area-inset-bottom);
      }}
      .nav-tab-item {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2px;
        color: var(--text-muted);
        text-decoration: none;
        font-size: 9px;
        font-weight: 700;
        cursor: pointer;
        padding: 5px 12px;
        border: none;
        background: transparent;
      }}
      .nav-tab-item.active {{
        color: var(--accent);
      }}
      .nav-tab-icon {{
        font-size: 18px;
      }}

      /* Modals on Mobile */
      .modal-card {{
        width: 95% !important;
        max-height: 88vh !important;
        padding: 12px !important;
      }}

      /* Sudoku Board Scaling on Mobile */
      .sudoku-board {{
        max-width: 100% !important;
        margin: 6px auto !important;
      }}
      .sudoku-cell {{
        font-size: 13px !important;
      }}
      .num-btn {{
        width: 30px !important;
        height: 34px !important;
        font-size: 13px !important;
      }}
    }}

    @media (min-width: 641px) {{
      .mobile-vol-stepper {{
        display: none !important;
      }}
      .mobile-bottom-nav {{
        display: none !important;
      }}
      .header-mobile-right {{
        display: none !important;
      }}
      .progress-toggle-icon {{
        display: none !important;
      }}
      .series-full-label {{
        display: inline !important;
      }}
      .series-mobile-label {{
        display: none !important;
      }}
    }}
  </style>"""

assert css_target in content, "css_target not found!"
content = content.replace(css_target, css_replacement)

# 2. Header Replacement
header_target = """  <header>
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
  </header>"""

header_replacement = """  <header>
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
    <div class="header-mobile-right">
      <div class="cloud-status" onclick="refreshFromFirebase()" style="padding:4px 8px; font-size:10px;">
        <div class="cloud-dot"></div>
        <span id="cloud-status-text-mobile">Sync</span>
      </div>
    </div>
  </header>"""

assert header_target in content, "header_target not found!"
content = content.replace(header_target, header_replacement)

# 3. Progress Card & Stepper HTML
middle_target = """  <!-- KDP PUBLISHING PROGRESS DASHBOARD -->
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
  <div class="tab-bar" id="tab-container"></div>"""

middle_replacement = """  <!-- KDP PUBLISHING PROGRESS DASHBOARD -->
  <div class="progress-card">
    <div class="progress-header" onclick="toggleProgressDetails()">
      <span style="font-weight:700; color:var(--text);" id="progress-text">📊 KDP Progress: 0 / 130 Live (0%)</span>
      <span style="font-size:11px; color:var(--accent);" id="projected-royalty-badge">Live: $0.00/mo</span>
      <span class="progress-toggle-icon" id="progress-toggle-icon">▾</span>
    </div>
    <div class="progress-bar-bg">
      <div class="progress-bar-fill" id="progress-bar-fill"></div>
    </div>
    <div class="progress-filter-bar" id="progress-filter-bar">
      <button class="filter-chip active" onclick="setStatusFilter('all')">All Books (130)</button>
      <button class="filter-chip" onclick="setStatusFilter('live')">🟢 Live (<span id="count-live">0</span>)</button>
      <button class="filter-chip" onclick="setStatusFilter('in_review')">🟡 Review (<span id="count-review">0</span>)</button>
      <button class="filter-chip" onclick="setStatusFilter('unpublished')">⚪ Unpub (<span id="count-unpub">130</span>)</button>
    </div>
  </div>

  <div class="top-toolbar">
    <input type="text" id="search-box" class="search-input" placeholder="🔍 Search 130 books across 9 series..." oninput="handleSearch()">
    <div class="catalog-badge">130 BOOKS</div>
  </div>

  <!-- Series Selector Pills -->
  <div class="series-bar" id="series-bar"></div>

  <!-- Mobile Volume Stepper -->
  <div class="mobile-vol-stepper">
    <button class="stepper-btn" onclick="stepVolume(-1)" aria-label="Previous Volume">◀</button>
    <select id="mobile-vol-select" class="stepper-select" onchange="onMobileSelectVolume(this.value)"></select>
    <button class="stepper-btn" onclick="stepVolume(1)" aria-label="Next Volume">▶</button>
  </div>

  <!-- Volume Tabs (Desktop) -->
  <div class="tab-bar" id="tab-container"></div>"""

assert middle_target in content, "middle_target not found!"
content = content.replace(middle_target, middle_replacement)

# 4. Bottom Nav Bar
bottom_target = """  <div id="toast" class="toast">Copied to clipboard! ✓</div>"""
bottom_replacement = """  <!-- Native Mobile Bottom Navigation Bar -->
  <nav class="mobile-bottom-nav">
    <button class="nav-tab-item active" onclick="window.scrollTo(0, 0)">
      <span class="nav-tab-icon">📚</span>
      <span>Catalog</span>
    </button>
    <button class="nav-tab-item" onclick="openGameModal()">
      <span class="nav-tab-icon">🎮</span>
      <span>Case #1</span>
    </button>
    <button class="nav-tab-item" onclick="openCalcModal()">
      <span class="nav-tab-icon">💰</span>
      <span>Calculator</span>
    </button>
    <button class="nav-tab-item" onclick="openZipModal()">
      <span class="nav-tab-icon">📦</span>
      <span>Downloads</span>
    </button>
  </nav>

  <div id="toast" class="toast">Copied to clipboard! ✓</div>"""

assert bottom_target in content, "bottom_target not found!"
content = content.replace(bottom_target, bottom_replacement)

# 5. JavaScript Helper Functions & Stepper
js_funcs_target = """    function toggleAplusDrawer(drawerId) {{
      const drawer = document.getElementById(drawerId);
      if (drawer) {{
        drawer.classList.toggle('open');
      }}
    }}"""

js_funcs_replacement = """    function toggleProgressDetails() {{
      const bar = document.getElementById('progress-filter-bar');
      const icon = document.getElementById('progress-toggle-icon');
      if (bar) {{
        bar.classList.toggle('open');
        if (icon) icon.textContent = bar.classList.contains('open') ? '▴' : '▾';
      }}
    }}

    function stepVolume(delta) {{
      const vols = getVolumesForActiveSeries();
      if (!vols.length) return;
      const curIdx = vols.findIndex(v => v.id === activeVolId);
      const nextIdx = (curIdx + delta + vols.length) % vols.length;
      activeVolId = vols[nextIdx].id;
      renderApp();
    }}

    function onMobileSelectVolume(val) {{
      activeVolId = val;
      renderApp();
    }}

    function toggleAplusDrawer(drawerId) {{
      const drawer = document.getElementById(drawerId);
      if (drawer) {{
        drawer.classList.toggle('open');
      }}
    }}"""

assert js_funcs_target in content, "js_funcs_target not found!"
content = content.replace(js_funcs_target, js_funcs_replacement)

# 6. JavaScript Series Pills & Icons & Mobile Stepper Population
series_loop_target = """      presentSeries.forEach(sName => {{
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
      }}"""

series_loop_replacement = """      const SERIES_SHORT_NAMES = {{
        "The Detective\'s Case Files": "Detective",
        "The Lupin Heists": "Lupin",
        "The Machine Protocols": "Machine",
        "Project X": "Project X",
        "The Ravencrest Chronicles": "Ravencrest",
        "The Bletchley Protocols": "Bletchley",
        "Crypt of the Pharaohs": "Pharaohs",
        "The Blackwood Asylum Files": "Asylum",
        "The Grand Orient Express": "Express"
      }};

      presentSeries.forEach(sName => {{
        const count = filtered.filter(b => b.series === sName).length;
        const pill = document.createElement('button');
        pill.className = `series-pill ${{sName === activeSeries ? 'active' : ''}}`;
        
        let icon = "📚";
        if (sName.includes("Detective")) icon = "🕵️";
        else if (sName.includes("Lupin")) icon = "🎩";
        else if (sName.includes("Machine")) icon = "👁️";
        else if (sName.includes("Project X")) icon = "🚀";
        else if (sName.includes("Ravencrest")) icon = "🏰";
        else if (sName.includes("Bletchley")) icon = "📻";
        else if (sName.includes("Pharaoh")) icon = "🏺";
        else if (sName.includes("Asylum")) icon = "🏥";
        else if (sName.includes("Express")) icon = "🚂";

        const shortName = SERIES_SHORT_NAMES[sName] || sName;
        pill.innerHTML = `<span class=\"series-full-label\">${{icon}} ${{sName}} (${{count}})</span><span class=\"series-mobile-label\">${{icon}} ${{shortName}} (${{count}})</span>`;
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
        contentContainer.innerHTML = `<div class=\"card\" style=\"text-align:center; padding:30px; color:var(--text-muted);\">No books found matching criteria.</div>`;
        return;
      }}

      if (!activeVolId || !vols.some(v => v.id === activeVolId)) {{
        activeVolId = vols[0].id;
      }}

      // Populate Mobile Volume Dropdown
      const mobileSelect = document.getElementById('mobile-vol-select');
      if (mobileSelect) {{
        mobileSelect.innerHTML = vols.map(v => 
          `<option value=\"${{v.id}}\" ${{v.id === activeVolId ? 'selected' : ''}}>${{v.tab_name || 'Vol ' + v.vol_number + ': ' + v.title}}</option>`
        ).join('');
      }}"""

assert series_loop_target in content, "series_loop_target not found!"
content = content.replace(series_loop_target, series_loop_replacement)

# 7. Book Title & Subtitle prominently at top of showcase card
showcase_target = """            <!-- COVER & PDF SHOWCASE HERO CARD -->
            <div class="cover-showcase-card">
              <div class="book-3d-wrap" onclick="openImageModal('${{wrapImg}}?v=luxury_v3', '${{escapeQuotes(book.title)}} - Full Cover Wrap')">
                <img src="${{frontImg}}?v=luxury_v3" class="book-cover-img" alt="${{escapeHtml(book.title)}} Front Cover" onerror="this.onerror=null; this.src='app_icon_1024.png';">
              </div>
              <div class="cover-tap-hint">🔍 Tap cover image to inspect full wrap (Front, Spine & Back)</div>"""

showcase_replacement = """            <!-- COVER & PDF SHOWCASE HERO CARD -->
            <div class="cover-showcase-card">
              <div class="book-title-header">
                <div class="book-vol-tag">${{escapeHtml(book.series)}} &bull; VOL #${{book.vol_number}}</div>
                <div class="book-main-title">${{escapeHtml(book.title)}}</div>
                <div class="book-main-subtitle">${{escapeHtml(book.subtitle)}}</div>
              </div>

              <div class="book-3d-wrap" onclick="openImageModal('${{wrapImg}}?v=luxury_v3', '${{escapeQuotes(book.title)}} - Full Cover Wrap')">
                <img src="${{frontImg}}?v=luxury_v3" class="book-cover-img" alt="${{escapeHtml(book.title)}} Front Cover" onerror="this.onerror=null; this.src='app_icon_1024.png';">
              </div>
              <div class="cover-tap-hint">🔍 Tap cover image to inspect 300 DPI full wrap (Front, Spine & Back)</div>"""

assert showcase_target in content, "showcase_target not found!"
content = content.replace(showcase_target, showcase_replacement)

# 8. Update updateProgressMetrics
progress_metrics_target = """      const pct = Math.round((live / currentCatalog.length) * 100);
      document.getElementById('progress-text').textContent = `📊 KDP Publishing Progress: ${{live}} / ${{currentCatalog.length}} Live (${{pct}}%)`;
      document.getElementById('progress-bar-fill').style.width = `${{pct}}%`;
      
      const liveMonthly = live * 3 * 30 * 4.68;
      document.getElementById('projected-royalty-badge').textContent = `Est. Live Royalties: $${{liveMonthly.toFixed(0)}}/mo`;"""

progress_metrics_replacement = """      const pct = Math.round((live / currentCatalog.length) * 100);
      document.getElementById('progress-text').textContent = `📊 KDP Progress: ${{live}} / ${{currentCatalog.length}} Live (${{pct}}%)`;
      document.getElementById('progress-bar-fill').style.width = `${{pct}}%`;
      
      const liveMonthly = live * 3 * 30 * 4.68;
      document.getElementById('projected-royalty-badge').textContent = `Live: $${{liveMonthly.toFixed(0)}}/mo`;"""

assert progress_metrics_target in content, "progress_metrics_target not found!"
content = content.replace(progress_metrics_target, progress_metrics_replacement)

with open("build_full_hub_v4.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully applied mobile overhaul to build_full_hub_v4.py!")
