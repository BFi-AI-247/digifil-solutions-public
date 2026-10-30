# Beispiel: eine Anleitung im Zwei-Kanal-Format 1.1

<!-- Erfundenes Beispiel zu readme-vorlage.md. Das Werkzeug „Termin-Erinnerer“ gibt es nicht; Dateinamen und Befehle
     sind ausgedacht, aber so konkret, wie eine echte Anleitung sie nennen müsste. -->

---

# Termin-Erinnerer 1.2

## BLOCK A – Auftrag an die einrichtende KI

```text
ZWECK:        Der Termin-Erinnerer schickt jeden Morgen zur eingestellten Uhrzeit (Vorgabe 7 Uhr) eine E-Mail mit den Terminen des Tages aus einer
              Kalenderdatei. Eingerichtet ist er, wenn der Testlauf eine E-Mail an die Testadresse erzeugt und das
              Protokoll eine Zeile mit „ok“ enthält.
GILT FÜR:     eine KI, die den Erinnerer für einen Verein oder eine Familie auf einem Linux-Rechner einrichtet.
GILT NICHT:   das Pflegen der Termine selbst (das macht der Mensch in der Kalenderdatei) · den Versand über andere Wege
              als E-Mail (nicht vorgesehen).
VORAUSSETZUNG: Python 3.10 oder neuer · ein E-Mail-Konto mit SMTP-Zugang (Server, Port, Benutzer, Passwort) · Schreibrecht
              im Ordner, in dem der Erinnerer liegt · cron oder ein vergleichbarer Zeitplaner.
DATEIEN:      erinnerer.py (liest die Kalenderdatei, baut die E-Mail, verschickt sie) · einstellungen.json (Empfänger,
              Absender, Testadresse, SMTP-Zugang, Uhrzeit, Zeitzone; Vorlage einstellungen.example.json) · termine.csv (die Termine, eine Zeile je
              Termin: Datum;Uhrzeit;Titel) · protokoll.log (eine Zeile je Lauf, wird angelegt) · test_erinnerer.py (Testlauf
              mit Testdaten, verschickt nur an die Testadresse aus einstellungen.json).
BEGRIFFE:     Termin des Tages = jede Zeile in termine.csv, deren Datum dem Kalendertag des Laufs in der Zeitzone aus
              einstellungen.json entspricht. Testadresse = Feld "test_an" in einstellungen.json; der Testlauf schickt nur dorthin.
VERHALTEN:    Ohne Termine am Tag wird keine E-Mail verschickt, aber eine Protokollzeile geschrieben („ok, 0 Termine“).
              Eine fehlerhafte Zeile in termine.csv (falsches Datumsformat) wird übersprungen und im Protokoll genannt;
              der Lauf bricht deswegen nicht ab. Das Passwort steht nur in einstellungen.json, nie im Protokoll.
```

### SCHRITTE (in dieser Reihenfolge; jeder Schritt hat ein prüfbares Ergebnis)

1. **Einstellungen anlegen.** `einstellungen.example.json` nach `einstellungen.json` kopieren und die Felder füllen:

   | Platzhalter | einsetzen |
   |---|---|
   | `"an"` | die Empfängeradresse aus dem Auftrag; fehlt sie: die Testadresse (in der Lieferung als offen nennen) |
   | `"von"` | die Absenderadresse des E-Mail-Kontos |
   | `"test_an"` | eine Adresse, die der Auftraggeber liest |
   | `"smtp"` | Server, Port, Benutzer, Passwort aus dem Auftrag; fehlt etwas: Schritt abbrechen, als offen melden |
   | `"uhrzeit"` | aus dem Auftrag; sonst `"07:00"` (in der Lieferung als offen nennen) |
   | `"zeitzone"` | aus dem Auftrag; sonst `"Europe/Berlin"` (in der Lieferung als offen nennen) |

   *Ergebnis:* `python3 -c "import json; json.load(open('einstellungen.json'))"` gibt keinen Fehler aus.
2. **Termine prüfen.** `termine.csv` muss je Zeile `JJJJ-MM-TT;HH:MM;Titel` enthalten; die erste Zeile ist die Überschrift.
   Liegt keine Datei vor: eine mit der Überschrift und einem Testtermin für heute anlegen.
   *Ergebnis:* `head -2 termine.csv` zeigt die Überschrift und eine gültige Zeile.
