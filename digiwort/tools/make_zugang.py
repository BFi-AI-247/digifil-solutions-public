#!/usr/bin/env python3
"""Erzeugt zugang.php für Rückmeldungen aus DW_GITHUB_TOKEN (Schlüssel) und DW_REPO (owner/repo).
Die Datei liegt auf dem Server außerhalb des Web-Ordners (<privat>/digiwort/), also nicht abrufbar."""
import os
import re
import sys
from pathlib import Path

gh = os.environ.get("DW_GITHUB_TOKEN", "").strip()
if gh and not re.fullmatch(r"[A-Za-z0-9_]+", gh):
    sys.exit("DW_GITHUB_TOKEN enthält unerwartete Zeichen.")
repo = os.environ.get("DW_REPO", "").strip()
if repo and not re.fullmatch(r"[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+", repo):
    sys.exit("DW_REPO bitte als owner/repo angeben.")
out = Path(sys.argv[1] if len(sys.argv) > 1 else "zugang.php")
out.write_text("<?php\n// automatisch erzeugt beim Upload – nicht bearbeiten\n" f"return ['gh' => '{gh}', 'repo' => '{repo}'];\n", encoding="utf-8")
print("zugang.php geschrieben" + ("" if gh and repo else " (ohne Schlüssel oder Repo – Rückmeldungen aus)"))
