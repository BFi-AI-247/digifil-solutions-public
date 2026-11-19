# Tech-Stack für Web-Werkzeuge 0.3

<!-- Zwei-Kanal-Format 1.3 (readme-vorlage): BLOCK A muss allein genügen, BLOCK B ist Klartext für Menschen. -->

## BLOCK A – für die bauende KI

```text
ZWECK:        Ein neues Web-Werkzeug so bauen, wie die bisherigen gebaut sind: Oberfläche im Browser, Daten im Browser
              oder als Dateien auf einem gemieteten Webspace mit PHP, Bau, Test und Auslieferung über GitHub. Das Ziel ist
              erreicht, wenn das Werkzeug die Schritte des Startpakets mit ihren Ergebnissen erfüllt und jede Abweichung
              in ANNAHMEN.md steht.
GILT FÜR:     eine KI, die ein neues Web-Werkzeug baut oder ein bestehendes an diese Vorgabe angleicht.
GILT NICHT:   Werkzeuge, die auf dem eigenen Rechner laufen (dafür gilt TECH-STACK.md in diesem Ordner) · Fachlogik
              und Inhalte des Werkzeugs (stehen im Auftrag) · Arbeitsweise der Rollen (TECH-STACK.md, Baustein 12) ·
              Recherche im Netz: Sie ist Fähigkeit der Umgebung eines Agenten; das Werkzeug bekommt nur ihr Ergebnis.
VORAUSSETZUNG: ein Webspace mit PHP und Zugang per SFTP, außerhalb des Web-Verzeichnisses ein privater Ordner · ein
              GitHub-Repo mit Actions · Bauumgebung mit Python ab 3.12 und Playwright (Chromium), PHP-Kommandozeile für
              lokale Tests · Server und Zugänge stehen nur in GitHub Secrets, Pfade und persönliche Werte in der
              Einstellungsdatei (1.3), nie im Code.
DATEIEN:      README.md des Werkzeugs (Zwei-Kanal-Format) · `src/` (Oberfläche) · `server/` (PHP, `.htaccess`) · `tools/`
              (Bauen, Zugangsdatei erzeugen, Prüfskripte) · `tests/` (lokaler Server, Durchlauf im Browser, Attrappen) ·
              `betrieb/` (ARBEITSWEISE.md), `wissen/` (entscheidungen.md), `log/` (Protokolle der Läufe).
BEGRIFFE:     <werkzeug> = Ordnername in Kleinbuchstaben · <Name> = Name in der Adresse · privater Ordner = Ordner auf
              dem Webspace außerhalb des Web-Verzeichnisses, z. B. `/privat/<werkzeug>/` · Vorschau = zweite Adresse des
              Werkzeugs, gebaut aus einem eigenen Branch · Attrappe = Ersatz für einen fremden Dienst im Test ·
              persönliche Daten = Namen, Ergebnisse, Fotos, Texte der Nutzer; sie bleiben im privaten Ordner oder im
              Browser · stehen = erprobt (läuft live) · gebaut (getestet, nicht live) · offen (noch nirgends gebaut).
```

### SCHRITTE – Startpaket (in dieser Reihenfolge; jeder Schritt hat ein prüfbares Ergebnis)

1. **Auftrag lesen.** Lies den Auftrag und diese Datei ganz. Leg den Ordner nach Baustein 1 an.
   *Ergebnis:* README.md (Block A und B), `wissen/entscheidungen.md` mit den Festlegungen aus dem Auftrag.
2. **Datenweg wählen.** Entscheide nach W1: Daten im Browser oder im privaten Ordner. Schreib die Wahl in
   `wissen/entscheidungen.md`.
   *Ergebnis:* Die Wahl steht mit Grund im Repo.
3. **Oberfläche bauen** nach Baustein 2, Daten nach Baustein 3, Server nach Baustein 4.
   *Ergebnis:* `bash tests/lokal.sh` startet das Werkzeug mit Testdaten; der Durchlauf im Browser (Baustein 11) endet
   mit „OK“.
