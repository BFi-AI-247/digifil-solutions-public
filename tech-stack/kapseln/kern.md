# Kapsel kern 0.5.0

Begriffe und Regeln, die für jedes Werkzeug gelten, gleich nach welchem Rezept.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt, was jedes Werkzeug gemeinsam hat: Begriffe, Umgang mit Kapseln, Geheimnisse und Firmendaten,
              Einstellungen, Version, Pflichtdateien, ehrlicher Stand, Tests, Lieferung.
GILT FÜR:     jedes Rezept (lokal-python, lokal-powershell, web); immer zuerst lesen.
BRAUCHT:      –
BEGRIFFE:     Repo = die Ablage des Werkzeugs: Code, Auftrag, Pflichtdateien, Verträge. Das muss kein GitHub-Repo sein;
              die Wahl regelt Regel 13. Wo diese Kapseln „Repo“ schreiben, ist die gewählte Ablage gemeint.
              Werkzeug = ein Programm mit eigenem Ordner. Rezept = Liste der Kapseln für eine Art von Werkzeug, mit
              Schritten. Kapsel = eine Datei unter kapseln/, die eine Aufgabe ganz regelt; sie gilt immer ganz.
              Zielsystem = wo das Werkzeug läuft (Windows-Rechner oder Webspace). Bauumgebung = die Umgebung der
              bauenden KI, meist Linux, ohne Windows und oft ohne Netz.
              Firmendaten = Kassen-, Preis-, Kurs-, Bestands-, Mengen-, Umsatz-, Filial- und Personendaten sowie echte
              Server-, Datenbank-, Postfach- und Empfängernamen. Persönliche Daten = Namen, Ergebnisse, Fotos und Texte
              der Nutzer. Geheimnisse = Zugangsschlüssel, Passwörter, Sitzungstoken.
              Stand: erprobt = beim Menschen auf dem Zielsystem gelaufen · gebaut = nur in der Bauumgebung getestet ·
              offen = noch nirgends gebaut. „Empfehlung (unbelegt)“ = noch ohne Vorbild; befolgen wie eine Regel.
              Platzhalter: <werkzeug> = Ordnername in Kleinbuchstaben (z. B. muster) · <Name> = derselbe Name mit großem
              Anfangsbuchstaben (Muster) · <port> = Port des Werkzeugs.
