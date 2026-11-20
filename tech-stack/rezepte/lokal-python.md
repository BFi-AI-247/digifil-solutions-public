# Rezept lokal-python 0.4.1

Ein lokales Werkzeug mit Python 3.14 im Werkzeugordner und Oberfläche im Browser.

## BLOCK A – Auftrag an die bauende KI

```text
ZWECK:        Du baust ein neues lokales Werkzeug in Python und entscheidest die Grundlagen nicht neu; sie stehen in den
              Kapseln unten. Das Ziel ist erreicht, wenn die Schritte mit ihren Ergebnissen erfüllt sind und jede
              Abweichung in ANNAHMEN.md steht.
ABLAGE:       „Repo“ heißt in diesem Rezept die Ablage des Werkzeugs. GitHub ist empfohlen, aber nicht Pflicht;
              SharePoint, das Projektwissen der KI oder ein lokaler Ordner gehen auch. Die Wahl ist Schritt 1 (Kapsel kern).
GILT FÜR:     ein Werkzeug auf einem Windows-Rechner mit Oberfläche im Browser · die Prüfung, ob ein bestehendes Werkzeug
              diesem Rezept folgt.
GILT NICHT:   Web-Werkzeuge auf einem Webspace (Rezept web) · Werkzeuge ohne Python (Rezept lokal-powershell) · die
              Fachlogik (steht im Auftrag).
VORAUSSETZUNG: Windows 11 ohne Administratorrechte; auf dem Rechner wird nichts installiert; ein Benutzer je Rechner;
              andere Anwender übernehmen das Werkzeug später. Bauumgebung: Python 3.13 oder 3.14 mit pytest, Node.js,
              Chrome oder Chromium, git.
KAPSELN:      Pflicht: kern · lokal-server · laufzeit-python · lokal-oberflaeche · lokal-befehle · lokal-log ·
              lokal-updates · lokal-tests
              Wahlweise, je nach Aufgabe: daten-sqlite · daten-json · sqlserver · austausch · windows-zugang ·
              github-backend · rueckmeldungen · arbeitsweise · veroeffentlichung
              Lies jede genannte Kapsel ganz, bevor du baust.
```

### SCHRITTE (in dieser Reihenfolge; jeder Schritt hat ein prüfbares Ergebnis)

1. **Ablage und Auftrag.** Leg die Ablage fest (Kapsel kern). Lass Absicht, Auftrag und Grenzen als Datei ins Repo
   schreiben; mit Kapsel arbeitsweise zusätzlich eine
   Rolle mit Kennung. Wähl die Kapseln aus der Liste oben und schreib die Wahl in `ANNAHMEN.md`.
   *Ergebnis:* Ablage, Auftrag und Kapselwahl stehen im Repo.
2. **Ordner und Port.** Lege den Ordner nach den Kapseln lokal-server und laufzeit-python an; wähl den Port.
   *Ergebnis:* Der Port steht in `PORTS.md` des Repos und als Standard im Code.
3. **Laufzeit und Start** nach Kapsel laufzeit-python. Das ist der erste Sperrpunkt: Der Mensch legt Archiv und
   Startdateien von Hand in einen leeren Installationsordner; ein kleinstes Paket gibt nur die Version aus.
   *Ergebnis:* Der Mensch meldet vom Zielrechner die Ausgabe des Starttests ohne Fehler.
4. **Server** nach den Kapseln lokal-server und lokal-befehle.
   *Ergebnis:* Tests für fremden Host, fremden `Origin`, falsches Sitzungstoken, OPTIONS, falschen Content-Type und 409
   beim Beenden während eines Auftrags sind grün.
5. **Oberfläche** nach Kapsel lokal-oberflaeche.
   *Ergebnis:* Ein Klickablauf im Headless-Chrome läuft ohne Fehler in der Konsole.
6. **Daten und Log** nach den gewählten Daten-Kapseln und Kapsel lokal-log.
   *Ergebnis:* Ein Test schreibt ein erfundenes Token ins Log, und die Logdatei enthält es nicht.
7. **Verteilung und Zugang** nach Kapsel lokal-updates; Kapsel windows-zugang nur, wenn das Werkzeug selbst einen fremden
   Dienst anspricht.
   *Ergebnis:* Die Prüfung des Manifests meldet Gleichstand; eine Installation nur aus dem Manifest startet in einem
   leeren Ordner.
8. **Probe am Zielrechner.** Der Mensch installiert, startet, stoppt und aktualisiert.
   *Ergebnis:* Der Mensch bestätigt Start, Stopp und Update; jede Kapsel steht als erprobt, gebaut oder offen in README
   oder `ANNAHMEN.md`.
9. **Pflichtdateien** nach Kapsel kern und laufzeit-python; mit Kapsel arbeitsweise ein Review durch eine zweite KI.
   *Ergebnis:* README nach Zwei-Kanal-Format; der Prüfbericht nennt je Fall Soll, Ist und Umgebung.

```text
PRÜFUNG:      Die Ergebnisse der Schritte 1 bis 9 gelten zusammen.
FAIL-MODE:    nach Kapsel kern, Regel 11.
NICHT TUN:    Firmendaten, Geheimnisse und persönliche Daten in Repo, Issues, Protokollen oder Beispielen · zur Laufzeit
              installieren oder aus fremden Quellen laden · still von einer Kapsel abweichen.
LIEFERUNG:    nach Kapsel kern, Regel 12, dazu der Port.
REFERENZ:     kapseln/ in diesem Ordner · Belege je Kapsel in einer Liste, die nicht öffentlich ist.
PFLEGE:       siehe README dieses Ordners.
```

## BLOCK B – für Menschen

Dieses Rezept ist der bewährte Weg für kleine Werkzeuge auf dem eigenen Windows-Rechner: Python kommt im Werkzeugordner
mit, ein kleiner Webserver antwortet nur dem eigenen Rechner, die Oberfläche läuft im Browser. Gib dem Bau-Chat dieses
Rezept mit; er liest die Kapseln, die es nennt. Prüfen musst du nur die Proben am eigenen Rechner: Start, Stopp und
Aktualisierung.
