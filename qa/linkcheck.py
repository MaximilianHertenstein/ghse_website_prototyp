#!/usr/bin/env python3
"""Interne Linkprüfung: sammelt alle href/src-Ziele aus public/ und testet sie."""
import os
import re
import sys
from urllib.parse import unquote, urlparse

WURZEL = os.path.join(os.path.dirname(__file__), "..", "public")
WURZEL = os.path.abspath(WURZEL)

ziele = set()
fehler = []

for ordner, _, dateien in os.walk(WURZEL):
    for datei in dateien:
        if not datei.endswith(".html"):
            continue
        pfad = os.path.join(ordner, datei)
        rel = os.path.relpath(pfad, WURZEL)
        text = open(pfad, encoding="utf-8").read()
        for attr in ("href", "src"):
            for treffer in re.finditer(r'%s="([^"]+)"' % attr, text):
                ziel = treffer.group(1)
                if ziel.startswith(("http://", "https://", "mailto:", "tel:",
                                    "data:", "#")):
                    continue
                ziele.add((rel, ziel))

fehler_ziele = set()
for quelle, ziel in sorted(ziele):
    p = urlparse(ziel)
    ziel_pfad = unquote(p.path)
    if not ziel_pfad:
        continue  # nur Fragment auf derselben Seite
    ziel_pfad = ziel_pfad.lstrip("/")
    kandidat = os.path.join(WURZEL, ziel_pfad)
    if os.path.isdir(kandidat):
        kandidat = os.path.join(kandidat, "index.html")
    if not os.path.isfile(kandidat):
        fehler_ziele.add((quelle, ziel))
    elif p.fragment and ziel_pfad.endswith(".html"):
        pass  # Fragmente werden hier nicht aufgelöst (bewusst)

print(f"Interne Ziele gesamt: {len(ziele)}")
print(f"Fehlschläge: {len(fehler_ziele)}")
for quelle, ziel in sorted(fehler_ziele)[:30]:
    print(f"  {quelle} -> {ziel}")
sys.exit(1 if fehler_ziele else 0)
