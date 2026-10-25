# Blattwerk

Arbeitsblatt-Editor für die Grundschule (Klasse 1–4), gemacht fürs iPad – ohne App-Store, im Browser.
Der Schwerpunkt liegt auf der **Gestaltung**: Inhalte bringt die Lehrkraft selbst mit. Es werden keine Schülerdaten verarbeitet.

## Was der Editor kann

- **Seitenrahmen:** Kopfzeile (Name, Datum, Klasse, Note, Punkte, Durchschnitt, Seite, freie Felder), Titelzeile,
  1–10 Aufgabenblöcke mit verschiebbaren Trennlinien, Punkte-Spalte, Summenfeld mit Notenschlüssel, Fußzeile
- **Seite einrichten:** Ränder, Linien ohne/außen/alle, Liniendicke und -farbe, Handgezeichnet-Stil
- **Elemente:** Aufgabennummern (automatisch in Lesereihenfolge), Textfelder, Lineatur 1–4, Kästchen, Bilder
- **Lineaturen** L1–L4 für die Klassenstufen, Höhe 50–300 %, Hauptzeile hervorheben, Ober-/Unterlänge einfärben, Schreibhäuschen
- **Bedienung per Touch:** Antippen fügt in den nächsten freien Block ein, Ziehen setzt frei; Einrasten an Rahmen und Elementen
- Mehrere Seiten, Rückgängig/Wiederholen, Zoom, Drucken/PDF (eine A4-Seite pro Blattseite)
- Blätter bleiben im Browser gespeichert (IndexedDB), Sicherung als `.blattwerk.json`

## Bauen und testen

```bash
python3 tools/fetch_fonts.py      # optional: Andika + Lexend selbst ausliefern (keine Anfragen an Google)
python3 tools/build.py            # → dist/index.html, dist/vorschau.html
pip install playwright && python3 -m playwright install chromium
python3 tests/smoke.py dist/index.html
```

`dist/index.html` funktioniert auch allein (z. B. direkt im Browser geöffnet) – dann ohne Passwort und ohne Rückmelde-Knopf.

## Auf eigenem Webspace betreiben

Aufbau auf dem Server (Ordner `privat` neben dem Web-Ordner, nicht abrufbar):

```
web/<pfad>/            index.php, lib.php, feedback.php, .htaccess, fonts/
web/<pfad>/vorschau/   index.php   (aus server/vorschau-index.php, optional)
privat/blattwerk/      app.html, app-vorschau.html, zugang.php
```

- `server/index.php` ist die **Passwort-Tür**; die App selbst liegt in `privat/` und wird erst nach der Anmeldung ausgeliefert.
  Ein Gerät bleibt 180 Tage angemeldet, ein neues Passwort meldet alle Geräte ab. Abmelden: `…/<pfad>/?abmelden`.
- `tools/make_zugang.py` erzeugt `zugang.php` aus Umgebungsvariablen:
  `BW_PASSWORT` (Pflicht, mind. 8 Zeichen – gespeichert wird nur ein Hash), `BW_PFAD` (z. B. `/blattwerk/`),
  optional `BW_GITHUB_TOKEN` + `BW_REPO` (Rückmeldungen als Issues), `BW_BETREIBER` (Name in Hinweisen),
  `BW_COOKIE` (Name des Anmelde-Cookies) und `BW_LABEL_RUECKFRAGE` (Label für Rückfragen, Vorgabe `rueckfrage`).
- Anderer privater Ordner als `privat/blattwerk`: `ort.php` neben `lib.php` mit `<?php return ['privat' => 'name'];`.
- Ein fertiger Upload-Workflow für SFTP liegt in [`beispiele/deploy.yml`](beispiele/deploy.yml).

## Rückmeldungen

Der Knopf „Rückmeldung“ legt über `server/feedback.php` ein Issue an (Labels `rueckmeldung` + Art: `fehler`, `wunsch`, `frage`),
auf Wunsch mit dem aktuellen Blatt als JSON. Die App zeigt den Stand der bisherigen Rückmeldungen
(Labels `rueckfrage`, `vorschau`, `live`). Der GitHub-Schlüssel braucht nur das Recht „Issues: Lesen und Schreiben“ für dieses eine Repo.

Entscheidungen zur Gestaltung: [`wissen/entscheidungen.md`](wissen/entscheidungen.md).
