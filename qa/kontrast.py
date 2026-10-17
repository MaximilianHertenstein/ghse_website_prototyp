#!/usr/bin/env python3
"""WCAG-2.2-Kontrastprüfung der Farb-Tokens aus static/css/main.css (Hell + Dunkel)."""


def lum(hexfarbe):
    h = hexfarbe.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]

    def f(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def cr(a, b):
    la, lb = lum(a), lum(b)
    return round((max(la, lb) + 0.05) / (min(la, lb) + 0.05), 2)


hell = {
    "schrift": "#101736", "grau": "#4c5063", "orange": "#bf4712",
    "link": "#141c4e", "rand": "#101736", "papier": "#fbfaf6",
    "flaeche": "#ffffff", "gelb": "#ffd400", "nacht": "#141c4e",
}
dunkel = {
    "schrift": "#f2f4fc", "grau": "#aab1cf", "orange": "#ff9d70",
    "link": "#ffd400", "rand": "#e8ebfa", "papier": "#10153a",
    "flaeche": "#1c2455", "gelb": "#ffd400", "nacht": "#0a0e28",
}

paare = [
    ("schrift auf papier", "schrift", "papier", 4.5),
    ("schrift auf flaeche", "schrift", "flaeche", 4.5),
    ("grau auf papier", "grau", "papier", 4.5),
    ("grau auf flaeche", "grau", "flaeche", 4.5),
    ("orange-tief auf papier (Kicker)", "orange", "papier", 4.5),
    ("orange-tief auf flaeche (Kicker)", "orange", "flaeche", 4.5),
    ("link auf papier", "link", "papier", 4.5),
    ("link auf flaeche", "link", "flaeche", 4.5),
    ("rand auf papier (Grafik 3:1)", "rand", "papier", 3.0),
    ("rand auf flaeche (Grafik 3:1)", "rand", "flaeche", 3.0),
    ("gelb auf nacht (Grafik 3:1)", "gelb", "nacht", 3.0),
    ("tinte auf gelb (Chip-Text)", "#101736", "gelb", 4.5),
    ("weiss auf nacht (Bänder)", "#ffffff", "nacht", 4.5),
]

sonder = {
    "HELL": [
        ("hero__unter #dfe3f5 auf nacht", "#dfe3f5", "#141c4e", 4.5),
        ("fuss-text #e6e9f7 auf nacht", "#e6e9f7", "#141c4e", 4.5),
        ("fuss-hinweis #b9bed6 auf tinte", "#b9bed6", "#101736", 4.5),
        ("hinweis tinte auf #fffbe6", "#101736", "#fffbe6", 4.5),
        ("warnung tinte auf #ffe9e6", "#101736", "#ffe9e6", 4.5),
    ],
    "DUNKEL": [
        ("hero__unter #dfe3f5 auf nacht", "#dfe3f5", "#0a0e28", 4.5),
        ("fuss-text #e6e9f7 auf nacht", "#e6e9f7", "#0a0e28", 4.5),
        ("fuss-hinweis #b9bed6 auf schatten-farbe", "#b9bed6", "#05071a", 4.5),
        ("hinweis tinte auf #fffbe6", "#101736", "#fffbe6", 4.5),
        ("warnung tinte auf #ffe9e6", "#101736", "#ffe9e6", 4.5),
        ("strong-Marker: schrift auf flaeche+35%gelb",
         "#f2f4fc", "#6b6237", 3.0),
    ],
}

fehler = 0
for name, t in (("HELL", hell), ("DUNKEL", dunkel)):
    print(f"--- {name} ---")
    for label, fg, bg, mindest in paare:
        a = t.get(fg, fg)
        b = t.get(bg, bg)
        wert = cr(a, b)
        ok = wert >= mindest
        fehler += 0 if ok else 1
        print(f'{"OK  " if ok else "FAIL"} {label}: {wert} (min {mindest})')
    for label, a, b, mindest in sonder[name]:
        wert = cr(a, b)
        ok = wert >= mindest
        fehler += 0 if ok else 1
        print(f'{"OK  " if ok else "FAIL"} {label}: {wert} (min {mindest})')

print("Fehler gesamt:", fehler)
raise SystemExit(1 if fehler else 0)
