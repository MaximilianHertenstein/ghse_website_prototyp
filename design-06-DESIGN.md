# GHSE – Gestaltungsvariante „Wegweiser“ (Design 6)

**Technische Kennung:** `design-06`  
**Sichtbarer Name:** Wegweiser  
**Kurzform im Umschalter:** Wegw.  
**Stand:** 16. November 2026  
**Status:** implementiert, geprüft, nicht committet und nicht veröffentlicht

---

## 1. Gestalterische Grundidee

**Die GHSE als begehbares Schulhaus.** Eine Besucherin steht im Foyer, liest
das Verzeichnis und findet ihren Weg. Die Seite ist eine Beschilderung, kein
Kartenkatalog: tiefblauer GHSE-Verlauf als Wand, weiße Emailschilder,
gelbe Pfeile und Registerlaschen, Orange als Standortmarke.

Die Startseite ist das **Foyer** der Schule:

- Der vollständige Schulname steht als Lagezeile in einer blauen Leiste.
- Die H1 „Wir machen Schule für alle“ ist der größte Text der Seite.
- Die fünf Abschlüsse sind echte Zielzeilen über die volle Panelbreite,
  keine dekorativen Sticker.
- Das Schulgebäude mit dem gelben Übergang ist das gerahmte Sichtfenster –
  ohne zusätzliche Bildzeile.
- Der Hero bleibt bewusst ohne zusätzliche Plakette und ohne Pfeil; die
  blauen Zielzeilen und das Sichtfenster tragen die Komposition.
- „Alle Schularten“ ist der gelbe Primärweg; die vier vorhandenen
  Schulartkarten sind die ersten Ziele.

Die Innenseiten setzen dieselbe Sprache ruhiger fort: Brotkrumen als
Wegzeile, Schulart-Details als Spezifikationsblatt mit gelbem
„Auf einen Blick“-Etikett, Downloads als Dokumentzeilen, News als Aushänge,
404 als blaue Wegtafel.

### Direction Contract

| Block | Inhalt |
| --- | --- |
| **Thesis** | Die GHSE als begehbares Schulhaus: Foyer, Verzeichnis, Weg. Die Seite verweigert den üblichen Split-Hero mit Kartenreihe. |
| **Own-World** | GHSE-Blauverlauf als Wand, weiße Schilder mit 1-px-Kante, gelbe Pfeile, Orange als Standortmarke, Archivo, tabellarische Ziffern. |
| **Story** | „Ich bin hier richtig. Diese Schule führt vom Hauptschulabschluss bis zum Abitur, und ich kann meinen Weg direkt wählen.“ |
| **First Viewport** | Links das weiße Standort-Panel mit Schulname, H1, Leitsatz und fünf Abschlusszielen; rechts das Gebäude als Sichtfenster; kein zusätzlicher Pfeil, keine Plakette. Auf 390 px: Panel, Ziele, Foto. |
| **Form** | Wegweiser, Position 1 der nach Resonanz geordneten Liste; Seed-Referenz `seed:260e25ab6884aefe`. Das Musterbuch bleibt als dokumentierte Alternative erhalten. |
| **Finish** | „unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance.“ |

Der vollständige Direction Contract liegt im Surface Brief
`.impeccable/surfaces/home.md`.

### Warum diese Richtung

Die Hauptzielgruppe sind Jugendliche am Ende der Sekundarstufe I und ihre
Eltern. Sie kommen mit einer konkreten Frage: *Welcher Abschluss, welcher
Weg, welche Schule?* Der Wegweiser beantwortet diese Frage direkter als eine
materialästhetische oder dokumentarische Metapher. Das Schulgebäude ist ein
echter lokaler Anker; die fünf Abschlüsse und acht Schularten sind die
eigentliche Information. Die Gestaltung ordnet sich dieser Klarheit unter.

---

## 2. Abgrenzung zu den fünf Bestandsdesigns

| Bestand | Was Wegweiser bewusst nicht übernimmt |
| --- | --- |
| **Neobrutalismus** | keine schwarzen Konturen, keine harten Versätze, keine Sticker, kein Gelb als ganze Seite |
| **Klar** | kein hellblaues Weißraum-Raster, keine runden Karten, keine Roboto/Poppins |
| **Funktional** | kein Schwarzweiß-Handbuch, keine 1-px-Kästen ohne Fläche, keine Hanken Grotesk |
| **Modern** | keine weißen Karten auf hellblauem Grund, keine weichen Schatten, keine Familjen Grotesk, kein runder Hero |
| **Lesebuch** | keine Serif, kein fester linker Rücken, kein Buchrücken, keine graugrüne Papierstimmung |

Die Eigenständigkeit liegt in der **räumlichen Ordnung**: blaue Wand,
weiße Schilder, gelbe Wegmarken, Archivo, ein Verzeichnis statt einer
Kartenwand. Die fünf Bestandsdesigns bleiben unverändert; der Schutz ist
über 704 Dateihashes und 150 pixelgleiche Referenzaufnahmen belegt.

---

## 3. Farbkonzept

### 3.1 Die vier GHSE-Originalfarben

Diese Werte sind unverändert und bilden die verbindliche Markenbasis:

| Rolle | HEX | RGB | Verwendung |
| --- | --- | --- | --- |
| GHSE Dunkelblau | `#222D71` | 34, 45, 113 | Einband, Kopfleiste, Überschriften, Primärflächen |
| GHSE Blau | `#006AB4` | 0, 106, 180 | Verlaufspol, Links, aktive Flächen, Fokus auf Papier |
| GHSE Orange | `#EE7330` | 238, 115, 48 | Standortmarke, Materialkante, Hover, Signal |
| GHSE Gelb | `#F6DC56` | 246, 220, 86 | Zielzeilen, Registerlaschen, Primärwege, Fokus auf Blau |