4. **Zugang und Auslieferung** nach Baustein 5 und 6: Zugangsdatei aus Secrets, Workflow für live und Vorschau.
   *Ergebnis:* Ein Push auf den Vorschau-Branch zeigt das Werkzeug unter der Vorschau-Adresse mit gelbem Schild.
5. **Sicherung** nach Baustein 7, wenn Daten im privaten Ordner liegen.
   *Ergebnis:* Der erste Lauf legt den Sicherungs-Branch an und schreibt eine Statusdatei.
6. **Rückmeldung** nach Baustein 8.
   *Ergebnis:* Ein Klick auf „Rückmeldung“ in der Vorschau legt ein Issue mit dem Label des Werkzeugs an.
7. **Freigabe.** Der Mensch prüft die Vorschau und gibt frei; dann geht `main` live.
   *Ergebnis:* Der Mensch bestätigt die Live-Adresse; du trägst jeden Baustein als „erprobt“, „gebaut“ oder „offen“
   in README oder ANNAHMEN.md ein.

### BAUSTEINE (Vorgaben mit Grund, Falle, Test und Stand)

**Baustein 1 – Aufbau eines Werkzeugs**
- 1.1 Ein Werkzeug = ein Ordner `<werkzeug>/` mit `src/`, `server/`, `tools/`, `tests/`, `betrieb/`, `wissen/`, `log/`
  und README.md. Was nicht hochgeladen wird (Vorlagen, Hinweise für den Server), liegt in einem eigenen Ordner und ist im
  README als „nie hochgeladen“ markiert.
- 1.2 Die Version steht in `src/VERSION` (z. B. 0.3.5) und wird beim Bauen in die Oberfläche eingesetzt.
- 1.3 Persönliche Werte (Namen einer Runde, Farben, Adressen) stehen in einer Einstellungsdatei, nicht im Code; so
  bleibt der Code gleich für die offene Fassung (Baustein 12).
- Grund: Jede KI findet in jedem Werkzeug dieselben Orte.
- Test: Der Ordner hat alle Unterordner aus 1.1; `src/VERSION` existiert.
- Stand: erprobt.

**Baustein 2 – Oberfläche**
- 2.1 Wenn das Werkzeug klein ist, dann ist die Oberfläche eine einzige HTML-Datei mit CSS und JavaScript; ein
  Bauskript `tools/build.py` setzt Platzhalter ein (z. B. `__VERSION__`) und schreibt `dist/`.
- 2.2 Wenn es größer ist, dann klassische Skripte ohne Build-Kette, die sich einen Namensraum teilen. Die Ladereihenfolge
  steht in `index.html` und ist verbindlich: Code, der beim Laden sofort läuft, nutzt nur früher geladene Dateien.
- 2.3 Wahlweise als installierbare Web-App: `manifest.webmanifest`, Symbole in 180, 192 und 512 Pixeln, ein Service
  Worker mit einer Konstante `VERSION`. Wenn sich eine Datei der Hülle ändert, dann erhöhst du `VERSION`; der Service
  Worker löscht beim Aktivieren alle Caches mit anderer Version. Daten holt er zuerst aus dem Netz.
- 2.4 Texte der Oberfläche stehen gesammelt (eine Tabelle je Sprache); Inhalte setzt du mit `textContent`, nie als HTML
  aus Nutzerdaten.
- 2.5 Ein Knopf „Rückmeldung“ ist auf jeder Seite (Baustein 8). Die Vorschau zeigt ein gelbes Schild.
- Grund: Ohne Build-Kette kann jede KI und jeder Mensch die Dateien direkt lesen und ändern.
- Falle: Ein Service Worker ohne neue `VERSION` liefert die alte Hülle weiter aus – der Nutzer sieht die Änderung nie.
- Test: Durchlauf im Browser (Baustein 11) lädt die Seite ohne Konsolenfehler.
- Stand: erprobt (einzelne HTML-Datei, klassische Skripte, Service Worker mit `VERSION`).

