# Kapsel windows-zugang 0.4.0

Zugangsschlüssel (z. B. für GitHub) in der Windows-Anmeldeinformationsverwaltung. Wahlweise.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt, wo ein lokales Werkzeug Zugangsschlüssel ablegt und wie es sie nie preisgibt.
GILT FÜR:     Rezepte lokal-python und lokal-powershell, wenn das Werkzeug selbst einen fremden Dienst anspricht.
BRAUCHT:      Kapseln kern · lokal-server
```

### REGELN
- 1 Leg den Schlüssel in der Windows-Anmeldeinformationsverwaltung ab: `advapi32` mit `CredWriteW`, `CredReadW` und
  `CredDeleteW`, Typ generisch, Persistenz lokal (nur dieser Benutzer auf diesem Rechner), Ziel `<Name>/GitHub`,
  Inhalt als UTF-16LE. Überschreib den Puffer nach dem Schreiben mit Nullen. Der Zugriff ist ein eigener, gekapselter
  Teil des Werkzeugs (wie, sagt die Laufzeit-Kapsel).
- 2 Rückfall: die Umgebungsvariable `GITHUB_TOKEN`. Sie gilt nur im Fenster, in dem sie gesetzt wurde. Ein Schlüssel mit
  Schreibrecht hat ein eigenes Ziel (z. B. `<Name>/GitHub-Protokolle`) und keinen Rückfall.
- 3 Ablegen: Der Mensch fügt den Schlüssel in der Oberfläche in ein Feld „Zugang zu GitHub“ ein und klickt „In Windows
  speichern“ (`POST /api/zugang/token`); löschen geht über `POST /api/zugang/loeschen`. Danach zeigt die Oberfläche nur
  „vorhanden ja/nein“ und die Quelle, nie den Schlüssel. Ein Schlüssel mit eigenem Ziel hat ein eigenes Feld und eigene
  Routen (z. B. `POST /api/protokolle/token` und `POST /api/protokolle/token/loeschen`). Ein Werkzeug baut nur die
  Felder, deren Schlüssel es braucht.
- 4 Ein Schlüssel steht nie in einer Datei, einer Antwort, einem Log, einem Chat oder auf der Befehlszeile. Ein Skript
  fragt ihn verdeckt ab (`Read-Host -AsSecureString`), legt ihn nicht ab, hat keinen Parameter dafür und leert am Ende
  seine Variablen.
- Grund: Windows PowerShell 5.1 schreibt jede eingetippte Befehlszeile im Klartext in eine Verlaufsdatei. Eine
  Umgebungsvariable sieht ein Start per Doppelklick nicht.
- Test: In der Bauumgebung prüft ein Test die Größe der Strukturen für x64; auf dem Zielrechner sucht der Mensch den
  Schlüssel im Installationsordner (0 Treffer).
- Stand: Python erprobt · PowerShell offen (kein Vorbild).
- Lehre: Ein Skript nahm den Zugangsschlüssel als Parameter; PowerShell 5.1 speicherte ihn im Verlauf (Regel 4).
- Lehre: Eine Installation lief mit 404, weil der Schlüssel im Konsolenfenster fehlte (Regeln 1, 2).

## BLOCK B – für Menschen

Den Schlüssel gibst du einmal in der Oberfläche ein; Windows verwahrt ihn für dein Konto. Danach steht er nirgends im
Klartext.