### 3.2 Erweitertes Blauspektrum

Die beiden Blauanker sind keine Beschränkung; das Spektrum zwischen und um
sie ist Teil des Systems. Alle Werte sind abgeleitet und dokumentiert:

| Token | Wert | Verwendung |
| --- | --- | --- |
| `--d6-blue-950` | `#080F26` | tiefster Grund, Fußleiste, Dunkelmodus |
| `--d6-blue-900` | `#101A4A` | Einbandgrund, Nutzleiste, Fuß |
| `--d6-blue-850` | `#141F55` | Registerflächen |
| `--d6-blue-800` | `#18245C` | Verlaufsmitte |
| `--d6-blue-700` | `#222D71` | Original, Primär |
| `--d6-blue-650` | `#1B3A74` | aktive Fläche |
| `--d6-blue-600` | `#174C96` | Verlauf, Links auf Papier |
| `--d6-blue-500` | `#0F57A0` | Hover, Linien |
| `--d6-blue-400` | `#006AB4` | Original, Verlaufspol |
| `--d6-blue-300` | `#2E8BCB` | Grafiken, dunkle Flächen |
| `--d6-blue-200` | `#8FC2E6` | Text auf dunklem Grund |
| `--d6-blue-100` | `#D6E8F5` | heller Hinweis |
| `--d6-blue-50` | `#EEF6FB` | hellster Hauch |

### 3.3 Semantische Tokens, hell

| Token | Wert | Verwendung |
| --- | --- | --- |
| `--d6-ground` | `#EDF1F5` | Seitengrund |
| `--d6-ground-2` | `#E3E9F0` | Bänder, Register |
| `--d6-panel` | `#FFFFFF` | Schilder, Karten, Zeilen |
| `--d6-panel-2` | `#F7F9FB` | Hinweise, Terminnotiz |
| `--d6-ink` | `#101828` | Text, Überschriften |
| `--d6-on-yellow` | `#101828` | Text und Ränder auf Gelb/Orange |
| `--d6-heading` | `#222D71` | Überschriften, Titel |
| `--d6-soft` | `#4A5568` | Zweittext, Daten |
| `--d6-line` | `#C9D3DF` | Haarlinien, Rahmen |
| `--d6-line-strong` | `#8FA1B6` | bedienbare Ränder |
| `--d6-blue-text` | `#0F4C8A` | Links auf hellem Grund |
| `--d6-orange-text` | `#A8430F` | Orangetext mit AA |
| `--d6-yellow-soft` | `#FBEFA8` | Hinweisfläche |
| `--d6-success` | `#1F6B45` | Erfolg |
| `--d6-warning` | `#8A4B00` | Warnung |
| `--d6-danger` | `#A32A1A` | Fehler |
| `--d6-focus` | `#B8430F` | Fokus auf Papier |
| `--d6-focus-on-blue` | `#F6DC56` | Fokus auf Blau und Dunkel |

### 3.4 Semantische Tokens, dunkel

| Token | Wert | Verwendung |
| --- | --- | --- |
| `--d6-ground` | `#080E1C` | Seitengrund |
| `--d6-ground-2` | `#0D1527` | Bänder |
| `--d6-panel` | `#101A2E` | Schilder, Karten |
| `--d6-panel-2` | `#14203A` | Hinweise, Notizen |
| `--d6-ink` | `#F2F5FA` | Text |
| `--d6-on-yellow` | `#101828` | Text und Ränder auf Gelb/Orange |
| `--d6-heading` | `#D6E4F7` | Überschriften |
| `--d6-soft` | `#B7C4D8` | Zweittext |
| `--d6-line` | `#26344C` | Haarlinien |
| `--d6-line-strong` | `#3C4E6B` | bedienbare Ränder |
| `--d6-blue-text` | `#8FC2E6` | Links auf dunklem Grund |
| `--d6-orange-text` | `#F09A6B` | Orangetext mit AA |
| `--d6-focus` | `#F6DC56` | Fokus auf Dunkel |
| `--d6-focus-on-blue` | `#F6DC56` | Fokus auf Blau |
| `--d6-shadow` | `0 18px 40px -28px rgba(0,0,0,.8)` | weiche Tiefe |

### 3.5 Farbverläufe

```css
--d6-wall: linear-gradient(
  135deg,
  #101A4A 0%,
  #18245C 28%,
  #222D71 52%,
  #174C96 78%,
  #006AB4 100%
);

--d6-wall-dark: linear-gradient(
  135deg,
  #060B16 0%,
  #0B1638 42%,
  #10254D 100%
);
```

Der Verlauf trägt:

- den Hero und die 404-Wegtafel,
- das Termine-Band,
- den Fuß,
- die blauen Registerflächen.

Er steht **nie** hinter kleinem Fließtext ohne ausreichend dunklen
Verlaufsbereich. Die hellste Stelle `#006AB4` hat mit Weiß 5,64:1; der
Leitsatz auf dem Band nutzt `rgba(255,255,255,.92)` und erreicht 5,03:1.
Gelb und Orange werden nicht als Verlaufsgrund für Text verwendet.

### 3.6 Kontrastwerte

