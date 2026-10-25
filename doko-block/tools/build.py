#!/usr/bin/env python3
"""Baut dist/index.html und dist/verlauf.html (gemeinsames CSS/JS eingesetzt)."""
from pathlib import Path
hier = Path(__file__).resolve().parent.parent
css = (hier / "src/basis.css").read_text(encoding="utf-8")
js = (hier / "src/basis.js").read_text(encoding="utf-8")
xl = (hier / "src/xlsx.js").read_text(encoding="utf-8")
(hier / "dist").mkdir(exist_ok=True)
for name in ["index.html", "verlauf.html"]:
    t = (hier / "src" / name).read_text(encoding="utf-8")
    assert "/*BASIS_CSS*/" in t and "/*BASIS_JS*/" in t, name
    (hier / "dist" / name).write_text(t.replace("/*BASIS_CSS*/", css).replace("/*BASIS_JS*/", js).replace("/*XLSX_JS*/", xl), encoding="utf-8")
print("gebaut: dist/index.html, dist/verlauf.html")
