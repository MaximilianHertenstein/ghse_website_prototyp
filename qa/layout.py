#!/usr/bin/env python3
"""Layoutmessung des GHSE-Prototyps in Chromium (ohne npm-Toolchain).

Misst die Prüfkriterien A1, A2 und A4 aus DESIGN-IDEEN.md an drei Breiten
(1440/640/390 px) und prüft zusätzlich die Höhe des Mobilkopfs:

  A1  Nach einem Ankersprung liegt das Ziel vollständig unter Kopf und
      Sprungleiste (getBoundingClientRect().top >= Kopfende + Leistenhöhe).
  A2  Die Sprungleiste überlappt den Kopf nicht (0 px).
  A4  Touch-Ziele erreichen auf grobem Zeiger mindestens 44 px (Buttons,
      Chips, Kalender-Karten – Pflichtaktionen nach A4); Textlinks wie
      .linkpfeil müssen die AA-Schwelle von 24 px erreichen. Gemessen wird
      die kleinste sichtbare Fläche je Selektor. Headless-Chromium meldet
      `pointer: coarse` nicht, deshalb wird ab 640 px Breite geprüft – genau
      dort greifen die CSS-Regeln laut Media-Query auch.

Dazu baut das Skript die Seite nach einem temporären Verzeichnis, hängt dort
eine Mess-Seite mit eingebetteten iframes an (gleicher Ursprung, damit der
Messcode in die Seite hineinschauen darf) und öffnet sie in Chromium
--dump-dom. Das entspricht der in DESIGN-IDEEN.md Abschnitt 12 beschriebenen
Messmethode.

Aufruf:  python3 qa/layout.py            (setzt ein fertiges public/ voraus)
         python3 qa/layout.py --bauen    (baut vorher mit `hugo -D`)
"""

import http.server
import json
import os
import re
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BREITEN = [1440, 640, 390]
ZIELE = ["/", "/news/", "/downloads/", "/schularten/technisches-gymnasium/"]
# Selektoren mit der zugehörigen Zielhöhe. A4 (DESIGN-IDEEN §7) verlangt
# ≥ 44 px auf grobem Zeiger ausdrücklich nur für Buttons, Chips und
# Kalender-Karten – das sind die Pflichtaktionen. Textlinks wie .linkpfeil
# sind dort nicht aufgeführt; für sie gilt die AA-Schwelle von 24 px.
# In Fließtext gesetzte Ausdrucke (.fliesstext .linkpfeil) bleiben bewusst
# außen vor – sie stehen im Satz, nicht als eigenes Ziel.
A4_ZIELE = {
    ".btn--klein": 44, ".chip": 44, ".kalender": 44,
    ".menueknopf": 44, ".modusknopf": 44, ".sprungleiste a": 44,
    ".linkpfeil": 24,
}

