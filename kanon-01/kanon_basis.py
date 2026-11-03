"""Kanon 01 Single Agent – Prüfbausteine für KI-Worker (Python, ohne Fremdpakete).

Herkunft: Kanon 01 Single Agent (kanon/kanon_01_single_agent, Regeln in regeln.md).
Grundsatz: Was nur im Prompt steht, lenkt. Was hier geprüft wird, gilt.
Jede Funktion nennt die Regel (B-Kennung, in regeln.md in Klammern an jeder Regel), die sie absichert.

In Projekten als Kopie einbinden und NICHT dort ändern. Änderungen nur an der Quelle, dann neu kopieren.
"""

from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

KANON_BASIS_VERSION = "1.1.2"

__all__ = [
    "KANON_BASIS_VERSION", "Abbruch", "regeln_laden", "regelstand_ok", "schema_fehler",
    "freigabe", "codebloecke", "text_gezeigt", "marker_offen", "zahlen_ohne_beleg",
    "sperrtreffer", "anker_zahl", "nachlesen", "behauptungen", "fehlversuche",
    "jetzt", "fusszeile", "dubletten", "norm", "sperrliste_laden", "schema_laden", "entfernte_zeilen",
    "laufzeile", "ERFAHRUNG_ARTEN", "erfahrungen_laden", "erfahrungsstand_ok", "erfahrung_pruefen", "erfahrung_anhaengen",
]


class Abbruch(Exception):
    """fail-closed: Der Lauf schreibt nichts und meldet den Grund (B16)."""


# ---------------------------------------------------------------- Hilfen
def norm(text: str) -> str:
    """Vergleichsform: Unicode NFC, geschützte Leerzeichen zu Leerzeichen, Leerraum zusammengefasst."""
    t = unicodedata.normalize("NFC", text or "").replace(" ", " ").replace("\r\n", "\n")
    return re.sub(r"\s+", " ", t).strip()


# ---------------------------------------------------------------- B1 Regelstand
# Zwei Formen: Worker-Regeldatei „Regelstand: 2026-10-27b“ (Zeile beginnt damit) und Kanon 3.x
# „STATUS: KANONISCH · Regelstand: kanon_01 3.1 (03.11.2026, L-038) · …“ (Stand bis zur Klammer oder zum ·).
_REGELSTAND = re.compile(r"^(?:STATUS:[^\n]*?· )?Regelstand:\s*([^\n(·]+?)\s*(?:\(|·|$)", re.MULTILINE)


def regeln_laden(pfad: str | Path) -> tuple[str, str]:
    """Regeln frisch aus der versionierten Datei. Fehlt Datei oder Regelstand-Zeile: Abbruch (B1, B16)."""
    p = Path(pfad)
    if not p.is_file():
        raise Abbruch(f"Regeldatei fehlt: {p.name}")
    text = p.read_text(encoding="utf-8")
    m = _REGELSTAND.search(text)
    if not m:
        raise Abbruch(f"Regeldatei {p.name} ohne Zeile „Regelstand:“")
    return text, m.group(1)


def regelstand_ok(antwort: dict, stand: str, feld: str = "regelstand") -> bool:
    """Hat das Modell den Regelstand wörtlich bestätigt? (B1)"""
    return isinstance(antwort, dict) and str(antwort.get(feld) or "").strip() == stand


# ---------------------------------------------------------------- B16 Schema
_TYPEN = {"object": dict, "array": list, "string": str, "boolean": bool,
          "integer": int, "number": (int, float), "null": type(None)}


