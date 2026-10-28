#!/usr/bin/env python3
"""Alle Quellpaare auf einmal prüfen und den Befund gegen die README abgleichen.

Aufruf:  python3 qa/paare.py          (aus dem Repository-Stammverzeichnis)

Jede der zweiunddreißig Seiten hat ihre eigene Originalseite, die Namen decken
sich aber nicht (das Original liegt unter `/schueler/beratung-2/`, bei uns
heißt die Seite `schulsozialarbeit`). Die Paare stehen deshalb hier explizit;
für einzeln Nachzuprüfendes sind das die beiden Argumente, die `qa/treue.py`
und `satzpruefung.py` verlangen. Siebenundzwanzig Quellen liegen als HTML vor,
fünf als Text (Markdown- oder Rohtext-Aufzeichnung); beide Formen lesen dieselbe
Wortfolge.

Abgezogen werden, was kein Textbefund ist:
  * Zuordnungs-Artefakte – ein Wortglied, das beidseitig vorkommt, aber an
    einer anderen Stelle steht, weil der Vergleich verrutscht ist;
  * die eigene Meta-Beschreibung (allgemein in Abschnitt 3 dokumentiert);
  * die Download-Größen, die Hugo beim Build aus der Datei ermittelt;
  * zwei Restfetzen der Vorlage („Anfahrt Maps Anrufen Krank“, „Uhr“), die
    zu kurz sind, um sie wie den übrigen Kopf- und Fußblock zu filtern;
  * Aufzeichnungs-Vermerke und Word-Reste („QUELLE saferspace“, der
    Microsoft-Word-Kopf „Normal 0 21 false …“), die in keiner Fassung der
    Seite stehen.

Was übrig bleibt, muss in README Abschnitt 3 als „alt“ → „neu“ zitiert
stehen – sonst beendet sich das Skript mit einem Befund und zeigt die
fehlenden Stellen. Ein sehr langer Löschblock (ein Reiter, den die Quelle
zweimal führt) wird nur mit seinen ersten zehn Wörtern gegen die README
geprüft; ein solcher Block wird dort mit seinem Anfang zitiert.
"""
import difflib
import re
import sys

sys.path.insert(0, "qa")
import treue  # noqa: E402

PAARE = [
    ("content/anfahrt.md", "recherche/quellen/anfahrt.html"),
    ("content/anmeldeformulare.md", "recherche/quellen/anmeldeformulare.html"),
    ("content/av-dual-begleitung.md", "recherche/quellen/av-dual.html"),
    ("content/beratungssystem.md", "recherche/quellen/beratung.html"),
    ("content/besser-ghse.md", "recherche/quellen/besserghse.html"),
    ("content/bewo.md", "recherche/bewo-roh.md"),
    ("content/datenschutz.md", "recherche/datenschutz.md"),
    ("content/die-ghse.md", "recherche/quellen/die-ghse.html"),
    ("content/erasmus.md", "recherche/quellen/erasmus.html"),
    ("content/fachgruppen.md", "recherche/quellen/fachgruppen.html"),
    ("content/berufsinformation.md", "recherche/quellen/berufsinformation.html"),
    ("content/foerderverein.md", "recherche/quellen/foerderverein.html"),
    ("content/impressum.md", "recherche/impressum.md"),
    ("content/krankmeldung.md", "recherche/quellen/online-abmelden.html"),
    ("content/schulleben.md", "recherche/quellen/schueler-schulleben-lehrer.html"),
    ("content/nextcloud.md", "recherche/quellen/nextcloud.html"),
    ("content/mint.md", "recherche/quellen/mint.html"),
    ("content/praktikum-fuer-studierende.md",
     "recherche/praktikum-fuer-studierende-roh.md"),
    ("content/projekte-und-software.md", "recherche/quellen/projekte.html"),
    ("content/schularten/berufsvorbereitende-schularten/av-dual.md",
     "recherche/quellen/bv-av-dual.html"),
    ("content/schularten/berufsvorbereitende-schularten/vabo.md",
     "recherche/quellen/bv-vabo.html"),
    ("content/schularten/berufsvorbereitende-schularten/vabkf.md",
     "recherche/quellen/bv-vabkf.html"),
    ("content/schularten/berufsvorbereitende-schularten/bve.md",
     "recherche/quellen/bv-bve.html"),
    ("content/saferspace.md", "recherche/saferspace-roh.md"),
    ("content/schulbienen.md", "recherche/quellen/schulbienen.html"),
    ("content/schulsanitaetsdienst.md", "recherche/quellen/schulsanitaet.html"),
    ("content/schulsozialarbeit.md", "recherche/quellen/schulsozialarbeit.html"),
    ("content/smv.md", "recherche/quellen/smv.html"),
    ("content/studienfahrten.md", "recherche/quellen/studienfahrten.html"),
    ("content/unesco-aktivitaeten.md", "recherche/quellen/unesco.html"),
    ("content/unesco.md", "recherche/quellen/unesco-washeisst.html"),
    ("content/vertretungsplan.md", "recherche/quellen/vertretungsplan.html"),
]