```

### REGELN
- 1 Kapseln: Das Rezept nennt die Kapseln, die gelten. Eine Kapsel gilt ganz; „wahlweise“ heißt, das Werkzeug baut sie
  nur, wenn es die Aufgabe hat, und dann ganz. Wer eine Regel nicht befolgt, schreibt das in `ANNAHMEN.md` mit
  Kapsel und Nummer, nie still. Verweise in Kapseln und Aufträgen nennen immer eine ganze Kapsel.
- 2 Ein Werkzeug = ein Ordner. Die bauende KI schreibt nur dort (und in die Workflows des Werkzeugs) und prüft vor jedem
  Commit mit `git status`, dass nichts anderes dabei ist.
- 3 Firmendaten, persönliche Daten und Geheimnisse stehen nie im Repo, in Issues, Protokollen, Beispielen oder Chats; dort
  stehen nur erfundene Werte. Übernimm aus vorhandenem Code nur bereinigte technische Muster, denn auch er kann solche
  Werte enthalten. Der Auftrag kann echte Werte verlangen – dann nur in der Einstellung auf dem Zielsystem.
- 4 Pfade, Adressen und persönliche Werte stehen in einer Einstellungsdatei, nie im Code. Relative Pfade beziehen sich
  auf den Werkzeugordner; andere Anwender können andere Pfade haben.
- 5 Zur Laufzeit wird nichts installiert und nichts aus fremden Quellen geladen (keine CDN-Dateien, fremden
  Schriftarten, Telemetrie). Jede mitgelieferte Abhängigkeit steht mit Version, Herkunft, Lizenz und Prüfsumme in den
  Pflichtdateien. „Ohne Installation“ heißt nicht „ohne Voraussetzungen“; die Voraussetzungen nennt die README.
- 6 Version: beginnt bei 0.1.0; die dritte Stelle zählt Behebungen, die zweite neue Funktionen; jede Änderung erhöht eine
  der beiden. Sie steht an genau einer Stelle im Code (wo, sagt die Laufzeit-Kapsel) und in der Überschrift der README.
  Fassungen von Formaten und Verträgen zählen getrennt davon.
- 7 Pflichtdateien jedes Werkzeugs: `README.md` im Zwei-Kanal-Format (Fassung 1.3, Vorlage `readme-vorlage.md` aus
  `zwei-kanal-format/` in digifil-solutions-public): Block A für die KI, Block B für Menschen; Block A muss allein
  ausführbar sein · `ANNAHMEN.md`: jede Festlegung mit Kennung, Anlass, Lösung, Folge und Prüfstand; keine stillen
  Entscheidungen · `ARCHITEKTUR.md` · `EINSCHRAENKUNGEN.md` · `tests/`. Weitere Pflichtdateien nennt das Rezept.
- 8 Bau das riskanteste Paket zuerst. Erst wenn der Mensch es auf dem Zielsystem sieht (Sperrpunkt), geht der Bau
  weiter.
- 9 Jede Änderung im Verhalten bekommt einen Test, der ohne sie fehlschlägt. Der Testordner heißt `tests/`, immer klein.
- 10 Stand ehrlich: erprobt, gebaut und offen werden nicht vermischt; „Vorbild vorhanden“ ist kein Stand, „statisch
  geprüft“ schließt nichts ab. Ohne Zielsystem meldest du keine erfolgreiche Ausführung, sondern lieferst die
  Prüfschritte für den Menschen. „Erprobt“ gilt für die genannte Fassung und Umgebung.
- 11 FAIL-MODE: Ist eine Regel „offen“, dann entscheide selbst, schreib es in `ANNAHMEN.md` und nenne es in der
  Lieferung. Funktioniert eine Regel auf dem Zielsystem nicht, dann bau die nächstbeste Lösung, schreib sie in
  `ANNAHMEN.md` und melde den Fund an die Rolle, die diese Kapsel pflegt. Passt eine Regel nicht zum Auftrag, dann
  gilt der Auftrag; die Stelle meldest du ebenso.
- 12 Lieferung: Liste der Kapseln mit Stand je Kapsel · Abweichungen mit Kennung aus `ANNAHMEN.md` · Ergebnisse der
  Schritte des Rezepts · Dateien, die nur auf dem Zielsystem laufen, als „auf dem Zielsystem ungeprüft“, bis der Mensch
  sie gesehen hat · jede Stelle, an der eine Kapsel nicht reichte, mit Zitat.
- 13 Ablage: Vor dem ersten Schritt steht fest, wo das Repo liegt, und es steht in `ANNAHMEN.md`. GitHub ist die
  Empfehlung, keine Bedingung; andere Ablagen sind SharePoint, das Projektwissen der KI oder ein lokaler Ordner. Fester
  Stand, Prüfsumme und Sicherung gelten dort genauso (offen: dafür ist noch nichts gebaut). Ohne GitHub ist vor allem zu
  entscheiden: wo Auftrag, Pflichtdateien und Verträge liegen · wie ein Stand ohne Commit festgelegt wird · woher
  Update-Skripte ihre Quelle kennen · wohin Rückmeldungen gehen. Das entscheidest du nach Regel 11 und nennst es in der
  Lieferung. Firmendaten gehen in keine Ablage außerhalb des Zielsystems. Ein Rezept oder eine Kapsel, die GitHub
  zwingend braucht, sagt das am Anfang.
- Grund: Jedes Werkzeug beantwortete diese Fragen sonst neu, und dieselben Fehler passierten mehrfach.
- Lehren: Die Version blieb nach einem Paket unverändert (Regel 6). `Tests/` und `tests/` sind unter Windows derselbe
  Ordner (Regel 9).
- Stand: erprobt.

## BLOCK B – für Menschen

Diese Kapsel gilt für jedes Werkzeug. Sie hält fest, was nie ins Repo gehört, wie Versionen zählen, welche Dateien jedes
Werkzeug mitbringt und wie ehrlich der Stand gemeldet wird.
