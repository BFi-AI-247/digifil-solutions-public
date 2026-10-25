// Gemeinsame Helfer für beide Seiten
const DK = (() => {
  let schluessel = '';
  try {
    const m = location.hash.match(/k=([A-Za-z0-9_\-]+)/);
    if (m) { localStorage.setItem('doko-k', m[1]); history.replaceState(null, '', location.pathname + location.search); }
    schluessel = localStorage.getItem('doko-k') || '';
  } catch (e) {
    const m = location.hash.match(/k=([A-Za-z0-9_\-]+)/); if (m) schluessel = m[1];
  }
  const API = 'api.php';
  async function api(aktion, body, opt = {}) {
    const kopf = { 'X-Doko-Schluessel': schluessel };
    let daten = body;
    if (!(body instanceof FormData)) { kopf['Content-Type'] = 'application/json'; daten = JSON.stringify(body || {}); }
    let r;
    try { r = await fetch(API + '?a=' + aktion, { method: 'POST', headers: kopf, body: daten, signal: opt.signal }); }
    catch (e) { throw new Error('Keine Verbindung zum Server.'); }
    let j = {};
    try { j = await r.json(); } catch (e) { throw new Error('Der Server hat unerwartet geantwortet (' + r.status + ').'); }
    if (!r.ok) { const f = new Error(j.fehler || ('Fehler ' + r.status)); f.status = r.status; f.daten = j; throw f; }
    return j;
  }
  async function fotoUrl(id) {
    const r = await fetch(API + '?a=foto&id=' + encodeURIComponent(id), { headers: { 'X-Doko-Schluessel': schluessel } });
    if (!r.ok) throw new Error('Foto nicht gefunden');
    return URL.createObjectURL(await r.blob());
  }
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const datum = iso => { if (!iso) return ''; const [y, m, d] = iso.slice(0, 10).split('-'); return `${d}.${m}.${y}`; };
  const wochentag = iso => ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'][new Date(iso + 'T12:00').getDay()];
  const zeit = iso => { const d = new Date(iso); return d.toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric' }) + ', ' + d.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' }); };
  const euro = v => v.toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' €';
  const zahl = (v, n = 2) => v.toLocaleString('de-DE', { minimumFractionDigits: n, maximumFractionDigits: n });
  const heute = () => { const d = new Date(); return new Date(d - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10); };
  function toast(t, ms = 2600) {
    const el = document.createElement('div'); el.className = 'toast'; el.textContent = t; document.body.appendChild(el);
    setTimeout(() => el.remove(), ms);
  }
  const chips = (plaetze, spieler) => spieler.slice().sort((a, b) => plaetze[a] - plaetze[b])
    .map(s => `<span class="chip" data-p="${esc(s)}">${plaetze[s]}. ${esc(s)}</span>`).join(' ');
  function hell(hex) { const n = parseInt(hex.slice(1), 16), r = n >> 16, g = (n >> 8) & 255, b = n & 255; return (0.299 * r + 0.587 * g + 0.114 * b) / 255 > 0.6; }
  function farben(f) {
    let el = document.getElementById('personenfarben');
    if (!el) { el = document.createElement('style'); el.id = 'personenfarben'; document.head.appendChild(el); }
    el.textContent = Object.entries(f || {}).filter(([, c]) => /^#[0-9a-f]{6}$/i.test(c))
      .map(([n, c]) => `.chip[data-p="${n.replace(/"/g, '')}"],[data-farbe="${n.replace(/"/g, '')}"]{background:${c}!important;color:${hell(c) ? '#1d1a10' : '#fff'}!important}`).join('\n');
  }
  function sperre(text) {
    document.querySelector('main').innerHTML = `<div class="karte sperre"><h2>Kein Zugang</h2><p class="leise">${esc(text)}</p></div>`;
  }
  return { api, fotoUrl, esc, datum, wochentag, zeit, euro, zahl, heute, toast, chips, farben, hell, sperre, hatSchluessel: () => !!schluessel };
})();
