---
name: GHSE Klar (Clean)
colors:
  primary: "#1E40AF"
  secondary: "#3B82F6"
  success: "#166534"
  warning: "#92400E"
  danger: "#991B1B"
  surface: "#FFFFFF"
  text: "#111827"
  neutral: "#F9FAFB"
typography:
  body:
    fontFamily: "Roboto"
    fontSize: 1.25rem
  heading:
    fontFamily: "Poppins"
    fontSize: 2rem
  label-caps:
    fontFamily: "Roboto"
    fontSize: 0.875rem
  weights: "400, 500, 600"
rounded:
  sm: 4px
  md: 8px
spacing:
  sm: 8px
  md: 16px
---

# GHSE – Gestaltungsvariante „klar“ (Design-System „Clean“)

Zweite Gestaltung derselben Website neben dem Neobrutalismus (`Neobrutalismus-DESIGN.md`). Aufgebaut nach dem Design-System **Clean** (typeui.sh): minimal, viel Weißraum, gut lesbare Schrift, begrenzte Palette. Angepasst für Leserinnen und Leser um 60 bis 65 Jahre. Wo Clean und Lesbarkeit kollidieren, gewinnt die Lesbarkeit; die Abweichungen stehen unten und sind begründet.

„Muss“ ist nicht verhandelbar, „sollte“ ist eine Empfehlung.

## 1. Kontext und Ziel

Absicht in einem Satz: *Dieselben Inhalte und dieselbe Navigation, ruhig und ohne Ablenkung gestaltet, sodass Text ohne Anstrengung lesbar und jedes Ziel sicher zu treffen ist.*

- Struktur, Inhalte, Menüs und Dropdowns sind identisch mit der Hauptvariante. Es ändert sich nur das Aussehen.
- Erreichbar über den Umschalter in der Kopfleiste (ab 1101 px) und im Menü (bis 1100 px) – dieselbe URL, ohne Neuladen.
- `params.designs` in `hugo.toml` listet die Varianten; `klar.css` wird auf jeder Seite mitgeladen und ist auf `:root[data-design="klar"]` begrenzt. Ohne Wahl bleibt die Hauptvariante (`data-design="neobrutalismus"`).
- Die Wahl liegt in `localStorage` (`ghse-design`); `?design=klar` öffnet die Variante ohne zu speichern (für QA und zum Teilen). `design.js` schaltet um und hält beide Menüs synchron.
- Jede Regel in `klar.css` trägt das Präfix `:root[data-design="klar"]` und gewinnt damit ohne `!important` (Ausnahmen: `translate` und der Druck-Block). Kein CSS-Nesting.
- `rel="canonical"` zeigt auf dieselbe URL; die Variante ist rein clientseitig und ändert das Markup nicht.

## 2. Tokens und Grundlagen

Rohwerte stehen nur im Token-Block am Anfang von `klar.css`. Alles Weitere benutzt Tokens.

| Rolle | Token | Hell | Dunkel | Verwendung |
| --- | --- | --- | --- | --- |
| Text | `--text` | `#111827` | `#f9fafb` | Fließtext, Überschriften (≥ 7:1) |
| Zweittext | `--text-leise` | `#4b5563` | `#d1d5db` | Beschreibungen, Metadaten (≥ 7:1) |
| Primär (Fläche) | `--primaer` | `#1e40af` | `#1e40af` | Flächen mit weißer Schrift, `.band--blau`, aktives Menü |
| Primär (Text) | `--primaer-text` | `#1e40af` | `#93c5fd` | Links, Textakzente (≥ 7:1) |
| Akzent | `--primaer-akzent` | `#3b82f6` | `#3b82f6` | Linien, Balken, Icons; **nie Text** (Clean-Primärblau) |
| Hellfläche | `--primaer-hell` | `#dbeafe` | `#dbeafe` | Hover, Markierung, mit dunkler Schrift |
| Aktion | `--aktion` / `--aktion-schrift` | `#1e40af` / `#fff` | `#93c5fd` / `#111827` | Primärer Button |
| Fläche | `--papier`, `--flaeche-leise` | `#fff`, `#f9fafb` | `#111827`, `#1f2937` | Seite, Hero, Karten im Dunkeln |
| Linie | `--rand-leise` / `--rand` | `#e5e7eb` / `#4b5563` | `#374151` / `#9ca3af` | Kartenrand und Trenner / Rand bedienbarer Elemente (≥ 3:1) |
| Erfolg, Warnung, Fehler | `--erfolg`, `--warnung`, `--fehler` | `#166534`, `#92400e`, `#991b1b` | `#86efac`, `#fcd34d`, `#fca5a5` | Clean-Signalfarben, für Text abgedunkelt (≥ 7:1) |

