#!/usr/bin/env python3
"""Instagram-Beiträge der GHSE in content/_index.md aktualisieren.

Aufruf:  python3 tools/instagram.py [--anzahl 4]

Lädt die Startseite des Schulaccounts (ohne Anmeldung, Googlebot-Trick),
liest die neuesten Beiträge aus (Media-pk, Bild-Adresse, Bildunterschrift),
leitet daraus den Kurzcode ab (Base64 des pk – nachweislich identisch mit
der Angabe in der Beitragsadresse), legt die Bilder als WebP unter
static/bilder/ ab und ersetzt die Liste `insta_beitraege` in
content/_index.md durch die aktuellen Beiträge.

Bildtexte (bildAlt) kann das Skript nicht erfinden:
  * Für bereits vorhandene Kurzcodes übernimmt es den stehenden Text.
  * Für neue Kurzcode trägt es einen auffälligen Platzhalter ein und
    weist auf der Konsole darauf zurück, dass die Bildbeschreibung
    fehlt – sie bitte vor dem Build ergänzen.
"""

import argparse
import base64
import io
import json
import re
import sys
import urllib.request
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
DATEI = WURZEL / "content" / "_index.md"
BILDER = WURZEL / "static" / "bilder"
PROFIL = "https://www.instagram.com/ghse_emmendingen/"
KENNUNG = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
PLATZHALTER = "TODO: Bildbeschreibung für {name} ergänzen – Bild unter static/bilder ansehen"


def laden(url, binär=False):
    anfrage = urllib.request.Request(url, headers={"User-Agent": KENNUNG})
    with urllib.request.urlopen(anfrage, timeout=60) as antwort:
        daten = antwort.read()
    return daten if binär else daten.decode("utf-8", "replace")


def kurzcode(pk):
    """Media-pk → Kurzcode der Beitragsadresse (Base64, URL-Alphabet)."""
    zahl = int(pk)
    kodiert = ""
    while zahl > 0:
        kodiert = ALPHABET[zahl % 64] + kodiert
        zahl //= 64
    return kodiert


def beiträge(seite):
    """(pk, Bildadresse, Text) je Beitrag, neueste zuerst."""
    ganze = [
        (m.start(), m.group(1))
        for m in re.finditer(r'"pk":"(\d{15,25})"', seite)
    ]
    ausgabe = []
    für = re.finditer(r'"caption":\{"pk":"\d+","text":"((?:[^"\\]|\\.)*)"', seite)
    for treffer in für:
        text = json.loads('"' + treffer.group(1) + '"')
        pk = None
        bild = None
        for pos, wert in ganze:
            if pos >= treffer.start():
                break
            pk = wert  # letzter pk vor der Unterschrift ist der Media-pk
        davor = seite.rfind('"display_uri":"', 0, treffer.start())
        if davor >= 0:
            bild = json.loads('"' + seite[davor + len('"display_uri":"'):
                                      seite.find('"', davor + len('"display_uri":"'))] + '"')
        if pk and bild:
            ausgabe.append({"pk": pk, "bild": bild.replace("\\/", "/"), "text": text})
    # Doppelte Medien (Vorschau + Beitrag) aussondern
    eindeutig = []
    gesehen = set()
    for beitrag in ausgabe:
        if beitrag["pk"] not in gesehen:
            gesehen.add(beitrag["pk"])
            eindeutig.append(beitrag)
    return eindeutig


def webp(beitrag, ziel):
    """Bild laden und wie die bisherigen Beiträge als 680-px-WebP ablegen."""
    quelle = beitrag["bild"].replace("s640x640", "s680x680")
    try:
        daten = laden(quelle, binär=True)
    except Exception:
        daten = laden(beitrag["bild"], binär=True)
    from PIL import Image
    bild = Image.open(io.BytesIO(daten)).convert("RGB")
    if bild.width > 680:
        bild = bild.resize((680, 680))
    bild.save(ziel, "WEBP", quality=82, method=6)


def kurzfassung(text, länge=150):
    """Erster Absatz ohne Emojis und Hashtags als Kurzfassung."""
    zeile = text.split("\n")[0]
    zeile = re.sub(r"[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u200D]+", "", zeile)
    zeile = re.sub(r"\s+", " ", zeile).strip()
    if len(zeile) > länge:
        zeile = zeile[:länge].rsplit(" ", 1)[0].rstrip(",;:") + " …"
    return zeile


def liste_ersetzen(text, einträge, bekannte_alt):
    """Den `insta_beitraege`-Block in _index.md austauschen."""
    anfang = re.search(r"^insta_beitraege:\s*$", text, re.M)
    if not anfang:
        raise SystemExit("insta_beitraege in _index.md nicht gefunden")
    rest = text[anfang.end():]
    ende = re.search(r"^\S", rest, re.M)
    block_neu = ""
    warnung = []
    for beitrag in einträge:
        code = kurzcode(beitrag["pk"])
        name = f"insta-{code}.webp"
        alt = bekannte_alt.get(code) or PLATZHALTER.format(name=name)
        if not bekannte_alt.get(code):
            warnung.append(code)
        block_neu += (f'  - bild: "/bilder/{name}"\n'
                      f'    bildAlt: "{alt}"\n'
                      f'    text: "{kurzfassung(beitrag["text"])}"\n'
                      f'    url: "https://www.instagram.com/p/{code}/"\n')
    return text[:anfang.end()] + "\n" + block_neu + text[anfang.end() + ende.start():], warnung


def bekannte_alts(text):
    """Alt-Texte der stehenden (nicht auskommentierten) Beiträge."""
    fund = {}
    for m in re.finditer(r'^  - bild: "/bilder/(insta-[A-Za-z0-9_-]+)\.webp"\n'
                         r'    bildAlt: "((?:[^"\\]|\\.)*)"', text, re.M):
        fund[m.group(1)[len("insta-"):]] = m.group(2)
    return fund


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--anzahl", type=int, default=4)
    argumente = parser.parse_args()

    seite = laden(PROFIL)
    einträge = beiträge(seite)[:argumente.anzahl]
    if not einträge:
        raise SystemExit("Keine Beiträge gefunden – Profilseite prüfen")

    text = DATEI.read_text()
    alt = bekannte_alts(text)

    for beitrag in einträge:
        code = kurzcode(beitrag["pk"])
        ziel = BILDER / f"insta-{code}.webp"
        if not ziel.exists():
            webp(beitrag, ziel)
            print(f"Bild abgelegt: {ziel.relative_to(WURZEL)}")
        else:
            print(f"Bild vorhanden: {ziel.relative_to(WURZEL)}")

    neu, warnung = liste_ersetzen(text, einträge, alt)
    DATEI.write_text(neu)
    print(f"{len(einträge)} Beiträge in {DATEI.relative_to(WURZEL)} aktualisiert.")
    if warnung:
        print("\nBITTE PRÜFEN – bildAlt ist ein Platzhalter für:")
        for code in warnung:
            print(f"  {code}  (static/bilder/insta-{code}.webp)")


if __name__ == "__main__":
    main()
