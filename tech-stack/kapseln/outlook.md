# Kapsel outlook 0.4.0

Mail-Entwürfe im klassischen Outlook für Windows, ohne automatischen Versand. Wahlweise.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt, wie ein lokales PowerShell-Werkzeug Entwürfe in Outlook anlegt und im Ordner der gesendeten
              Elemente wiederfindet.
GILT FÜR:     Rezept lokal-powershell, wenn das Werkzeug Mails vorbereitet.
BRAUCHT:      Kapseln kern · lokal-befehle · lokal-log · laufzeit-powershell
```

### REGELN
- 1 Voraussetzungen: klassisches Outlook für Windows, ein eingerichtetes Profil, eine angemeldete Benutzersitzung. Das
  neue Outlook kennt das Objektmodell nicht. Geprüft wird nur auf ausdrücklichen Auftrag, denn schon das COM-Objekt kann
  Outlook starten. Fehlendes Profil, fehlende COM-Anbindung und gesperrter Zugriff werden getrennt gemeldet.
- 2 Alle Aufrufe stehen in `App/Modules/Outlook.psm1`. Sie laufen in einem eigenen Hilfsprozess
  (`powershell.exe -NoProfile -STA`), der die Aufträge nacheinander abarbeitet; COM-Objekte bleiben dort und gehen nie
  in Runspaces des Servers.
- 3 Übergabe an den Hilfsprozess über einen Kanal nur für den Benutzer (z. B. eine Named Pipe mit geprüfter
  Zugriffsregel), mit Auftragskennung und festem JSON-Schema; Dateien nur als dokumentierte Alternative mit engen
  Rechten. Mailinhalte nie als Code, Befehlszeile oder Skriptparameter.
- 4 Ein Entwurfsauftrag trägt `request_id`, Empfänger, CC, Betreff, Klartext oder bereinigte HTML-Bausteine, das Konto
  und wahlweise ausdrücklich gewählte Anhänge. BCC, ein anderes Absenderkonto oder ein gemeinsames Postfach nur aus dem
  Auftrag. Empfänger, Dateien und Grenzen werden vorher geprüft; unbekannte Empfänger löst das Werkzeug nicht selbst auf.
- 5 Entwurf: `MailItem` anlegen, das gewählte Konto setzen, das Fenster öffnen, die Signatur von Outlook übernehmen und den
  Inhalt in den vorhandenen HTML-Text einfügen; Bilder der Signatur bleiben erhalten. Fehlt die erwartete Signatur, dann
  meldet das Werkzeug das, statt eine zu erfinden.
- 6 `Save()` wird ausdrücklich aufgerufen, wenn ein gespeicherter Entwurf zugesagt ist. Zustände getrennt: `angefordert`,
  `geöffnet`, `gespeichert`, `unklar`, `gesendet gefunden`. Ein offenes Fenster ist kein gespeicherter Entwurf; die
  Kennung eines Elements kann sich beim Verschieben ändern.
- 7 Die `request_id` wird vor dem Schritt nach außen lokal vermerkt und, wo es geht, am Element. Vor einem neuen Entwurf
  wird nach einem vorhandenen gesucht. Nach einem Absturz gibt es kein „genau einmal“; ein unklarer Auftrag wird geklärt,
  bevor ein zweiter entsteht.
- 8 Kein automatisches `Send()`. Der Mensch prüft und sendet im Outlook-Fenster. Versand durch das Werkzeug ist eine
  eigene Kapsel mit eigenem Auftrag. Ein Fund unter „Gesendete Elemente“ ist kein Zustell- oder Lesebeleg.
- 9 Abgleich: nur im gewählten Konto, mit Grenzen für Zeitraum, Zahl der Elemente und Laufzeit; eine abgeschnittene Suche
  wird gemeldet. Erkennungsmerkmal ist eine Kennung zusammen mit Konto, Empfängern, Zeit und fachlichem Bezug; Betreff
  und Text allein reichen nicht. Ergebnis: `Treffer`, `mehrdeutig`, `kein Treffer im Suchbereich`, `Suche
  unvollständig` oder `Fehler`. Von Hand gesetzte Markierungen bleiben als solche erkennbar.
- 10 Anhänge, Lesen des Posteingangs, Speichern von Anhängen, Antworten und Weiterleiten sind je eine eigene Erweiterung
  mit festgelegter Auswahl, Rechten, Dateinamen und Wiederholung; „Outlook“ allein erlaubt keine Verarbeitung des
  ganzen Postfachs.
- 11 Fehler: „Outlook beschäftigt“, Dialoge, verlorene Verbindung und Zeitüberschreitung werden ausdrücklich behandelt;
  eine Zeitüberschreitung beendet die Wirkung nicht. Solange eine Aktion unklar ist, startet keine zweite. Der
  Outlook-Prozess des Benutzers wird nie beendet; eigene COM-Verweise werden in umgekehrter Reihenfolge freigegeben, nie
  ein blindes `Quit()`.
- 12 Inhalte und Empfänger kommen nicht ins Log (Kapsel lokal-log). Outlook braucht keinen Zugangsschlüssel. Ein
  geplanter Lauf ohne angemeldeten Benutzer ist kein Weg für Outlook.
- Grund: Zwischen der Wirkung in Outlook und der eigenen Bestätigung gibt es keine gemeinsame Transaktion; deshalb
  entscheidet der Mensch über den Versand, und unklare Fälle werden geklärt statt wiederholt.
- Test: in der Bauumgebung ein Adapter mit festen Antworten (Kapsel lokal-tests). Auf dem Zielrechner: Entwurf,
  Speichern, Signatur mit Bild, Umlaute und Kyrillisch, wahlweise Anhang, geänderter Betreff, mehrere Konten, kein
  Treffer, Wiederholung nach verlorener Bestätigung. Ein echter Testversand nur auf eigenen Auftrag an genannte
  Empfänger; sonst bleibt er offen.
- Stand: Empfehlung (unbelegt) – im eigenen Bestand gibt es kein Vorbild; Entwurf, Signatur und begrenzte Suche gibt es
  in einem Werkzeug außerhalb dieses Bestands, Speichern, Hilfsprozess, mehrere Konten und Anhänge nirgends.

## BLOCK B – für Menschen

Das Werkzeug legt Mails als Entwurf in deinem Outlook an, mit deiner Signatur. Senden tust du selbst; danach kann das
Werkzeug nachsehen, ob die Mail unter „Gesendete Elemente“ liegt.
