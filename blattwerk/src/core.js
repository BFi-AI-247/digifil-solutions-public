/*
 * Blattwerk – Kern: Datenmodell, Seitenrahmen-Geometrie, Lineaturen, Handgezeichnet-Stil, Punkte und Noten.
 * Alle Maße in Millimetern. Läuft im Browser (window.BW) und in Node (module.exports) für Tests.
 */
(function (root) {
  'use strict';

  var PAGE = { w: 210, h: 297 };

  // ---------- Lineaturen nach der Vorlage (Lineaturelemente.pdf), Maße bei 100 % ----------
  // zones: Oberlänge / Mittelband / Unterlänge; gap: Abstand zwischen zwei Zeilen
  var LINEATUREN = {
    L1: { name: 'Lineatur 1', klasse: 'Klasse 1', zones: [5, 5, 5], gap: 5 },
    L2: { name: 'Lineatur 2', klasse: 'Klasse 2', zones: [4, 4, 4], gap: 3 },
    L3: { name: 'Lineatur 3', klasse: 'Klasse 3', band: 4, pitch: 15 },
    L4: { name: 'Lineatur 4', klasse: 'Klasse 4 und Aufsatz', line: 10, pitch: 15 }
  };

  function uid() { return Math.random().toString(36).slice(2, 9) + Date.now().toString(36).slice(-4); }
  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function r2(n) { return Math.round(n * 100) / 100; }

  // ---------- Datenmodell ----------
  var DEFAULT_SCALE = [
    { note: 1, min: 95 }, { note: 2, min: 80 }, { note: 3, min: 65 },
    { note: 4, min: 50 }, { note: 5, min: 25 }, { note: 6, min: 0 }
  ];

  function newFrame(blocks) {
    return {
      header: { name: true, datum: true, klasse: true, note: false, punkte: false, durchschnitt: false, seite: false, free: [] },
      title: { show: true, text: '' },
      blocks: { count: blocks === undefined ? 4 : blocks, weights: null, pointsCol: false, points: [], sum: false, grades: false },
      footer: { show: false, text: '' }
    };
  }
  function newPage(frame) { return { id: uid(), frame: frame ? clone(frame) : newFrame(), items: [] }; }
  function newDoc() {
    return {
      v: 2, id: uid(), title: '', updated: Date.now(), klasse: 1,
      setup: { margins: { top: 15, bottom: 15, left: 20, right: 15 }, lineWidth: 0.4, lineColor: '#1b2430', handdrawn: false, lines: 'all' },
      grading: { scale: clone(DEFAULT_SCALE) },
      pages: [newPage()],
      assets: {}
    };
  }

  function newItem(type, opts) {
    var it = { id: uid(), type: type, x: 0, y: 0, w: 20, h: 10 };
    if (type === 'number') { it.w = 9.2; it.h = 9.2; it.auto = true; it.value = 1; it.shadow = true; }
    if (type === 'text') { it.w = 120; it.h = 12; it.html = ''; it.size = 14; it.align = 'left'; it.border = false; }
    if (type === 'lineatur') { it.kind = 'L1'; it.scale = 100; it.color = '#1b2430'; it.main = false; it.fill = false; it.house = false; it.w = 140; it.h = 35; it.lines = []; }
    if (type === 'karo') { it.cell = 5; it.color = '#9aa8b8'; it.w = 140; it.h = 30; it.cells = {}; it.under = []; }
    if (type === 'image') { it.asset = null; it.w = 50; it.h = 35; }
    if (type === 'table') {
      it.w = 140; it.rows = 2; it.cols = 3; it.colW = [1, 1, 1]; it.rowH = [9, 9]; it.cells = [];
      it.pad = [2, 2, 2, 2]; it.size = 12; it.ha = 'left'; it.va = 'middle';
      it.lines = 'all'; it.lineW = 0.3; it.lineColor = '#1b2430'; it.lineStyle = 'solid';
    }
    if (opts) for (var k in opts) it[k] = opts[k];
    if (type === 'table') normTable(it);
    return it;
  }

  // ---------- Tabelle ----------
  // Ergänzt fehlende oder kaputte Angaben (alte oder eingelesene Blätter), verwirft nichts
  function normTable(it) {
    var R = Math.max(1, Math.min(30, it.rows | 0 || 1)), C = Math.max(1, Math.min(12, it.cols | 0 || 1)), r, c;
    it.rows = R; it.cols = C;
    if (!Array.isArray(it.colW)) it.colW = [];
    for (c = 0; c < C; c++) if (!(Number(it.colW[c]) > 0)) it.colW[c] = 1;
    it.colW.length = C;
    if (!Array.isArray(it.rowH)) it.rowH = [];
    for (r = 0; r < R; r++) if (!(Number(it.rowH[r]) > 0)) it.rowH[r] = 9;
    it.rowH.length = R;
    if (!Array.isArray(it.cells)) it.cells = [];
    for (r = 0; r < R; r++) {
      if (!Array.isArray(it.cells[r])) it.cells[r] = [];
      for (c = 0; c < C; c++) { var x = it.cells[r][c]; if (!x || typeof x !== 'object') it.cells[r][c] = { t: typeof x === 'string' ? esc(x) : '' }; else if (typeof x.t !== 'string') x.t = ''; }
      it.cells[r].length = C;
    }
    it.cells.length = R;
    if (!Array.isArray(it.pad) || it.pad.length !== 4) it.pad = [2, 2, 2, 2];
    if (['all', 'outer', 'inner', 'horiz', 'none'].indexOf(it.lines) < 0) it.lines = 'all';
    if (['solid', 'dashed', 'dotted'].indexOf(it.lineStyle) < 0) it.lineStyle = 'solid';
    if (!(Number(it.lineW) > 0)) it.lineW = 0.3;
    if (typeof it.lineColor !== 'string') it.lineColor = '#1b2430';
    if (['left', 'center', 'right'].indexOf(it.ha) < 0) it.ha = 'left';
    if (['top', 'middle', 'bottom'].indexOf(it.va) < 0) it.va = 'middle';
    if (!(Number(it.size) > 0)) it.size = 12;
    return it;
  }
  // Rahmenlinien einer Zelle: welche Seiten eine Linie bekommen
  function tableEdges(it, r, c) {
    var top = r === 0, bot = r === it.rows - 1, left = c === 0, right = c === it.cols - 1, m = it.lines;
    if (m === 'all') return { t: 1, r: 1, b: 1, l: 1 };
    if (m === 'outer') return { t: top, r: right, b: bot, l: left };
    if (m === 'inner') return { t: !top, r: !right, b: !bot, l: !left };
    if (m === 'horiz') return { t: 1, r: 0, b: 1, l: 0 };
    return { t: 0, r: 0, b: 0, l: 0 };
  }
  function tableInsert(it, what, at) {
    normTable(it);
    var r, c;
    if (what === 'row' && it.rows < 30) {
      var row = []; for (c = 0; c < it.cols; c++) row.push({ t: '' });
      it.cells.splice(at, 0, row); it.rowH.splice(at, 0, it.rowH[Math.max(0, at - 1)] || 9); it.rows++;
    } else if (what === 'col' && it.cols < 12) {
      for (r = 0; r < it.rows; r++) it.cells[r].splice(at, 0, { t: '' });
      it.colW.splice(at, 0, it.colW[Math.max(0, at - 1)] || 1); it.cols++;
    }
  }
  function tableRemove(it, what, at) {
    normTable(it);
    if (what === 'row' && it.rows > 1) { it.cells.splice(at, 1); it.rowH.splice(at, 1); it.rows--; }
    else if (what === 'col' && it.cols > 1) { for (var r = 0; r < it.rows; r++) it.cells[r].splice(at, 1); it.colW.splice(at, 1); it.cols--; }
  }

  // ---------- Seitenrahmen-Geometrie ----------
  var HEADER_H = 20, TITLE_H = 20, SUM_H = 14, GRADE_H = 14, FOOTER_H = 10, POINTS_W = 18;

  var HEADER_FIELDS = [
    ['name', 'Name:', true], ['datum', 'Datum:', true], ['klasse', 'Klasse:', true],
    ['note', 'Note:', false], ['punkte', 'Punkte:', false], ['durchschnitt', 'Durchschnitt:', false], ['seite', 'Seite:', false]
  ];

  // Liefert alle Rechtecke des Rahmens einer Seite
  function frameLayout(doc, page) {
    var m = doc.setup.margins, f = page.frame;
    var L = m.left, R = PAGE.w - m.right, T = m.top, B = PAGE.h - m.bottom, W = R - L;
    var out = { box: { x: L, y: T, w: W, h: B - T }, header: null, cells: [], title: null, blocks: [], sum: null, footer: null, pointsCol: null };
    var y = T;
    var cells = [];
    HEADER_FIELDS.forEach(function (hf) { if (f.header[hf[0]]) cells.push({ key: hf[0], label: hf[1], line: hf[2] }); });
    (f.header.free || []).forEach(function (lbl, i) { cells.push({ key: 'free' + i, label: lbl, line: true, free: i }); });
    if (cells.length) {
      out.header = { x: L, y: y, w: W, h: HEADER_H };
      var cw = W / cells.length;
      cells.forEach(function (c, i) { c.x = L + i * cw; c.y = y; c.w = cw; c.h = HEADER_H; });
      out.cells = cells;
      y += HEADER_H;
    }
    if (f.title.show) { out.title = { x: L, y: y, w: W, h: TITLE_H }; y += TITLE_H; }
    var bottom = B;
    if (f.footer.show) { out.footer = { x: L, y: B - FOOTER_H, w: W, h: FOOTER_H }; bottom -= FOOTER_H; }
    if (f.blocks.sum) {
      var sh = SUM_H + (f.blocks.grades ? GRADE_H : 0);
      out.sum = { x: L, y: bottom - sh, w: W, h: sh, gradeH: f.blocks.grades ? GRADE_H : 0 };
      bottom -= sh;
    }
    var n = Math.max(0, Math.min(10, f.blocks.count | 0));
    var areaH = bottom - y;
    if (n > 0 && areaH > 10) {
      var wts = f.blocks.weights && f.blocks.weights.length === n ? f.blocks.weights : null;
      var sum = 0, i;
      for (i = 0; i < n; i++) sum += wts ? wts[i] : 1;
      var by = y;
      for (i = 0; i < n; i++) {
        var bh = areaH * (wts ? wts[i] : 1) / sum;
        out.blocks.push({ i: i, x: L, y: by, w: W, h: bh, points: Number((f.blocks.points || [])[i]) || 0 });
        by += bh;
      }
      if (f.blocks.pointsCol) out.pointsCol = { x: R - POINTS_W, w: POINTS_W };
    } else {
      out.free = { x: L, y: y, w: W, h: areaH };
    }
    out.contentBottom = bottom;
    return out;
  }

  // Wo neue Elemente in einem Block hinkommen (wie in der Vorlage: Nummer 9 mm vom Rand, Inhalt ab 25 mm)
  function blockSlots(lay, block) {
    var right = (lay.pointsCol ? lay.pointsCol.x : lay.box.x + lay.box.w) - 6;
    return { numX: block.x + 9, numY: block.y + 11.5, cx: block.x + 25, cy: block.y + 10, cw: right - (block.x + 25) };
  }

  // ---------- Handgezeichnet-Stil: leicht zittrige, aber stabile Linien ----------
  function seeded(seed) {
    var h = 2166136261;
    for (var i = 0; i < seed.length; i++) { h ^= seed.charCodeAt(i); h = Math.imul(h, 16777619); }
    return function () { h ^= h << 13; h ^= h >>> 17; h ^= h << 5; return ((h >>> 0) % 10000) / 10000; };
  }
  function linePath(x1, y1, x2, y2, hand, seed) {
    if (!hand) return 'M' + r2(x1) + ' ' + r2(y1) + 'L' + r2(x2) + ' ' + r2(y2);
    var rnd = seeded(seed || (x1 + ',' + y1 + ',' + x2 + ',' + y2));
    var dx = x2 - x1, dy = y2 - y1, len = Math.sqrt(dx * dx + dy * dy) || 1;
    var nx = -dy / len, ny = dx / len, steps = Math.max(2, Math.round(len / 22)), amp = 0.45;
    var d = 'M' + r2(x1 + (rnd() - 0.5) * 0.3) + ' ' + r2(y1 + (rnd() - 0.5) * 0.3);
    for (var i = 1; i <= steps; i++) {
      var t = i / steps, tm = (i - 0.5) / steps, off = (rnd() - 0.5) * 2 * amp;
      var cx = x1 + dx * tm + nx * off, cy = y1 + dy * tm + ny * off;
      var ex = x1 + dx * t + (i === steps ? (rnd() - 0.5) * 0.3 : nx * (rnd() - 0.5) * amp);
      var ey = y1 + dy * t + (i === steps ? (rnd() - 0.5) * 0.3 : ny * (rnd() - 0.5) * amp);
      d += 'Q' + r2(cx) + ' ' + r2(cy) + ' ' + r2(ex) + ' ' + r2(ey);
    }
    return d;
  }
  function circlePath(cx, cy, r, hand, seed) {
    if (!hand) return 'M' + r2(cx - r) + ' ' + r2(cy) + 'a' + r + ' ' + r + ' 0 1 0 ' + 2 * r + ' 0a' + r + ' ' + r + ' 0 1 0 ' + -2 * r + ' 0';
    var rnd = seeded(seed || 'c' + cx + cy), n = 14, d = '', start = rnd() * Math.PI * 2;
    for (var i = 0; i <= n + 1; i++) {
      var a = start + i / n * Math.PI * 2, rr = r * (1 + (rnd() - 0.5) * 0.08);
      var px = cx + Math.cos(a) * rr, py = cy + Math.sin(a) * rr;
      d += (i === 0 ? 'M' : 'L') + r2(px) + ' ' + r2(py);
    }
    return d;
  }

  // Rahmenlinien als SVG-Pfade (in mm, Seitenkoordinaten)
  function frameSvg(doc, page, lay) {
    var s = doc.setup, hand = !!s.handdrawn, mode = s.lines || 'all', p = [];
    if (mode === 'none') return '';
    var b = lay.box, seed = page.id;
    function ln(x1, y1, x2, y2, k) { p.push(linePath(x1, y1, x2, y2, hand, seed + k)); }
    ln(b.x, b.y, b.x + b.w, b.y, 't'); ln(b.x + b.w, b.y, b.x + b.w, b.y + b.h, 'r');
    ln(b.x + b.w, b.y + b.h, b.x, b.y + b.h, 'b'); ln(b.x, b.y + b.h, b.x, b.y, 'l');
    if (mode === 'all') {
      if (lay.header) {
        ln(b.x, lay.header.y + lay.header.h, b.x + b.w, lay.header.y + lay.header.h, 'hb');
        lay.cells.forEach(function (c, i) { if (i) ln(c.x, c.y, c.x, c.y + c.h, 'hc' + i); });
      }
      if (lay.title) ln(b.x, lay.title.y + lay.title.h, b.x + b.w, lay.title.y + lay.title.h, 'tb');
      lay.blocks.forEach(function (bl, i) { if (i < lay.blocks.length - 1) ln(b.x, bl.y + bl.h, b.x + b.w, bl.y + bl.h, 'bb' + i); });
      if (lay.pointsCol && lay.blocks.length) {
        var top = lay.blocks[0].y, bot = lay.blocks[lay.blocks.length - 1].y + lay.blocks[lay.blocks.length - 1].h;
        ln(lay.pointsCol.x, top, lay.pointsCol.x, bot, 'pc');
      }
      if (lay.sum) {
        ln(b.x, lay.sum.y, b.x + b.w, lay.sum.y, 'su');
        if (lay.sum.gradeH) ln(b.x, lay.sum.y + SUM_H, b.x + b.w, lay.sum.y + SUM_H, 'sg');
      }
      if (lay.footer) ln(b.x, lay.footer.y, b.x + b.w, lay.footer.y, 'fo');
    }
    return '<path d="' + p.join('') + '" fill="none" stroke="' + esc(s.lineColor) + '" stroke-width="' + s.lineWidth + '" stroke-linecap="round" stroke-linejoin="round"/>';
  }

  // ---------- Lineatur-Zeichnung (lokale Koordinaten des Elements) ----------
  function lineaturRows(it) {
    var spec = LINEATUREN[it.kind] || LINEATUREN.L1, k = (it.scale || 100) / 100, rows = [];
    if (spec.zones) {
      var zs = spec.zones.map(function (z) { return z * k; }), rowH = zs[0] + zs[1] + zs[2], pitch = rowH + spec.gap * k;
      for (var y = 0; y + rowH <= it.h + 0.01; y += pitch) rows.push({ y: y, z: zs });
    } else if (spec.band) {
      var bh = spec.band * k, pt = spec.pitch * k;
      for (var y2 = 0; y2 + bh <= it.h + 0.01; y2 += pt) rows.push({ y: y2, band: bh });
    } else {
      var lo = spec.line * k, p2 = spec.pitch * k;
      for (var y3 = lo; y3 <= it.h + 0.01; y3 += p2) rows.push({ y: y3, single: true });
    }
    return rows;
  }
  // Höhe für n Zeilen (zum Einrasten beim Aufziehen)
  function lineaturHeightFor(it, n) {
    var spec = LINEATUREN[it.kind] || LINEATUREN.L1, k = (it.scale || 100) / 100;
    n = Math.max(1, n);
    if (spec.zones) { var rh = (spec.zones[0] + spec.zones[1] + spec.zones[2]) * k; return rh + (n - 1) * (rh + spec.gap * k); }
    if (spec.band) return spec.band * k + (n - 1) * spec.pitch * k;
    return spec.line * k + (n - 1) * spec.pitch * k + 2;
  }
  function lineaturSvg(it, lineWidth, hand) {
    var rows = lineaturRows(it), w = it.w, c = esc(it.color || '#1b2430'), lw = lineWidth || 0.3, out = [];
    var fillC = '#e4effa', mainC = '#e6e8eb';
    rows.forEach(function (r, i) {
      if (r.z) {
        var y0 = r.y, y1 = y0 + r.z[0], y2 = y1 + r.z[1], y3 = y2 + r.z[2];
        if (it.fill) {
          out.push(rect(0, y0, w, r.z[0], fillC), rect(0, y2, w, r.z[2], fillC));
        }
        if (it.main) out.push(rect(0, y1, w, r.z[1], mainC));
        var x0 = 0;
        if (it.house) {
          x0 = houseW(r);
          out.push(house(r, c, lw));
        }
        out.push(hline(x0, y0, w, c, lw, hand, i + 'a'), hline(x0, y1, w, c, lw * 0.8, hand, i + 'b'),
          hline(x0, y2, w, c, it.main ? lw * 2.2 : lw, hand, i + 'c'), hline(x0, y3, w, c, lw * 0.8, hand, i + 'd'));
        out.push('<path d="M0 ' + r2(y0) + 'V' + r2(y3) + 'M' + r2(w) + ' ' + r2(y0) + 'V' + r2(y3) + '" stroke="' + c + '" stroke-width="' + lw + '" fill="none"/>');
      } else if (r.band) {
        if (it.main) out.push(rect(0, r.y, w, r.band, mainC));
        out.push('<rect x="0" y="' + r2(r.y) + '" width="' + r2(w) + '" height="' + r2(r.band) + '" fill="none" stroke="' + c + '" stroke-width="' + lw + '"/>');
      } else {
        out.push(hline(0, r.y, w, c, lw, hand, i + 's'));
      }
    });
    return out.join('');
    function rect(x, y, ww, hh, f) { return '<rect x="' + r2(x) + '" y="' + r2(y) + '" width="' + r2(ww) + '" height="' + r2(hh) + '" fill="' + f + '"/>'; }
    function hline(x, y, ww, col, sw, hd, k) {
      return '<path d="' + linePath(x, y, ww, y, hd, it.id + k) + '" stroke="' + col + '" stroke-width="' + r2(sw) + '" fill="none"/>';
    }
    function houseW(r) { return r.z[1] * 1.6; }
    function house(r, col, sw) {
      var hw = houseW(r) - 1, y0 = r.y, y1 = y0 + r.z[0], y2 = y1 + r.z[1], y3 = y2 + r.z[2], cx = hw / 2;
      return '<path d="M0 ' + r2(y1) + 'L' + r2(cx) + ' ' + r2(y0) + 'L' + r2(hw) + ' ' + r2(y1) + 'Z" fill="#fde8c8" stroke="' + col + '" stroke-width="' + sw + '"/>' +
        '<rect x="0" y="' + r2(y1) + '" width="' + r2(hw) + '" height="' + r2(r.z[1]) + '" fill="#d9ecd4" stroke="' + col + '" stroke-width="' + sw + '"/>' +
        '<rect x="0" y="' + r2(y2) + '" width="' + r2(hw) + '" height="' + r2(r.z[2]) + '" fill="#dbe4f3" stroke="' + col + '" stroke-width="' + sw + '"/>';
    }
  }
  // Schrift in Lineaturen: je Zeile Grundlinie, Schriftgröße (mm) und Einzug, sodass die x-Höhe das Mittelband füllt.
  // xr = x-Höhe der Blattschrift im Verhältnis zur Schriftgröße (im Browser gemessen, sonst 0,5)
  var INK = '#1b2430', INK_TRACE = '#b4bcc6';
  function lineaturTextRows(it, xr) {
    var k = (it.scale || 100) / 100; xr = xr || 0.5;
    return lineaturRows(it).map(function (r) {
      if (r.z) return { base: r.y + r.z[0] + r.z[1], size: r.z[1] / xr, x: (it.house ? r.z[1] * 1.6 : 0) + 1.5 };
      if (r.band) return { base: r.y + r.band, size: r.band / xr, x: 1.5 };
      return { base: r.y, size: 4 * k / xr, x: 1.5 };
    });
  }
  function karoSize(it) { var s = it.cell || 5; return { s: s, nx: Math.floor(it.w / s + 0.001), ny: Math.floor(it.h / s + 0.001) }; }
  // cur: {r, c} = Schreibmarke beim Hineinschreiben (nur auf dem Bildschirm)
  function karoSvg(it, cur) {
    var c = esc(it.color || '#9aa8b8'), g = karoSize(it), s = g.s, nx = g.nx, ny = g.ny, d = '', out = '';
    if (cur && cur.r < ny && cur.c < nx) out += '<rect class="kcur" x="' + r2(cur.c * s) + '" y="' + r2(cur.r * s) + '" width="' + s + '" height="' + s + '" fill="rgba(47,111,228,.16)" stroke="#2f6fe4" stroke-width="0.35"/>';
    for (var i = 0; i <= nx; i++) d += 'M' + r2(i * s) + ' 0V' + r2(ny * s);
    for (var j = 0; j <= ny; j++) d += 'M0 ' + r2(j * s) + 'H' + r2(nx * s);
    out += '<path d="' + d + '" stroke="' + c + '" stroke-width="0.2" fill="none"/>';
    var ink = it.trace ? INK_TRACE : INK, cells = it.cells || {}, txt = '';
    Object.keys(cells).forEach(function (key) {
      var rc = key.split(','), r = +rc[0], cc = +rc[1], ch = cells[key];
      if (!ch || r >= ny || cc >= nx) return;
      txt += '<text x="' + r2((cc + 0.5) * s) + '" y="' + r2((r + 0.5) * s) + '">' + esc(ch) + '</text>';
    });
    if (txt) out += '<g class="ktext" fill="' + ink + '" font-size="' + r2(s * 0.78) + '" text-anchor="middle" dominant-baseline="central" style="font-family:var(--font-sheet)">' + txt + '</g>';
    var u = '';
    (it.under || []).forEach(function (r) { if (r < ny) u += 'M0 ' + r2((r + 1) * s) + 'H' + r2(nx * s); });
    if (u) out += '<path class="kunder" d="' + u + '" stroke="' + INK + '" stroke-width="0.55" fill="none"/>';
    return out;
  }

  // ---------- Nummerierung, Punkte, Noten ----------
  // Automatische Nummern in Lesereihenfolge: Seite, dann von oben nach unten, dann links nach rechts
  function numberItems(doc) {
    var list = [];
    doc.pages.forEach(function (p, pi) { p.items.forEach(function (it) { if (it.type === 'number') list.push({ it: it, pi: pi }); }); });
    list.sort(function (a, b) { return a.pi - b.pi || (Math.abs(a.it.y - b.it.y) > 4 ? a.it.y - b.it.y : a.it.x - b.it.x); });
    var n = 0, map = {};
    list.forEach(function (e) { if (e.it.auto !== false) { n++; map[e.it.id] = n; } else { map[e.it.id] = e.it.value; n = Math.max(n, Number(e.it.value) || n); } });
    return map;
  }
  function totalPoints(doc) {
    var t = 0;
    doc.pages.forEach(function (p) {
      var b = p.frame.blocks;
      if (!b.pointsCol) return;
      for (var i = 0; i < b.count; i++) t += Number((b.points || [])[i]) || 0;
    });
    return t;
  }
  function fmtPts(n) { return (Math.round(n * 2) / 2).toString().replace('.', ','); }
  function gradeRanges(doc) {
    var T = totalPoints(doc), scale = doc.grading.scale.slice().sort(function (a, b) { return a.note - b.note; }), out = [], upper = T;
    scale.forEach(function (g, i) {
      var lower = i === scale.length - 1 ? 0 : Math.ceil(g.min / 100 * T * 2) / 2;
      if (lower > upper) out.push({ note: g.note, from: null, to: null });
      else { out.push({ note: g.note, from: lower, to: upper }); upper = lower - 0.5; }
    });
    return out;
  }
  function rangeTxt(x) { return x.from === null ? '–' : x.from === x.to ? fmtPts(x.from) : fmtPts(x.to) + '–' + fmtPts(x.from); }

  // Beispielblatt: entspricht der Vorlage „Lineaturelemente“
  function exampleDoc() {
    var d = newDoc();
    d.title = 'Beispiel: Lineaturen'; d.example = true;
    var p = d.pages[0];
    p.frame.header = { name: true, datum: true, klasse: true, note: true, punkte: true, durchschnitt: true, seite: true, free: [] };
    p.frame.title.text = 'Schreibe ab.';
    var lay = frameLayout(d, p);
    var kinds = [['L1', 35], ['L2', 42], ['L3', 34], ['L4', 40]];
    lay.blocks.forEach(function (bl, i) {
      var s = blockSlots(lay, bl);
      p.items.push(newItem('number', { x: s.numX, y: s.numY }));
      var it = newItem('lineatur', { kind: kinds[i][0], x: s.cx, y: bl.y + (kinds[i][0] === 'L4' ? 2.8 : 10), w: 140 });
      it.h = lineaturHeightFor(it, i === 0 ? 2 : 3);
      p.items.push(it);
    });
    return d;
  }

  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }

  var api = {
    PAGE: PAGE, LINEATUREN: LINEATUREN, HEADER_FIELDS: HEADER_FIELDS, SUM_H: SUM_H, GRADE_H: GRADE_H, POINTS_W: POINTS_W,
    uid: uid, clone: clone, esc: esc, newDoc: newDoc, newPage: newPage, newFrame: newFrame, newItem: newItem, exampleDoc: exampleDoc,
    frameLayout: frameLayout, blockSlots: blockSlots, frameSvg: frameSvg, linePath: linePath, circlePath: circlePath,
    lineaturRows: lineaturRows, lineaturTextRows: lineaturTextRows, karoSize: karoSize, normTable: normTable, tableEdges: tableEdges, tableInsert: tableInsert, tableRemove: tableRemove, INK: INK, INK_TRACE: INK_TRACE, lineaturHeightFor: lineaturHeightFor, lineaturSvg: lineaturSvg, karoSvg: karoSvg,
    numberItems: numberItems, totalPoints: totalPoints, fmtPts: fmtPts, gradeRanges: gradeRanges, rangeTxt: rangeTxt
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.BW = api;
})(typeof self !== 'undefined' ? self : this);
