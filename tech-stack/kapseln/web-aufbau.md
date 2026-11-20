# Kapsel web-aufbau 0.4.0

Aufbau eines Web-Werkzeugs: Ordner, Version, Einstellungsdatei.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt Ordner, Version und Einstellungen eines Web-Werkzeugs, damit jede KI es gleich anlegt.
GILT FÜR:     Rezept web
BRAUCHT:      Kapseln kern
```

### REGELN
- 1 Ein Werkzeug = ein Ordner `<werkzeug>/` mit `src/`, `server/`, `tools/`, `tests/`, `betrieb/`, `wissen/`, `log/`
  und README.md. Was nicht hochgeladen wird (Vorlagen, Hinweise für den Server), liegt in einem eigenen Ordner und ist im
  README als „nie hochgeladen“ markiert.
- 2 Die Version steht in `src/VERSION` (z. B. 0.3.5) und wird beim Bauen in die Oberfläche eingesetzt.
- 3 Persönliche Werte (Namen einer Runde, Farben, Adressen) stehen in einer Einstellungsdatei, nicht im Code; so
  bleibt der Code gleich für die offene Fassung (Kapsel veroeffentlichung).
- Grund: Jede KI findet in jedem Werkzeug dieselben Orte.
- Test: Der Ordner hat alle Unterordner aus Regel 1; `src/VERSION` existiert.
- Stand: erprobt.

### WAHL UND LEHREN
- Lehre: Zielgerät früh festlegen (z. B. Tablet mit Touch); die Bedienung hängt daran mehr als am Code.

## BLOCK B – für Menschen

Jedes Web-Werkzeug hat denselben Aufbau. Wer eines kennt, findet sich in allen zurecht.
