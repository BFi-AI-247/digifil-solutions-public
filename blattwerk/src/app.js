/* Blattwerk – Editor mit Seitenrahmen und frei platzierbaren Elementen. Benötigt BW aus core.js. */
(function () {
  'use strict';
  var B = window.BW;
  var ENV = window.BLATT_ENV || 'web';
  var STAGE = window.BLATT_STAGE || 'live';
  var DB_NAME = window.BLATT_DB || 'blattwerk2';
  var VERSION = window.BLATT_VERSION || '';
  var FEEDBACK_URL = (STAGE === 'vorschau' ? '../' : '') + 'feedback.php';
  var PX_MM = 96 / 25.4; // CSS-Pixel pro mm bei 100 %
  var $ = function (id) { return document.getElementById(id); };
  var LINE_COLORS = ['#1b2430', '#4a5563', '#2456a4', '#0e7d63', '#9a3d2b'];

  // ---------- Hilfen ----------
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html !== undefined) e.innerHTML = html; return e; }
  function icon(n) { return '<svg aria-hidden="true"><use href="#i-' + n + '"/></svg>'; }
  function r1(n) { return Math.round(n * 10) / 10; }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function toast(msg) { var t = $('toast'); t.textContent = msg; t.hidden = false; clearTimeout(toast.t); toast.t = setTimeout(function () { t.hidden = true; }, 2600); }
  function fileSafe(s) { return (s || 'Arbeitsblatt').replace(/[\\/:*?"<>|]+/g, '').replace(/\s+/g, ' ').trim().slice(0, 80) || 'Arbeitsblatt'; }
  // Maße der Blattschrift (x-Höhe, Ober-/Unterlänge im Verhältnis zur Schriftgröße), im Browser gemessen
  var metr = null;
  function sheetMetrics() {
    if (metr) return metr;
    var m = { x: 0.5, a: 0.95, d: 0.25 };
    try {
      var fam = getComputedStyle(document.documentElement).getPropertyValue('--font-sheet').trim() || 'Andika, sans-serif';
      var cx = document.createElement('canvas').getContext('2d'); cx.font = '100px ' + fam;
      var t = cx.measureText('x');
      if (t.actualBoundingBoxAscent > 20 && t.actualBoundingBoxAscent < 80) m.x = t.actualBoundingBoxAscent / 100;
      if (t.fontBoundingBoxAscent > 50 && t.fontBoundingBoxDescent > 0) { m.a = t.fontBoundingBoxAscent / 100; m.d = t.fontBoundingBoxDescent / 100; }
    } catch (e) { /* Standardwerte */ }
    return (metr = m);
  }
  function itemEl(id) { return document.querySelector('.item[data-id="' + id + '"]'); }
  var ALLOWED = { B: 1, STRONG: 1, I: 1, EM: 1, U: 1, BR: 1, DIV: 1, P: 1 };
  function cleanHtml(html) {
    var t = document.createElement('template'); t.innerHTML = html;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (c) {
        if (c.nodeType === 3) return;
        if (c.nodeType !== 1) { c.remove(); return; }
        walk(c);
        if (!ALLOWED[c.tagName]) { while (c.firstChild) c.parentNode.insertBefore(c.firstChild, c); c.remove(); return; }
        while (c.attributes.length) c.removeAttribute(c.attributes[0].name);
      });
    })(t.content);
    var out = t.innerHTML; return out === '<br>' ? '' : out;
  }

  // ---------- Speicher ----------
  var store = (function () {
    var mem = {}, dbp = null;
    function open() {
      if (dbp) return dbp;
      dbp = new Promise(function (res) {
        try {
          var r = indexedDB.open(DB_NAME, 1);
          r.onupgradeneeded = function () { r.result.createObjectStore('docs', { keyPath: 'id' }); };
          r.onsuccess = function () { res(r.result); }; r.onerror = function () { res(null); };
        } catch (e) { res(null); }
      });
      return dbp;
    }
    function tx(mode, fn) {
      return open().then(function (db) {
        if (!db) return fn(null);
        return new Promise(function (res, rej) {
          try { var t = db.transaction('docs', mode), out = fn(t.objectStore('docs')); t.oncomplete = function () { res(out && out.result !== undefined ? out.result : out); }; t.onerror = function () { rej(t.error); }; }
          catch (e) { rej(e); }
        });
      });
    }
    return {
      ok: function () { return open().then(function (d) { return !!d; }); },
      all: function () { return tx('readonly', function (s) { return s ? s.getAll() : null; }).then(function (r) { return r || Object.keys(mem).map(function (k) { return mem[k]; }); }); },
      put: function (d) { var c = B.clone(d); mem[d.id] = c; return tx('readwrite', function (s) { if (s) s.put(c); }); },
      del: function (id) { delete mem[id]; return tx('readwrite', function (s) { if (s) s.delete(id); }); }
    };
  })();
  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* egal */ } }

  // ---------- Zustand ----------
  var docs = [], D = null;
  var sel = null;          // {pi, id} Element | {pi, block} Punkte eines Blocks
  var editing = null;      // ID des Elements im Schreibmodus (Textfeld, Lineatur, Kästchen)
  var editBefore = null;   // Stand vor dem Hineinschreiben (ein Rückgängig-Schritt je Schreibvorgang)
  var kcur = null;         // Schreibmarke in Kästchen {r, c, c0}
  var tcur = null;         // aktive Zelle in einer Tabelle {r, c}
  var tanc = null;         // Anfang einer Zellen-Auswahl in der Tabelle {r, c} (Ende = tcur)
  var textend = false;     // nächstes Antippen einer Zelle erweitert die Auswahl (iPad)
  var tdrag = null;        // Auswahl mit der Maus aufziehen
  var WRITABLE = ['text', 'lineatur', 'karo', 'table'];
  var CELL_BG = ['', '#fff3c4', '#dcefe8', '#dbe8f7', '#f9dede', '#ececec'];
  var cur = 0;             // aktuelle Seite
  var zoom = 'fit', scale = 1;
  var undoStack = [], redoStack = [];

  function page(pi) { return D.pages[pi === undefined ? cur : pi]; }
  function itemById(pi, id) { var p = D.pages[pi]; if (!p) return null; for (var i = 0; i < p.items.length; i++) if (p.items[i].id === id) return p.items[i]; return null; }
  function selItem() { return sel && sel.id ? itemById(sel.pi, sel.id) : null; }
  function snap() { var s = B.clone(D); delete s.assets; return JSON.stringify(s); }
  function restore(json) { var a = D.assets; D = JSON.parse(json); D.assets = a; replaceDoc(D); }
  function replaceDoc(d) { for (var i = 0; i < docs.length; i++) if (docs[i].id === d.id) { docs[i] = d; return; } docs.unshift(d); }

  // Änderung mit Rückgängig, Speichern und Neuzeichnen
  function change(fn, opts) {
    undoStack.push(snap()); if (undoStack.length > 60) undoStack.shift(); redoStack = [];
    fn(); save(); updateUndo();
    if (!opts || opts.render !== false) render();
  }
  function undo() { if (!undoStack.length) return; redoStack.push(snap()); restore(undoStack.pop()); after(); }
  function redo() { if (!redoStack.length) return; undoStack.push(snap()); restore(redoStack.pop()); after(); }
  function after() { if (sel && !(sel.id ? selItem() : page(sel.pi))) sel = null; cur = Math.min(cur, D.pages.length - 1); editing = null; editBefore = null; kcur = null; tcur = null; tanc = null; textend = false; save(); updateUndo(); render(); }
  function updateUndo() { $('btnUndo').disabled = !undoStack.length; $('btnRedo').disabled = !redoStack.length; }

  var saveT = null, storageOk = true;
  function save() {
    D.updated = Date.now(); $('saveState').textContent = 'Speichert …';
    clearTimeout(saveT);
    saveT = setTimeout(function () {
      store.put(D).then(function () { $('saveState').textContent = storageOk ? 'Gespeichert' : 'Nur bis zum Schließen gespeichert'; },
        function () { $('saveState').textContent = 'Speichern fehlgeschlagen'; });
      lsSet('blattwerk.current', D.id);
    }, 600);
  }

  // Rahmen ändern: Elemente wandern mit ihrem Aufgabenblock mit
  function contentRight(lay) { return (lay.pointsCol ? lay.pointsCol.x : lay.box.x + lay.box.w) - 6; }
  function reanchor(p, oldL, newL, items) {
    var dx = newL.box.x - oldL.box.x, oR = contentRight(oldL), nR = contentRight(newL);
    (items || p.items).forEach(function (it) {
      var cy = it.y + Math.min(it.h, 12) / 2, i = -1;
      oldL.blocks.forEach(function (b, k) { if (cy >= b.y && cy < b.y + b.h) i = k; });
      if (i >= 0 && newL.blocks.length) {
        var ob = oldL.blocks[i], nb = newL.blocks[Math.min(i, newL.blocks.length - 1)];
        it.y = r1(nb.y + (it.y - ob.y));
      } else if (oldL.blocks.length && newL.blocks.length && cy >= oldL.contentBottom) {
        it.y = r1(it.y + (newL.contentBottom - oldL.contentBottom));
      }
      it.x = r1(it.x + dx);
      var right = it.x + it.w, stretch = ['lineatur', 'karo', 'text', 'table'].indexOf(it.type) >= 0;
      if (stretch && (Math.abs(right - (oR + dx)) < 1.5 || right > nR + 0.1)) {
        var w = Math.max(20, nR - it.x);
        if (it.type === 'karo') w = Math.max(it.cell || 5, Math.floor(w / (it.cell || 5)) * (it.cell || 5));
        it.w = r1(w);
      } else if (!stretch && right > nR + 6.1) it.x = r1(Math.max(0, nR + 6 - it.w));
    });
  }
  function frameChange(fn, allPages) {
    change(function () {
      var targets = allPages ? D.pages : [page()];
      var olds = targets.map(function (p) { return B.frameLayout(D, p); });
      fn();
      targets.forEach(function (p, k) { reanchor(p, olds[k], B.frameLayout(D, p)); });
    });
  }

  // ---------- Zeichnen ----------
  var numMap = {};
  function render() {
    numMap = B.numberItems(D);
    $('docTitle').value = D.title || '';
    var host = $('pages'), desk = $('desk'), keep = desk.scrollTop;
    host.style.minHeight = host.offsetHeight + 'px'; // verhindert Springen beim Neuaufbau
    host.innerHTML = '';
    D.pages.forEach(function (p, pi) { host.appendChild(renderPage(p, pi)); });
    host.appendChild(el('div', 'sel-layer')).id = 'selLayer';
    layout();
    host.style.minHeight = '';
    desk.scrollTop = keep;
    renderInspector();
    renderPagebar();
    if (editing && kcur) placeKInput(); else hideKInput();
    syncTables();
    if (editing && tcur) focusCell(false);
  }
  // Tabellen: Höhe folgt dem Inhalt (Zeilen wachsen mit dem Text)
  function syncTableH(d, it) {
    var t = d && d.querySelector('table'); if (!t) return false;
    var h = r1(t.offsetHeight / PX_MM);
    if (h > 0 && Math.abs(h - it.h) > 0.15) { it.h = h; placeItem(d, it); return true; }
    return false;
  }
  function syncTables() {
    var ch = false;
    D.pages.forEach(function (p) { p.items.forEach(function (it) { if (it.type === 'table' && syncTableH(itemEl(it.id), it)) ch = true; }); });
    if (ch) { drawSelection(); save(); }
  }
  function focusCell(caretEnd) {
    var it = editing && sel ? itemById(sel.pi, editing) : null, d = it && itemEl(it.id);
    if (!d || it.type !== 'table' || !tcur) return;
    var td = d.querySelector('td[data-r="' + tcur.r + '"][data-c="' + tcur.c + '"]');
    if (!td) return;
    Array.prototype.forEach.call(d.querySelectorAll('td.cur'), function (x) { x.classList.remove('cur'); }); td.classList.add('cur');
    if (document.activeElement !== td) { if (caretEnd === false) td.focus({ preventScroll: true }); else focusRow(td); }
  }

  // Zellen-Auswahl: Rechteck von tanc bis tcur
  function tRange(it) {
    if (!tcur) return null;
    var a = tanc || tcur, R = it ? it.rows - 1 : 99, C = it ? it.cols - 1 : 99;
    return { r0: Math.min(Math.min(a.r, tcur.r), R), r1: Math.min(Math.max(a.r, tcur.r), R), c0: Math.min(Math.min(a.c, tcur.c), C), c1: Math.min(Math.max(a.c, tcur.c), C) };
  }
  function tEach(it, fn) {
    var g = tRange(it); if (!g) return;
    for (var r = g.r0; r <= g.r1; r++) for (var c = g.c0; c <= g.c1; c++) fn(it.cells[r][c], r, c);
  }
  function tCount(it) { var g = tRange(it); return g ? (g.r1 - g.r0 + 1) * (g.c1 - g.c0 + 1) : 0; }
  function markRange(d, it) {
    var g = tRange(it), multi = tCount(it) > 1;
    Array.prototype.forEach.call(d.querySelectorAll('td'), function (td) {
      var r = Number(td.dataset.r), c = Number(td.dataset.c);
      td.classList.toggle('insel', !!(multi && editing === it.id && r >= g.r0 && r <= g.r1 && c >= g.c0 && c <= g.c1));
    });
  }
  function tableExtend(it, r, c) {
    if (!tcur) { tcur = { r: r, c: c }; return; }
    if (!tanc) tanc = { r: tcur.r, c: tcur.c };
    tcur = { r: r, c: c }; textend = false;
    var d = itemEl(it.id); if (d) markRange(d, it);
    focusCell(false); renderInspector();
  }

  function renderPage(p, pi) {
    var wrap = el('div', 'page-wrap'); wrap.dataset.pi = pi;
    var lbl = el('div', 'page-label' + (pi === cur ? ' cur' : ''), 'Seite ' + (pi + 1)); wrap.appendChild(lbl);
    var pg = el('div', 'page' + (!sel ? ' framemode' : '')); pg.dataset.pi = pi; wrap.appendChild(pg);
    var lay = B.frameLayout(D, p), s = D.setup;
    pg.insertAdjacentHTML('beforeend', '<svg class="frame" viewBox="0 0 210 297" aria-hidden="true">' + B.frameSvg(D, p, lay) + '</svg>');
    function box(cls, r, html) { var d = el('div', cls, html); d.style.left = r.x + 'mm'; d.style.top = r.y + 'mm'; d.style.width = r.w + 'mm'; d.style.height = r.h + 'mm'; pg.appendChild(d); return d; }
    var total = B.totalPoints(D);
    lay.cells.forEach(function (c) {
      var d = box('cell' + (c.line ? '' : ' mid'), c);
      d.appendChild(el('span', '', '')).textContent = c.label;
      if (c.line) d.appendChild(el('span', 'u'));
      if (c.key === 'seite') d.appendChild(el('span', 'val', String(pi + 1) + (D.pages.length > 1 ? ' / ' + D.pages.length : '')));
      if (c.key === 'punkte' && total > 0) d.appendChild(el('span', 'val', 'von ' + B.fmtPts(total)));
    });
    if (lay.title) {
      var t = box('ttl', lay.title); t.contentEditable = 'true'; t.spellcheck = true; t.dataset.ph = 'Titel eingeben'; t.dataset.role = 'title';
      t.textContent = p.frame.title.text || '';
    }
    if (lay.pointsCol) {
      lay.blocks.forEach(function (bl) {
        var d = box('pts' + (sel && sel.pi === pi && sel.block === bl.i ? ' sel' : ''), { x: lay.pointsCol.x, y: bl.y, w: lay.pointsCol.w, h: Math.min(bl.h, 24) },
          '<span class="wline"></span><span>/ ' + B.fmtPts(bl.points) + '</span>');
        d.dataset.block = bl.i; d.title = 'Punkte für diesen Aufgabenblock';
      });
    }
    if (lay.sum) {
      box('sum', { x: lay.sum.x, y: lay.sum.y, w: lay.sum.w, h: B.SUM_H },
        '<span><b>Gesamt:</b> ________ von ' + B.fmtPts(total) + ' Punkten</span>' + (p.frame.blocks.grades ? '<span><b>Note:</b> ________</span>' : ''));
      if (lay.sum.gradeH) {
        var r = B.gradeRanges(D), g = box('grades', { x: lay.sum.x, y: lay.sum.y + B.SUM_H, w: lay.sum.w, h: lay.sum.gradeH });
        g.style.gridTemplateColumns = '26mm repeat(' + r.length + ', 1fr)';
        g.innerHTML = '<div><span>Note</span><span>Punkte</span></div>' + r.map(function (x) { return '<div><b>' + x.note + '</b><span>' + B.rangeTxt(x) + '</span></div>'; }).join('');
      }
    }
    if (lay.footer) {
      var f = box('foot', lay.footer); f.contentEditable = 'true'; f.dataset.role = 'footer'; f.textContent = p.frame.footer.text || '';
    }
    lay.blocks.forEach(function (bl, i) {
      if (i === lay.blocks.length - 1) return;
      var dv = box('divider', { x: bl.x, y: bl.y + bl.h, w: bl.w, h: 5 }); dv.dataset.div = i; dv.style.height = ''; dv.title = 'Höhe der Aufgabenblöcke ziehen';
    });
    p.items.forEach(function (it) { pg.appendChild(renderItem(it, pi)); });
    pg.insertAdjacentHTML('beforeend', '<svg class="guides" viewBox="0 0 210 297" aria-hidden="true"></svg>');
    void s;
    return wrap;
  }

  function renderItem(it, pi) {
    var d = el('div', 'item ' + it.type); d.dataset.id = it.id; d.dataset.pi = pi;
    placeItem(d, it);
    fillItem(d, it);
    return d;
  }
  function placeItem(d, it) { d.style.left = it.x + 'mm'; d.style.top = it.y + 'mm'; d.style.width = it.w + 'mm'; d.style.height = it.h + 'mm'; }
  function fillItem(d, it) {
    var s = D.setup;
    if (it.type === 'number') {
      var r = it.w / 2, c = B.circlePath(r, r, r - 0.3, s.handdrawn, it.id);
      d.innerHTML = '<svg viewBox="0 0 ' + it.w + ' ' + it.h + '">' +
        (it.shadow ? '<path d="' + B.circlePath(r + 0.5, r + 0.5, r - 0.3, false) + '" fill="#c9ced6"/>' : '') +
        '<path d="' + c + '" fill="#fff" stroke="' + B.esc(s.lineColor) + '" stroke-width="' + s.lineWidth + '"/></svg><span class="num"></span>';
      d.lastChild.textContent = String(numMap[it.id] || it.value || '');
      d.lastChild.style.fontSize = (it.w * 1.2) + 'pt';
    } else if (it.type === 'text') {
      d.classList.toggle('border', !!it.border);
      d.innerHTML = '<div class="txt"></div>';
      var t = d.firstChild; t.innerHTML = it.html || ''; t.style.fontSize = (it.size || 14) + 'pt'; t.style.textAlign = it.align || 'left';
      if (editing === it.id) { d.classList.add('editing'); t.contentEditable = 'true'; t.spellcheck = true; }
    } else if (it.type === 'lineatur') {
      d.innerHTML = '<svg viewBox="0 0 ' + it.w + ' ' + it.h + '" preserveAspectRatio="none">' + B.lineaturSvg(it, Math.max(0.25, s.lineWidth * 0.75), false) + '</svg>';
      var mt = sheetMetrics(), lines = Array.isArray(it.lines) ? it.lines : [], ed = editing === it.id;
      B.lineaturTextRows(it, mt.x).forEach(function (r, i) {
        var lh = r.size * 1.25, top = r.base - ((lh - (mt.a + mt.d) * r.size) / 2 + mt.a * r.size);
        var row = el('div', 'lrow'); row.dataset.row = i;
        row.style.left = r.x + 'mm'; row.style.top = (Math.round(top * 100) / 100) + 'mm';
        row.style.height = row.style.lineHeight = (Math.round(lh * 100) / 100) + 'mm'; row.style.fontSize = (Math.round(r.size * 100) / 100) + 'mm';
        row.style.color = it.trace ? B.INK_TRACE : B.INK;
        row.textContent = lines[i] == null ? '' : String(lines[i]);
        if (ed) { row.contentEditable = 'true'; row.spellcheck = false; row.setAttribute('autocapitalize', 'off'); }
        d.appendChild(row);
      });
      d.classList.toggle('editing', ed);
    } else if (it.type === 'karo') {
      d.innerHTML = '<svg viewBox="0 0 ' + it.w + ' ' + it.h + '" preserveAspectRatio="none">' + B.karoSvg(it, editing === it.id ? kcur : null) + '</svg>';
      d.classList.toggle('editing', editing === it.id);
    } else if (it.type === 'table') {
      B.normTable(it);
      var ted = editing === it.id, sumW = it.colW.reduce(function (a, b) { return a + Number(b); }, 0);
      var bl = it.lineW + 'mm ' + it.lineStyle + ' ' + it.lineColor;
      var tb = el('table', 'tbl' + (it.lines === 'none' ? ' noline' : '')); tb.style.fontSize = it.size + 'pt';
      var cg = el('colgroup');
      it.colW.forEach(function (w) { var col = el('col'); col.style.width = (Number(w) / sumW * 100) + '%'; cg.appendChild(col); });
      tb.appendChild(cg);
      var tbody = el('tbody'); tb.appendChild(tbody);
      for (var tr = 0; tr < it.rows; tr++) {
        var row = el('tr'); tbody.appendChild(row);
        for (var tc = 0; tc < it.cols; tc++) {
          var cell = it.cells[tr][tc], td = el('td'), e = B.tableEdges(it, tr, tc);
          td.dataset.r = tr; td.dataset.c = tc;
          td.style.height = it.rowH[tr] + 'mm';
          td.style.padding = it.pad.map(function (v) { return (Number(v) || 0) + 'mm'; }).join(' ');
          td.style.textAlign = it.ha; td.style.verticalAlign = it.va;
          if (cell.bg) td.style.background = cell.bg;
          td.style.borderTop = e.t ? bl : 'none'; td.style.borderRight = e.r ? bl : 'none'; td.style.borderBottom = e.b ? bl : 'none'; td.style.borderLeft = e.l ? bl : 'none';
          if (cell.u) { td.style.borderBottom = r1(Math.max(0.6, Number(it.lineW) + 0.3)) + 'mm solid ' + it.lineColor; td.classList.add('under'); }
          td.innerHTML = cell.t || '';
          if (ted) { td.contentEditable = 'true'; td.spellcheck = true; if (tcur && tcur.r === tr && tcur.c === tc) td.classList.add('cur'); }
          row.appendChild(td);
        }
      }
      d.innerHTML = ''; d.appendChild(tb);
      d.classList.toggle('editing', ted);
      if (ted) markRange(d, it);
    } else if (it.type === 'image') {
      var src = it.asset && D.assets[it.asset];
      d.innerHTML = src ? '<img alt="">' : '<div class="ph">Bild antippen<br>oder hierher ziehen</div>';
      if (src) d.firstChild.src = src;
    }
  }

  // Maßstab: Seiten an die Breite anpassen oder fester Zoom
  function layout() {
    var desk = $('desk'), avail = desk.clientWidth - 48;
    var fit = Math.min(1.6, Math.max(0.3, avail / (210 * PX_MM)));
    scale = zoom === 'fit' ? fit : zoom;
    $('btnZoomFit').textContent = Math.round(scale * 100) + ' %';
    Array.prototype.forEach.call(document.querySelectorAll('.page-wrap'), function (w) {
      w.style.width = (210 * PX_MM * scale) + 'px'; w.style.height = (297 * PX_MM * scale) + 'px';
      w.querySelector('.page').style.transform = 'scale(' + scale + ')';
    });
    drawSelection();
  }

  // ---------- Auswahl, Griffe, schwebende Werkzeuge ----------
  function pageEl(pi) { return document.querySelector('.page[data-pi="' + pi + '"]'); }
  function toLayer(pi, xmm, ymm) {
    var w = document.querySelector('.page-wrap[data-pi="' + pi + '"]');
    return { x: w.offsetLeft + xmm * PX_MM * scale, y: w.offsetTop + ymm * PX_MM * scale };
  }
  function drawSelection() {
    var layer = $('selLayer'), fl = $('float');
    if (!layer) return;
    layer.innerHTML = '';
    var it = selItem();
    if (!it) { fl.hidden = true; return; }
    var a = toLayer(sel.pi, it.x, it.y), w = it.w * PX_MM * scale, h = it.h * PX_MM * scale;
    var box = el('div', 'selbox'); box.style.left = a.x + 'px'; box.style.top = a.y + 'px'; box.style.width = w + 'px'; box.style.height = h + 'px';
    layer.appendChild(box);
    if (editing !== it.id) {
      var dirs = it.type === 'number' ? ['se'] : it.type === 'image' ? ['nw', 'ne', 'sw', 'se'] : ['nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w'];
      dirs.forEach(function (dname) {
        var hd = el('div', 'handle'); hd.dataset.dir = dname;
        hd.style.left = (a.x + (dname.indexOf('w') >= 0 ? 0 : dname.indexOf('e') >= 0 ? w : w / 2)) + 'px';
        hd.style.top = (a.y + (dname.indexOf('n') >= 0 ? 0 : dname.indexOf('s') >= 0 ? h : h / 2)) + 'px';
        layer.appendChild(hd);
      });
    }
    fl.hidden = false;
    $('fEdit').hidden = WRITABLE.indexOf(it.type) < 0 || editing === it.id;
    var fx = a.x + w / 2, fy = a.y - 52;
    if (fy < 4) fy = a.y + h + 14;
    fl.style.left = '0px'; fl.style.top = '0px';
    var pages = $('pages');
    fl.style.left = clamp(fx - fl.offsetWidth / 2 + pages.offsetLeft, 6, $('desk').scrollWidth - fl.offsetWidth - 6) + 'px';
    fl.style.top = (fy + pages.offsetTop) + 'px';
  }
  function select(s) {
    if (editing && (!s || s.id !== editing)) stopEdit();
    sel = s;
    if (s) setCur(s.pi);
    Array.prototype.forEach.call(document.querySelectorAll('.page'), function (p) { p.classList.toggle('framemode', !sel); });
    Array.prototype.forEach.call(document.querySelectorAll('.pts'), function (p) {
      p.classList.toggle('sel', !!(sel && sel.block !== undefined && Number(p.closest('.page').dataset.pi) === sel.pi && Number(p.dataset.block) === sel.block));
    });
    drawSelection(); renderInspector();
  }
  function setCur(pi) {
    if (pi === cur) return;
    cur = pi;
    Array.prototype.forEach.call(document.querySelectorAll('.page-label'), function (l, i) { l.classList.toggle('cur', i === cur); });
    renderPagebar();
    if (!sel) renderInspector();
  }

  // ---------- Textfelder bearbeiten ----------
  function startEdit(id, at) {
    var it = itemById(sel.pi, id); if (!it || WRITABLE.indexOf(it.type) < 0) return;
    if (editing && editing !== id) stopEdit();
    if (editing === id) return;
    editing = id; editBefore = snap();
    var d = itemEl(id);
    d.classList.add('editing');
    if (it.type === 'text') {
      var t = d.querySelector('.txt'); t.contentEditable = 'true'; t.spellcheck = true;
      t.focus();
      try { var r = document.createRange(); r.selectNodeContents(t); r.collapse(false); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); } catch (e) { /* egal */ }
    } else if (it.type === 'lineatur') {
      fillItem(d, it);
      var tr = B.lineaturTextRows(it, sheetMetrics().x), i = 0;
      if (at) { var ly = at.y - it.y; i = tr.length - 1; for (var k = 0; k < tr.length; k++) if (ly <= tr[k].base + 2) { i = k; break; } }
      focusRow(d.querySelectorAll('.lrow')[i]);
    } else if (it.type === 'table') {
      tcur = { r: 0, c: 0 }; tanc = null; textend = false;
      if (at) {
        var trs = d.querySelectorAll('tr'), sw = 0, tw = it.colW.reduce(function (a, b) { return a + Number(b); }, 0), fx = (at.x - it.x) / it.w;
        Array.prototype.forEach.call(trs, function (row, k) { if (it.y + row.offsetTop / PX_MM <= at.y) tcur.r = k; });
        for (var cc = 0; cc < it.cols; cc++) { if (fx >= sw / tw) tcur.c = cc; sw += Number(it.colW[cc]); }
      }
      fillItem(d, it); focusCell(true);
    } else if (it.type === 'karo') {
      var g = B.karoSize(it), lx = at ? at.x - it.x : 0, ly2 = at ? at.y - it.y : 0;
      kcur = { r: clamp(Math.floor(ly2 / g.s), 0, Math.max(0, g.ny - 1)), c: clamp(Math.floor(lx / g.s), 0, Math.max(0, g.nx - 1)) }; kcur.c0 = kcur.c;
      fillItem(d, it); placeKInput(true);
    }
    drawSelection(); renderInspector();
  }
  function focusRow(row) {
    if (!row) return;
    row.focus();
    try { var r = document.createRange(); r.selectNodeContents(row); r.collapse(false); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); } catch (e) { /* egal */ }
  }
  function stopEdit() {
    if (!editing) return;
    var id = editing, d = itemEl(id), before = editBefore;
    editing = null; editBefore = null;
    var it = d ? itemById(Number(d.dataset.pi), id) : null;
    if (it && it.type === 'text') {
      var t = d.querySelector('.txt'), html = cleanHtml(t.innerHTML);
      if (html !== it.html) change(function () { it.html = html; }, { render: false });
      t.contentEditable = 'false';
    } else {
      if (before && snap() !== before) { undoStack.push(before); if (undoStack.length > 60) undoStack.shift(); redoStack = []; updateUndo(); save(); }
      kcur = null; tcur = null; tanc = null; textend = false; hideKInput();
      if (it && d) { fillItem(d, it); if (it.type === 'table') syncTableH(d, it); }
    }
    if (d) d.classList.remove('editing');
  }

  // ---------- In Kästchen schreiben: ein Zeichen je Kästchen ----------
  var SENT = '\u200b';
  function editKaro() { var it = editing && sel ? itemById(sel.pi, editing) : null; return it && it.type === 'karo' && kcur ? it : null; }
  function hideKInput() { var k = $('kIn'); if (k && !k.hidden) { k.hidden = true; if (document.activeElement === k) k.blur(); } }
  function placeKInput(focus) {
    var k = $('kIn'), it = editKaro(); if (!k || !it) return;
    var g = B.karoSize(it), a = toLayer(sel.pi, it.x + kcur.c * g.s, it.y + kcur.r * g.s), pages = $('pages');
    k.hidden = false; k.style.left = (a.x + pages.offsetLeft) + 'px'; k.style.top = (a.y + pages.offsetTop) + 'px';
    if (k.value !== SENT) k.value = SENT;
    if (focus || document.activeElement !== k) { try { k.focus({ preventScroll: true }); } catch (e) { k.focus(); } }
    try { k.setSelectionRange(1, 1); } catch (e) { /* egal */ }
  }
  function refreshKaro(it) { var d = itemEl(it.id); if (d) fillItem(d, it); placeKInput(); save(); }
  function karoMove(it, dr, dc, keepStart) {
    var g = B.karoSize(it);
    kcur.r = clamp(kcur.r + dr, 0, Math.max(0, g.ny - 1)); kcur.c = clamp(kcur.c + dc, 0, Math.max(0, g.nx - 1));
    if (!keepStart) kcur.c0 = kcur.c;
  }
  function karoPut(it, ch) {
    var g = B.karoSize(it), key = kcur.r + ',' + kcur.c;
    if (!it.cells || typeof it.cells !== 'object') it.cells = {};
    if (ch === ' ') delete it.cells[key]; else it.cells[key] = ch;
    if (kcur.c < g.nx - 1) kcur.c++;
    else if (kcur.r < g.ny - 1) { kcur.r++; kcur.c = kcur.c0 < g.nx - 1 ? kcur.c0 : 0; }
  }
  function karoBack(it) {
    if (!it.cells) it.cells = {};
    if (kcur.c > 0 && !it.cells[kcur.r + ',' + kcur.c]) kcur.c--;
    delete it.cells[kcur.r + ',' + kcur.c];
  }
  function toggleUnder(it) {
    var u = Array.isArray(it.under) ? it.under.slice() : [], i = u.indexOf(kcur.r);
    if (i >= 0) u.splice(i, 1); else u.push(kcur.r);
    it.under = u; refreshKaro(it); renderInspector();
  }
  function setupKaroInput() {
    var k = document.createElement('input'); k.id = 'kIn'; k.className = 'kin'; k.type = 'text'; k.hidden = true;
    k.autocomplete = 'off'; k.spellcheck = false; k.setAttribute('autocapitalize', 'off'); k.setAttribute('autocorrect', 'off');
    k.setAttribute('aria-label', 'In die Kästchen schreiben');
    $('desk').appendChild(k);
    k.addEventListener('input', function (e) {
      var it = editKaro(); if (!it) { k.value = SENT; return; }
      var v = k.value.replace(/\u200b/g, '');
      if (e.inputType === 'deleteContentBackward' || (!v && k.value.length < SENT.length)) karoBack(it);
      else Array.from(v).forEach(function (ch) { if (ch === '\n' || ch === '\r') return; karoPut(it, ch); });
      k.value = SENT; refreshKaro(it);
    });
    k.addEventListener('keydown', function (e) {
      var it = editKaro(); if (!it) return;
      var mv = { ArrowLeft: [0, -1], ArrowRight: [0, 1], ArrowUp: [-1, 0], ArrowDown: [1, 0] }[e.key];
      if (mv) { e.preventDefault(); karoMove(it, mv[0], mv[1]); refreshKaro(it); return; }
      if (e.key === 'Enter') { e.preventDefault(); var g = B.karoSize(it); if (kcur.r < g.ny - 1) { kcur.r++; kcur.c = kcur.c0; } refreshKaro(it); return; }
      if (e.key === 'Tab') { e.preventDefault(); karoMove(it, 0, e.shiftKey ? -1 : 1); refreshKaro(it); }
    });
  }
  function karoTap(e, it) {
    var g = B.karoSize(it), m = mmAt(sel.pi, e.clientX, e.clientY);
    kcur.r = clamp(Math.floor((m.y - it.y) / g.s), 0, Math.max(0, g.ny - 1)); kcur.c = clamp(Math.floor((m.x - it.x) / g.s), 0, Math.max(0, g.nx - 1)); kcur.c0 = kcur.c;
    var d = itemEl(it.id); fillItem(d, it); placeKInput(true); renderInspector();
  }
  function growText(d, it) {
    var t = d.querySelector('.txt'), need = t.scrollHeight / PX_MM;
    if (need > it.h + 0.3) { it.h = r1(need + 1); placeItem(d, it); drawSelection(); }
  }

  // ---------- Elemente hinzufügen ----------
  function slotFor(kind) {
    var p = page(), lay = B.frameLayout(D, p), s = selItem();
    var area = lay.blocks.length ? lay.blocks : [lay.free];
    var isNum = kind === 'number';
    if (s && sel.pi === cur && !isNum) {
      var bx = lay.blocks.length ? lay.blocks.filter(function (b) { return s.y >= b.y - 1 && s.y < b.y + b.h; })[0] : lay.free;
      var nx = s.type === 'number' ? s.x + 16 : s.x, ny = s.type === 'number' ? s.y - 1.5 : s.y + s.h + 4;
      var right = (lay.pointsCol ? lay.pointsCol.x : lay.box.x + lay.box.w) - 6;
      return { x: nx, y: ny, w: Math.max(30, right - nx), maxH: bx ? bx.y + bx.h - ny - 3 : 40 };
    }
    function has(b, types) {
      return p.items.some(function (it) { return types.indexOf(it.type) >= 0 && it.y + it.h / 2 >= b.y && it.y + it.h / 2 < b.y + b.h; });
    }
    var target = area.filter(function (b) { return !has(b, isNum ? ['number'] : ['lineatur', 'karo', 'text', 'image', 'table']); })[0] || area[area.length - 1];
    if (lay.blocks.length) {
      var sl = B.blockSlots(lay, target);
      return isNum ? { x: sl.numX, y: sl.numY } : { x: sl.cx, y: sl.cy, w: sl.cw, maxH: target.y + target.h - sl.cy - 4 };
    }
    return { x: target.x + 10, y: target.y + 10, w: target.w - 20, maxH: 60 };
  }
  function makeItem(kind, at) {
    var it;
    if (kind === 'number') it = B.newItem('number', { x: at.x, y: at.y });
    else if (kind === 'text') it = B.newItem('text', { x: at.x, y: at.y, w: at.w || 120, h: 12, size: 14 });
    else if (kind === 'karo') { it = B.newItem('karo', { x: at.x, y: at.y }); it.w = Math.floor((at.w || 140) / 5) * 5; it.h = clamp(Math.floor((at.maxH || 30) / 5) * 5, 10, 30); }
    else if (kind === 'image') it = B.newItem('image', { x: at.x, y: at.y });
    else if (kind === 'table') { it = B.newItem('table', { x: at.x, y: at.y, w: r1(at.w || 140) }); it.h = it.rowH.reduce(function (a, b) { return a + b; }, 0); }
    else {
      it = B.newItem('lineatur', { kind: kind, x: at.x, y: at.y, w: at.w || 140 });
      var rows = kind === 'L1' ? 2 : 3;
      while (rows > 1 && B.lineaturHeightFor(it, rows) > (at.maxH || 99)) rows--;
      it.h = B.lineaturHeightFor(it, rows);
    }
    it.x = r1(clamp(it.x, 0, 210 - Math.min(it.w, 200))); it.y = r1(clamp(it.y, 0, 297 - 5));
    return it;
  }
  function addTool(kind, at, pi) {
    if (pi === undefined) pi = cur;
    var a = at || slotFor(kind);
    var it = makeItem(kind, a);
    change(function () { D.pages[pi].items.push(it); sel = { pi: pi, id: it.id }; cur = pi; });
    if (kind === 'image') pickImage(it.id);
    if (kind === 'text') startEdit(it.id);
    scrollIntoView(it);
  }
  function scrollIntoView(it) {
    var a = toLayer(sel.pi, it.x, it.y), desk = $('desk'), top = a.y + $('pages').offsetTop;
    if (top < desk.scrollTop + 20 || top > desk.scrollTop + desk.clientHeight - 140) desk.scrollTo({ top: Math.max(0, top - 120), behavior: 'smooth' });
  }

  // ---------- Bilder ----------
  var pickTarget = null;
  function pickImage(id) { pickTarget = id; $('fileImg').value = ''; $('fileImg').click(); }
  function readImage(file) {
    return new Promise(function (res, rej) {
      var fr = new FileReader();
      fr.onload = function () {
        var img = new Image();
        img.onload = function () {
          var max = 1600, w = img.naturalWidth, h = img.naturalHeight, k = Math.min(1, max / Math.max(w, h));
          var cw = Math.max(1, Math.round(w * k)), ch = Math.max(1, Math.round(h * k)), cv = document.createElement('canvas');
          cv.width = cw; cv.height = ch; var ctx = cv.getContext('2d'), png = /png|gif|svg/.test(file.type);
          if (!png) { ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, cw, ch); }
          ctx.drawImage(img, 0, 0, cw, ch);
          res({ src: png ? cv.toDataURL('image/png') : cv.toDataURL('image/jpeg', 0.88), w: cw, h: ch });
        };
        img.onerror = function () { rej(new Error('kein Bild')); };
        img.src = fr.result;
      };
      fr.onerror = function () { rej(fr.error); };
      fr.readAsDataURL(file);
    });
  }
  function placeImage(file, targetId, pi, at) {
    return readImage(file).then(function (r) {
      var aid = B.uid();
      change(function () {
        D.assets[aid] = r.src;
        var it = targetId && itemById(pi, targetId);
        if (!it) { it = makeItem('image', at || slotFor('image')); D.pages[pi].items.push(it); }
        var ratio = r.h / r.w;
        it.asset = aid; it.natW = r.w; it.natH = r.h;
        it.w = r1(Math.min(it.w > 20 ? it.w : 60, 120)); it.h = r1(it.w * ratio);
        if (it.h > 120) { it.h = 120; it.w = r1(120 / ratio); }
        sel = { pi: pi, id: it.id };
      });
    }, function () { toast('Dieses Bild ließ sich nicht öffnen. Versuche ein JPG oder PNG.'); });
  }

  // ---------- Zeigerereignisse: Auswählen, Verschieben, Größe ändern ----------
  var drag = null;
  function mmAt(pi, cx, cy) {
    var r = pageEl(pi).getBoundingClientRect();
    return { x: (cx - r.left) * 210 / r.width, y: (cy - r.top) * 297 / r.height };
  }
  function pageAt(cx, cy) {
    var pages = document.querySelectorAll('.page');
    for (var i = 0; i < pages.length; i++) {
      var r = pages[i].getBoundingClientRect();
      if (cx >= r.left && cx <= r.right && cy >= r.top && cy <= r.bottom) return Number(pages[i].dataset.pi);
    }
    return -1;
  }
  function guidesFor(pi, exceptId) {
    var p = D.pages[pi], lay = B.frameLayout(D, p), gx = [lay.box.x, lay.box.x + 9, lay.box.x + 25, lay.box.x + lay.box.w, lay.box.x + lay.box.w - 6], gy = [];
    if (lay.pointsCol) gx.push(lay.pointsCol.x, lay.pointsCol.x - 6);
    lay.blocks.forEach(function (b) { gy.push(b.y, b.y + 10, b.y + 11.5, b.y + b.h); });
    if (lay.free) gy.push(lay.free.y, lay.free.y + lay.free.h);
    p.items.forEach(function (it) { if (it.id !== exceptId) { gx.push(it.x, it.x + it.w); gy.push(it.y, it.y + it.h); } });
    return { x: gx, y: gy };
  }
  function snapVal(vals, guides, th) {
    var best = null;
    vals.forEach(function (v, i) { guides.forEach(function (g) { var d = g - v; if (Math.abs(d) <= th && (!best || Math.abs(d) < Math.abs(best.d))) best = { d: d, g: g, i: i }; }); });
    return best;
  }
  function showGuides(pi, gx, gy) {
    var svg = pageEl(pi).querySelector('svg.guides'), h = '';
    if (gx !== null && gx !== undefined) h += '<line x1="' + gx + '" y1="0" x2="' + gx + '" y2="297" stroke="#2f6fe4" stroke-width="0.25" stroke-dasharray="1.5 1"/>';
    if (gy !== null && gy !== undefined) h += '<line x1="0" y1="' + gy + '" x2="210" y2="' + gy + '" stroke="#2f6fe4" stroke-width="0.25" stroke-dasharray="1.5 1"/>';
    svg.innerHTML = h;
  }

  function setupPointer() {
    var desk = $('desk');
    desk.addEventListener('pointerdown', function (e) {
      if (e.button > 0) return;
      var t = e.target;
      var hd = t.closest('.handle');
      if (hd && sel && sel.id) { e.preventDefault(); beginDrag(e, 'resize', hd.dataset.dir); return; }
      if (t.closest('.float')) return;
      var itEl = t.closest('.item');
      if (itEl) {
        var pi = Number(itEl.dataset.pi), id = itEl.dataset.id;
        var tdx = editing === id && t.closest('td');
        if (tdx && (e.shiftKey || textend) && tcur) { e.preventDefault(); tableExtend(itemById(pi, id), Number(tdx.dataset.r), Number(tdx.dataset.c)); return; }
        if (tdx && e.pointerType !== 'touch') tdrag = { pid: e.pointerId, pi: pi, id: id, r: Number(tdx.dataset.r), c: Number(tdx.dataset.c), on: false };
        if (editing === id && (t.closest('.txt') || t.closest('.lrow') || t.closest('td'))) return; // Schreiben: Browser übernimmt
        if (editing === id && itEl.classList.contains('karo')) { e.preventDefault(); karoTap(e, itemById(pi, id)); return; }
        e.preventDefault();
        var was = sel && sel.id === id;
        if (!was) select({ pi: pi, id: id });
        beginDrag(e, 'move', null, was);
        return;
      }
      var pts = t.closest('.pts');
      if (pts) { e.preventDefault(); select({ pi: Number(pts.closest('.page').dataset.pi), block: Number(pts.dataset.block) }); return; }
      var dv = t.closest('.divider');
      if (dv) { e.preventDefault(); select(null); beginDrag(e, 'divider', Number(dv.dataset.div)); setCur(Number(dv.closest('.page').dataset.pi)); return; }
      var pg = t.closest('.page');
      if (pg) { setCur(Number(pg.dataset.pi)); if (!t.closest('[contenteditable=true]')) select(null); else if (sel) select(null); return; }
      if (!t.closest('.page-wrap')) select(null);
    });
    document.addEventListener('pointermove', function (e) {
      if (drag && e.pointerId === drag.pid) moveDrag(e);
      if (tdrag && e.pointerId === tdrag.pid && e.buttons) {
        var over = document.elementFromPoint(e.clientX, e.clientY), od = over && over.closest && over.closest('.item.table td');
        if (!od || od.closest('.item').dataset.id !== tdrag.id || editing !== tdrag.id) return;
        var r = Number(od.dataset.r), c = Number(od.dataset.c), ti = itemById(tdrag.pi, tdrag.id);
        if (!tdrag.on && r === tdrag.r && c === tdrag.c) return;
        if (!tdrag.on) { tdrag.on = true; tcur = { r: tdrag.r, c: tdrag.c }; tanc = null; }
        try { window.getSelection().removeAllRanges(); } catch (x) { /* egal */ }
        if (!tcur || tcur.r !== r || tcur.c !== c || !tanc) tableExtend(ti, r, c);
      }
    });
    document.addEventListener('pointerup', function (e) { if (drag && e.pointerId === drag.pid) endDrag(e); if (tdrag && e.pointerId === tdrag.pid) tdrag = null; });
    document.addEventListener('pointercancel', function (e) { if (drag && e.pointerId === drag.pid) endDrag(e, true); });
  }
  function beginDrag(e, mode, arg, wasSelected) {
    var pi = mode === 'divider' ? Number(e.target.closest('.page').dataset.pi) : sel.pi;
    var it = mode === 'divider' ? null : selItem();
    drag = { mode: mode, arg: arg, pid: e.pointerId, pi: pi, sx: e.clientX, sy: e.clientY, start: mmAt(pi, e.clientX, e.clientY),
      orig: it ? B.clone(it) : null, moved: false, was: wasSelected, before: snap() };
    if (mode === 'divider') {
      var p = D.pages[pi], lay = B.frameLayout(D, p);
      drag.heights = lay.blocks.map(function (b) { return b.h; });
      drag.lay0 = lay; drag.items0 = B.clone(p.items);
    }
    try { e.target.setPointerCapture(e.pointerId); } catch (err) { /* egal */ }
  }
  function moveDrag(e) {
    var dpx = Math.hypot(e.clientX - drag.sx, e.clientY - drag.sy);
    if (!drag.moved && dpx < 4) return;
    drag.moved = true;
    var m = mmAt(drag.pi, e.clientX, e.clientY), dx = m.x - drag.start.x, dy = m.y - drag.start.y;
    var p = D.pages[drag.pi];
    if (drag.mode === 'divider') {
      var i = drag.arg, h = drag.heights.slice(), tot = h[i] + h[i + 1];
      h[i] = clamp(drag.heights[i] + dy, 15, tot - 15); h[i + 1] = tot - h[i];
      p.frame.blocks.weights = h.map(r1);
      p.items = B.clone(drag.items0);
      reanchor(p, drag.lay0, B.frameLayout(D, p));
      refreshPage(drag.pi);
      return;
    }
    var it = selItem(), o = drag.orig, g = guidesFor(drag.pi, it.id), th = 1.6, sx = null, sy = null;
    if (drag.mode === 'move') {
      var nx = Math.round((o.x + dx) * 2) / 2, ny = Math.round((o.y + dy) * 2) / 2;
      var bx = snapVal([nx, nx + o.w], g.x, th), by = snapVal([ny, ny + o.h], g.y, th);
      if (bx) { nx += bx.d; sx = bx.g; } if (by) { ny += by.d; sy = by.g; }
      it.x = r1(clamp(nx, -o.w + 5, 205)); it.y = r1(clamp(ny, -o.h + 5, 292));
    } else {
      var dir = drag.arg, x1 = o.x, y1 = o.y, x2 = o.x + o.w, y2 = o.y + o.h;
      if (dir.indexOf('w') >= 0) x1 = o.x + dx; if (dir.indexOf('e') >= 0) x2 = o.x + o.w + dx;
      if (dir.indexOf('n') >= 0) y1 = o.y + dy; if (dir.indexOf('s') >= 0) y2 = o.y + o.h + dy;
      var sxv = snapVal([dir.indexOf('w') >= 0 ? x1 : x2], g.x, th), syv = snapVal([dir.indexOf('n') >= 0 ? y1 : y2], g.y, th);
      if (sxv && dir.match(/[we]/)) { if (dir.indexOf('w') >= 0) x1 += sxv.d; else x2 += sxv.d; sx = sxv.g; }
      if (syv && dir.match(/[ns]/)) { if (dir.indexOf('n') >= 0) y1 += syv.d; else y2 += syv.d; sy = syv.g; }
      var w = Math.max(6, x2 - x1), h2 = Math.max(4, y2 - y1);
      if (it.type === 'number') { var s = clamp(Math.max(w, h2), 6, 24); w = s; h2 = s; }
      if (it.type === 'image' && o.natW) { var ratio = o.h / o.w; if (Math.abs(dx) > Math.abs(dy)) h2 = w * ratio; else w = h2 / ratio; }
      if (it.type === 'karo') { var c = it.cell || 5; w = Math.max(c, Math.round(w / c) * c); h2 = Math.max(c, Math.round(h2 / c) * c); }
      if (it.type === 'table') {
        var sumO = o.rowH.reduce(function (a, b) { return a + Number(b); }, 0) || 1;
        it.rowH = o.rowH.map(function (x) { return Math.max(4, r1(Number(x) * h2 / sumO)); }); w = Math.max(20, w);
      }
      if (it.type === 'lineatur') {
        var n = 1; while (B.lineaturHeightFor(it, n + 1) <= h2 + 2) n++;
        h2 = B.lineaturHeightFor(it, n); w = Math.max(20, w);
      }
      it.w = r1(w); it.h = r1(h2);
      it.x = r1(dir.indexOf('w') >= 0 ? x2 - it.w : x1); it.y = r1(dir.indexOf('n') >= 0 ? y2 - it.h : y1);
    }
    var d = document.querySelector('.item[data-id="' + it.id + '"]');
    placeItem(d, it);
    if (drag.mode === 'resize' && it.type !== 'text') { fillItem(d, it); if (it.type === 'table') syncTableH(d, it); }
    showGuides(drag.pi, sx, sy);
    drawSelection();
  }
  function endDrag(e, cancel) {
    var d = drag; drag = null;
    if (!d) return;
    if (d.mode !== 'divider') showGuides(d.pi, null, null);
    if (!d.moved) {
      if (!cancel && d.mode === 'move' && d.was) {
        var it = selItem();
        if (it && WRITABLE.indexOf(it.type) >= 0) startEdit(it.id, d.start);
        else if (it && it.type === 'image' && !it.asset) pickImage(it.id);
      } else if (!cancel && d.mode === 'move') {
        var it2 = selItem();
        if (it2 && it2.type === 'image' && !it2.asset) pickImage(it2.id);
      }
      return;
    }
    if (cancel) { restore(d.before); render(); return; }
    undoStack.push(d.before); if (undoStack.length > 60) undoStack.shift(); redoStack = [];
    save(); updateUndo();
    if (d.mode === 'move') { // Nummern können sich durch die Reihenfolge ändern
      numMap = B.numberItems(D);
      Array.prototype.forEach.call(document.querySelectorAll('.item.number'), function (n) { n.querySelector('.num').textContent = String(numMap[n.dataset.id] || ''); });
      var it3 = selItem();
      if (it3 && (it3.y > 297 || it3.y + it3.h < 0)) render();
    }
    renderInspector();
  }
  function refreshPage(pi) {
    var old = document.querySelector('.page-wrap[data-pi="' + pi + '"]');
    var nw = renderPage(D.pages[pi], pi);
    old.parentNode.replaceChild(nw, old);
    layout();
  }

  // ---------- Ziehen aus der Elementleiste ----------
  function setupPalette() {
    var tdrag = null;
    Array.prototype.forEach.call(document.querySelectorAll('[data-add]'), function (b) {
      b.addEventListener('pointerdown', function (e) {
        if (e.button > 0) return;
        e.preventDefault();
        tdrag = { kind: b.dataset.add, sx: e.clientX, sy: e.clientY, pid: e.pointerId, ghost: null, label: b.textContent.trim() };
        try { b.setPointerCapture(e.pointerId); } catch (err) { /* egal */ }
      });
      b.addEventListener('pointermove', function (e) {
        if (!tdrag || e.pointerId !== tdrag.pid) return;
        if (!tdrag.ghost && Math.hypot(e.clientX - tdrag.sx, e.clientY - tdrag.sy) > 8) {
          tdrag.ghost = el('div', 'ghost-tool'); tdrag.ghost.textContent = tdrag.label; document.body.appendChild(tdrag.ghost);
        }
        if (tdrag.ghost) { tdrag.ghost.style.left = e.clientX + 'px'; tdrag.ghost.style.top = e.clientY + 'px'; }
      });
      function fin(e, cancel) {
        if (!tdrag || e.pointerId !== tdrag.pid) return;
        var t = tdrag; tdrag = null;
        if (t.ghost) {
          t.ghost.remove();
          if (cancel) return;
          var pi = pageAt(e.clientX, e.clientY);
          if (pi < 0) return;
          var m = mmAt(pi, e.clientX, e.clientY), p = D.pages[pi], lay = B.frameLayout(D, p);
          var right = (lay.pointsCol ? lay.pointsCol.x : lay.box.x + lay.box.w) - 6;
          var at = { x: m.x - 3, y: m.y - 3, w: Math.max(30, right - (m.x - 3)), maxH: 40 };
          if (t.kind === 'number') { at.x = m.x - 4.6; at.y = m.y - 4.6; }
          addTool(t.kind, at, pi);
        } else if (!cancel) { addTool(t.kind); }
      }
      b.addEventListener('pointerup', function (e) { fin(e); });
      b.addEventListener('pointercancel', function (e) { fin(e, true); });
    });
  }

  // ---------- Drag-and-Drop von außen und Einfügen ----------
  function setupDrop() {
    var desk = $('desk');
    desk.addEventListener('dragover', function (e) { if (e.dataTransfer && Array.prototype.indexOf.call(e.dataTransfer.types, 'Files') >= 0) e.preventDefault(); });
    desk.addEventListener('drop', function (e) {
      var files = Array.prototype.filter.call((e.dataTransfer && e.dataTransfer.files) || [], function (f) { return /^image\//.test(f.type); });
      if (!files.length) return;
      e.preventDefault();
      var pi = pageAt(e.clientX, e.clientY); if (pi < 0) pi = cur;
      var m = mmAt(pi, e.clientX, e.clientY);
      var ph = e.target.closest && e.target.closest('.item.image');
      var target = ph && !itemById(pi, ph.dataset.id).asset ? ph.dataset.id : null;
      var p = Promise.resolve();
      files.forEach(function (f, i) { p = p.then(function () { return placeImage(f, i === 0 ? target : null, pi, { x: m.x + i * 6, y: m.y + i * 6 }); }); });
    });
    document.addEventListener('paste', function (e) {
      var cd = e.clipboardData; if (!cd) return;
      var img = Array.prototype.find.call(cd.items || [], function (it) { return it.kind === 'file' && /^image\//.test(it.type); });
      if (img) { e.preventDefault(); var s = selItem(); placeImage(img.getAsFile(), s && s.type === 'image' && !s.asset ? s.id : null, cur); return; }
      if (e.target.closest && e.target.closest('[contenteditable=true]')) {
        e.preventDefault(); document.execCommand('insertText', false, cd.getData('text/plain') || '');
      }
    });
  }

  // ---------- Eigenschaften ----------
  function renderInspector() {
    var box = $('insp'); box.innerHTML = '';
    var head = el('div', 'row'); head.style.justifyContent = 'space-between'; head.style.flexWrap = 'nowrap';
    var hl = el('div');
    var closeBtn = el('button', 'btn icon ghost close-insp', icon('x')); closeBtn.setAttribute('aria-label', 'Schließen');
    closeBtn.onclick = function () { $('insp').classList.remove('open'); };
    head.appendChild(hl); head.appendChild(closeBtn); box.appendChild(head);
    frameMode = false;
    var it = selItem();
    if (it) { inspectItem(box, hl, it); return; }
    if (sel && sel.block !== undefined) inspectPoints(box, hl);
    inspectFrame(box, sel && sel.block !== undefined ? null : hl);
  }
  function title(hl, t, sub) { if (!hl) return; hl.innerHTML = '<h2></h2>' + (sub ? '<p class="sub"></p>' : ''); hl.firstChild.textContent = t; if (sub) hl.lastChild.textContent = sub; }
  function sec(box, h) { var s = el('div', 'sec'); if (h) s.appendChild(el('h4', '', h)); box.appendChild(s); return s; }
  var frameMode = false; // Steuerelemente des Seitenrahmens verschieben Elemente mit
  function apply(fn) { if (frameMode) frameChange(fn); else change(fn); }
  function chk(parent, label, val, fn, id) {
    var l = el('label', 'chk'), i = document.createElement('input'); i.type = 'checkbox'; i.checked = !!val; if (id) i.id = id;
    i.onchange = function () { apply(function () { fn(i.checked); }); };
    l.appendChild(i); l.appendChild(document.createTextNode(label)); parent.appendChild(l); return i;
  }
  function stepper(parent, label, val, step, min, max, show, fn) {
    var row = el('div', 'row'), lb = el('label'); lb.textContent = label; row.appendChild(lb);
    var w = el('div', 'stepper'), mi = el('button', '', '−'), out = el('output'), pl = el('button', '', '+');
    mi.setAttribute('aria-label', label + ' weniger'); pl.setAttribute('aria-label', label + ' mehr'); out.textContent = show(val);
    [mi, pl].forEach(function (b, k) {
      b.onclick = function () { var nv = clamp(Math.round((Number(val) + (k ? step : -step)) * 100) / 100, min, max); if (nv === val) return; val = nv; apply(function () { fn(nv); }); };
    });
    w.appendChild(mi); w.appendChild(out); w.appendChild(pl); row.appendChild(w); parent.appendChild(row); return row;
  }
  function seg(parent, opts, val, fn, label) {
    var s = el('div', 'seg'); s.setAttribute('role', 'group'); if (label) s.setAttribute('aria-label', label);
    opts.forEach(function (o) { var b = el('button', ''); b.textContent = o[1]; b.setAttribute('aria-pressed', String(o[0] === val)); b.onclick = function () { if (o[0] !== val) change(function () { fn(o[0]); }); }; s.appendChild(b); });
    parent.appendChild(s); return s;
  }
  function numInput(parent, label, val, fn, step) {
    var row = el('div', 'row'), lb = el('label'), i = document.createElement('input');
    lb.textContent = label; i.type = 'number'; i.className = 'inp num'; i.step = step || 0.5; i.value = val; i.inputMode = 'decimal';
    i.onchange = function () { var v = parseFloat(String(i.value).replace(',', '.')); if (!isNaN(v)) change(function () { fn(v); }); };
    row.appendChild(lb); row.appendChild(i); parent.appendChild(row); return i;
  }
  function colors(parent, val, fn, list) {
    var s = el('div', 'swatches');
    (list || LINE_COLORS).forEach(function (c) { var b = el('button', 'swatch'); b.style.background = c; b.setAttribute('aria-label', 'Farbe ' + c); b.setAttribute('aria-pressed', String(c.toLowerCase() === String(val).toLowerCase())); b.onclick = function () { change(function () { fn(c); }); }; s.appendChild(b); });
    parent.appendChild(s);
  }

  function inspectFrame(box, hl) {
    var p = page(), f = p.frame;
    frameMode = true;
    title(hl, 'Seitenrahmen', 'Seite ' + (cur + 1) + ' von ' + D.pages.length);
    var s1 = sec(box, 'Kopfzeile');
    var g = el('div', 'chks'); s1.appendChild(g);
    B.HEADER_FIELDS.forEach(function (hf) { chk(g, hf[1].replace(':', ''), f.header[hf[0]], function (v) { f.header[hf[0]] = v; }); });
    var fl = el('div', 'free-list'); s1.appendChild(fl);
    (f.header.free || []).forEach(function (lbl, i) {
      var row = el('div', 'row'), inp = document.createElement('input'); inp.className = 'inp'; inp.value = lbl; inp.setAttribute('aria-label', 'Freier Baustein ' + (i + 1));
      inp.onchange = function () { change(function () { f.header.free[i] = inp.value.trim() ? inp.value.trim().replace(/:?$/, ':') : 'Feld:'; }); };
      var del = el('button', 'btn icon ghost', icon('trash')); del.setAttribute('aria-label', 'Feld entfernen');
      del.onclick = function () { frameChange(function () { f.header.free.splice(i, 1); }); };
      row.appendChild(inp); row.appendChild(del); fl.appendChild(row);
    });
    var addF = el('button', 'btn', icon('plus') + 'Freies Feld'); addF.onclick = function () { frameChange(function () { (f.header.free = f.header.free || []).push('Fach:'); }); };
    s1.appendChild(addF);
    chk(s1, 'Zusätzliche Titelzeile', f.title.show, function (v) { f.title.show = v; });

    var s2 = sec(box, 'Aufgabenblöcke');
    stepper(s2, 'Anzahl', f.blocks.count, 1, 0, 10, function (v) { return v === 0 ? 'keine' : v + ' Blöcke'; }, function (v) { f.blocks.count = v; f.blocks.weights = null; });
    chk(s2, 'Punkte-Spalte einfügen', f.blocks.pointsCol, function (v) { f.blocks.pointsCol = v; });
    if (f.blocks.pointsCol) {
      var pl = el('p', 'hint', 'Tippe in der Punkte-Spalte auf einen Block, um seine Punkte festzulegen.'); s2.appendChild(pl);
    }
    chk(s2, 'Summenfeld am unteren Rand', f.blocks.sum, function (v) { f.blocks.sum = v; if (v && !f.blocks.pointsCol) f.blocks.pointsCol = true; });
    if (f.blocks.sum) chk(s2, 'Notenschlüssel im Summenfeld', f.blocks.grades, function (v) { f.blocks.grades = v; });
    if (f.blocks.weights) { var rb = el('button', 'btn', 'Gleich hohe Blöcke'); rb.onclick = function () { frameChange(function () { f.blocks.weights = null; }); }; s2.appendChild(rb); }
    else s2.appendChild(el('p', 'hint', 'Die Trennlinien zwischen den Blöcken lassen sich am rechten Rand verschieben.'));

    if (f.blocks.sum && f.blocks.grades) {
      var s3 = sec(box, 'Notenschlüssel');
      var tbl = el('table', 'grade-tbl'), r = B.gradeRanges(D);
      tbl.innerHTML = '<thead><tr><th>Note</th><th>ab %</th><th class="r">Punkte</th></tr></thead>';
      var tb = el('tbody'); tbl.appendChild(tb);
      D.grading.scale.slice().sort(function (a, b) { return a.note - b.note; }).forEach(function (gr, i) {
        var tr = el('tr'); tr.innerHTML = '<td>' + gr.note + '</td><td></td><td class="r">' + B.rangeTxt(r[i]) + '</td>';
        if (gr.note < 6) {
          var inp = document.createElement('input'); inp.type = 'number'; inp.className = 'inp'; inp.min = 0; inp.max = 100; inp.value = gr.min; inp.setAttribute('aria-label', 'Note ' + gr.note + ' ab Prozent');
          inp.onchange = function () { var v = clamp(Number(inp.value) || 0, 0, 100); change(function () { gr.min = v; }); };
          tr.children[1].appendChild(inp);
        } else tr.children[1].textContent = 'darunter';
        tb.appendChild(tr);
      });
      s3.appendChild(tbl);
      s3.appendChild(el('p', 'hint', 'Gesamt: ' + B.fmtPts(B.totalPoints(D)) + ' Punkte aus allen Seiten. Gerechnet wird in halben Punkten.'));
    }

    var s4 = sec(box, 'Fußzeile');
    chk(s4, 'Fußzeile zeigen', f.footer.show, function (v) { f.footer.show = v; if (v && !f.footer.text) f.footer.text = 'Viel Erfolg!'; });

    if (D.pages.length > 1) {
      var s5 = sec(box, 'Mehrere Seiten');
      var ab = el('button', 'btn', 'Diesen Rahmen auf alle Seiten übertragen');
      ab.onclick = function () { change(function () { D.pages.forEach(function (q) { if (q !== p) q.frame = B.clone(f); }); }); toast('Rahmen auf alle Seiten übertragen'); };
      s5.appendChild(ab);
    }
  }

  function inspectPoints(box, hl) {
    var p = D.pages[sel.pi], b = p.frame.blocks, i = sel.block;
    frameMode = false;
    title(hl, 'Punkte für Block ' + (i + 1), 'Seite ' + (sel.pi + 1));
    var s = sec(box);
    stepper(s, 'Punkte', Number((b.points || [])[i]) || 0, 0.5, 0, 100, function (v) { return B.fmtPts(v) + ' P.'; }, function (v) { b.points = b.points || []; b.points[i] = v; });
    s.appendChild(el('p', 'hint', 'Gesamt auf allen Seiten: ' + B.fmtPts(B.totalPoints(D)) + ' Punkte.'));
    var done = el('button', 'btn', icon('check') + 'Fertig'); done.onclick = function () { select(null); }; s.appendChild(done);
  }

  function inspectItem(box, hl, it) {
    var names = { number: 'Aufgabennummer', text: 'Textfeld', lineatur: (B.LINEATUREN[it.kind] || {}).name || 'Lineatur', karo: 'Kästchen', image: 'Bild', table: 'Tabelle' };
    title(hl, names[it.type], it.type === 'lineatur' ? B.LINEATUREN[it.kind].klasse : '');
    if (it.type === 'lineatur') {
      var s = sec(box, 'Lineatur');
      seg(s, [['L1', '1'], ['L2', '2'], ['L3', '3'], ['L4', '4']], it.kind, function (v) {
        var n = B.lineaturRows(it).length; it.kind = v; it.h = B.lineaturHeightFor(it, n);
      }, 'Lineatur für Klasse');
      stepper(s, 'Zeilen', B.lineaturRows(it).length, 1, 1, 30, function (v) { return v + (v === 1 ? ' Zeile' : ' Zeilen'); }, function (v) { it.h = B.lineaturHeightFor(it, v); });
      stepper(s, 'Höhe', it.scale || 100, 10, 50, 300, function (v) { return v + ' %'; }, function (v) { var n = B.lineaturRows(it).length; it.scale = v; it.h = B.lineaturHeightFor(it, n); });
      var s2 = sec(box, 'Darstellung');
      var z = !!B.LINEATUREN[it.kind].zones;
      chk(s2, 'Hauptzeile hervorheben', it.main, function (v) { it.main = v; });
      if (z) chk(s2, 'Ober- und Unterlänge einfärben', it.fill, function (v) { it.fill = v; });
      if (z) chk(s2, 'Schreibhäuschen', it.house, function (v) { it.house = v; });
      var rc = el('div', 'row'); rc.appendChild(el('label', '', 'Linienfarbe')); s2.appendChild(rc);
      colors(s2, it.color, function (c) { it.color = c; });
      var lw = sec(box, 'Hineinschreiben');
      writeControls(lw, it, Array.isArray(it.lines) && it.lines.some(function (x) { return x; }), function () { it.lines = []; },
        'Tippe die Lineatur zweimal an und schreib los. Mit der Eingabetaste geht es in die nächste Zeile.');
    }
    if (it.type === 'karo') {
      var sk = sec(box, 'Kästchen');
      seg(sk, [[5, '5 mm'], [7, '7 mm'], [10, '10 mm']], it.cell || 5, function (v) { it.cell = v; it.w = Math.max(v, Math.round(it.w / v) * v); it.h = Math.max(v, Math.round(it.h / v) * v); }, 'Kästchengröße');
      colors(sk, it.color, function (c) { it.color = c; }, ['#9aa8b8', '#4a5563', '#7fa7d9', '#86c2a9']);
      var kw = sec(box, 'Hineinschreiben');
      writeControls(kw, it, it.cells && Object.keys(it.cells).length > 0, function () { it.cells = {}; },
        'Tippe die Kästchen zweimal an, dann in das Kästchen, wo es losgehen soll. Jedes Zeichen bekommt ein eigenes Kästchen.');
      var under = Array.isArray(it.under) ? it.under : [];
      if (editing === it.id && kcur) {
        var on = under.indexOf(kcur.r) >= 0;
        var ub = el('button', 'btn' + (on ? ' primary' : ''), (on ? 'Strich entfernen' : 'Zeile unterstreichen') + ' (Zeile ' + (kcur.r + 1) + ')');
        ub.id = 'btnUnder';
        ub.addEventListener('pointerdown', function (e) { e.preventDefault(); });
        ub.onclick = function () { toggleUnder(it); };
        kw.appendChild(ub);
      } else kw.appendChild(el('p', 'hint', 'Unterstreichen: beim Hineinschreiben in die Zeile tippen, dann hier „Zeile unterstreichen“.'));
      if (under.length) { var ur = el('button', 'btn', 'Alle Striche entfernen'); ur.onclick = function () { change(function () { it.under = []; }); }; kw.appendChild(ur); }
    }
    if (it.type === 'number') {
      var sn = sec(box, 'Nummer');
      chk(sn, 'Automatisch nummerieren', it.auto !== false, function (v) { it.auto = v; if (!v) it.value = numMap[it.id] || 1; });
      if (it.auto === false) stepper(sn, 'Nummer', Number(it.value) || 1, 1, 1, 99, String, function (v) { it.value = v; });
      chk(sn, 'Schatten', it.shadow, function (v) { it.shadow = v; });
      stepper(sn, 'Größe', r1(it.w), 1, 6, 24, function (v) { return r1(v).toString().replace('.', ',') + ' mm'; }, function (v) { it.w = v; it.h = v; });
    }
    if (it.type === 'text') {
      var st = sec(box, 'Text');
      var fmtRow = el('div', 'row');
      [['bold', '<b>F</b>', 'Fett'], ['italic', '<i>K</i>', 'Kursiv'], ['underline', '<u>U</u>', 'Unterstrichen']].forEach(function (f) {
        var b = el('button', 'btn icon', f[1]); b.title = f[2]; b.setAttribute('aria-label', f[2]);
        b.addEventListener('pointerdown', function (e) { e.preventDefault(); });
        b.onclick = function () {
          if (editing !== it.id) startEdit(it.id);
          document.execCommand(f[0], false, null);
        };
        fmtRow.appendChild(b);
      });
      st.appendChild(fmtRow);
      if (editing !== it.id) { var eb = el('button', 'btn', icon('edit') + 'Text bearbeiten'); eb.onclick = function () { startEdit(it.id); }; st.appendChild(eb); }
      stepper(st, 'Schriftgröße', it.size || 14, 1, 8, 48, function (v) { return v + ' pt'; }, function (v) { it.size = v; });
      seg(st, [['left', 'Links'], ['center', 'Mitte'], ['right', 'Rechts']], it.align || 'left', function (v) { it.align = v; }, 'Ausrichtung');
      chk(st, 'Rahmen um den Text', it.border, function (v) { it.border = v; });
    }
    if (it.type === 'table') inspectTable(box, it);
    if (it.type === 'image') {
      var si = sec(box, 'Bild');
      var pb = el('button', 'btn', it.asset ? 'Bild ersetzen' : 'Bild wählen'); pb.onclick = function () { pickImage(it.id); }; si.appendChild(pb);
      si.appendChild(el('p', 'hint', 'Bilder kannst du auch aus Fotos oder Dateien direkt aufs Blatt ziehen oder einfügen.'));
    }
    var sp = sec(box, 'Position in mm');
    var g2 = el('div', 'grid2'); sp.appendChild(g2);
    numInput(g2, 'Links', r1(it.x), function (v) { it.x = v; });
    numInput(g2, 'Oben', r1(it.y), function (v) { it.y = v; });
    if (it.type !== 'number') {
      numInput(g2, 'Breite', r1(it.w), function (v) { it.w = Math.max(5, v); if (it.type === 'image' && it.natW) it.h = r1(it.w * it.natH / it.natW); });
      if (it.type !== 'lineatur' && it.type !== 'table') numInput(g2, 'Höhe', r1(it.h), function (v) { it.h = Math.max(4, v); if (it.type === 'image' && it.natW) it.w = r1(it.h * it.natW / it.natH); });
    }
    var sa = sec(box, 'Anordnen');
    var ar = el('div', 'row');
    var front = el('button', 'btn', 'Nach vorne'), back = el('button', 'btn', 'Nach hinten');
    front.onclick = function () { change(function () { var a = page(sel.pi).items, i = a.indexOf(it); a.splice(i, 1); a.push(it); }); };
    back.onclick = function () { change(function () { var a = page(sel.pi).items, i = a.indexOf(it); a.splice(i, 1); a.unshift(it); }); };
    ar.appendChild(front); ar.appendChild(back); sa.appendChild(ar);
    var ar2 = el('div', 'row');
    var cp = el('button', 'btn', icon('copy') + 'Kopieren'), dl = el('button', 'btn danger', icon('trash') + 'Löschen');
    cp.onclick = duplicate; dl.onclick = removeSel;
    ar2.appendChild(cp); ar2.appendChild(dl); sa.appendChild(ar2);
  }

  function keepFocus(b) { b.addEventListener('pointerdown', function (e) { e.preventDefault(); }); }
  function inspectTable(box, it) {
    B.normTable(it);
    var st = sec(box, 'Tabelle');
    stepper(st, 'Spalten', it.cols, 1, 1, 12, String, function (v) { while (it.cols < v) B.tableInsert(it, 'col', it.cols); while (it.cols > v) B.tableRemove(it, 'col', it.cols - 1); if (tcur) tcur.c = Math.min(tcur.c, it.cols - 1); });
    stepper(st, 'Zeilen', it.rows, 1, 1, 30, String, function (v) { while (it.rows < v) B.tableInsert(it, 'row', it.rows); while (it.rows > v) B.tableRemove(it, 'row', it.rows - 1); if (tcur) tcur.r = Math.min(tcur.r, it.rows - 1); });
    if (editing !== it.id) { var wb = el('button', 'btn', icon('edit') + 'In die Zellen schreiben'); wb.onclick = function () { startEdit(it.id); }; st.appendChild(wb); }
    else { var fb = el('button', 'btn', icon('check') + 'Fertig'); fb.onclick = function () { stopEdit(); drawSelection(); renderInspector(); }; st.appendChild(fb); }
    st.appendChild(el('p', 'hint', 'Tabelle zweimal antippen, dann in eine Zelle tippen und schreiben. Die Tab-Taste springt zur nächsten Zelle. Zeilen wachsen mit dem Text mit; höher ziehen geht am unteren Griff.'));
    if (editing === it.id && tcur) {
      var r = tcur.r, c = tcur.c, n = tCount(it), multi = n > 1;
      var sa = sec(box, multi ? 'Auswahl: ' + n + ' Zellen' : 'Zelle: Zeile ' + (r + 1) + ', Spalte ' + (c + 1));
      var allU = true; tEach(it, function (x) { if (!x.u) allU = false; });
      var ub = el('button', 'btn' + (allU ? ' primary' : ''), '<u>U</u>&nbsp; ' + (allU ? 'Strich entfernen' : (multi ? 'Auswahl unterstreichen' : 'Zelle unterstreichen')));
      ub.id = 'btnCellUnder'; ub.setAttribute('aria-pressed', String(allU));
      ub.onclick = function () { change(function () { tEach(it, function (x) { if (allU) delete x.u; else x.u = true; }); }); };
      keepFocus(ub); sa.appendChild(ub);
      var ga = el('div', 'grid2'); sa.appendChild(ga);
      [['Ganze Zeile', function () { tanc = { r: r, c: 0 }; tcur = { r: r, c: it.cols - 1 }; }], ['Ganze Spalte', function () { tanc = { r: 0, c: c }; tcur = { r: it.rows - 1, c: c }; }]].forEach(function (a) {
        var b = el('button', 'btn', a[0] + ' auswählen'); b.onclick = function () { a[1](); textend = false; var d0 = itemEl(it.id); if (d0) markRange(d0, it); focusCell(false); renderInspector(); }; keepFocus(b); ga.appendChild(b);
      });
      var xb = el('button', 'btn' + (textend ? ' primary' : ''), textend ? 'Jetzt auf die letzte Zelle tippen' : 'Bis zu einer Zelle auswählen');
      xb.id = 'btnCellExtend'; xb.setAttribute('aria-pressed', String(textend));
      xb.onclick = function () { textend = !textend; renderInspector(); };
      keepFocus(xb); sa.appendChild(xb);
      if (multi) { var eb = el('button', 'btn', 'Nur diese eine Zelle'); eb.onclick = function () { tanc = null; textend = false; var d0 = itemEl(it.id); if (d0) markRange(d0, it); renderInspector(); }; keepFocus(eb); sa.appendChild(eb); }
      sa.appendChild(el('p', 'hint', 'Mehrere Zellen: mit dem Finger „Bis zu einer Zelle auswählen“ und dann die letzte Zelle antippen; mit der Maus über die Zellen ziehen oder mit gedrückter Umschalttaste klicken. Der Strich kommt unter jede ausgewählte Zelle.'));
      var sc = sec(box, multi ? 'Zeilen und Spalten (bei Zeile ' + (r + 1) + ', Spalte ' + (c + 1) + ')' : 'Zeilen und Spalten');
      var g = el('div', 'grid2'); sc.appendChild(g);
      [['Zeile darüber', function () { B.tableInsert(it, 'row', r); }], ['Zeile darunter', function () { B.tableInsert(it, 'row', r + 1); tcur.r = r + 1; }],
        ['Spalte links', function () { B.tableInsert(it, 'col', c); }], ['Spalte rechts', function () { B.tableInsert(it, 'col', c + 1); tcur.c = c + 1; }]].forEach(function (a) {
        var b = el('button', 'btn', icon('plus') + a[0]); b.onclick = function () { tanc = null; change(a[1]); }; g.appendChild(b);
      });
      var dr = el('button', 'btn danger', icon('trash') + 'Zeile löschen'); dr.disabled = it.rows < 2;
      dr.onclick = function () { tanc = null; change(function () { B.tableRemove(it, 'row', r); tcur.r = Math.min(r, it.rows - 1); }); };
      var dc = el('button', 'btn danger', icon('trash') + 'Spalte löschen'); dc.disabled = it.cols < 2;
      dc.onclick = function () { tanc = null; change(function () { B.tableRemove(it, 'col', c); tcur.c = Math.min(c, it.cols - 1); }); };
      g.appendChild(dr); g.appendChild(dc);
      var rl = el('div', 'row'); rl.appendChild(el('label', '', multi ? 'Hintergrund der Auswahl' : 'Hintergrund der Zelle')); sc.appendChild(rl);
      var sw = el('div', 'swatches'); sc.appendChild(sw);
      CELL_BG.forEach(function (col) {
        var b = el('button', 'swatch' + (col ? '' : ' none')); b.style.background = col || '#ffffff';
        b.setAttribute('aria-label', col ? 'Hintergrund ' + col : 'Kein Hintergrund'); b.setAttribute('aria-pressed', String((it.cells[r][c].bg || '') === col));
        b.onclick = function () { change(function () { tEach(it, function (x) { if (col) x.bg = col; else delete x.bg; }); }); };
        sw.appendChild(b);
      });
      var rowBg = el('button', 'btn', 'Diese Farbe für die ganze Zeile');
      rowBg.onclick = function () { var col = it.cells[r][c].bg; change(function () { it.cells[r].forEach(function (x) { if (col) x.bg = col; else delete x.bg; }); }); };
      sc.appendChild(rowBg);
    }
    var sx = sec(box, 'Text in den Zellen');
    var fmtRow = el('div', 'row');
    [['bold', '<b>F</b>', 'Fett'], ['italic', '<i>K</i>', 'Kursiv'], ['underline', '<u>U</u>', 'Unterstrichen']].forEach(function (f) {
      var b = el('button', 'btn icon', f[1]); b.title = f[2]; b.setAttribute('aria-label', f[2]);
      b.addEventListener('pointerdown', function (e) { e.preventDefault(); });
      b.onclick = function () { if (editing !== it.id) startEdit(it.id); document.execCommand(f[0], false, null); };
      fmtRow.appendChild(b);
    });
    sx.appendChild(fmtRow);
    stepper(sx, 'Schriftgröße', it.size, 1, 8, 36, function (v) { return v + ' pt'; }, function (v) { it.size = v; });
    seg(sx, [['left', 'Links'], ['center', 'Mitte'], ['right', 'Rechts']], it.ha, function (v) { it.ha = v; }, 'Waagerecht ausrichten');
    seg(sx, [['top', 'Oben'], ['middle', 'Mitte'], ['bottom', 'Unten']], it.va, function (v) { it.va = v; }, 'Senkrecht ausrichten');
    var sl = sec(box, 'Tabellenrahmen');
    seg(sl, [['all', 'Alle'], ['outer', 'Außen'], ['inner', 'Innen'], ['horiz', 'Quer'], ['none', 'Ohne']], it.lines, function (v) { it.lines = v; }, 'Welche Linien');
    seg(sl, [['solid', 'Linie'], ['dashed', 'Gestrichelt'], ['dotted', 'Gepunktet']], it.lineStyle, function (v) { it.lineStyle = v; }, 'Linienstil');
    seg(sl, [[0.2, 'Dünn'], [0.3, 'Standard'], [0.5, 'Kräftig'], [0.8, 'Dick']], it.lineW, function (v) { it.lineW = v; }, 'Liniendicke');
    colors(sl, it.lineColor, function (c2) { it.lineColor = c2; });
    var sp = sec(box, 'Zell-Innenabstand in mm');
    var gp = el('div', 'grid2'); sp.appendChild(gp);
    ['Oben', 'Rechts', 'Unten', 'Links'].forEach(function (lbl, k) { numInput(gp, lbl, it.pad[k], function (v) { it.pad[k] = clamp(v, 0, 10); }); });
  }

  function writeControls(sec2, it, hasText, clear, hint) {
    if (editing !== it.id) { var wb = el('button', 'btn', icon('edit') + 'Hineinschreiben'); wb.onclick = function () { startEdit(it.id); }; sec2.appendChild(wb); }
    else {
      var fb = el('button', 'btn', icon('check') + 'Fertig'); fb.onclick = function () { stopEdit(); drawSelection(); renderInspector(); }; sec2.appendChild(fb);
    }
    sec2.appendChild(el('p', 'hint', hint));
    chk(sec2, 'Schrift hellgrau (zum Nachspuren)', it.trace, function (v) { it.trace = v; });
    if (hasText) { var cb = el('button', 'btn danger', icon('trash') + 'Schrift löschen'); cb.onclick = function () { stopEdit(); change(clear); }; sec2.appendChild(cb); }
  }

  function duplicate() {
    var it = selItem(); if (!it) return;
    var c = B.clone(it); c.id = B.uid(); c.y = r1(it.y + it.h + 3);
    if (c.y + c.h > 290) { c.y = it.y; c.x = r1(it.x + 6); }
    change(function () { page(sel.pi).items.push(c); sel = { pi: sel.pi, id: c.id }; });
  }
  function removeSel() {
    var it = selItem(); if (!it) return;
    var pi = sel.pi;
    change(function () { var a = D.pages[pi].items; a.splice(a.indexOf(it), 1); sel = null; editing = null; });
    toast('Gelöscht. „Rückgängig“ holt es zurück.');
  }

  // ---------- Seiten ----------
  function renderPagebar() {
    $('pageInfo').textContent = 'Seite ' + (cur + 1) + ' von ' + D.pages.length;
    $('btnDelPage').disabled = D.pages.length < 2;
    $('delPageConfirm').hidden = true;
  }
  function scrollToPage(pi) {
    var w = document.querySelector('.page-wrap[data-pi="' + pi + '"]'); if (!w) return;
    $('desk').scrollTo({ top: w.offsetTop + $('pages').offsetTop - 30, behavior: 'smooth' });
  }

  // ---------- Dialoge ----------
  function openModal(id) { $(id).hidden = false; var f = $(id).querySelector('button, input'); if (f) f.focus(); }
  function closeModal(id) { $(id).hidden = true; }
  function fillSetup() {
    var s = D.setup, m = s.margins;
    $('mT').value = m.top / 10; $('mB').value = m.bottom / 10; $('mL').value = m.left / 10; $('mR').value = m.right / 10;
    Array.prototype.forEach.call($('segLines').children, function (b) { b.setAttribute('aria-pressed', String(b.dataset.v === s.lines)); });
    $('lineW').value = String(s.lineWidth);
    $('optHand').checked = !!s.handdrawn;
    var lc = $('lineColors'); lc.innerHTML = '';
    LINE_COLORS.forEach(function (c) {
      var b = el('button', 'swatch'); b.style.background = c; b.setAttribute('aria-label', 'Linienfarbe ' + c); b.setAttribute('aria-pressed', String(c === s.lineColor));
      b.onclick = function () { change(function () { s.lineColor = c; }); fillSetup(); }; lc.appendChild(b);
    });
  }
  function fillDocs() {
    var ul = $('docList'); ul.innerHTML = '';
    docs.slice().sort(function (a, b) { return b.updated - a.updated; }).forEach(function (d) {
      var li = el('li'), b = el('button'); b.setAttribute('aria-current', String(d.id === D.id));
      b.innerHTML = '<span></span><small></small>';
      b.firstChild.textContent = d.title || 'Ohne Titel';
      b.lastChild.textContent = (d.example ? 'Beispiel · ' : '') + d.pages.length + (d.pages.length === 1 ? ' Seite' : ' Seiten') + ' · ' + new Date(d.updated).toLocaleDateString('de-DE');
      b.onclick = function () { openDoc(d.id); closeModal('mDocs'); };
      li.appendChild(b); ul.appendChild(li);
    });
    $('delDocConfirm').hidden = true;
  }
  function openDoc(id) {
    stopEdit();
    docs.forEach(function (d) { if (d.id === id) D = d; });
    sel = null; cur = 0; undoStack = []; redoStack = []; updateUndo();
    lsSet('blattwerk.current', D.id); render(); $('desk').scrollTop = 0;
  }

  // ---------- Dateien ----------
  function offerFile(name, data, mime) {
    if (ENV === 'artifact') {
      var p = window.claude && window.claude.use ? window.claude.use('downloads') : Promise.resolve(null);
      return p.then(function (dl) {
        if (!dl) { toast('Speichern ist in dieser Vorschau nicht möglich.'); return; }
        return dl.save({ filename: name, data: data }).then(function () { toast('Gespeichert: ' + name); }, function (err) { if (!err || err.code !== 'declined') toast('Speichern hat nicht geklappt.'); });
      });
    }
    var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([data], { type: mime })); a.download = name;
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 4000);
    return Promise.resolve();
  }
  function importDoc(file) {
    var fr = new FileReader();
    fr.onload = function () {
      try {
        var d = JSON.parse(fr.result); d = d.doc || d;
        if (!d || d.v !== 2 || !Array.isArray(d.pages)) throw new Error('kein Blatt');
        d.id = B.uid(); d.updated = Date.now(); delete d.example; d.assets = d.assets || {};
        d.pages.forEach(function (p) { p.id = B.uid(); p.items.forEach(function (it) {
          it.id = B.uid(); if (it.html) it.html = cleanHtml(it.html);
          if (it.type === 'table') { B.normTable(it); it.cells.forEach(function (row) { row.forEach(function (x) { x.t = cleanHtml(x.t); if (typeof x.bg !== 'string' || !/^#[0-9a-f]{3,8}$/i.test(x.bg)) delete x.bg; if (x.u === true) x.u = true; else delete x.u; }); }); }
        }); });
        docs.unshift(d); store.put(d); openDoc(d.id); closeModal('mDocs'); toast('Blatt geöffnet: ' + (d.title || 'Ohne Titel'));
      } catch (e) { toast('Diese Datei ist kein Blattwerk-Blatt.'); }
    };
    fr.readAsText(file);
  }

  // ---------- Rückmeldungen ----------
  var fbArt = 'wunsch';
  function blattOhneBilder() {
    var c = B.clone(D); c.assets = {}; var n = 0;
    c.pages.forEach(function (p) { p.items.forEach(function (it) { if (it.type === 'image' && it.asset) { it.asset = null; n++; } }); });
    c.bilderEntfernt = n; return c;
  }
  function loadFeedbackList() {
    var ul = $('fbList');
    fetch(FEEDBACK_URL, { credentials: 'same-origin', headers: { Accept: 'application/json' } })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        ul.innerHTML = '';
        if (!res.ok) { ul.appendChild(el('li', 'hint')).textContent = res.j && res.j.fehler || 'Die Liste ließ sich gerade nicht laden.'; return; }
        if (!res.j.liste.length) { ul.appendChild(el('li', 'hint')).textContent = 'Noch keine Rückmeldungen.'; return; }
        res.j.liste.forEach(function (x) {
          var li = el('li'), t = el('span'), st = el('span', 'st' + (x.status === 'Erledigt' ? ' ok' : ''));
          t.textContent = '#' + x.nr + ' ' + x.titel; t.title = x.titel + ' · ' + x.datum; st.textContent = x.status;
          li.appendChild(t); li.appendChild(st); ul.appendChild(li);
        });
      })
      .catch(function () { ul.innerHTML = ''; ul.appendChild(el('li', 'hint')).textContent = 'Keine Verbindung. Die Liste erscheint, sobald das Gerät online ist.'; });
  }
  function openFeedback() {
    stopEdit();
    $('fbState').textContent = ''; $('fbSend').disabled = false;
    $('appVersion').textContent = 'Blattwerk ' + (VERSION ? 'v' + VERSION : '') + (STAGE === 'vorschau' ? ' · Vorschau' : '');
    openModal('mFeedback'); $('fbText').focus(); loadFeedbackList();
  }
  function sendFeedback() {
    var text = $('fbText').value.trim();
    if (text.length < 3) { $('fbState').textContent = 'Bitte schreib ein paar Worte dazu.'; return; }
    $('fbSend').disabled = true; $('fbState').textContent = 'Wird gesendet …';
    var payload = {
      art: fbArt, text: text,
      fassung: (STAGE === 'vorschau' ? 'Vorschau' : 'Live') + (VERSION ? ' v' + VERSION : ''),
      geraet: navigator.userAgent, bildschirm: window.innerWidth + ' × ' + window.innerHeight,
      blatt: (D.title || 'Ohne Titel') + ', ' + D.pages.length + (D.pages.length === 1 ? ' Seite' : ' Seiten')
    };
    if ($('fbBlatt').checked) payload.blattDatei = blattOhneBilder();
    fetch(FEEDBACK_URL, { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(payload) })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        if (!res.ok) { $('fbState').textContent = res.j && res.j.fehler || 'Senden hat nicht geklappt.'; $('fbSend').disabled = false; return; }
        $('fbText').value = ''; $('fbState').textContent = 'Danke! Ist angekommen als Nr. ' + res.j.nr + '.'; $('fbSend').disabled = false;
        loadFeedbackList();
      })
      .catch(function () { $('fbState').textContent = 'Keine Verbindung. Bitte später noch einmal senden, der Text bleibt stehen.'; $('fbSend').disabled = false; });
  }

  // ---------- Ereignisse ----------
  function bind() {
    $('btnUndo').onclick = undo; $('btnRedo').onclick = redo;
    $('btnZoomIn').onclick = function () { zoom = clamp(Math.round((scale + 0.1) * 10) / 10, 0.3, 2.5); layout(); };
    $('btnZoomOut').onclick = function () { zoom = clamp(Math.round((scale - 0.1) * 10) / 10, 0.3, 2.5); layout(); };
    $('btnZoomFit').onclick = function () { zoom = 'fit'; layout(); };
    if (ENV === 'artifact') $('btnPrint').hidden = true;
    if (ENV === 'web') { $('btnFeedback').hidden = false; $('btnFeedback').onclick = openFeedback; }
    if (STAGE === 'vorschau') { $('stageBadge').hidden = false; document.title = 'Blattwerk Vorschau'; }
    $('fbSend').onclick = sendFeedback;
    $('fbArt').onclick = function (e) {
      var b = e.target.closest('button'); if (!b) return; fbArt = b.dataset.v;
      Array.prototype.forEach.call($('fbArt').children, function (x) { x.setAttribute('aria-pressed', String(x === b)); });
    };
    $('btnPrint').onclick = function () { stopEdit(); select(null); setTimeout(function () { window.print(); }, 60); };
    $('btnInsp').onclick = function () { $('insp').classList.toggle('open'); };
    $('fProps').onclick = function () { $('insp').classList.add('open'); };
    $('fCopy').onclick = duplicate; $('fDel').onclick = removeSel;
    $('fEdit').onclick = function () { var it = selItem(); if (it) startEdit(it.id); };
    $('docTitle').addEventListener('input', function () { D.title = $('docTitle').value; save(); });

    $('btnAddPage').onclick = function () {
      var f = page().frame;
      change(function () { var np = B.newPage(f); np.frame.title.text = ''; D.pages.splice(cur + 1, 0, np); cur = cur + 1; sel = null; });
      scrollToPage(cur);
    };
    $('btnDupPage').onclick = function () {
      change(function () { var c = B.clone(page()); c.id = B.uid(); c.items.forEach(function (it) { it.id = B.uid(); }); D.pages.splice(cur + 1, 0, c); cur++; sel = null; });
      scrollToPage(cur); toast('Seite kopiert');
    };
    $('btnDelPage').onclick = function () { $('delPageConfirm').hidden = false; };
    $('btnDelPageNo').onclick = function () { $('delPageConfirm').hidden = true; };
    $('btnDelPageYes').onclick = function () { change(function () { D.pages.splice(cur, 1); cur = Math.max(0, cur - 1); sel = null; }); toast('Seite gelöscht'); };

    $('btnSetup').onclick = function () { fillSetup(); openModal('mSetup'); };
    ['mT', 'mB', 'mL', 'mR'].forEach(function (id) {
      $(id).onchange = function () {
        var v = clamp(parseFloat(String($(id).value).replace(',', '.')) || 1.5, 0.5, 4) * 10, k = { mT: 'top', mB: 'bottom', mL: 'left', mR: 'right' }[id];
        frameChange(function () { D.setup.margins[k] = v; }, true);
      };
    });
    $('segLines').onclick = function (e) { var b = e.target.closest('button'); if (!b) return; change(function () { D.setup.lines = b.dataset.v; }); fillSetup(); };
    $('lineW').onchange = function () { change(function () { D.setup.lineWidth = Number($('lineW').value); }); };
    $('optHand').onchange = function () { change(function () { D.setup.handdrawn = $('optHand').checked; }); };

    $('btnDocs').onclick = function () { fillDocs(); openModal('mDocs'); };
    $('btnNewDoc').onclick = function () { var d = B.newDoc(); docs.unshift(d); store.put(d); openDoc(d.id); closeModal('mDocs'); $('docTitle').focus(); };
    $('btnDupDoc').onclick = function () {
      var c = B.clone(D); c.id = B.uid(); c.title = (D.title || 'Ohne Titel') + ' (Kopie)'; delete c.example; c.updated = Date.now();
      docs.unshift(c); store.put(c); openDoc(c.id); fillDocs(); toast('Kopie angelegt');
    };
    $('btnDelDoc').onclick = function () { $('delDocConfirm').hidden = false; };
    $('btnDelDocNo').onclick = function () { $('delDocConfirm').hidden = true; };
    $('btnDelDocYes').onclick = function () {
      var id = D.id; store.del(id); docs = docs.filter(function (d) { return d.id !== id; });
      if (!docs.length) { var d = B.newDoc(); docs.push(d); store.put(d); }
      openDoc(docs[0].id); fillDocs(); toast('Blatt gelöscht');
    };
    $('btnExport').onclick = function () { stopEdit(); offerFile(fileSafe(D.title) + '.blattwerk.json', JSON.stringify({ blattwerk: 2, doc: D }), 'application/json'); };
    $('btnImport').onclick = function () { $('fileDoc').value = ''; $('fileDoc').click(); };
    $('fileDoc').onchange = function () { var f = $('fileDoc').files[0]; if (f) importDoc(f); };
    $('fileImg').onchange = function () { var f = $('fileImg').files[0], t = pickTarget; pickTarget = null; if (f) placeImage(f, t, sel ? sel.pi : cur); };
    Array.prototype.forEach.call(document.querySelectorAll('[data-close]'), function (b) { b.onclick = function () { closeModal(b.closest('.modal').id); }; });
    Array.prototype.forEach.call(document.querySelectorAll('.modal'), function (m) { m.addEventListener('click', function (e) { if (e.target === m) closeModal(m.id); }); });

    // Titel und Fußzeile direkt auf dem Blatt
    $('pages').addEventListener('input', function (e) {
      var t = e.target;
      if (t.dataset && t.dataset.role) {
        var pi = Number(t.closest('.page').dataset.pi), f = D.pages[pi].frame;
        if (t.dataset.role === 'title') f.title.text = t.textContent; else f.footer.text = t.textContent;
        save(); return;
      }
      var tdc = t.closest && t.closest('.item.table td');
      if (tdc) {
        var te = tdc.closest('.item'), ti = itemById(Number(te.dataset.pi), te.dataset.id);
        if (!ti) return;
        B.normTable(ti); ti.cells[Number(tdc.dataset.r)][Number(tdc.dataset.c)].t = cleanHtml(tdc.innerHTML);
        if (syncTableH(te, ti)) drawSelection();
        save(); return;
      }
      var lr = t.closest && t.closest('.lrow');
      if (lr) {
        var le = lr.closest('.item'), li = itemById(Number(le.dataset.pi), le.dataset.id), ri = Number(lr.dataset.row);
        if (!li) return;
        if (lr.children.length) lr.textContent = lr.textContent;
        if (!Array.isArray(li.lines)) li.lines = [];
        while (li.lines.length < ri) li.lines.push('');
        li.lines[ri] = lr.textContent.replace(/[\r\n]+/g, ' ');
        save(); return;
      }
      var itEl = t.closest && t.closest('.item.text');
      if (itEl) growText(itEl, itemById(Number(itEl.dataset.pi), itEl.dataset.id));
    });
    $('pages').addEventListener('focusout', function (e) {
      if (e.target.dataset && e.target.dataset.role) return;
      var lrEl = e.target.closest && e.target.closest('.item.lineatur, .item.table');
      if (lrEl && editing === lrEl.dataset.id) setTimeout(function () {
        var a = document.activeElement;
        if (editing === lrEl.dataset.id && !(a && a.closest && (a.closest('.inspector') || a.closest('.float') || a.closest('.item[data-id="' + lrEl.dataset.id + '"]')))) { stopEdit(); drawSelection(); renderInspector(); }
      }, 0);
      var itEl = e.target.closest && e.target.closest('.item.text');
      if (itEl && editing === itEl.dataset.id) setTimeout(function () { if (editing === itEl.dataset.id && !document.activeElement.closest('.inspector')) { stopEdit(); drawSelection(); renderInspector(); } }, 0);
    });
    $('pages').addEventListener('focusin', function (e) {
      var td = e.target.closest && e.target.closest('.item.table td');
      if (!td || editing !== td.closest('.item').dataset.id) return;
      var r = Number(td.dataset.r), c = Number(td.dataset.c);
      if (tcur && tcur.r === r && tcur.c === c) return;
      if (tdrag && tdrag.on) return;
      tcur = { r: r, c: c }; tanc = null; focusCell(false); markRange(td.closest('.item'), itemById(Number(td.closest('.item').dataset.pi), td.closest('.item').dataset.id)); renderInspector();
    });
    $('pages').addEventListener('keydown', function (e) {
      if (e.target.dataset && e.target.dataset.role && e.key === 'Enter') { e.preventDefault(); e.target.blur(); return; }
      var td = e.target.closest && e.target.closest('.item.table td');
      if (td && e.key === 'Tab') {
        var tit = itemById(Number(td.closest('.item').dataset.pi), td.closest('.item').dataset.id), k = Number(td.dataset.r) * tit.cols + Number(td.dataset.c) + (e.shiftKey ? -1 : 1);
        e.preventDefault();
        if (k >= 0 && k < tit.rows * tit.cols) { tcur = { r: Math.floor(k / tit.cols), c: k % tit.cols }; tanc = null; markRange(td.closest('.item'), tit); focusCell(true); renderInspector(); }
        return;
      }
      var lr = e.target.closest && e.target.closest('.lrow');
      if (!lr) return;
      var rows = lr.parentNode.querySelectorAll('.lrow'), i = Number(lr.dataset.row);
      if (e.key === 'Enter' || e.key === 'ArrowDown') { e.preventDefault(); focusRow(rows[Math.min(rows.length - 1, i + 1)]); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); focusRow(rows[Math.max(0, i - 1)]); }
      else if (e.key === 'Backspace' && !lr.textContent && i > 0) { e.preventDefault(); focusRow(rows[i - 1]); }
    });
    // iPad: Tastatur für die Kästchen erst beim Antippen (Klick) öffnen
    $('desk').addEventListener('click', function (e) { if (editKaro() && e.target.closest && e.target.closest('.item.karo')) placeKInput(true); });

    document.addEventListener('keydown', function (e) {
      var inField = e.target.closest && e.target.closest('input, textarea, select, [contenteditable=true]');
      var mod = e.metaKey || e.ctrlKey;
      if (mod && e.key.toLowerCase() === 'z' && !inField) { e.preventDefault(); if (e.shiftKey) redo(); else undo(); return; }
      if (e.key === 'Escape') { if (editing) { stopEdit(); drawSelection(); renderInspector(); } else select(null); Array.prototype.forEach.call(document.querySelectorAll('.modal'), function (m) { m.hidden = true; }); return; }
      if (inField || !sel || !sel.id) return;
      if (e.key === 'Delete' || e.key === 'Backspace') { e.preventDefault(); removeSel(); return; }
      if (mod && e.key.toLowerCase() === 'd') { e.preventDefault(); duplicate(); return; }
      var step = e.shiftKey ? 5 : 1, dx = { ArrowLeft: -step, ArrowRight: step }[e.key] || 0, dy = { ArrowUp: -step, ArrowDown: step }[e.key] || 0;
      if (dx || dy) { e.preventDefault(); var it = selItem(); change(function () { it.x = r1(it.x + dx); it.y = r1(it.y + dy); }); }
    });

    // aktuelle Seite beim Scrollen
    $('desk').addEventListener('scroll', function () {
      if (sel) return;
      var desk = $('desk'), mid = desk.scrollTop + desk.clientHeight / 2 - $('pages').offsetTop, best = cur;
      Array.prototype.forEach.call(document.querySelectorAll('.page-wrap'), function (w) { if (w.offsetTop <= mid) best = Number(w.dataset.pi); });
      setCur(best);
    }, { passive: true });

    setupPointer(); setupPalette(); setupDrop(); setupKaroInput();
    if (window.ResizeObserver) new ResizeObserver(function () { layout(); }).observe($('desk'));
    window.addEventListener('beforeprint', function () { stopEdit(); });
  }

  // ---------- Start ----------
  function start() {
    bind();
    D = B.exampleDoc(); docs = [D]; render();
    store.ok().then(function (ok) { storageOk = ok; });
    store.all().then(function (all) {
      all = (all || []).filter(function (d) { return d && d.v === 2; });
      if (all.length) {
        docs = all;
        var c = lsGet('blattwerk.current'), f = null;
        all.forEach(function (d) { if (d.id === c) f = d; });
        D = f || all.slice().sort(function (a, b) { return b.updated - a.updated; })[0];
        render();
      } else { store.put(D); }
    }, function () { /* bleibt beim Beispiel */ });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { metr = null; if (!editing) render(); else layout(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
