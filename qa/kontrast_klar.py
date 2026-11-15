#!/usr/bin/env python3
"""Kontrastprüfung der Variante „klar“ (assets/css/klar.css).

Ergänzt qa/kontrast.py, das nur main.css liest. Geprüft wird, was klar.css
selbst festlegt:
  1. Der dunkle Satz (Media-Query und data-theme) ist in beiden Formen
     identisch – wie in main.css.
  2. Der dunkle Satz setzt jedes Farb-Token, das der helle setzt, und jedes,
     das main.css im Dunkeln setzt; sonst schiene der dunkle Satz aus
     main.css durch (Pflegehinweis im Kopf von klar.css).
  3. Alle Text-Paare erreichen 7:1 (AAA), Rahmen 3:1.

Aufruf:  python3 qa/kontrast_klar.py     (aus dem Repository-Stammverzeichnis)
"""

import re
import sys
from pathlib import Path

CSS = Path(__file__).resolve().parent.parent / "assets" / "css"
klar = (CSS / "klar.css").read_text(encoding="utf-8")
haupt = (CSS / "main.css").read_text(encoding="utf-8")


def block(text, kopf):
    i = text.index(kopf)
    j = text.index("{", i)
    tief, k = 1, j + 1
    while tief:
        tief += {"{": 1, "}": -1}.get(text[k], 0)
        k += 1
    return text[j + 1:k - 1]


def tokens(körper):
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"--([\w-]+):\s*([^;]+);", körper)}


P = ':root[data-design="klar"]'
hell = tokens(block(klar, P + " {"))
dunkel_media = tokens(block(block(klar, "@media (prefers-color-scheme: dark)"), P + ":not("))
dunkel_attr = tokens(block(klar, P + '[data-theme="dark"]'))
basis = tokens(block(haupt, ":root {"))

fehler = []
if dunkel_media != dunkel_attr:
    fehler.append("Dunkel-Satz in @media und [data-theme=dark] ist nicht identisch: "
                  + ", ".join(sorted(set(dunkel_media) ^ set(dunkel_attr) | {k for k in dunkel_media if dunkel_media.get(k) != dunkel_attr.get(k)})))

PRAEFIXE = ("papier", "papier2", "schrift", "grau", "rand", "orange", "link", "haarlinie", "marker", "hinweis",
            "warn", "fuss", "primaer", "aktion", "text", "flaeche", "erfolg", "warnung", "fehler", "linie",
            "schatten-farbe", "blau", "gelb", "tinte", "kategorie", "wert")
FARBEN = {k for k in hell if any(k == p or k.startswith(p + "-") for p in PRAEFIXE)}
fehlt = sorted(FARBEN - set(dunkel_attr))
if fehlt:
    fehler.append("im dunklen Satz fehlen Tokens des hellen Satzes: " + ", ".join(fehlt))


haupt_dunkel = tokens(block(haupt, ':root[data-theme="dark"] {'))
offen = sorted(set(haupt_dunkel) - set(dunkel_attr))
if offen:
    fehler.append("main.css setzt im dunklen Satz, klar.css nicht: " + ", ".join(offen))


def wert(satz, name, tiefe=0):
    v = satz.get(name) or basis.get(name)
    m = re.fullmatch(r"var\(--([\w-]+)\)", v or "")
    if m and tiefe < 8:
        return wert(satz, m.group(1), tiefe + 1)
    return v


def lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def verhältnis(a, b):
    x, y = sorted((lum(a), lum(b)), reverse=True)
    return (x + 0.05) / (y + 0.05)


# (Vordergrund, Hintergrund, Mindestwert). Text 7:1 (AAA), Linien und Icons 3:1.
PAARE = [
    ("schrift", "papier", 7), ("schrift", "papier2", 7), ("schrift", "flaeche", 7),
    ("grau", "papier", 7), ("grau", "papier2", 7), ("grau", "flaeche", 7),
    ("link", "papier", 7), ("link", "papier2", 7), ("link", "flaeche", 7),
    ("orange-tief", "papier", 4.5), ("orange-tief", "papier2", 4.5),
    ("rand", "papier", 3), ("rand", "flaeche", 3), ("primaer-akzent", "papier", 3),
    ("aktion-schrift", "aktion", 7), ("aktion", "papier", 3),
    ("weiss", "blau", 7), ("tinte", "gelb", 7),
    ("schrift", "hinweis-flaeche", 7), ("link", "hinweis-flaeche", 7), ("hinweis-rand", "hinweis-flaeche", 3),
    ("schrift", "warn-flaeche", 7), ("warn-rand", "warn-flaeche", 3),
    ("erfolg", "papier", 7), ("warnung", "papier", 7), ("fehler", "papier", 7),
    ("fuss-schrift", "fuss-flaeche", 7), ("fuss-link", "fuss-flaeche", 7),
    ("fuss-titel", "fuss-flaeche", 7), ("fuss-leiste-schrift", "fuss-leiste-flaeche", 7),
    ("orange-tief", "fuss-flaeche", 4.5),
]

for modus, satz in (("hell", {**basis, **hell}), ("dunkel", {**basis, **dunkel_attr})):
    kleinster = 99
    for fg, bg, soll in PAARE:
        a, b = wert(satz, fg), wert(satz, bg)
        if not (a and b and a.startswith("#") and b.startswith("#")):
            fehler.append(f"{modus}: {fg}/{bg} nicht auflösbar ({a} / {b})")
            continue
        v = verhältnis(a, b)
        kleinster = min(kleinster, v / soll * 7)
        if v < soll:
            fehler.append(f"{modus}: {fg} auf {bg} = {v:.2f}:1, verlangt {soll}:1")
    print(f"{modus}: {len(PAARE)} Paare geprüft")

if fehler:
    print("\nFEHLER:\n  " + "\n  ".join(fehler))
    sys.exit(1)
print("klar.css: alle Kontrastpaare bestehen, beide Dunkel-Sätze sind identisch und vollständig.")