**Baustein 3 – Daten**
- 3.1 Zwei Wege (W1): im Browser oder im privaten Ordner auf dem Server.
- 3.2 Im Browser: `localStorage` mit einem Präfix je Werkzeug (die Vorschau mit eigenem Präfix) für kleine Stände,
  IndexedDB für Dokumente. Jeder Zugriff steht in `try/catch`. Der Nutzer kann alles als Datei sichern und wieder laden;
  für den Wechsel des Geräts gibt es einen Übertragungs-Code ohne Server.
- 3.3 Auf dem Server: JSON-Dateien im privaten Ordner. Schreiben unter einer Sperre (`flock`), erst in eine `.tmp`, dann
  `rename`. Ein Protokoll als `.jsonl`, eine Zeile je Änderung, nur anhängen. Löschen heißt Papierkorb, wiederherstellbar.
- 3.4 Eine Auslieferung (Workflow nach Baustein 6) lädt nie Daten in den privaten Ordner, außer der Zugangsdatei
  (Baustein 5); vorhandene Daten überschreibt sie nie. Das Wiederherstellen aus der Sicherung (7.3) ist ein eigener
  Schritt, den ein Mensch auslöst.
- 3.6 Jede Speicherung zählt einen Stand (`stand` + 1). Ändern zwei Personen gleichzeitig, dann gewinnt die letzte; das
  Protokoll zeigt beide. Empfehlung (unbelegt): Die Oberfläche schickt den gelesenen Stand mit; weicht er ab, dann
  antwortet der Server mit 409 und die Oberfläche lädt neu.
- 3.5 Ein neues Format liest alte Daten weiter. Die Reihenfolge einer Liste, an der etwas hängt (z. B. ein Tagesplan),
  änderst du nie; du ersetzt an gleicher Stelle oder hängst hinten an.
- Grund: Kein Datenbankserver; Dateien lassen sich sichern und von Hand prüfen.
- Falle: Zwei gleichzeitige Speichervorgänge ohne Sperre löschen einen davon.
- Test: zwei gleichzeitige Schreibvorgänge im lokalen Test; Laden einer alten Datei aus `tests/attrappe/`.
- Stand: erprobt.

**Baustein 4 – Server (PHP, ohne Datenbank)**
- 4.1 Eine Datei `server/api.php` für alle Aufrufe der Oberfläche; Antworten als JSON mit Statuscode. Jede Eingabe wird
  geprüft (Typ, Länge, erlaubte Werte), bevor sie gespeichert wird.
- 4.2 `server/.htaccess`: `Options -Indexes`; private Hilfsdateien mit `Require all denied`; Kopfzeilen
  `X-Content-Type-Options: nosniff` und `Referrer-Policy: same-origin`; HTML mit `Cache-Control: no-cache`, Symbole
  lange im Cache; `AddType application/manifest+json .webmanifest`.
- 4.3 Der Pfad zum privaten Ordner kommt aus einer Umgebungsvariable oder einer Hilfsdatei; im Test zeigt er auf einen
  Temp-Ordner.
- Grund: PHP läuft auf jedem einfachen Webspace; eine Datei ist leicht zu prüfen.
- Test: lokaler PHP-Server (Baustein 11) mit falschen Eingaben → 400, ohne Zugang → 403.
- Stand: erprobt.

**Baustein 5 – Zugang und Geheimnisse**
- 5.1 Schlüssel für fremde Dienste (GitHub, KI-Anbieter) stehen nur in GitHub Secrets. Beim Ausliefern schreibt
  `tools/make_zugang.py` daraus `zugang.php` und lädt sie in den privaten Ordner. Fehlt ein Schlüssel, dann ist die
  Funktion aus und das Werkzeug sagt es.
- 5.2 Persönlicher Zugang ohne Konto: jeder bekommt einen Link `…/<Name>/#k=<schlüssel>`. Der Schlüssel steht nach `#`
  und geht so nicht in Server-Logs; im Repo steht nur sein SHA-256 (`server/zugaenge.json`). Das Gerät merkt sich den
  Schlüssel, bis der Nutzer sich abmeldet.
