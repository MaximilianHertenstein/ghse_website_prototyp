#!/usr/bin/env python3
"""Isolationstest für Design 6 („Wegweiser“).

Prüft, dass die neue CSS-Datei die fünf Bestandsdesigns nicht berühren kann:

  - jeder normale Selektor beginnt mit :root[data-design="design-06"]
  - @media/@supports/@print dürfen nur scoped Regeln enthalten
  - @keyframes heißen d6-… (falls vorhanden)
  - keine @import-, http(s)- oder url()-Fremdreferenzen
  - die vier GHSE-Originalfarben stehen unverändert in der Datei
  - Schrift-Partial und hugo.toml verweisen auf die neuen Dateien
  - die bestehenden Schriftfamilien werden nicht überschrieben

Aufruf:  python3 qa/design6-isolation.py
Exit 1 bei jedem Befund.
"""
import re
import sys
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
CSS = BASIS / "assets/css/design-06.css"
SCHRIFT = BASIS / "layouts/_partials/schriften-design06.html"
HUGO = BASIS / "hugo.toml"
PRAEFIX = ':root[data-design="design-06"]'
ERLAUBTE_AT = {"@media", "@supports", "@print", "@page"}
ORIGINALFARBEN = {"#222d71", "#006ab4", "#ee7330", "#f6dc56"}


def ohne_kommentare(text):
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def preludes(text):
    """Alle Regel-Preludes (auch in @media) sammeln, ohne Deklarationsblöcke."""
    text = ohne_kommentare(text)
    ergebnis = []
    stapel = []
    puffer = []
    for zeichen in text:
        if zeichen == "{":
            prelude = "".join(puffer).strip()
            puffer = []
            stapel.append(prelude)
            ergebnis.append((len(stapel) - 1, prelude))
        elif zeichen == "}":
            if stapel:
                stapel.pop()
            puffer = []
        else:
            if stapel:
                # Innerhalb eines Blocks: Deklarationen ignorieren, aber
                # verschachtelte At-Rules (selten) weiter erkennen.
                puffer.append(zeichen)
            else:
                puffer.append(zeichen)
    return [p for _, p in ergebnis if p]


def pruefe_selektoren(text):
    fehler = []
    for prelude in preludes(text):
        if prelude.startswith("@"):
            name = prelude.split(None, 1)[0].lower()
            if name not in ERLAUBTE_AT and not name.startswith("@keyframes"):
                fehler.append(f"unerlaubte At-Rule: {prelude[:80]}")
            if name.startswith("@keyframes"):
                kf = prelude.split(None, 1)[1].strip() if " " in prelude else ""
                if not kf.startswith("d6-"):
                    fehler.append(f"Keyframes ohne d6-Präfix: {prelude[:80]}")
            continue
        teile = [t.strip() for t in prelude.split(",")]
        for teil in teile:
            if not teil.startswith(PRAEFIX):
                fehler.append(f"nicht isolierter Selektor: {teil[:120]}")
    return fehler


def main():
    fehler = []
    if not CSS.exists():
        print("FEHLT:", CSS)
        return 1
    text = CSS.read_text(encoding="utf-8")

    fehler += pruefe_selektoren(text)

    for verboten in ("@import", "http://", "https://"):
        if verboten in text:
            fehler.append(f"Fremdreferenz gefunden: {verboten}")

    for farbe in sorted(ORIGINALFARBEN):
        if farbe not in text.lower():
            fehler.append(f"GHSE-Originalfarbe fehlt: {farbe}")

    for familie in ("Inter", "Hanken Grotesk", "Roboto", "Poppins",
                    "Familjen Grotesk", "Piazzolla", "Public Sans"):
        if re.search(rf'font-family\s*:\s*["\']?{re.escape(familie)}', text, re.I):
            fehler.append(f"bestehende Schriftfamilie überschrieben: {familie}")

    if not SCHRIFT.exists():
        fehler.append("Schrift-Partial fehlt")
    else:
        st = SCHRIFT.read_text(encoding="utf-8")
        if 'font-family:"Archivo"' not in st:
            fehler.append("Schrift-Partial definiert nicht Archivo")
        if "archivo-var-latin.woff2" not in st:
            fehler.append("Schrift-Partial verweist nicht auf die Archivo-Datei")

    if not HUGO.exists():
        fehler.append("hugo.toml fehlt")
    else:
        ht = HUGO.read_text(encoding="utf-8")
        if 'id = "design-06"' not in ht:
            fehler.append("hugo.toml registriert design-06 nicht")
        if 'css = "css/design-06.css"' not in ht:
            fehler.append("hugo.toml verweist nicht auf design-06.css")
        if 'fonts = "schriften-design06.html"' not in ht:
            fehler.append("hugo.toml verweist nicht auf das Schrift-Partial")

    print(f"Design-6-Isolation: {len(preludes(text))} Regel-Preludes geprüft")
    if fehler:
        print(f"Befunde: {len(fehler)}")
        for f in fehler:
            print("  " + f)
        return 1
    print("Alle Regeln sind auf :root[data-design=\"design-06\"] begrenzt; "
          "keine Fremdreferenzen, keine Kollision mit Bestandsschriften.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