def schema_fehler(wert, schema: dict, pfad: str = "$") -> list[str]:
    """Kleiner Prüfer für den in antwortschema.json genutzten Teil von JSON Schema:
    type, required, properties, additionalProperties(false), enum, items, maxItems, minLength, maxLength, pattern.
    Gibt eine Liste von Fehlern zurück; leer = gültig (B16)."""
    fehler: list[str] = []
    typ = schema.get("type")
    if typ:
        typen = typ if isinstance(typ, list) else [typ]
        ok = any(isinstance(wert, _TYPEN[t]) and not (t in ("integer", "number") and isinstance(wert, bool))
                 for t in typen)
        if not ok:
            return [f"{pfad}: erwartet {'/'.join(typen)}, ist {type(wert).__name__}"]
    if "enum" in schema and wert not in schema["enum"]:
        fehler.append(f"{pfad}: Wert {wert!r} nicht erlaubt")
    if isinstance(wert, str):
        if "minLength" in schema and len(wert) < schema["minLength"]:
            fehler.append(f"{pfad}: zu kurz")
        if "maxLength" in schema and len(wert) > schema["maxLength"]:
            fehler.append(f"{pfad}: zu lang ({len(wert)} > {schema['maxLength']})")
        if "pattern" in schema and not re.search(schema["pattern"], wert):
            fehler.append(f"{pfad}: passt nicht zum Muster")
    if isinstance(wert, dict):
        for k in schema.get("required", []):
            if k not in wert:
                fehler.append(f"{pfad}: Pflichtfeld „{k}“ fehlt")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for k in wert:
                if k not in props:
                    fehler.append(f"{pfad}: unbekanntes Feld „{k}“")
        for k, s in props.items():
            if k in wert:
                fehler += schema_fehler(wert[k], s, f"{pfad}.{k}")
    if isinstance(wert, list):
        if "maxItems" in schema and len(wert) > schema["maxItems"]:
            fehler.append(f"{pfad}: höchstens {schema['maxItems']} Einträge")
        if "items" in schema:
            for i, x in enumerate(wert):
                fehler += schema_fehler(x, schema["items"], f"{pfad}[{i}]")
    return fehler


# ---------------------------------------------------------------- B4 Freigabe
_FUELL = {"ok", "okay", "ja", "jo", "danke", "dankeschön", "super", "gut", "prima", "perfekt", "genau",
          "so", "das", "alles", "bitte", "speichern", "übernehmen", "schön", "klasse", "top", "fein", "sehr",
          "vielen", "dank", "es", "ist", "gerne", "gern", "und", "dir", "mir", "zu", "auch", "sieht", "aus",
          "schließen", "schliessen", "issue", "kannst", "du", "wunderbar", "passend", "richtig", "läuft"}
_NEIN = re.compile(r"\b(nicht|noch\s+nicht|kein|keine|nein)\b", re.IGNORECASE)


def freigabe(kommentar: str, wort: str = "passt", fuellwoerter: set[str] | None = None) -> tuple[bool, str]:
    """Freigabe nur durch das benannte Wort, ohne Verneinung und ohne Zusatzwünsche (B4).
    „passt“ → frei. „Passt, danke!“ → frei. „passt nicht“ → nicht frei.
    „Passt, aber nimm 1998“ → nicht frei (Kontext vor Kurzwort: ein Zusatz ist eine Rückfrage).
    Gibt (frei, grund) zurück."""
    # zitierte Zeilen („> …“) gehören nicht zum Kommentar, sondern zum zitierten Vorschlag
    t = "\n".join(z for z in (kommentar or "").splitlines() if not z.lstrip().startswith(">")).strip()
    if not re.search(rf"\b{re.escape(wort)}\b", t, re.IGNORECASE):
        return False, f"kein „{wort}“"
    if _NEIN.search(t):
        return False, "Verneinung im Kommentar"
    fuell = _FUELL if fuellwoerter is None else fuellwoerter
    rest = [w for w in re.findall(r"[\wäöüß]+", t.lower()) if w != wort.lower() and w not in fuell]
    if rest:
        return False, "„" + wort + "“ mit Zusatz: " + " ".join(rest[:8])
    return True, "ok"


# ---------------------------------------------------------------- B4/B7 gezeigter Text
_BLOCK = re.compile(r"```[a-zA-Z]*\n(.*?)```", re.DOTALL)


def codebloecke(text: str) -> list[str]:
    """Alle Codeblöcke einer früheren Antwort (der Text, den der Mensch gesehen hat)."""
    return [m.group(1) for m in _BLOCK.finditer(text or "")]


