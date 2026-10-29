#!/usr/bin/env python3
"""Bilder einer Originalseite herunterladen und als WebP ablegen.

Aufruf:  python3 tools/schularten-bilder.py <quelldatei> <praefix> [zielordner]

Je Seite wird für jeden Bildnamen die größte vorhandene Variante geholt
(WordPress legt zusätzlich Vorschaubilder ab – gezählt wird das Original).
Die Ziele landen als <praefix>-<n>.webp im Zielordner (Vorgabe:
static/bilder/schularten).

    python3 tools/schularten-bilder.py recherche/quellen/schulart-sg-6.html sg-6
"""
import io
import os
import re
import sys
import time
import urllib.parse
import urllib.request

from PIL import Image, UnidentifiedImageError

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS = re.compile(
    r"https://www\.ghse\.de/wp-content/uploads/[^'\"\\ )]+"
    r"\.(?:jpe?g|png|gif|webp|bmp|tiff?)(?:\?[^'\"\\ )]*)?", re.I)


def varianten(urls):
    """Basisname → Liste der Varianten (Original zuerst gewünscht)."""
    gruppen = {}
    for u in urls:
        name = u.split("/uploads/")[-1]
        basis = re.sub(r"-scaled", "", re.sub(r"-e\d+", "", name))
        basis = re.sub(r"-\d+x\d+(\.\w+)$", r"\1", basis)
        gruppen.setdefault(basis, []).append(name)
    return gruppen


def hole(url):
    anfrage = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(anfrage, timeout=60) as antwort:
        return antwort.read()


def bild_url(name):
    """Vollständige Bild-URL – Umlaute und Leerzeichen müssen maskiert sein.

    Die Vorlage legt Dateinamen wie „2-BFH2-2017-18-Wir-haben-die-schönsten-
    Hipsterbeutel…“ ab. Ohne Maskierung sucht der Server die Datei nicht und
    liefert eine Fehlermeldung statt des Bildes.
    """
    return "https://www.ghse.de/wp-content/uploads/" + \
        urllib.parse.quote(name, safe="/._-")


def main():
    quelle, praefix = sys.argv[1], sys.argv[2]
    zielordner = sys.argv[3] if len(sys.argv) > 3 else os.path.join(
        WURZEL, "static", "bilder", "schularten")
    os.makedirs(zielordner, exist_ok=True)
    roh = open(quelle, encoding="utf-8", errors="replace").read()
    gruppen = varianten(UPLOADS.findall(roh))
    for nr, (basis, namen) in enumerate(sorted(gruppen.items()), start=1):
        ziel = os.path.join(zielordner, f"{praefix}-{nr}.webp")
        if os.path.exists(ziel):
            print(f"{praefix}-{nr}.webp  vorhanden")
            continue
        beste = None
        # Neben der im Quelltext genannten Variante kommt auch das Original
        # infrage: die Vorlage verlinkt oft nur die Vorschau, das große Bild
        # liegt aber unter demselben Namen ohne Größenangabe.
        kandidaten = list(namen)
        if re.search(r"\.\w+$", basis) and basis not in kandidaten:
            kandidaten.append(basis)
        for name in sorted(kandidaten, key=lambda n: -int(
                (re.search(r"-(\d+)x(\d+)", n) or re.match(r".*?(\d+)x(\d+)", n) or
                 re.match(r"(\d+)x(\d+)", n) or [0, 0, 0])[1] if re.search(
                     r"\d+x\d+", n) else 0)):
            url = bild_url(name)
            try:
                daten = hole(url)
            except Exception as e:
                print(f"  fehlgeschlagen {name}: {e}")
                continue
            try:
                im = Image.open(io.BytesIO(daten)).convert("RGB")
            except (UnidentifiedImageError, OSError) as e:
                # Neben den Bildern liegen im Uploads-Ordner auch Dateien, die
                # keine Bilder sind (PDF, Dokumente) – die übergehen wir.
                print(f"  keine Bilddatei {name}: {e}")
                continue
            if beste is None or im.width * im.height > beste[1].width * beste[1].height:
                beste = (url, im)
            time.sleep(0.3)
        if beste:
            url, im = beste
            if im.width > 1400:
                im = im.resize((1400, round(im.height * 1400 / im.width)),
                               Image.LANCZOS)
            im.save(ziel, "WEBP", quality=82, method=6)
            print(f"{praefix}-{nr}.webp  {im.size}  aus {url.split('/uploads/')[-1][:60]}")


if __name__ == "__main__":
    main()