MESS_JS = r"""
const berichte = [];
function warte(ms) { return new Promise(r => setTimeout(r, ms)); }
// fonts.ready gegen eine Frist abriegeln: unter --virtual-time-budget hängt
// gelegentlich der Schrift-Ready-Signalisierer, dann darf die Messung
// trotzdem weiterlaufen.
function mitFrist(p, ms) {
  return Promise.race([p, new Promise(r => setTimeout(() => r(null), ms))]);
}

async function messe(iframe, breite, pfad) {
  const w = iframe.contentWindow, d = iframe.contentDocument;
  if (!d || !d.body) return null;
  if (d.fonts && d.fonts.ready) { try { await mitFrist(d.fonts.ready, 3000); } catch (e) {} }
  // Zweimal kurz warten: einmal für den Stylesheet-Layoutdurchlauf, einmal
  // damit die in nav.js gemessene Kopfhöhe angekommen ist. Bewusst kein
  // requestAnimationFrame – der feuert im dump-Dom-Betrieb nicht.
  await warte(60);
  await warte(60);

  const kopf = d.querySelector('.kopf');
  const leiste = d.querySelector('.leiste');
  const kL = kopf ? kopf.getBoundingClientRect() : null;
  const leisteSichtbar = leiste && getComputedStyle(leiste).display !== 'none';
  const kopfEnde = kL ? kL.bottom : 0;

  // A2: Gescrollt sitzt die Sprungleiste (sticky) direkt unter dem Kopf.
  // Eine Überlappung wäre ein Rasterfehler; ihre Höhe ist zugleich die
  // Unterlage, unter der ein Ankersprungziel landen muss.
  d.documentElement.style.scrollBehavior = 'auto';
  const sprungleiste = d.querySelector('.sprungleiste');
  let sprungHoehe = 0, ueberlappung = 0;
  if (sprungleiste) {
    sprungHoehe = Math.round(sprungleiste.getBoundingClientRect().height);
    w.scrollTo(0, 2000);
    ueberlappung = Math.max(0, Math.round(
      kopf.getBoundingClientRect().bottom - sprungleiste.getBoundingClientRect().top));
    w.scrollTo(0, 0);
  }

  // A1: Ankersprung auf die erste Download-Kategorie (nur dort gibt es
  // Ziele, die unter der Sprungleiste liegen).
  const noetig = kopfEnde + sprungHoehe;
  let sprung = null;
  const ziel = d.querySelector('h2[id^="dl-"]');
  if (ziel) {
    w.location.hash = ziel.id;
    const top = ziel.getBoundingClientRect().top;
    sprung = { id: ziel.id, top: Math.round(top), noetig: Math.round(noetig),
               ok: top >= noetig - 1 };
    w.history.replaceState(null, '', w.location.pathname);
  }

  // A4: Touch-Ziele. Der bindende Wert ist die KLEINSTE sichtbare Fläche –
  // ein zu kleines Ziel darf nicht von einem größeren Geschwisterteil
  // verdeckt werden, deshalb minimum statt Maximum.
  const ziele = {};
  for (const sel of A4) {
    const e = [...d.querySelectorAll(sel)].filter(x => x.offsetParent !== null || x === d.activeElement);
    if (!e.length) continue;
    const hoehen = e.map(x => Math.round(x.getBoundingClientRect().height));
    ziele[sel] = { n: e.length, min: Math.min(...hoehen), max: Math.max(...hoehen) };
  }

  // Mobilmenü: Krankmelden muss dort erreichbar sein, wo die Leiste fehlt.
  let menue = null;
  const btn = d.querySelector('[data-menu-button]');
  if (btn && getComputedStyle(btn).display !== 'none') {
    btn.click();
    const schnell = d.querySelector('.menue__schnell');
    const sichtbar = schnell && getComputedStyle(schnell).display !== 'none';
    const kranks = schnell ? [...schnell.querySelectorAll('a')].some(a => /krankmelden/i.test(a.textContent)) : false;
    menue = { schnellSichtbar: !!sichtbar, krankmelden: kranks,
              hoehe: schnell && sichtbar ? Math.round(schnell.getBoundingClientRect().height) : 0 };
    btn.click();
  }

  // Rasterlöcher: Karten derselben Zeile auf gleicher Höhe?
  const raster = {};
  for (const sel of ['.raster--news', '.raster--2', '.raster--3']) {
    const g = d.querySelector(sel);
    if (!g) continue;
    const karten = [...g.children];
    raster[sel] = { n: karten.length,
      zeilen: [...new Set(karten.map(k => Math.round(k.getBoundingClientRect().top)))].length };
  }

  return { pfad, breite, kopfHoehe: kL ? Math.round(kL.height) : null,
    token: getComputedStyle(d.documentElement).getPropertyValue('--kopfhoehe').trim(),
    leisteSichtbar, sprungHoehe, sprung, ueberlappung,
    ziele, menue, raster };
}

(async function () {
  const ausgabe = document.getElementById('ausgabe');
  try {
  const iframes = [];
  for (const b of BREITEN) for (const p of ZIELE) {
    const f = document.createElement('iframe');
    f.style.cssText = `width:${b}px;height:1400px;border:0;display:block`;
    f.src = p;
    document.body.appendChild(f);
    iframes.push([f, b, p]);
  }
  await new Promise(r => {
    let n = 0;
    for (const [f] of iframes) f.addEventListener('load', () => { if (++n === iframes.length) r(); });
    setTimeout(r, 12000);
  });
  for (const [f, b, p] of iframes) {
    try { const m = await messe(f, b, p); if (m) berichte.push(m); }
    catch (e) { berichte.push({ pfad: p, breite: b, fehler: String(e && e.stack || e) }); }
  }
  ausgabe.textContent = JSON.stringify(berichte, null, 1);
  } catch (e) {
    // Ein Stillstand wäre sonst nicht sichtbar: Fehler immer ausgeben.
    ausgabe.textContent = 'FEHLER ' + (e && e.stack || e) +
      '\ngemessen: ' + berichte.length;
  }
})();
"""

