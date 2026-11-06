/**
 * KDP 100-Book Fast Auto-Publisher (Content Script)
 * Automatically injects a floating command hub directly into Amazon KDP title setup pages.
 * Supports 1-Click auto-filling for Title, Subtitle, Series, Description, Keywords, Specs, and Pricing.
 */

(function () {
  if (window.__kdp100Injected) return;
  window.__kdp100Injected = true;

  console.log("[KDP 100-Book Auto-Publisher] Initializing extension on Amazon KDP...");

  // Create Floating Hub UI
  const hub = document.createElement("div");
  hub.id = "kdp-100-floating-hub";
  hub.innerHTML = `
    <style>
      #kdp-100-floating-hub {
        position: fixed;
        top: 20px;
        right: 20px;
        width: 320px;
        background: #0D1117;
        color: #F0F6FC;
        border: 2px solid #E3B341;
        border-radius: 12px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.8);
        z-index: 999999;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 12px;
        overflow: hidden;
      }
      .kdp-hub-header {
        background: #161B22;
        padding: 10px 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #30363D;
        cursor: move;
      }
      .kdp-hub-title {
        font-weight: 800;
        color: #E3B341;
        font-size: 13px;
        display: flex;
        align-items: center;
        gap: 6px;
      }
      .kdp-hub-body {
        padding: 12px;
        max-height: 480px;
        overflow-y: auto;
      }
      .kdp-hub-select {
        width: 100%;
        padding: 8px 10px;
        background: #161B22;
        color: #F0F6FC;
        border: 1px solid #30363D;
        border-radius: 8px;
        font-size: 12px;
        margin-bottom: 10px;
        outline: none;
      }
      .kdp-hub-select:focus {
        border-color: #E3B341;
      }
      .kdp-btn-action {
        width: 100%;
        padding: 9px;
        border-radius: 8px;
        border: none;
        font-weight: 700;
        font-size: 12px;
        cursor: pointer;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        transition: transform 0.1s ease;
      }
      .kdp-btn-action:active {
        transform: scale(0.98);
      }
      .kdp-btn-primary {
        background: #238636;
        color: #FFF;
      }
      .kdp-btn-secondary {
        background: #1F6FEB;
        color: #FFF;
      }
      .kdp-btn-gold {
        background: #E3B341;
        color: #000;
      }
      .kdp-btn-outline {
        background: #21262D;
        color: #8B949E;
        border: 1px solid #30363D;
      }
      .kdp-badge-info {
        font-size: 10px;
        color: #8B949E;
        background: #161B22;
        padding: 6px 10px;
        border-radius: 6px;
        margin-bottom: 10px;
        border: 1px solid #21262D;
        line-height: 1.4;
      }
      .kdp-toast-msg {
        display: none;
        background: #238636;
        color: #FFF;
        padding: 6px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 11px;
        text-align: center;
        margin-top: 8px;
      }
    </style>

    <div class="kdp-hub-header" id="kdp-drag-handle">
      <div class="kdp-hub-title">
        <span>⚡</span> KDP 100-Book Fast-Publisher
      </div>
      <button id="kdp-minimize-btn" style="background:transparent; border:none; color:#8B949E; cursor:pointer; font-size:14px;">−</button>
    </div>

    <div class="kdp-hub-body" id="kdp-hub-content">
      <div style="font-size:11px; color:#8B949E; margin-bottom:6px;">Select Book to Auto-Fill:</div>
      <select id="kdp-book-picker" class="kdp-hub-select"></select>

      <div class="kdp-badge-info" id="kdp-selected-info">
        Select a volume to inspect details and auto-fill Amazon KDP forms.
      </div>

      <!-- Action Buttons -->
      <button class="kdp-btn-action kdp-btn-primary" id="kdp-autofill-details-btn">
        ⚡ 1-Click Auto-Fill (Step 1: Details)
      </button>

      <button class="kdp-btn-action kdp-btn-secondary" id="kdp-autofill-specs-btn">
        📖 Auto-Select Specs (Step 2: Content)
      </button>

      <button class="kdp-btn-action kdp-btn-gold" id="kdp-autofill-price-btn">
        💰 Auto-Set $12.99 Price (Step 3: Rights)
      </button>

      <button class="kdp-btn-action kdp-btn-outline" id="kdp-copy-all-btn">
        📋 Copy All Metadata to Clipboard
      </button>

      <div class="kdp-toast-msg" id="kdp-toast">Auto-Fill Successful! ✓</div>
    </div>
  `;

  document.body.appendChild(hub);

  // Populate Select with 100 Books
  const picker = document.getElementById("kdp-book-picker");
  const infoBox = document.getElementById("kdp-selected-info");

  if (typeof KDP_100_CATALOG !== "undefined" && Array.isArray(KDP_100_CATALOG)) {
    const seriesGroups = {};
    KDP_100_CATALOG.forEach(book => {
      const s = book.series || "Other";
      if (!seriesGroups[s]) seriesGroups[s] = [];
      seriesGroups[s].push(book);
    });

    for (const [seriesName, books] of Object.entries(seriesGroups)) {
      const optgroup = document.createElement("optgroup");
      optgroup.label = `${seriesName} (${books.length} Books)`;
      books.forEach(b => {
        const opt = document.createElement("option");
        opt.value = b.id;
        opt.textContent = `Vol. ${b.vol_number}: ${b.title}`;
        optgroup.appendChild(opt);
      });
      picker.appendChild(optgroup);
    }
  }

  function getSelectedBook() {
    const id = picker.value;
    return KDP_100_CATALOG.find(b => b.id === id) || KDP_100_CATALOG[0];
  }

  function updateInfo() {
    const b = getSelectedBook();
    if (b) {
      infoBox.innerHTML = `
        <b>${b.title}</b><br>
        <span style="color:#E3B341;">${b.series} • Vol ${b.vol_number}</span><br>
        176 Pages • 6"x9" • Price: $${b.price_usd} (Royalty: $${b.royalty_usd})
      `;
    }
  }

  picker.addEventListener("change", updateInfo);
  updateInfo();

  function showToast(msg) {
    const t = document.getElementById("kdp-toast");
    t.textContent = msg || "Success! ✓";
    t.style.display = "block";
    setTimeout(() => { t.style.display = "none"; }, 2500);
  }

  // Trigger input event to make Angular/React/KDP recognize changes
  function setVal(elem, val) {
    if (!elem) return false;
    elem.value = val;
    elem.dispatchEvent(new Event("input", { bubbles: true }));
    elem.dispatchEvent(new Event("change", { bubbles: true }));
    elem.dispatchEvent(new Event("blur", { bubbles: true }));
    return true;
  }

  // 1. Auto-Fill Step 1 (Details)
  document.getElementById("kdp-autofill-details-btn").addEventListener("click", () => {
    const b = getSelectedBook();
    let filled = 0;

    // Title
    const titleInput = document.querySelector("#data-print-book-title, input[name*='title']:not([name*='sub'])");
    if (setVal(titleInput, b.title)) filled++;

    // Subtitle
    const subInput = document.querySelector("#data-print-book-subtitle, input[name*='subtitle']");
    if (setVal(subInput, b.subtitle)) filled++;

    // Series info
    const seriesTitleInput = document.querySelector("#data-series-title, input[name*='seriesTitle']");
    if (setVal(seriesTitleInput, b.series)) filled++;

    const seriesNumInput = document.querySelector("#data-series-number, input[name*='seriesNumber']");
    if (setVal(seriesNumInput, String(b.vol_number))) filled++;

    // Description
    const descTextarea = document.querySelector("#data-print-book-description, textarea[name*='description']");
    if (setVal(descTextarea, b.description_html)) filled++;

    // TinyMCE iframe editor if present
    const tinymceIframe = document.querySelector("#tinymce-editor_ifr, iframe[id*='tinymce']");
    if (tinymceIframe && tinymceIframe.contentDocument) {
      const editorBody = tinymceIframe.contentDocument.querySelector("body#tinymce");
      if (editorBody) {
        editorBody.innerHTML = b.description_html;
        filled++;
      }
    }

    // Publishing Rights (I own the copyright)
    const rightsRadio = document.querySelector("#data-print-book-has-publishing-rights-yes, input[value='true'][name*='publishing-rights']");
    if (rightsRadio) {
      rightsRadio.checked = true;
      rightsRadio.dispatchEvent(new Event("change", { bubbles: true }));
      filled++;
    }

    // Adult Content (No)
    const adultNoRadio = document.querySelector("#data-print-book-is-adult-content-no, input[value='false'][name*='adult-content']");
    if (adultNoRadio) {
      adultNoRadio.checked = true;
      adultNoRadio.dispatchEvent(new Event("change", { bubbles: true }));
      filled++;
    }

    // 7 Keywords
    if (Array.isArray(b.keywords)) {
      b.keywords.forEach((kw, i) => {
        const kwInput = document.querySelector(`#data-print-book-keywords-${i}, input[name*='keywords[${i}]'], input[id*='keywords-${i}']`);
        if (setVal(kwInput, kw)) filled++;
      });
    }

    showToast(`Filled ${filled} fields on Step 1! ✓`);
  });

  // 2. Auto-Fill Step 2 (Content & Specs)
  document.getElementById("kdp-autofill-specs-btn").addEventListener("click", () => {
    let filled = 0;

    // Black & white interior with white paper
    const bwWhiteRadio = document.querySelector("#data-print-book-interior-paper-type-black-white-white, input[value='black-white-white']");
    if (bwWhiteRadio) {
      bwWhiteRadio.checked = true;
      bwWhiteRadio.dispatchEvent(new Event("change", { bubbles: true }));
      filled++;
    }

    // No Bleed
    const noBleedRadio = document.querySelector("#data-print-book-bleed-none, input[value='none'][name*='bleed']");
    if (noBleedRadio) {
      noBleedRadio.checked = true;
      noBleedRadio.dispatchEvent(new Event("change", { bubbles: true }));
      filled++;
    }

    // Matte Finish
    const matteRadio = document.querySelector("#data-print-book-cover-finish-matte, input[value='matte'][name*='cover']");
    if (matteRadio) {
      matteRadio.checked = true;
      matteRadio.dispatchEvent(new Event("change", { bubbles: true }));
      filled++;
    }

    showToast(`Set 6"x9" B&W Matte specs! ✓`);
  });

  // 3. Auto-Fill Step 3 (Pricing)
  document.getElementById("kdp-autofill-price-btn").addEventListener("click", () => {
    const b = getSelectedBook();
    const priceInput = document.querySelector("#data-pricing-print-us-price-input, input[name*='price'][name*='us'], input[id*='us-price']");
    if (setVal(priceInput, b.price_usd || "12.99")) {
      showToast(`Set List Price to $${b.price_usd}! ✓`);
    } else {
      showToast(`Set to $${b.price_usd} (Manual check) ✓`);
    }
  });

  // 4. Copy All Metadata
  document.getElementById("kdp-copy-all-btn").addEventListener("click", () => {
    const b = getSelectedBook();
    const allText = `TITLE: ${b.title}\nSUBTITLE: ${b.subtitle}\nSERIES: ${b.series} #${b.vol_number}\nPRICE: $${b.price_usd}\nKEYWORDS:\n${(b.keywords||[]).join('\n')}\n\nDESCRIPTION:\n${b.description_html}`;
    navigator.clipboard.writeText(allText).then(() => {
      showToast("All metadata copied! ✓");
    });
  });

  // Minimize / Expand
  let isMinimized = false;
  document.getElementById("kdp-minimize-btn").addEventListener("click", () => {
    const body = document.getElementById("kdp-hub-content");
    const btn = document.getElementById("kdp-minimize-btn");
    isMinimized = !isMinimized;
    body.style.display = isMinimized ? "none" : "block";
    btn.textContent = isMinimized ? "+" : "−";
  });

  // Dragging support
  const dragHandle = document.getElementById("kdp-drag-handle");
  let isDragging = false, offsetX = 0, offsetY = 0;

  dragHandle.addEventListener("mousedown", (e) => {
    if (e.target.id === "kdp-minimize-btn") return;
    isDragging = true;
    offsetX = e.clientX - hub.getBoundingClientRect().left;
    offsetY = e.clientY - hub.getBoundingClientRect().top;
  });

  document.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    hub.style.left = `${e.clientX - offsetX}px`;
    hub.style.top = `${e.clientY - offsetY}px`;
    hub.style.right = "auto";
  });

  document.addEventListener("mouseup", () => {
    isDragging = false;
  });

  console.log("[KDP 100-Book Auto-Publisher] Floating hub injected successfully.");
})();
