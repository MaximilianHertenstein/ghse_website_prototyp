#!/usr/bin/env python3
"""Browserprüfung der Variante „klar“ (siehe clean-DESIGN.md, Abschnitt 4 und 8).

Prüft in Chromium (Hell und Dunkel, 1440 und 390 px) an einer Stichprobe von
Seiten und misst in einem Sweep den waagerechten Überlauf aller Seiten bei
elf Breiten:

  - keine Versalien (text-transform)
  - keine Drehung (transform mit Rotation) und keine harten Schatten
  - keine Schrift unter 14 px
  - Zeigeziele (Links, Knöpfe außerhalb von Fließtext) mindestens 44 px hoch,
    außer sie haben eine unsichtbar vergrößerte Fläche (::after, absolut)
  - Text- und Linkkontrast mindestens 7:1 (große Schrift 4,5:1) gegen den
    tatsächlich dahinterliegenden Hintergrund
  - kein waagerechter Überlauf (320–1440 px)

Voraussetzung: Python-Paket playwright mit Chromium
    pip install playwright && playwright install chromium

Aufruf (Bau mit Basis-URL „/“; die Variante kommt über ?design=klar):
    hugo --baseURL / --minify --gc -d /tmp/klar
    python3 qa/klar_pruefung.py /tmp/klar            # Stichprobe + Sweep (einige Minuten)
    python3 qa/klar_pruefung.py /tmp/klar --schnell  # nur Stichprobe

Ausgabe: Befunde je Prüfung. Exit 1, wenn es Befunde gibt.
"""
import os
import shutil
import socket
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

BREITEN = [320, 360, 414, 480, 640, 768, 834, 1024, 1112, 1280, 1440]
KEIN_UEBERLAUF = "html,body{overflow-x:visible !important}"  # main.css klemmt mit overflow-x: clip

JS = r"""
() => {
  const r = {upper: [], rot: [], shadow: [], klein: [], ziel: [], kontrast: [], geprueft: 0};
  const sel = e => { let s = e.tagName.toLowerCase(); if (e.className && typeof e.className === 'string') s += '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.'); return s; };
  const sichtbar = e => { const b = e.getBoundingClientRect(), c = getComputedStyle(e); return b.width > 0 && b.height > 0 && c.visibility !== 'hidden' && c.display !== 'none' && c.opacity !== '0'; };
  const farbe = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return {r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1}; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const verh = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const misch = (v, h) => ({r: v.r * v.a + h.r * (1 - v.a), g: v.g * v.a + h.g * (1 - v.a), b: v.b * v.a + h.b * (1 - v.a), a: 1});
  const hintergrund = el => { const lagen = []; for (let e = el; e; e = e.parentElement) { const c = getComputedStyle(e); if (c.backgroundImage !== 'none') return null; const f = farbe(c.backgroundColor); if (f && f.a > 0) { lagen.push(f); if (f.a >= 1) break; } } let g = {r: 255, g: 255, b: 255, a: 1}; for (let i = lagen.length - 1; i >= 0; i--) g = misch(lagen[i], g); return g; };
  for (const el of document.body.querySelectorAll('*')) {
    if (!sichtbar(el)) continue;
    const cs = getComputedStyle(el);
    if (cs.textTransform === 'uppercase' || cs.textTransform === 'capitalize') r.upper.push(sel(el));
    const m = cs.transform.match(/matrix\(([^)]+)\)/);
    if (m) { const v = m[1].split(',').map(Number); if (Math.abs(v[1]) > 0.001 || Math.abs(v[2]) > 0.001) r.rot.push(sel(el) + ' ' + cs.transform); }
    if (cs.boxShadow !== 'none' && /-?\d+px -?\d+px 0px/.test(cs.boxShadow) && !/rgba\(0, 0, 0, 0\)/.test(cs.boxShadow)) r.shadow.push(sel(el) + ' ' + cs.boxShadow);
    const text = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim());
    if (text.length) {
      const px = parseFloat(cs.fontSize), probe = text[0].textContent.trim().slice(0, 28);
      if (px < 14) r.klein.push(sel(el) + ' ' + px + 'px "' + probe + '"');
      const v = farbe(cs.color), h = hintergrund(el);
      if (v && h) {
        r.geprueft++;
        const gross = px >= 24 || (px >= 18.66 && parseInt(cs.fontWeight) >= 700), v2 = misch(v, h), q = verh(v2, h);
        if (q < (gross ? 4.5 : 7)) r.kontrast.push(q.toFixed(2) + ' ' + sel(el) + ' "' + probe + '"');
      }
    }
    if ((el.tagName === 'A' || el.tagName === 'BUTTON') && !el.closest('p,.verborgen,.sprungmarke') && cs.display !== 'inline') {
      const b = el.getBoundingClientRect(), af = getComputedStyle(el, '::after');
      if (!(af.position === 'absolute' && af.content !== 'none') && (b.height < 44 || b.width < 44)) r.ziel.push(sel(el) + ' ' + Math.round(b.width) + 'x' + Math.round(b.height) + ' "' + (el.textContent || '').trim().slice(0, 22) + '"');
    }
  }
  r.ueberlauf = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  return r;
}
"""


