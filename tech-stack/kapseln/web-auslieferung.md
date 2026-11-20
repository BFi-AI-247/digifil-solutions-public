# Kapsel web-auslieferung 0.4.0

Auslieferung auf den Webspace: live und Vorschau.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt Bauen, Prüfen und Hochladen per Workflow, mit Vorschau vor dem Livegang.
GILT FÜR:     Rezept web
BRAUCHT:      Kapseln kern · web-aufbau · web-tests
```

### REGELN
- 1 Ein Workflow je Werkzeug, ausgelöst durch Push auf `main` (live) und auf den Vorschau-Branch (Vorschau), nur für
  Pfade des Werkzeugs. Ablauf: bauen → Rauchtest im Browser (Kapsel web-tests) → Zugangsdatei erzeugen → hochladen.
- 2 Hochladen per SFTP mit `lftp`; der Schlüssel des Servers ist festgelegt (`known_hosts` aus einem Secret,
  `StrictHostKeyChecking=yes`). Hochgeladen werden einzelne Dateien mit `put`, kein Spiegeln mit Löschen.
- 3 Die Vorschau hat eine eigene Adresse, ein gelbes Schild und eigene Daten (eine Kopie oder ein eigener Präfix);
  Einträge dort zählen nicht; mit Server-Daten hat die Vorschau einen eigenen privaten Ordner. Suchmaschinen sehen die
  Vorschau nicht.
- 4 Eine statische Seite ohne Server-Teil kann auf GitHub Pages liegen (W3).
- Grund: Kein Mensch lädt von Hand hoch; jeder Stand ist ein Commit.
- Falle: Scheitert der Rauchtest, dann darf nichts hochgeladen werden – der Schritt bricht den Lauf ab.
- Test: ein Push auf den Vorschau-Branch; die Vorschau zeigt die neue Version.
- Stand: erprobt.

### WAHL UND LEHREN
- W3 Webspace mit PHP oder GitHub Pages (Regel 4; für Seiten mit Zeitplan Kapsel web-zeitplan).
- Lehre: Die Vorschau braucht eigene Daten, sonst zählen Probeeinträge mit (Regel 3).

## BLOCK B – für Menschen

Jede Änderung erscheint erst in einer Vorschau mit gelbem Schild; live geht sie nach Freigabe.