| Kombination | Verhältnis | Bewertung |
| --- | --- | --- |
| `#101828` auf `#F6DC56` | 12,92:1 | AAA |
| `#101828` auf `#EE7330` | 6,03:1 | AA |
| `#0F4C8A` auf `#FFFFFF` | 8,67:1 | AAA |
| `#4A5568` auf `#FFFFFF` | 7,53:1 | AAA |
| `#101828` auf `#EDF1F5` | 15,64:1 | AAA |
| `#FFFFFF` auf `#222D71` | 12,49:1 | AAA |
| `#FFFFFF` auf `#006AB4` | 5,64:1 | AA |
| `#F6DC56` auf `#222D71` | 9,09:1 | AAA |
| `#D6E4F7` auf `#101A2E` | 13,48:1 | AAA |
| `#F2F5FA` auf `#080E1C` | 17,63:1 | AAA |
| `#B7C4D8` auf `#080E1C` | 10,92:1 | AAA |
| `#8FC2E6` auf `#080E1C` | 10,12:1 | AAA |
| `#B8430F` auf `#EDF1F5` | ca. 5,2:1 | AA |
| `#F6DC56` auf `#101A4A` | 9,09:1 | AAA |

Der vollständige Kontrast-Sweep über 83 Seiten in hell und dunkel ergab
**0 Textkontrast-Fehler**. Die gelbe Datumsmarke, die gelben Download-
Buttons und das gelbe „Auf einen Blick“-Etikett tragen in beiden Modi
dunkle Schrift (`#101828`).

### 3.7 Komponentenbezogene Farbregeln

| Komponente | Fläche | Schrift | Kante / Marke |
| --- | --- | --- | --- |
| Nutzleiste | `#101A4A` | `#F2F5FA` | gelbe Unterstreichung |
| Kopf | `#FFFFFF` | `#101828` | `#C9D3DF`; aktive Fläche `#222D71` |
| Hero-Panel | `#FFFFFF` | `#101828` / `#222D71` | `#8FA1B6`; Standort Orange |
| Hero-Wand | Blauverlauf | Weiß | gelbe Pfeile, orange Marke |
| Schulartkarte | `#FFFFFF` | `#101828` / `#222D71` | gelbe bzw. orange Kategorie |
| News-Aushang | `#222D71` / `#F6DC56` / `#EE7330` | Weiß bzw. `#101828` | 1-px-Linie |
| Download-Zeile | `#FFFFFF` | `#101828` | `#C9D3DF`; Button Gelb |
| Spezifikationskarte | `#F6DC56` | `#101828` | Kopf `#222D71` |
| Termine | Blauverlauf | Weiß | weiße Schilder |
| Fuß | `#101A4A` | `#F2F5FA` | gelbe Titel, gelbe Oberkante |
| 404 | Blauverlauf | Weiß | weiße Schilder, gelber Primärweg |
| Fokus | – | – | `#B8430F` auf Papier, `#F6DC56` auf Blau/Dunkel |

---

## 4. Typografie

**Archivo** – variabel, `wght 100–900`, `wdth 62–125`, SIL Open Font
License 1.1, selbst gehostet unter `assets/fonts/design-06/`. Die Datei ist
88 KB (Latin-Subset), `font-display: swap`, kein Preload, keine externe
Font-CDNs.

| Rolle | Schnitt | Größe | Zeile | Einsatz |
| --- | --- | --- | --- | --- |
| Display / H1 | 800, `wdth 118` | `clamp(2,9rem, 5,6vw, 4,7rem)` | 0,94 | Hero, Seitenkopf |
| H2 | 800, `wdth 112` | `clamp(1,8rem, 3,2vw, 2,6rem)` | 1,0 | Abschnitte |
| H3 | 750, `wdth 106` | `clamp(1,15rem, 1,5vw, 1,4rem)` | 1,12 | Karten, Zeilen |
| Fließtext | 400, `wdth 100` | 1,0625 rem | 1,7 | Lesespalte |
| Labels | 700, `wdth 100` | 0,875 rem | 1,4 | Schilder, Register |
| Daten | 650, tabellarisch | 0,875 rem | 1,4 | Datum, Größe, Nummer |

- **Lesebreite:** 64ch im Fließtext, 46ch im Leitsatz, 52ch in Karten.
- **Spationierung:** Display `-0,035em`, Überschriften `-0,02em`,
  Labels `0,04em`. Keine künstliche Sperrung von Fließtext.
- **Fallback:** `"Archivo", "Arial Narrow", "Helvetica Neue", Arial,
  sans-serif`.
- **Ziffern:** `font-variant-numeric: tabular-nums` für Datum, Größe,
  Nummern und Kalender.
- **Umbruch:** `text-wrap: balance` für Überschriften, `pretty` für
  Absätze, `hyphens: auto` im Fließtext (aus der Grundlage).
- **Mindestgröße:** 14 px für sichtbaren Text; alle gerenderten
  Textknoten wurden in beiden Modi geprüft.

---

## 5. Design-Tokens

Die vollständigen Tokens stehen im Token-Block von
`assets/css/design-06.css`. Die wichtigsten:

### Farbe

```css
:root[data-design="design-06"] {
  --d6-navy: #222d71;
  --d6-blue: #006ab4;
  --d6-orange: #ee7330;
  --d6-yellow: #f6dc56;
  --d6-ground: #edf1f5;
  --d6-panel: #ffffff;
  --d6-ink: #101828;
  --d6-on-yellow: #101828;
  --d6-heading: #222d71;
  --d6-soft: #4a5568;
  --d6-line: #c9d3df;
  --d6-line-strong: #8fa1b6;
  --d6-blue-text: #0f4c8a;
  --d6-orange-text: #a8430f;
  --d6-focus: #b8430f;
  --d6-focus-on-blue: #f6dc56;
  --d6-wall: linear-gradient(135deg, #101a4a 0%, #18245c 28%,
             #222d71 52%, #174c96 78%, #006ab4 100%);
}
```

