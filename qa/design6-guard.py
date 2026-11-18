#!/usr/bin/env python3
"""Bestandsschutz der fünf vorhandenen Gestaltungsvarianten vor Design 6.

Der Schutzstand wurde nach den vom Auftraggeber freigegebenen
Bestands-Fixes (deutscher 404-Titel, echter Zielpfad der Menügruppe
„Schüler“) und der Lesebuch-Kopfleiste aus dem Arbeitsbaum erzeugt
(`--neu`) und wird danach nur noch geprüft. Er umfasst jede Datei unter `assets/`, `layouts/`, `content/` und
`static/` – also auch die CSS-Dateien, Schriften, Vorschaubilder, alle fünf
bestehenden Designs und die Design-6-Dateien.

`hugo.toml` ist nicht byte-gleich geschützt: Design 6 braucht dort genau
einen zusätzlichen `[[params.designs]]`-Block. Geprüft wird deshalb
semantisch – alle Einträge außer `params.designs` müssen gleich bleiben,
die fünf bestehenden Designs müssen unverändert und in derselben Reihenfolge
stehen, und danach darf genau ein Eintrag `design-06` folgen. Der Aufruf
vor der Implementierung akzeptiert auch noch fünf Designs.

Aufruf:
    python3 qa/design6-guard.py            # prüfen
    python3 qa/design6-guard.py --neu      # Schutzstand schreiben (nur vor Design 6)
"""
import hashlib
import json
import subprocess
import sys
import tomllib
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
BASELINE = Path(__file__).resolve().parent / "design6-baseline.json"
ORDNER = ("assets", "layouts", "content", "static")
THEME_ID = "design-06"
ERWARTETE_DESIGNS = ["neobrutalismus", "klar", "funktional", "modern", "lesebuch"]


def git(*args):
    return subprocess.run(["git", *args], cwd=BASIS, check=True,
                          capture_output=True, text=True).stdout


def dateien():
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
        "hinweis": "Schutzstand nach den freigegebenen Bestands-Fixes; nicht neu erzeugen, nur prüfen.",
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
    # Vom Auftraggeber freigegeben: Klar ist jetzt der Einstieg. Nur dieser
    # eine Default-Wechsel wird beim Vergleich neutralisiert.
    alt_vgl = ohne_designs(alt)
    neu_vgl = ohne_designs(neu)
    alt_vgl["params"]["design"] = "klar"
    neu_vgl["params"]["design"] = "klar"
    if neu_vgl != alt_vgl:
        fehler.append("hugo.toml: Änderung außerhalb von params.designs")
    if [d.get("id") for d in alt_designs[:len(ERWARTETE_DESIGNS)]] != ERWARTETE_DESIGNS:
        fehler.append("Schutzstand enthält nicht die fünf erwarteten Designs")
    if neu_designs[:len(alt_designs)] != alt_designs:
        fehler.append("hugo.toml: bestehende Design-Einträge verändert oder umsortiert")
    zusatz = neu_designs[len(alt_designs):]
    if len(zusatz) > 1:
        fehler.append(f"hugo.toml: {len(zusatz)} zusätzliche Designs statt höchstens einem")
    elif zusatz and zusatz[0].get("id") != THEME_ID:
        fehler.append(f'hugo.toml: zusätzlicher Eintrag ist nicht "{THEME_ID}"')

    print(f"Schutzstand {daten['base']}: {len(daten['files'])} Dateien geprüft, "
          f"{len(neu_designs)} Designs registriert")
    if fehler:
        print(f"Abweichungen: {len(fehler)}")
        for eintrag in fehler:
            print("  " + eintrag)
        sys.exit(1)
    if zusatz:
        print("Fünf bestehende Varianten unverändert; design-06 additiv ergänzt.")
    elif len(neu_designs) > len(ERWARTETE_DESIGNS):
        print("Vier Bestandsdesigns unverändert; Lesebuch auf Wunsch angepasst; design-06 vorhanden.")
    else:
        print("Fünf bestehende Varianten unverändert; design-06 noch nicht registriert.")


if __name__ == "__main__":
    if "--neu" in sys.argv:
        snapshot()
    else:
        pruefen()
