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

- Alle Seitenabschnitte liegen auf derselben Papierfläche (`.band--papier`,
  auf der Startseite `.band--blau` für die beiden Feed-Sektionen mit blauen
  Sekundärknöpfen). Gelbe Vollflächen tragen nur einzelne Komponenten
  (Aktionen, `.kasten--gelb`, Hinweise), keine ganzen Seitenbänder.
- Gelb markiert Aktionen und Marker, Orange Struktur (Kicker, Kategorien,
  Linien), Blau Links und einzelne Sekundäraktionen.
- Schwarze 3-px-Rahmen und harte Schatten (6 px, klein 4 px) tragen die
  Kontur; Fokusringe sind 3 px tieforange mit 3 px Abstand.
- Dark Mode tauscht nur die Tokens (`--papier`, `--schrift`, `--rand`,
  `--link` …), nicht die Regeln. Gelbe Flächen behalten dunkle Schrift.

## Komponenten (Anatomie, Varianten, Zustände)

- **Hero:** gelbes Schulnamen-Badge, große Überschrift, Abschluss-Chips;
  die Wege führen über die Kopfnavigation, die Sektionen und den
  „Alle Schularten"-Knopf.
- **Knöpfe (`btn`):** Varianten `--akzent` (gelb), `--geist`
  (transparent, schwarze Kontur), `--klein` (z. B. in Download-Zeilen und
  Hinweisen). Zustände: hover hebt 2 px, `:active` drückt auf den
  Schatten, disabled über `aria-disabled`. Label ist ein Verb mit Ziel
  („Alle Schularten", „Mehr erfahren →"), nie „Hier klicken".
- **Chips (`chip`):** kleine Großbeschriftung; `--akzent` (gelbe Fläche)
  für Hauptpfade, `--ruhig` für Sekundäres, `--klein` in Meta-Zeilen.
  Teilzeit orange, Vollzeit gelb (über `data-kategorie`).
