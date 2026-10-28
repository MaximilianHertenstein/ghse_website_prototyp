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
