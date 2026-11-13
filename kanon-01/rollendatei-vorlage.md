STATUS: `<ENTWURF | GÜLTIG | ZURÜCKGEZOGEN>` (Kanon 01, §7.4)

# Rolle `<Name>` – `<Repo oder Thema>`

<!-- Vorlage Kanon 01 Single Agent 3.1, BETRIEB (§6). Ablage: <repo>/betrieb/rollen/<rolle>.md. Schreibt nur die
     aktive Instanz der Rolle. Nach JEDEM Schritt STAND und OFFEN nachtragen (§6.3). Alle `<…>` ersetzen, Kommentare löschen. -->

```text
ROLLE:         <Name> – <ein Satz, wofür die Rolle da ist>
REPO:          <owner/repo>, Arbeitszweig <…>, live <…>
SCHREIBT:      <Pfade, die nur diese Rolle ändert, z. B. public/**> · <außerdem: Issues mit Label …, Postfach-Nachrichten, andere Repos>
SCHREIBT NIE:  <Pfade anderer Rollen, Regeldateien, Kanon-Kopien> → zuständig: <Rolle>
AUFTRÄGE VON:  Betreiber<, Rolle X>            (§2.2: wer diese Rolle beauftragen darf; fehlt die Zeile: nur der Betreiber)
REGELN:        Kanon 01 Single Agent 3.1 (KERN + BETRIEB, kanon_01_single_agent/regeln.md) · Projektregeln: <Datei oder „keine“> · Betriebsregeln: <z. B. betrieb/ARBEITSWEISE.md>
STÄNDE:        Regelstand <für Claude-Instanzen: „kanon_01 3.1“; für Worker: Regelstand ihrer Regeldatei> · Logstand L-<NNN>
               (kanon/AENDERUNGEN.md) · Erfahrungsstand E-<NNN> (betrieb/<rolle>-erfahrungen.md)
POSTFACH:      <Postfach-Repo>/post/<rolle>/ (beim Start `ls`; fehlt der Ordner: noch keine Nachrichten)
FRAGEN:        höchstens <N> je Liste (§5.6; fehlt die Zeile: drei)
DIENST:        aktiv: <Rolle>_<Nr> seit <Datum, Zeit gemessen> · vorher: <Rolle>_<Nr> (<von–bis>, Grund des Wechsels)
```

## STAND (nach jedem Schritt nachtragen, §6.3)
- `<Was ist live, was liegt auf dem Arbeitszweig, letzter Commit mit Kennung>`
- `<Woran arbeitet die aktive Instanz gerade, welcher Schritt ist der nächste>`

## OFFEN (nummeriert, mit Datum)
1. `<…>`

## ENTSCHEIDUNGEN DES BETREIBERS (neueste oben; Zitat, Datum, betroffene Datei) – oder Verweis auf betrieb/entscheidungen.md
- `<JJJJ-MM-TT>` „`<Zitat>`“ → `<Datei>`

## RISIKOLISTE (§4.7: Vorfälle ohne Code-Prüfung, je mit Vorbeuge-Prüfung)
- `<Vorfall>` → `<was vor jedem Schritt geprüft wird>`

## ÜBERGABEN (§6.3, nur anhängen)
DIENSTBEGINN · DIENSTENDE · NACHFOLGER · VERMÄCHTNIS · GRUND
