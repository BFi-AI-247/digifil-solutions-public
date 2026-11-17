# Vorlage: Auftrag im Zwei-Kanal-Format (Anwendung 1)

<!-- Kopiere den Block und ersetze alle Platzhalter in spitzen Klammern. Jedes Feld von Block A ist gefüllt. Ein Hinweis
     hinter ← nennt die Bedingung für eine Zeile: Lösche die Zeile, wenn sie nicht zutrifft, und lösche in jedem Fall
     den Hinweis. Lösche diesen Kommentar. Beispiel: beispiel-auftrag.md. -->

```text
BLOCK A
VON: <Kennung des Absenders aus Rolle und Nummer, z. B. Redaktion_2>
AN: <Kennung des Empfängers, z. B. Bau_1>
DATUM: <JJJJ-MM-TT, HH:MM Zeitzone> (gemessen | Kontextangabe, nicht gemessen)
RUN-ID: <Kürzel des Absenders>-<fortlaufende Nummer>
AUFTRAG: <Die Handlung in einem Satz.>
PARAMETER:
- <Datei, Pfad, Wert, Frist – alles, was der Empfänger zum Ausführen braucht, je Zeile ein Punkt.>
- <Wo das Format steht (Ordner oder Datei).>   ← wenn der Empfänger selbst im Format schreiben soll
- <Datei mit dem Hintergrund und wozu der Empfänger sie liest.>   ← wenn Block B länger als drei Absätze würde
- offen: <fehlende Angabe> – <was der Empfänger damit tut>   ← wenn dir eine Angabe fehlt
LEITPLANKEN: <Je Grenze erst, was richtig ist, dann was der Empfänger lässt – ausgeschrieben oder als Kennung aus einem
  Katalog, den Absender und Empfänger beide haben. Ohne Grenze: „keine“.>
FAIL-MODE: <Was der Empfänger tut, wenn ein Teil nicht geht.>
REQUIRE-ACK: <Was zurückkommt: mindestens RUN-ID und Stand der Ausführung, dazu alles, was der Absender prüfen will.>
ESKALATION: <Wer entscheidet, wenn der Empfänger nicht weiterkommt, und wie er ihn erreicht – nur für Blocker, die allein
  der Genannte lösen kann. Rückfragen kommen mit der Quittung. Ohne: „keine“.>

BLOCK B
<Hintergrund, Motivation, Einordnung für einen Menschen ohne Fachwissen, in höchstens drei Absätzen.>
```

## Quittung (Antwort des Empfängers, nicht mitschicken)

```text
<RUN-ID> · Quittung
Empfangen: <JJJJ-MM-TT, HH:MM Zeitzone> (gemessen)
Stand: <erledigt | teilweise | nicht begonnen> – <ein Satz>
Abweichungen: <keine | welcher Umstand welchem Feld entgegenstand>
Fragen: <keine | Rückfragen an den Absender>
Beleg: <Datei, Commit, Protokollzeile>
```