def text_gezeigt(neu: str, gezeigt: list[str], kontext: str = "") -> bool:
    """Ist der zu schreibende Text genau ein gezeigter Block? (B4: Freigabe gilt nur für den gezeigten Text)
    Genau heißt: gleich bis auf Leerraum. Optional darf der Block zusätzlich mit einer Kontextzeile
    beginnen (z. B. der Ankerzeile, unter der eingefügt wird). Ein Teilstück eines Blocks reicht nicht."""
    n = norm(neu)
    if not n:
        return False
    erlaubt = {n}
    if kontext.strip():
        erlaubt.add(norm(kontext.strip("\n") + "\n" + neu))
    return any(norm(b) in erlaubt for b in gezeigt)


def entfernte_zeilen(alt: str, neu: str) -> list[str]:
    """Zeilen, die beim Ersetzen von alt durch neu wegfallen (B4: was wegfällt, muss gezeigt sein)."""
    bleibt = {norm(z) for z in (neu or "").splitlines()}
    return [z for z in (alt or "").splitlines() if z.strip() and norm(z) not in bleibt]


# ---------------------------------------------------------------- B6 offene Marker
def marker_offen(text: str, muster: str = r"⟦\s*Vorschlag") -> list[str]:
    """Nicht aufgelöste Vorschlags-Marker. Text mit offenem Marker wird nicht gespeichert (B6)."""
    return re.findall(muster + r"[^⟧]*⟧?", text or "")


# ---------------------------------------------------------------- B7 Zahlen
_ZAHL = re.compile(r"(?<![\w.,])\d+(?:[.,]\d+)*(?![\d])")


def zahlen_ohne_beleg(neu: str, belege: list[str], listen_nummern: bool = True) -> list[str]:
    """Zahlen (auch Jahre, „20er“) im neuen Text, die in keinem Beleg vorkommen (B7: wörtlich, nicht präzisieren).
    Listen-Nummern am Zeilenanfang („1. “) werden ignoriert."""
    text = neu or ""
    if listen_nummern:
        text = re.sub(r"(?m)^\s*\d+\.\s", " ", text)
    vorrat = {m.group(0) for b in belege for m in _ZAHL.finditer(b or "")}
    gesehen, fehlt = set(), []
    for m in _ZAHL.finditer(text):
        z = m.group(0)
        if z not in vorrat and z not in gesehen:
            gesehen.add(z)
            fehlt.append(z)
    return fehlt


# ---------------------------------------------------------------- B14 Sperrliste
def sperrtreffer(text: str, woerter: list[str]) -> list[str]:
    """Gesperrte Einträge, ohne Groß/Klein. Treffer → nicht schreiben (B14b).
    Normaler Eintrag = ganzes Wort („Anna“ trifft nicht „Annabell“). Mit „*“ am Ende = Wortanfang („Kontonummer*“
    trifft auch „Kontonummern“). Mit „re:“ davor = regulärer Ausdruck für Muster (z. B. Kontonummern, siehe README).
    Ein ungültiger Ausdruck sperrt immer (fail-closed)."""
    t, treffer = text or "", []
    for w in woerter:
        w = w.strip()
        if not w:
            continue
        if w.startswith("re:"):
            try:
                hit = re.search(w[3:], t, re.IGNORECASE)
            except re.error:
                hit = True
        elif w.endswith("*"):
            hit = re.search(rf"(?<!\w){re.escape(w[:-1])}", t, re.IGNORECASE)
        else:
            hit = re.search(rf"(?<!\w){re.escape(w)}(?!\w)", t, re.IGNORECASE)
        if hit:
            treffer.append(w)
    return treffer


def sperrliste_laden(pfad: str | Path) -> list[str]:
    """Eine Zeile je Eintrag (Wort, Wort* oder re:Muster), „ #“ (Leerzeichen + #) leitet Kommentare ein. Fehlende Datei = leere Liste (Sperre ist Zusatz)."""
    p = Path(pfad)
    if not p.is_file():
        return []
    zeilen = [z.strip() for z in p.read_text(encoding="utf-8").splitlines()]
    return [z.split(" #", 1)[0].strip() for z in zeilen if z and not z.startswith("#") and z.split(" #", 1)[0].strip()]


