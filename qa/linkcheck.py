#!/usr/bin/env python3
"""Interne Linkprüfung: sammelt alle href/src-Ziele aus public/ und testet sie.

Neben dem Ziel selbst wird auch das Fragment aufgelöst: ein `#abschnitt`
verlangt ein `id=` (oder ein altes `name=`) in der Zieldatei. Ein toter
Anker fällt sonst durch keine Prüfung auf – er landet stillschweigend
oben auf der Seite.
"""
import os
import re
import sys
from urllib.parse import unquote, urlparse

WURZEL = os.path.join(os.path.dirname(__file__), "..", "public")
WURZEL = os.path.abspath(WURZEL)
# Optional: anderes Ziel-Verzeichnis, z. B. der Bau mit
# --baseURL /ghse_website_prototyp/, der (verschachtelt abgelegt) unter dem
# Basispfad geprüft wird:  python3 qa/linkcheck.py <verzeichnis>
if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
    WURZEL = os.path.abspath(sys.argv[1])

ziele = set()
fehler_ziele = set()
fehler_anker = set()

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
                                    "data:")):
                    continue
                # Der Livereload-Kasten entsteht nur, wenn parallel ein
                # "hugo server" läuft – er gehört nicht zur Seite.
                if "livereload" in ziel:
                    continue
                ziele.add((rel, ziel))

# Ankernamen je Datei, einmalig gelesen
_ids_cache = {}


def ankernamen(rel):
    if rel in _ids_cache:
        return _ids_cache[rel]
    pfad = os.path.join(WURZEL, rel)
    if not os.path.isfile(pfad):
        _ids_cache[rel] = set()
        return _ids_cache[rel]
    text = open(pfad, encoding="utf-8").read()
    gefundene = set(re.findall(r'\bid="([^"]+)"', text))
    gefundene |= set(re.findall(r'\bname="([^"]+)"', text))
    _ids_cache[rel] = gefundene
    return gefundene


for quelle, ziel in sorted(ziele):
    p = urlparse(ziel)
    ziel_pfad = unquote(p.path)
    anker = unquote(p.fragment)

    if not ziel_pfad:
        # Nur Fragment: Ziel ist die verlinkende Datei selbst
        if anker and anker not in ankernamen(quelle):
            fehler_anker.add((quelle, "#" + anker))
        continue

    if ziel_pfad.startswith("/"):
        # Wurzel-absolute Ziele (im Unterpfad-Bau samt Basispfad) gegen das
        # Lauf-Verzeichnis auflösen.
        kandidat = os.path.join(WURZEL, ziel_pfad.lstrip("/"))
    else:
        # Seitenrelative Ziele („vabkf/“): gegen das Verzeichnis der
        # verlinkenden Seite auflösen.
        kandidat = os.path.normpath(
            os.path.join(WURZEL, os.path.dirname(quelle), unquote(p.path)))
    if os.path.isdir(kandidat):
        kandidat = os.path.join(kandidat, "index.html")
    if not os.path.isfile(kandidat):
        fehler_ziele.add((quelle, ziel))
    elif anker and kandidat.endswith(".html"):
        rel_ziel = os.path.relpath(kandidat, WURZEL)
        if anker not in ankernamen(rel_ziel):
            fehler_anker.add((quelle, ziel))

print(f"Interne Ziele gesamt: {len(ziele)}")
print(f"Fehlschläge Ziel:     {len(fehler_ziele)}")
for quelle, ziel in sorted(fehler_ziele)[:30]:
    print(f"  {quelle} -> {ziel}")
print(f"Fehlschläge Anker:    {len(fehler_anker)}")
for quelle, ziel in sorted(fehler_anker)[:30]:
    print(f"  {quelle} -> {ziel}")
sys.exit(1 if (fehler_ziele or fehler_anker) else 0)