- **Karten (`karte`):** `karte__bild` (16:10, unten Rahmen), `karte__koerper`
  mit Marke, Titel als einzigem Link (`karte__link`), Text und Aktion;
  hover/:focus-within hebt 3 px, Fokusring über `:has()`. Varianten:
  `--gross` (erste Meldung), `--text` (ohne Bild), `--news`. Die Aktion
  („Mehr erfahren") trägt die Akzentfarbe der Karte als **Unterstrich**,
  nicht als Textfarbe – Gelb auf Weiß ist 1,36:1, Orange 3,03:1, als Text
  unlesbar.
- **Zeilen (`zeile`, Downloads):** Titel, Metadaten (Tabellenziffern),
  Aktion rechts; unter 640 px Vollbreite mit vollem Knopf.
- **Bilder im Fließtext (`bild`, Shortcode):** 26rem breit (gut zwei Drittel
  der Lesespalte), zentriert, schwarzer Rahmen mit Versatzschatten;
  `breite="voll"` über die ganze Lesespalte. Stehen mehrere Bilder
  unmittelbar nebeneinander, ordnet sie das Raster der Liste
  (`.fliesstext ul:has(> li .bild)`) nebeneinander an – ab 15rem
  Spaltenbreite zwei Spalten, sonst untereinander; die Pfeilzeichen der
  Aufzählung entfallen dort. Die natürliche Breite steht als Variable
  (`--breite`) im Bild: kleine Originale (Porträts, Logos) werden nicht
  hochskaliert, und die Größe ist vor dem Laden bekannt, damit der Text
  beim Nachladen nicht springt. Gallerien mit Bildunterschrift nutzen
  `bilder` (Front Matter), alle Bilder 4:3 im Raster.
- **Hinweise (`hinweis`, Shortcode):** blasse Gelbfläche
  (`--hinweis-flaeche`), Titel als Kicker, optional ein
  `btn--geist btn--klein` mit Ziel; Variante `--warnung` (rote Fläche,
  Tieforange-Rand).
- **Kalender-Karten (`kalender`):** Name plus Aktionsspalte; ganzflächig
  klickbar, hover/focus heben 3 px mit größerem Schatten wie die Karten.
- **Menü (Kopf):** acht Kategorien mit Tafeln; ab 1200 px aufklappend
  (hover/`:focus-within`), darunter Panel mit einklappbaren Kategorien
  (Pfeilknopf, `aria-expanded`). Aktiver Pfad als blauer Block mit weißer
  Schrift (`aria-current="page"`).
- **Werte-Quadrate (`wert__marke`, Shortcode):** reine Grafik, mit
  `aria-hidden`; die Beschriftung daneben trägt die Aussage – Farbe allein
  vermittelt keine Bedeutung. Sechs Farben, „Vielfalt" als Streifen.

## Text und Ton

- **Labels eindeutig:** Knöpfe und Links benennen das Ziel („Alle
  Meldungen", „Mehr erfahren →"); Pfeile und ↗ als `aria-hidden`-Zier,
  nicht als einzige Information.
- **Kicker:** zwei bis drei Wörter, Großbuchstaben, ordnen die Sektion
  ein („Bildungsangebote", „Schuljahresplaner") – kein Werbetext.
- **Kurzfassungen:** erste Aussage der Quelle, bei Instagram mit „…"
  gekappt, ohne Emojis und Hashtags; nichts erfinden, keine Zahlen
  ergänzen, die die Quelle nicht nennt.
- **Alt-Texte:** beschreiben das Bild für jemanden, der es nicht sieht
  (Konstellation, Schriftzüge wörtlich), statt „Bild" oder Dateiname.

## Responsiv

- **Ab 1200 px:** Dropdown-Tafeln im Kopfmennü (CSS-only, hover und
  `:focus-within`), Zeile und Adresse sichtbar.
- **Unter 1199 px:** die Navigation wird zum Aufklappmenü (`.menueknopf`,
  Panel mit `aria-expanded`, scrollbar, `overscroll-behavior: contain`).
- **Unter 1000 px:** Karten- und Zeilenraster stapeln; Hero einspaltig,
  Bild versetzt den Schatten nach unten.
- **Unter 900 px:** Adressleiste aus, Kopfhöhe schrumpft auf 4,5 rem,
  Schnellzugriff wandert ins Menüpanel, Modusknopf ohne Schrift.
- **Unter 640/560 px:** Typo-Skala abschwächen (Fließtext 1,02 rem),
  Karten-, Zeilen-, Kalender- und Fußraster einspaltig, Buttons mehrzeilig
  fähig (`white-space: normal`) und aktionsbreit, Wertequadrat-Raster
  einspaltig; Touch-Ziele bleiben ≥ 44 px.
- **Kantenfälle:** Raster mit `minmax(0, 1fr)` (kein Überlauf durch lange
  Wörter), Buttons umbrechen mehrzeilig statt zu kneifen, Longtexte über
  `text-wrap: balance` in Überschriften. Geprüft von `qa/reflow.py`
  (alle Seiten × 11 Breiten) und `qa/layout.py` (1440/640/390).

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
7. Nach Token-Änderungen: Dark-Mode-Sichtprobe – Kopie von `public/` mit
   `data-theme="dark"` am `<html>` ansehen (Achtung: `nav.js` setzt den
   Modus am laufenden Dokument, im Testkopie den Anfangs-`stelle()`-Aufruf
   überspringen).
8. `python3 qa/unterpfad.py` – derselbe Stand unter
   `/ghse_website_prototyp/` (Bau mit `--baseURL`, dann Linkcheck, Reflow
   und Layoutmessung im Wegwerf-Verzeichnis). Fängt genau die Fehler, die
   unter "/" unsichtbar bleiben: Schriften und alle Inhalts-Links brechen
   unter dem GitHub-Pages-Unterpfad, wenn ein Pfad nicht durch `relURL`
   läuft.
