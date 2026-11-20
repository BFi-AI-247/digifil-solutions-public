# Rezept web 0.4.1

Ein Web-Werkzeug: Oberfläche im Browser, Daten im Browser oder als Dateien auf einem Webspace mit PHP, Bau, Test und
Auslieferung über GitHub.

## BLOCK A – für die bauende KI

```text
ZWECK:        Ein neues Web-Werkzeug so bauen, wie die bisherigen gebaut sind. Das Ziel ist erreicht, wenn die Schritte
              mit ihren Ergebnissen erfüllt sind und jede Abweichung in ANNAHMEN.md steht.
ABLAGE:       Dieses Rezept braucht ein GitHub-Repo mit Actions, denn Auslieferung, Sicherung und Rückmeldungen laufen
              darüber (Kapseln web-auslieferung, web-sicherung, rueckmeldungen). Ohne GitHub sind diese Kapseln offen;
              dann gilt Kapsel kern (Ablage).
GILT FÜR:     eine KI, die ein neues Web-Werkzeug baut oder ein bestehendes an dieses Rezept angleicht.
GILT NICHT:   Werkzeuge auf dem eigenen Rechner (Rezepte lokal-python, lokal-powershell) · Fachlogik und Inhalte (stehen
              im Auftrag) · Recherche im Netz: Sie ist Fähigkeit der Umgebung eines Agenten; das Werkzeug bekommt nur
              ihr Ergebnis.
VORAUSSETZUNG: ein Webspace mit PHP und Zugang per SFTP, außerhalb des Web-Verzeichnisses ein privater Ordner · ein
              GitHub-Repo mit Actions (siehe ABLAGE) · Bauumgebung mit Python ab 3.12 und Playwright (Chromium), PHP-Kommandozeile für
              lokale Tests · Server und Zugänge stehen nur in GitHub Secrets.
KAPSELN:      Pflicht: kern · web-aufbau · web-oberflaeche · web-daten · web-tests · web-auslieferung
              Wahlweise, je nach Aufgabe: web-server-php (Daten im privaten Ordner) · web-zugang · web-sicherung ·
              rueckmeldungen · web-ki · web-feeds · web-zeitplan · arbeitsweise · veroeffentlichung
              Lies jede genannte Kapsel ganz, bevor du baust.
```

### SCHRITTE (in dieser Reihenfolge; jeder Schritt hat ein prüfbares Ergebnis)

1. **Auftrag lesen.** Lies den Auftrag und dieses Rezept ganz; leg den Ordner nach Kapsel web-aufbau an; wähl die
   Kapseln.
   *Ergebnis:* README.md (Block A und B), `wissen/entscheidungen.md` mit den Festlegungen aus dem Auftrag und der
   Kapselwahl.
2. **Datenweg wählen** nach Kapsel web-daten (W1).
   *Ergebnis:* Die Wahl steht mit Grund in `wissen/entscheidungen.md`.
3. **Oberfläche, Daten, Server** nach den Kapseln web-oberflaeche, web-daten und web-server-php.
   *Ergebnis:* `bash tests/lokal.sh` startet das Werkzeug mit Testdaten; der Durchlauf im Browser (Kapsel web-tests)
   endet mit „OK“.
4. **Zugang und Auslieferung** nach den Kapseln web-zugang und web-auslieferung.
   *Ergebnis:* Ein Push auf den Vorschau-Branch zeigt das Werkzeug unter der Vorschau-Adresse mit gelbem Schild.
5. **Sicherung** nach Kapsel web-sicherung, wenn Daten im privaten Ordner liegen.
   *Ergebnis:* Der erste Lauf legt den Sicherungs-Branch an und schreibt eine Statusdatei.
6. **Rückmeldung** nach Kapsel rueckmeldungen.
   *Ergebnis:* Ein Klick auf „Rückmeldung“ in der Vorschau legt ein Issue mit dem Label des Werkzeugs an.
7. **Freigabe.** Der Mensch prüft die Vorschau und gibt frei; dann geht `main` live.
   *Ergebnis:* Der Mensch bestätigt die Live-Adresse; jede Kapsel steht als erprobt, gebaut oder offen in README oder
   `ANNAHMEN.md`.

```text
PRÜFUNG:      Jede Kapsel hat einen Test; die Schritte haben Ergebnisse.
FAIL-MODE:    nach Kapsel kern, Regel 11.
NICHT TUN:    Schlüssel, Passwörter und persönliche Daten stehen nur in Secrets, im privaten Ordner oder im Browser des
              Nutzers · eine Auslieferung lädt nie Daten in den privaten Ordner außer der Zugangsdatei · nichts geht
              live ohne Vorschau und Freigabe · fremde Dienste ruft nur der Server.
LIEFERUNG:    README.md, Workflow, Tests und ANNAHMEN.md; dazu je Kapsel der Stand. Die Lieferung ändert nur den Ordner
              des Werkzeugs und seine Workflows.
REFERENZ:     kapseln/ in diesem Ordner · Zwei-Kanal-Format 1.3 · Belege je Kapsel in einer Liste, die nicht öffentlich
              ist.
PFLEGE:       siehe README dieses Ordners.
```

## BLOCK B – für Menschen

Dieses Rezept beschreibt, wie die kleinen Web-Werkzeuge gebaut sind: eine Seite im Browser, die Daten entweder im
Browser des Nutzers oder als Dateien in einem geschützten Ordner auf dem gemieteten Webspace, Schlüssel nur in den
Geheimnissen von GitHub, und jede Änderung erst in einer Vorschau mit gelbem Schild. Ein Programm auf GitHub baut, testet
und lädt hoch; ein zweites sichert die Daten jede Nacht. Live geht erst, was ein Mensch freigibt.
