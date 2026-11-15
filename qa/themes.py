#!/usr/bin/env python3
"""Browserprüfung aller vier Gestaltungsvarianten.

Aufruf (Preview-Server muss laufen):
    python3 tools/preview-server.py public 8735
    python3 qa/themes.py http://127.0.0.1:8735/

Geprüft werden für jede Variante (Neo, Klar, Funktional, Modern):
  - data-design wird gesetzt, die Variante ist wählbar
  - kein waagerechter Überlauf bei 1440/1024/768/390 px
  - bei den neuen Varianten: keine Versalien, keine Drehung
  - Schriftgrößen mindestens 14 px
  - Textkontrast mindestens 4,5:1 (große Schrift 3:1)
  - Zeigeziele außerhalb von Fließtext mindestens 24 px hoch (mobil)
  - genau vier Theme-Optionen im Umschalter

Voraussetzung: Playwright mit Chromium (wie qa/klar_pruefung.py).
Exit 1 bei Befunden.
"""
import shutil
import sys

from playwright.sync_api import sync_playwright

BASIS = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8735").rstrip("/") + "/"
SEITEN = ["/", "/downloads/", "/schularten/technisches-gymnasium/", "/news/besuch-aus-china/", "/404.html"]
THEMES = ["neobrutalismus", "klar", "funktional", "modern"]
NEU = {"funktional", "modern"}
BREITEN = [1440, 1024, 768, 390, 320]
KEIN_UEBERLAUF = "html,body{overflow-x:visible !important}"

JS = r"""
() => {
  const sichtbar = e => {
    const b = e.getBoundingClientRect(), c = getComputedStyle(e);
    return b.width > 0 && b.height > 0 && c.visibility !== 'hidden' && c.display !== 'none' && c.opacity !== '0';
  };
  const farbe = c => {
    const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);
    return {r:p[0], g:p[1], b:p[2], a:p.length > 3 ? p[3] : 1};
  };
  const lum = c => { const f = v => { v /= 255; return v <= .03928 ? v/12.92 : Math.pow((v+.055)/1.055, 2.4); }; return .2126*f(c.r)+.7152*f(c.g)+.0722*f(c.b); };
  const verh = (a,b) => { const x=lum(a), y=lum(b); return (Math.max(x,y)+.05)/(Math.min(x,y)+.05); };
  const misch = (v,h) => ({r:v.r*v.a+h.r*(1-v.a), g:v.g*v.a+h.g*(1-v.a), b:v.b*v.a+h.b*(1-v.a), a:1});
  const hintergrund = el => {
    const lagen = [];
    for (let e = el; e; e = e.parentElement) {
      const c = getComputedStyle(e);
      if (c.backgroundImage !== 'none') return null;
      const f = farbe(c.backgroundColor);
      if (f && f.a > 0) { lagen.push(f); if (f.a >= 1) break; }
    }
    let g = {r:255,g:255,b:255,a:1};
    for (let i=lagen.length-1; i>=0; i--) g = misch(lagen[i], g);
    return g;
  };
  const r = {upper:0, rot:0, klein:0, ziel:0, kontrast:0, text:0, ziele:0, details:[]};
  for (const el of document.body.querySelectorAll('*')) {
    if (!sichtbar(el)) continue;
    const cs = getComputedStyle(el);
    const eigen = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (eigen) {
      r.text++;
      if (cs.textTransform === 'uppercase') r.upper++;
      const px = parseFloat(cs.fontSize);
      if (px < 14) { r.klein++; if (r.details.length < 8) r.details.push('klein ' + px + 'px ' + (el.className || el.tagName)); }
      const fg = farbe(cs.color), bg = hintergrund(el);
      if (fg && bg) {
        const schwell = (px >= 24 || (px >= 18.66 && parseInt(cs.fontWeight, 10) >= 700)) ? 3 : 4.5;
        const q = verh(fg, bg);
        if (q < schwell) { r.kontrast++; if (r.details.length < 8) r.details.push('kontrast ' + q.toFixed(2) + ' ' + (el.className || el.tagName)); }
      }
    }
    const t = cs.transform;
    if (t && t !== 'none') {
      const m = t.match(/matrix\(([^)]+)\)/);
      if (m) { const v = m[1].split(',').map(Number); if (Math.abs(v[1]) > 0.01 || Math.abs(v[2]) > 0.01) r.rot++; }
    }
    if (el.matches('button,select,summary,.btn,.chip,.menueknopf,.modusknopf,.stilwahl__auswahl,.leiste__schnell a,.menue a')) {
      r.ziele++;
      if (el.getBoundingClientRect().height < 24) {
        r.ziel++; if (r.details.length < 8) r.details.push('ziel ' + Math.round(el.getBoundingClientRect().height) + 'px ' + (el.className || el.tagName));
      }
    }
  }
  r.ueberlauf = Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - document.documentElement.clientWidth;
  return r;
}
"""


def browser_oeffnen(p):
    try:
        return p.chromium.launch()
    except Exception:
        exe = next((shutil.which(x) for x in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable") if shutil.which(x)), None)
        if not exe:
            raise
        return p.chromium.launch(executable_path=exe)


def main():
    befunde = []
    with sync_playwright() as p:
        browser = browser_oeffnen(p)
        try:
            ctx = browser.new_context(viewport={"width": 1440, "height": 900})
            page = ctx.new_page()
            page.goto(BASIS + "?design=funktional", wait_until="load")
            optionen = page.eval_on_selector_all(".stilwahl--leiste option", "els => els.map(e => e.value)")
            if optionen != THEMES:
                befunde.append("Theme-Optionen: %r" % optionen)
            ctx.close()

            for theme in THEMES:
                for breite in BREITEN:
                    ctx = browser.new_context(viewport={"width": breite, "height": 900})
                    page = ctx.new_page()
                    for seite in SEITEN:
                        page.goto(f"{BASIS}{seite.lstrip('/')}?design={theme}", wait_until="load")
                        page.add_style_tag(content=KEIN_UEBERLAUF)
                        page.wait_for_timeout(120)
                        r = page.evaluate(JS)
                        ist = page.evaluate("document.documentElement.getAttribute('data-design')")
                        if ist != theme:
                            befunde.append(f"{theme} {breite} {seite}: data-design={ist}")
                        if theme in NEU and r["ueberlauf"] > 1:
                            befunde.append(f"{theme} {breite} {seite}: Überlauf {r['ueberlauf']} px")
                        if theme in NEU:
                            if r["upper"]:
                                befunde.append(f"{theme} {breite} {seite}: {r['upper']} Versalien")
                            if r["rot"]:
                                befunde.append(f"{theme} {breite} {seite}: {r['rot']} Drehungen")
                            if r["klein"]:
                                befunde.append(f"{theme} {breite} {seite}: {r['klein']} Texte < 14 px")
                            if r["kontrast"]:
                                befunde.append(f"{theme} {breite} {seite}: {r['kontrast']} Kontraste < 4,5:1")
                            if r["ziel"] and breite == 390:
                                befunde.append(f"{theme} {breite} {seite}: {r['ziel']} Ziele < 24 px")
                            for d in r["details"][:3]:
                                befunde.append(f"    {theme} {breite} {seite}: {d}")
                    ctx.close()
            print(f"Geprüft: {len(THEMES)} Varianten x {len(SEITEN)} Seiten x {len(BREITEN)} Breiten")
        finally:
            browser.close()
    if befunde:
        print("Befunde:", len(befunde))
        for b in befunde[:40]:
            print("   ", b)
        sys.exit(1)
    print("Alle vier Varianten ohne Befund.")


if __name__ == "__main__":
    main()