Die Tokens aus `main.css` (`--gelb`, `--orange`, `--blau`, `--link` …) werden in `klar` auf diese Rollen abgebildet. So verschwinden Gelb und Orange ohne Eingriff in die Templates; die fünf Wertefarben der Schule (`--wert-*`) bleiben als Inhalt erhalten.

**Schrift.** Roboto (Text) und Poppins 600 (Überschriften), selbst gehostet unter `assets/fonts/klar/` (Lizenz: SIL OFL, Text in `LIZENZ.txt`). Die `@font-face`-Regeln stehen auf jeder Seite (`_partials/schriften-klar.html`); geladen werden die Dateien erst, wenn die Variante sie benutzt (`font-display: swap`, kein Preload). Inter wird dann nicht abgerufen.

| Stufe | Token | Größe | Verwendung |
| --- | --- | --- | --- |
| Beschriftung | `--t-xs` | 14 px | Datum, Bildunterschrift (kleinste erlaubte Größe) |
| Zweittext | `--t-s` | 16 px | Fuß, Kasten, Brotkrumen |
| Bedienung¹ | `--t-ui` | 18 px (mobil 16) | Menü, Buttons, Chips, Kartentext |
| Fließtext | `--t-m` | 20 px (mobil 18) | Absätze, Einleitungen |
| H3 / H2 | `--t-h3` / `--t-h2` | 20–24 / 24–32 px | Überschriften |
| H1 / Hero¹ | `--t-h1` / `--t-display` | 32–40 / 32–48 px | Seitentitel, Hero |

¹ Abweichung von Clean (12/14/16/20/24/32): zusätzlich 18, 40 und 48 px; 12 px entfällt. Begründung: 16 px ist für diese Zielgruppe die Untergrenze und nicht der Normalfall.

**Raster.** 8 pt: Abstände und Polster in Vielfachen von 0,5 rem (4 px nur für Kleinstabstände), Abschnitte `clamp(3rem, 6vw, 5rem)`, Zeigeziele mindestens 3 rem hoch. Radius 8 px (Karten, Buttons), 4 px (Chips, Marken).

## 3. Komponenten

Gemeinsam: keine Schatten (Ausnahme: Dropdown-Tafel), keine Schrägstellung, keine Bewegung beim Überfahren, keine Versalien.

| Komponente | Aufbau und Varianten | Zustände |
| --- | --- | --- |
| Button `.btn` | min. 48 px hoch, 18 px/600, Rand 2 px `--rand`. `--akzent` gefüllt (`--aktion`), `--geist` transparent, `--klein` 16 px | Hover: Unterstreichung + innerer Rand 2 px. Aktiv: innerer Rand 3 px. Fokus: 4 px Ring. Deaktiviert: `main.css` |
| Chip `.chip`, Hero-Chips | 48 px hoch, Rand 1 px `--rand`, Radius 8 px | wie Button |
| Karte `.karte`, `.service`, `.zeile`, `.kalender`, `.instabeitrag` | weiß, Rand 1 px `--rand-leise`, Radius 8 px, Polster 24 px, kein Balken | Hover und Fokus innen: Rand `--primaer-akzent`. Titel unterstrichen |
| Menü und Dropdown | gleiche Struktur wie `main`, Einträge 48 px hoch, Tafel mit Rand und weichem Schatten | Hover: `--primaer-hell`. Aktuelle Seite: `--primaer` mit Weiß. Tafel schließt 0,35 s verzögert, Wechsel zur nächsten Kategorie sofort |
| Link im Text | `--primaer-text`, unterstrichen 2 px | Hover: `--primaer-hell`, Unterstreichung bleibt |
| Gestaltungswahl `.stilwahl` | Label 14 px in `--text-leise`; Auswahlfeld 44 px hoch, Rand 1 px, Radius 8 px, kein Schatten. Ab 1101 px in der Leiste, darunter im Menü | Fokus: 4 px Ring; Wechsel ohne Neuladen |
| Hinweis `.hinweis` | `--hinweis-flaeche`, Rand 1 px `--hinweis-rand` | – |
| Tabelle | Rand 1 px, Polster 8/12 px (mobil 4/8), lange Wörter trennen und brechen | – |

Responsiv: ab 1200 px Dropdowns, darunter Panel mit Pfeilknöpfen. Unter 640 px: Fließtext 18 px, Kopfzeile mit Logo, Farbmodus, Krankmelden und Menü; unter 380 px kleineres Logo. Die Gestaltungswahl steht ab 1101 px in der Leiste, darunter im Menü. Leer-, Lade- und Fehlerzustände gibt es auf dieser statischen Seite nicht; sollten Formulare dazukommen, gelten `--fehler` und `--erfolg` mit Symbol und Text (nie nur Farbe).

