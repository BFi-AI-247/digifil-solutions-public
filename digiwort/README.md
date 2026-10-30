# Digiwort

Deutsches Wortspiel: Finde das Wort in sechs Versuchen. Jeden Tag ein Rätsel mit 5 und eins mit 6 Buchstaben
(für alle gleich, neu um Mitternacht), dazu Endlos- und Schwer-Modus, Statistik, Teilen als Kästchen und Übertragung des Spielstands per Code.
Kein Konto, keine Werbung, kein Tracking – der Spielstand bleibt im Browser.

## Bauen und testen

```bash
DW_ADRESSE=https://example.org/digiwort/ DW_BETREIBER=Max python3 tools/build.py
pip install playwright && python3 -m playwright install chromium
DW_ADRESSE=https://example.org/digiwort/ python3 tests/smoke.py dist/index.html   # muss mit OK enden
```

`dist/index.html` ist das ganze Spiel in einer Datei und läuft auch ohne Server. Einstellungen beim Bauen (alle optional):

| Variable | Wirkung |
|---|---|
| `DW_ADRESSE` | öffentliche Adresse, steht am Ende des geteilten Ergebnisses; Rückmeldungen und Besuchszähler laufen nur auf diesem Host |
| `DW_BETREIBER` | Name im Rückmelde-Dialog („Max liest jede Rückmeldung.“) |
| `DW_HEIMAT` | Webseite des Betreibers, z. B. `https://example.org/` – Link unten auf der Seite und unter „Über Digiwort“ |
| `DW_QUELLCODE` | Adresse des Quellcodes, z. B. dieses Ordners auf GitHub – unter „Über Digiwort“ mit Lizenzhinweis |

Bleiben `DW_HEIMAT` und `DW_QUELLCODE` leer, entfallen Link und Abschnitt „Über Digiwort“.

## Aufbau

| Pfad | Inhalt |
|---|---|
| `src/game.html` | das ganze Spiel (HTML, CSS, JS) mit Platzhaltern für Wortlisten, Version, Fassung und Adresse |
| `data/loesungenN.txt` | Lösungswörter, **Reihenfolge = Tagesplan** |
| `data/erlaubtN.txt` | alle erlaubten Versuche |
| `server/feedback.php` | Rückmeldungen → GitHub-Issues (optional) mit Spam-Bremse, ohne IP |
| `server/zaehler.php` | Besuchszähler: nur Anzahlen pro Tag, kein Cookie, keine IP |
| `tools/build.py`, `tools/make_zugang.py` | bauen; `zugang.php` aus `DW_GITHUB_TOKEN` und `DW_REPO` erzeugen |
| `tools/wortlisten/` | Skripte, mit denen die Listen ursprünglich erzeugt wurden |

Tagesrätsel: Nr. 1 = 25.10.2026, das Wort des Tages ist `loesungenN.txt[(Tag − 1) mod Länge]`.
Darum die Reihenfolge nie ändern; ein Wort streichen heißt, es an derselben Stelle zu ersetzen. Neue Wörter nur ans Ende.

## Auf eigenem Webspace

```
web/<pfad>/          index.html, feedback.php, zaehler.php, .htaccess, manifest.webmanifest, icon-*.png
web/<pfad>/vorschau/ index.html   (aus dist/vorschau.html, optional, eigener Spielstand)
privat/digiwort/     zugang.php – dazu legen die Skripte zaehler.json und feedback-zaehler.json an
```

Anderer privater Ordner: `ort.php` neben `feedback.php` mit `<?php return ['privat' => 'name'];`.
Ein Upload-Workflow für SFTP liegt in [`beispiele/deploy.yml`](beispiele/deploy.yml).

## Wortquellen und Lizenz

- igerman98 von Björn Jacke (GPL-2.0 oder GPL-3.0), Fassung aus [wooorm/dictionaries](https://github.com/wooorm/dictionaries) – Grundlage der erlaubten Wörter
- [FrequencyWords](https://github.com/hermitdave/FrequencyWords) von Hermit Dave (Inhalt CC BY-SA 4.0, OpenSubtitles 2018) – Auswahl der Lösungswörter nach Häufigkeit
- Namen, Orte, Marken, Anstößiges und Englisches von Hand aussortiert. ß wird als SS geschrieben.

Weil die Wortlisten daraus abgeleitet sind, steht **dieser Ordner unter der GPL-3.0** ([`LICENSE`](LICENSE)) –
abweichend vom Rest des Repos (EUPL-1.2).
