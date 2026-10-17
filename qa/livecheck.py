#!/usr/bin/env python3
"""Crawlt die veröeffentlichte Seite und prueft interne Ziele + Basispfad.

Aufruf: python3 qa/livecheck.py https://<benutzer>.github.io/<repo>
"""
import re
import sys
import urllib.request

BASIS = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else ""
if not BASIS:
    sys.exit("Aufruf: python3 qa/livecheck.py <basis-url>")

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
REPOPFAD = "/" + BASIS.rsplit("/", 1)[-1]  # z. B. /ghse_website_prototyp
offen = [BASIS + "/"]
gesehen = set()
fehler = []

while offen:
    url = offen.pop()
    if url in gesehen:
        continue
    gesehen.add(url)
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as antwort:
            typ = antwort.headers.get("Content-Type", "")
            roh = antwort.read() if "text/html" in typ else b""
    except Exception as fehler_obj:
        fehler.append((url, str(fehler_obj)))
        continue
    text = roh.decode("utf-8", "ignore")
    for treffer in re.finditer(r'(?:href|src)="([^"]+)"', text):
        ziel = treffer.group(1).split("#")[0]
        if not ziel:
            continue  # nur Fragment
        if ziel.startswith(BASIS):
            if ziel not in gesehen:
                offen.append(ziel)
        elif ziel.startswith(REPOPFAD):
            kandidat = BASIS + ziel[len(REPOPFAD):]
            if kandidat not in gesehen:
                offen.append(kandidat)
        elif ziel.startswith("/"):
            fehler.append((url, "Basispfad fehlt: " + ziel))

print("Geprüft:", len(gesehen), "| Fehler:", len(fehler))
for wo, was in sorted(fehler)[:25]:
    print(" ", was, "->", wo)
sys.exit(1 if fehler else 0)