def seiten(wurzel):
    gefunden = []
    for ordner, _, dateien in os.walk(wurzel):
        rel = os.path.relpath(ordner, wurzel)
        if "index.html" in dateien and not rel.startswith(("css", "bilder", "fonts", "js")):
            gefunden.append("/" if rel == "." else "/" + rel + "/")
    return sorted(gefunden)


def stichprobe(alle):
    wahl = ["/"]
    for fest in ("/news/", "/downloads/", "/unsere-schule/"):
        if fest in alle:
            wahl.append(fest)
    wahl += [s for s in alle if s.startswith("/schularten/") and s.count("/") == 3][:2]
    wahl += [s for s in alle if s.startswith("/news/") and s.count("/") == 3][:1]
    return wahl


def design_url(basis):
    trenner = "&" if "?" in basis else "?"
    return f"{basis}{trenner}design=klar"


def freier_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    schnell = "--schnell" in sys.argv
    if not args:
        sys.exit(__doc__)
    wurzel = os.path.abspath(args[0])
    alle = seiten(wurzel)
    probe = stichprobe(alle)
    port = freier_port()
    server = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "-d", wurzel],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    befunde = {}
    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch()
            except Exception:
                # Kein Playwright-Chromium installiert: das System-Chromium nehmen.
                exe = next((shutil.which(x) for x in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable") if shutil.which(x)), None)
                if not exe:
                    raise
                browser = p.chromium.launch(executable_path=exe)
            for modus in ("light", "dark"):
                for breite in (1440, 390):
                    ctx = browser.new_context(viewport={"width": breite, "height": 900}, color_scheme=modus)
                    pg = ctx.new_page()
                    for s in probe:
                        pg.goto(design_url(f"http://localhost:{port}{s}"), wait_until="load")
                        pg.add_style_tag(content=KEIN_UEBERLAUF)
                        pg.wait_for_timeout(250)
                        r = pg.evaluate(JS)
                        for art in ("upper", "rot", "shadow", "klein", "ziel", "kontrast"):
                            for x in r[art]:
                                befunde.setdefault(art, set()).add(f"{modus} {breite}px {s}: {x}")
                        if r["ueberlauf"] > 0:
                            befunde.setdefault("ueberlauf", set()).add(f"{modus} {breite}px {s}: {r['ueberlauf']} px")
                    ctx.close()
            print(f"Stichprobe: {len(probe)} Seiten x 2 Breiten x 2 Modi geprüft")
            if not schnell:
                n = 0
                for modus in ("light", "dark"):
                    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, color_scheme=modus)
                    pg = ctx.new_page()
                    for s in alle:
                        pg.goto(design_url(f"http://localhost:{port}{s}"), wait_until="domcontentloaded")
                        pg.add_style_tag(content=KEIN_UEBERLAUF)
                        for breite in BREITEN:
                            pg.set_viewport_size({"width": breite, "height": 900})
                            pg.wait_for_timeout(15)
                            n += 1
                            d = pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
                            if d > 0:
                                befunde.setdefault("ueberlauf", set()).add(f"{modus} {breite}px {s}: {d} px")
                    ctx.close()
                print(f"Sweep: {len(alle)} Seiten x {len(BREITEN)} Breiten x 2 Modi = {n} Kombinationen")
            browser.close()
    finally:
        server.terminate()
    namen = {"upper": "Versalien", "rot": "Drehung", "shadow": "harter Schatten", "klein": "Schrift < 14 px",
             "ziel": "Zeigeziel < 44 px", "kontrast": "Kontrast < 7:1", "ueberlauf": "waagerechter Überlauf"}
    for art, name in namen.items():
        liste = sorted(befunde.get(art, []))
        print(f"{name}: {len(liste)}")
        for x in liste[:8]:
            print("   ", x)
    sys.exit(1 if befunde else 0)


if __name__ == "__main__":
    main()