### Typografie und Raster

```css
--d6-font: "Archivo", "Arial Narrow", "Helvetica Neue", Arial, sans-serif;
--t-display: clamp(2.9rem, 5.6vw, 4.7rem);
--t-h1: clamp(2.2rem, 4.4vw, 3.4rem);
--t-h2: clamp(1.8rem, 3.2vw, 2.6rem);
--t-h3: clamp(1.15rem, 1.5vw, 1.4rem);
--t-xs: 0.875rem;
--t-s: 0.9375rem;
--t-m: 1.0625rem;
--container: 1200px;
--schmal: 760px;
```

### Tiefe und Form

```css
--d6-shadow: 0 18px 40px -28px rgba(16, 24, 40, 0.45);
--d6-shadow-soft: 0 10px 28px -22px rgba(16, 24, 40, 0.35);
--d6-radius: 2px;
```

Es gibt **keine harten Offset-Schatten** außerhalb der
Neobrutalismus-Welt. Die Schilder stehen auf 1-px-Kanten; die weiche Tiefe
ist nur für schwebende Panels (Hero, Menü, 404) reserviert. Karten und
Zeilen bleiben flach.

**Linien:** Alle sichtbaren Rahmen und Trennlinien sind **1 px**. Die
früheren 2-/3-px-Akzente an Ticket, Hinweis, Überschriften, Kartenaktion,
Service-Kante, Video-Knopf und Footer-Titel wurden auf dasselbe Maß
gebracht. Der Fokusring bleibt als eigener Zugänglichkeitszustand 3 px.

---

## 6. Aufbau und Komponenten

### 6.1 Nutzleiste und Kopf

- **Nutzleiste:** dunkelblau, 44 px, Adresse/Telefon links, Schnellzugriffe
  rechts, Stilwahl und Farbmodus. Die Schnellzugriffe sind 28 px hoch
  (Sekundärziele; WCAG 24 px eingehalten).
- **Kopf:** weißes Schild, 76 px, freigestelltes Logo als transparentes WebP ohne weiße Platte, Hauptnavigation
  rechts. Aktive Seite als navyfarbene Platte mit weißer Schrift;
  Hover als gelbe Platte.
- **Krankmelden:** ab 1200 px in der Nutzleiste, darunter als gelber Knopf
  im Kopf (44 px).
- **Mobile:** Menüknopf mit sichtbarem „Menü“ ab 360 px, sonst Icon;
  Panel als weißes Verzeichnis, Untermenüs klappen über den Pfeil auf.
- **Stilwahl:** nativer Select; `kurz = "Wegw."`, vollständiger Name
  „Wegweiser“ als Optionstitel. Der kurze Wert schützt die pixelgleiche
  Breite der fünf Bestandsdesigns; „Wegweiser“ würde die Kopfzeile von
  Funktional und Modern verschieben.

### 6.2 Hero / Standortpanel

- 7/5-Grid auf Desktop; Panel und Sichtfenster sind weiße Schilder.
- Schulname als blaue Lagezeile mit orangem Standortquadrat.
- H1 in displayweitem Archivo, navy, max. 12ch.
- Leitsatz 43ch; Terminnotiz als Papierkarte mit gelber Oberkante.
- Fünf Abschlüsse als Zielzeilen über die volle Panelbreite; 44 px hoch;
  Orange-Tick links, Pfeil rechts; Hover verlängert den Tick und schiebt
  den Pfeil.
- Keine zusätzliche Standortplakette und kein Pfeil; die Abschlusszeilen und das Sichtfenster tragen die Komposition.
- Gebäude als gerahmtes Sichtfenster ohne Bildzeile.
- Auf ≤1199 px stapeln Panel und Bild, beide max. 46rem und zentriert.

### 6.3 Schularten / Zielschilder

- Startseite: vier vorhandene Karten (bestehender Inhalt), 2 Spalten.
- Übersicht: Gruppen Vollzeit/Teilzeit, 2 oder 3 Spalten je nach Anzahl.
- Karte: weißes Schild, 1-px-Linie, 16:10-Bild, Kategorie-Lasche
  (Gelb = Vollzeit, Orange = Teilzeit), Titel, Text, „Mehr erfahren“ mit
  gelber Unterstreichung.
- Hover: 3 px anheben, Bild 1,025 skalieren, Rahmen navy; Reduced Motion
  setzt alles zurück.
- „Alle Schularten“ ist auf der Startseite ein gelber Primärweg.

### 6.4 News / Aushänge

- Bildmeldungen: farbiger Aushang (Navy, Gelb, Orange im Wechsel) mit
  Datum/Quelle, großer Schlagzeile, Teaser und „Meldung lesen“.
- Textmeldungen: weißes Schild mit Quelle, großem Datum, Titel, Teaser.
- Featured-Karte: volle Breite, 21:9-Bild bzw. großer Aushang.
- Detailseite: Meta-Zeile mit gelbem Datumsbadge und
  „Zeitungsausschnitt“-Etikett; Scan als gerahmte Tafel mit
  „Vergrößern“-Plakette unten rechts; Bildunterschrift und Quelle.
- Die „Vergrößern“-Plakette sitzt innerhalb des Bildes und überdeckt
  keine Bildunterschrift.

### 6.5 Downloads / Dokumentzeilen

- Sprungleiste: navy, gelbe Kategoriebeschriftung, weiße Kategorie-Schilder;
  sticky unter dem Kopf, auf schmalen Geräten eine Zeile mit horizontalem
  Scroll.