- 5.3 Kein Schlüssel eines Dienstes liegt in der Oberfläche; Aufrufe fremder Dienste gehen über den Server.
- 5.4 Neuer Link: ein Skript in `tools/` erzeugt einen Schlüssel, trägt seine Prüfsumme in `server/zugaenge.json` ein
  und gibt den Link einmal aus; der Mensch verteilt ihn, die nächste Auslieferung macht ihn gültig. Zurückziehen:
  Eintrag löschen und ausliefern.
- Grund: Ein öffentliches oder gespiegeltes Repo darf nichts Geheimes enthalten.
- Falle: Ein Schlüssel als Parameter in der Adresse (`?k=`) landet in Logs und Verlauf.
- Test: Suche im Repo nach Schlüsselmustern ergibt nichts; ein Aufruf ohne gültigen Schlüssel ergibt 403.
- Stand: erprobt.

**Baustein 6 – Auslieferung**
- 6.1 Ein Workflow je Werkzeug, ausgelöst durch Push auf `main` (live) und auf den Vorschau-Branch (Vorschau), nur für
  Pfade des Werkzeugs. Ablauf: bauen → Rauchtest im Browser (Baustein 11) → Zugangsdatei erzeugen → hochladen.
- 6.2 Hochladen per SFTP mit `lftp`; der Schlüssel des Servers ist festgelegt (`known_hosts` aus einem Secret,
  `StrictHostKeyChecking=yes`). Hochgeladen werden einzelne Dateien mit `put`, kein Spiegeln mit Löschen.
- 6.3 Die Vorschau hat eine eigene Adresse, ein gelbes Schild und eigene Daten (eine Kopie oder ein eigener Präfix);
  Einträge dort zählen nicht; mit Server-Daten hat die Vorschau einen eigenen privaten Ordner. Suchmaschinen sehen die
  Vorschau nicht.
- 6.4 Eine statische Seite ohne Server-Teil kann auf GitHub Pages liegen (W3).
- Grund: Kein Mensch lädt von Hand hoch; jeder Stand ist ein Commit.
- Falle: Scheitert der Rauchtest, dann darf nichts hochgeladen werden – der Schritt bricht den Lauf ab.
- Test: ein Push auf den Vorschau-Branch; die Vorschau zeigt die neue Version.
- Stand: erprobt.

**Baustein 7 – Sicherung**
- 7.1 Wenn Daten im privaten Ordner liegen, dann holt ein Workflow sie täglich per SFTP und legt sie im verwaisten
  Branch `<werkzeug>-sicherung` desselben privaten Repos ab (Fotos und große Dateien nur, wenn der Auftrag es sagt).
- 7.2 Vor dem Ablegen prüft der Workflow die Datei (lesbares JSON, erwartete Felder). Danach schreibt er eine
  Statusdatei in den privaten Ordner; die Oberfläche zeigt den Stand der letzten Sicherung.
- 7.3 Wiederherstellen: Datei aus dem Branch in den privaten Ordner hochladen. Das steht im README.
- Grund: Der Webspace ist die einzige Ablage der Daten.
- Test: erster Lauf legt den Branch an; zweiter Lauf ohne Änderung erzeugt keinen neuen Commit.
- Stand: erprobt.

**Baustein 8 – Rückmeldungen und Betrieb**
- 8.1 Der Knopf „Rückmeldung“ schickt Art, Text und technische Angaben (Version, Browser) an `server/rueckmeldung.php`;
  der Server legt mit dem Schlüssel aus `zugang.php` ein Issue an, mit den Labels `<werkzeug>`, `rueckmeldung` und der
  Art. Persönliche Daten kommen nur hinein, wenn der Nutzer sie selbst schreibt. Ein öffentliches Werkzeug nimmt
  Rückmeldungen ohne persönlichen Link an; eines mit Zugang (5.2) nur mit gültigem Schlüssel.
