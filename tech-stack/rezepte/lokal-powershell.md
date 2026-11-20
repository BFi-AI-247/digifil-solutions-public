# Rezept lokal-powershell 0.4.1

Ein lokales Werkzeug in Windows PowerShell 5.1, ohne Python, mit Oberfläche im Browser; wahlweise mit Outlook.

## BLOCK A – Auftrag an die bauende KI

```text
ZWECK:        Du baust ein neues lokales Werkzeug in Windows PowerShell 5.1 und entscheidest die Grundlagen nicht neu;
              sie stehen in den Kapseln unten. Das Ziel ist erreicht, wenn die Schritte mit ihren Ergebnissen erfüllt
              sind und jede Abweichung in ANNAHMEN.md steht.
ABLAGE:       „Repo“ heißt in diesem Rezept die Ablage des Werkzeugs. GitHub ist empfohlen, aber nicht Pflicht;
              SharePoint, das Projektwissen der KI oder ein lokaler Ordner gehen auch. Die Wahl ist Schritt 1 (Kapsel kern).
GILT FÜR:     ein Werkzeug auf einem Windows-Rechner, auf dem nichts mitgebracht werden darf, das nicht Windows selbst
              enthält · die Prüfung, ob ein bestehendes PowerShell-Werkzeug diesem Rezept folgt.
GILT NICHT:   Werkzeuge mit Datenbank oder großen Datenmengen (Rezept lokal-python) · Web-Werkzeuge (Rezept web) · die
              Fachlogik (steht im Auftrag).
VORAUSSETZUNG: Windows 10 oder 11 mit Windows PowerShell 5.1, ohne Administratorrechte; nichts wird installiert.
              Für Kapsel outlook: klassisches Outlook mit Profil. Bauumgebung ohne Windows: statische Prüfung, die
              Ausführung prüft der Mensch.
KAPSELN:      Pflicht: kern · lokal-server · laufzeit-powershell · lokal-oberflaeche · lokal-befehle · lokal-log ·
              daten-json · lokal-updates · lokal-tests
              Wahlweise, je nach Aufgabe: outlook · sqlserver · austausch · windows-zugang · github-backend ·
              rueckmeldungen · arbeitsweise · veroeffentlichung
              Lies jede genannte Kapsel ganz, bevor du baust.
```

### SCHRITTE (in dieser Reihenfolge; jeder Schritt hat ein prüfbares Ergebnis)

1. **Ablage und Auftrag.** Leg die Ablage fest (Kapsel kern). Schreib Bedarf, gewünschtes Ergebnis und Grenzen in `AUFTRAG.md`; wähl die Kapseln und schreib die Wahl
   in `ANNAHMEN.md`. Fehlende Angaben stehen dort als offene Punkte.
   *Ergebnis:* Ablage, `AUFTRAG.md` und Kapselwahl stehen im Repo.
2. **Zielumgebung und riskantester Teil.** Ein kleiner Vortest prüft Fassung, Edition, 64 Bit und Sprachmodus
   (Kapsel laufzeit-powershell), den Start des Servers ohne Administratorrechte und – mit Kapsel outlook – die
   Erreichbarkeit von Outlook. Das ist der erste Sperrpunkt.
   *Ergebnis:* Der Mensch meldet die Ausgabe des Vortests vom Zielrechner.
3. **Ordner und Port** nach den Kapseln lokal-server und laufzeit-powershell.
   *Ergebnis:* Der Port steht in `PORTS.md` des Repos und als Standard in `App/Version.psd1` oder der Vorlage der
   Einstellung.
4. **Start, Server und Schutz** nach Kapsel lokal-server, zuerst mit erfundenen Daten.
   *Ergebnis:* Tests für fremden Host, fremden `Origin`, falsches Token, OPTIONS, falschen Content-Type, zu großen Körper
   und 409 beim Beenden während eines Auftrags sind beschrieben und, wo Windows da ist, grün.
5. **Oberfläche, Daten und Aufträge** nach den Kapseln lokal-oberflaeche, daten-json, lokal-befehle und lokal-log; dann
   die gewählten Kapseln (z. B. outlook).
   *Ergebnis:* Ein Ablauf vom Start bis zum Ergebnis läuft; ein erfundenes Token steht in keiner Ausgabedatei.
6. **Paket und Update** nach Kapsel lokal-updates.
   *Ergebnis:* `Tools/Erzeuge-Manifest.ps1` meldet Gleichstand; eine Installation aus dem ZIP in einen leeren Ordner
   startet.
7. **Pflichtdateien und Abnahme** nach den Kapseln kern, laufzeit-powershell und lokal-tests.
   *Ergebnis:* `PRUEFBERICHT.md` nennt je Fall Soll, Ist und Umgebung; Block A der README ist ohne Block B ausführbar.

### WEITERE FÄHIGKEITEN (noch ohne Kapsel)
- Excel-Dateien lesen: nur mit einer mitgelieferten, geprüften Bibliothek (Version, Lizenz, Grenzen in
  `ABHAENGIGKEITEN.md`), nie aus dem Netz, nie mit Makros.
- Dateien auswählen: über die Dateiauswahl des Browsers; ein Pfad auf dem Rechner kommt so nicht mit. Eine Auswahl auf
  dem Server ist eine eigene Fähigkeit mit Pfadprüfung.
- PDF und Texterkennung: keine; braucht ein Werkzeug sie, dann ist das eine neue Kapsel.
- Neue Fähigkeiten werden eine Kapsel nach der README dieses Ordners (Pflege).

```text
PRÜFUNG:      Die Ergebnisse der Schritte 1 bis 7 gelten zusammen. Ohne Windows: statische Ergebnisse und
              Prüfschritte, keine gemeldete Ausführung.
FAIL-MODE:    nach Kapsel kern, Regel 11.
NICHT TUN:    Firmendaten, echte Empfänger und Postfächer, Geheimnisse in Repo, Beispielen oder Log · Module zur
              Laufzeit nachladen · Prozesse nach Namen beenden · Mails ohne Auftrag senden · still von einer Kapsel
              abweichen.
LIEFERUNG:    nach Kapsel kern, Regel 12, dazu Port und ZIP mit Manifest.
REFERENZ:     kapseln/ in diesem Ordner · Belege je Kapsel in einer Liste, die nicht öffentlich ist.
PFLEGE:       siehe README dieses Ordners.
```

## BLOCK B – für Menschen

Dieses Rezept ist für Rechner gedacht, auf die man nichts mitbringen darf: PowerShell ist auf jedem Windows schon da.
Das Werkzeug läuft wie die Python-Werkzeuge im Browser und nach demselben Vertrag, kann aber zusätzlich Mail-Entwürfe in
Outlook anlegen. Senden tust du immer selbst.