- Dokumentzeile: weiß, 1-px-Linie, Titel/Beschreibung links, Format/Größe
  und gelber „Herunterladen“-Button rechts; auf ≤768 px gestapelt.
- PDF/DOC/ZIP und Größe als kleine Schilder, keine erfundenen Daten.

### 6.6 Schulart-Detail / Spezifikationsblatt

- Brotkrumen als Wegzeile mit Pfeilen; H1; Lead; Lesespalte 64ch.
- Mobile Sidebar vor dem Text, Desktop Sidebar rechts und sticky.
- „Auf einen Blick“: gelbes Spezifikationsetikett mit navyfarbenem Kopf,
  Fakten (Schulart, Abschluss/Ziel), „Alle Downloads“, Sekretariat.
- Galerie als Ansichtsband: 4 Spalten ab 1200 px, 3 bis 768 px, 2 darunter;
  alle Bilder bleiben im DOM und in Lesereihenfolge.
- Downloads zu diesem Bildungsgang als eigener Kasten mit Dokumentzeilen.

### 6.7 Service, Hinweise, Bilder

- Service-Karten: weiße Merkblätter mit gelber 1-px-Oberkante, Titel, Text und
  Textlink; 2 Spalten, mobil 1.
- Hinweise: weißes Merkblatt mit gelber Oberkante, kein dicker Seitenbalken.
- Werte: farbige Quadrate aus der bestehenden Leitbild-Palette; Text trägt
  die Bedeutung, Farbe ist nie allein.
- Bilder: 1-px-Rahmen, keine Drehung, keine harten Schatten.
- Video: gerahmtes Vorschaubild, gelber Play-Knopf mit dunklem Dreieck,
  Dateilink; keine automatische Wiedergabe.

### 6.8 Fuß

- Navyflächen mit gelber Oberkante; vier Spalten (Kontakt, Sekretariat,
  Service, Rechtliches), gelbe Titel mit gelber Haarlinie, weiße Links.
- Fußleiste dunkler, Copyright, 24-px-Ziele für Listenlinks.

### 6.9 404

- Blaue Wegtafel mit weißer H1 und weißem Leitsatz.
- Weiße Schilder für die sechs vorhandenen Ziele; „Zur Startseite“ ist der
  gelbe Primärweg; „Krankmelden“ ist dort nur ein weißes Schild.
- Fällt in Browsern ohne `:has` auf den normalen weißen Seitenkopf zurück;
  die Funktion bleibt erhalten.

### 6.10 Zustände

| Zustand | Regel |
| --- | --- |
| Hover | 3 px anheben, Rahmen navy, Bild 1,025; bei Schildern Gelb/Orange |
| Fokus | 3 px, `#B8430F` auf Papier, `#F6DC56` auf Blau/Dunkel; Offset 3 px (Sidebar 2 px) |
| Aktiv | aktive Navigation navy mit weißer Schrift; `aria-current` bleibt |
| Auswahl | gelbe Fläche, dunkle Schrift |
| Reduced Motion | Übergänge 0,01 ms, Karten/Bilder/Pfeile ohne Transform, `scroll-behavior: auto` |
| Print | weiße Fläche, schwarze Schrift, Kopf/Fuß/Werkzeuge ausgeblendet |

---

## 7. Navigation und Designschalter

Die bestehende Architektur bleibt unverändert:

1. `hugo.toml` registriert sechs Designs; `design-06` ist der letzte Eintrag.
2. `baseof.html` setzt `data-design` vor dem ersten Bild und lädt alle
   Design-CSS-Dateien.
3. `?design=design-06` öffnet die Variante ohne zu speichern.
4. `design.js` speichert die Wahl in `localStorage` (`ghse-design`) und
   synchronisiert beide Selects.
5. Der Standard bleibt `funktional`.
6. Der Hell-/Dunkelmodus läuft unabhängig über `ghse-theme` und
   `data-theme`; `nav.js` steuert die Schaltflächen.

**Kein neuer Schalter, keine neue Speicherung, kein neues JavaScript.**
`stilwahl.html`, `design.js` und `nav.js` wurden nicht verändert;
`baseof.html` erhielt ausschließlich den freigegebenen deutschen 404-Titel.

Der Umschalter zeigt „Wegw.“, weil der vollständige Name „Wegweiser“ die
intrinsische Breite des Selects in Funktional und Modern verändern und
damit deren pixelgleiche Kopfzeilen brechen würde. Der vollständige Name
steht im `title` der Option und in dieser Dokumentation.

---

## 8. Hell- und Dunkelmodus

Beide Modi sind vollständige Tokensätze, keine Invertierung.

- **Hell:** kühles Papiergrau `#EDF1F5`, weiße Schilder, navyfarbene
  Überschriften, GHSE-Blau als Link- und Aktionsfarbe.
- **Dunkel:** tiefes Blauschwarz `#080E1C`, Schilder `#101A2E`, warmes Weiß
  `#F2F5FA`, Überschriften `#D6E4F7`, Linien `#26344C`.
- Gelb und Orange bleiben in beiden Modi Marken; Text auf Gelb bleibt
  dunkel (`#101828`), auch im Dunkelmodus.
- Der Hero-Verlauf wechselt auf `--d6-wall-dark`; das Gebäudefoto bleibt
  unverändert und leuchtet als echtes Fenster.
- Der Modusschalter setzt `aria-pressed`, `data-ist` und den sichtbaren
  Zieltext; die Wahl überlebt Neuladen.
- Ohne gespeicherte Wahl folgt die Seite `prefers-color-scheme`.

