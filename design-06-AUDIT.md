# Design 6 „Wegweiser“ – Impeccable Audit

**Ziel:** gesamte Design-6-Variante der GHSE-Website  
**Stand:** 16. November 2026  
**Umfang:** 83 gebaute Seiten, 6 Gestaltungsvarianten, hell/dunkel, 320–1440 px  
**Art:** technischer Audit nach dem Polish und den freigegebenen Bestands-Fixes

---

## Audit Health Score

| # | Dimension | Score | Key Finding |
|---|---|---:|---|
| 1 | Accessibility | **3/4** | WCAG AA weitgehend erfüllt: 0 Textkontrast-Fehler in 83 Seiten × 2 Modi, Lighthouse 100. Bewusst: geteiltes Menü-Fokusverhalten (Bestand) und kompakte Desktop-Sekundärbedienung (≥ 24 px); die Gruppenlinks sind jetzt echte Ziele. |
| 2 | Performance | **4/4** | Lighthouse 95 mobil / 100 Desktop; 60 KB minifiziertes CSS, 88 KB Archivo, kein neues JavaScript, lazy Bilder, keine externen Requests. |
| 3 | Theming | **4/4** | Vollständiger Hell-/Dunkel-Tokensatz, GHSE-Originalfarben unverändert, Blauspektrum dokumentiert, Dark Mode ohne Kontrastfehler. |
| 4 | Responsive Design | **4/4** | 82 Seiten × 11 Breiten = 902 Kombinationen ohne Überlauf; 24-px-Ziele überall, 44-px-Primäraktionen; mobile Menüs, Galerie und Sidebar funktionieren. |
| 5 | Implementation Integrity | **4/4** | Kohärentes, produktspezifisches System; 459 isolierte CSS-Preludes; 83/83 Seiten ohne Detector-Befund; fünf Bestandsdesigns 150-mal pixelgleich; `DESIGN.md` additiv um Design 6 ergänzt. Die Inhalts-/Strukturpunkte sind entschieden; eine bewusste Bestandsgrenze bleibt der geteilte Menü-Fokus. |
| **Gesamt** |  | **19/20** | **Excellent (minor polish)** |

---

## Implementation Integrity Verdict

**Pass.** Die Umsetzung trägt ein eigenes, produktspezifisches System: GHSE-Blau als Wand, weiße Emailschilder, gelbe Wegmarken, Archivo, Standortleiste, Zielzeilen, Spezifikationsetiketten und eine 404-Wegtafel. Das ist nicht austauschbar mit einer beliebigen Schulwebsite; die fünf Bestandsdesigns bleiben nachweislich unberührt.

Belege:

- `qa/design6-guard.py`: **704 Dateien** (inkl. Design 6), fünf Bestandsdesigns unverändert.
- `qa/design6-isolation.py`: **459 Regel-Preludes**, alle unter `:root[data-design="design-06"]`.
- 150 Referenzaufnahmen der fünf Bestandsdesigns: **0 Pixelabweichungen**.
- Impeccable Detector: **83/83 Seiten 0 Laufzeitbefunde**.
- Keine Konsolenfehler, keine fehlgeschlagenen Requests, kein `livereload.js`.

---

## Executive Summary

- **Audit Health Score:** 19/20 – Excellent (minor polish).
- **Befunde:** 0 × P0, 0 × P1; 3 × P2 und 2 × P3 sind entschieden bzw. als bewusste Grenze dokumentiert, nicht offen.
- **Die drei dunklen AA-Blocker aus der Critique sind behoben und im Verdict-Pass bestätigt:** Download-Buttons 12,92:1, News-Datum 12,92:1, Sidebar-Fokus 12,92:1; Sprungleisten-Fokus 9,09:1.
- **Top-Themen:** Die zwei inhaltlichen Wege sind entschieden: kompaktes Galerie-Raster und vier vorhandene Schulartkarten plus gelber „Alle Schularten“-Weg. Ein Template-/Content-Umbau ist dafür nicht nötig.
- **Nächste Schritte:** Keine offenen Pflichtmaßnahmen. Die geteilte Menü-Fokusfrage bleibt als bewusste Bestandsgrenze; alle anderen Punkte sind entschieden oder behoben.

---

## Detailed Findings by Severity

### P2 – entschieden: TG-Galerie bleibt als kompaktes Raster vor dem Text

- **Location:** `layouts/schularten/page.html` (Content-Reihenfolge), `assets/css/design-06.css` (Galerieband).
- **Category:** Implementation Integrity / Informationsarchitektur.
- **Impact:** Die wichtigste Schulartseite beginnt mit 23 Eventfotos; die erste H2 folgt bei ca. 1.912 px (1440) bzw. 2.914 px (390). Eltern und Jugendliche finden „Was ist das, für wen, wie bewerbe ich mich?“ erst nach der Galerie.
- **Standard:** Kein WCAG-Verstoß; ein Hierarchie- und Auffindbarkeitsproblem.
- **Entscheidung:** Kompaktes 4/3/2-Raster (umgesetzt); die Content-Reihenfolge bleibt bewusst. Design 6 hat die Galerie von 2.850 px auf 1.381 px (1440) komprimiert.

