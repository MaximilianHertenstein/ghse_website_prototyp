#!/usr/bin/env python3
"""Bestandsschutz der vier vorhandenen Gestaltungsvarianten vor Theme 5.

Der Schutzstand wird beim Start von Theme 5 aus dem damaligen Arbeitsbaum
erzeugt (`--neu`) und danach nur noch geprüft. Er umfasst jede vorhandene
Datei unter `assets/`, `layouts/`, `content/` und `static/` sowie die
Theme-Registrierung in `hugo.toml`.

`hugo.toml` ist nicht byte-gleich geschützt: Theme 5 braucht dort genau
einen zusätzlichen `[[params.designs]]`-Block. Geprüft wird deshalb
semantisch – alle Einträge außer `params.designs` müssen gleich bleiben,
die ersten vier Designs müssen unverändert und in derselben Reihenfolge
stehen, und danach darf genau ein Eintrag `lesebuch` folgen.

Aufruf:
    python3 qa/theme5-guard.py            # prüfen
    python3 qa/theme5-guard.py --neu      # Schutzstand schreiben (nur vor Theme 5)
"""
import hashlib
import json
import subprocess
import sys
import tomllib
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
BASELINE = Path(__file__).resolve().parent / "theme5-baseline.json"
ORDNER = ("assets", "layouts", "content", "static")
THEME_ID = "lesebuch"


def git(*args):
    return subprocess.run(["git", *args], cwd=BASIS, check=True,
                          capture_output=True, text=True).stdout


def dateien():
    """Alle vorhandenen Dateien der geschützten Ordner, relativ zum Projekt."""
    liste = []
    for ordner in ORDNER:
        basis = BASIS / ordner
        if not basis.is_dir():
            continue
        for pfad in sorted(basis.rglob("*")):
            if pfad.is_file() and ".git" not in pfad.parts:
                liste.append(str(pfad.relative_to(BASIS)))
    return liste


def sha(pfad):
    return hashlib.sha256((BASIS / pfad).read_bytes()).hexdigest()


def snapshot():
    daten = {
        "base": git("rev-parse", "--short", "HEAD").strip(),
        "hinweis": "Schutzstand vor Theme 5; nur additiv ändern.",
        "files": {p: sha(p) for p in dateien()},
        "hugo_toml": (BASIS / "hugo.toml").read_text(encoding="utf-8"),
    }
    BASELINE.write_text(json.dumps(daten, indent=1, sort_keys=True) + "\n",
                        encoding="utf-8")
    print(f"Schutzstand {daten['base']} geschrieben: {len(daten['files'])} Dateien")


def ohne_designs(daten):
    kopie = {k: v for k, v in daten.items() if k != "params"}
    params = dict(daten.get("params", {}))
    params.pop("designs", None)
    kopie["params"] = params
    return kopie


def pruefen():
    daten = json.loads(BASELINE.read_text(encoding="utf-8"))
    fehler = []
    for pfad, soll in daten["files"].items():
        ziel = BASIS / pfad
        if not ziel.exists():
            fehler.append(f"fehlt: {pfad}")
        elif sha(pfad) != soll:
            fehler.append(f"geändert: {pfad}")

    alt = tomllib.loads(daten["hugo_toml"])
    neu = tomllib.loads((BASIS / "hugo.toml").read_text(encoding="utf-8"))
    alt_designs = alt.get("params", {}).get("designs", [])
    neu_designs = neu.get("params", {}).get("designs", [])
    if ohne_designs(neu) != ohne_designs(alt):
        fehler.append("hugo.toml: Änderung außerhalb von params.designs")
    if neu_designs[:len(alt_designs)] != alt_designs:
        fehler.append("hugo.toml: bestehende Design-Einträge verändert oder umsortiert")
    if len(neu_designs) != len(alt_designs) + 1:
        fehler.append(f"hugo.toml: {len(neu_designs)} Designs statt "
                      f"{len(alt_designs) + 1}")
    elif neu_designs[-1].get("id") != THEME_ID:
        fehler.append(f'hugo.toml: letzter Eintrag ist nicht "{THEME_ID}"')

    print(f"Schutzstand {daten['base']}: {len(daten['files'])} Dateien geprüft, "
          f"{len(alt_designs)} bestehende Designs")
    if fehler:
        print(f"Abweichungen: {len(fehler)}")
        for eintrag in fehler:
            print("  " + eintrag)
        sys.exit(1)
    print("Vier bestehende Varianten unverändert; hugo.toml nur additiv erweitert.")


if __name__ == "__main__":
    if "--neu" in sys.argv:
        snapshot()
    else:
        pruefen()