## 4. Barrierefreiheit (prüfbar)

| Anforderung | Schwelle | Prüfung |
| --- | --- | --- |
| Text- und Linkkontrast | ≥ 7:1 (AAA); Rand bedienbarer Elemente und Akzentlinien ≥ 3:1 | `qa/kontrast_klar.py` (Hell und Dunkel, 31 Paare); `qa/klar_pruefung.py` (berechnete Farben aller Textstellen) |
| Kleinste Schrift | ≥ 14 px | `qa/klar_pruefung.py` |
| Zeigeziele | ≥ 44 px Höhe; kleine Textlinks durch unsichtbar vergrößerte Fläche | `qa/klar_pruefung.py` |
| Fokus | 4 px Ring, 4 px Abstand, auf blauem Band hell; nicht vom Kopf verdeckt (`--kopfhoehe`) | Tab-Durchlauf von Hand |
| Tastatur | Dropdowns öffnen per Fokus; erster Eintrag per Tab erreichbar | Tab-Durchlauf von Hand |
| Bewegung | keine Hover-Bewegung (`translate: none`); `prefers-reduced-motion` wie in `main.css` | `qa/klar_pruefung.py` (keine Rotation) |
| Reflow | kein waagerechter Überlauf bei 320–1440 px, Hell und Dunkel | `qa/klar_pruefung.py` |
| Semantik | Markup identisch mit der Hauptvariante, kein ARIA hinzugefügt | `qa/linkcheck.py`, Vergleich der HTML-Ausgabe |

## 5. Inhalt und Ton

Klar und freundlich, ohne Versalien. Kleinschreibung nach Satzregeln gilt auch für Beschriftungen; keine Kürzel ohne Erklärung.

| Do | Don't |
| --- | --- |
| „Termine im Schuljahr“, „Mehr erfahren“ | „TERMINE“, „Hier klicken“ |
| Links benennen ihr Ziel („Anfahrt“) | Links nur mit „mehr“ oder „weiter“ |
| Ein Absatz, ein Gedanke, ≤ 66 Zeichen Zeilenbreite | lange Textwände, zentrierter Fließtext |

## 6. Anti-Patterns

- **Muss nicht:** Versalien, gesperrte Schrift, Schrägstellung, harte Schatten, Hover-Hüpfen, Farbe als einziger Bedeutungsträger, Text kleiner als 14 px.
  Don't: `text-transform: uppercase`, `transform: rotate()`, `box-shadow: 4px 4px 0`.
- **Muss nicht:** neue Rohfarben oder Pixelwerte in Komponenten. Do: Token verwenden. Don't: `#3b82f6` als Textfarbe (3,7:1).
- **Sollte nicht:** mehr als eine Akzentfarbe. Do: `--primaer-akzent`. Don't: wieder Gelb/Orange/Blau reihum.

## 7. Wenn sich `main.css` ändert (Migration)

- Neue Komponente mit Rahmen, Schatten, Schräglage, Hover-Versatz oder Versalien: in `klar.css` mit demselben Selektor plus Präfix zurücknehmen.
- Setzt `main.css` im Dunkeln ein neues Token, setzt `klar.css` es ebenfalls (`qa/kontrast_klar.py` schlägt sonst an).
- Neue feste Schriftgrößen (rem außerhalb von `--t-*`) bleiben unverändert, bis sie in `klar.css` angehoben werden.
- Neue harte Schatten über `--schatten-farbe` sind in klar automatisch unsichtbar, feste Farben nicht.

## 8. QA-Checkliste (Code-Review)

1. `python3 qa/kontrast_klar.py` → 0 Fehler.
2. `python3 qa/linkcheck.py public` → 0 Fehler (beide Varianten nutzen dieselben Links).
3. Hauptvariante vor/nach der Änderung bauen und mit `diff -rq` vergleichen → keine sichtbaren Unterschiede außer dem Umschalter.
4. `hugo --baseURL / -d /tmp/klar` und `python3 qa/klar_pruefung.py /tmp/klar` → 0 Befunde (Versalien, Rotation, Schatten, Schrift, Zeigeziele, Kontrast, Überlauf). Die Prüfung ruft die Seiten mit `?design=klar` auf.
5. Sichtprobe: Hell, Dunkel, 1440 px und 390 px; Menü mit Maus und Tab; Hero, Karte, Tabelle, Download-Zeile; Umschalter in Leiste und Menü.
6. Keine neue Rohfarbe, keine neue feste Pixelgröße außerhalb des Token-Blocks.
7. `python3 qa/layout.py`, `qa/reflow.py`, `qa/unterpfad.py` für die Hauptvariante bleiben grün.