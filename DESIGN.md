---
name: GHSE – zwei Gestaltungsvarianten
colors:
  primary: "#F6DC56"
  secondary: "#114C92"
  success: "#1A9C5A"
  warning: "#EE7330"
  danger: "#B8430F"
  surface: "#FFFFFF"
  text: "#000000"
  neutral: "#FFFFFF"
typography:
  h1:
    fontFamily: "Inter"
    fontSize: 2.1rem
  body-md:
    fontFamily: "Inter"
    fontSize: 1.0625rem
  weights: "100–900 (variabel)"
rounded:
  sm: 0
  md: 0
spacing:
  sm: 4px
  md: 8px
---

## Überblick

Dieselben Seiten, Inhalte und URLs gibt es in zwei Gestaltungsvarianten.
Beide nutzen dieselben Hugo-Templates; nur das Aussehen wechselt.

| Variante | Aussehen | Dokument |
| --- | --- | --- |
| **Neobrutalismus** (Standard) | GHSE-Gelb/Orange/Blau, schwarze Konturen, harte Schatten, Inter | `Neobrutalismus-DESIGN.md` |
| **Klar** (Clean) | viel Weißraum, Roboto/Poppins, Blau als einziger Akzent, keine Schatten | `clean-DESIGN.md` |

## Umschaltung

- `params.designs` in `hugo.toml` listet die Varianten mit `id`, `name`,
  `kurz`, optional `css` und `fonts`.
- `layouts/baseof.html` setzt `data-design` am `<html>` vor dem ersten
  Bild (localStorage `ghse-design`, sonst `params.design`). Die
  Standardvariante braucht keine Zusatz-CSS.
- Der Umschalter (`_partials/stilwahl.html`) steht ab 1101 px in der
  Kopfleiste, bis 1100 px im Menü. `assets/js/design.js` schaltet um,
  speichert die Wahl und hält beide Menüs synchron.
- `?design=klar` öffnet eine Variante ohne zu speichern (QA, Teilen).
- **Drittes Theme:** Eintrag in `params.designs`, eine CSS-Datei, deren
  Regeln unter `:root[data-design="<id>"]` stehen, und bei eigenen
  Schriften ein Partial in `fonts`. Templates und Skript bleiben
  unverändert.

## Gemeinsame Grundlage

- Eine Seitenstruktur, eine Navigation, ein Inhaltsbestand; keine
  Variante erfindet Inhalte oder Ziele.
- Jede Variante prüft ihre eigenen Kontrast- und Lesbarkeitswerte
  (`qa/kontrast.py` für Neobrutalismus, `qa/kontrast_klar.py` für Klar).
- Farbe und Schrift sind pro Variante über Tokens gesetzt; Komponenten
  lesen nur Tokens, keine Rohwerte.
