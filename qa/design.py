#!/usr/bin/env python3
"""Prüft den Umschalter der Gestaltungsvarianten im Browser.

Aufruf (Preview-Server muss laufen):
    python3 tools/preview-server.py public 8735
    python3 qa/design.py http://127.0.0.1:8735/

Geprüft wird: Einstieg ist Funktional, der Wechsel auf Klar setzt
`data-design`, speichert in localStorage und lädt Roboto; nach dem Neuladen
bleibt die Wahl; `?design=klar` öffnet Klar ohne zu speichern; der
Rückwechsel lädt wieder Hanken Grotesk bzw. Inter. Voraussetzung ist
Playwright mit Chromium (wie qa/klar_pruefung.py).
"""
import shutil
import sys

from playwright.sync_api import sync_playwright

BASIS = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8735").rstrip("/") + "/"


def browser_oeffnen(p):
    try:
        return p.chromium.launch()
    except Exception:
        exe = next((shutil.which(x) for x in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable") if shutil.which(x)), None)
        if not exe:
            raise
        return p.chromium.launch(executable_path=exe)


def zustand(page):
    return page.evaluate("""() => ({
      design: document.documentElement.getAttribute('data-design'),
      gespeichert: localStorage.getItem('ghse-design'),
      schrift: getComputedStyle(document.body).fontFamily,
      wahl: document.querySelector('.stilwahl--leiste select')?.value
    })""")


def pruefe(bedingung, name):
    if not bedingung:
        raise SystemExit("FEHLER: " + name)


def main():
    with sync_playwright() as p:
        browser = browser_oeffnen(p)
        try:
            ctx = browser.new_context(viewport={"width": 1440, "height": 900})
            page = ctx.new_page()
            page.goto(BASIS, wait_until="load")
            s = zustand(page)
            pruefe(s["design"] == "funktional", "Start ist nicht Funktional: %r" % s)
            pruefe("Hanken" in s["schrift"], "Funktional nutzt nicht Hanken Grotesk: %r" % s["schrift"])
            pruefe(s["wahl"] == "funktional", "Auswahl zeigt nicht Funktional: %r" % s["wahl"])

            page.select_option(".stilwahl--leiste select", "klar")
            page.wait_for_timeout(250)
            s = zustand(page)
            pruefe(s["design"] == "klar", "Wechsel auf Klar fehlt: %r" % s)
            pruefe(s["gespeichert"] == "klar", "Wahl nicht gespeichert: %r" % s)
            pruefe("Roboto" in s["schrift"], "Klar nutzt nicht Roboto: %r" % s["schrift"])

            page.reload(wait_until="load")
            page.wait_for_timeout(250)
            s = zustand(page)
            pruefe(s["design"] == "klar", "Wahl überlebt Neuladen nicht: %r" % s)
            pruefe(s["wahl"] == "klar", "Auswahl nach Neuladen falsch: %r" % s["wahl"])

            optionen = page.eval_on_selector_all(".stilwahl--leiste option", "els => els.map(e => e.value)")
            pruefe(optionen == ["neobrutalismus", "klar", "funktional", "modern"], "Theme-Optionen: %r" % optionen)

            page.select_option(".stilwahl--leiste select", "funktional")
            page.wait_for_timeout(250)
            s = zustand(page)
            pruefe(s["design"] == "funktional", "Wechsel auf Funktional fehlt: %r" % s)
            pruefe("Hanken" in s["schrift"], "Funktional nutzt nicht Hanken Grotesk: %r" % s["schrift"])
            pruefe(s["gespeichert"] == "funktional", "Funktional nicht gespeichert: %r" % s)

            page.select_option(".stilwahl--leiste select", "modern")
            page.wait_for_timeout(250)
            s = zustand(page)
            pruefe(s["design"] == "modern", "Wechsel auf Modern fehlt: %r" % s)
            pruefe("Familjen" in s["schrift"], "Modern nutzt nicht Familjen Grotesk: %r" % s["schrift"])

            page.select_option(".stilwahl--leiste select", "neobrutalismus")
            page.wait_for_timeout(250)
            s = zustand(page)
            pruefe(s["design"] == "neobrutalismus", "Rückwechsel fehlt: %r" % s)
            pruefe("Inter" in s["schrift"], "Rückwechsel nutzt nicht Inter: %r" % s)
            ctx.close()

            ctx2 = browser.new_context(viewport={"width": 1440, "height": 900})
            page2 = ctx2.new_page()
            page2.goto(BASIS + "?design=klar", wait_until="load")
            page2.wait_for_timeout(250)
            s = zustand(page2)
            pruefe(s["design"] == "klar", "?design=klar greift nicht: %r" % s)
            pruefe(s["gespeichert"] is None, "?design=klar speichert ungefragt: %r" % s)
            page2.goto(BASIS + "?design=modern", wait_until="load")
            page2.wait_for_timeout(250)
            s = zustand(page2)
            pruefe(s["design"] == "modern", "?design=modern greift nicht: %r" % s)
            ctx2.close()
        finally:
            browser.close()
    print("OK: vier Varianten, Speicherung, Neuladen und ?design=… funktionieren.")


if __name__ == "__main__":
    main()
