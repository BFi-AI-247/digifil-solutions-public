# Kapsel rueckmeldungen 0.4.0

Rückmeldungen aus dem Werkzeug als Issues im Repo. Wahlweise.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt den Knopf „Rückmeldung“ und was mit der Rückmeldung geschieht.
GILT FÜR:     jedes Rezept, wahlweise; Regel 1 für lokale Werkzeuge, Regeln 2–4 für Web-Werkzeuge, Regel 5 für beide.
BRAUCHT:      Kapsel kern; im Web zusätzlich web-zugang
```

### REGELN
- 1 Lokal: Ein Knopf „Rückmeldung“ öffnet im Browser die Seite `https://github.com/{owner}/{repo}/issues/new` mit
  vorbelegtem Titel, Label und Text (Version, Browser, Zustand, Fehlerart). Der Mensch ergänzt und sendet selbst; das
  Werkzeug braucht dafür keinen Schlüssel. Vorbelegt werden nur technische Angaben; Meldungstexte, die Pfade, Datei-
  oder Servernamen oder Firmendaten enthalten können, gehören nicht dazu. Bei einem privaten Repo braucht der Mensch
  dort Zugang; die README sagt das.
- 2 Web: Der Knopf „Rückmeldung“ ist auf jeder Seite und schickt Art, Text und technische Angaben (Version, Browser) an
  `server/rueckmeldung.php`; der Server legt mit dem Schlüssel aus `zugang.php` ein Issue an, mit den Labels
  `<werkzeug>`, `rueckmeldung` und der Art. Persönliche Daten kommen nur hinein, wenn der Nutzer sie selbst schreibt.
  Ein öffentliches Werkzeug nimmt Rückmeldungen ohne persönlichen Link an; eines mit Zugang nur mit gültigem Schlüssel.
- 3 Inhalte, die Nutzer im Werkzeug anlegen (Beiträge, Ergebnisse), gehen nicht über Git; nur Änderungen am Werkzeug.
- 4 Wahlweise reagiert ein Workflow (Issue-Assistent) auf Issues mit dem Label des Werkzeugs, ordnet sie ein und
  antwortet aus dem Code.
- 5 Eine Rückmeldung ist kein Diagnosepaket. Technische Angaben darüber hinaus stellt das Werkzeug nur über eine
  Positivliste ohne Firmendaten zusammen und zeigt sie vor dem Senden vollständig an; es gibt keinen Upload ohne Zutun
  des Menschen.
- Grund: Rückmeldungen landen dort, wo gebaut wird.
- Test: lokal prüft ein Test die vorbelegte Adresse; im Web die Rückmeldung aus der Vorschau gegen eine Attrappe der
  GitHub-API (eine Umgebungsvariable `…_GITHUB_API` zeigt auf den Test).
- Stand: Web erprobt · lokal gebaut · Regel 5 Empfehlung (unbelegt).

## BLOCK B – für Menschen

Mit einem Klick auf „Rückmeldung“ wird aus einem Fehler oder Wunsch eine Aufgabe im Repo. Lokal schickst du sie selbst
ab; im Web legt der Server sie an.
