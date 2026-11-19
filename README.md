# digifil-solutions-public

Kleine, offene Werkzeuge, Regeln und Vorlagen für die Arbeit mit KI – zum Nachbauen, Selbst-Hosten und Weiterverwenden.

| Ordner | Was es ist | Voraussetzungen |
|---|---|---|
| [`blattwerk/`](blattwerk/) | Arbeitsblatt-Editor für die Grundschule (Klasse 1–4), gemacht fürs iPad: Seitenrahmen, frei platzierte Elemente, Lineaturen, Ausgabe als PDF. | Betrieb: PHP-Webspace. Gebaut wird automatisch auf GitHub (`beispiele/deploy.yml`) oder von der einrichtenden KI. |
| [`blog/`](blog/) | Kleines Blog-Werkzeug: Beiträge mit Serien, Deutsch und Englisch, Editor im Browser, Feeds, Import aus einem bestehenden Blog. | Betrieb: PHP-Webspace; für die Übersetzung ein Mistral-API-Schlüssel. Gebaut von der einrichtenden KI. |
| [`digiwort/`](digiwort/) | Deutsches Wortspiel: jeden Tag ein Wort mit 5 und eins mit 6 Buchstaben, sechs Versuche. Eine einzige HTML-Datei, kein Tracking. | Betrieb: Webspace; PHP nur für Zähler und Rückmeldungen. Gebaut wird automatisch auf GitHub (`beispiele/deploy.yml`) oder von der einrichtenden KI. |
| [`doko-block/`](doko-block/) | Ergebnisliste für eine feste Doppelkopf-Runde: Foto vom Block → KI liest die Spiele aus → prüfen → speichern. Statistik, Kasse, Termine. | Betrieb: PHP-8-Webspace und ein API-Schlüssel für Claude oder Mistral. Gebaut wird automatisch auf GitHub (`beispiele/deploy.yml`) oder von der einrichtenden KI. |
| [`kanon-01/`](kanon-01/) | Kanon 01 Single Agent 3.1 – Regeln für einen einzelnen KI-Worker oder -Agenten (42 Regeln in sieben Paragraphen, je Gebot – Grund – Verboten), dazu Antwortschema, Prüfbausteine Python/PHP, Beispiel-Worker und Tests. | Lesen: keine. Prüfbausteine: Python 3 oder PHP. |
| [`skills/`](skills/) | Skills für KI-Assistenten. `bfi-mail-checker`: prüft E-Mails, Briefe und andere Texte auf Rechtschreibung, Grammatik und Zeichensetzung und gibt den korrigierten Text mit Kommentaren auf Deutsch zurück. | Ein KI-Assistent: die `SKILL.md` als Skill hinzufügen oder ihren Text zu Beginn des Gesprächs als Anweisung geben. |
| [`tech-stack/`](tech-stack/) | Kein Programm, sondern eine Bauvorgabe für lokale Werkzeuge auf einem Windows-Rechner (Python mit SQLite, Oberfläche im Browser, Updates über GitHub), mit den Berichten ihrer Prüfungen. | Lesen: keine. Bauen lassen: eine KI mit eigener Bauumgebung. Die Werkzeuge laufen auf Windows 11, ohne Administratorrechte. |
| [`zwei-kanal-format/`](zwei-kanal-format/) | Kein Programm, sondern ein Schreibformat für Texte, nach denen eine KI handeln soll (Aufträge zwischen KI-Agenten, Anleitungen): Block A für die KI, Block B für den Menschen. Mit Konzept, zwei Vorlagen und zwei Beispielen. | Keine. |

## BLOCK A – für die lesende KI

```text
ZWECK:        Du findest den Ordner, der zur Aufgabe passt, prüfst seine Voraussetzungen und arbeitest dann nach
              dessen eigener Anleitung weiter. Dieser Text ist erfüllt, wenn du den Ordner (oder „keiner passt“),
              das Ergebnis der Voraussetzungen und die Anleitung nennst, nach der du weiterarbeitest.
GILT FÜR:     Menschen und KI-Instanzen, die einen Ordner dieses Repos nutzen, nachbauen, betreiben oder prüfen.
GILT NICHT:   Einrichtung und Bedienung eines einzelnen Ordners (steht in dessen Anleitung, siehe DATEIEN) · die
              privaten Repos, aus denen der Inhalt stammt.
VORAUSSETZUNG: Lesezugriff auf dieses Repo. Die Spalte „Voraussetzungen“ der Tabelle oben ist eine Kurzfassung;
              vollständig stehen sie in der Anleitung des Ordners.
DATEIEN:      README.md (dieser Einstieg) · LICENSE (EUPL-1.2) · werkzeug/spiegel.py (übernimmt neue Stände aus den
              privaten Repos und prüft sie) · Anleitung je Ordner der Tabelle: dessen README.md; für skills/ die
              SKILL.md des Skills.
BEGRIFFE:     passt = die Aufgabe ist das, wofür der Ordner laut Spalte „Was es ist“ gebaut ist; ein ähnlicher
              Ordner für einen anderen Zweck passt nicht.
              unbekannt = aus Aufgabe und Umgebung nicht erkennbar; zählt wie „fehlt“, bis es geklärt ist.
              Web-Werkzeug = blattwerk/, blog/, digiwort/, doko-block/: Oberfläche in src/, PHP in server/, Bauen und
              Zugang erzeugen in tools/, Tests in tests/ (Playwright); Betrieb auf eigenem Webspace.
```

