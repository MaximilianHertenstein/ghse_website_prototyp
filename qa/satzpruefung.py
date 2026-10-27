#!/usr/bin/env python3
"""Satzprüfung: für jeden Satz einer Inhaltsseite das passende Stück der
Originalseite suchen und nur die abweichenden Wörter ausgeben.

Aufruf:  python3 qa/satzpruefung.py content/fachgruppen.md recherche/quellen/fachgruppen.html

Damit sieht man auf einen Blick, ob ein Satz aus dem Original stammt (nur
Tippfehler oder Satzzeichen weichen ab), ob er umformuliert wurde oder ob er
in der Quelle gar nicht vorkommt – also erfunden ist. Überschriften,
Baustein-Aufrufe und Bildunterschriften der eigenen Seite sind davon nicht
erfasst; sie stehen nirgends als Fließtext.
"""
import difflib
import re
import sys

from treue import quelltext, worte


def normal_roh(text: str) -> str:
    return re.sub(r"[^\wäöüßÄÖÜ]", "", text).lower()


def bestes_stueck(ziel, quelle):
    """Fenster der Quelle, das dem Satz am nächsten kommt."""
    if not ziel:
        return None, []
    treffer = [i for i, w in enumerate(quelle) if w == ziel[0]]
    if not treffer:
        return None, []
    bestes, beste_zahl = None, None
    laenge = len(ziel)
    for i in treffer:
        fenster = quelle[i:i + laenge + 6]
        sm = difflib.SequenceMatcher(a=ziel, b=fenster, autojunk=False)
        abzüge = sum(3 if t == "replace" else 1 for t, *_ in sm.get_opcodes() if t != "equal")
        if beste_zahl is None or abzüge < beste_zahl:
            beste_zahl, bestes = abzüge, fenster
    sm = difflib.SequenceMatcher(a=ziel, b=bestes, autojunk=False)
    abweichungen = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        abweichungen.append((tag, " ".join(ziel[i1:i2]), " ".join(bestes[j1:j2])))
    return bestes, abweichungen


def pruefen(seite: str, quelle_datei: str, mindestlaenge: int = 25) -> int:
    quelle = worte(quelltext(quelle_datei))
    t = open(seite, encoding="utf-8").read()
    t = re.sub(r"^---.*?---", "", t, flags=re.S)
    t = re.sub(r"\{\{<[^>]*>\}\}", "", t)
    t = re.sub(r"^\s*#+\s*", "", t, flags=re.M)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"^\s*[\-*+]\s+", "", t, flags=re.M)
    t = re.sub(r"\*\*(.*?)\*\*", r"\1", t)
    t = t.replace("\n", " ")
    sätze = [s.strip() for s in re.split(r"(?<=[.!?])\s+", t) if len(s.strip()) > mindestlaenge]

    q_roh = normal_roh(" ".join(quelle))
    print(f"{seite}")
    problem = 0
    for satz in sätze:
        if normal_roh(satz) in q_roh:
            continue
        ziel = worte(satz)
        _, abw = bestes_stueck(ziel, quelle)
        echt = [a for a in abw if a[0] != "replace" or a[1] != a[2]]
        problem += 1
        print(f"  ? {satz[:110]}")
        for tag, alt, neu in echt:
            if tag == "delete":
                print(f"      in Quelle, bei uns nicht: {alt!r}")
            elif tag == "insert":
                print(f"      bei uns, nicht in Quelle:  {neu!r}")
            else:
                print(f"      {alt!r} -> {neu!r}")
    print(f"  ({problem} Sätze mit Abweichung)\n")
    return problem


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    sys.exit(1 if pruefen(sys.argv[1], sys.argv[2]) else 0)