# ---------------------------------------------------------------- B12/B13 Anker und Rücklese
def anker_zahl(text: str, anker: str) -> int:
    """Wie oft steht der Anker im Text? Schreiben nur bei genau 1 (B12)."""
    return text.count(anker) if anker else 0


def nachlesen(pfad: str | Path, neu: str, anker: str | None = None, vorher: str | None = None) -> None:
    """Rücklese nach dem Schreiben (B13). Prüft gegen den Stand vor dem Schreiben (`vorher`, None = Datei neu):
    der neue Text steht genau einmal MEHR als vorher, der Anker unverändert oft, keine neue Doppelzeile direkt
    hintereinander, keine doppelt kodierten Umlaute. Sonst Abbruch."""
    p = Path(pfad)
    roh = p.read_bytes()
    text = roh.decode("utf-8")
    alt = vorher or ""
    kern = (neu or "").strip("\n")
    if kern and text.count(kern) != alt.count(kern) + 1:
        raise Abbruch(f"Nachlesen {p.name}: der neue Text steht {text.count(kern)}-mal in der Datei "
                      f"(vorher {alt.count(kern)}-mal, erwartet {alt.count(kern) + 1})")
    if anker and text.count(anker) != max(1, alt.count(anker)):
        raise Abbruch(f"Nachlesen {p.name}: die Ankerzeile steht {text.count(anker)}-mal in der Datei")

    def doppel(t: str) -> int:
        z = [x for x in t.splitlines() if x.strip()]          # Überschriften zählen als Trenner mit
        return sum(1 for a, b in zip(z, z[1:]) if a == b and not a.startswith("#"))
    if doppel(text) > doppel(alt):
        raise Abbruch(f"Nachlesen {p.name}: durch die Änderung steht eine Zeile zweimal direkt hintereinander")
    if re.search(rb"\xc3[\x82\x83]\xc2[\x80-\xbf]|\xc3\xa2\xc2\x80", roh):
        raise Abbruch(f"Nachlesen {p.name}: doppelt kodierte Zeichen gefunden")


# ---------------------------------------------------------------- B5 Behauptungen
_ERFOLG = r"(gespeichert|gepusht|committet|geschlossen|hochgeladen|gelöscht|geändert|übernommen|eingetragen|hinzugefügt|ergänzt|erledigt|live)"
_BEHAUPTUNG = re.compile(
    rf"\b(ich\s+habe\s+(?:\S+\s+){{0,4}}{_ERFOLG}|habe\s+ich\s+(?:\S+\s+){{0,4}}{_ERFOLG}"
    rf"|(ist|wurde|sind|wurden)\s+(jetzt\s+|nun\s+|bereits\s+|schon\s+)?{_ERFOLG})",
    re.IGNORECASE)


def behauptungen(text: str) -> list[str]:
    """Erfolgsbehauptungen des Modells. Erfolg meldet nur der Code (B5)."""
    return [m.group(0) for m in _BEHAUPTUNG.finditer(text or "")]


# ---------------------------------------------------------------- B18 Versuche
def fehlversuche(texte: list[str], marker: str) -> int:
    """Wie oft steht die Fehler-Fußzeile des Codes schon im Verlauf? (B18: höchstens drei Versuche)"""
    return sum((t or "").count(marker) for t in texte)


# ---------------------------------------------------------------- Zeit (Messen statt erinnern)
def jetzt(zone: str = "Europe/Berlin") -> str:
    """Gemessene Zeit mit echter Zeitzone (nie fester Versatz wie „+2h“)."""
    return datetime.now(ZoneInfo(zone)).isoformat(timespec="seconds")


# ---------------------------------------------------------------- B21 Beleg
def fusszeile(gespeichert: list[str], fehler: list[str], beleg: dict[str, str]) -> str:
    """Die einzige Erfolgsmeldung: geschrieben vom Code, mit Beleg (B5, B15, B21).
    beleg z. B. {"Commit": "abc1234", "Regelstand": "2026-10-27b", "Modell": "mistral-large-latest (Konfiguration)"}."""
    teile = []
    belegtext = " · ".join(f"{k} {v}" for k, v in (beleg or {}).items() if v)
    if gespeichert:
        teile.append("✅ Gespeichert: " + ", ".join(f"`{d}`" for d in gespeichert) + (f" ({belegtext})" if belegtext else ""))
    if fehler:
        teile.append("⚠️ Nicht gespeichert: " + "; ".join(fehler))
    return "\n".join(teile) or "Nichts gespeichert."


