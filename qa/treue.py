#!/usr/bin/env python3
"""Worttreue-Prüfung: vergleicht eine Inhaltsseite mit ihrer Originalseite.

Aufruf:  python3 qa/treue.py content/anfahrt.md recherche/quellen/anfahrt.html

Die Quelle wird dabei auf den Fließtext beschränkt (Navigation, Kopf- und
Fußzeile fliegen raus), Titel und Meta-Beschreibung der Front-Matter gehen in
den Vergleich ein, weil sie von der Originalseite übernommen sind. Ausgegeben
wird jede Abweichung als Austausch, Löschung oder Einfügung – reine
Satzzeichen- und Trennstrich-Anpassungen sind als solche gekennzeichnet.

Grundlage: Unterschiede entstehen entweder durch Tippfehler des Originals
(dokumentiert in der README), durch die Struktur des Prototyps (Bausteine,
Sprungmarken, PDF-Links) oder durch Fehler beim Übernehmen. Letztere sind
das, was diese Prüfung findet.
"""
import difflib
import re
import sys
import unicodedata

import lxml.html as LH

SATZZEICHEN = set(".,;:!?–-—()[]{}„“”‘’»«/|*#~+='")


_CHROME = None
_N = 6


def chrome_menge() -> set:
    """Wortgruppen, die auf vielen Originalseiten gleich stehen.

    Adresse, Öffnungszeiten und der Wiederholungs-Block der Vorlage liegen im
    Seiteninhalt statt in der Navigation. Als Sechser-Wortgruppen gefiltert
    (nicht als Satz) bleibt der Rest des Satzes erhalten, sonst reißt der
    Filter mitten drin ein Loch in den Vergleich. Gezählt wird, auf wie
    vielen Seiten die Gruppe steht, nicht wie oft – sonst trägt eine Zeile,
    die auf einer Seite mehrfach wiederholt wird, ganze Abschnitte des
    Inhalts aus dem Vergleich.
    """
    global _CHROME
    if _CHROME is None:
        import glob
        dateien = glob.glob("recherche/quellen/*.html")
        zaehler = {}
        for datei in dateien:
            woerter = worte(quelltext(datei))
            lokal = set()
            for i in range(len(woerter) - _N + 1):
                lokal.add(" ".join(w.lower() for w in woerter[i:i + _N]))
            for gram in lokal:
                zaehler[gram] = zaehler.get(gram, 0) + 1
        grenze = max(3, len(dateien) // 3)
        _CHROME = {g for g, n in zaehler.items() if n >= grenze}
    return _CHROME


def ohne_chrome(woerter, gramme: set):
    """Entfernt alle Stellen, die eine häufige Wortgruppe bilden."""
    klein = [w.lower() for w in woerter]
    draussen = []
    i = 0
    while i < len(woerter):
        if i + _N <= len(woerter) and " ".join(klein[i:i + _N]) in gramme:
            i += _N
        else:
            draussen.append(woerter[i])
            i += 1
    return draussen


def quelltext(datei: str) -> str:
    """Fließtext der Originalseite.

    Der Baum wird mit lxml gelesen und die Blöcke herausgenommen, die nicht
    zum Inhalt gehören: Navigation, Kopf- und Fußzeile (bei Elementor über
    data-elementor-type bzw. elementor-location), Skripte, Stile und das
    Einwilligungs-Banner. Eine Tiefenzählung über rohe Tags, wie sie eine
    rein textbasierte Lesart bräuchte, geht bei den ungeschlossenen
    Elementen der Vorlage sofort schief und schluckt den Rest der Seite.
    """
    wurzel = LH.parse(datei).getroot()
    weg = wurzel.xpath(
        "//script | //style | //noscript | //nav | //header | //footer | //svg"
        ' | //form | //iframe | //*[contains(@class, "wpconsent")]'
        ' | //*[contains(@class, "cookie")] | //*[contains(@class, "consent")]'
        ' | //*[@data-elementor-type="header" or @data-elementor-type="footer"'
        '      or @data-elementor-type="popup"]'
        ' | //*[contains(@class, "elementor-location-header")]'
        ' | //*[contains(@class, "elementor-location-footer")]'
    )
    for el in weg:
        if el.getparent() is not None:
            el.drop_tree()
    if wurzel.body is not None:
        wurzel = wurzel.body
    # itertext() setzt zwischen allen Textstücken ein Leerzeichen: die Vorlage
    # lässt Absätze ohne Trennzeichen ineinander übergehen, und vergleicht man
    # ohne den Zwischenraum, erscheint jeder Absatzwechsel als Änderung.
    return re.sub(r"\s+", " ", " ".join(wurzel.itertext()))


def eigener_text(datei: str) -> str:
    t = open(datei, encoding="utf-8").read()
    titel = beschreibung = ""
    bildtitel = []
    fm = re.match(r"^---\n(.*?)\n---\n", t, flags=re.S)
    if fm:
        m = re.search(r'^title:\s*"(.*)"\s*$', fm.group(1), flags=re.M)
        titel = m.group(1) if m else ""
        m = re.search(r'^description:\s*"(.*)"\s*$', fm.group(1), flags=re.M)
        beschreibung = m.group(1) if m else ""
        # Die Bildunterschriften stehen im Front-Matter und werden vom
        # Bilder-Baustein übernommen; ohne sie fehlten sie im Vergleich,
        # obwohl sie auf der Seite zu lesen sind.
        bildtitel = [n.strip('" ') for n in
                     re.findall(r'^\s*name:\s*(.+?)\s*$', fm.group(1), flags=re.M)]
        t = t[fm.end():]
    # Der Bilder-Baustein zeigt die Bilder nebst Unterschrift an seiner
    # Stelle – dort gehören sie auch in den Vergleichstext, sonst und nur
    # dort. Fehlt der Baustein, hängen wir sie ans Ende, damit sie als
    # eingebundener Inhalt geprüft und nicht übergangen werden.
    if re.search(r"\{\{<\s*bilder\b[^}]*>\}\}", t):
        t = re.sub(r"\{\{<\s*bilder\b[^}]*>\}\}", " ".join(bildtitel), t)
    elif bildtitel:
        t += " " + " ".join(bildtitel)
    t = re.sub(r"\{\{<.*?>\}\}", " ", t)          # Bausteine (bilder, bild, hinweis …)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)  # Links auf ihren Text
    t = re.sub(r"^\s*[\-*+]\s+", "", t, flags=re.M)  # Aufzählungszeichen
    # Der Genderstern bleibt Wortgrenze wie im Original, sonst erscheint
    # „Schüler*innen“ hier als Abweichung zu „Schüler*innen“ der Vorlage.
    t = t.replace("*", " ")
    t = re.sub(r"[_`>#]", "", t)
    return f"{titel} {beschreibung} {t}"


def worte(text: str):
    text = unicodedata.normalize("NFC", text)
    return re.findall(r"[A-Za-zÄÖÜäöüß0-9][A-Za-zÄÖÜäöüß0-9'’.-]*", text)


def nur_satzzeichen(a, b) -> bool:
    streifen = "".join(a) + "".join(b)
    return all(c in SATZZEICHEN or c.isspace() for c in streifen)


def kern(wort: str) -> str:
    """Wortkern ohne angehängte Satzzeichen: „Island.“ = „Island“.

    worte() nimmt Satzzeichen am Wortende mit in das Wort auf, deshalb
    erscheint jeder fehlende oder ergänzte Satzpunkt sonst als inhaltliche
    Abweichung, obwohl nur die Interpunktion anders ist. Angehängte Trenn-
    striche fallen hier mit hinein: „KFZ-Abteilung-“ am Zeilenende ist
    derselbe Fall wie ein Punkt.
    """
    return wort.rstrip(".,;:!?–—-")


def nur_kern(a, b) -> bool:
    """Zwei Wortfolgen unterscheiden sich nur durch solche Anhängsel."""
    return [kern(w) for w in a.split()] == [kern(w) for w in b.split()]


def pruefen(eigen: str, quelle: str, laut: bool = False) -> int:
    q = ohne_chrome(worte(quelltext(quelle)), chrome_menge())
    m = worte(eigener_text(eigen))
    sm = difflib.SequenceMatcher(
        a=[w.lower() for w in q], b=[w.lower() for w in m], autojunk=False
    )
    abweichungen = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        alt, neu = " ".join(q[i1:i2]), " ".join(m[j1:j2])
        if nur_satzzeichen(alt, neu) or nur_kern(alt, neu):
            abweichungen.append(("satz", alt, neu))
        elif tag == "replace":
            abweichungen.append(("tausch", alt, neu))
        elif tag == "delete":
            abweichungen.append(("fehlt", alt, ""))
        else:
            abweichungen.append(("neu", "", neu))

    echt = [a for a in abweichungen if a[0] != "satz"]
    print(f"{eigen}  ({len(q)} Wörter Quelle, {len(m)} Wörter Prototyp)")
    print(f"  Satzzeichen/Umbruch: {len(abweichungen) - len(echt)}   Inhaltliche Abweichungen: {len(echt)}")
    for art, alt, neu in echt:
        kuerz = lambda s: s if len(s) < 100 else "…" + s[-95:]
        if art == "tausch":
            print(f"    TAUSCH  {kuerz(alt)!r}\n            -> {neu[:95]!r}")
        elif art == "fehlt":
            print(f"    FEHLT   {kuerz(alt)!r}")
        else:
            print(f"    NEU     {neu[:95]!r}")
    if laut:
        for art, alt, neu in abweichungen:
            if art == "satz":
                print(f"    satz    {alt!r} -> {neu!r}")
    print()
    return len(echt)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    sys.exit(1 if pruefen(sys.argv[1], sys.argv[2], "-v" in sys.argv) else 0)
