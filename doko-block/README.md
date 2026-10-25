# Doko-Block

Ergebnisliste für eine feste Doppelkopf-Runde mit vier Leuten.
Ein Foto vom Block → die KI (Claude oder Mistral) liest die Spiele aus → prüfen → speichern. **Der Zettel gilt.**

- **Erfassen:** Foto hochladen, Entwurf mit allen Spielen, Endstand und Plätzen prüfen; Unsicheres wird markiert
- **Abende:** Liste mit Suche, Details, Foto, Löschen in den Papierkorb (wiederherstellbar)
- **Statistik:** Plätze, Jahresübersicht, Kassenbetrag je Abend, Punkte und Soli aus den erfassten Zetteln
- **Fragen:** KI-Feld für Fragen zur Statistik und Korrekturen – es macht nur Vorschläge, ausgeführt wird erst nach „Übernehmen“
- **Verlauf:** zweite Seite, auf der alle sehen, wer was gemacht hat, plus Stand der Rückmeldungen
- Termine, eigene Personenfarbe, als App auf den Home-Bildschirm (Manifest), hell und dunkel

## Einrichten

1. `server/einstellungen.example.json` nach `server/einstellungen.json` kopieren und anpassen:
   Name der Runde, die vier Spieler, Farben, Euro pro Platz, Spiele pro Abend, optional `repo` für Rückmeldungen.
2. Für jeden Spieler einen persönlichen Link erzeugen:
   ```bash
   python3 tools/make_zugang.py --neu Anna
   ```
   Die ausgegebene Prüfsumme kommt in `server/zugaenge.json` (Vorlage: `zugaenge.example.json`),
   den Link mit `#k=…` bekommt nur Anna. Im Repo und auf dem Server stehen nur Prüfsummen.
3. Beide Dateien sind per `.gitignore` ausgeschlossen. Beim Upload kommen sie aus Secrets (siehe [`beispiele/deploy.yml`](beispiele/deploy.yml)).

`tools/make_zugang.py out/zugang.php` erzeugt daraus mit den API-Schlüsseln (`ANTHROPIC_API_KEY`, `MISTRAL_API_KEY`,
optional `DOKO_GITHUB_TOKEN`) die Datei `zugang.php`.

## Aufbau auf dem Server

```
web/<pfad>/          index.html, verlauf.html, api.php, .htaccess, manifest.webmanifest, icon-*.png
privat/doko-block/   zugang.php, optional altdaten.json – dazu legt die App daten.json, fotos/, protokoll.jsonl an
```

Daten, Fotos und Protokoll liegen außerhalb des Web-Ordners und werden beim Upload nie überschrieben.
Ohne `altdaten.json` startet die Runde leer. Eine alte Excel-Liste lässt sich mit `tools/import_excel.py` übernehmen
(Spalten im Skript beschrieben, ggf. anpassen).

## Testen

```bash
python3 -m pip install playwright pillow && python3 -m playwright install chromium
bash tests/lokal.sh /tmp/doko && python3 tests/e2e.py /tmp/shots
```

Der lokale Testserver nutzt erfundene Beispieldaten (`tests/attrappe/altdaten.json`) und eine KI-Attrappe – es gehen keine Anfragen an Claude oder Mistral.

## Regeln, die eingebaut sind

20 Spiele pro Abend (16 + 4 Pflichtsoli, einstellbar), Platz 1–4, je Platz ein fester Betrag in die Kasse
(Platz 1 zahlt einmal, Platz 4 viermal). Bei Gleichstand wird gestochen; das steht auf dem Zettel.
