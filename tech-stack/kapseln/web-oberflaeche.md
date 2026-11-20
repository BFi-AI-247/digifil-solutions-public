# Kapsel web-oberflaeche 0.4.0

Oberfläche eines Web-Werkzeugs.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt die Oberfläche im Browser: eine Datei oder klassische Skripte, wahlweise als installierbare Web-App.
GILT FÜR:     Rezept web
BRAUCHT:      Kapseln kern · web-aufbau
```

### REGELN
- 1 Wenn das Werkzeug klein ist, dann ist die Oberfläche eine einzige HTML-Datei mit CSS und JavaScript; ein
  Bauskript `tools/build.py` setzt Platzhalter ein (z. B. `__VERSION__`) und schreibt `dist/`.
- 2 Wenn es größer ist, dann klassische Skripte ohne Build-Kette, die sich einen Namensraum teilen. Die Ladereihenfolge
  steht in `index.html` und ist verbindlich: Code, der beim Laden sofort läuft, nutzt nur früher geladene Dateien.
- 3 Wahlweise als installierbare Web-App: `manifest.webmanifest`, Symbole in 180, 192 und 512 Pixeln, ein Service
  Worker mit einer Konstante `VERSION`. Wenn sich eine Datei der Hülle ändert, dann erhöhst du `VERSION`; der Service
  Worker löscht beim Aktivieren alle Caches mit anderer Version. Daten holt er zuerst aus dem Netz.
- 4 Texte der Oberfläche stehen gesammelt (eine Tabelle je Sprache); Inhalte setzt du mit `textContent`, nie als HTML
  aus Nutzerdaten.
- 5 Ein Knopf „Rückmeldung“ ist auf jeder Seite (Kapsel rueckmeldungen). Die Vorschau zeigt ein gelbes Schild.
- Grund: Ohne Build-Kette kann jede KI und jeder Mensch die Dateien direkt lesen und ändern.
- Falle: Ein Service Worker ohne neue `VERSION` liefert die alte Hülle weiter aus – der Nutzer sieht die Änderung nie.
- Test: Durchlauf im Browser (Kapsel web-tests) lädt die Seite ohne Konsolenfehler.
- Stand: erprobt (einzelne HTML-Datei, klassische Skripte, Service Worker mit `VERSION`).

### WAHL UND LEHREN
- W2 Einzelne HTML-Datei mit Bauskript oder klassische Skripte ohne Build (Regeln 1, 2).
- Lehre: Ein Service Worker ohne neue `VERSION` hält alte Dateien fest (Regel 3).

## BLOCK B – für Menschen

Die Oberfläche braucht keine Build-Kette und läuft auch als App auf dem Tablet.
