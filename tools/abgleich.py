#!/usr/bin/env python3
"""Wortabgleich einer Seite mit ihrer Originalseite (ohne README-Prüfung).

Aufruf:  python3 tools/abgleich.py <eigene.md> <quelle.html> [<eigene.md> <quelle.html> …]

Anders als `qa/paare.py` bricht dieses Skript nicht ab, wenn eine Abweichung
noch nicht in README Abschnitt 3 belegt ist: es zeigt nur den Befund. Damit
lässt sich beim Übernehmen einer Seite Schritt für Schritt prüfen, bis der
Wortlaut der Vorlage entspricht.
"""
import os
import sys

sys.path.insert(0, "qa")
import paare  # noqa: E402
import treue  # noqa: E402


def vergleich(md, quelle):
    q = [w.lower() for w in paare.quellwoerter(quelle)]
    m = [w.lower() for w in treue.worte(treue.eigener_text(md))]
    beschreibung = [w.lower() for w in
                    treue.worte(paare.frontmatter(md, "description"))]
    start = len(treue.worte(paare.frontmatter(md, "title")))
    if beschreibung and m[start:start + len(beschreibung)] == beschreibung:
        del m[start:start + len(beschreibung)]
    return paare.abweichungen(q, m)


def main():
    args = sys.argv[1:]
    if len(args) % 2:
        sys.exit(__doc__)
    summe = 0
    for i in range(0, len(args), 2):
        md, quelle = args[i], args[i + 1]
        raus = vergleich(md, quelle)
        summe += len(raus)
        print(f"== {md}  ({len(raus)} Abweichungen)")
        for tag, alt, neu in raus:
            if tag == "insert":
                print(f"   [neu]     {neu[:160]!r}")
            elif tag == "delete":
                print(f"   [fehlt]   {alt[:160]!r}")
            else:
                print(f"   [tausch]  {alt[:120]!r}\n             -> {neu[:120]!r}")
    print(f"\nSumme: {summe} Abweichungen")
    return 0


if __name__ == "__main__":
    sys.exit(main())