# ---------------------------------------------------------------- B11 Dubletten
def dubletten(neu: str, dateien: dict[str, str], min_laenge: int = 40) -> list[tuple[str, str]]:
    """Längere Zeilen des neuen Textes, die schon in anderen Dateien stehen (B11: eine Wahrheit genau einmal)."""
    treffer = []
    for z in (neu or "").splitlines():
        k = norm(z.lstrip("-*# "))
        if len(k) < min_laenge:
            continue
        for name, inhalt in dateien.items():
            if k in norm(inhalt):
                treffer.append((name, k[:80]))
                break
    return treffer


def schema_laden(pfad: str | Path) -> dict:
    return json.loads(Path(pfad).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- B23 Laufprotokoll
_PROTOKOLL_KOPF = "| Start | Dauer | Auslöser | Regelstand | Ergebnis | Grund |\n|---|---|---|---|---|---|\n"


def _zelle(text: str, laenge: int = 200) -> str:
    t = re.sub(r"\s+", " ", str(text or "")).replace("|", "/").strip()
    return (t[: laenge - 1] + "…") if len(t) > laenge else (t or "–")


def _dauer(d: timedelta) -> str:
    s = max(0, round(d.total_seconds()))
    return f"{s} s" if s < 120 else f"{round(s / 60)} min"


def laufzeile(pfad: str | Path, start: datetime, ende: datetime, ausloeser: str, regelstand: str,
              ergebnis: str, grund: str, titel: str = "Laufprotokoll") -> None:
    """Hängt genau eine Zeile je Lauf an das Protokoll an (B23); legt die Datei mit Kopf an, wenn sie fehlt.
    start/ende: gemessene Zeiten mit Zeitzone (datetime.now(ZoneInfo(...))). ergebnis: „ok“ (Lauf ordentlich beendet,
    auch ohne Speichern) oder „fehler“ (Abbruch oder ein Schreibfehler). Alte Zeilen bleiben unverändert – sonst Abbruch.
    Nebenpflicht: Der Aufrufer fängt Fehler ab, damit der Lauf nie daran scheitert (B17)."""
    if ergebnis not in ("ok", "fehler"):
        raise ValueError("ergebnis muss „ok“ oder „fehler“ sein")
    if start.tzinfo is None or ende.tzinfo is None:
        raise ValueError("start und ende brauchen eine Zeitzone (gemessen, nie fester Versatz)")
    p = Path(pfad)
    vorher = p.read_text(encoding="utf-8") if p.is_file() else None
    zeile = (f"| {start.strftime('%Y-%m-%d %H:%M:%S %Z')} (gemessen) | {_dauer(ende - start)} | {_zelle(ausloeser, 80)} "
             f"| {_zelle(regelstand, 40)} | {ergebnis} | {_zelle(grund)} |\n")
    basis = vorher if vorher is not None else f"# {titel}\n\nEine Zeile je Lauf, geschrieben vom Programm. Nur anhängen.\n\n{_PROTOKOLL_KOPF}"
    if basis and not basis.endswith("\n"):
        basis += "\n"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(basis + zeile, encoding="utf-8")
    neu = p.read_text(encoding="utf-8")
    if not neu.startswith(vorher or "") or not neu.endswith(zeile):
        raise Abbruch(f"Protokoll {p.name}: Rücklese passt nicht – alte Zeilen müssen unverändert bleiben")


# ---------------------------------------------------------------- B24/B25 Erfahrungen
ERFAHRUNG_ARTEN = ("Werkzeug", "Format", "Fehlervermeidung", "Ablauf")
_EINTRAG = re.compile(r"^E-(\d{3,}) · ", re.MULTILINE)


def erfahrungen_laden(pfad: str | Path) -> tuple[str, str]:
    """Erfahrungen für den Prompt und ihr Stand = Nummer des neuesten Eintrags (B25). Fehlt die Datei: ("", "E-000").
    Ist die Datei da, aber nicht lesbar, fliegt der Fehler durch (fail-closed wie bei den Regeln)."""
    p = Path(pfad)
    if not p.is_file():
        return "", "E-000"
    text = p.read_text(encoding="utf-8")
    nummern = [int(n) for n in _EINTRAG.findall(text)]
    return text, f"E-{max(nummern, default=0):03d}"


def erfahrungsstand_ok(antwort: dict, stand: str, feld: str = "erfahrungsstand") -> bool:
    """Hat das Modell den Stand der Erfahrungen wörtlich bestätigt? (B25, wie B1)"""
    return regelstand_ok(antwort, stand, feld)


def erfahrung_pruefen(e, bestand: str, belege: list[str]) -> list[str]:
    """Prüft einen vorgeschlagenen Eintrag (B24). Leere Liste = darf angehängt werden.
    e = {"art": eine aus ERFAHRUNG_ARTEN, "was": ein Satz, "warum": ein Satz}; bestand = bisherige Erfahrungen;
    belege = Texte, aus denen Zahlen stammen dürfen (Kommentar, Dateien, Verlauf des Betreibers)."""
    if not isinstance(e, dict):
        return ["Erfahrung ist kein Objekt"]
    fehler = []
    if e.get("art") not in ERFAHRUNG_ARTEN:
        fehler.append(f"Art muss eine von {', '.join(ERFAHRUNG_ARTEN)} sein")
    for feld in ("was", "warum"):
        w = str(e.get(feld) or "")
        if not w.strip():
            fehler.append(f"„{feld}“ fehlt")
        elif "\n" in w.strip() or len(w) > 300:
            fehler.append(f"„{feld}“ muss ein Satz sein (eine Zeile, höchstens 300 Zeichen)")
    text = f"{e.get('was') or ''} {e.get('warum') or ''}"
    if marker_offen(text):
        fehler.append("enthält einen offenen Vorschlag")
    ohne = zahlen_ohne_beleg(text, belege)
    if ohne:
        fehler.append("Zahlen ohne Beleg: " + ", ".join(ohne[:5]))
    was = norm(str(e.get("was") or "")).lower().rstrip(".")
    vorhanden = {norm(z[4:]).lower().rstrip(".") for z in (bestand or "").splitlines() if z.startswith("Was:")}
    if was and (was in vorhanden or (len(was) >= 40 and was in norm(bestand).lower())):
        fehler.append("steht schon in den Erfahrungen")       # gleicher „Was“-Satz oder langer Satz im freien Text
    return fehler


def erfahrung_anhaengen(pfad: str | Path, e: dict, datum: str, lauf: str, titel: str = "Erfahrungen") -> str:
    """Hängt einen geprüften Eintrag mit der nächsten Nummer an (nur anhängen, B24) und liest zurück (B13).
    Gibt die neue Nummer zurück, z. B. „E-018“. Bei Fehler wird die Datei auf den alten Stand zurückgesetzt."""
    p = Path(pfad)
    vorher = p.read_text(encoding="utf-8") if p.is_file() else None
    _, stand = erfahrungen_laden(p)
    nr = f"E-{int(stand[2:]) + 1:03d}"
    block = (f"{nr} · {datum} · Lauf {lauf} · Art: {e['art']}\n"
             f"Was: {norm(str(e['was']))}\nWarum: {norm(str(e['warum']))}\n")
    basis = vorher if vorher is not None else (f"# {titel}\n\nVom Programm angehängt (Vorschläge des Modells, geprüft). "
                                              f"Daten, keine Regeln. Nur anhängen; was sich bewährt, wird über eine "
                                              f"neue Regelfassung zur Projektregel.\n")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(basis.rstrip("\n") + "\n\n" + block, encoding="utf-8")
    try:
        nachlesen(p, block, vorher=vorher)
        if not p.read_text(encoding="utf-8").startswith((vorher or "").rstrip("\n")):
            raise Abbruch(f"Erfahrungen {p.name}: alte Einträge haben sich verändert")
    except Abbruch:
        if vorher is None:
            p.unlink()
        else:
            p.write_text(vorher, encoding="utf-8")
        raise
    return nr
