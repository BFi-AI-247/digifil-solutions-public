# Kapsel lokal-server 0.4.0

Der kleine Webserver eines lokalen Werkzeugs: Port, Ordner, eine Instanz, Schutz, Status, Beenden. Gleich für jede
Laufzeit; wie es in Python oder PowerShell gebaut wird, sagt die Laufzeit-Kapsel.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt den Vertrag des lokalen Servers, den jedes lokale Werkzeug und jedes Steuerpult kennt.
GILT FÜR:     Rezepte lokal-python und lokal-powershell.
BRAUCHT:      Kapseln kern · laufzeit-python oder laufzeit-powershell
BEGRIFFE:     Sitzungstoken = Schlüssel der Oberfläche für POST-Anfragen, bei jedem Start neu; nie ein Zugangsschlüssel.
              Auftrag = eine längere Verarbeitung im Hintergrund, z. B. ein Import. Steuerpult = ein Werkzeug, das
              andere Werkzeuge anzeigt, startet, stoppt und aktualisiert.
```

### REGELN
- 1 Port: Jedes Werkzeug hat einen festen Port. Reihenfolge: Schalter beim Start, sonst die Einstellung, sonst der
  Standard im Code. Empfehlung (unbelegt): Alle Werkzeuge nehmen Ports aus einem eigenen Bereich, z. B. 8700–8799, jeder
  Port nur einmal; `PORTS.md` in der Wurzel des Repos führt eine Zeile je Werkzeug und Port, fehlt sie, dann leg sie
  an. Häufig belegte Ports wie 8000 und 8080 meidest du.
- 2 Der Server lauscht nur auf 127.0.0.1, nie auf `+`, `*` oder einem Hostnamen von außen. Der Browser öffnet eine
  Adresse, die die Host-Prüfung (Regel 7) annimmt; welche, sagt die Laufzeit-Kapsel.
- 3 Ordner: Den Werkzeugordner ermittelt das Werkzeug aus dem Ort seiner Startdatei, nie aus dem Arbeitsverzeichnis.
  Darin `Config/` (Einstellungen in `Config/<werkzeug>.config.json`, UTF-8 ohne BOM; fehlt sie, dann legt das Werkzeug
  sie aus einer Vorlage an; ein Update legt nur Fehlendes an) · `Data/` (Daten; kein Update fasst sie an) · `Logs/` ·
  `Backup/` (vom Update) · `Web/` · `Tools/` · `tests/`. `Data/` und `Logs/` legt das Werkzeug beim Start an; im Repo
  stehen dort höchstens leere Platzhalter. Netzlaufwerke und synchronisierte Ordner sind kein Ort für den aktiven
  Datenbestand.
- 4 Zweiter Start: Prüf mit einer Verbindungsprobe auf 127.0.0.1, ob der Port belegt ist, dann mit einer zeitlich
  begrenzten Abfrage von `GET /api/status`. Antwortet dort das eigene Werkzeug (`produkt`) mit gleichem `build`, dann
  öffne nur den Browser; Rückgabe 0. Antwortet etwas anderes oder ist die Identität unklar, dann melde „Port belegt“ mit
  dem Vorschlag, einen anderen Port zu nehmen; Rückgabe 1. Ein Startfehler heißt nicht „läuft schon“.
- 5 Eine Instanz: Ein Werkzeug, das Daten schreibt, hält während der ganzen schreibenden Laufzeit eine exklusive Sperre
  des Betriebssystems auf `Data/instance.lock` (die Datei ist ohne Freigabe für andere geöffnet). Daneben steht
  `Data/instance.json` mit `pid`, Startzeit des Prozesses, `port`, `version`, `build` und bei einem Lauf ohne Oberfläche
  `kommandozeile: true` mit Port 0; nie ein Token. Es entscheidet die gehaltene Sperre, nicht eine Datei oder eine PID.
  Ist die Sperre nicht zu bekommen, dann startet nie eine zweite schreibende Instanz: Ein Lauf ohne Oberfläche wird
  gemeldet („arbeitet gerade ohne Oberfläche“, Rückgabe 2), sonst gilt Regel 4 oder 6. Nach einem Absturz ersetzt das
  Werkzeug `instance.json` unter der neu erworbenen Sperre und schreibt eine Warnung ins Log.
- 6 Ablösen einer anderen Fassung (anderer `build`): nur über ihre API (`sitzungstoken` aus `/api/status`, dann
  `POST /api/shutdown`), auf ihr Ende warten, dann starten. Läuft dort ein Auftrag (409), dann löst du nicht ab, sondern
  meldest es; Rückgabe 2. Beende nie Prozesse nach Name oder ähnlicher Befehlszeile. Lässt sich die Identität nicht
  sicher prüfen, dann melde den Konflikt und lass die laufende Instanz bestehen.
- 7 Prüf jede Anfrage vor dem Routing, in dieser Reihenfolge: Host-Kopf ist `localhost`, `127.0.0.1` oder `[::1]` mit
  dem eigenen Port, sonst 400 · Gegenstelle ist Loopback (eine IPv4-Adresse in IPv6 vorher auflösen; `X-Forwarded-*`
  zählt nicht), sonst 403 · Methode ist GET oder POST, sonst 405; OPTIONS bekommt keine CORS-Freigabe · ein vorhandener
  `Origin` ist genau die eigene Adresse, sonst 403 (Aufrufe ohne `Origin` sind mit Token erlaubt) · bei POST trägt der
  Kopf `X-<Name>-Token` das Sitzungstoken, nach Prüfung von Format und Länge als Bytes mit gleichbleibender Laufzeit
  verglichen, sonst 403 · bei POST beginnt `Content-Type` mit `application/json` (ein Zusatz wie `; charset=utf-8` ist
  erlaubt), sonst 415. Kein Zeichen in einem Kopf darf eine unbehandelte Ausnahme auslösen.
- 8 Sitzungstoken: bei jedem Start neu aus einem kryptografischen Zufallsgenerator, mindestens 16 Byte (Empfehlung 32);
  nie eine Zufallszahl oder GUID. Es lebt nur im Speicher. Die Oberfläche bekommt es beim Ausliefern von `index.html`
  (Platzhalter `{{SITZUNGSTOKEN}}`) oder über `GET /api/status`. `/api/status` darf es nennen, denn eine fremde
  Webseite kann die Antwort nicht lesen, solange Regel 7 greift; ein lokales Programm braucht es zum Beenden. Es steht
  in keiner Datei, keinem Log, keiner Befehlszeile und keinem Chat; geriet es in einen Chat, dann starte das Werkzeug
  neu. Es schützt vor Webseiten, nicht vor Programmen im selben Benutzerkonto.
- 9 Setz auf jede eigene Antwort, auch auf Fehler: `Cache-Control: no-store` · `X-Content-Type-Options: nosniff` ·
  `X-Frame-Options: DENY` · `Referrer-Policy: no-referrer` · `Content-Security-Policy: default-src 'self'; script-src
  'self'; style-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none';
  form-action 'none'`. Eine Lockerung steht konkret in `ANNAHMEN.md`. Fehler, die das System selbst vor dem Werkzeug
  erzeugt, trägt der Prüfbericht getrennt ein.
- 10 Statische Dateien nur aus `Web/`: erlaubte Zeichen, kein `%`, kein `\`, kein Nullbyte, keine Segmente `.` oder
  `..`, keine versteckten Dateien und keine Verknüpfungen, nur feste Endungen; der aufgelöste Pfad liegt unter `Web/`
  (oder eine beim Start erzeugte Liste erlaubter Pfade). `Config/`, `Data/`, `Logs/` und Skripte sind nie erreichbar;
  ein Export geht über eine eigene Route.
- 11 Größen: Jede Route hat eine feste Grenze für den Körper (Standard 16 KiB für Steuerbefehle, 10 MiB für JSON-Importe;
  andere Werte in `ANNAHMEN.md`); gezählt werden die gelesenen Bytes, nicht nur `Content-Length`. Zu groß: 413;
  ungültiges JSON oder Schema: 400. UTF-8 wird streng gelesen, Verschachtelung und Zahl der Datensätze sind begrenzt;
  keine Eingabe wird als Code ausgeführt.
- 12 Status: `GET /api/status` nennt `produkt`, `version`, `build`, `pid`, `port`, `state_key`, die laufenden Aufträge und
  `sitzungstoken`. `state_key` ist `ready`, `processing` (ein Auftrag läuft), `stopping` oder `error`. Der Status liest
  nur vorhandenen Zustand; er startet keine lange Prüfung und kein fremdes Programm. Eine lange Aktion antwortet mit 202
  und einer Auftragskennung; ihren Zustand nennt eine eigene Route.
- 13 `build` ist ein Fingerabdruck: SHA-256, die ersten 12 Zeichen, über die Version und die Programmdateien (sortiert,
  relativer Pfad und Inhalt), ohne Daten, Logs, Einstellungen und Zwischendateien.
- 14 Beenden: `POST /api/shutdown`, geschützt wie jede POST-Anfrage. Läuft kein Auftrag, dann antwortet es `{"ok":true}`
  und der Server endet nach rund 0,3 s. Läuft ein Auftrag, dann antwortet es mit 409. Der Mensch kann dann einen
  kontrollierten Stopp anfordern: keine neuen Aufträge, Warten bis zur nächsten sicheren Grenze, dann Ende
  (`state_key` `stopping`). Eine Notabschaltung ist ein eigener, klar benannter Vorgang. Ohne Steuerpult beendet der
  Mensch über einen Knopf „Beenden“ oder den Schalter `--stop`; beide gehen über `POST /api/shutdown` und fragen bei 409
  nach.
- 15 Nach normalem Ende sind die Daten geschrieben, das Log abgeschlossen, die Verbindungen zu und die Sperre frei. Ein
  Fehler beim Start ohne Konsole zeigt einen Hinweis ohne Geheimnisse; geplante Läufe zeigen nie ein Fenster, sie
  schreiben ins Log.
- 16 Rückgabecodes: 0 = in Ordnung · 1 = Fehler · 2 = gerade blockiert (ein Auftrag läuft, eine andere Instanz
  arbeitet) oder eine Entscheidung des Menschen ist nötig. Andere Codes stehen in `ANNAHMEN.md`.
- 17 Steuerpult: Jedes Werkzeug bringt eine Startdatei ohne Konsole, `/api/status` und `/api/shutdown` mit. Ein
  Steuerpult liest vor dem Beenden `/api/status`; läuft ein Auftrag, dann fragt es den Menschen, und ein Update startet
  erst nach dem Auftrag. Eine Antwort 409 behandelt es als „noch nicht“, nicht als Fehler.
- Grund: Zwei Instanzen schreiben gegeneinander; eine fremde Webseite im selben Browser kann über DNS-Rebinding
  Anfragen an localhost schicken – Host-Prüfung, Origin, Sitzungstoken und Content-Type schließen das aus; ein
  Steuerpult braucht feste Wege für Start, Zustand und Stopp.
- Fallen: Windows vergibt Prozessnummern neu; eine Datei mit fremder lebender PID darf den Start nicht blockieren – die
  gehaltene Sperre entscheidet. Eine Bind-Probe meldet einen eben beendeten Server noch Sekunden als belegt. Ohne
  Host-Prüfung nimmt ein Server jeden Host an. Ein Vergleich des Tokens als Text wirft bei Nicht-ASCII einen Fehler;
  die Antwort wird 500 und verliert die Sicherheitsköpfe. Ein Stopp mitten im Import hinterlässt Daten bis zur letzten
  sicheren Grenze.
- Test: zweiter Start bei laufendem Werkzeug · fremder Prozess auf dem Port · Absturz und Neustart · rohe Anfragen mit
  fremdem Host, fremdem `Origin`, Token mit Umlaut, OPTIONS, falschem Content-Type, zu großem und stückweise
  gesendetem Körper und Pfaden mit `%2e%2e` · Status und `POST /api/shutdown` während eines nachgestellten Auftrags.
- Stand: Python: Port, Ablösung, Start, Stopp und Host-Prüfung erprobt; Verbindungsprobe, übrige Prüfungen, `processing`
  und Sicherheitsköpfe (ohne `object-src 'none'`) gebaut; Sperre des Betriebssystems, `Origin`, 409, kontrollierter
  Stopp, 413, 202 und Rückgabecode 2 offen – bis dahin gilt die erprobte Sperrdatei aus Kapsel laufzeit-python.
  PowerShell: Server, Sperre und Rückgabecode 2 haben Vorbilder (Belege); der Vertrag als Ganzes ist offen.

### WAHL UND LEHREN
- W1 Schutz der POST-Anfragen: Sitzungstoken je Start (Empfehlung) oder ein fester Kopf wie `X-<Name>: 1`, der nur über
  die Vorabfrage des Browsers schützt.
- W2 Sicherheitsköpfe: voller Satz auf jeder Antwort (Regel 9, Empfehlung) oder nur `no-store` und `nosniff` auf
  statischen Dateien.
- W3 Zweiter Start: Verbindungsprobe (Empfehlung) oder Bind-Probe. Die Sperre ist keine Wahl (Regel 5).
- W4 Feldname des Sitzungstokens in `/api/status`: `sitzungstoken` (Empfehlung) oder `token`.
- Lehre: Der Server prüfte den Host-Kopf nicht; eine fremde Webseite hätte das Sitzungstoken lesen und Befehle auslösen
  können (Regel 7).
- Lehre: Das Sitzungstoken wurde als Text verglichen; ein Umlaut ergab 500 ohne Sicherheitsköpfe (Regeln 7, 9).
- Lehre: Eine Sperrdatei mit wiederverwendeter Prozessnummer blockierte den Start (Regel 5).
- Lehre: Eine Bind-Probe meldete einen eben beendeten Server noch über 10 s als belegt (Regel 4).
- Lehre: Ein Stopp von außen hätte einen 33 Minuten langen Import mittendrin abgebrochen (Regel 14).
- Lehre: Ein Sitzungstoken geriet in einen Chat; das Werkzeug musste neu starten (Regel 8).

## BLOCK B – für Menschen

Jedes lokale Werkzeug hat einen eigenen kleinen Webserver, der nur auf deinem Rechner antwortet. Er läuft nur einmal,
nimmt nur Anfragen der eigenen Oberfläche an und lässt sich nicht mitten in einer Verarbeitung beenden, ohne dass du
gefragt wirst.
