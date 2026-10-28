#!/usr/bin/env python3
"""Unterpfad-Probe: derselbe Stand unter /ghse_website_prototyp/.

Das GitHub-Pages-Deployment liegt nicht unter "/", sondern unter
`/ghse_website_prototyp/` – dort greifen absolute Pfade (`/fonts/…`,
`/downloads/…`) nicht. Dieser Lauf baut dieselben Inhalte mit
`--baseURL /ghse_website_prototyp/` in einen Wegwerf-Ordner und prüft
dort Linkcheck, Reflow und Layoutmessung:

    python3 qa/unterpfad.py [basis]     (Standard: ghse_website_prototyp)
"""
import os
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIS = (sys.argv[1] if len(sys.argv) > 1 else "ghse_website_prototyp").strip("/")


def main():
    fehler = 0
    with tempfile.TemporaryDirectory(prefix="ghse-unterpfad-") as tmp:
        # Hugo schreibt den Bau direkt in das Ziel-Verzeichnis (der Basispfad
        # der baseURL steckt nur in den erzeugten Adressen). Für die Prüfung
        # den Bau deshalb unter <tmp>/<basis>/ ablegen:
        bau = tempfile.TemporaryDirectory(prefix="ghse-bau-")
        subprocess.run(
            ["hugo", "--cleanDestinationDir", "-d", bau.name, "--baseURL", f"/{BASIS}/"],
            cwd=REPO, check=True, stdout=subprocess.DEVNULL,
        )
        nest = os.path.join(tmp, BASIS)
        os.makedirs(nest)
        for eintrag in os.listdir(bau.name):
            os.rename(os.path.join(bau.name, eintrag), os.path.join(nest, eintrag))
        bau.cleanup()
        print(f"--- Linkcheck unter /{BASIS}/ ---")
        r = subprocess.run([sys.executable, os.path.join(REPO, "qa", "linkcheck.py"), tmp])
        fehler += r.returncode
        print(f"--- Reflow unter /{BASIS}/ ---")
        r = subprocess.run([sys.executable, os.path.join(REPO, "qa", "reflow.py"), tmp, "8733"])
        fehler += r.returncode
        print(f"--- Layout unter /{BASIS}/ ---")
        r = subprocess.run([sys.executable, os.path.join(REPO, "qa", "layout.py"), "--basis", BASIS])
        fehler += r.returncode
    print("Fehler gesamt:", fehler)
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
