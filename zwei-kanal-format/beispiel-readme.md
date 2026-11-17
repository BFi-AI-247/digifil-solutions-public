# Beispiel: eine Anleitung im Zwei-Kanal-Format

<!-- Erfundenes Beispiel zu readme-vorlage.md. Das Werkzeug „Termin-Erinnerer“ gibt es nicht; Dateinamen und Befehle
     sind ausgedacht, aber so konkret, wie eine echte Anleitung sie nennen müsste. -->

---

# Termin-Erinnerer 1.2

## BLOCK A – Auftrag an die einrichtende KI

```text
ZWECK:        Der Termin-Erinnerer schickt jeden Morgen zur eingestellten Uhrzeit eine E-Mail mit den Terminen des Tages
              aus einer Kalenderdatei. Er ist eingerichtet, wenn der Testlauf eine E-Mail an die Testadresse erzeugt
              und das Protokoll eine Zeile mit „ok“ enthält.
GILT FÜR:     Eine KI richtet den Erinnerer für einen Verein oder eine Familie auf einem Linux-Rechner ein.
GILT NICHT:   Die Termine pflegt der Mensch selbst in der Kalenderdatei. Einen anderen Versandweg als E-Mail hat der
              Erinnerer nicht.
VORAUSSETZUNG: Python 3.10 oder neuer · ein E-Mail-Konto mit SMTP-Zugang (Server, Port, Benutzer, Passwort) · Schreibrecht
              im Ordner, in dem der Erinnerer liegt · cron oder ein vergleichbarer Zeitplaner.
DATEIEN:      erinnerer.py (liest die Kalenderdatei, baut die E-Mail, verschickt sie) · einstellungen.json (Adresse,
              Absender, Testadresse, SMTP-Zugang, Uhrzeit, Zeitzone; Vorlage einstellungen.example.json) · termine.csv
              (die Termine, eine Zeile je Termin: Datum;Uhrzeit;Titel) · protokoll.log (eine Zeile je Lauf, wird
              angelegt) · test_erinnerer.py (Testlauf mit Testdaten, verschickt nur an die Testadresse).
BEGRIFFE:     Termin des Tages = jede Zeile in termine.csv, deren Datum dem Kalendertag des Laufs in der Zeitzone aus
              einstellungen.json entspricht. Testadresse = Feld "test_an" in einstellungen.json.
VERHALTEN:    Ohne Termine am Tag wird keine E-Mail verschickt, aber eine Protokollzeile geschrieben („ok, 0 Termine“).
              Eine fehlerhafte Zeile in termine.csv (falsches Datumsformat) wird übersprungen und im Protokoll genannt;
              der Lauf bricht deswegen nicht ab. Das Passwort steht nur in einstellungen.json, nie im Protokoll.
```

### SCHRITTE (in dieser Reihenfolge; jeder Schritt hat ein prüfbares Ergebnis)

1. **Einstellungen anlegen.** Kopiere `einstellungen.example.json` nach `einstellungen.json` und fülle die Felder:

   | Platzhalter | einsetzen |
   |---|---|
   | `"an"` | die Adresse aus dem Auftrag, an die die E-Mail geht. Wenn sie fehlt, dann lass das Feld leer und nenne es in der Lieferung als offen; Schritt 4 wartet. |
   | `"von"` | die Absenderadresse des E-Mail-Kontos |
   | `"test_an"` | eine Adresse, die der Auftraggeber liest. Wenn sie fehlt, dann brich den Schritt ab und melde sie als offen. |
   | `"smtp"` | Server, Port, Benutzer und Passwort aus dem Auftrag. Wenn etwas fehlt, dann brich den Schritt ab und melde es als offen. |
   | `"uhrzeit"` | die Uhrzeit aus dem Auftrag. Wenn der Auftrag keine nennt, dann gilt die Vorgabe `"07:00"`; nenne sie in der Lieferung als offen. |
   | `"zeitzone"` | die Zeitzone aus dem Auftrag. Wenn der Auftrag keine nennt, dann gilt die Vorgabe `"Europe/Berlin"`; nenne sie in der Lieferung als offen. |

   *Ergebnis:* `python3 -c "import json; json.load(open('einstellungen.json'))"` gibt keinen Fehler aus.
2. **Termine prüfen.** `termine.csv` enthält je Zeile `JJJJ-MM-TT;HH:MM;Titel`; die erste Zeile ist die Überschrift.
   Wenn die Datei fehlt, dann lege eine mit der Überschrift und einem Testtermin für heute an.
   *Ergebnis:* `head -2 termine.csv` zeigt die Überschrift und eine gültige Zeile.
3. **Testlauf.** Führe `python3 test_erinnerer.py` aus.
   *Ergebnis:* Die Ausgabe endet mit „TEST OK“; an der Testadresse liegt eine E-Mail mit dem Testtermin;
   `tail -1 protokoll.log` beginnt mit dem heutigen Datum und enthält „ok“.
4. **Zeitplan setzen.** Wenn der Auftraggeber die Test-E-Mail aus Schritt 3 gesehen und „passt“ gesagt hat und das Feld
   `"an"` gefüllt ist, dann lege in cron eine Zeile an:
   `<Minute> <Stunde> * * * cd <Ordner des Erinnerers> && python3 erinnerer.py`. Nimm Minute und Stunde aus dem Feld
   `"uhrzeit"` und ersetze den Ordner durch den absoluten Pfad. Bis dahin nennst du den Schritt in der Lieferung als
   „wartet auf Bestätigung“.
   *Ergebnis:* `crontab -l` zeigt die Zeile mit Uhrzeit und Pfad.

```text
PRÜFUNG:      Die Ergebnisse von Schritt 3 und, nach der Bestätigung, von Schritt 4 gelten zusammen.
FAIL-MODE:    Wenn ein Schritt nicht geht, dann brich ab und melde, welcher Schritt mit welchem Befund scheiterte.
              Wenn der Testlauf nichts verschickt, dann melde die SMTP-Angaben als unsicher und bleib bei diesem Konto.
              Wenn nur eine Angabe fehlt, dann gilt die Zeile des Felds in Schritt 1.
NICHT TUN:    Das Passwort steht nur in einstellungen.json; in eine andere Datei oder in die Lieferung schreibst du es
              nicht. · In termine.csv legst du höchstens die Testzeile aus Schritt 2 an; den übrigen Inhalt änderst du
              nicht. · Setz die Uhrzeit aus Schritt 1 und keine andere. · Schick bis zur Bestätigung des Auftraggebers
              nur an die Testadresse; an echte Adressen geht vorher nichts.
LIEFERUNG:    einstellungen.json ohne Passwort-Zeile · Ausgabe von Schritt 3 · die cron-Zeile · offene Punkte ·
              jede Stelle, an der diese Anleitung nicht reichte, mit Zitat.
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
