# Design 6 „Wegweiser“ – Impeccable Critique

**Ziel:** Design 6 der GHSE-Website, Startseite und alle tragenden Seitentypen  
**Stand:** 16. November 2026  
**Methode:** zwei isolierte Assessments (A: Design Review, B: Detector/Browser-Evidenz), danach Synthese und Verdict-Pass nach dem Polish.

---

## 1. Prüfrahmen

- **Assessment A:** Design Review mit `critique-rubric.md`, Nielsen-Heuristiken, kognitiver Last, emotionaler Reise und Personas. Keine Detector-Ausgabe gelesen.
- **Assessment B:** `impeccable detect` auf CSS und URL, Browser-Evidenz mit Playwright/Chromium, Kontrast-Sweep, Tastatur, Zustände, Anker, Sticky-Sidebar.
- **Seiten:** Startseite, Schulartenübersicht, Technisches Gymnasium, News-Liste, News-Detail, Downloads, Unsere Schule, 404.
- **Breiten:** 1440 × 900, 768 × 1024, 390 × 844; Randfälle 320/360 px.
- **Modi:** hell und dunkel; `prefers-reduced-motion: reduce`.
- **Interaktionen:** Menü öffnen/schließen, Escape, Fokus, Theme-/Stilwechsel, Hover, Anker.

---

## 2. Assessment A – Design Review

**Gesamturteil vor den Fixes:** 6,5/10  
**Nielsen:** 27/40 („Acceptable“, knapp unter der Good-Schwelle)  
**Design-Spezifität:** 7/10  
**Holistisches Design:** 6/10

### Stärken

1. **Der erste Bildschirm trägt.** Schulname, große H1, Leitsatz, fünf Abschlussziele und das echte Gebäude bilden eine ruhige, lokale Begrüßung; auf 390 px beginnt das Foto noch im ersten Bildschirm.
2. **Das System ist handwerklich sauber.** Vollständiger Hell-/Dunkel-Tokensatz, selbst gehostete Archivo, sichtbare Fokusringe, Skip-Link, keine Überläufe, konsistente Karten/Register/Zeilen über acht Seitentypen.
3. **Die Innenseiten haben ein eigenes Vokabular.** Wegzeile, gelbes „Auf einen Blick“-Etikett und Download-Zeilen mit Format/Größe/Aktion funktionieren als System.

### Priorisierte Probleme

| Priorität | Problem | Begründung |
| --- | --- | --- |
| P1 | Dark-Mode-Kontraste | Download-Buttons 1,39:1, News-Datum 1,26:1, Sidebar-Fokus 1,0:1 |
| P1 | TG-Detailseite beginnt mit 23 Fotos | Erste H2 bei 3.357 px (1440) / 6.957 px (390); „Wie bewerbe ich mich?“ bei 13.074 px (390) |
| P1 | Startseite zeigt 4 von 8 Schularten | Alle vier sichtbaren Karten sind Vollzeit; Pflege und Berufsschule fehlen |
| P2 | Mobiles Menü | „Stil“ unsichtbar (1,09:1), „Wegw.“ kryptisch, Fokus kann hinter das Overlay wandern |
| P2 | Primäre Handlung zu klein | Zielzeilen nur 235 px breit; „Krankmelden“ der einzige gefüllte Header-Button; Sidebar ohne Anmelde-CTA; 404 mit sechs Aktionen |

### Kognitive Last

3 von 8 Prüfpunkten verfehlt: Chunking ≤ 4, minimale Entscheidungen ≤ 4 und Working Memory. An fast jedem Entscheidungspunkt stehen mehr als vier Optionen (8 Hauptnav-Punkte, 5 Schnellzugriffe, 7 Download-Kategorien, 6 Aktionen auf 404).

### Personas

- **Jordan (Erstbesucher):** „Abitur“ führt zur Übersicht, „FH-Reife“ zu einem einzelnen Berufskolleg; die fünf Zeilen sehen wie gleichartige Abschlüsse aus, obwohl „Berufsausbildung“ ein Weg ist. Auf der TG-Seite kommen 23 Fotos vor der Erklärung.
- **Sam (Screenreader/Tastatur):** Skip-Link und Fokus gut; „Stil“ unsichtbar, Fokus hinter dem Overlay, dunkle Buttons/Datum unlesbar, Footer-Links 20 px.
- **Casey (mobil):** TG 16.592 px lang; „Wie bewerbe ich mich?“ bei 13.074 px; News-Scan in ca. 8-px-Schrift.
- **Miriam (Mutter):** sieht vier Schularten, keine Pflege/Berufsschule; „Auf einen Blick“ ohne Dauer/Voraussetzungen/Anmeldezeitraum; „Krankmelden“ der lauteste Button.
- **Bernd (Ausbildungsbetrieb):** findet die Berufsschule nicht im Startseitenraster; kein eigener Einstieg „Für Betriebe“.

---

## 3. Assessment B – Detector und Browser-Evidenz

### Detector

- **CSS:** 81 Advisories vor dem Token-Feinschliff (52 Farbe, 29 Schriftgröße), 0 Warnungen/Fehler. Nach Einführung von `--d6-on-yellow`: **43 Advisories** (15 Farbe, 28 Schriftgröße), alle dokumentiert.
- **URL:** 0 Laufzeitbefunde auf den Kernseiten; der spätere 83-Seiten-Sweep ergab nach Behebung eines Video-Schattenbefunds **0/83**.
- **Einordnung:** Die Farbadvisories betreffen die neue, dokumentierte Design-6-Palette und die vier GHSE-Originalfarben; die Schriftgrößen-Advisories die neue Skala. Keine echten Slop-Warnungen nach dem Polish.