- 8.2 Ein Workflow (Issue-Assistent) reagiert auf Issues mit dem Label des Werkzeugs, ordnet sie ein und antwortet
  aus dem Code.
- 8.3 Änderungen am Werkzeug baut ein geplanter Lauf nach `betrieb/ARBEITSWEISE.md` in den Vorschau-Branch; live geht
  es erst nach Freigabe des Menschen. Jeder Lauf schreibt ein Protokoll nach `log/`.
- 8.4 Inhalte, die Nutzer im Werkzeug anlegen (Beiträge, Ergebnisse), gehen nicht über Git; nur Änderungen am Werkzeug.
- Grund: Rückmeldungen landen dort, wo gebaut wird; nichts geht ungeprüft live.
- Test: Rückmeldung aus der Vorschau gegen eine Attrappe der GitHub-API (`…_GITHUB_API` zeigt auf den Test).
- Stand: erprobt.

**Baustein 9 – KI-Anbindung**
- 9.1 KI-Aufrufe gehen nur über den Server; die Schlüssel stehen in `zugang.php`. Wenn mehrere Anbieter möglich sind,
  dann wählt der Nutzer; fehlt ein Schlüssel, dann sagt der Server „nicht eingerichtet“ (503).
- 9.2 Die KI macht nur Vorschläge. Ausgeführt wird erst, wenn der Mensch „Übernehmen“ drückt.
- 9.3 Antworten der KI liest das Werkzeug tolerant: Es sucht das erwartete JSON auch in umgebendem Text und meldet, was
  es nicht lesen konnte, statt abzubrechen (Stand: gebaut, als eigene Sammlung von Lesern für PHP, JavaScript und
  Python).
- 9.4 Im Test ersetzt eine Attrappe die KI (Umgebungsvariable, die auf einen Ordner mit festen Antworten zeigt).
- 9.5 Ohne eigenen Schlüssel keine KI-Funktion für Fremde; eine Ausnahme gibt nur der Auftrag.
- Grund: Kosten und Fehler der KI bleiben beim Menschen sichtbar und umkehrbar.
- Test: Durchlauf mit Attrappe; Anfrage ohne Schlüssel ergibt 503.
- Stand: erprobt (9.1, 9.2, 9.4) · gebaut (9.3).

**Baustein 10 – Fremde Quellen und Feeds**
- 10.1 Ein Werkzeug hat keine freie Suche im Netz. Fremde Feeds holt nur der Server, und nur aus einer festen Liste
  erlaubter Quellen. Er puffert die Antwort
  (z. B. 10 Minuten), repariert falsch kodierte Zeichen und liefert ein einheitliches JSON.
- 10.2 Eigene Inhalte bietet das Werkzeug als Atom-Feed an (`feed.xml`), mit `<link rel="alternate">` in jeder Seite.
- Grund: Keine offene Weiterleitung; die Oberfläche sieht immer dieselbe Form.
- Test: Quelle außerhalb der Liste ergibt einen Fehler; ein Feed mit falschen Zeichen kommt repariert an.
- Stand: erprobt.

**Baustein 11 – Tests**
- 11.1 `tests/lokal.sh <ordner>` startet `php -S 127.0.0.1:<port>` mit einem privaten Temp-Ordner und Attrappen
  (KI, GitHub); `tests/e2e.py` klickt den Ablauf in Chromium (Playwright) durch und legt Bilder ab.
- 11.2 `tests/smoke.py` prüft die gebaute Seite: lädt ohne Konsolenfehler, Kernfunktion geht. Der Workflow lässt ihn vor
  jedem Hochladen laufen (6.1).
- 11.3 Prüfskripte für Daten und Inhalte (Wortlisten, Kartendateien, Quellenlisten) laufen vor dem Bauen; ein Fehler
  stoppt den Bau.
- 11.4 Bei Spielen und Regeln: ein Simulator spielt zufällige Partien und prüft feste Regeln; jeder Lauf hängt eine
  Zeile an ein Protokoll.