HARNESS = f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>Messung</title></head><body>
<pre id="ausgabe">läuft…</pre>
<script>const BREITEN={json.dumps(BREITEN)};const ZIELE={json.dumps(ZIELE)};const A4={json.dumps(list(A4_ZIELE))};</script>
<script>{MESS_JS}</script>
</body></html>"""


class StillerHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def end_headers(self):
        # Kein Caching, damit der frische Bau immer ankommt.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def hago_bauen(ziel):
    print(f"baue nach {ziel} …")
    subprocess.run(["hugo", "-D", "-d", ziel], cwd=REPO, check=True,
                   stdout=subprocess.DEVNULL)


def starte_server(versatz):
    handler = lambda *a, **kw: StillerHandler(*a, directory=versatz, **kw)
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


def chromium_dom(url):
    cmd = [
        "chromium", "--headless", "--no-sandbox", "--disable-gpu",
        "--hide-scrollbars", "--no-first-run", "--disable-extensions",
        "--virtual-time-budget=20000", "--dump-dom", url,
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    m = re.search(r'<pre id="ausgabe">(.*?)</pre>', out.stdout, re.S)
    if not m:
        raise SystemExit("Chromium lieferte keine Messung:\n"
                         + out.stdout[:2000] + out.stderr[:2000])
    roh = m.group(1)
    # HTML-Entities zurückdrehen, die Chromium beim Dump-DOM setzt.
    for alt, neu in (("&quot;", '"'), ("&#39;", "'"), ("&lt;", "<"),
                     ("&gt;", ">"), ("&amp;", "&")):
        roh = roh.replace(alt, neu)
    if not roh.lstrip().startswith("["):
        raise SystemExit("Messung abgebrochen:\n" + roh)
    return json.loads(roh)


def pruefe(b):
    fehler = []
    if b.get("fehler"):
        return [f"Messtechnik: {b['fehler']}"]
    if b["ueberlappung"] > 0:
        fehler.append(f"A2 Sprungleiste überlappt den Kopf um {b['ueberlappung']} px")
    if b["kopfHoehe"] and b["token"]:
        token = b["token"].removesuffix("px") if b["token"].endswith("px") else None
        if token and abs(float(token) - b["kopfHoehe"]) > 1.5:
            fehler.append(f"M1 Token {b['token']} weicht vom gemessenen Kopf "
                          f"{b['kopfHoehe']} px ab")
    if b["breite"] == 390 and b["kopfHoehe"] and b["kopfHoehe"] > 96:
        fehler.append(f"N1 Mobilkopf ist {b['kopfHoehe']} px hoch (Ziel ≤ 96)")
    if b["sprung"]:
        s = b["sprung"]
        if not s["ok"]:
            fehler.append(f"A1 Ankersprung: Ziel bei {s['top']} px, gebraucht "
                          f"{s['noetig']} px")
    # A4 gilt auf grobem Zeiger. Headless-Chromium meldet `pointer: coarse`
    # bei keiner Breite (nicht einmal `fine`), deshalb wird hier über die
    # Breite angenähert: die CSS-Regeln selbst stehen unter
    # `(pointer: coarse), (max-width: 640px)`, gelten also ab 640 px nach.
    if b["breite"] <= 640:
        for sel, m in (b["ziele"] or {}).items():
            soll = A4_ZIELE.get(sel)
            if soll and m["min"] < soll:
                fehler.append(f"A4 {sel} ist {m['min']} px hoch (Ziel ≥ {soll}, "
                              f"{m['n']} Stück, größtes {m['max']} px)")
    if b["breite"] == 390 and b["menue"] and not b["menue"]["krankmelden"]:
        fehler.append("N1 „Krankmelden“ fehlt im Mobilmenü")
        if b["menue"] and not b["menue"]["krankmelden"]:
            fehler.append("N1 „Krankmelden“ fehlt im Mobilmenü")
    return fehler


def main():
    public = os.path.join(REPO, "public")
    if "--bauen" in sys.argv or not os.path.isdir(public):
        hago_bauen(public)

    with tempfile.TemporaryDirectory(prefix="ghse-layout-") as tmp:
        # Bau kopieren: die Mess-Seite liegt im selben Verzeichnis und ist
        # damit gleicher Ursprung wie die gemessenen Seiten.
        for eintrag in os.listdir(public):
            quel = os.path.join(public, eintrag)
            ziel = os.path.join(tmp, eintrag)
            shutil.copytree(quel, ziel) if os.path.isdir(quel) else shutil.copy(quel, ziel)
        with open(os.path.join(tmp, "__harness.html"), "w", encoding="utf-8") as f:
            f.write(HARNESS)

        srv, port = starte_server(tmp)
        try:
            berichte = chromium_dom(f"http://127.0.0.1:{port}/__harness.html")
        finally:
            srv.shutdown()

    gesamt = 0
    for b in sorted(berichte, key=lambda x: (-x.get("breite", 0), x.get("pfad", ""))):
        fehler = pruefe(b)
        status = "OK  " if not fehler else "FAIL"
        kopf = f"Kopf {b.get('kopfHoehe')} px (Token {b.get('token')})"
        leiste = f", Überlappung {b.get('ueberlappung')} px"
        print(f'{status} {b.get("breite"):>4} px {b.get("pfad"):<44} {kopf}{leiste}')
        if b.get("sprung"):
            s = b["sprung"]
            print(f'      Ankersprung {s["id"]}: Ziel bei {s["top"]} px, '
                  f'benötigt {s["noetig"]} px')
        if b.get("ziele") and b.get("breite", 0) <= 640:
            z = {s: v for s, v in b["ziele"].items() if s in A4_ZIELE}
            if z:
                klein = min(z.items(), key=lambda kv: kv[1]["min"])
                print(f'      Touch-Ziele: kleinster {klein[1]["min"]} px '
                      f'({klein[0]}, {klein[1]["n"]} Stück, Ziel ≥ {A4_ZIELE[klein[0]]})')
        for fehler_text in fehler:
            print(f"      -> {fehler_text}")
        gesamt += len(fehler)

    print("Fehler gesamt:", gesamt)
    return 1 if gesamt else 0


if __name__ == "__main__":
    sys.exit(main())
