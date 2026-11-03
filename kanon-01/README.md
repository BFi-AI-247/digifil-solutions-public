# Kanon 01 Single Agent

Regeln für einen einzelnen KI-Worker oder -Agenten – und der Code, der sie prüft.
**Beginne mit `regeln.md`.** Stand: Kanon 01 3.1 (Regeln), Code 1.1.2.

## Was hier liegt

| Datei | Was es ist |
|---|---|
| `regeln.md` | Die Regeln: sieben Paragraphen, 42 Regeln, je Gebot – Grund – Verboten. Vorn ein Glossar und die Rangfolge Regeln > Rollen > Werkzeuge > Logs. Erste Zeile: Status und Regelstand. |
| `antwortschema.json` | JSON-Schema für die Antwort eines Workers: Felder `regelstand`, `erfahrungsstand`, `antwort`, `unsicher`, dazu `aenderungen` (nur nach Freigabe) und `erfahrung` (höchstens eine je Lauf). |
| `kanon_basis.py`, `kanon_basis.php` | Prüfbausteine ohne Abhängigkeiten: Regelstand lesen und abgleichen, Schema prüfen, Freigabe-Wort erkennen, gezeigten Text mit geschriebenem vergleichen, Rücklese nach dem Schreiben, Sperrliste, Laufzeile, Erfahrungen laden und anhängen. Jede Funktion nennt die Regel, die sie absichert. |
| `beispiel_worker.py` | Ein vollständiger Worker als Vorlage: liest Regeln und Erfahrungen, baut den Prompt, prüft die Antwort, schreibt nur nach Freigabe, liest zurück, schreibt die Laufzeile. Läuft auch ohne Modell (Trockenlauf). |
| `beispiel/` | Zwei Beispielantworten (Vorschlag, Freigabe). |
| `tests/` | Tests für die Bausteine und den Beispiel-Worker (Python, im Ordner: `python3 -m unittest discover -s tests`; PHP: `php tests/test_kanon_basis.php`). |
| `rollendatei-vorlage.md` | Vorlage für die Rollendatei einer Instanz, die über viele Aufträge lebt (Chat): Rechte, Pfade, Stände, Stand, offene Punkte, Übergabe. |

## Wie es zusammenspielt

Regeln im Prompt lenken, Prüfungen im Code gelten. Der Worker bekommt `regeln.md` und die
Erfahrungen seiner Rolle als System-Prompt und antwortet mit einem JSON-Objekt nach
`antwortschema.json`. Das Programm liest den Regelstand aus der ersten Zeile von `regeln.md` (`kanon_basis.regeln_laden`), prüft die Antwort (Schema, Regelstand, Erfahrungsstand), schreibt
nur, was der Mensch im gezeigten Wortlaut freigegeben hat, liest jede Datei nach dem Schreiben
zurück und hängt eine gültige Erfahrung an. Was die Regeln verlangen und wie der Code es absichert,
steht an jeder Regel (Klammer mit der alten Kennung B1–B41) und an jeder Funktion.

Zwei Schichten: KERN gilt für jede Instanz, BETRIEB zusätzlich für Instanzen mit Rollendatei. Ein
Worker ist KERN; er nennt in jeder Antwort Regelstand und Erfahrungsstand (§1.3).

## Noch nicht hier

Eine Schritt-für-Schritt-Anleitung zum Einrichten eines Workers mit diesen Bausteinen gibt es aus
der Fassung 2.3; sie wird auf die Paragraphen-Fassung umgestellt und dann hier abgelegt.
