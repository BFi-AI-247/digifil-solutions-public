// Blog – kleine Helfer auf den Lese-Seiten: obere Zeile (Sprache, Serien, Gestaltung als Auswahl), Rückmelde-Fenster.
(function () {
  var html = document.documentElement;
  var basis = (document.querySelector('link[rel=stylesheet][href$="blog.css"]') || {}).getAttribute
    ? document.querySelector('link[rel=stylesheet][href$="blog.css"]').getAttribute('href').replace(/blog\.css$/, '') : '/';

  // Gestaltung wählen: Leser in der oberen Zeile (Kaffeehaus / digifil), in der Vorschau zusätzlich A/B/C im Schild – nur in diesem Browser gemerkt
  var auswahl = document.querySelectorAll('select[data-stilwahl]');
  var schild = document.querySelector('.vorschau-schild');
  var zeige = function () {
    auswahl.forEach(function (s) { s.value = html.dataset.stil; });
    if (schild) schild.querySelectorAll('button[data-s]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.s === html.dataset.stil)); });
  };
  var setze = function (stil) {
    html.dataset.stil = stil;
    try { localStorage.setItem('blog-stil', stil); } catch (x) {}
    zeige();
  };
  auswahl.forEach(function (s) { s.addEventListener('change', function () { setze(s.value); }); });
  if (schild) schild.addEventListener('click', function (e) { var b = e.target.closest('button[data-s]'); if (b) setze(b.dataset.s); });
  zeige();

  // Auswahllisten, die zu einer Seite springen (Sprache, Serien oben; Serien-Kasten ab 5 Serien)
  document.querySelectorAll('select[data-springe]').forEach(function (s) {
    s.addEventListener('change', function () { if (s.value) location.href = s.value; });
  });

  // Rückmeldung: Fenster über der Seite
  var fenster = document.getElementById('rm-fenster');
  if (fenster && fenster.showModal) {
    document.querySelectorAll('[data-rm-auf]').forEach(function (k) { k.addEventListener('click', function () { fenster.showModal(); }); });
    fenster.querySelectorAll('[data-rm-zu]').forEach(function (k) { k.addEventListener('click', function () { fenster.close(); }); });
    fenster.addEventListener('click', function (e) { if (e.target === fenster) fenster.close(); }); // Tippen neben das Fenster schließt
  }
  var f = document.getElementById('rm');
  if (f) f.addEventListener('submit', function (e) {
    e.preventDefault();
    var st = f.querySelector('.rm-status'), knopf = f.querySelector('button[type=submit]');
    var art = (f.querySelector('input[name=art]:checked') || {}).value || 'sonstiges';
    knopf.disabled = true; st.textContent = '…';
    fetch(basis + 'rueckmeldung.php', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: f.text.value, art: art, web: f.web.value, seite: location.pathname })
    }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (x) {
        if (x.ok) { st.textContent = st.dataset.danke; f.text.value = ''; }
        else st.textContent = x.j.fehler || 'Fehler';
      })
      .catch(function () { st.textContent = 'Keine Verbindung – bitte später noch einmal.'; })
      .finally(function () { knopf.disabled = false; });
  });
})();
