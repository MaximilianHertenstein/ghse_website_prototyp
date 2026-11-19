#!/usr/bin/env python3
"""Isolationstest für „Neo Ruhig“ (neo-ruhig).

Die Variante ist bewusst eine reine Begradigung von Neobrutalismus:

  - jeder Selektor beginnt mit :root[data-design="neo-ruhig"]
  - die einzige Deklaration ist `transform: none`
  - keine Drehung, keine Neigung, keine Fremdreferenz
  - keine Farb-, Schatten- oder Schriftänderung
  - hugo.toml registriert die Variante und ihre CSS-Datei

Aufruf:  python3 qa/neo-ruhig-isolation.py
Exit 1 bei jedem Befund.
"""
import re
import sys
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
CSS = BASIS / "assets/css/neo-ruhig.css"
HUGO = BASIS / "hugo.toml"
PRAEFIX = ':root[data-design="neo-ruhig"]'


def ohne_kommentare(text):
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def regeln(text):
    """Alle einfachen Regeln als (Selektor, Deklarationen) sammeln."""
    text = ohne_kommentare(text)
    return [(m.group(1).strip(), m.group(2).strip())
            for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", text)]


def preludes(text):
    return [selektor for selektor, _ in regeln(text)]


def main():
    fehler = []
    if not CSS.exists():
        print("FEHLT:", CSS)
        return 1
    text = CSS.read_text(encoding="utf-8")

    for prelude in preludes(text):
        if prelude.startswith("@"):
            fehler.append(f"unerlaubte At-Rule: {prelude[:80]}")
            continue
        for teil in [t.strip() for t in prelude.split(",")]:
            if not teil.startswith(PRAEFIX):
                fehler.append(f"nicht isolierter Selektor: {teil[:120]}")

    for block in re.findall(r"\{([^}]*)\}", ohne_kommentare(text)):
        for deklaration in block.split(";"):
            deklaration = deklaration.strip()
            if deklaration and deklaration != "transform: none":
                fehler.append(f"unerlaubte Deklaration: {deklaration}")

    for verboten in ("@import", "http://", "https://", "rotate(", "skew("):
        if verboten in text:
            fehler.append(f"Fremdreferenz oder Schräglage gefunden: {verboten}")

    if not HUGO.exists():
        fehler.append("hugo.toml fehlt")
    else:
        ht = HUGO.read_text(encoding="utf-8")
        if 'id = "neo-ruhig"' not in ht:
            fehler.append("hugo.toml registriert neo-ruhig nicht")
        if 'css = "css/neo-ruhig.css"' not in ht:
            fehler.append("hugo.toml verweist nicht auf neo-ruhig.css")

    print(f"Neo-Ruhig-Isolation: {len(preludes(text))} Regel-Preludes geprüft")
    if fehler:
        print(f"Befunde: {len(fehler)}")
        for f in fehler:
            print("  " + f)
        return 1
    print("Alle Regeln sind auf :root[data-design=\"neo-ruhig\"] begrenzt "
          "und begradigen ausschließlich (transform: none).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