- Test: Alle drei laufen ohne Netz.
- Stand: erprobt (11.1–11.3) · gebaut (11.4).

**Baustein 12 – Veröffentlichung**
- 12.1 Eine offene Fassung entsteht durch Spiegeln in ein öffentliches Repo. Der Spiegel prüft eine Liste verbotener
  Begriffe (Namen, Orte, Adressen) und bricht bei einem Treffer ab; persönliche Werte stehen deshalb nur in
  Einstellungen (1.3).
- 12.2 Code, der in beiden Fassungen gleich ist, wird im privaten Repo gepflegt und gespiegelt, nie im öffentlichen
  geändert.
- Stand: erprobt.

**Baustein 13 – Statische Seiten mit Zeitplan**
- 13.1 Eine Seite, die regelmäßig neue Ausgaben erzeugt, liegt als statisches HTML auf GitHub Pages; ein Workflow mit
  Zeitplan (`cron`) veröffentlicht oder kündigt neue Ausgaben an, z. B. als Beitrag in einem sozialen Netz mit einem
  App-Passwort aus Secrets.
- 13.2 Zu jeder Ausgabe gibt es einen Feed; Ausgaben bleiben unter fester Adresse (Archiv).
- 13.3 Je Ausgabe ein Lauf eines Agenten nach einer festen Vorlage; die vorige Ausgabe ist nie die Vorlage.
- 13.4 Vor jedem Veröffentlichen eine Endkontrolle nach einer Liste mit prüfbaren Punkten (Zahlen, Eigennamen, Mix der
  Quellen, eigene Formulierung, Zweitquelle, Vollständigkeit); das Ergebnis steht im Bericht des Laufs.
- 13.5 Veröffentlichte Ausgaben sind unveränderlich; eine spätere Änderung steht als Einzeiler mit Zeitstempel oben
  und im Detail unten.
- 13.6 Zentrale Seiten (Startseite, Feed) baut der Lauf nie neu: Er holt den Inhalt frisch am Stand des Commits und
  fügt nur ein. Jede geschriebene Datei liest er im selben Lauf zurück und prüft die Struktur (erwartete Zahl der
  Einträge, Datei-Fuß vorhanden). Einen gekürzten Stand schreibt er nie fort.
- 13.7 Angekündigt wird erst, wenn die Seite ausgeliefert ist; nach Ablauf der Wartezeit kein Beitrag, sondern
  Nachholen von Hand. Eine Datei mit dem Stand der Ankündigungen verhindert doppelte Beiträge.
- 13.8 Zeitplan in der Ortszeit: Der Lauf für die Ankündigung startet frühestens eine Stunde nach der Ausgabe und wird
  bei jeder Zeitumstellung angepasst.
- 13.9 Was ein Agent im Netz recherchiert, steht in der Ausgabe vollständig in eigener Formulierung, mit Link und
  Datenstand der Quelle; die Ausgabe hängt nicht davon ab, dass die Quelle erreichbar bleibt. Volltexte fremder
  Quellen speichert kein Werkzeug.
- 13.10 Eine Quelle öffnet der Agent ganz, bevor er sie verwendet (Schnipsel einer Trefferliste reichen nicht). Eine
  kurze oder leere Antwort beim Abruf ist ein Fehler, kein Inhalt; dann neu holen oder eine andere Quelle nehmen.
- 13.11 Bei Formaten, die Tatsachen melden, sucht der Agent zu jeder Meldung eine zweite, unabhängige Quelle (Kopien
  einer Agenturmeldung zählen nicht); das prüft die Endkontrolle (13.4).
- Stand: erprobt (13.1–13.11).

### WAHLMÖGLICHKEITEN
- W1 Daten im Browser (kein Server, kein Konto, Sicherung durch den Nutzer) oder im privaten Ordner (mehrere Nutzer
  teilen Daten, Sicherung nach Baustein 7). Empfehlung: im Browser, wenn nur eine Person die Daten braucht.