VORLAGE = r"\b(uhr|aktuelles|anfahrt maps anrufen krank)\b"
AUFZEICHNUNG = (r"\b(quelle saferspace"
                r"|normal 0 21 false false false de x-none x-none)\b")
LANG = 15      # ab wie vielen Wörtern nur noch der Anfang zitiert wird
KOPF = 10      # wie viele Wörter des Anfangs dann verglichen werden


def w_woerter(wort):
    return [x.lower() for x in wort.split()]


def anzahl(seq, glied):
    return sum(1 for i in range(len(seq)) if seq[i:i + len(glied)] == glied)


def readme_woerter():
    """README als Wortfolge: Umbruch-Bindestriche zusammen, dann worte()."""
    t = open("README.md", encoding="utf-8").read().lower().replace("\n", " ")
    return treue.worte(re.sub(r"-\s+", "-", t))


def enthaelt(seq, glied):
    if not glied:
        return True
    return any(seq[i:i + len(glied)] == glied
               for i in range(len(seq) - len(glied) + 1))


def frontmatter(datei, schluessel):
    t = open(datei, encoding="utf-8").read()
    m = re.search(r'^%s:\s*"(.*)"\s*$' % schluessel, t, flags=re.M)
    return m.group(1) if m else ""


def quellwoerter(datei: str):
    """Wortfolge der Quelle – HTML über lxml, Text aus der Aufzeichnung.

    Die fünf Textquellen (Impressum, Datenschutz, BewO, Praktikum, Safer
    Space) liegen als Markdown bzw. als Rohtext vor. Linkziele und
    HTML-Kommentare fliegen raus, damit nur die sichtbaren Wörter zählen.
    """
    if datei.endswith(".html"):
        return treue.ohne_chrome(treue.worte(treue.quelltext(datei)),
                                 treue.chrome_menge())
    t = open(datei, encoding="utf-8").read()
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"<([^>]+)>", r"\1", t)
    return treue.ohne_chrome(treue.worte(t), treue.chrome_menge())


def abweichungen(q, m):
    """Wortabweichungen zwischen Quelle und eigener Seite."""
    raus = []
    sm = difflib.SequenceMatcher(a=q, b=m, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        alt, neu = " ".join(q[i1:i2]), " ".join(m[j1:j2])
        if treue.nur_satzzeichen(alt, neu) or treue.nur_kern(alt, neu):
            continue                      # reine Interpunktion, siehe Modultext
        if re.search(VORLAGE, alt) or re.search(VORLAGE, neu):
            continue                      # Restfetzen der Vorlage
        if re.search(AUFZEICHNUNG, alt) or re.search(AUFZEICHNUNG, neu):
            continue                      # Aufzeichnungs- und Word-Reste
        if "datei en" in alt or "datei en" in neu:
            continue                      # Download-Größe, der Build rechnet sie
        glied_a, glied_m = w_woerter(alt), w_woerter(neu)
        if tag == "insert" and anzahl(m, glied_m) <= anzahl(q, glied_m):
            continue                      # Paarungs-Artefakt
        if tag == "delete" and anzahl(q, glied_a) <= anzahl(m, glied_a):
            continue                      # Paarungs-Artefakt
        raus.append((tag, alt, neu))
    return raus


def main():
    readme = readme_woerter()
    unbekannt, summe = [], 0

    for md, quelle in PAARE:
        q = quellwoerter(quelle)
        m = treue.worte(treue.eigener_text(md))
        # Die eigene Meta-Beschreibung folgt im Vergleichstext auf den Titel
        # und ist allgemein in Abschnitt 3 dokumentiert.
        beschreibung = [w.lower() for w in
                        treue.worte(frontmatter(md, "description"))]
        start = len(treue.worte(frontmatter(md, "title")))
        if beschreibung and \
                [w.lower() for w in m[start:start + len(beschreibung)]] == beschreibung:
            del m[start:start + len(beschreibung)]
        q, m = [w.lower() for w in q], [w.lower() for w in m]

        raus = abweichungen(q, m)
        summe += len(raus)
        print(f"{md:40} {len(raus):3} Abweichungen")
        for tag, alt, neu in raus:
            pruef_a, pruef_n = w_woerter(alt), w_woerter(neu)
            if len(pruef_a) > LANG:       # langer Löschungsblock: Anfang genügt
                pruef_a = pruef_a[:KOPF]
            if tag == "insert":
                drin = enthaelt(readme, pruef_n)
            elif tag == "delete":
                drin = enthaelt(readme, pruef_a)
            else:
                drin = enthaelt(readme, pruef_a) or enthaelt(readme, pruef_n)
            if not drin:
                unbekannt.append((md, tag, alt, neu))

    print(f"\nSumme: {summe} Abweichungen, davon {len(unbekannt)} nicht "
          f"in README Abschnitt 3 zitiert\n")
    for md, tag, alt, neu in unbekannt:
        if tag == "replace":
            print(f"  {md}\n      {alt!r}\n   -> {neu!r}")
        elif tag == "delete":
            print(f"  {md}\n      fehlt bei uns: {alt!r}")
        else:
            print(f"  {md}\n      bei uns neu:  {neu!r}")
    return 1 if unbekannt else 0


if __name__ == "__main__":
    sys.exit(main())
