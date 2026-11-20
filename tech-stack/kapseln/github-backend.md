# Kapsel github-backend 0.4.1

GitHub als Ablage eines lokalen Werkzeugs: Protokolle senden, Austausch ohne Firmendaten, Zugang prüfen. Wahlweise.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt, was ein lokales Werkzeug selbst mit GitHub tut, außer Updates (Kapsel lokal-updates) und
              Rückmeldungen (Kapsel rueckmeldungen).
GILT FÜR:     Rezepte lokal-python und lokal-powershell, wenn das Werkzeug Protokolle sendet oder über GitHub austauscht.
BRAUCHT:      Kapseln kern · windows-zugang · lokal-log
```

### REGELN
- 1 Diese Kapsel gilt nur, wenn die Ablage GitHub ist (Wahl der Ablage: Kapsel kern). Firmendaten gehen nie nach
  GitHub. Bau nur, was das Werkzeug braucht.
- 2 Protokolle: Auf Knopfdruck legt das Werkzeug Protokolle ohne Firmendaten als einen Commit in einem Protokoll-Repo ab,
  Ordner `protokolle/<werkzeug>/<JJJJ-MM-TT_HHMM>/`. Das Protokoll-Repo ist ein eigenes Repo, nicht das des Werkzeugs;
  Besitzer, Repo, Branch und Ordner haben einen Standard im Code (den nennt der Auftrag) und lassen sich in der
  Einstellung (Abschnitt `protokolle`) ändern. Es gilt eine Positivliste von Dateien und Feldern, kein Suchfilter. Vor
  dem Senden zeigt eine Vorschau jede Datei mit Inhalt. Der Schlüssel dafür hat Schreibrecht nur auf das Protokoll-Repo
  und ein eigenes Ziel ohne Rückfall (Kapsel windows-zugang). Gesendet wird über die Git-Data-API: Baum mit
  `base_tree`, Commit, Ref vorschieben ohne `force`.
- 3 Technik-Protokoll: `Logs/technik_JJJJMMTT.log` (UTF-8 ohne BOM, LF), eine Zeile je Ereignis: Zeit, dann
  `ereignis=<name>` und `schluessel=wert`-Paare. Feste Ereignisse mit festen Feldern: `start` (Format, Version, Build,
  Port, Laufzeit, PID) · `ende` (Version, Build, Dauer) · `job` (Auftrag, Ergebnis `ok`, `nicht_ok` oder `fehler`,
  Dauer, wahlweise Zahl der Dateien gefunden/eingelesen/übersprungen/fehlerhaft, Zahl der Zeilen, Fehlerart, Quelle
  `server` oder `kommandozeile`). Zahlen von Dateien und Zeilen sind technische Zählwerte, keine Mengendaten. Nie:
  Pfade, Datei- oder Servernamen, Meldungstexte oder Firmendaten; jeder Wert wird gegen ein Muster geprüft, was nicht
  passt, ergibt eine Zeile `ereignis=defekt`. Eine Datei mit einer solchen Zeile oder einer Zeile außerhalb des Musters
  ist defekt und wird nicht gesendet. Das Tageslog gehört nie zu den gesendeten Dateien.
- 4 Austausch über GitHub nur ohne Firmendaten: Einstellungen, Vorlagen, Nachrichten zwischen KIs. Firmendaten tauschen
  Werkzeuge lokal aus (Kapsel austausch).
- 5 „Zugang prüfen“: `GET /repos/{owner}/{repo}`; die Meldung trennt Token fehlt · Token falsch oder abgelaufen · kein
  Zugriff auf das Repo · Abrufgrenze · Netz. Der Kopf lautet `Authorization: Bearer <token>`; bei einer Umleitung auf
  einen anderen Host fällt er weg.
- Grund: Protokolle ohne Firmendaten lassen eine KI Fehler prüfen, ohne dass etwas vom Rechner abfließt.
- Test: nachgebautes GitHub; eine Zeile mit Pfad ergibt `ereignis=defekt`, die Datei wird nicht gesendet.
- Stand: Protokolle erprobt (Python) · Knowledge, SharePoint und lokale Dateien als Ablage offen · PowerShell offen.

### WAHL
- W1 Kopf zu GitHub: `Authorization: Bearer` (Empfehlung) oder `Authorization: token`. GitHub nimmt beide an.

## BLOCK B – für Menschen

Auf Knopfdruck schickt das Werkzeug ein technisches Protokoll ohne Firmendaten nach GitHub; du siehst vorher jede Datei.
So kann eine KI einen Fehler prüfen, ohne an deine Daten zu kommen.
