# Kapsel web-tests 0.4.0

Tests für Web-Werkzeuge.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt lokaler Server, Durchlauf im Browser, Rauchtest und Prüfskripte.
GILT FÜR:     Rezept web
BRAUCHT:      Kapseln kern
```

### REGELN
- 1 `tests/lokal.sh <ordner>` startet `php -S 127.0.0.1:<port>` mit einem privaten Temp-Ordner und Attrappen
  (KI, GitHub); `tests/e2e.py` klickt den Ablauf in Chromium (Playwright) durch und legt Bilder ab.
- 2 `tests/smoke.py` prüft die gebaute Seite: lädt ohne Konsolenfehler, Kernfunktion geht. Der Workflow lässt ihn vor
  jedem Hochladen laufen (Kapsel web-auslieferung).
- 3 Prüfskripte für Daten und Inhalte (Wortlisten, Kartendateien, Quellenlisten) laufen vor dem Bauen; ein Fehler
  stoppt den Bau.
- 4 Bei Spielen und Regeln: ein Simulator spielt zufällige Partien und prüft feste Regeln; jeder Lauf hängt eine
  Zeile an ein Protokoll.
- Test: Alle drei laufen ohne Netz.
- Stand: erprobt (Regeln 1–3) · gebaut (Regel 4).

## BLOCK B – für Menschen

Vor jedem Hochladen läuft das Werkzeug lokal mit Testdaten und einmal im echten Browser durch.
