# Kapsel web-server-php 0.4.0

Server-Teil in PHP ohne Datenbank.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt die eine PHP-Datei für alle Aufrufe, ihr Schutz und der Weg zum privaten Ordner.
GILT FÜR:     Rezept web
BRAUCHT:      Kapseln kern · web-aufbau · web-daten
```

### REGELN
- 1 Eine Datei `server/api.php` für alle Aufrufe der Oberfläche; Antworten als JSON mit Statuscode. Jede Eingabe wird
  geprüft (Typ, Länge, erlaubte Werte), bevor sie gespeichert wird.
- 2 `server/.htaccess`: `Options -Indexes`; private Hilfsdateien mit `Require all denied`; Kopfzeilen
  `X-Content-Type-Options: nosniff` und `Referrer-Policy: same-origin`; HTML mit `Cache-Control: no-cache`, Symbole
  lange im Cache; `AddType application/manifest+json .webmanifest`.
- 3 Der Pfad zum privaten Ordner kommt aus einer Umgebungsvariable oder einer Hilfsdatei; im Test zeigt er auf einen
  Temp-Ordner.
- Grund: PHP läuft auf jedem einfachen Webspace; eine Datei ist leicht zu prüfen.
- Test: lokaler PHP-Server (Kapsel web-tests) mit falschen Eingaben → 400, ohne Zugang → 403.
- Stand: erprobt.

## BLOCK B – für Menschen

Ein kleiner PHP-Teil auf dem Webspace nimmt die Aufrufe der Oberfläche an und schreibt in den privaten Ordner.
