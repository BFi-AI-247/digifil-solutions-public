# digifil-solutions-public

Kleine, offene Werkzeuge für den Alltag – entstanden im Dialog mit KI, gedacht zum Nachbauen und Selbst-Hosten.
Jedes Werkzeug läuft auf einfachem PHP-Webspace, braucht keine Datenbank und speichert nichts bei Dritten.

| Ordner | Was es ist |
|---|---|
| [`blattwerk/`](blattwerk/) | Arbeitsblatt-Editor für die Grundschule (Klasse 1–4), gemacht fürs iPad: Seitenrahmen, frei platzierte Elemente, Lineaturen, Ausgabe als PDF. |
| [`doko-block/`](doko-block/) | Ergebnisliste für eine feste Doppelkopf-Runde: Foto vom Block → KI liest die Spiele aus → prüfen → speichern. Statistik, Kasse, Termine. |

## Gemeinsame Bauweise

- **Ein Ordner = ein Werkzeug**, mit `src/` (Oberfläche), `server/` (PHP), `tools/` (Bauen, Zugang erzeugen), `tests/` (Browser-Tests mit Playwright).
- **Geheimes liegt nie im Repo.** Passwörter, API-Schlüssel und persönliche Zugänge erzeugt `tools/make_zugang.py` beim Upload als `zugang.php` in einem Ordner außerhalb des Web-Verzeichnisses.
- **Rückmeldungen als Issues (optional).** Beide Werkzeuge haben einen Rückmelde-Knopf, der Issues in einem Repo deiner Wahl anlegt.
- **Upload per GitHub Actions.** Unter `beispiele/deploy.yml` liegt je ein Workflow für SFTP-Webspace; er ist nicht aktiv, bis du ihn nach `.github/workflows/` kopierst.

## Selbst ausprobieren

```bash
# Blattwerk – reine Seite, läuft auch ohne Server
cd blattwerk && python3 tools/build.py && open dist/index.html

# Doko-Block – lokaler Testserver mit Beispieldaten und KI-Attrappe (PHP 8 nötig)
cd doko-block && bash tests/lokal.sh /tmp/doko
# → http://127.0.0.1:8765/#k=testschluessel
```

## Lizenz

[EUPL-1.2](LICENSE) – frei nutzbar, veränderbar und weitergebbar; Verbesserungen an verteilten Fassungen bleiben offen.
Die Schriften Andika und Lexend (Blattwerk) stehen unter der SIL Open Font License und werden nicht mitgeliefert, sondern beim Bauen geladen.
