# Kapsel austausch 0.4.0

Daten zwischen lokalen Werkzeugen über Dateien mit Version; Dateien von außen und für den Menschen.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt Austauschdateien, Eingänge und Exporte, damit nie ein halber oder gemischter Stand gelesen wird und
              Firmendaten auf dem Rechner bleiben.
GILT FÜR:     Rezepte lokal-python und lokal-powershell, wenn das Werkzeug Daten liefert, liest oder exportiert.
BRAUCHT:      Kapseln kern · daten-json
```

### REGELN
- 1 Werkzeuge tauschen Daten lokal über JSON-Dateien aus. Der Vertrag steht als eigene Markdown-Datei mit Nummer der
  Version im Repo des liefernden Werkzeugs: `format`, ganzzahlige `version`, Datentypen, Pflichtfelder, Zeitdarstellung,
  Schlüssel und Fehlerverhalten.
- 2 Jede Datei trägt `format`, `version`, `table`, `exported_at`, `filter`, `columns`, `rows` und `row_count`; sie heißt
  `<art>_<JJJJMMTT-hhmmss>.json`.
- 3 Ein Exportlauf: Alle Dateien tragen denselben Zeitstempel und dasselbe `exported_at`. Erst entstehen alle als `.tmp`,
  dann werden alle umbenannt. Bricht der Lauf ab, dann entsteht keine `.json`, und die `.tmp` werden entfernt.
  Empfehlung (unbelegt): Bei mehreren Dateien schließt eine Manifest-Datei mit Prüfsummen den Satz ab; erst sie gibt
  ihn frei.
- 4 Der Leser nimmt den jüngsten vollständigen Satz und prüft `format`, `version`, `table`, `row_count` und das gleiche
  `exported_at` (und das Manifest, wenn es eines gibt). Eine unbekannte Version deutet er nicht: Er liest den Satz nicht
  ein, meldet gelesene und erwartete Version in Log und Oberfläche, und seine Daten bleiben auf dem zuletzt gelesenen
  Stand. `.tmp` zählt nicht. Er liest nur.
- 5 Ein neues Feld bedeutet eine neue Version des Vertrags; sie zählt getrennt von der Version des Werkzeugs (Kapsel
  kern). Der Vertrag wird vorher mit dem Leser abgestimmt: schriftlich im Repo, mit der Rolle oder dem Menschen, der den
  Leser baut. Empfehlung (unbelegt): Zuerst lernt der Leser die neue Version und liest die alte weiter, dann schreibt der
  Lieferer die neue; so fällt beim Update keiner aus. Beim Lieferer steigt zudem die zweite Stelle der Version.
- 6 Der Ablageort ist eine Einstellung beider Werkzeuge; der Lieferer schreibt dorthin, der Leser liest dort. Den Ordner
  nennt der Auftrag oder der Mensch. Wie lange alte Sätze liegen bleiben, ist offen.
- 7 Dateien von außen (z. B. ein CSV-Eingang) liest das Werkzeug nur, aus einem Ordner, den der Mensch in der Oberfläche
  wählt oder der in der Einstellung steht; sie bleiben auf dem Zielrechner. Eine Datei, die noch geschrieben wird,
  verarbeitet es erst nach einem vereinbarten Fertig-Signal oder nach erfolgreichem exklusivem Lesen; im Zweifel
  zurückstellen und melden (Empfehlung, unbelegt). „Original gesichert“ heißt nur, wenn die Bytes gesichert sind.
- 8 Dateien für den Menschen (z. B. eine Tabelle auf Knopfdruck) legt das Werkzeug in einen eigenen Unterordner unter
  `Data/`, je Lauf ein Ordner mit Zeitstempel (z. B. `Data/Export/<art>-JJJJMMTT-hhmmss/`). Eine vorhandene Datei
  überschreibt es nie. Das Format nennt der Auftrag.
- 9 CSV für Excel: dokumentiertes Trennzeichen, richtige Maskierung, UTF-8 mit BOM. Werte, die mit `=`, `+`, `-` oder `@`
  beginnen, werden im Export für Menschen gegen Ausführung als Formel geschützt; die gespeicherten Rohwerte bleiben
  unverändert. Für den Austausch zwischen Werkzeugen gilt Regel 2, nicht CSV.
- Grund: So lesen zwei Werkzeuge nie einen halben oder gemischten Stand, und Firmendaten bleiben auf dem Rechner.
- Test: unvollständiger Satz · falsche Zeilenzahl · neue Version · Export und Import gleichzeitig · Umlaute, Kyrillisch,
  `&`, `<`, Anführungszeichen und ein Emoji überstehen den Weg.
- Stand: Export erprobt; Leser gebaut (Python); Manifest des Satzes, Fertig-Signal und Formelschutz Empfehlung
  (unbelegt); PowerShell offen.

## BLOCK B – für Menschen

Werkzeuge reichen Daten über Dateien weiter, die eine Version tragen. Ein Werkzeug liest nur vollständige Sätze, und
alles bleibt auf deinem Rechner.
