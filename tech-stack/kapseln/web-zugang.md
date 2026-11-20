# Kapsel web-zugang 0.4.0

Zugang und Geheimnisse eines Web-Werkzeugs.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt Schlüssel für fremde Dienste und persönliche Links ohne Konto.
GILT FÜR:     Rezept web
BRAUCHT:      Kapseln kern · web-server-php
```

### REGELN
- 1 Schlüssel für fremde Dienste (GitHub, KI-Anbieter) stehen nur in GitHub Secrets. Beim Ausliefern schreibt
  `tools/make_zugang.py` daraus `zugang.php` und lädt sie in den privaten Ordner. Fehlt ein Schlüssel, dann ist die
  Funktion aus und das Werkzeug sagt es.
- 2 Persönlicher Zugang ohne Konto: jeder bekommt einen Link `…/<Name>/#k=<schlüssel>`. Der Schlüssel steht nach `#`
  und geht so nicht in Server-Logs; im Repo steht nur sein SHA-256 (`server/zugaenge.json`). Das Gerät merkt sich den
  Schlüssel, bis der Nutzer sich abmeldet.
- 3 Kein Schlüssel eines Dienstes liegt in der Oberfläche; Aufrufe fremder Dienste gehen über den Server.
- 4 Neuer Link: ein Skript in `tools/` erzeugt einen Schlüssel, trägt seine Prüfsumme in `server/zugaenge.json` ein
  und gibt den Link einmal aus; der Mensch verteilt ihn, die nächste Auslieferung macht ihn gültig. Zurückziehen:
  Eintrag löschen und ausliefern.
- Grund: Ein öffentliches oder gespiegeltes Repo darf nichts Geheimes enthalten.
- Falle: Ein Schlüssel als Parameter in der Adresse (`?k=`) landet in Logs und Verlauf.
- Test: Suche im Repo nach Schlüsselmustern ergibt nichts; ein Aufruf ohne gültigen Schlüssel ergibt 403.
- Stand: erprobt.

## BLOCK B – für Menschen

Schlüssel liegen nur in den Geheimnissen von GitHub; Nutzer bekommen einen persönlichen Link statt eines Kontos.
