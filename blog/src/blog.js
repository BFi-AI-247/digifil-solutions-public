// Blog – kleine Helfer auf den Lese-Seiten: Rückmelde-Formular und Wahl der Gestaltung.
(function () {
  var html = document.documentElement;
  var basis = (document.querySelector('link[rel=stylesheet][href$="blog.css"]') || {}).getAttribute
    ? document.querySelector('link[rel=stylesheet][href$="blog.css"]').getAttribute('href').replace(/blog\.css$/, '') : '/';

  // Gestaltung wählen: Leser im Fuß (Kaffeehaus / digifil), in der Vorschau zusätzlich A/B/C im Schild – nur in diesem Browser gemerkt
  var wahl = document.querySelectorAll('.vorschau-schild, .stilwahl');
  var zeige = function () {
    wahl.forEach(function (w) { w.querySelectorAll('button[data-s]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.s === html.dataset.stil)); }); });
  };
  wahl.forEach(function (w) {
    w.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-s]'); if (!b) return;
      html.dataset.stil = b.dataset.s;
      try { localStorage.setItem('blog-stil', b.dataset.s); } catch (x) {}
      zeige();
    });
  });
  zeige();

  // Rückmeldung
  var f = document.getElementById('rm');
  if (f) f.addEventListener('submit', function (e) {
    e.preventDefault();
    var st = f.querySelector('.rm-status'), knopf = f.querySelector('button');
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
