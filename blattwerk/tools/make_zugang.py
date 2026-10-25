#!/usr/bin/env python3
"""Erzeugt zugang.php (Passwort-Hash, Cookie-Schlüssel, GitHub-Schlüssel für Rückmeldungen)
aus den Umgebungsvariablen BW_PASSWORT und BW_GITHUB_TOKEN (optional) sowie den
Einstellungen BW_PFAD (z. B. /blattwerk/), BW_REPO (owner/repo für Rückmeldungen) und BW_BETREIBER.

Das Passwort selbst landet nirgends. Die Werte sind deterministisch, damit ein neuer Upload
die Anmeldung auf dem iPad nicht ungültig macht; erst ein neues Passwort meldet alle Geräte ab.
"""
import hashlib
import json
import hmac
import os
import re
import sys
from pathlib import Path


def php_str(s: str) -> str:
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def php_array(d: dict) -> str:
    return "[" + ", ".join(f"{php_str(k)} => {php_str(v)}" for k, v in d.items()) + "]"


def einstellungen() -> dict:
    pfad = os.environ.get("BW_PFAD", "/blattwerk/").strip() or "/blattwerk/"
    if not re.fullmatch(r"/[A-Za-z0-9_\-/]*/", pfad):
        sys.exit("BW_PFAD muss mit / beginnen und enden, z. B. /blattwerk/")
    repo = os.environ.get("BW_REPO", "").strip()
    if repo and not re.fullmatch(r"[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+", repo):
        sys.exit("BW_REPO bitte als owner/repo angeben.")
    return {"pfad": pfad, "repo": repo, "betreiber": os.environ.get("BW_BETREIBER", "dem Betreiber").strip()[:60]}


def main() -> None:
    pw = os.environ.get("BW_PASSWORT", "")
    if len(pw) < 8:
        sys.exit("BW_PASSWORT fehlt oder ist kürzer als 8 Zeichen.")
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "zugang.php")
    salt = hashlib.sha256((pw + "|blattwerk-salz").encode()).hexdigest()[:32]
    pw_hash = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt.encode(), 100000, dklen=32).hex()
    key = hmac.new(pw.encode(), b"blattwerk-cookie", hashlib.sha256).hexdigest()
    gh = os.environ.get("BW_GITHUB_TOKEN", "").strip()
    if gh and not re.fullmatch(r"[A-Za-z0-9_]+", gh):
        sys.exit("BW_GITHUB_TOKEN enthält unerwartete Zeichen.")
    out.write_text(
        "<?php\n// automatisch erzeugt beim Upload – nicht bearbeiten\n"
        f"return ['salt' => '{salt}', 'hash' => '{pw_hash}', 'key' => '{key}', 'gh' => '{gh}',\n"
        f"  'einstellungen' => {php_array(einstellungen())}];\n",
        encoding="utf-8",
    )
    print("zugang.php geschrieben")


if __name__ == "__main__":
    main()
