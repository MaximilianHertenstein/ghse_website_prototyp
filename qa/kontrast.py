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
    "papier2": "#f1efe6",
}
dunkel = {
    "schrift": "#f2f4fc", "grau": "#aab1cf", "orange": "#ff9d70",
    "link": "#ffd400", "rand": "#e8ebfa", "papier": "#10153a",
    "flaeche": "#1c2455", "gelb": "#ffd400", "nacht": "#0a0e28",
    "papier2": "#171d49",
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
    # Kategoriefarbe der Teilzeitschularten (gemeinsam in Hell und Dunkel,
    # weil die Fläche in beiden Modi Tinte-Schrift behält).
    ("tinte auf teilzeit-orange (Chip-Text)", "#101736", "#ee6a2b", 4.5),
    ("weiss auf teilzeit-orange (Grafik 3:1)", "#ffffff", "#ee6a2b", 3.0),
    # Zitatblöcke stehen auf --papier2 (blockquote, .fliesstext) und erben die
    # Fließtextfarbe. Die Fläche war bislang in keinem Paar erfasst.
    ("blockquote: schrift auf papier2 (Zitat)", "schrift", "papier2", 4.5),
]

# Überblendung: Textfarbe auf einem Band liegt nicht direkt auf dem Token,
# sondern auf der überdeckten Fläche – deshalb wird hier verrechnet.
def mischen(grund, deck, anteil):
    g, d = grund.lstrip("#"), deck.lstrip("#")
    werte = [round(int(g[i:i + 2], 16) * (1 - anteil) + int(d[i:i + 2], 16) * anteil)
             for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(werte)


# Sekundärtext auf Nacht-Bändern (rgba(255,255,255,.85) in main.css) für beide
# Nacht-Hintergründe: hell (#141c4e) und dunkel (#0a0e28).
def weiss_auf_nacht(nacht_hex, anteil=0.85):
    return mischen(nacht_hex, "#ffffff", anteil)


sonder = {
    "HELL": [
        ("hero__unter #dfe3f5 auf nacht", "#dfe3f5", "#141c4e", 4.5),
        ("fuss-text #e6e9f7 auf nacht", "#e6e9f7", "#141c4e", 4.5),
        ("fuss-hinweis #b9bed6 auf tinte", "#b9bed6", "#101736", 4.5),
        ("band--nacht Sekundärtext (Einleitung, hinweiszeile)",
         weiss_auf_nacht("#141c4e"), "#141c4e", 4.5),
        ("hinweis schrift auf hinweis-flaeche", "#101736", "#fffbe6", 4.5),
        ("warnung schrift auf warn-flaeche", "#101736", "#ffe9e6", 4.5),
        ("warn-rand auf warn-flaeche (Grafik 3:1)", "#bf4712", "#ffe9e6", 3.0),
        # Marker hinter fett gesetztem Fließtext (rgba(255,212,0,.75) über der
        # Seitengrundfläche). Wurde bisher nur im Dunkelmodus geprüft.
        ("strong-Marker: schrift auf papier+75%gelb",
         "#101736", mischen("#fbfaf6", "#ffd400", 0.75), 4.5),
    ],
    "DUNKEL": [
        ("hero__unter #dfe3f5 auf nacht", "#dfe3f5", "#0a0e28", 4.5),
        ("fuss-text #e6e9f7 auf nacht", "#e6e9f7", "#0a0e28", 4.5),
        ("fuss-hinweis #b9bed6 auf schatten-farbe", "#b9bed6", "#05071a", 4.5),
        ("band--nacht Sekundärtext (Einleitung, hinweiszeile)",
         weiss_auf_nacht("#0a0e28"), "#0a0e28", 4.5),
        ("hinweis schrift auf hinweis-flaeche", "#f2f4fc", "#33311a", 4.5),
        ("warnung schrift auf warn-flaeche", "#f2f4fc", "#3b2016", 4.5),
        ("warn-rand auf warn-flaeche (Grafik 3:1)", "#ff9d70", "#3b2016", 3.0),
        # Schwellwert 4.5 statt 3.0: der Marker hinterläuft normal großen
        # Fließtext (1.09rem/800), der nach WCAG 2.2 Text und nicht Grafik ist.
        ("strong-Marker: schrift auf flaeche+35%gelb",
         "#f2f4fc", "#6b6237", 4.5),
    ],
}

# Streifenmuster: die Fläche unter den Diagonalstreifen wird zur Hälfte
# geprüft, denn Text steht abwechselnd auf Papier und auf Streifen.
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
    # Gestreiftes Band: Text steht abwechselnd auf Papier und auf Streifen,
    # deshalb die streifenbedeckte Hälfte der Fläche als eigene Paare.
    # Der Kicker fehlt absichtlich: .band--gestreift .kicker liegt auf einer
    # deckenden Papierfläche (siehe main.css), sonst fiele er selbst bei
    # schwachen Streifen unter 4,5:1. Wer die Regel dort entfernt, verschiebt
    # genau dieses Paar – es ist mit .kicker auf Papier bereits geprüft.
    streif = mischen(t["papier"], "#101736" if name == "HELL" else "#ffffff", 0.08)
    for label, fg, mindest in (
        ("schrift auf gestreifter Fläche", "schrift", 4.5),
        ("grau auf gestreifter Fläche (Einleitung)", "grau", 4.5),
    ):
        wert = cr(t[fg], streif)
        ok = wert >= mindest
        fehler += 0 if ok else 1
        print(f'{"OK  " if ok else "FAIL"} {label}: {wert} (min {mindest})')

print("Fehler gesamt:", fehler)
raise SystemExit(1 if fehler else 0)
