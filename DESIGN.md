---
name: GHSE-Farben
colors:
  primary: "#F8DC54"
  secondary: "#1060A0"
  success: "#1A9C5A"
  warning: "#EC7030"
  danger: "#B8430F"
  surface: "#FFFFFF"
  text: "#000000"
  neutral: "#F2F2F2"
typography:
  h1:
    fontFamily: "Inter"
    fontSize: 2.1rem
  body-md:
    fontFamily: "Inter"
    fontSize: 1.0625rem
  label-caps:
    fontFamily: "Inter"
    fontSize: 0.8125rem
  sourceScale: "13/15/17/19/27/34/43/77 px"
  weights: "100–900 (variable)"
rounded:
  sm: 0
  md: 0
spacing:
  sm: 4px
  md: 8px
  sourceScale: "4/8/12/16/24/32/48/64/80"
---

## Überblick

Neobrutalismus mit den Farben des GHSE-Logos: schwarze Konturen, harte
Schatten, weißes Papier und Gelb, Orange und Blau als Akzente. Die Typografie
ist eine einzige variable Inter-Datei in den Schnitten 100 bis 900.

## Grundlagen

- **Stil:** klar, kontrastreich, flächig; keine Verläufe, keine Rundungen.
- **Schrift:** Inter (variabel, selbst gehostet), Fließtext 1,0625 rem,
  H1 `clamp(2.1rem, 4.6vw, 3.5rem)`, H2 `clamp(1.7rem, 3.4vw, 2.6rem)`.
- **Gewichte:** 400 für Text, 700/800 für Labels, 900 für Überschriften.
- **Farben:** Gelb `#F8DC54`, Orange `#EC7030`, Blau `#1060A0` – die drei
  Farbwerte stehen so im GHSE-Logo, das Blau aus dem helleren Teil des
  Verlaufs (das dunkle Navy bleibt unbenutzt). Tieforange `#B8430F` für
  Fokusringe und Warnungen, Schwarz/Weiß als Basis.
- **Abstände:** 4/8/12/16/24/32/48/64/80 px, Container 1180 px,
  Lesespalte 760 px.

## Flächen und Farbe

- Alle Seitenabschnitte liegen auf derselben Papierfläche (`.band--papier`).
  Gelbe Vollflächen tragen nur einzelne Komponenten (Aktionen,
  `.kasten--gelb`, Hinweise), keine ganzen Seitenbänder.
- Gelb markiert Aktionen und Marker, Orange Struktur (Kicker, Kategorien,
  Linien), Blau Links und einzelne Sekundäraktionen.
- Schwarze 3-px-Rahmen und harte Schatten (6 px, klein 4 px) tragen die
  Kontur; Fokusringe sind 3 px tieforange mit 3 px Abstand.
- Dark Mode tauscht nur die Tokens (`--papier`, `--schrift`, `--rand`,
  `--link` …), nicht die Regeln. Gelbe Flächen behalten dunkle Schrift.

## Komponenten

- **Hero:** gelbes Schulnamen-Badge, große Überschrift, zwei Aktionen.
- **Kicker:** orange, Großbuchstaben, gesperrt; führt jede Sektion ein.
- **Karten:** weiß, schwarzer Rahmen, harter Schatten, Titel als Link.
- **Chips/Marken:** klein, Großbuchstaben; Teilzeitschularten orange,
  Vollzeitschularten gelb.
- **Buttons:** `btn--akzent` (gelb), `btn--geist` (transparent, schwarze
  Kontur), `btn--orange` (orange Fläche).

## Zustände (Pflicht für jedes interaktive Element)

- **default / hover:** Hover hebt um 2 px und lässt den Schatten weiter
  stehen (`translate(-2px, -2px)`); `:active` drückt auf den Schatten
  (`translate(4px, 4px)`, Schatten aus). Nicht nur die Farbe ändern.
- **focus-visible:** 3 px Ring in Tieforange mit 3 px Abstand, auf allen
  Flächen derselbe Token (`--orange-tief`).
- **disabled:** `.btn:disabled` und `[aria-disabled="true"]` senken das
  Erscheinungsbild ohne Grau-in-Grau-Kontrastverlust; Kontrollelemente
  zusätzlich per `disabled`/`aria-disabled` aus dem Fokus nehmen.
- **geöffnet (Mobilmenü):** `aria-expanded` am Knopf, `aria-controls` auf
  das Panel; der Zustand hängt am Element, nicht an einer Klasse allein.

## Barrierefreiheit (prüfbare Kriterien)

- Textkontrast ≥ 4,5:1, Grafik ≥ 3:1 in beiden Farbmodi – geprüft von
  `qa/kontrast.py` gegen die Tokens des Stylesheets (nicht gegen Kopien).
- Touch-Ziele ≥ 44 px (`qa/layout.py`), Tastaturpfad über die Sprungleiste,
  Fokus sichtbar an jedem interaktiven Element.
- `prefers-reduced-motion`: Bewegungen (Hover-Drehungen, Smooth-Scroll)
  abgeschaltet; Bilder mit beschreibendem `alt`, dekorative mit `alt=""`.

## Anti-Patterns

- Farben ohne Token („mal eben“ ein Hexwert in einer Komponente) – neue
  Farben kommen in `:root`/den dunklen Satz, sonst schweigt `kontrast.py`.
- Runde Ecken, Verläufe, weiche Schatten – der Stil lebt von Kante und
  hartem Schatten.
- Grau-auf-Grau-Sekundärtext: Sekundärtext steht in `--grau` nur auf
  Papier/Fläche, nie auf farbigen Flächen.
- Farbige Vollflächen-Bänder als Sektionshintergrund – Flächenfarbe gehört
  der Komponente (Chip, Knopf, Kasten), nicht der Sektion.

## QA-Checkliste (vor jedem Commit)

1. `hugo` baut ohne Warnung.
2. `python3 qa/kontrast.py` → 0 Fehler (Hell und Dunkel).
3. `python3 qa/linkcheck.py` → 0 Fehlschläge; `python3 qa/extlinkcheck.py`
   vor Veröffentlichung.
4. `python3 qa/layout.py` → 0 Fehler (Anker, Sprungleiste, Touch-Ziele).
5. `python3 qa/reflow.py` → 0 Überlauf über alle Seiten und Breiten.
6. Lighthouse mobil ≥ 98 Performance, 100 A11y/SEO
   (`tools/preview-server.py` als Server, kein Parallel-Chromium).
