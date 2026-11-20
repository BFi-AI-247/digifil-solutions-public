# Kapsel web-sicherung 0.4.0

Tägliche Sicherung der Daten im privaten Ordner.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt die nächtliche Sicherung in einen eigenen Branch und das Wiederherstellen.
GILT FÜR:     Rezept web
BRAUCHT:      Kapseln kern · web-daten
```

### REGELN
- 1 Wenn Daten im privaten Ordner liegen, dann holt ein Workflow sie täglich per SFTP und legt sie im verwaisten
  Branch `<werkzeug>-sicherung` desselben privaten Repos ab (Fotos und große Dateien nur, wenn der Auftrag es sagt).
- 2 Vor dem Ablegen prüft der Workflow die Datei (lesbares JSON, erwartete Felder). Danach schreibt er eine
  Statusdatei in den privaten Ordner; die Oberfläche zeigt den Stand der letzten Sicherung.
- 3 Wiederherstellen: Datei aus dem Branch in den privaten Ordner hochladen. Das steht im README.
- Grund: Der Webspace ist die einzige Ablage der Daten.
- Test: erster Lauf legt den Branch an; zweiter Lauf ohne Änderung erzeugt keinen neuen Commit.
- Stand: erprobt.

## BLOCK B – für Menschen

Ein Programm auf GitHub holt die Daten jede Nacht und legt sie geprüft in einem eigenen Branch ab.