- W2 Einzelne HTML-Datei mit Bauskript oder klassische Skripte ohne Build (2.1, 2.2).
- W3 Webspace mit PHP oder GitHub Pages (6.4, 13).
- W4 KI-Anbieter: Claude oder Mistral, wählbar (9.1).

### LEHREN
- Die Reihenfolge einer Lösungsliste ist der Tagesplan; umsortieren hätte alle früheren Tage geändert (3.5).
- Ein neuer Import überschreibt nie, was jemand im Editor bearbeitet hat; bearbeitete Inhalte werden eine eigene
  Fassung.
- Die Vorschau braucht eigene Daten, sonst zählen Probeeinträge mit (6.3).
- Fremde Feeds kommen mit falsch kodierten Zeichen; ohne Reparatur auf dem Server zeigt jede Oberfläche Zeichensalat
  (10.1).
- Ein Service Worker ohne neue `VERSION` hält alte Dateien fest (2.3).
- Zielgerät früh festlegen (z. B. Tablet mit Touch); die Bedienung hängt daran mehr als am Code.
- Eine Startseite, die aus Vorlagen neu gebaut statt minimal ergänzt wurde, verlor einen Link (13.6).
- Text aus Web-Abrufen kam doppelt kodiert an; Text im Speicher bauen, vor dem Commit Byte für Byte prüfen, nie über
  eine Umleitung der Shell schreiben.
- Abrufe aus dem Netz scheitern manchmal still mit einer kurzen Fehlerantwort; ohne Prüfung von Größe und Inhalt wird
  sie als Inhalt weiterverwendet (13.10).
- Ein Feed wurde beim Commit abgeschnitten und eine Ausgabe fehlte; danach ganz neu im Speicher aufbauen und nach jedem
  Commit die Struktur prüfen (13.6).

### PRÜFUNG
Jeder Baustein hat einen Test; die Schritte haben Ergebnisse. Am Ende nennst du je Baustein „erprobt“, „gebaut“ oder
„offen“.

### FAIL-MODE
Wenn ein Baustein oder eine Vorgabe hier „offen“ ist, dann entscheide selbst, schreib die Entscheidung in ANNAHMEN.md
und nenne sie in der Lieferung. Wenn eine Vorgabe nicht zum Auftrag passt, dann folgst du dem Auftrag und meldest die
Stelle an die Rolle, die diese Datei führt.

### NICHT TUN
Schlüssel, Passwörter und persönliche Daten stehen nur in Secrets, im privaten Ordner oder im Browser des Nutzers ·
eine Auslieferung lädt nie Daten in den privaten Ordner außer der Zugangsdatei · nichts geht live ohne Vorschau und
Freigabe · fremde Dienste ruft nur der Server.

### LIEFERUNG
README.md, Workflow, Tests und ANNAHMEN.md; dazu je Baustein der Stand. Die Lieferung ändert nur den Ordner des
Werkzeugs und seine Workflows.

### REFERENZ
TECH-STACK.md in diesem Ordner (lokale Werkzeuge; Baustein 12 Arbeitsweise) · Zwei-Kanal-Format 1.3 · Belege je
Vorgabe in einer Liste, die nicht öffentlich ist.

### PFLEGE
Diese Datei führt eine Rolle. Jede neue Vorgabe braucht einen Beleg; die zweite Stelle der Fassung zählt neue
Vorgaben, die dritte Berichtigungen.

## BLOCK B – für Menschen

Diese Vorgabe beschreibt, wie die kleinen Web-Werkzeuge gebaut sind: eine Seite im Browser, die Daten entweder im
Browser des Nutzers oder als Dateien in einem geschützten Ordner auf dem gemieteten Webspace, Schlüssel nur in den
Geheimnissen von GitHub, und jede Änderung erst in einer Vorschau mit gelbem Schild.

Ein Programm auf GitHub baut, testet und lädt hoch; ein zweites sichert die Daten jede Nacht. Rückmeldungen aus dem
Werkzeug werden Aufgaben im Repo, und eine KI baut sie in die Vorschau – live geht erst, was ein Mensch freigibt.