3. **Testlauf.** `python3 test_erinnerer.py` ausführen.
   *Ergebnis:* Ausgabe endet mit „TEST OK“; an der Testadresse liegt eine E-Mail mit dem Testtermin; `tail -1 protokoll.log`
   beginnt mit dem heutigen Datum und enthält „ok“.
4. **Zeitplan setzen – erst nach Bestätigung.** Erst wenn der Auftraggeber die Test-E-Mail aus Schritt 3 gesehen und „passt“
   gesagt hat; bis dahin diesen Schritt nicht ausführen und in der Lieferung als „wartet auf Bestätigung“ nennen. Dann in cron
   eine Zeile anlegen: `<Minute> <Stunde> * * * cd <Ordner des Erinnerers> && python3 erinnerer.py`, Minute und Stunde aus dem
   Feld `"uhrzeit"`, den Ordner durch den absoluten Pfad ersetzen.
   *Ergebnis:* `crontab -l` zeigt die Zeile mit Uhrzeit und Pfad.

```text
PRÜFUNG:      Die Ergebnisse zusammen: Schritt 3 („TEST OK“, E-Mail angekommen, Protokollzeile mit „ok“) und – nach der
              Bestätigung – Schritt 4 (Zeile in crontab -l).
FAIL-MODE:    Ein Schritt geht nicht: nicht improvisieren, abbrechen und melden, welcher Schritt mit welchem Befund scheiterte.
              Verschickt der Testlauf nichts: SMTP-Angaben als unsicher melden, kein anderes Konto probieren.
              Fehlt nur eine Angabe: Vorgabe aus Schritt 1 nehmen und in der Lieferung als offen nennen.
NICHT TUN:    das Passwort in eine andere Datei oder in die Lieferung schreiben · termine.csv inhaltlich ändern (außer der
              Testzeile aus Schritt 2) · eine andere Uhrzeit als die aus Schritt 1 setzen · an echte Empfänger schicken,
              bevor der Auftraggeber den Testlauf gesehen hat (deshalb Schritt 4 erst nach seiner Bestätigung).
LIEFERUNG:    einstellungen.json ohne Passwort-Zeile · Ausgabe von Schritt 3 · die cron-Zeile · offene Punkte ·
              jede Stelle, an der diese Anleitung nicht reichte (mit Zitat).
```

---

## BLOCK B – für Menschen

Ein Verein hatte einen Kalender auf der Website, aber die Vorstandsmitglieder schauten nicht jeden Tag hinein – und so
stand beim Sommerfest niemand pünktlich am Grill. Der Termin-Erinnerer löst das auf die einfachste Art: Jeden Morgen kommt
eine E-Mail mit dem, was heute ansteht. Gibt es nichts, kommt auch keine E-Mail.

Die Termine pflegst du in einer einfachen Tabelle, eine Zeile je Termin. Das Programm liest sie, schreibt die E-Mail und
hält in einem Protokoll fest, dass es gelaufen ist. Eine fehlerhafte Zeile bringt nicht alles zum Stehen; sie wird
übersprungen und im Protokoll erwähnt, damit du sie findest.

## Was du im Alltag tust

Neue Termine trägst du in die Tabelle ein, alte lässt du einfach stehen. Kommt an einem Tag mit Terminen keine E-Mail,
schau ins Protokoll: Dort steht, ob das Programm gelaufen ist und was es gefunden hat. Mehr ist nicht zu tun.

---

## Was dieses Beispiel zeigt

- Jeder Schritt nennt Datei, Stelle und Wert und endet mit einem prüfbaren Ergebnis; Platzhalter haben eine Vorgabe und
  den Hinweis „in der Lieferung als offen nennen“.
- VERHALTEN beschreibt, was das Werkzeug heute tut – eine KI, die später Fragen dazu beantwortet, muss den Code nicht lesen.
- Block B kommt ohne Dateinamen, Befehle und Feldnamen aus und sagt trotzdem, wozu das Ganze gut ist und was der Mensch tut.
- Ein Blindtest dieser Anleitung würde eine frische KI nur mit Block A und dem Auftrag „richte den Erinnerer für einen
  Chor ein“ losschicken und ihre Liste der Ratestellen auswerten.
