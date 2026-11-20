# Kapsel lokal-tests 0.4.0

Bauumgebung und Tests lokaler Werkzeuge, wenn die bauende KI kein Windows hat.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt, was in der Bauumgebung getestet wird, was nur auf dem Zielrechner geht und wie der Prüfbericht
              aussieht.
GILT FÜR:     Rezepte lokal-python und lokal-powershell; die Werkzeuge der Tests nennt die Laufzeit-Kapsel.
BRAUCHT:      Kapsel kern
```

### REGELN
- 1 Die Bauumgebung hat meist kein Windows und kein Netz. Teste dort gegen den echten Server auf 127.0.0.1 an einem
  freien Port und mit echten Dateien im Temp-Ordner.
- 2 Ersetze Windows-APIs und fremde Programme durch Attrappen: Größen der Strukturen für x64 · Datenbankserver durch eine
  Attrappe · andere Werkzeuge durch nachgebaute Prozesse · Outlook durch einen Adapter mit festen Antworten. Eine
  Attrappe belegt keinen Betrieb mit dem echten Programm.
- 3 Klickabläufe laufen mit Node im Headless-Chrome über das DevTools-Protokoll und warten höchstens 15 s auf einen neuen
  Zustand. Der Headless-Browser gehört zur Bauumgebung, nie zur Installation.
- 4 `.cmd`, `.vbs` und `.ps1` laufen ohne Windows nicht. Ihr Test prüft den Text (bei PowerShell zusätzlich mit dem
  Parser, wo einer da ist); die Lieferung nennt sie „unter Windows ungeprüft“. Eine Prüfung nur mit PowerShell 7 belegt
  keine Eignung für 5.1.
- 5 Ein Test prüft das Manifest gegen den Git-Index (Kapsel lokal-updates).
- 6 Mindestfälle über alle Kapseln: Start ohne Administratorrechte · fremdes Arbeitsverzeichnis · Pfad mit Leerzeichen
  und Umlauten · zweiter Start · Host, `Origin`, Token, Content-Type · Pfadgrenzen · Größen · Zeichensatz · null, ein
  und viele Datensätze · Sperre · Abbruch · Wiederholung · Rücknahme eines Updates · Schwärzung. Fachliche Tests
  ergänzen sie, ohne nur den Code nachzuschreiben.
- 7 Prüfbericht (`PRUEFBERICHT.md` oder Abschnitt der README): je Fall Soll, Ist, Umgebung (Windows-, Laufzeit- und
  Browserfassung), Datum und Ergebnis. Ohne Windows lieferst du die statischen Ergebnisse und die Prüfschritte für den
  Menschen.
- Grund: Was unter Linux grün ist, ist auf Windows noch nicht gelaufen; der Bericht hält beides auseinander.
- Stand: Regeln 1–5 erprobt (Python); Regeln 6 und 7 Empfehlung (unbelegt).

## BLOCK B – für Menschen

Die KI testet, so weit es ohne Windows geht, und sagt dir genau, was du auf deinem Rechner selbst prüfen musst.
