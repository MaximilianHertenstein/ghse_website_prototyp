#!/usr/bin/env python3
"""Referenz- und Regressionsaufnahmen der Gestaltungsvarianten.

Nimmt für jede Variante dieselben Seiten bei denselben Breiten auf, immer
mit denselben Bedingungen: heller Modus, reduzierte Bewegung, Schriften
geladen, alle Bilder geladen (vorher einmal durchscrollen), fester
Viewport. Damit lassen sich zwei Läufe pixelgenau vergleichen
(`qa/themebilder.py ... --vergleich ALT NEU`).

Aufruf:
    python3 qa/themebilder.py --out /tmp/opencode/t5/refs \
        --themes neobrutalismus,klar,funktional,modern \
        --breiten 1440,1024,390

    python3 qa/themebilder.py --out NEU
    python3 qa/themebilder.py --vergleich /tmp/opencode/t5/refs /tmp/opencode/t5/neu

Voraussetzung: Playwright mit Chromium (wie qa/klar_pruefung.py).
"""
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

SEITEN = {
    "home": "/",
    "news": "/news/",
    "downloads": "/downloads/",
    "tg": "/schularten/technisches-gymnasium/",
    "schule": "/unsere-schule/",
    "artikel": "/news/den-naechsten-schritt-wagen/",
}
THEMES = ["neobrutalismus", "klar", "funktional", "modern", "lesebuch"]
BREITEN = [1440, 1024, 390]

BEREIT = """() => Promise.race([
  Promise.all([
    document.fonts ? document.fonts.ready : Promise.resolve(),
    ...[...document.images].filter(i => !i.complete).map(i => new Promise(r => {
      i.addEventListener('load', r, {once: true});
      i.addEventListener('error', r, {once: true});
    }))
  ]),
  new Promise(r => setTimeout(r, 3000))
])"""


def browser_oeffnen(p):
    try:
        return p.chromium.launch()
    except Exception:
        exe = next((shutil.which(x) for x in ("chromium", "chromium-browser",
                                              "google-chrome", "google-chrome-stable")
                    if shutil.which(x)), None)
        if not exe:
            raise
        return p.chromium.launch(executable_path=exe)


def aufnehmen(basis, ziel, themes, breiten, ruhe=True):
    from playwright.sync_api import sync_playwright
    ziel = Path(ziel)
    ziel.mkdir(parents=True, exist_ok=True)
    manifest = {}
    with sync_playwright() as p:
        b = browser_oeffnen(p)
        try:
            for theme in themes:
                for breite in breiten:
                    ctx = b.new_context(viewport={"width": breite, "height": 900},
                                        color_scheme="light")
                    seite = ctx.new_page()
                    if ruhe:
                        seite.emulate_media(reduced_motion="reduce")
                    for name, pfad in SEITEN.items():
                        url = f"{basis.rstrip('/')}/{pfad.lstrip('/')}"
                        sep = "&" if "?" in url else "?"
                        url = f"{url}{sep}design={theme}"
                        seite.goto(url, wait_until="load")
                        seite.wait_for_timeout(250)
                        # Lazy-Bilder laden: einmal bis unten und zurück.
                        seite.evaluate("""async () => {
                          const h = document.body.scrollHeight;
                          for (let y = 0; y < h; y += 600) {
                            window.scrollTo(0, y);
                            await new Promise(r => setTimeout(r, 40));
                          }
                          window.scrollTo(0, 0);
                        }""")
                        seite.evaluate(BEREIT)
                        seite.wait_for_timeout(150)
                        datei = ziel / f"{theme}-{name}-{breite}.png"
                        seite.screenshot(path=str(datei), full_page=True)
                        roh = datei.read_bytes()
                        manifest[datei.name] = {
                            "sha256": hashlib.sha256(roh).hexdigest(),
                            "bytes": len(roh),
                        }
                    ctx.close()
        finally:
            b.close()
    (ziel / "manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{len(manifest)} Aufnahmen in {ziel}")


def vergleichen(alt, neu):
    alt, neu = Path(alt), Path(neu)
    ma = json.loads((alt / "manifest.json").read_text(encoding="utf-8"))
    mn = json.loads((neu / "manifest.json").read_text(encoding="utf-8"))
    fehler = []
    for name, daten in ma.items():
        if name not in mn:
            fehler.append(f"fehlt: {name}")
        elif mn[name]["sha256"] != daten["sha256"]:
            fehler.append(f"abweichend: {name}")
    if fehler:
        print(f"Abweichungen: {len(fehler)} von {len(ma)}")
        for e in fehler:
            print("  " + e)
        sys.exit(1)
    print(f"Alle {len(ma)} Aufnahmen pixelgleich (SHA-256 der PNG-Datei).")


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--out")
    a.add_argument("--basis", default="http://127.0.0.1:8735")
    a.add_argument("--themes", default=",".join(THEMES))
    a.add_argument("--breiten", default=",".join(map(str, BREITEN)))
    a.add_argument("--vergleich", nargs=2, metavar=("ALT", "NEU"))
    args = a.parse_args()
    if args.vergleich:
        vergleichen(*args.vergleich)
        return
    if not args.out:
        a.error("--out fehlt")
    aufnehmen(args.basis, args.out,
              [t for t in args.themes.split(",") if t],
              [int(b) for b in args.breiten.split(",") if b])


if __name__ == "__main__":
    main()
