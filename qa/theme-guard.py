#!/usr/bin/env python3
"""Schutzprüfung für die beiden bestehenden Gestaltungsvarianten.

Vergleicht alle vorhandenen Layouts, Assets, Inhalte und statischen Dateien
mit dem Stand `qa/theme-baseline.json` (Commit 8a9a82a). Neue Theme-Dateien
der Varianten „funktional“ und „modern“ sind nicht Teil der Baseline und
werden ignoriert; `hugo.toml` ist bewusst ausgenommen, weil dort nur die
beiden neuen Theme-Einträge additiv ergänzt wurden.

Aufruf:  python3 qa/theme-guard.py
Exit 1, sobald eine bestehende Datei fehlt oder sich inhaltlich ändert.
"""
import hashlib
import json
import sys
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
BASELINE = Path(__file__).resolve().parent / "theme-baseline.json"

# Vom Auftraggeber freigegeben: deutscher 404-Titel in baseof.html.
# Nur dieser neue Hash ist zugelassen; jede weitere Änderung schlägt fehl.
AUSNAHMEN = {"layouts/baseof.html": "ad77a9316aacff617680dd9603b4e7c3b27098a344e03e1dc70f9511e43e13b9"}


def main():
    daten = json.loads(BASELINE.read_text(encoding="utf-8"))
    fehler = []
    for datei, soll in daten["files"].items():
        pfad = BASIS / datei
        if not pfad.exists():
            fehler.append((datei, "fehlt"))
            continue
        ist = hashlib.sha256(pfad.read_bytes()).hexdigest()
        if ist != soll and AUSNAHMEN.get(datei) != ist:
            fehler.append((datei, "geändert"))
    print(f"Schutzstand {daten['base']}: {len(daten['files'])} Dateien geprüft")
    if fehler:
        print(f"Abweichungen: {len(fehler)}")
        for datei, art in fehler:
            print(f"  {art}: {datei}")
        sys.exit(1)
    print("Beide bestehenden Varianten sind unverändert (Inhalte, Layouts, Assets).")


if __name__ == "__main__":
    main()
