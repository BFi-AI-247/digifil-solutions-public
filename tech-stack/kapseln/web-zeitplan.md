# Kapsel web-zeitplan 0.4.0

Statische Seiten mit Zeitplan.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt Seiten, die regelmäßig neue Ausgaben bekommen, gebaut von einem Agenten nach Vorlage.
GILT FÜR:     Rezept web
BRAUCHT:      Kapseln kern · web-feeds
```

### REGELN
- 1 Eine Seite, die regelmäßig neue Ausgaben erzeugt, liegt als statisches HTML auf GitHub Pages; ein Workflow mit
  Zeitplan (`cron`) veröffentlicht oder kündigt neue Ausgaben an, z. B. als Beitrag in einem sozialen Netz mit einem
  App-Passwort aus Secrets.
- 2 Zu jeder Ausgabe gibt es einen Feed; Ausgaben bleiben unter fester Adresse (Archiv).
- 3 Je Ausgabe ein Lauf eines Agenten nach einer festen Vorlage; die vorige Ausgabe ist nie die Vorlage.
- 4 Vor jedem Veröffentlichen eine Endkontrolle nach einer Liste mit prüfbaren Punkten (Zahlen, Eigennamen, Mix der
  Quellen, eigene Formulierung, Zweitquelle, Vollständigkeit); das Ergebnis steht im Bericht des Laufs.
- 5 Veröffentlichte Ausgaben sind unveränderlich; eine spätere Änderung steht als Einzeiler mit Zeitstempel oben
  und im Detail unten.
- 6 Zentrale Seiten (Startseite, Feed) baut der Lauf nie neu: Er holt den Inhalt frisch am Stand des Commits und
  fügt nur ein. Jede geschriebene Datei liest er im selben Lauf zurück und prüft die Struktur (erwartete Zahl der
  Einträge, Datei-Fuß vorhanden). Einen gekürzten Stand schreibt er nie fort.
- 7 Angekündigt wird erst, wenn die Seite ausgeliefert ist; nach Ablauf der Wartezeit kein Beitrag, sondern
  Nachholen von Hand. Eine Datei mit dem Stand der Ankündigungen verhindert doppelte Beiträge.
- 8 Zeitplan in der Ortszeit: Der Lauf für die Ankündigung startet frühestens eine Stunde nach der Ausgabe und wird
  bei jeder Zeitumstellung angepasst.
- 9 Was ein Agent im Netz recherchiert, steht in der Ausgabe vollständig in eigener Formulierung, mit Link und
  Datenstand der Quelle; die Ausgabe hängt nicht davon ab, dass die Quelle erreichbar bleibt. Volltexte fremder
  Quellen speichert kein Werkzeug.
- 10 Eine Quelle öffnet der Agent ganz, bevor er sie verwendet (Schnipsel einer Trefferliste reichen nicht). Eine
  kurze oder leere Antwort beim Abruf ist ein Fehler, kein Inhalt; dann neu holen oder eine andere Quelle nehmen.
- 11 Bei Formaten, die Tatsachen melden, sucht der Agent zu jeder Meldung eine zweite, unabhängige Quelle (Kopien
  einer Agenturmeldung zählen nicht); das prüft die Endkontrolle (Regel 4).
- Stand: erprobt (Regeln 1–11).

### WAHL UND LEHREN
- Lehre: Eine Startseite, die aus Vorlagen neu gebaut statt minimal ergänzt wurde, verlor einen Link (Regel 6).
- Lehre: Text aus Web-Abrufen kam doppelt kodiert an; Text im Speicher bauen, vor dem Commit Byte für Byte prüfen, nie
  über eine Umleitung der Shell schreiben.
- Lehre: Abrufe aus dem Netz scheitern manchmal still mit einer kurzen Fehlerantwort; ohne Prüfung von Größe und
  Inhalt wird sie als Inhalt weiterverwendet (Regel 10).
- Lehre: Ein Feed wurde beim Commit abgeschnitten und eine Ausgabe fehlte; danach ganz neu im Speicher aufbauen und
  nach jedem Commit die Struktur prüfen (Regel 6).

## BLOCK B – für Menschen

Eine Seite mit festen Ausgaben, etwa täglich, die ein Agent nach Vorlage baut und erst nach der Endkontrolle ankündigt.
