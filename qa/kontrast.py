#!/usr/bin/env python3
"""WCAG-2.2-Kontrastprüfung der Farb-Tokens aus static/css/main.css.

Das Skript liest die Tokens direkt aus dem Stylesheet – der helle Satz aus
`:root`, der dunkle aus `@media (prefers-color-scheme: dark)` und aus
`:root[data-theme="dark"]` (beide müssen identisch sein, sonst Fehler).
Dadurch kann die Prüfung nicht mehr neben dem Stylesheet stehen.

Geprüft werden die Paare, die die Bausteine wirklich verwenden (Kicker,
Links, Menü-Marke, Chips, Hinweise, Warnungen, Marker hinter fettem Text).
Verweis: README Abschnitt „Farbmodus“, qa/layout.py für die Measure-Seite.

Aufruf:  python3 qa/kontrast.py     (aus dem Repository-Stammverzeichnis)
"""

import re
import sys
from pathlib import Path

STYLESHEET = Path(__file__).resolve().parent.parent / "static" / "css" / "main.css"


def regeln(css):
    """(Selektor, Deklarationsblock) von oben nach unten, @media gefaltet."""
    ausgabe = []
    stapel = [("", css)]
    while stapel:
        kontext, quelle = stapel.pop(0)
        offen = quelle.find("{")
        while offen >= 0:
            selektor = re.sub(r"/\*.*?\*/", "", quelle[:offen], flags=re.S).strip()
            tief = 1
            i = offen + 1
            while i < len(quelle) and tief:
                if quelle[i] == "{":
                    tief += 1
                elif quelle[i] == "}":
                    tief -= 1
                i += 1
            körper = quelle[offen + 1:i - 1]
            if selektor.startswith("@media"):
                stapel.append((kontext + selektor, körper))
            else:
                ausgabe.append((kontext, selektor, körper.strip()))
            quelle = quelle[i:]
            offen = quelle.find("{")
    return ausgabe


def tokens(körper):
    out = {}
    for m in re.finditer(r"--([\w-]+):\s*([^;]+);", körper):
        out[m.group(1)] = m.group(2).strip()
    return out


def auflösen(wert, satz, gesehen=None):
    """var(--x) und var(--x, Ersatzwert) durch die Tokenwerte ersetzen."""
    gesehen = gesehen or set()
    m = re.fullmatch(r"var\(\s*--([\w-]+)\s*(?:,\s*([^)]+)\s*)?\)", wert)
    if not m:
        return wert
    name, ersatz = m.groups()
    if name in gesehen:
        raise SystemExit(f"Zirkuläre Referenz bei --{name}")
    if name in satz:
        return auflösen(satz[name], satz, gesehen | {name})
    return ersatz.strip() if ersatz else wert