---

## 9. Responsive Regeln

| Breite | Verhalten |
| --- | --- |
| ≥ 1200 px | volle Kopfzeile; Hero 7/5; Schularten 2 Spalten; News 3; Instagram 4; Galerie 4; Sidebar 300 px sticky |
| 1101–1199 px | Kopf wird Menü; Hero stapelt, Panel/Bild max. 46rem zentriert; Galerie 3; Sidebar sticky bleibt bis 1101 |
| 901–1100 px | Menü; Sidebar wird mobile Kopie vor dem Text; Downloads 3-spaltig; News 2 |
| 769–900 px | Menü; Hero gestapelt; Galerie 2; Schularten 2 |
| 641–768 px | Karten/News/Service/Kalender 1 Spalte; Downloads 1; Galerie 2; Footer 2 |
| 481–640 px | kompakter Kopf; H1 `clamp(2,55rem, 12vw, 3,4rem)`; Menütext sichtbar; Galerie 2; Instagram 2 |
| 361–480 px | Instagram 1; Schulleben 1; Partner 2; Footer 1 |
| ≤ 360 px | kompaktere Innenabstände, Logo 2,1rem, Krankmelden enger; kein Überlauf |

- **Gemessene Kopfhöhe:** 118 px Desktop, 73 px Mobil (per `nav.js`).
- **Kein horizontaler Überlauf** bei 320/360/390/414/480/640/768/834/1024/
  1112/1280/1440 px über 82 Seiten (902 Kombinationen).
- **Sprungziele** liegen unter Kopf und Sprungleiste; die Leiste bleibt
  auf schmalen Geräten eine Zeile mit horizontalem Scroll.
- **Sticky-Sidebar** ab 1101 px; darunter die mobile Kopie vor dem Text.

---

## 10. Barrierefreiheit

Ziel: **WCAG 2.2 AA**.

### Belegt

- **Kontrast:** 83 Seiten × hell/dunkel, 0 Textkontrast-Fehler; die
  wichtigsten Paare stehen in Abschnitt 3.6.
- **Lighthouse Accessibility:** 100/100 auf Startseite (mobil) und
  TG-Detailseite (Desktop).
- **Tastatur:** Skip-Link als erster Stopp; Menü per Enter/Escape;
  `aria-expanded`, `aria-controls`, `aria-current`; sichtbare Fokusringe
  auf allen geprüften Flächen.
- **Ziele:** alle interaktiven Ziele ≥ 24 × 24 px; primäre Aktionen
  (Abschlussziele, Karten, Buttons, mobiler Kopf) 44 px.
- **Semantik:** eine H1 pro Seite, Überschriftenhierarchie, echte Listen,
  Tabellen mit `th`, `aria-label` für Navigationen, `aria-hidden` für
  dekorative Grafik.
- **Bilder:** echte `alt`-Texte; im Hero gibt es keine zusätzliche
  Bildzeile, die mit der Beschreibung konkurriert.
- **Bewegung:** `prefers-reduced-motion` schaltet Übergänge, Bildskalierung
  und Pfeilverschiebung ab.
- **Farbunabhängigkeit:** Kategorien stehen als Text, nicht nur als Farbe;
  Fokus ist nicht nur ein Farbwechsel.
- **Formulare:** keine eigenen Formulare; bestehende Links und Buttons
  bleiben.

### Bewusste Grenzen

- **Desktop-Nutzleiste, Stil-Select, Theme-Knopf und Hauptnavigation**
  liegen zwischen 28 und 40 px Höhe. Sie sind Sekundärbedienung und
  erfüllen die WCAG-24-px-Schwelle; das 44-px-Produktziel gilt den
  primären Aktionen.
- **Fokus im mobilen Menü:** `nav.js` ist geteiltes Bestandsverhalten und
  schließt das Panel nicht bei Fokusverlust. Eine Fokusfalle würde alle
  fünf Bestandsdesigns funktional verändern und wurde deshalb nicht
  eigenmächtig eingebaut.
- **Gruppenlinks:** „Schüler“ führt jetzt auf `/smv/`, „Anmeldung“ auf
  `/anmeldeformulare/`; die Untermenüs öffnen weiter über den Pfeil. Die
  fünf Bestandsdesigns behalten auf den Referenzseiten dieselbe Darstellung.
- **404-Titel:** Der Browser-Titel ist jetzt „Seite nicht gefunden |
  GHSE Emmendingen“; die sichtbare Seite und der Titel stimmen überein.
- **TG-Galerie:** Die 23 Fotos stehen im Inhalt vor dem ersten erklärenden
  Absatz. Design 6 komprimiert sie auf ein 4/3/2-spaltiges Ansichtsband,
  kann die Content-Reihenfolge aber nicht ohne Template-/Inhaltsänderung
  verschieben.
- **Startseiten-Raster:** Es zeigt die vier vorhandenen Schulartkarten
  (alle Vollzeit); Pflege und Berufsschule stehen auf `/schularten/`.
  Weitere Karten würden Inhalte/Template ändern. „Alle Schularten“ ist
  deshalb ein gelber Primärweg.

---

## 11. Technische Besonderheiten

### Dateien

```text
assets/css/design-06.css
assets/fonts/design-06/archivo-var-latin.woff2
assets/fonts/design-06/LIZENZ.txt
layouts/_partials/schriften-design06.html
design-06-DESIGN.md
qa/design6-guard.py
qa/design6-baseline.json
qa/design6-isolation.py
```

`hugo.toml` enthält genau einen zusätzlichen Eintrag:

```toml
[[params.designs]]
  id = "design-06"
  name = "Wegweiser"
  kurz = "Wegw."
  css = "css/design-06.css"
  fonts = "schriften-design06.html"
```

### Isolation

- **459 Regel-Preludes** in `design-06.css`; jede normale Regel beginnt mit
  `:root[data-design="design-06"]`.
- Keine globalen `:root`-Tokens, keine ungeschützten Elementselektoren,
  keine `@import`-, `http(s)`- oder `url()`-Fremdreferenzen.
- Keine Keyframes; keine Kollision mit Bestandsanimationen.
- Schriftfamilie „Archivo“ ist neu und eindeutig; bestehende Familien
  werden nicht überschrieben.
- `@font-face` steht im eigenen Schrift-Partial, nicht im globalen CSS.

### Build und Last

- Hugo 0.169.0 extended; `hugo --gc --minify` erfolgreich, 88 Seiten.
- Design-CSS: 76.617 Bytes Quelle, ca. 60 KB minifiziert.
- Archivo: 88 KB (Latin-Subset), wird nur bei aktiver Variante geladen.
- Kein neues JavaScript; `design.js`, `nav.js`, `video.js` unverändert.
- Keine externen Requests; alle Bilder und Schriften lokal.

### QA-Werkzeuge

| Werkzeug | Ergebnis |
| --- | --- |
| `qa/themes.py` | 6 Varianten × 5 Seiten × 5 Breiten: 0 Befunde |
| `qa/layout.py --design design-06` | 0 Fehler; Anker, Sprungleiste, Touch-Ziele |
| `qa/reflow.py --design design-06` | 82 Seiten × 11 Breiten = 902 Kombinationen: 0 Probleme |
| `qa/linkcheck.py` | 5.850 interne Ziele, 0 Fehler |
| `qa/design.py` | 6 Varianten, Speicherung, Neuladen, `?design=` |
| `qa/design6-isolation.py` | 459 Preludes, alle scoped |
| `qa/design6-guard.py` | 704 Dateien, 5 Bestandsdesigns unverändert |
| `qa/theme5-guard.py` | 692 Dateien, additiv erweitert |
| `qa/theme-guard.py` | 681 Dateien, unverändert |
| `qa/themebilder.py` / Referenzlauf | 150 Aufnahmen, 0 Pixelabweichungen |
| Kontrast-Sweep | 83 Seiten × hell/dunkel: 0 Textkontrast-Fehler |
| Impeccable Detector (URL) | 83 Seiten: 0 Laufzeitbefunde |
| Impeccable Audit | 19/20 (Accessibility 3, Performance 4, Theming 4, Responsive 4, Implementation Integrity 4) |
| Impeccable Detector (CSS) | 43 Advisories (15 Farbe, 28 Schriftgröße), 0 Warnungen/Fehler; Tokens und Skala sind hier dokumentiert |
| Lighthouse Startseite mobil | Performance 95, Accessibility 100, Best Practices 100, SEO 85 (lokale `robots.txt`/Canonical) |
| Lighthouse TG Desktop | Performance 100, Accessibility 100, Best Practices 100, SEO 85 (lokal) |
| Konsole | 0 Fehler, 0 fehlgeschlagene Requests; kein `livereload.js` |

**Bestandsschutz:** 150 Referenzaufnahmen der fünf Bestandsdesigns
(5 Themen × 5 Seiten × 3 Breiten × hell/dunkel) sind SHA-256-pixelgleich
zum Stand vor Design 6. Die fünf Designs, ihre CSS-Dateien, Layouts,
Inhalte und Assets sind unverändert.

---

## 12. Critique, Polish und Audit

### Critique

Die Impeccable-Critique lief mit zwei unabhängigen Gutachten:

- **Assessment A (Design Review):** 6,5/10, Nielsen 27/40 vor den Fixes.
  Stärken: erster Bildschirm, GHSE-Farbwelt, handwerkliche Sauberkeit.
  Prioritäten: Dark-Mode-Kontraste, TG-Fotowand, sichtbare Schulbreite,
  mobiles Menü, Primärhierarchie.
- **Assessment B (Detector/Browser):** drei dunkle AA-Blocker
  (Download-Buttons 1,39:1, News-Datum 1,26:1, Sidebar-Fokus 1,0:1),
  unsichtbares „Stil“-Label (1,09:1), Sprungleisten-Fokus 2,29:1,
  44-px-Restflächen, Galeriehöhe.

### Polish

Umgesetzt:

- Hero-Zielzeilen über die volle Panelbreite; gelber „Alle Schularten“-
  Primärweg; auf Wunsch ohne Standortplakette und ohne Pfeil.
- Dark-Mode-Kontraste: dunkle Schrift auf Gelb für Download-Buttons,
  Datumsbadges und Sidebar-Fokus; gelber Fokus auf der Sprungleiste.
- Mobiles „Stil“-Label sichtbar; Select 44 px; Menütext „Menü“ ab 360 px.
- 404 als blaue Wegtafel mit „Zur Startseite“ als Primärweg.
- Galerie 4/3/2 Spalten statt 2-Spalten-Wand; Lesespalte 64ch;
  Breadcrumb-Tracking reduziert.
- Footer-Links 24 px; mobile Kopfziele 44 px; Reduced Motion vollständig.
- Video-Play-Knopf ohne harten Offset-Schatten; Pfeilspitzen als
  `clip-path` statt Side-Tab-Border.

### Verdict-Pass

