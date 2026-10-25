// Kleiner Excel-Schreiber (.xlsx) ohne fremde Bibliothek: ZIP ohne Kompression, Zahlen, Text, Datum, Formeln, Fettdruck.
// XL.datei([{ name, spalten: [Breite…], zeilen: [[zelle…]…] }]) → Blob
// Zelle: null | Zahl | Text | { v, f?, s?: 'fett' | 'datum' | 'zahl2' | 'euro' | 'fett-zahl2' | 'fett-euro' }
const XL = (() => {
  const enc = new TextEncoder();
  const CRC = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
  const crc32 = b => { let c = 0xFFFFFFFF; for (let i = 0; i < b.length; i++) c = CRC[(c ^ b[i]) & 255] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; };
  function zip(dateien) {
    const teile = [], zentral = []; let pos = 0;
    for (const [name, inhalt] of dateien) {
      const n = enc.encode(name), d = enc.encode(inhalt), c = crc32(d);
      const k = new DataView(new ArrayBuffer(30));
      k.setUint32(0, 0x04034b50, true); k.setUint16(4, 20, true); k.setUint16(6, 0x0800, true);
      k.setUint32(14, c, true); k.setUint32(18, d.length, true); k.setUint32(22, d.length, true); k.setUint16(26, n.length, true);
      teile.push(new Uint8Array(k.buffer), n, d);
      const z = new DataView(new ArrayBuffer(46));
      z.setUint32(0, 0x02014b50, true); z.setUint16(4, 20, true); z.setUint16(6, 20, true); z.setUint16(8, 0x0800, true);
      z.setUint32(16, c, true); z.setUint32(20, d.length, true); z.setUint32(24, d.length, true); z.setUint16(28, n.length, true); z.setUint32(42, pos, true);
      zentral.push(new Uint8Array(z.buffer), n);
      pos += 30 + n.length + d.length;
    }
    const groesse = zentral.reduce((s, x) => s + x.length, 0);
    const e = new DataView(new ArrayBuffer(22));
    e.setUint32(0, 0x06054b50, true); e.setUint16(8, dateien.length, true); e.setUint16(10, dateien.length, true);
    e.setUint32(12, groesse, true); e.setUint32(16, pos, true);
    return new Blob([...teile, ...zentral, new Uint8Array(e.buffer)], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
  }
  const x = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const spalte = i => { let s = ''; i++; while (i) { const m = (i - 1) % 26; s = String.fromCharCode(65 + m) + s; i = (i - m - 1) / 26; } return s; };
  const STIL = { fett: 1, datum: 2, zahl2: 3, euro: 4, 'fett-zahl2': 5, 'fett-euro': 6 };
  function blatt(b) {
    const zeilen = b.zeilen.map((z, r) => `<row r="${r + 1}">` + z.map((c, i) => {
      if (c === null || c === undefined || c === '') return '';
      const o = typeof c === 'object' ? c : { v: c };
      const ref = spalte(i) + (r + 1), s = o.s ? ` s="${STIL[o.s]}"` : '';
      if (o.f) return `<c r="${ref}"${s}><f>${x(o.f)}</f>${typeof o.v === 'number' && isFinite(o.v) ? `<v>${o.v}</v>` : ''}</c>`;
      if (typeof o.v === 'number') return `<c r="${ref}"${s}><v>${o.v}</v></c>`;
      return `<c r="${ref}" t="inlineStr"${s}><is><t xml:space="preserve">${x(o.v)}</t></is></c>`;
    }).join('') + '</row>').join('');
    const cols = (b.spalten || []).map((w, i) => `<col min="${i + 1}" max="${i + 1}" width="${w}" customWidth="1"/>`).join('');
    return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">`
      + (b.fixiert ? `<sheetViews><sheetView workbookViewId="0"><pane ySplit="${b.fixiert}" topLeftCell="A${b.fixiert + 1}" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>` : '')
      + (cols ? `<cols>${cols}</cols>` : '') + `<sheetData>${zeilen}</sheetData></worksheet>`;
  }
  function datei(blaetter) {
    const ns = 'http://schemas.openxmlformats.org';
    const f = [
      ['[Content_Types].xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="${ns}/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>${blaetter.map((_, i) => `<Override PartName="/xl/worksheets/sheet${i + 1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>`).join('')}</Types>`],
      ['_rels/.rels', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="${ns}/package/2006/relationships"><Relationship Id="rId1" Type="${ns}/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>`],
      ['xl/workbook.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="${ns}/spreadsheetml/2006/main" xmlns:r="${ns}/officeDocument/2006/relationships"><sheets>${blaetter.map((b, i) => `<sheet name="${x(b.name)}" sheetId="${i + 1}" r:id="rId${i + 1}"/>`).join('')}</sheets><calcPr calcId="0" fullCalcOnLoad="1"/></workbook>`],
      ['xl/_rels/workbook.xml.rels', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="${ns}/package/2006/relationships">${blaetter.map((_, i) => `<Relationship Id="rId${i + 1}" Type="${ns}/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet${i + 1}.xml"/>`).join('')}<Relationship Id="rId${blaetter.length + 1}" Type="${ns}/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>`],
      ['xl/styles.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="${ns}/spreadsheetml/2006/main"><numFmts count="2"><numFmt numFmtId="164" formatCode="DD.MM.YYYY"/><numFmt numFmtId="165" formatCode="#,##0.00 &quot;€&quot;"/></numFmts><fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts><fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs><cellXfs count="7"><xf/><xf fontId="1" applyFont="1"/><xf numFmtId="164" applyNumberFormat="1"/><xf numFmtId="2" applyNumberFormat="1"/><xf numFmtId="165" applyNumberFormat="1"/><xf numFmtId="2" fontId="1" applyNumberFormat="1" applyFont="1"/><xf numFmtId="165" fontId="1" applyNumberFormat="1" applyFont="1"/></cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>`],
      ...blaetter.map((b, i) => [`xl/worksheets/sheet${i + 1}.xml`, blatt(b)])
    ];
    return zip(f);
  }
  const excelDatum = iso => Math.round((Date.UTC(+iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10)) - Date.UTC(1899, 11, 30)) / 86400000);
  return { datei, excelDatum, spalte };
})();
