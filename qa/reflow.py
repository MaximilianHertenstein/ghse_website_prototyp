#!/usr/bin/env python3
"""Reflow-Sweep.

Alle gebauten Seiten x 11 Breiten auf horizontalen Ueberlauf pruefen.
Voraussetzung: `hugo -D` ist gelaufen; ein statischer Server bedient `public/`
auf Port 8732 (wird hier, falls noch nicht laeuft, selbst gestartet).

    python3 qa/reflow.py

Ausgabe: Seitenzahl, Kombinationszahl, Fehlerliste. Exit 1 bei Problemen.
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")
ROOT = os.path.abspath(ROOT)
PORT = 8732
BREITEN = [320, 360, 414, 480, 640, 768, 834, 1024, 1112, 1280, 1440]

# Optional: anderes Ziel-Verzeichnis und Port, z. B. für den Bau mit
# --baseURL /ghse_website_prototyp/ (Unterpfad-Probe):
#   python3 qa/reflow.py <verzeichnis> [port]
if len(sys.argv) > 1:
    ROOT = os.path.abspath(sys.argv[1])
if len(sys.argv) > 2:
    PORT = int(sys.argv[2])

PROBE = """<!doctype html><meta charset="utf-8"><body style="margin:0"><pre id="a">lade</pre>
<iframe id="f" style="border:0;width:100%;height:1400px"></iframe>
<script>
var t=location.hash.slice(1),f=document.getElementById('f');
f.onload=function(){try{
var d=f.contentDocument,w=f.contentWindow,sw=d.documentElement.scrollWidth,iw=w.innerWidth,bad=[];
if(sw>iw+1){var a=d.querySelectorAll('*');for(var i=0;i<a.length;i++){var r=a[i].getBoundingClientRect();
if(r.right>iw+1&&r.width>0){bad.push((a[i].tagName+'.'+(a[i].className||'')).slice(0,52)+' r='+Math.round(r.right));if(bad.length>5)break;}}}
document.getElementById('a').textContent=JSON.stringify({t:t,sw:sw,iw:iw,bad:bad});
}catch(e){document.getElementById('a').textContent=JSON.stringify({t:t,err:String(e)})}};
f.src=t;
</script>
"""


def server_stellt_sich_sicher():
    """Statischen Server auf 8732 sicherstellen, damit die Probe gleich-origin laden kann."""
    base = "http://127.0.0.1:%d" % PORT

    def erreichbar():
        try:
            urllib.request.urlopen(base, timeout=2).read()
            return True
        except Exception:
            return False

    if erreichbar():
        return
    subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    for _ in range(20):
        time.sleep(0.25)
        if erreichbar():
            return
    sys.exit("Server auf Port %d nicht erreichbar." % PORT)


def seiten_aus_public():
    treffer = []
    for ordner, _, dateien in os.walk(ROOT):
        if "index.html" in dateien:
            rel = os.path.relpath(ordner, ROOT)
            treffer.append("/" if rel == "." else "/" + rel.strip("/") + "/")
    return sorted(treffer)


def pruefe(arg):
    url, breite = arg
    try:
        html = subprocess.run(
            ["chromium", "--headless=new", "--no-sandbox", "--disable-gpu",
             "--disable-dev-shm-usage", "--virtual-time-budget=4000",
             "--window-size=%d,900" % breite, "--dump-dom",
             "http://127.0.0.1:%d/__probe.html#%s" % (PORT, url)],
            capture_output=True, text=True, timeout=60,
        ).stdout
    except subprocess.TimeoutExpired:
        return (url, breite, "TIMEOUT", "")
    m = re.search(r'<pre id="a">(.*?)</pre>', html, re.S)
    if not m:
        return (url, breite, "KEIN-PROTOKOLL", "")
    try:
        d = json.loads(m.group(1))
    except Exception:
        return (url, breite, "UNLESBAR", m.group(1)[:80])
    if "err" in d:
        return (url, breite, "FEHLER", d["err"])
    if d["sw"] > d["iw"] + 1:
        return (url, breite, "UEBERLAUF", "; ".join(d["bad"]))
    return (url, breite, "ok", "")


def main():
    if not os.path.isdir(ROOT):
        sys.exit("public/ fehlt – zuerst `hugo -D` ausfuehren.")
    server_stellt_sich_sicher()
    seiten = seiten_aus_public()
    probe_pfad = os.path.join(ROOT, "__probe.html")
    with open(probe_pfad, "w", encoding="utf-8") as f:
        f.write(PROBE)
    try:
        kombis = [(u, b) for u in seiten for b in BREITEN]
        with ThreadPoolExecutor(max_workers=6) as ex:
            ergebnisse = list(ex.map(pruefe, kombis))
    finally:
        os.remove(probe_pfad)

    probleme = [r for r in ergebnisse if r[2] != "ok"]
    print("Seiten: %d | Breiten: %d | Kombinationen: %d"
          % (len(seiten), len(BREITEN), len(ergebnisse)))
    print("Probleme: %d" % len(probleme))
    for p in sorted(probleme, key=lambda x: (x[0], x[1]))[:40]:
        print("   %-34s %4d  %-12s %s" % (p[0], p[1], p[2], p[3]))
    return 1 if probleme else 0


if __name__ == "__main__":
    sys.exit(main())
