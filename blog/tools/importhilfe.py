"""Gemeinsame Helfer für die Import-Werkzeuge: Laden, HTML → Markdown, Bilder holen, Kennungen.

Läuft im GitHub-Workflow „Blog Import“ (dort gibt es freies Netz), lokal im Test mit Dateien statt Adressen.
Benötigt: beautifulsoup4, markdownify
"""
import hashlib, json, re, sys, urllib.parse, urllib.request
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
from markdownify import markdownify

AGENT = "Mozilla/5.0 (compatible; Blog-Import; einmaliger Umzug eigener Beiträge)"


def hole(adresse, roh=False):
    """Adresse oder lokale Datei (file:// oder Pfad) laden."""
    if not re.match(r"https?://", adresse):
        p = Path(adresse.removeprefix("file://"))
        return p.read_bytes() if roh else p.read_text(encoding="utf-8")
    req = urllib.request.Request(adresse, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(req, timeout=40) as r:
        d = r.read()
    return d if roh else d.decode("utf-8", "replace")


def slug(s, laenge=80):
    s = s.lower()
    for a, b in {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "é": "e", "è": "e", "á": "a", "à": "a", "ó": "o", "í": "i", "ñ": "n", "ç": "c"}.items():
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s[:laenge].strip("-") or "beitrag"


def de_stand(titel, text):
    """Gleiche Prüfsumme wie de_stand() in server/lib.php"""
    return hashlib.sha1((titel + "\n" + text).encode("utf-8")).hexdigest()[:12]


def bild_gross(url):
    """Blogger-Bildadressen auf eine große Fassung umstellen (s1600 bzw. =s1600)."""
    if "blogger.googleusercontent.com" in url or "bp.blogspot.com" in url:
        url = re.sub(r"/s\d{2,4}(-[a-z0-9-]+)?/", "/s1600/", url)
        url = re.sub(r"=(w\d+-h\d+|s\d+)[^/?#]*$", "=s1600", url)
        url = re.sub(r"/w\d+-h\d+(-[a-z0-9-]+)?/", "/s1600/", url)
    return url


def html_zu_markdown(html, basis, beitrag_id, bilder_ordner, bilder_pfad, bericht):
    """Wandelt Blog-HTML in einfaches Markdown. Bilder werden heruntergeladen und lokal verlinkt."""
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    for t in soup.find_all(["iframe", "embed", "object", "video"]):
        src = t.get("src") or t.get("data") or ""
        if src:
            src = urllib.parse.urljoin(basis, src)
            p = soup.new_tag("p"); a = soup.new_tag("a", href=src); a.string = "Eingebettetes Video/Inhalt: " + src
            p.append(a); t.replace_with(p)
        else:
            t.decompose()
    # Bilder: Link um das Bild entfernen (zeigt bei Blogger nur auf die große Fassung), Bild holen
    nr = 0
    for img in soup.find_all("img"):
        src = img.get("src") or ""
        if not src:
            img.decompose(); continue
        eltern = img.parent
        if eltern and eltern.name == "a" and len(eltern.find_all(True)) == 1:
            ziel = eltern.get("href") or ""
            if re.search(r"\.(jpe?g|png|gif|webp)(\?|$)", ziel, re.I) or "googleusercontent" in ziel or "bp.blogspot" in ziel:
                src = ziel or src
            eltern.replace_with(img)
        url = bild_gross(urllib.parse.urljoin(basis, src))
        nr += 1
        try:
            daten = hole(url, roh=True)
            endung = {b"\xff\xd8": "jpg", b"\x89P": "png", b"GI": "gif", b"RI": "webp"}.get(daten[:2], "jpg")
            name = f"{beitrag_id}-{nr}.{endung}"
            (bilder_ordner / name).write_bytes(daten)
            img["src"] = f"{bilder_pfad}/{name}"
            bericht.append(f"    Bild übernommen: {name} ({len(daten) // 1024} KB)")
        except Exception as e:  # Bild bleibt als Link stehen
            bericht.append(f"    ⚠ Bild nicht geladen ({e.__class__.__name__}): {url}")
            a = soup.new_tag("a", href=url); a.string = img.get("alt") or "Bild"
            img.replace_with(a)
    # Links absolut machen, kaputte Links (about:invalid, javascript:) zu Text
    for a in soup.find_all("a"):
        h = (a.get("href") or "").strip()
        if not h or re.match(r"(about|javascript|data):", h, re.I):
            a.unwrap(); continue
        if not h.startswith("beitrag:"):
            a["href"] = urllib.parse.urljoin(basis, h)
    # Blogger-Eigenheiten: <div> als Absatz, doppelte <br> als Absatzwechsel
    for d in soup.find_all("div"):
        if not d.find(["p", "div", "ul", "ol", "table", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6"]):
            d.name = "p"
        else:
            d.unwrap()
    for s in soup.find_all(["span", "font", "u"]):
        s.unwrap()
    # Zeilenumbrüche im Quelltext sind keine Absätze: Leerraum in Texten zusammenfassen (außer in <pre>)
    for t in soup.find_all(string=True):
        if not t.find_parent("pre") and "\n" in t:
            t.replace_with(re.sub(r"\s+", " ", str(t)))
    md = markdownify(str(soup), heading_style="ATX", bullets="-", strip=["table"], escape_underscores=False, escape_asterisks=False)
    md = md.replace(" ", " ")
    md = re.sub(r"[ \t]+\n", lambda m: "  \n" if m.group(0).startswith("  ") else "\n", md)
    md = re.sub(r"(  \n){2,}", "\n\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"^#\s", "## ", md, flags=re.M)  # Haupttitel gibt es nur einmal (der Beitragstitel)
    return md.strip()


def berlin(iso):
    """Zeitpunkt einheitlich in Europe/Berlin (ISO 8601), damit Sortieren über Quellen hinweg stimmt."""
    from datetime import datetime
    from zoneinfo import ZoneInfo
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(ZoneInfo("Europe/Berlin")).replace(microsecond=0).isoformat()


def lade_json(p, vorgabe):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else vorgabe


def schreibe_json(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def alte_uebersetzung(ziel, b):
    """Übersetzung aus einem früheren Import übernehmen, wenn sich der deutsche Text nicht geändert hat."""
    alt = ziel / "beitraege" / (b["id"] + ".json")
    if alt.exists():
        a = json.loads(alt.read_text(encoding="utf-8"))
        if a.get("en", {}).get("stand") == de_stand(b["titel"], b["text"]):
            return a["en"]
    return {"titel": "", "text": "", "geprueft": False, "stand": ""}


def stopp(text):
    print("Import abgebrochen:", text, file=sys.stderr); sys.exit(1)
