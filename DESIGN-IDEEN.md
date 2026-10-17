# Design-Ideen für den GHSE-Prototyp

**Stand:** 17. Oktober 2026 · Grundlage: gebauter Stand (Commit `6e373aa`),
Skill `neobrutalism`, lokale Prüfung in Chromium (Desktop 1440 px, Mobil 390/640 px)
sowie `qa/kontrast.py`.

**Charakter dieser Datei:** Vorschlagskatalog, keine fertige Spezifikation.
Jede Maßnahme nennt Wirkung, Aufwand und ein Prüfkriterium. Punkte mit
Daten- oder Bildbedarf sind als Content-Auftrag markiert und brauchen die
Freigabe der GHSE.

**Aufwandsschätzung:** `XS` ≤ 2 h · `S` ½ Tag · `M` 1–2 Tage · `L` > 2 Tage.

---

## 0. Top-Prioritäten

| # | Maßnahme | Wirkung | Aufwand | Abschnitt |
|---|---|---|---|---|
| 1 | Kopfhöhe/Ankersprung reparieren (Sprungleiste verdeckt Inhalte) | hoch | XS | 4.1, 7 |
| 2 | „Krankmelden" auf Mobil sichtbar machen | hoch | XS | 5.7 |
| 3 | News-Raster: Featured-Karte + Jahr-Gruppen | hoch | S | 5.3 |
| 4 | Schularten-Finder („Welcher Weg passt zu mir?") | hoch | M | 6.2 |
| 5 | „Nächster Termin"-Ticket im/unter dem Hero | hoch | S | 5.6 |
| 6 | Kategorie-Farbcode Vollzeit/Teilzeit + einheitliches Chip-System | mittel | S | 4.2, 5.1 |
| 7 | Kalender-Karten komplett klickbar | mittel | XS | 5.4 |
| 8 | Sprungleiste mobil als scrollbare Chip-Zeile | mittel | XS | 5.8 |
| 9 | Partner-Logostreifen als HTML-Gitter | mittel | S | 5.10 |
| 10 | Fokusring auf dunklen Flächen auf Gelb umstellen | mittel | XS | 4.3 |
| 11 | Buttons/Chips mobil auf ≥ 44 px bringen | mittel | XS | 7 (A4) |
| 12 | Prototyp-Hinweise als eigener Hinweisbaustein | niedrig | XS | 6.2, 8 |

---

## 1. Kontext und Ziele

**Nutzer/innen und ihre Kernaufgaben.** Für eine berufliche Schule gilt
dieselbe Rangfolge wie auf Schulwebsites üblich:

1. Krankmeldung, 2. Termine/Stundenplan, 3. Anmeldung/Formulare,
4. „Welcher Bildungsweg passt nach meinem Abschluss?", 5. Kontakt/Anfahrt,
6. Aktuelles.

**Designziele.** (a) Bildungswege in unter 30 Sekunden erfassbar machen,
(b) Kernaufgaben in höchstens zwei Klicks, (c) Neobrutalismus-Ton halten –
harte Kanten, Flächen, Versatzschatten, Drehungen sparsam, (d) WCAG 2.2 AA,
(e) Lighthouse mobil ≥ 98, (f) Inhalte bleiben über Pages CMS pflegbar.

**Leitplanken.** Kein Build-Schritt (kein npm/PostCSS), ein Stylesheet,
Vanilla-JS unter ~5 KB, keine Drittanbieter-Embeds, deutsche Token-Namen,
Dark Mode in beiden Token-Blöcken pflegen, jedes neue Front-Matter-Feld
zusätzlich in `.pages.yml` eintragen.

---

## 2. Was heute trägt (nicht antasten)

* **Tokens statt Einzelwerte** (`static/css/main.css:18`): Flächen, Text,
  Rahmen, Schatten, Streifen sind semantisch; Dark Mode tauscht Werte, nicht
  Regeln. Neue Farben nur als Token, nie ad hoc.
* **Kontrast:** `qa/kontrast.py` prüft 37 Paare in Hell und Dunkel, kleinster
  Textwert 4,87:1. Jede neue Farbpaarung wandert dort hinein.
* **Fokus, Tastatur, Reduced Motion:** sichtbare Ringe, Sprungmarke,
  `aria-expanded` am Mobilmenü, `prefers-reduced-motion` global.
* **Karten-Hover-Lift** und Fokus-Versatz (`.karte:hover`,
  `translate(-3px,-3px)` + größerer Schatten) – das ist der wiedererkennbare
  Kern der Sprache.
* **Sprungleiste** auf der Download-Seite, **Druck-Reset**, **Hero-Preload**,
  **WebP + echte Bildmaße**: Qualitätsniveau, das jede Änderung erhalten oder
  verbessern muss.

---

## 3. Befund mit Messwerten (Ist-Zustand)

Lokal gebaut (`hugo -D`), über `tools/preview-server.py`, Layoutmessung in
Chromium:

| Messung | Ergebnis | Folge |
|---|---|---|
| Desktop: Kopfhöhe vs. Token | 128 px vs. `--kopfhoehe: 7rem` (112 px) | Sprungleiste klebt 16 px unter der Kopfkante (Messung: Kopf unten 128, Leiste oben 112) |
| Mobil 390/640: Kopfhöhe vs. Token | 110 px vs. `4.5rem` (72 px) | 38 px Überlappung; nach Anker-Sprung steht die Zielüberschrift bei 88 px, Kopf+Leiste enden bei ~114 px → **21–26 px der Überschrift verdeckt** |
| News-Raster Desktop | Zeilenhöhen 469 / 469 / 493 / 542 px | Zeilen springen, unruhige Kanten |
| Meldung ohne Bild („Von Pädagogik bis Physik prämiert") | Textkörper 463 px, Bildkarten nur 232 px | ≈ 230 px Leerfläche in der Karte |
| Touch-Ziele mobil | Download-Button 42 px, Chip 43 px, Kalender-Link 28 px, Hero-Chip 33 px | WCAG-AA (24 px) erfüllt, 44-px-Ziel nicht |
| Mobilkopf: Menüknopf vs. Logo | 83 px vs. 64 px, Kopffeld dadurch 110 px | unruhige Oberkante, beansprucht ⅛ des Sichtbereichs |
| Fokusfarbe auf Nachtbändern | Orange `#bf4712` auf Nacht `#141c4e` ≈ 3,2:1 | besteht die Grafikgrenze 3:1 nur knapp; Gelb liefert ≈ 11:1 |
| Demo-Absatz auf `/schularten/` | gleiche Schriftgröße/Farbe wie Einleitungstext | Prototypenhinweis liest sich wie Inhalt |

---

## 4. Foundations: Tokens und Grundregeln

### 4.1 Kopfhöhe und Ankerziele (M1) — XS

Das Problem ist systemisch, nicht kosmetisch: `--kopfhoehe` wird an drei
Stellen verwendet (`[id] scroll-margin-top`, `.sprungleiste top`, Mobile-
Breakpoint), passt aber zu keiner echten Kopfhöhe.

**Empfehlung (robust):** Kopfhöhe zur Laufzeit messen und als CSS-Variable
setzen; die statischen Werte dienen nur als Startwert.

```js
// nav.js – dritter Block
var kopf = document.querySelector('.kopf');
function setzeKopfhoehe() {
  if (kopf) document.documentElement.style.setProperty(
    '--kopfhoehe', kopf.offsetHeight + 'px');
}
setzeKopfhoehe();
window.addEventListener('resize', setzeKopfhoehe);
```

Zusätzlich: Ziele, die unter der **Sprungleiste** landen, brauchen mehr Abstand
als der generische `[id]`-Wert:

```css
/* Download-Kategorien liegen unter Kopf + Sprungleiste */
h2[id^="dl-"] { scroll-margin-top: calc(var(--kopfhoehe) + 4.5rem); }
```

**Prüfkriterium:** Auf 390 px und 1440 px liegt nach Klick auf einen
Kategorie-Link die Zielüberschrift vollständig sichtbar unter Kopf und Leiste
(`getBoundingClientRect().top ≥ Kopfende + Leistenhöhe`).

### 4.2 Farbcode Vollzeit/Teilzeit (F1) — S

Die 8 Schularten zerfallen in genau zwei Kategorien (Front Matter
`kategorie`). Zwei Farbtöne machen Liste und Karten scanbar, ohne die
Markenpalette zu verlassen:

| Kategorie | Fläche | Text | Kontrast |
|---|---|---|---|
| Vollzeitschularten | Gelb `#ffd400` (bestehend) | Tinte `#101736` | 12,3:1 |
| Teilzeitschularten | Orange `#ee6a2b` (neu als Fläche) | Tinte `#101736` | ≈ 5,6:1 |

Weiß darf auf Orange nur für Zeichen ≥ 24 px/3:1 stehen, nicht für Fließtext.
Beide Paare kommen in `qa/kontrast.py`; Dark Mode behält Gelb/Orange mit
Tinte-Schrift (funktioniert in beiden Modi).

```html
<p class="chip chip--sticker" data-kategorie="{{ .Params.kategorie | lower }}">
```

```css
[data-kategorie="teilzeitschularten"] { background: var(--orange); }
```

### 4.3 Fokusfarbe auf dunklen Flächen (A1) — XS

```css
.hero :focus-visible,
.band--nacht :focus-visible,
.fuss :focus-visible,
.kopf .leiste :focus-visible {
  outline-color: var(--gelb);
}
```

**Prüfkriterium:** Tabulatorschritt durch Hero, Nachtband und Footer auf
beiden Farbmodi: Ring gegen beide angrenzenden Farben deutlich sichtbar
(≥ 3:1), Screenshot als Beleg.

### 4.4 Typografie-Feinschliff (T1) — XS

* Datums- und Größenangaben: `font-variant-numeric: tabular-nums` auf
  `.meta time`, `.tag`, `.zeile__daten` – Spalten stehen ruhig.
* Kartentitel: `text-wrap: balance` ergänzen (h1 hat es bereits).
* `hyphens: auto` bleibt dem Fließtext vorbehalten; Karten brechen hart um.

### 4.5 Muster und Flächen — S

* Das Streifenmuster liegt bei 5 % Alpha/10 px und ist auf Papier kaum
  sichtbar (Vergleich Screenshots). Entweder auf 7–8 %/12 px verstärken oder
  durch ein Punktraster ersetzen – aber bei höchstens zwei Musterarten bleiben.
* Regel für Gelb als Vollfläche: nur wo eine Aufgabe im Mittelpunkt steht
  (Faktenband, Schularten-Kopf, später „Zahlenband"). Sonst bleibt Gelb
  Akzent.

---

## 5. Komponenten

### 5.1 Chip-System konsolidieren (F2) — S

Heute existieren vier ähnliche Bausteine: `.marke` (gelb, gedreht), `.tag`
(weiß), `.meta time` (gelb) und `.chip` (weiß, mit Unterzeile). Unterschiede
sind zufällig, nicht begründet.

**Vorschlag:** ein Baustein `chip` mit Varianten:

| Variante | Fläche | Einsatz | Zustände |
|---|---|---|---|
| `chip--akzent` | Gelb, Tinte | Kategorie, Datum, Zahl | als Link: Hover invertiert (Tinte-Fläche, Gelb-Text) |
| `chip--neutral` | Weiß/Fläche | Format, Größe, Zusatz | als Link: Hover Gelb |
| `chip--ruhig` | transparent, 2 px Rand | Hinweise („abonnierbar", „Scan") | als Link: Hover Gelb |
| `chip--sticker` | wie akzent/neutral | max. 1–2 pro Seite, Drehung −2°/+1,5° | nicht verlinkt |

Fokus in allen Varianten: 3-px-Ring `--orange-tief`, auf Nachtbändern Gelb
(4.3).

**Regeln:** höchstens zwei Chips pro Karte; Großschreibung beibehalten;
Label ≤ 18 Zeichen; als Link auf grobem Zeigegerät ≥ 44 px hoch.
Migration per Suchen/Ersetzen; `.marke` bleibt als Alias für
`chip--akzent chip--sticker` erhalten, damit Templates schrittweise
umgestellt werden können.

### 5.2 Karte (K3) — S

* **Fokus:** Ring am Kartenrahmen statt am inneren Link (vermeidet doppelte
  Ringe):

```css
.karte:has(.karte__link:focus-visible) {
  outline: 3px solid var(--orange-tief); outline-offset: 3px;
}
.karte__link:focus-visible { outline: none; }
```

* **Featured-Variante** `karte--gross`: spannt zwei Spalten, Bild 21:9,
  Titel in `--t-h2`. Einsatz: jüngste Meldung (5.3).
* **Kein-Bild-Variante** `karte--text`: statt 230 px Leerfläche ein
  typografischer Kopf – Quelle als Sticker, darunter Datum riesig
  (`clamp(2rem,4vw,3rem)`, tabular-nums) – oder die Karte spannt zwei Spalten.
  Entscheidung im Prototyp; Test: keine Karte hat mehr als ~8 rem Fläche ohne
  Inhalt, Zeilenhöhen bleiben waagerecht geschlossen.

### 5.3 News-Raster (K1) — S

* **Startseite:** 1 × `karte--gross` (neueste) + 4 normale in 2×2. Füllt das
  3er-Raster exakt, statt heute 5 Karten mit Loch.
* **Übersicht:** erste Meldung `karte--gross`, Rest in 3er-Raster (die
  Zelle links neben dem Featured-Beitrag füllt die zweitneueste Meldung).
  Zusätzlich Jahr-Gruppen („2026", „2025") als `h2` mit Sprungmarke statt
  loser Meta-Zeile.
* **Presse-Scans** bleiben als Kartenbild; Erklärung statt Look-Verbiegung:
  `chip--ruhig` „Zeitungsausschnitt" auf Scans mit Textanteil.

### 5.4 Kalender-Karte (K2) — XS

Die ganze Karte wird Link (Muster `.karte__link`), Fußzeile „Kalender öffnen ↗"
bleibt als sichtbare Affordanz. Dadurch wächst das Touch-Ziel von 28 px auf
die volle Kartenfläche. Zusatz möglich: `chip--ruhig` „abonnierbar".

### 5.5 Download-Zeile (D2) — XS

* `.btn--klein` auf ≥ 44 px (`min-height: 2.75rem`) bei grobem Zeiger
  (heute 42 px).
* Hover auch auf der Zeile (wie Karte): `translate(-2px,-2px)` plus größerer
  Schatten, damit die ganze Zeile als Einheit lesbar ist.
* Warnhinweis „Datei fehlt": Farben als Token (`--warn-flaeche`,
  `--warn-rand`) mit Dunkelmodus-Wert; heute bleibt `#ffe9e6` im Dunkeln grell.

### 5.6 Hero (H1, H2) — S

* **Termin-Ticket:** zweite Aktion „Nächster Termin": Datum groß
  (tabular-nums), Label, Ort, Pfeil – als Karte auf der Bildkante oder
  Schiene unter dem Faktenband. Neues Front-Matter-Feld:

```yaml
naechster_termin:
  titel: "Tag der offenen Tür"
  datum: "2027-02-06"
  ort: "Jahnstr. 12-14"
  url: "/news/"
```

  plus Feld in `.pages.yml`. Regel: genau ein Termin; pflegbar ohne
  Designarbeit.
* **Abschluss-Chips** (Hauptschulabschluss … Berufsausbildung) werden Links:
  entweder auf Anker der Schularten-Seite oder – mit Finder (6.2) – auf
  `/schularten/?abschluss=abitur`. Zielgröße ≥ 44 px.
* **Sticker:** „UNESCO-Projektschule", „MINT-Schule" als ein bis zwei gedrehte
  Sticker auf der Bildkante; ersetzt nichts, ergänzt nur.
* **Regeln:** Hero-Text ≤ 320 Zeichen, Überschrift ≤ 5 Wörter, ein dominanter
  Primärbutton (besteht).

### 5.7 Kopf und Navigation (N1) — XS

* **Krankmelden mobil:** Der Schnellzugriff ist unter 900 px ausgeblendet und
  taucht nur im Footer auf. Vorschlag: kompakte Aktionszeile direkt unter dem
  Logo (`Krankmelden · Mail · Anfahrt`) oder als erster Block im
  Aufklappmenü, visuell als Chips. Das ist die am häufigsten genutzte
  Funktion der Schule.
* **Mobilkopf beruhigen:** Menüknopf auf ≤ 64 px Höhe (heute 83 px),
  Modusknopf mobil nur als Icon mit `aria-label="Farbschema umschalten"`,
  beide ≥ 44 px; Ziel: Kopfhöhe ≤ 96 px statt 110 px.
* **Menüpanel:** aktuell nur oben/unten Linien (`position: absolute` im
  Container). Entweder Rand links/rechts ergänzen oder Panel in voller
  Breite aufspannen – beides wirkt geschlossener als heute.
* **Menüpunkte:** „Termine" (`/#termine`) als sechsten Punkt aufnehmen – es
  ist eine Kernaufgabe; „Service" bleibt Anker.

### 5.8 Sprungleiste (D1) — XS

* Überlappung beheben (4.1).
* Mobil statt vier gestapelter Buttons (~200 px) eine **horizontal scrollbare
  Chip-Zeile**:

```css
@media (max-width: 640px) {
  .sprungleiste ul { flex-wrap: nowrap; overflow-x: auto; scroll-snap-type: x mandatory; }
  .sprungleiste li { scroll-snap-align: start; }
}
```

* Nach dem Sprung das Ziel markieren:
  `h2:target { background: var(--gelb); padding-inline: 0.4rem; }` –
  statische Hervorhebung, keine Animation nötig.

### 5.9 Fußbereich — nachrangig

Bleibt wie er ist. Optional „Zum Seitenanfang" im Rechtsstreifen.

### 5.10 Partner (P1) — S (mit Content-Auftrag)

Der Logostreifen ist ein Einzelbild (1023 px breit, sieben Logos, wird auf
1180 px hochskaliert) und für Screenreader eine einzige Grafik. Vorschlag:
**HTML-Gitter** aus Einzel-Logos (weiße Zelle, `--rahmen`,
`--schatten-klein`, sprechende Alt-Texte, optional je Link). Vorteile: scharf
auf allen Displays, einzeln pflegbar über Pages CMS (Liste), lesbar und
suchmaschinenfähig. Arbeitspaket: Logos aus der Quelldatei vereinzeln,
Freigabe einholen.
**Übergangslösung (XS):** Überschrift „Partner aus der Region", ein Satz
Kontext, besseres `alt`.

### 5.11 Instagram (I2) — XS

* Reel-Plakette (Play-Dreieck, Gelb, 44 px) auf den beiden Reel-Kacheln –
  bewegte Inhalte sind sonst von Fotos nicht zu unterscheiden.
* Stand-Hinweis als `hinweiszeile` („Stand: Oktober 2026 – der Feed wird
  redaktionell aktualisiert"), statt ein Live-Versprechen zu suggerieren.

---

## 6. Seiten und Wege

### 6.1 Startseite — S

Reihenfolge heute ist gut (Schularten → Aktuelles → Termine). Vorschläge:

1. Termin-Ticket (5.6) macht die Startseite handlungsfähig.
2. **Kategorie-Farbcode** (4.2) verbindet „Schularten entdecken" mit der
   Übersicht.
3. **Zahlenband (optional, Content-Auftrag):** vier Kennzahlen
   (Schüler:innen, Bildungsgänge, Lehrkräfte, Abschlüsse) als Kacheln mit
   Ziffern `clamp(3rem, 6vw, 5rem)`. Nur mit belegten Zahlen der GHSE und
   Quellenangabe im CMS-Feld; sonst nicht bauen.
4. Genau ein Band als Vollton-Gelb unterhalb des Faktenbands – Kandidat:
   „Schulleben" – damit Gelb nicht nur Linienfarbe ist.
5. Beschriftungen schärfen (Abschnitt 8).

### 6.2 Schularten (S1–S4) — M (Finder), S (Rest)

* **Finder (S1):** Filterleiste direkt unter dem Seitenkopf:

```text
Ich habe … [Hauptschulabschluss] [Mittlere Reife] [Fachhochschulreife] [Abitur]
Ich möchte … [Ausbildung] [Studium] [Beruf vorbereiten]
                                        [N Treffer] [Zurücksetzen]
```

  Technik: Karten erhalten `data-abschluss`/`data-kategorie` aus dem Front
  Matter; ~30 Zeilen Vanilla-JS filtern per `hidden`. Ohne JavaScript bleibt
  die heutige Liste vollständig sichtbar (progressive enhancement).
  Voraussetzung: `abschluss`-Werte vereinheitlichen (Datenauftrag mit der
  GHSE).
* **Zweier-Gruppen (S2):** Bei zwei Karten `.raster--2` verwenden – heute
  bleibt im „Teilzeitschularten"-Band die dritte Spalte leer.
* **Farbcode (F1)** und **Demo-Hinweis (I1):** Der Absatz „Diese Demo zeigt
  eine Auswahl …" wandert aus dem Einleitungstext in eine `hinweis`-Box mit
  Kicker „Prototyp" – gleiche Größe wie die anderen Hinweise, damit er nicht
  mit echtem Inhalt konkurriert.
* **Detailseite (S3):** Breadcrumb statt Zurück-Link (`Start › Schularten ›
  Technisches Gymnasium`), `nav[aria-label="Brotkrumen"]` inklusive. Die
  Kurzprofil-Hinweise (`layouts/schularten/page.html:14`) behalten – sie sind
  ehrlich und gut gestaltet.
* **Content-Auftrag (S4):** Kartenbilder mit schwacher Wirkung (z. B. die
  Flyer-Grafik beim Berufskolleg) durch Fotos ersetzen, sobald die GHSE
  liefert.

### 6.3 News (K1, T1)

Featured-Karte + Jahr-Gruppen (5.3). Detailseite: Meta-Zeile (Datum, Quelle)
unter die h1 als Chip-Zeile ziehen – heute steht sie darüber und konkurriert
mit dem Zurück-Link. Zoom-Plakette und Druck-Lesbarkeit unverändert lassen.

### 6.4 Downloads (D1–D3)

Sprungleiste reparieren (4.1, 5.8). Ein Textfilter lohnt sich erst ab ~30
Dateien – **nicht jetzt bauen** (bewusster Verzicht, siehe Abschnitt 9).

### 6.5 404 (W1) — XS

Hilfreicher machen: zusätzlich „Krankmelden" und „Termine" verlinken, Text
auf Aufgaben ausrichten („Vielleicht suchen Sie: …") statt nur auf
Seitenbereiche.

---

## 7. Barrierefreiheit: prüfbare Kriterien

| ID | Kriterium | Zielwert | Prüfweg |
|---|---|---|---|
| A1 | Ankersprung unter Kopf **und** Sprungleiste sichtbar | Überschrift volle Höhe sichtbar | Chromium 390/1440 px, `getBoundingClientRect` |
| A2 | Sprungleiste überlappt den Kopf nicht | 0 px Überlappung (heute 16/38 px) | gleiche Messung |
| A3 | Fokusring in jedem Band | ≥ 3:1 gegen beide Nachbarfarben; auf Nachtbändern Gelb | Tab-Reihe hell/dunkel, Screenshot |
| A4 | Zielgrößen | ≥ 24 px (AA); ≥ 44 px auf grobem Zeiger für Buttons, Chips, Kalender-Karten | Messung wie in Abschnitt 3 |
| A5 | Kontrast | jedes neue Tokenpaar in `qa/kontrast.py`, alle Paare bestehen | Skriptlauf |
| A6 | Dark Mode | neue Komponenten (Sticker, Featured-Karte, Warnhinweis, Finder) in beiden Token-Blöcken | Sichtprüfung + Skript |
| A7 | Reduced Motion | neue Interaktionen ohne Pflicht-Animation | `prefers-reduced-motion`-Emulation |
| A8 | Druck | Finder/Sprungleiste ausgeblendet, Featured-Karte druckt einspaltig | Druckvorschau Meldung/Downloads |

---

## 8. Inhalt und Tonalität

**Label-Regeln:** Imperativ oder Substantiv, ≤ 4 Wörter, kein „Hier klicken",
ein Ausrufezeichen pro Seite maximal, Umlaute korrekt.

| Ort | heute | Vorschlag |
|---|---|---|
| Servicerubrik H2 | „Über die GHSE" | „Service für Schüler/innen, Eltern und Lehrkräfte" |
| Berufsinfo-Button | „Noch mehr Infos" | „Alle Beiträge zur Berufsorientierung" |
| Schulleben-Button | „Jetzt erkunden" | „Zum Schulleben" |
| Kopf-CTA | „Anmelden & Formulare" | „Formulare & Anmeldung" (Ziel ist `/downloads/`) |
| Sprungleiste | „Sprung zu:" | „Kategorie:" |
| Servicekarte | „Einfach E-Mail: Jeder Lehrer ist …" | redaktionell glätten („Lehrkräfte sind über kuerzel@ghse.de erreichbar – …") |
| Demo-Hinweise | Fließtext-Absatz | einheitlicher Baustein „Prototyp-Hinweis" mit einem Satz und Link zur Originalseite |

---

## 9. Anti-Patterns (was wir nicht machen)

* Keine weiteren Schattenrichtungen/-farben, keine Verläufe, kein Blur, keine
  abgerundeten Ecken – der harte Kantenlook ist die Identität.
* Höchstens zwei Musterarten und drei Schriftgrößen-Sprünge pro Band.
* Keine Emoji als Icons; wenn Icons, dann ein kleines Inline-SVG-Set.
* Keine Live-Embeds (Instagram, Karten, Formulare Dritter) und kein
  Cookie-Banner als Attrappe.
* Kein Carousel für Aktuelles, keine Auto-Animationen ohne
  `prefers-reduced-motion`.
* Keine neuen Farben ohne Eintrag in `qa/kontrast.py`, kein neues
  Front-Matter-Feld ohne `.pages.yml`, keine erfundenen Zahlen oder Zitate.
* Kein JS-Bundle > ~5 KB; Lighthouse mobil nicht unter 98 drücken.

---

## 10. Priorisierung

**Stufe 1 – Quick Wins (je ≤ 2 h):** M1 Kopfhöhe/Anker (4.1) · N1
Krankmelden mobil + Kopf beruhigen (5.7) · A1 Fokusgelb auf Nachtbändern
(4.3) · K2 Kalender ganz klickbar (5.4) · D1 Leiste mobil scrollen (5.8) ·
D2 Button 44 px + Zeilen-Hover (5.5) · T1 tabular-nums (4.4) · I1
Hinweisbaustein (8) · W1 404-Quicklinks (6.5).

**Stufe 2 – halbe bis zwei Tage:** K1 Featured-News + Jahr-Gruppen (5.3) ·
F1/F2 Farbcode + Chip-System (4.2, 5.1) · H1 Termin-Ticket (5.6) · H2
Abschluss-Chips als Links (5.6) · S2 Zweier-Raster (6.2) · I2
Instagram-Reels (5.11) · P1 Partner-Gitter inkl. Logo-Vereinzelung (5.10).

**Stufe 3 – größer / mit Content-Bedarf:** S1 Schularten-Finder inkl.
`abschluss`-Datenpflege (6.2) · Zahlenband mit belegten Zahlen (6.1) ·
Schulleben als gelbes Vollflächenband (4.5) · Breadcrumbs (6.2) ·
AVIF-Bilder (nur wenn Lighthouse fällt).

---

## 11. QA-Checkliste nach jeder Runde

- [ ] `hugo -D` läuft ohne Warnungen; `qa/kontrast.py` ohne Fehler.
- [ ] `qa/linkcheck.py` gegen `public/` läuft fehlerfrei (interne Ziele).
- [ ] Lighthouse mobil ≥ 98 für Startseite, News, Schularten, Downloads.
- [ ] Ankersprung: Kategorie-Ziel bei 390 px vollständig sichtbar (A1/A2).
- [ ] Tab-Reihe durch Hell und Dunkel: Fokusring überall ≥ 3:1 (A3).
- [ ] Zielgrößen-Messung: keine Pflichtaktion unter 44 px mobil (A4).
- [ ] Dark Mode gesichtet: beide Token-Blöcke identisch gepflegt (A6).
- [ ] Druckvorschau für Meldung und Download-Seite (A8).
- [ ] Neue Felder in `.pages.yml`, Feldnamen exakt wie im Template.
- [ ] Neue Farben als Token, keine Hex-Werte in Komponenten.

---

## 12. Werkzeuge und Nachweise

* Kontrast: `qa/kontrast.py` (37 Paare, Hell/Dunkel) – neue Paare ergänzen.
* Links: `qa/linkcheck.py`, `qa/livecheck.py`.
* Messserver (Keep-Alive + gzip wie GitHub Pages): `tools/preview-server.py`.
* Metriken: `METRIKEN.md` (GL 99, YL 96, MO 50 C – letzter Lauf 17.10.2026).
* Messmethode dieses Dokuments: lokaler Hugo-Bau, Chromium-Headless mit
  eingebetteten iframes (1440/640/390 px), Layoutwerte per
  `getBoundingClientRect`; bestehende Belegscreenshots liegen in `qa/`
  (heller und dunkler Modus).

---

*Hinweis: Vorschläge 6.1 (Zahlenband), 5.10 (Partnerlogos einzeln) und
6.2 (Finder-Datenpflege) brauchen Inhalte oder Freigaben der GHSE. Alles
andere ist mit dem vorhandenen Stand umsetzbar, ohne die Leitplanken aus
Abschnitt 1 zu verlassen.*