def lum(farbe):
    h = farbe.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]

    def f(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def cr(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return round((la + 0.05) / (lb + 0.05), 2)


def mischen(grund, deck, anteil):
    """Textfarbe auf einer überlegten Fläche (z. B. Marker) vorrechnen."""
    g, d = grund.lstrip("#"), deck.lstrip("#")
    werte = [round(int(g[i:i + 2], 16) * (1 - anteil) + int(d[i:i + 2], 16) * anteil)
             for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(werte)


def paare(satz, dunkel):
    """Die Prüfpaare je Farbmodus. Namen verweisen auf die Bausteine."""
    liste = [
        ("schrift auf papier (Fließtext)", "schrift", "papier", 4.5),
        ("schrift auf flaeche (Kästen, Karten)", "schrift", "flaeche", 4.5),
        ("schrift auf papier2 (Zitate, Kopffelder)", "schrift", "papier2", 4.5),
        ("grau auf papier (Sekundärtext, Einleitungen)", "grau", "papier", 4.5),
        ("grau auf flaeche", "grau", "flaeche", 4.5),
        ("orange-tief auf papier (Kicker)", "orange-tief", "papier", 4.5),
        ("orange-tief auf flaeche (Kicker in Kästen)", "orange-tief", "flaeche", 4.5),
        ("link auf papier", "link", "papier", 4.5),
        ("link auf flaeche", "link", "flaeche", 4.5),
        ("rand auf papier (Rahmen, Grafik 3:1)", "rand", "papier", 3.0),
        ("rand auf papier2 (Grafik 3:1)", "rand", "papier2", 3.0),
        ("tinte auf gelb (btn--akzent, Vollzeit-Chip)", "tinte", "gelb", 4.5),
        ("tinte auf orange (Orange-Flächen: Kalender, Karten)", "tinte", "orange", 4.5),
        ("tinte auf kategorie-teilzeit (Teilzeit-Chip)", "tinte", "kategorie-teilzeit", 4.5),
        ("weiss auf blau (Menüpunkt aktiv, blaues Band)", "weiss", "blau", 4.5),
        ("weiss auf nacht (Fuß, schwarzes Band)", "weiss", "nacht", 4.5),
        ("gelb auf nacht (Fuß-Überschriften)", "gelb", "nacht", 4.5),
        ("schrift auf hinweis-flaeche", "schrift", "hinweis-flaeche", 4.5),
        ("schrift auf warn-flaeche", "schrift", "warn-flaeche", 4.5),
        ("warn-rand auf warn-flaeche (Grafik 3:1)", "warn-rand", "warn-flaeche", 3.0),
        ("orange-tief als Fokusfarbe auf papier (Grafik 3:1)",
         "orange-tief", "papier", 3.0),
    ]
    # Marker hinter fett gesetztem Fließtext: der Anteil steht im Alpha
    # des Tokens (0.75 hell, 0.35 dunkel) und wird hier herausgerechnet.
    anteil = float(re.search(r"([\d.]+)\s*\)", satz["marker-hintergrund"]).group(1))
    flaeche = auflösen(satz["papier"], satz)
    marker = auflösen(satz["marker-hintergrund"], satz)
    rot, grün, blau = [int(x) for x in re.findall(r"\d+", marker)[:3]]
    deck = "#%02x%02x%02x" % (rot, grün, blau)
    liste.append(("strong-Marker: schrift auf papier+Marker",
                  "schrift", mischen(flaeche, deck, anteil), 4.5))
    return liste


def main():
    regeln_css = regeln(STYLESHEET.read_text())
    hell = {}
    dunkel_media = {}
    dunkel_data = {}
    for kontext, selektor, körper in regeln_css:
        if selektor == ":root" and not kontext:
            hell = tokens(körper)
        elif selektor.startswith(":root") and "prefers-color-scheme: dark" in kontext:
            dunkel_media = tokens(körper)
        elif selektor.startswith(':root[data-theme="dark"]'):
            dunkel_data = tokens(körper)
    if not hell or not dunkel_media or not dunkel_data:
        raise SystemExit("Tokensätze nicht gefunden – Stylesheet prüfen")
    if dunkel_media != dunkel_data:
        raise SystemExit("Der dunkle Satz weicht zwischen prefers-color-scheme "
                         "und data-theme=dark ab: "
                         + str(set(dunkel_media) ^ set(dunkel_data)))

    fehler = 0
    for name, satz in (("HELL", hell), ("DUNKEL", {**hell, **dunkel_data})):
        print(f"--- {name} ---")
        for label, vorder, hinter, mindest in paare(satz, name == "DUNKEL"):
            a = auflösen(satz[vorder.lstrip("#")], satz) if vorder.startswith("--") \
                else (satz.get(vorder.lstrip("#")) or vorder)
            b = satz.get(hinter.lstrip("#")) or hinter
            a, b = auflösen(a, satz), auflösen(b, satz)
            wert = cr(a, b)
            status = "OK " if wert >= mindest else "FEHLER"
            if wert < mindest:
                fehler += 1
            print(f"{status:6} {label}: {wert} (min {mindest})")
    print("Fehler gesamt:", fehler)
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
