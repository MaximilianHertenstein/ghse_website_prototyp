#!/usr/bin/env python3
"""Reflow-Sweep.

Alle gebauten Seiten x 11 Breiten auf horizontalen Ueberlauf pruefen.
Voraussetzung: `hugo -D` ist gelaufen; ein statischer Server bedient `public/`
auf Port 8732 (wird hier, falls noch nicht laeuft, selbst gestartet).
Jede Seite wird einmal in Chromium geladen und anschließend in allen Breiten
im iframe vermessen. Die Messbreite bildet dabei den inneren Viewport der
bisherigen Fenstergrößen nach, inklusive Chromium-Mindestbreite und Scrollbar.

    python3 qa/reflow.py

Ausgabe: Seitenzahl, Kombinationszahl, Fehlerliste. Exit 1 bei Problemen.
"""
import atexit
import json
import os
import re
import socket
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
var t=location.hash.slice(1),f=document.getElementById('f'),breiten=__BREITEN__;
f.onload=async function(){
var d=f.contentDocument,berichte=[];
for(var b of breiten){
var scrollbar=window.innerWidth-document.documentElement.clientWidth;
f.style.width=(Math.max(b,window.innerWidth)-scrollbar)+'px';
await new Promise(function(resolve){setTimeout(resolve,60)});
try{
var w=f.contentWindow,sw=d.documentElement.scrollWidth,iw=w.innerWidth,bad=[];
if(sw>iw+1){var a=d.querySelectorAll('*');for(var i=0;i<a.length;i++){var r=a[i].getBoundingClientRect();
if(r.right>iw+1&&r.width>0){bad.push((a[i].tagName+'.'+(a[i].className||'')).slice(0,52)+' r='+Math.round(r.right));if(bad.length>5)break;}}}
berichte.push({t:t,breite:b,sw:sw,iw:iw,bad:bad});
}catch(e){berichte.push({t:t,breite:b,err:String(e)})}
}
document.getElementById('a').textContent=JSON.stringify(berichte);
};
f.src=t;
</script>
"""


def freier_port():
    """Ein Port, auf dem gerade nichts laeuft."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def server_stellt_sich_sicher():
    """Statischen Server auf PORT sicherstellen, damit die Probe gleich-origin laden kann.

    Ein Server, der schon auf dem Port laeuft, kann ein fremder sein: er
    bedient dann ein altes, inzwischen geloeschtes Verzeichnis und antwortet
    mit 404, ohne dass die Probe anlaeuft. Deshalb wird zuerst geprueft, ob
    der Port unsere Probe-Datei ausliefert; wenn nicht, zieht der Lauf auf
    einen freien Port. Der selbst gestartete Server wird am Ende beendet –
    sonst blockiert er den naechsten Lauf.
    """
    global PORT
    base = "http://127.0.0.1:%d" % PORT

    def liefert_probe():
        try:
            with urllib.request.urlopen(base + "/__probe.html", timeout=2) as antwort:
                return "lade" in antwort.read().decode("utf-8", "replace")
        except Exception:
            return False

    if liefert_probe():
        return
    # Der Port ist belegt, aber nicht von uns: freien Port suchen.
    PORT = freier_port()
    base = "http://127.0.0.1:%d" % PORT
    prozess = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    atexit.register(prozess.terminate)
    for _ in range(20):
        time.sleep(0.25)
        if liefert_probe():
            return
    sys.exit("Server auf Port %d nicht erreichbar." % PORT)


def seiten_aus_public():
    treffer = []
    for ordner, _, dateien in os.walk(ROOT):
        if "index.html" in dateien:
            rel = os.path.relpath(ordner, ROOT)
            treffer.append("/" if rel == "." else "/" + rel.strip("/") + "/")
    return sorted(treffer)


def pruefe(url):
    try:
        html = subprocess.run(
            ["chromium", "--headless=new", "--no-sandbox", "--disable-gpu",
             "--disable-dev-shm-usage", "--virtual-time-budget=4000",
             "--window-size=320,900", "--dump-dom",
             "http://127.0.0.1:%d/__probe.html#%s" % (PORT, url)],
            capture_output=True, text=True, timeout=60,
        ).stdout
    except subprocess.TimeoutExpired:
        return [(url, breite, "TIMEOUT", "") for breite in BREITEN]
    m = re.search(r'<pre id="a">(.*?)</pre>', html, re.S)
    if not m:
        return [(url, breite, "KEIN-PROTOKOLL", "") for breite in BREITEN]
    try:
        d = json.loads(m.group(1))
    except Exception:
        return [(url, breite, "UNLESBAR", m.group(1)[:80]) for breite in BREITEN]
    if not isinstance(d, list) or len(d) != len(BREITEN):
        return [(url, breite, "UNLESBAR", "unerwartete Messdaten")
                for breite in BREITEN]
    ergebnisse = []
    for messung in d:
        breite = messung["breite"]
        if "err" in messung:
            status, details = "FEHLER", messung["err"]
        elif messung["sw"] > messung["iw"] + 1:
            status, details = "UEBERLAUF", "; ".join(messung["bad"])
        else:
            status, details = "ok", ""
        ergebnisse.append((url, breite, status, details))
    return ergebnisse


def main():
    if not os.path.isdir(ROOT):
        sys.exit("public/ fehlt – zuerst `hugo -D` ausfuehren.")
    seiten = seiten_aus_public()
    probe_pfad = os.path.join(ROOT, "__probe.html")
    with open(probe_pfad, "w", encoding="utf-8") as f:
        f.write(PROBE.replace("__BREITEN__", json.dumps(BREITEN)))
    # Die Probe-Datei muss vor dem Server stehen, damit der Test erkennen
    # kann, ob der Port wirklich unser Verzeichnis ausliefert.
    server_stellt_sich_sicher()
    try:
        with ThreadPoolExecutor(max_workers=2) as ex:
            ergebnisse = [r for gruppe in ex.map(pruefe, seiten) for r in gruppe]
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
