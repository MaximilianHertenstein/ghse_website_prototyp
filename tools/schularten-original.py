#!/usr/bin/env python3
"""Originalseiten der Schularten auslesen: Textstruktur und Bilder.

Aufruf:  python3 tools/schularten-original.py [quelldatei ...]

Ohne Argument werden alle recherche/quellen/schulart-*.html gelesen.
Für jede Seite werden Überschriften, Absätze, Listen, Knöpfe, Bilder und
die FAQ-Akkordeons in Dokumentreihenfolge ausgegeben – als Markdown-Baustein,
damit die Seite im Quellwortlaut übernommen werden kann. Navigation, Suche
und Formulare bleiben außen vor.

Der Lauf geht über den Inhaltsbereich der Seite, nicht über einzelne
Elementor-Widgets: die Vorlage setzt manche Absätze direkt in den Container
und nicht in einen Baustein – über die Widgets gingen sie verloren. Jeder
Block (Absatz, Listenpunkt, Überschrift) bekommt den Text, der direkt an
ihm hängt; Text in der Zeile darunter gehört zum nächsten Block.
"""
import glob
import os
import re
import sys

import lxml.html

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WEG = ("nav", "header", "footer", "form", "script", "style", "noscript",
       "svg", "iframe", "button")

BLOCK = ("p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "div", "section",
         "ul", "ol", "table", "tr", "td", "th", "figure", "figcaption",
         "blockquote", "article", "main", "aside", "dl", "dt", "dd")


def text(el):
    return " ".join(el.text_content().split())


def inhaltsbereich(baum):
    """Der Bereich mit dem Seiteninhalt – ohne Kopf- und Fußbereich."""
    bereich = None
    for xpf in ("//*[@data-elementor-type='wp-page']",
                "//*[contains(@class,'elementor-location-single')]",
                "//main",
                "//article"):
        treffer = baum.xpath(xpf)
        if treffer:
            bereich = treffer[0]
            break
    if bereich is None:
        bereich = baum
    for el in bereich.xpath(
            "//nav | //header | //footer | //form | //script | //style"
            " | //noscript | //svg | //iframe"
            ' | //*[@data-elementor-type="header" or @data-elementor-type="footer"'
            '      or @data-elementor-type="popup"]'
            ' | //*[contains(@class, "elementor-location-header")]'
            ' | //*[contains(@class, "elementor-location-footer")]'
    ):
        if el.getparent() is not None:
            el.drop_tree()
    return bereich


def eigener_text(el):
    """Der Text, der unmittelbar an diesem Block hängt.

    Kindelemente, die selbst Blöcke sind, gehören nicht dazu – ihr Text
    wird an der eigenen Stelle ausgegeben.
    """
    teile = []
    if el.text and el.text.strip():
        teile.append(el.text.strip())
    for kind in el:
        if not isinstance(kind.tag, str):
            continue
        if kind.tag.lower() not in BLOCK:
            t = text(kind)
            if t:
                teile.append(t)
        if kind.tail and kind.tail.strip():
            teile.append(kind.tail.strip())
    return " ".join(teile)


def sammle(el):
    """Textblöcke und Bilder eines Bereichs in Dokumentreihenfolge."""
    ergebnis = []
    for knoten in el.iter():
        if not isinstance(knoten.tag, str):
            continue
        tag = knoten.tag.lower()
        klasse = knoten.get("class") or ""
        if tag == "div" and "elementor-tab-title" in klasse:
            inhalt = knoten.getparent()
            antwort = inhalt.xpath(
                ".//*[contains(@class,'elementor-tab-content')]") if inhalt is not None else []
            ergebnis.append(("faq", text(knoten),
                             text(antwort[0]) if antwort else ""))
            continue
        if "elementor-tab-content" in klasse or "elementor-accordion" in klasse:
            continue
        if tag == "img":
            quelle = knoten.get("src") or knoten.get("data-src") or ""
            if quelle and "/uploads/" in quelle:
                ergebnis.append(("img", quelle, (knoten.get("alt") or "").strip()))
            continue
        if tag == "a":
            if knoten.xpath("ancestor::p") or knoten.xpath("ancestor::li"):
                continue
            if knoten.xpath("ancestor::*[contains(@class,'elementor-accordion')]"):
                continue
            t = text(knoten)
            if t:
                ergebnis.append(("link", t, knoten.get("href") or ""))
            continue
        if tag not in BLOCK:
            continue
        t = eigener_text(knoten)
        if not t:
            continue
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            ergebnis.append(("head", tag, t))
        elif tag == "p":
            ergebnis.append(("p", "", t))
        elif tag == "li":
            ergebnis.append(("li", "", t))
        elif tag in ("td", "th"):
            ergebnis.append(("zelle", "", t))
        else:
            # Container, der den Text unmittelbar trägt.
            ergebnis.append(("p", "", t))
    return ergebnis


def main():
    dateien = sys.argv[1:] or sorted(glob.glob(
        os.path.join(WURZEL, "recherche", "quellen", "schulart-*.html")))
    for datei in dateien:
        roh = open(datei, encoding="utf-8", errors="replace").read()
        baum = lxml.html.fromstring(roh)
        name = os.path.basename(datei)[len("schulart-"):-len(".html")]
        print("=" * 72)
        print("###", name)
        for art, a, b in sammle(inhaltsbereich(baum)):
            if art == "head":
                stufe = int(a[1])
                print("#" * min(stufe + 1, 5) + " " + b)
            elif art == "p":
                print(b)
            elif art == "li":
                print("- " + b)
            elif art == "zelle":
                print("| " + b)
            elif art == "img":
                if re.search(r"-\d+x\d+\.\w+$", a):
                    continue                      # Vorschaubild, das Original zählt
                print(f"BILD: {a}  ||  alt={b!r}")
            elif art == "link":
                print(f"  [LINK] {a} -> {b}")
            elif art == "faq":
                print("FAQ: " + a)
                if b:
                    print("  " + b)


if __name__ == "__main__":
    main()
