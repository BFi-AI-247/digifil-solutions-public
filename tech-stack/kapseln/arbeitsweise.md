# Kapsel arbeitsweise 0.4.0

Wie Mensch und KI ein Werkzeug gemeinsam bauen: Ablauf, Regeln für KI-Instanzen, Belege. Wahlweise.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt den Ablauf des Baus und die Belege; dazu Regeln und Rollen für KI-Instanzen, wenn das Projekt
              sie hat.
GILT FÜR:     jedes Rezept, wahlweise. Regeln 1–3 gelten immer, wenn das Rezept diese Kapsel nennt; Regel 4 nur, wenn
              das Projekt Regeln für KI-Instanzen und Rollen führt; Regel 5 nur bei geplanten Läufen.
BRAUCHT:      Kapsel kern
```

### REGELN
- 1 Ablauf (Intent-Driven Development): Der Mensch nennt Bedarf und Grund · eine KI schlägt vor und stellt höchstens
  drei Rückfragen, jede mit Empfehlung · der Mensch entscheidet, seine Worte kommen wörtlich in den Auftrag · Auftrag
  als Datei im Repo · Bau in Paketen, das riskanteste zuerst, Sperrpunkt auf dem Zielsystem · Zwischenstand · Review
  durch eine zweite KI mit Datei und Zeile · Abnahme am echten System. Keine KI prüft ihre eigene Arbeit; was gelten
  soll, steht als Datei im Repo.
- 2 Belege: Jede Regel einer Kapsel und jede Abnahme hat einen Beleg mit Datei, Zeile und Commit des Vorbilds. Belege, die
  interne Namen tragen, stehen in einer eigenen Datei, die nicht öffentlich ist.
- 3 Ein Auftrag und eine Anleitung folgen dem Zwei-Kanal-Format (Fassung 1.3, Vorlagen `readme-vorlage.md` und
  `auftrag-vorlage.md` aus `zwei-kanal-format/` in digifil-solutions-public).
- 4 Wenn das Projekt sie hat: Regeln für KI-Instanzen nach `kanon-01/` (Single Agent) in digifil-solutions-public; jede
  Instanz hat eine Rolle mit Kennung und Grenzen, ohne Rolle schreibt sie nicht ins Repo; die Rollendatei nennt den
  Ordner des Werkzeugs. Hat das Projekt keine, dann behauptet das Werkzeug keine Kenntnis von Rollen- oder Regeldateien,
  die nicht vorliegen; für ein bestehendes Repo gelten zusätzlich dessen tatsächlich gelesene Regeln.
- 5 Geplante Läufe: Änderungen am Werkzeug baut ein geplanter Lauf nach `betrieb/ARBEITSWEISE.md` in einen
  Vorschau-Branch; live geht es erst nach Freigabe des Menschen. Jeder Lauf schreibt ein Protokoll nach `log/`.
- Grund: Was gelten soll, steht als Datei; so kann jede neue KI weiterbauen, und eine zweite KI kann prüfen.
- Stand: erprobt.

## BLOCK B – für Menschen

Diese Kapsel beschreibt, wie ein Werkzeug mit KI entsteht: Du nennst Bedarf und Grund, die KI fragt höchstens dreimal
nach, und am Ende prüfst du auf dem echten System. Ob dabei feste Rollen für KI-Instanzen gelten, entscheidet das
Projekt.