### P2 – entschieden: Startseite zeigt vier vorhandene Schularten plus CTA

- **Location:** `layouts/home.html` (vier feste Karten), `assets/css/design-06.css` („Alle Schularten“ gelb).
- **Category:** Implementation Integrity / Produktklarheit.
- **Impact:** Pflege und Berufsschule – die beiden Teilzeit-Schularten und stärksten Belege der GHSE-Breite – fehlen im sichtbaren Raster. „Schule für alle“ bleibt eine Behauptung, bis man `/schularten/` öffnet.
- **Standard:** Kein WCAG-Verstoß; ein Positioning- und IA-Problem.
- **Entscheidung:** Vier vorhandene Karten plus gelber „Alle Schularten“-Weg (umgesetzt); keine neuen Inhalte/Template-Änderung.

### P2 – entschieden: Geteiltes Menü schließt nicht bei Fokusverlust

- **Location:** `assets/js/nav.js` (Fokusverhalten).
- **Category:** Accessibility.
- **Impact:** Nach dem letzten Menüpunkt kann der Fokus für einen Tab-Schritt hinter das offene Overlay wandern. Das betrifft alle sechs Varianten, weil `nav.js` geteilt ist.
- **Standard:** WCAG 2.2 – Fokus nicht hinter Inhalten verstecken.
- **Entscheidung:** `nav.js` bleibt für alle sechs Varianten unverändert; die Fokusfalle wird nicht eigenmächtig in das geteilte Bestandsverhalten eingebaut.

### P3 – entschieden: Desktop-Sekundärbedienung bleibt kompakt

- **Location:** Nutzleiste (28 px), Stil-Select/Theme-Knopf (32 px), Hauptnavigation (ca. 39,5 px).
- **Category:** Accessibility / Responsive.
- **Impact:** Kein WCAG-AA-Verstoß (alle ≥ 24 px); das in `PRODUCT.md` formulierte 44-px-Ziel gilt den primären Aktionen und ist dort erfüllt. Die Sekundärbedienung ist kleiner.
- **Entscheidung:** Kompakt lassen (umgesetzt); alle Ziele bleiben ≥ 24 px, die primären Aktionen 44 px.

### P3 – entschieden: „Wegw.“ als sichtbare Kurzform

- **Location:** `hugo.toml`, `kurz = "Wegw."`.
- **Category:** Implementation Integrity.
- **Impact:** Der vollständige Name „Wegweiser“ steht nur im Optionstitel; auf Touch-Geräten ist die Kurzform erklärungsbedürftig.
- **Entscheidung:** „Wegw.“ bleibt; „Wegweiser“ würde die intrinsische Select-Breite in Funktional/Modern verändern und die pixelgleichen Kopfzeilen der Bestandsdesigns brechen.

---

## Patterns & Systemic Issues

- **Content-Reihenfolge vs. Theme:** Die zwei inhaltlichen Punkte (TG-Galerie, 4/8-Schularten) sind entschieden: kompaktes Raster bzw. vier Karten plus CTA. Sie bleiben als bewusste Grenzen dokumentiert.
- **Geteilte Bestandslogik:** `nav.js` ist für alle sechs Varianten gemeinsam. Eine Fokusfalle würde die fünf Bestandsdesigns funktional verändern; deshalb bewusst unverändert und dokumentiert.
- **Dokumentation:** Die neue Farb- und Typowelt ist in `design-06-DESIGN.md` vollständig dokumentiert; `DESIGN.md` wurde additiv um die sechste Variante ergänzt, ohne die fünf Bestandsdokumente zu ersetzen.

---

## Positive Findings

- **Kontrast:** 83 Seiten × hell/dunkel, 0 Textkontrast-Fehler; die dunklen AA-Blocker sind behoben.
- **Bestandsschutz:** 150 Aufnahmen der fünf Bestandsdesigns pixelgleich; 704 Dateien im neuen Schutzstand; 459 isolierte CSS-Preludes.
- **Responsive:** 902 Kombinationen ohne Überlauf; keine Ziele unter 24 px; mobile Kopfziele 44 px.
- **Performance:** Lighthouse 95 mobil / 100 Desktop, Accessibility 100, Best Practices 100; kein neues JavaScript, lokale Schriften und Bilder.
- **Zustände:** sichtbarer Fokus, Tastaturmenü, Theme-/Stilwechsel, Reduced Motion, Skip-Link, Sticky-Sidebar, Anker.
- **404:** echte Wegtafel statt Buttonstapel; „Zur Startseite“ ist der gelbe Primärweg.
- **Konsistenz:** ein Token-System, eine Schrift, ein 1-px-Liniensystem und klare Schild-/Registerlogik über acht Seitentypen.

---

## Recommended Actions

Keine offenen Pflichtmaßnahmen. Die technischen P1-Blocker sind behoben, die Inhalts- und Bestandsfragen sind entschieden, und der Polish-Pass ist abgeschlossen. Die Dokumentation ist in `design-06-DESIGN.md`, `design-06-CRITIQUE.md` und `design-06-AUDIT.md` nachvollziehbar.