### SCHRITTE (in dieser Reihenfolge; jeder Schritt hat ein prüfbares Ergebnis)

1. **Ordner wählen.** Lies die Spalte „Was es ist“ und wähle den Ordner, der zur Aufgabe passt (BEGRIFFE). Ist ein
   Ordner nur ähnlich, nennst du ihn als „ähnlich, braucht Umbau“ und wählst ihn nicht.
   *Ergebnis:* Du nennst einen Ordner mit dem Satz der Tabelle, der zur Aufgabe passt, oder „keiner passt“.
2. **Voraussetzungen prüfen.** Gleiche zuerst die Spalte „Voraussetzungen“ und dann das Feld VORAUSSETZUNG (oder den
   entsprechenden Abschnitt) in der Anleitung des Ordners mit der Umgebung ab, in der gebaut oder betrieben wird.
   *Ergebnis:* Du nennst jede Voraussetzung mit „vorhanden“, „fehlt“ oder „unbekannt“; vor dem Bau ist keine offen.
3. **Nach der Anleitung des Ordners arbeiten.** Öffne die Anleitung des Ordners (DATEIEN) und folge ihr.
   *Ergebnis:* Du nennst die Anleitung und ihren ersten Schritt; ab dann gilt sie.

```text
PRÜFUNG:      Ordner (oder „keiner passt“), jede Voraussetzung mit Status und die Anleitung mit ihrem ersten Schritt
              sind genannt.
FAIL-MODE:    Wenn kein Ordner passt, dann sagst du das; einen ähnlichen nennst du nur als „ähnlich, braucht Umbau“. Wenn eine Voraussetzung fehlt, dann
              nennst du sie und baust nicht auf Verdacht. Wenn eine Anleitung nicht reicht, dann melde es als Issue in
              diesem Repo, mit Datei und Zeile; ohne Zugang dazu nennst du es dem Menschen, für den du arbeitest.
NICHT TUN:    Zugangsdaten, Passwörter und API-Schlüssel gehören nie in ein Repo; die Web-Werkzeuge erzeugen sie beim
              Upload mit tools/make_zugang.py in einem Ordner außerhalb des Web-Verzeichnisses. · Gib keinen Ordner
              unter einer anderen Lizenz weiter, als in „Lizenz“ unten steht.
LIEFERUNG:    Gewählter Ordner oder „keiner passt“ · Voraussetzungen mit „vorhanden“/„fehlt“/„unbekannt“ · genutzte
              Anleitung · jede Stelle, an der dieser Text nicht reichte, mit Zitat.
REFERENZ:     Abschnitte „Woher der Inhalt kommt“ und „Lizenz“ unten.
```

---

## BLOCK B – für Menschen

Alles hier ist im Gespräch mit KI entstanden und läuft im eigenen Alltag: vier kleine Web-Werkzeuge für einfachen
Webspace, dazu Regeln, ein Schreibformat, eine Bauvorgabe und ein Skill für die Arbeit mit KI-Assistenten. Welche
Ordner einen Server brauchen und welche nur gelesen werden, zeigt die Spalte „Voraussetzungen“.

Die Web-Werkzeuge sind gleich gebaut. Geheimes liegt nie im Repo, Rückmeldungen gehen auf Wunsch als Issues in ein Repo
deiner Wahl, und blattwerk/, digiwort/ und doko-block/ bringen unter `beispiele/deploy.yml` einen Upload-Workflow für
SFTP-Webspace mit; er ist nicht aktiv, bis du ihn nach `.github/workflows/` kopierst.

## Woher der Inhalt kommt

Alles entsteht in privaten Repos und läuft dort im eigenen Betrieb – mit genau diesem Stand. Persönliches (Namen, Pfade,
Schlüssel, Daten) steckt nur in Einstellungen, die privat bleiben. [`werkzeug/spiegel.py`](werkzeug/spiegel.py) übernimmt
neue Stände als Pull Request hierher und bricht ab, sobald ein verbotener Begriff oder ein Schlüssel auftaucht. Für
eigenständige Texte wie `zwei-kanal-format/` und `tech-stack/` prüft er zusätzlich, dass kein Verweis aus dem Ordner
herausführt, keine internen Kennungen vorkommen und keine Platzhalter in spitzen Klammern stehen, die GitHub nicht
anzeigen würde.

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
**Ausnahme:** [`digiwort/`](digiwort/) steht unter der [GPL-3.0](digiwort/LICENSE), weil seine Wortlisten aus GPL-Quellen stammen.
Die Schriften Andika und Lexend (Blattwerk) stehen unter der SIL Open Font License und werden nicht mitgeliefert, sondern beim Bauen geladen.
