"""Tests für kanon_basis.py – Aufruf im Ordner kanon_01_single_agent: python3 -m unittest discover -s tests"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

BASIS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASIS))
import kanon_basis as k  # noqa: E402


class Regelstand(unittest.TestCase):
    def test_laden_und_bestaetigen(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d, "regeln.md")
            p.write_text("Regelstand: 2026-10-27b\n\n# Regeln\n", encoding="utf-8")
            text, stand = k.regeln_laden(p)
            self.assertEqual(stand, "2026-10-27b")
            self.assertTrue(k.regelstand_ok({"regelstand": " 2026-10-27b "}, stand))
            self.assertFalse(k.regelstand_ok({"regelstand": "2026-10-27a"}, stand))
            self.assertFalse(k.regelstand_ok({}, stand))
            p.write_text("STATUS: KANONISCH · Regelstand: kanon_01 3.1 (03.11.2026, L-038) · freigegeben\n\n# Regeln\n", encoding="utf-8")
            _, stand = k.regeln_laden(p)
            self.assertEqual(stand, "kanon_01 3.1")

    def test_fehlende_datei_bricht_ab(self):
        with self.assertRaises(k.Abbruch):
            k.regeln_laden("/gibt/es/nicht.md")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d, "r.md"); p.write_text("# ohne Stand", encoding="utf-8")
            with self.assertRaises(k.Abbruch):
                k.regeln_laden(p)


class Schema(unittest.TestCase):
    schema = json.loads((BASIS / "antwortschema.json").read_text(encoding="utf-8"))

    def test_gueltig(self):
        a = {"regelstand": "2026-10-27b", "erfahrungsstand": "E-000", "antwort": "Vorschlag …", "unsicher": [],
             "aenderungen": [{"datei": "wissen/a.md", "aktion": "anhaengen", "neu": "x"}], "erfahrung": None}
        self.assertEqual(k.schema_fehler(a, self.schema), [])
        a["erfahrung"] = {"art": "Format", "was": "a", "warum": "b"}
        self.assertEqual(k.schema_fehler(a, self.schema), [])
        a["erfahrung"] = {"art": "Gefühl", "was": "a"}
        self.assertEqual(len(k.schema_fehler(a, self.schema)), 2)
        a["erfahrungsstand"] = "17"
        self.assertIn("$.erfahrungsstand: passt nicht zum Muster", k.schema_fehler(a, self.schema))

    def test_fehler(self):
        a = {"antwort": 3, "unsicher": "nein", "extra": 1,
             "aenderungen": [{"datei": "a", "aktion": "loeschen", "neu": "x"}]}
        f = " | ".join(k.schema_fehler(a, self.schema))
        for teil in ("regelstand", "erfahrungsstand", "unbekanntes Feld „extra“", "$.antwort", "$.unsicher", "nicht erlaubt"):
            self.assertIn(teil, f)


class Freigabe(unittest.TestCase):
    def test_faelle(self):
        frei = ["passt", "Passt!", "passt, danke", "Ok, passt so.", "Passt, bitte speichern",
                "Passt, bitte speichern und schließen", "passt so, danke dir", "passt!\n\nsieht gut aus",
                "> - Er hört gern Jazz.\n\npasst"]
        nicht = ["passt nicht", "passt noch nicht", "Passt, aber nimm 1998", "passt – und ergänze Hamburg",
                 "danke", "gut so", "Das passt nicht zu den Jahren"]
        for t in frei:
            self.assertTrue(k.freigabe(t)[0], t)
        for t in nicht:
            self.assertFalse(k.freigabe(t)[0], t)

    def test_gezeigt(self):
        vorher = "Vorschlag:\n```markdown\n## Musik\n- Er hört gern Jazz.\n```\nNichts geändert."
        bl = k.codebloecke(vorher)
        self.assertTrue(k.text_gezeigt("## Musik\n- Er hört gern  Jazz.", bl))
        self.assertTrue(k.text_gezeigt("- Er hört gern Jazz.", bl, kontext="## Musik"))
        self.assertFalse(k.text_gezeigt("- Er hört gern Jazz.", bl))  # Teilstück reicht nicht
        self.assertFalse(k.text_gezeigt("Jazz.", bl))
        self.assertFalse(k.text_gezeigt("- Er hört gern Jazz und Blues.", bl))
        self.assertFalse(k.text_gezeigt("", bl))

    def test_entfernte_zeilen(self):
        self.assertEqual(k.entfernte_zeilen("a\nb\nc", "a\nc"), ["b"])
        self.assertEqual(k.entfernte_zeilen("Satz alt.", "Satz alt."), [])


class Inhalt(unittest.TestCase):
    def test_marker(self):
        self.assertTrue(k.marker_offen("Gedicht ⟦Vorschlag: Rilke, 1902⟧"))
        self.assertEqual(k.marker_offen("ohne Marker"), [])

    def test_zahlen(self):
        belege = ["Ich habe das in meinen 20ern gelesen."]
        self.assertEqual(k.zahlen_ohne_beleg("Er las es in seinen 20ern.", belege), [])
        self.assertEqual(k.zahlen_ohne_beleg("Er las es in den 2000ern.", belege), ["2000"])
        self.assertEqual(k.zahlen_ohne_beleg("1. Punkt\n2. Punkt", []), [])

    def test_sperre(self):
        self.assertEqual(k.sperrtreffer("Mit Anna im Urlaub", ["anna", "Ben"]), ["anna"])
        self.assertEqual(k.sperrtreffer("Annabell", ["Anna"]), [])
        self.assertEqual(k.sperrtreffer("zwei Kontonummern", ["Kontonummer", "Kontonummer*"]), ["Kontonummer*"])
        iban = r"re:\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){3,7}(?:\s?[A-Z0-9]{1,3})?\b"
        self.assertEqual(k.sperrtreffer("Konto DE89 3704 0044 0532 0130 00 bitte", [iban]), [iban])
        self.assertEqual(k.sperrtreffer("Treffen am 13.10.2026 um 19 Uhr", [iban]), [])
        self.assertEqual(k.sperrtreffer("egal", ["re:(kaputt"]), ["re:(kaputt"])      # ungültiges Muster sperrt
        p = Path(tempfile.mkdtemp()) / "s.txt"
        p.write_text("# Kommentar\nAnna  # Nachbarin\nre:\\d{4}#x\n", encoding="utf-8")
        self.assertEqual(k.sperrliste_laden(p), ["Anna", "re:\\d{4}#x"])

    def test_behauptungen(self):
        self.assertTrue(k.behauptungen("Ich habe die Datei gespeichert und das Issue ist jetzt geschlossen."))
        self.assertEqual(k.behauptungen("Nach deinem „passt“ wird es gespeichert."), [])

    def test_dubletten(self):
        lang = "Er spielt seit vielen Jahren in einer festen Doppelkopf-Runde."
        self.assertTrue(k.dubletten("- " + lang, {"hobbys.md": "# Hobbys\n" + lang}))
        self.assertEqual(k.dubletten("kurz", {"a.md": "kurz"}), [])

    def test_fehlversuche(self):
        self.assertEqual(k.fehlversuche(["⚠️ Nicht gespeichert: x", "ok", "⚠️ Nicht gespeichert: y"], "⚠️ Nicht gespeichert"), 2)


class Schreiben(unittest.TestCase):
    def test_nachlesen(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d, "a.md")
            p.write_text("# T\nA\nB\n", encoding="utf-8")
            k.nachlesen(p, "B", anker="A")
            p.write_text("# T\nA\nB\nB\n", encoding="utf-8")
            with self.assertRaises(k.Abbruch):
                k.nachlesen(p, "")
            p.write_bytes("# T\nGrÃ¼ÃŸe\n".encode("utf-8"))
            with self.assertRaises(k.Abbruch):
                k.nachlesen(p, "")

    def test_anker(self):
        self.assertEqual(k.anker_zahl("a\nb\na", "a"), 2)
        self.assertEqual(k.anker_zahl("a", ""), 0)


class Zeit(unittest.TestCase):
    def test_zeitzone_statt_versatz(self):
        t = k.jetzt()
        self.assertRegex(t, r"\+0[12]:00$")

    def test_fusszeile(self):
        f = k.fusszeile(["wissen/a.md"], [], {"Commit": "abc1234", "Regelstand": "x"})
        self.assertIn("✅ Gespeichert: `wissen/a.md` (Commit abc1234 · Regelstand x)", f)
        self.assertIn("⚠️ Nicht gespeichert: kaputt", k.fusszeile([], ["kaputt"], {}))


class Laufprotokoll(unittest.TestCase):
    def test_zeile_anlegen_und_anhaengen(self):
        from datetime import datetime, timedelta
        from zoneinfo import ZoneInfo
        with tempfile.TemporaryDirectory() as d:
            p = Path(d, "protokoll.md")
            s = datetime(2026, 10, 28, 20, 47, 3, tzinfo=ZoneInfo("Europe/Berlin"))
            k.laufzeile(p, s, s + timedelta(seconds=12), "Kommentar (mensch)", "2026-10-28a", "ok", "Gespeichert: a.md")
            k.laufzeile(p, s, s + timedelta(minutes=5), "Kommentar | x", "2026-10-28a", "fehler", "Regeln\nnicht bestätigt")
            zeilen = p.read_text(encoding="utf-8").splitlines()
            self.assertEqual(zeilen[0], "# Laufprotokoll")
            self.assertIn("| 2026-10-28 20:47:03 CET (gemessen) | 12 s | Kommentar (mensch) | 2026-10-28a | ok | Gespeichert: a.md |", zeilen)
            self.assertEqual(zeilen[-1], "| 2026-10-28 20:47:03 CET (gemessen) | 5 min | Kommentar / x | 2026-10-28a | fehler | Regeln nicht bestätigt |")
            with self.assertRaises(ValueError):
                k.laufzeile(p, s, s, "x", "y", "vielleicht", "z")
            with self.assertRaises(ValueError):
                k.laufzeile(p, datetime(2026, 1, 1), datetime(2026, 1, 1), "x", "y", "ok", "z")   # ohne Zeitzone


class Erfahrungen(unittest.TestCase):
    def test_laden_pruefen_anhaengen(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d, "erfahrungen.md")
            self.assertEqual(k.erfahrungen_laden(p), ("", "E-000"))
            e = {"art": "Fehlervermeidung", "was": "Protokolle nennen den Ort nur in der Kopfzeile.",
                 "warum": "Beim Ergänzen fehlte der Ort, weil nur der Textteil gelesen wurde."}
            self.assertEqual(k.erfahrung_pruefen(e, "", []), [])
            self.assertEqual(k.erfahrung_anhaengen(p, e, "2026-10-28", "2026-10-28T20:47:03+01:00"), "E-001")
            text, stand = k.erfahrungen_laden(p)
            self.assertEqual(stand, "E-001")
            self.assertIn("E-001 · 2026-10-28 · Lauf 2026-10-28T20:47:03+01:00 · Art: Fehlervermeidung\nWas: Protokolle", text)
            self.assertIn("steht schon in den Erfahrungen", k.erfahrung_pruefen(e, text, []))
            kurz = {"art": "Format", "was": "Ort", "warum": "b"}                 # kurzes Wort irgendwo im Text ist kein Doppel
            self.assertEqual(k.erfahrung_pruefen(kurz, text, []), [])
            frei = "Freier Bestand: Der Abrufdienst schneidet JSON bei rund 4000 Zeichen ab, danach fehlt alles."
            lang = {"art": "Werkzeug", "was": "Der Abrufdienst schneidet JSON bei rund 4000 Zeichen ab", "warum": "x"}
            self.assertIn("steht schon in den Erfahrungen", k.erfahrung_pruefen(lang, frei, ["4000"]))
            e2 = {"art": "Werkzeug", "was": "Das Modell rundet auf 15 Minuten.", "warum": "So stand es im Kommentar."}
            self.assertTrue(any("Zahlen ohne Beleg" in f for f in k.erfahrung_pruefen(e2, text, ["kein Beleg"])))
            self.assertEqual(k.erfahrung_pruefen(e2, text, ["bitte auf 15 Minuten runden"]), [])
            self.assertEqual(k.erfahrung_anhaengen(p, e2, "2026-10-29", "x"), "E-002")
            self.assertEqual(k.erfahrungen_laden(p)[1], "E-002")
            self.assertTrue(k.erfahrungsstand_ok({"erfahrungsstand": "E-002"}, "E-002"))
            self.assertFalse(k.erfahrungsstand_ok({"erfahrungsstand": "E-001"}, "E-002"))
            for falsch in ({"art": "Gefühl", "was": "a", "warum": "b"}, {"art": "Format", "was": "", "warum": "b"},
                           {"art": "Format", "was": "zwei\nZeilen", "warum": "b"},
                           {"art": "Format", "was": "⟦Vorschlag: x⟧", "warum": "b"}, "kein Objekt"):
                self.assertTrue(k.erfahrung_pruefen(falsch, "", []), falsch)


if __name__ == "__main__":
    unittest.main()
