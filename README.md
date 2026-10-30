# digifil-solutions-public

Kleine, offene Werkzeuge für den Alltag – entstanden im Dialog mit KI, gedacht zum Nachbauen und Selbst-Hosten.
Jedes Werkzeug läuft auf einfachem PHP-Webspace, braucht keine Datenbank und speichert nichts bei Dritten.

| Ordner | Was es ist |
|---|---|
| [`blattwerk/`](blattwerk/) | Arbeitsblatt-Editor für die Grundschule (Klasse 1–4), gemacht fürs iPad: Seitenrahmen, frei platzierte Elemente, Lineaturen, Ausgabe als PDF. |
| [`blog/`](blog/) | Kleines Blog-Werkzeug: Beiträge mit Serien, Deutsch und Englisch, Editor im Browser, Feeds, Import aus einem bestehenden Blog. |
| [`digiwort/`](digiwort/) | Deutsches Wortspiel: jeden Tag ein Wort mit 5 und eins mit 6 Buchstaben, sechs Versuche. Eine einzige HTML-Datei, kein Tracking. |
| [`doko-block/`](doko-block/) | Ergebnisliste für eine feste Doppelkopf-Runde: Foto vom Block → KI liest die Spiele aus → prüfen → speichern. Statistik, Kasse, Termine. |
| [`zwei-kanal-format/`](zwei-kanal-format/) | Kein Programm, sondern ein Schreibformat für Texte, nach denen eine KI handeln soll (Aufträge zwischen KI-Agenten, Anleitungen): Block A für die KI, Block B für den Menschen. Mit Konzept, zwei Vorlagen und zwei Beispielen. |

## Gemeinsame Bauweise

- **Ein Ordner = ein Werkzeug**, mit `src/` (Oberfläche), `server/` (PHP), `tools/` (Bauen, Zugang erzeugen), `tests/` (Browser-Tests mit Playwright).
  Ausnahme: `zwei-kanal-format/` besteht nur aus Markdown-Dateien und ist in sich abgeschlossen.
- **Geheimes liegt nie im Repo.** Passwörter, API-Schlüssel und persönliche Zugänge erzeugt `tools/make_zugang.py` beim Upload als `zugang.php` in einem Ordner außerhalb des Web-Verzeichnisses.
- **Rückmeldungen als Issues (optional).** Alle Werkzeuge haben einen Rückmelde-Knopf, der Issues in einem Repo deiner Wahl anlegt.
- **Upload per GitHub Actions.** Unter `beispiele/deploy.yml` liegt je ein Workflow für SFTP-Webspace; er ist nicht aktiv, bis du ihn nach `.github/workflows/` kopierst.

## Woher der Code kommt

Die Werkzeuge entstehen in privaten Repos und laufen dort auch im eigenen Betrieb – mit genau diesem Code.
Persönliches (Namen, Pfade, Schlüssel, Daten) steckt nur in Einstellungen, die privat bleiben.
[`werkzeug/spiegel.py`](werkzeug/spiegel.py) übernimmt neue Stände als Pull Request hierher und bricht ab,
sobald ein verbotener Begriff oder ein Schlüssel auftaucht. Neues Werkzeug = ein Eintrag mehr in der Spiegel-Konfiguration.
Für eigenständige Texte wie `zwei-kanal-format/` prüft er zusätzlich, dass kein Verweis aus dem Ordner herausführt, keine internen
Kennungen vorkommen und keine Platzhalter in spitzen Klammern stehen, die GitHub nicht anzeigen würde.

## Selbst ausprobieren

```bash
# Blattwerk – reine Seite, läuft auch ohne Server
cd blattwerk && python3 tools/build.py && open dist/index.html

# Doko-Block – lokaler Testserver mit Beispieldaten und KI-Attrappe (PHP 8 nötig)
cd doko-block && bash tests/lokal.sh /tmp/doko
# → http://127.0.0.1:8765/#k=testschluessel
```

Zum Zwei-Kanal-Format: mit [`zwei-kanal-format/README.md`](zwei-kanal-format/README.md) beginnen – die Anleitung ist selbst in dem Format geschrieben.

## Lizenz

[EUPL-1.2](LICENSE) – frei nutzbar, veränderbar und weitergebbar; Verbesserungen an verteilten Fassungen bleiben offen.
**Ausnahme:** [`digiwort/`](digiwort/) steht unter der [GPL-3.0](digiwort/LICENSE), weil seine Wortlisten aus GPL-Quellen stammen.
Die Schriften Andika und Lexend (Blattwerk) stehen unter der SIL Open Font License und werden nicht mitgeliefert, sondern beim Bauen geladen.
