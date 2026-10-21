#!/usr/bin/env python3
"""Externe Linkprüfung: testet alle http(s)-Ziele, die aus public/ herausführen.

Getrennt wird streng zwischen zwei Lagen:

  * nachweisbar tot  (404/410, DNS-Auflösung fehlt)  -> Fehler, Exit 1
  * lebend, aber blockiert (503, Verbindungsabbruch bei intakter DNS)
                                              -> Hinweis, kein Fehler

Viele Schul-, Behörden- und Verbandsseiten sperren automatisierte Zugriffe.
Wer sie als Fehler wertet, lernt nur, den Prüfer zu überspringen; als Hinweis
bleiben sie sichtbar, ohne die Routineprüfung zu lähmen.
"""
import os
import re
import subprocess
import sys
from collections import defaultdict

WURZEL = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public"))

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

ziele = defaultdict(set)
for ordner, _, dateien in os.walk(WURZEL):
    for datei in dateien:
        if not datei.endswith(".html"):
            continue
        rel = os.path.relpath(os.path.join(ordner, datei), WURZEL)
        text = open(os.path.join(ordner, datei), encoding="utf-8").read()
        for m in re.finditer(r'(?:href|src)="(https?://[^"]+)"', text):
            ziel = m.group(1)
            if "127.0.0.1" in ziel or "localhost" in ziel:
                continue
            ziele[ziel].add(rel)

tot, blockiert, unklar = [], [], []
for ziel in sorted(ziele):
    p = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-L",
         "--max-time", "25", "-H", "User-Agent: " + UA,
         "-H", "Accept: text/html,application/xhtml+xml", ziel],
        capture_output=True, text=True)
    code = p.stdout.strip()
    if code in ("200", "204", "301", "302"):
        continue
    host = re.sub(r'https?://([^/]+).*', r'\1', ziel)
    dns = subprocess.run(["getent", "hosts", host],
                         capture_output=True, text=True).stdout.split()
    if code == "000" and not dns:
        tot.append((ziel, code, "Domain existiert nicht"))
    elif code in ("404", "410"):
        tot.append((ziel, code, "Seite fehlt"))
    elif not dns:
        tot.append((ziel, code, "DNS-Aufloesung fehlt"))
    elif code == "000" or code == "503":
        blockiert.append((ziel, code, "lebend, Zugriff gesperrt"))
    else:
        unklar.append((ziel, code, "Status pruefen"))

print(f"Externe Ziele gesamt:      {len(ziele)}")
print(f"Nachweisbar tot:           {len(tot)}")
for z, c, b in tot:
    print(f"  HTTP {c:<5} {b}")
    print(f"     {z}")
print(f"Lebend, aber gesperrt:     {len(blockiert)}")
for z, c, b in blockiert:
    print(f"  HTTP {c:<5} {z}")
print(f"Unklarer Status:           {len(unklar)}")
for z, c, b in unklar:
    print(f"  HTTP {c:<5} {z}")
sys.exit(1 if (tot or unklar) else 0)
