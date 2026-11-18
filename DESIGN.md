---
name: GHSE – sechs Gestaltungsvarianten
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

Dieselben Seiten, Inhalte und URLs gibt es in sechs Gestaltungsvarianten.
Alle nutzen dieselben Hugo-Templates; nur das Aussehen wechselt.

| Variante | Kennung | Aussehen | Dokument |
| --- | --- | --- | --- |
| **Neobrutalismus** | `neobrutalismus` | GHSE-Gelb/Orange/Blau, schwarze Konturen, harte Schatten, Inter | `Neobrutalismus-DESIGN.md` |
| **Klar** (Clean, Einstieg) | `klar` | viel Weißraum, Roboto/Poppins, Blau für Text/Aktionen, Orange für Linien, Gelb für Flächen, keine Schatten | `clean-DESIGN.md` |
| **Funktional** | `funktional` | Weiß/Schwarz, Hanken Grotesk, GHSE-Logofarben nur als Akzente, flache Kästen, harte Linien, keine Schatten | `funktional-DESIGN.md` |
| **Modern** | `modern` | Marineblau/GHSE-Blau/Gelb/Orange, Familjen Grotesk, weiße Karten auf hellem Blau, weiche Schatten | `modern-DESIGN.md` |
| **Lesebuch** | `lesebuch` | Graugrünes Papier, blaue Kopfleiste als Verzeichnis, Piazzolla/Public Sans, Tafeln und Haarlinien statt Karten | `lesebuch-DESIGN.md` |
| **Wegweiser** | `design-06` | GHSE-Blauverlauf als Wand, weiße Emailschilder, gelbe Zielwege, Archivo, Standortleiste und Spezifikationsetiketten | `design-06-DESIGN.md` |

## Sechste Variante: Wegweiser

Die sechste Variante ist eine eigenständige Designwelt, keine Ableitung der
fünf bestehenden. Sie überträgt die Beschilderung eines Schulgebäudes auf die
Website: tiefblauer GHSE-Verlauf als Wand, weiße Schilder, gelbe Pfeile und
Registerlaschen, Orange als Standortmarke. Archivo ist die einzige Schrift;
die GHSE-Originalfarben `#222D71`, `#006AB4`, `#EE7330` und `#F6DC56` bleiben
unverändert, ergänzt um ein dokumentiertes Blauspektrum.

- Kennung: `design-06`; sichtbarer Name „Wegweiser“; Kurzform „Wegw.“.
- CSS: `assets/css/design-06.css`; Schrift: `layouts/_partials/schriften-design06.html`; Dokumentation: `design-06-DESIGN.md`.
- Die fünf bestehenden Varianten, ihre CSS-Dateien, Layouts, Inhalte und
  Dokumentationen bleiben unverändert.
- Critique, Polish und Audit: `design-06-CRITIQUE.md`, `design-06-AUDIT.md`.

## Umschaltung

- `params.designs` in `hugo.toml` listet die Varianten mit `id`, `name`,
  `kurz`, optional `css` und `fonts`.
- `layouts/baseof.html` setzt `data-design` am `<html>` vor dem ersten
  Bild (localStorage `ghse-design`, sonst `params.design`). Ohne
  gespeicherte Wahl startet die Seite in `funktional`; Neo steht in
  `main.css` und braucht keine eigene CSS-Datei.
- Der Umschalter (`_partials/stilwahl.html`) steht ab 1101 px in der
  Kopfleiste, bis 1100 px im Menü. `assets/js/design.js` schaltet um,
  speichert die Wahl und hält beide Menüs synchron.
- `?design=klar` öffnet eine Variante ohne zu speichern (QA, Teilen).
- **Weiteres Theme:** Eintrag in `params.designs`, eine CSS-Datei, deren
  Regeln unter `:root[data-design="<id>"]` stehen, und bei eigenen
  Schriften ein Partial in `fonts`. Templates und Skript bleiben
  unverändert. Die CSS-Datei wird automatisch mitgeladen.

## Gemeinsame Grundlage

- Eine Seitenstruktur, eine Navigation, ein Inhaltsbestand; keine
  Variante erfindet Inhalte oder Ziele.
- Jede Variante prüft ihre eigenen Kontrast- und Lesbarkeitswerte
  (`qa/kontrast.py` für Neobrutalismus, `qa/kontrast_klar.py` für Klar,
  `qa/themes.py` für alle vier im Browser).
- Farbe und Schrift sind pro Variante über Tokens gesetzt; Komponenten
  lesen nur Tokens, keine Rohwerte.
