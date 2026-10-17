#!/usr/bin/env python3
"""Liest einen Lighthouse-Bericht, fragt Yellow Lab Tools und den MDN
Observatory ab und schreibt daraus die Datei METRIKEN.md.

Aufruf (CI): python3 tools/metriken.py --lighthouse lighthouse.json \\
                 --observatory observatory.json --url <live-url>

Metriken:
  GL  Google Lighthouse: Durchschnitt der vier Kategorien (0-100).
  YL  Yellow Lab Tools Gesamtscore (0-100), per Public API gemessen.
  MO  MDN/Mozilla Observatory Score (0-100 und Note) aus dem JSON der
      Observatory-CLI (@mdn/mdn-http-observatory) — deren API-Variante
      kennt keine Unterpfade, die CLI hingegen schon.

Alle externen Messungen sind fehlertolerant: Schlägt ein Dienst fehl,
wird die Metrik mit „n/a" und Grund eingetragen statt abzubrechen.
"""
import argparse
import datetime
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

YLT_API = "https://yellowlab.tools/api"
UA = {"User-Agent": "ghse-prototyp-metriken"}


def aufrufen(url, methode="GET", koerper=None, timeout=60):
    daten = json.dumps(koerper).encode() if koerper is not None else None
    kopf = dict(UA)
    if daten:
        kopf["Content-Type"] = "application/json"
    anfrage = urllib.request.Request(url, data=daten, headers=kopf, method=methode)
    with urllib.request.urlopen(anfrage, timeout=timeout) as antwort:
        return json.loads(antwort.read().decode())


def yellow_lab(url):
    """Startet einen YLT-Lauf und wartet auf das Ergebnis."""
    antwort = aufrufen(f"{YLT_API}/runs", "POST", {"url": url, "device": "desktop"})
    lauf_id = antwort.get("runId") or antwort.get("id")
    if not lauf_id:
        raise RuntimeError(f"YLT lieferte keine Lauf-ID: {antwort}")
    ergebnis_url = f"https://yellowlab.tools/result/{lauf_id}"
    for _ in range(60):  # maximal ~15 Minuten
        zeit = aufrufen(f"{YLT_API}/runs/{lauf_id}")
        status = zeit.get("status")
        code = status.get("statusCode") if isinstance(status, dict) else status
        if code in ("complete", "failed", "error", "cancelled"):
            break
        time.sleep(15)
    else:
        raise RuntimeError("Zeitüberschreitung bei Yellow Lab Tools")
    if code != "complete":
        raise RuntimeError(f"YLT-Lauf endete mit Status {code}")
    punkte = aufrufen(f"{YLT_API}/results/{lauf_id}/generalScores")
    wert = punkte.get("globalScore")
    if wert is None:  # Fassung ohne Sammelscore: Kategorien mitteln
        kat = punkte.get("categories", {})
        werte = [k.get("categoryScore") for k in kat.values()
                 if isinstance(k, dict) and k.get("categoryScore") is not None]
        wert = round(sum(werte) / len(werte))
    return round(wert), ergebnis_url


def observatory(pfad):
    """Liest das JSON der MDN-Observatory-CLI (@mdn/mdn-http-observatory)."""
    scan = json.load(open(pfad, encoding="utf-8"))["scan"]
    if scan.get("error"):
        raise RuntimeError(scan["error"])
    return round(scan["score"]), str(scan.get("grade") or "").upper()


def badge(label, wert, farbe):
    text = urllib.parse.quote(str(wert), safe="")
    return f"![{label}](https://img.shields.io/badge/{label}-{text}-{farbe})"


def lighthouse_wert(pfad):
    daten = json.load(open(pfad, encoding="utf-8"))
    kategorien = daten["categories"]
    return round(sum(k["score"] for k in kategorien.values()) / len(kategorien) * 100)


def hauptteil():
    p = argparse.ArgumentParser()
    p.add_argument("--lighthouse", required=True, help="Pfad zum Lighthouse-JSON")
    p.add_argument("--observatory", required=True, help="Pfad zum Observatory-JSON")
    p.add_argument("--url", required=True, help="Live-URL der Startseite")
    a = p.parse_args()

    host = urllib.parse.urlsplit(a.url).netloc
    jetzt = datetime.datetime.now(datetime.timezone.utc)
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    lauf_link = (f"https://github.com/MaximilianHertenstein/ghse_website_prototyp/"
                 f"actions/runs/{run_id}" if run_id else "")
    obs_link = f"https://developer.mozilla.org/de/observatory/?host={host}"

    gl = lighthouse_wert(a.lighthouse)

    yl_punkte, yl_anzeige, yl_link, yl_fehler = None, "n/a", "", ""
    try:
        yl_punkte, yl_link = yellow_lab(a.url)
        yl_anzeige = str(yl_punkte)
    except Exception as fehler:  # Quota, Warteschlange, Umbau ...
        yl_fehler = str(fehler)

    mo_punkte, mo_anzeige, mo_fehler = None, "n/a", ""
    try:
        mo_punkte, note = observatory(a.observatory)
        mo_anzeige = f"{mo_punkte} ({note})" if note else str(mo_punkte)
    except Exception as fehler:
        mo_fehler = str(fehler)

    def farbe(punkte):
        if not isinstance(punkte, int):
            return "lightgrey"
        return "brightgreen" if punkte >= 90 else ("green" if punkte >= 70 else "yellow")

    zeilen = [
        ("GL", "Google Lighthouse Ø", "Durchschnitt der vier Kategorien (0–100), höher = besser",
         f"**{gl}**", farbe(gl)),
        ("YL", "Yellow Lab Tools", "Gesamtscore Performance/Best Practices/SEO (0–100), höher = besser",
         f"**{yl_anzeige}**" + (f" ({yl_fehler})" if yl_fehler else ""), farbe(yl_punkte)),
        ("MO", "MDN/Mozilla Observatory", "Sicherheits-Header (0–100 und Note), höher = besser",
         f"**{mo_anzeige}**" + (f" ({mo_fehler})" if mo_fehler else ""), farbe(mo_punkte)),
    ]

    links = []
    if lauf_link:
        links.append(f"[Lighthouse-JSON & Logs der letzten Messung]({lauf_link})")
    if yl_link:
        links.append(f"[Yellow-Lab-Tools-Ergebnis]({yl_link})")
    links.append(f"[MDN Observatory]({obs_link})")

    text = f"""# Qualitäts-Metriken

> Automatisch geschrieben vom Workflow
> [Qualitäts-Metriken](https://github.com/MaximilianHertenstein/ghse_website_prototyp/actions/workflows/metriken.yml)
> (wöchentlich montags oder manuell unter „Actions" → „Qualitäts-Metriken" → „Run workflow").
> Kein Wert im Repository ist von Hand gepflegt.

{' '.join(badge(k, re.sub(r"\*\*", "", w), f) for k, _, _, w, f in zeilen)}

| Kürzel | Metrik | Bedeutung | Letzter Wert |
|---|---|---|---|
""" + "\n".join(f"| {k} | {n} | {b} | {w} |" for k, n, b, w, _ in zeilen) + f"""

Letzte Messung: {jetzt.strftime('%Y-%m-%d %H:%M')} UTC gegen <{a.url}>

Details: {' · '.join(links)}
"""
    with open("METRIKEN.md", "w", encoding="utf-8") as datei:
        datei.write(text)
    print(f"METRIKEN.md geschrieben: GL={gl} YL={yl_anzeige} MO={mo_anzeige}")


if __name__ == "__main__":
    sys.exit(hauptteil())