| Befund | Status |
| --- | --- |
| Dark-Mode-Kontraste | **resolved** (12,92:1; Sidebar 12,92:1; Sprungleiste 9,09:1) |
| Mobiles „Stil“-Label | **resolved** (17,75:1; Select 44 px) |
| 404-Wegtafel | **resolved** (blau, weiße Schilder, gelber Primärweg) |
| Reduced Motion | **resolved** |
| Galeriehöhe | **entschieden** (4/3/2-Raster; 1.381 px statt 2.850 px bei 1440) |
| Sichtbare Schulbreite (4 von 8) | **entschieden** (vier Karten + gelber „Alle Schularten“-Weg) |
| Primäre Hierarchie | **entschieden** (Hero/404 gestärkt; „Schüler“ und „Anmeldung“ echte Ziele; Sidebar bleibt inhaltlich) |
| Mobiles Menü-Fokus | **entschieden** (Label/Select behoben; geteiltes `nav.js` bleibt) |
| 44-px-Ziele | **entschieden** (mobile/Kernwege 44 px; Desktop-Sekundärbedienung kompakt, ≥24 px) |
| „Wegw.“ | **entschieden** (Pixelgleichheit der fünf Bestandsdesigns hat Vorrang) |
| Designsystem-Doku | **resolved** (`DESIGN.md` additiv um die sechste Variante ergänzt; fünf Bestandsdokumente unverändert) |
| „Schüler“-Ziel / 404-Titel | **resolved** (`/smv/`; „Seite nicht gefunden“) |
| Linien | **resolved** (einheitlich 1 px; Fokusring als Zustand 3 px) |

Neue materielle Probleme durch die Fixes: **keine**.

### Audit

- WCAG-2.2-AA-Kontraste: 0 Textfehler in 83 Seiten × 2 Modi.
- Lighthouse Accessibility 100 auf Startseite und TG.
- Kein Überlauf, keine Konsolenfehler, keine defekten internen Ziele.
- Tastatur, Skip-Link, Menü, Theme-/Stilwechsel, Anker und Sticky-Sidebar
  geprüft.
- Die verbleibenden Punkte sind Content-/Struktur-/Bestandsgrenzen, keine
  Design-6-CSS-Fehler; sie stehen in Abschnitt 10 und 12.

---

## 13. Pflege

- Neue Regeln immer unter `:root[data-design="design-06"]` schreiben.
- Keine globalen Tokens, keine nackten Elementselektoren, keine
  `!important`-Kaskaden außer im Druckblock.
- Farben nur über die `--d6-*`-Tokens; die vier Originalwerte bleiben
  unverändert.
- Schriften nur über `--d6-font` und die eigene `@font-face`-Definition.
- Hover/Fokus/Reduced Motion gemeinsam prüfen.
- Nach jeder Änderung:
  ```bash
  hugo --gc --minify
  python3 qa/design6-isolation.py
  python3 qa/design6-guard.py
  python3 qa/themes.py http://127.0.0.1:8735/
  python3 qa/layout.py --design design-06
  python3 qa/reflow.py --design design-06
  python3 qa/linkcheck.py
  ```
- Referenzaufnahmen der fünf Bestandsdesigns nicht neu erzeugen, solange
  der Schutzstand `7ad5bea` gilt.

---

## 14. Bewusste Grenzen und Entscheidungen

Diese Punkte sind entschieden oder als Bestandsgrenze dokumentiert:

1. **Startseite zeigt 4 von 8 Schularten** (alle Vollzeit). Entschieden:
   vier vorhandene Karten plus gelber „Alle Schularten“-Weg; keine neuen
   Inhalte. Pflege und Berufsschule stehen auf `/schularten/`.
2. **TG-Galerie** steht im Inhalt vor dem ersten erklärenden Absatz.
   Entschieden: kompaktes 4/3/2-Raster; keine Content-/Template-Umstellung.
3. **Mobiles Menü** schließt nicht bei Fokusverlust. Entschieden: `nav.js`
   bleibt geteiltes Bestandsverhalten; keine Fokusfalle in den fünf
   Bestandsdesigns.
4. **Desktop-Nutzleiste/Stil/Theme/Nav** liegen unter 44 px, aber über
   24 px. Entschieden: kompakt lassen; das 44-px-Ziel gilt den primären
   Aktionen.

---

## 15. Dateien und Stand

- **Neu:** `assets/css/design-06.css`,
  `assets/fonts/design-06/archivo-var-latin.woff2`,
  `assets/fonts/design-06/LIZENZ.txt`,
  `static/bilder/themes/wegweiser-logo.webp`,
  `layouts/_partials/schriften-design06.html`, `design-06-DESIGN.md`,
  `design-06-KONZEPTE.md`, `design-06-CRITIQUE.md`, `design-06-AUDIT.md`, `design-06-konzepte/`,
  `qa/design6-guard.py`, `qa/design6-baseline.json`,
  `qa/design6-isolation.py`, `PRODUCT.md`.
- **Additiv geändert:** `hugo.toml` (ein Design-Eintrag, Kommentar,
  `Schüler`-Ziel), `layouts/baseof.html` (deutscher 404-Titel),
  `DESIGN.md` (sechste Variante ergänzt), `qa/themes.py` (sechste Variante),
  `qa/design.py` (sechste Variante und Wegweiser-Prüfung),
  `qa/theme5-guard.py` (optionaler zweiter Zusatz und freigegebene
  Ausnahmen), `.gitignore` (Baseline-Ausnahme).
- **Unverändert:** alle fünf Bestandsdesigns, ihre CSS-Dateien, Layouts,
  Inhalte, Assets und die fünf bestehenden Design-Dokumentationen.
- **Nicht committet, nicht gepusht, nicht veröffentlicht.**