### P1 – hohe Schwere (vor den Fixes)

1. **Dunkle Download-Buttons:** `#8FC2E6` auf `#F6DC56` = **1,39:1**; 32 Buttons auf 7 Seiten.
2. **Dunkles News-Datum:** `#F2F5FA` auf `#F6DC56` = **1,26:1**; 10 Detailseiten.
3. **Sidebar-Fokus dunkel:** gelber Ring auf gelbem „Auf einen Blick“ = **1,0:1**; 37 Seiten.

### P2 – mittlere Schwere (vor den Fixes)

- **Mobiles „Stil“-Label:** `#F2F5FA` auf Weiß = **1,09:1**.
- **Sprungleisten-Fokus hell:** `#B8430F` auf Navy = **2,29:1**.

### P3 – niedrige Schwere

- 44-px-Ziel nicht durchgängig in der Desktop-Sekundärbedienung (28–40 px; alle ≥ 24 px).
- „Wegw.“ als Kurzform.
- Dokumentationsdrift (`DESIGN.md` fünf Varianten; `hugo.toml`-Kommentar „Vier“).
- `livereload.js`-404 war ein Umgebungsartefakt des alten Builds; im finalen Build nicht vorhanden.
- 404-Browsertitel englisch (Hugo-Grundlage).

### Was bestanden ist

- Kein horizontaler Überlauf: 8 Seiten × 5 Breiten, zusätzliche Breakpoint-Sonden.
- Kontrast hell: 83 Seiten, 0 Textfehler; schlechtester Wert 5,03:1 auf dem Blauverlauf.
- Dark-Mode-Token vollständig; Theme-/Stilwechsel, Speicherung, `?design=`.
- Tastaturmenü: Enter/Escape, `aria-expanded`, Fokus zurück auf den Menüknopf.
- Anker/Sprungleiste, Sticky-Sidebar, Reduced Motion, Bilder/Schriften.
- 150 Referenzaufnahmen der fünf Bestandsdesigns pixelgleich; 704 Dateien im neuen Schutzstand.

---

## 4. Synthese und Polish

Die Critique wurde als Polish-Pass umgesetzt; die fünf Bestandsdesigns bleiben visuell unverändert. Die freigegebenen Bestands-Fixes betreffen nur das `Schüler`-Ziel und den 404-Titel.

| Befund | Fix | Verdict |
| --- | --- | --- |
| Dunkle Download-Buttons | `.fliesstext a.btn--akzent` dunkle Schrift; `--d6-on-yellow` | **resolved** (12,92:1) |
| Dunkles News-Datum | `.meta time` dunkle Schrift auf Gelb | **resolved** (12,92:1) |
| Sidebar-Fokus dunkel | dunkler Fokusring mit 2 px Offset | **resolved** (12,92:1) |
| Mobiles „Stil“-Label | dunkle Farbe im Menü; Select 44 px | **resolved** (17,75:1) |
| Sprungleisten-Fokus | gelber Fokus auf Navy | **resolved** (9,09:1) |
| Unterschiedliche Strichstärken | alle sichtbaren Rahmen/Trennlinien auf 1 px; Fokusring bleibt Zustand | **resolved** |
| Hero-Zielzeilen zu schmal | volle Panelbreite, Pfeil rechts | **resolved** |
| Pfeil/Plakette im Hero | Auf Wunsch des Auftraggebers entfernt; Zielzeilen und Sichtfenster tragen den Hero | **entschieden** |
| 404 Buttonstapel | blaue Wegtafel, weiße Schilder, „Zur Startseite“ gelb | **resolved** |
| „Schüler“ ohne `href` | echtes Ziel `/smv/`; „Anmeldung“ bereits `/anmeldeformulare/` | **resolved** |
| Galerie 2.850 px | 4/3/2 Spalten, 1.381 px bei 1440 | **entschieden** (kompaktes Raster; Content-Reihenfolge bleibt bewusst) |
| Startseite 4/8 | „Alle Schularten“ gelb; Inhalt unverändert | **entschieden** (4 Karten + CTA, keine neuen Inhalte) |
| Menü-Fokus | Label/Select behoben; Fokusfalle im geteilten `nav.js` nicht geändert | **entschieden** (Bestandslogik bleibt) |
| 44-px-Ziele | mobil/Kernwege resolved; Desktop-Sekundärbedienung 28–40 px | **entschieden** (kompakt, ≥24 px) |
| „Wegw.“ | bewusst für pixelgleiche Bestandsköpfe | **entschieden** |
| Dokumentation | `design-06-DESIGN.md` vollständig; `DESIGN.md` additiv um die sechste Variante ergänzt | **resolved** |

**Neue materielle Probleme durch die Fixes:** keine. Der Verdict-Pass bestätigt die P1-Behebungen; die verbleibenden Content-/Strukturpunkte und die geteilte Menülogik sind bewusst entschieden.

---

## 5. Ehrliches Fazit

Design 6 ist nach dem Polish ein technisch sauberes, farblich konsistentes und auf allen Seitentypen tragfähiges System. Die drei dunklen AA-Blocker, der unsichtbare „Stil“-Wert, der Sprungleisten-Fokus, die 404-Wegtafel, die Galeriehöhe und die mobilen Kopfziele sind behoben.

Die zwei wichtigsten inhaltlichen Fragen sind entschieden: **kompaktes Galerie-Raster** statt einer Content-Umstellung und **vier vorhandene Karten plus gelber „Alle Schularten“-Weg** statt neuer Karten. Beide bleiben als bewusste Grenzen dokumentiert; Design 6 hat die vorhandenen Inhalte so gut komprimiert und gewichtet, wie es ohne Template-/Content-Umbau möglich ist.
