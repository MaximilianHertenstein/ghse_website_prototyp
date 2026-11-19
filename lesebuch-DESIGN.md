# GHSE – Gestaltungsvariante „Lesebuch“ (Theme 5)

Fünfte Gestaltung derselben Website. Eigenständiger Entwurf, kein Ableger
der vier bestehenden Varianten. Interne Kennung `lesebuch`; im Umschalter
steht „Lesebuch“.

## 1. Konzept

**Die Schule als Buch mit blauer Kopfleiste.** Die GHSE ist eine Schule, an der
sehr verschiedene Menschen und Fächer zusammenkommen. Statt einen einzelnen
Fachbereich zum Bild der Schule zu machen, zeigt dieses Theme die Schule als
*Lese- und Schaubuch*: ein Band, in dem viele Kapitel stehen. Die blaue
Kopfleiste ist der Rücken des Bandes; sie liegt über der Seite und bleibt
beim Lesen sichtbar. Das gelbe Lesebändchen markiert die Stelle, an der man
gerade ist. Die Seiten sind rötlich-graues, griffiges Papier, die Fotografien
sind Tafeln, die Zwischenüberschriften sind Kapitelanfänge.

Daraus folgen alle Entscheidungen:

- **Ort der Navigation:** Die blaue Kopfleiste trägt das Verzeichnis. Sie
  liegt über der Seite und bleibt beim Lesen langer Seiten (Schularten,
  Downloads, UNESCO) immer erreichbar; die Seite darunter bleibt eine ruhige
  Lesefläche. Die frühere feste Randspalte ist bewusst aufgegeben.
- **Lesefläche statt Kartenwand:** Karten, Schatten und Rundungen entfallen.
  Einträge werden zu Zeilen und Tafeln, getrennt durch Haarlinien. Das Buch
  hat keine Karten; es hat Absätze, Tafeln und ein Register.
- **Eine Schrift mit klarer Aufgabe:** Public Sans trägt Überschriften,
  Fließtext, Navigation, Beschriftungen, Daten und Bedienelemente. Eine
  Serifenschrift wird bewusst nicht verwendet; die Buchwirkung entsteht aus
  Papier, Tafeln, Haarlinien und dem Verzeichnis, nicht aus dem Satz.
- **Fotografie als Tafel:** Die echten GHSE-Fotos stehen in der Breite ihrer
  Spalte, mit 1-px-Linie, ohne Rahmen, Schatten oder Drehung. Sie zeigen
  Menschen und Orte der Schule, keine Stockmotive.

## 2. Verhältnis zu den vier bestehenden Varianten

| Variante | Gestalterischer Ansatz | Was „Lesebuch“ bewusst nicht übernimmt |
| --- | --- | --- |
| Neo | Plakativ, gelbe Markenfläche, harte Schatten, Sticker, Inter | keine Flächenmarke, keine Schatten, keine Sticker, keine Plakativität |
| Klar | Freundlich, hellblau, viel Weißraum, runde Karten, Roboto/Poppins | kein Hellblau als Grundton, keine Karten, keine Rundungen |
| Funktional | Streng schwarz/weiß, Handbuch, Hanken Grotesk, harte Linien | keine Schwarzweiß-Strenge; Papier ist warm-grau und trägt den Ton |
| Modern | Marineblau/GHSE-Blau, Familjen Grotesk, weiche Karten, Verläufe | keine Karten, keine Verläufe, kein blaues Hero-Band; Blau ist der Buchrücken, nicht die Seite |

Die Eigenständigkeit liegt nicht in einer weiteren Palette, sondern in der
**räumlichen Ordnung**: blaue Kopfleiste mit Verzeichnis, Lesespalte,
Tafeln und Haarlinien statt Kartenraster. Auf den ersten Blick unterscheidet
sich „Lesebuch“ von allen vier durch die blaue Kopfleiste, die ruhige
Grotesk und das Fehlen von Karten.

## 3. Farben

| Rolle | Token | Hell | Dunkel | Verwendung |
| --- | --- | --- | --- | --- |
| Papier | `--lb-papier` | `#e3e5dd` | `#161a17` | Seitenfläche |
| Papier tief | `--lb-papier-2` | `#d7dad0` | `#1e231f` | Bänder, Fuß, Register |
| Tinte | `--lb-tinte` | `#171b18` | `#eceee4` | Text, Überschriften, Linien |
| Leise | `--lb-leise` | `#4e544c` | `#b4b9ac` | Sekundärtext, Daten |
| Haarlinie | `--lb-linie` | `#b3b8ac` | `#3a413a` | Trennlinien, Rahmen |
| Kopfleiste | `--lb-blau` | `#114c92` | `#0d3a70` | Navigationsleiste, Kopf |
| Kopfleiste tief | `--lb-blau-tief` | `#0c3a71` | `#092c56` | Verlaufspol, Hover |
| Serviceleiste | `--lb-logo-flaeche` | `#f2f0e6` | `#1e231f` | helle Leiste über der Kopfleiste; früher nur Logo-Fläche |
| Lesebändchen | `--lb-gelb` | `#f6dc56` | `#f6dc56` | aktive Stelle, Fokus auf Blau |
| Link | `--lb-link` | `#0f3f7a` | `#a9c6ea` | Links im Text |
| Fokus | `--lb-fokus` | `#0f3f7a` | `#f6dc56` | Fokusring auf Papier |

Blau und Gelb sind die Farben des GHSE-Zeichens; sie werden hier
strukturell eingesetzt (Kopfleiste, Lesebändchen), nicht als Dekoration. Grün
und Orange entfallen ganz. Das Papier ist ein kühles Graugrün, kein Creme.

Kontraste (hell): Tinte/Papier 13,7:1 · Leise/Papier 6,1:1 · Link/Papier
8,2:1 · Blau/Papier 6,7:1 · Gelb/Blau 6,2:1 · Hell/Blau 7,8:1 ·
Tinte/Gelb 12,7:1. Dunkel: Tinte/Papier 15,0:1 · Leise/Papier 8,8:1 ·
Link/Papier 10,0:1 · Gelb/Blau 8,2:1. Text auf Gelb bleibt in beiden Modi
`#171b18` (`--lb-auf-gelb`), damit der Button im Dunkelmodus nicht kippt.

## 4. Typografie

- **Public Sans** (variabel 400–700, selbst gehostet, SIL OFL): eine
  Schrift für alles. Fließtext 1,09 rem / 1,7; H1
  `clamp(2,2rem, 4vw, 3,15rem)` / 1,03; H2 `clamp(1,9rem, 3vw, 2,5rem)` /
  1,1; H3 1,35 rem. Überschriften 600, keine künstliche Laufweite unter 0.
- **Bedienung:** Navigation 1 rem, Beschriftungen 0,8125 rem, Zeile 1,4;
  keine Versalien, keine Sperrung.
- **Ziffern:** Datum, Dateigröße und Telefonnummern in Public Sans mit
  `font-variant-numeric: tabular-nums`.
- **Zeilenlänge:** Fließtext 68ch; Einleitungen 46ch; Karten-/Tafeltexte
  höchstens 55ch.
- **Umbruch:** `text-wrap: balance` für Überschriften, `pretty` für Absätze,
  `hyphens: auto` im Fließtext.

## 5. Aufbau

### Kopfleiste (alle Breiten)

- Zwei Zeilen: eine helle **Serviceleiste** im Papierton mit Adresse/Telefon,
  Schnellzugriffen, Stilwahl und Farbmodus; darunter die blaue
  **Kopfleiste** mit Logo, Hauptnavigation und gelbem „Krankmelden“.
- Das GHSE-Zeichen steht ohne Plakette direkt auf dem blauen Verlauf; der
  Verlauf nimmt die Blautöne des Zeichens auf. Die frühere Logo-Fläche ist
  jetzt die volle Serviceleiste.
- Ab 1200 px stehen die acht Kapitel waagerecht. Die aktive Stelle trägt ein
  gelbes Lesebändchen (4 px) an der Unterkante; Unterkapitel öffnen als
  Papier-Dropdown bei Hover und Tastaturfokus, nicht dauerhaft. Die
  Menüpfeile entfallen am Desktop.
- Unter 1200 px bleibt die Kopfzeile mit Menüknopf; das Panel ist eine
  Papierseite mit Verzeichnis, dieselben Linien und das gelbe Lesebändchen.
  Die Serviceleiste ist ab 901 px sichtbar und auf schmalen Geräten
  ausgeblendet.
- `assets/js/lesebuch.js` hält die Serviceleiste in der DOM-Reihenfolge oben;
  es gibt keine Umsortierung mehr. `nav.js` misst die Kopfhöhe für
  Ankersprünge und die Sprungleiste.
- Die Seite läuft über die volle Breite; die Lesespalte bleibt zentriert.
- Der Schulname steht als Masthead über dem Titel: 1,15–1,6 rem, Tinte,
  Haarlinie darunter. Er ist kein Etikett, sondern der Name der Schule;
  auf Wunsch der GHSE bewusst größer als in den anderen Varianten.

### Seiten

- **Startseite:** Titelseite mit großem Schulnamen als Masthead, H1,
  Leitsatz, Abschluss-Verzeichnis und einer Tafel, die die rechte Spalte
  in der Höhe des Textblocks füllt; danach Kapitel (Schularten, Instagram,
  Aktuelles, Termine, Service, Schulleben, Partner). Die Abschluss-Links sind unterstrichen,
  die Instagram-Beiträge stehen als vierteiliger Streifen, nicht als
  Posterwand.
- **Seitenkopf:** Brotkrumen als leise Zeile, H1 in Public Sans, Leitsatz in
  1,3 rem, darunter eine Haarlinie statt Farbkante.
- **Kapitel:** H2 in Public Sans, 2,5 rem, mit Haarlinie darüber; die
  Kapitelaktion ist ein unterstrichener Textlink, kein Knopf.
- **Einträge:** Bildtafel (16:10), darüber eine Haarlinie, darunter
  Kategorie, Titel, Text, Aktion als unterstrichener Text. Kein Kasten,
  kein Schatten, kein Radius.
- **Schulart-Seite:** Lesespalte und Randspalte mit „Auf einen Blick“ als
  Randnote (2-px-Blaulinie links, keine Karte); die Bildfolge ist ein
  Tafelraster mit Bildunterschriften.
- **Downloads:** Registerleiste mit Kategorien als Text, klebend unter dem
  oberen Rand; Zeilen mit Haarlinie, Dateiangaben als leiser Text,
  „Herunterladen“ als unterstrichener Textlink. Mobil bleibt das Label
  „Kategorie“ sticky, der Streifen zeigt einen dünnen Scrollbalken und
  kein Scroll-Snap, damit die erste Kategorie nicht unter dem Label liegt.
- **Meldungen:** Meldungskopf mit Datum und Quelle als Zeile, H1, Leitsatz,
  danach Fließtext; Zeitungsscans als Tafel mit Rahmen.
- **Fuß:** Papier tief, Haarlinie oben, vier Spalten als Kolophon;
  Abschnittstitel in Public Sans, Links unterstrichen; keine Farbkante.
  Auf kurzen Seiten sitzt der Fuß am unteren Fensterrand.

## 6. Bewegung und Zustände

- Keine Auftrittsanimationen. Übergänge nur für Farbe, Unterstreichung und
  Rahmen (150 ms), nie für Größe oder Position.
- Hover: Unterstreichung oder Farbwechsel; kein Anheben, kein Zoomen.
- Fokus: 3 px Ring, 3 px Abstand, sofort sichtbar; auf Blau gelb, auf
  Papier blau.
- `prefers-reduced-motion` wird respektiert (keine Übergänge).

## 7. Zugänglichkeit

- Alle Texte ≥ 4,5:1, Fließtext ≥ 7:1; Fokusring ≥ 3:1 zur Fläche.
- Zeigeziele ≥ 44 px auf Touch; die Navigationszeilen sind 44 px hoch.
- Semantik und Reihenfolge bleiben unverändert (dieselben Templates); die
  Kopfleiste ist die Hauptnavigation und behält ihre `aria-label`.
- Der Umschalter bleibt ein natives Auswahlfeld; Tastatur und
  Screenreader-Verhalten ändern sich nicht.
- Keine Information hängt an Farbe allein: die aktive Stelle trägt
  `aria-current`, das Lesebändchen ist zusätzlich eine Linie.

## 8. Technische Isolation

- Neue Datei `assets/css/lesebuch.css`; jede Regel ist auf
  `:root[data-design="lesebuch"]` begrenzt. Keine Änderung an `main.css`,
  `klar.css`, `funktional.css`, `modern.css`, an Layouts oder gemeinsamen
  Skripten; `assets/js/lesebuch.js` gehört ausschließlich zur Variante.
- Neue Schrift Public Sans unter `assets/fonts/lesebuch/` (SIL OFL), eingebunden über
  `layouts/_partials/schriften-lesebuch.html`; das Partial wird nur durch
  den neuen Eintrag in `params.designs` geladen.
- `assets/js/lesebuch.js` (nur über das Theme-Partial geladen) hält die
  Serviceleiste in der DOM-Reihenfolge oben; es gibt keine Umsortierung
  mehr. Kontakt und Öffnungszeiten stehen im Fuß.
- `hugo.toml` erhält ausschließlich einen weiteren Eintrag am Ende der
  Design-Liste.
- Vorschau: `static/bilder/themes/lesebuch.webp`.

## 9. Qualitätssicherung

- Hallmark: Stamp und Pre-emit-Kritik im CSS-Kopf, `sloplint` gegen die
  gebaute Seite, Prüfung der Gates (Floor/Reflex/Finish).
- Impeccable: Detector auf Start, Meldungen, Downloads, Schulart und
  Artikel bei 1440/1024/390; Critique und Polish; anschließend erneut.
- Projekt-QA: `qa/themes.py` (sieben Varianten), `qa/design.py`,
  `qa/layout.py`, `qa/reflow.py`, `qa/linkcheck.py`, `qa/unterpfad.py`,
  Kontrastprüfung der eigenen Tokens.
- Bestandsschutz: `qa/theme5-guard.py` mit Prüfsummen aller vorhandenen
  Dateien; `qa/themebilder.py` mit Referenzaufnahmen der vier Varianten
  (1440/1024/390, sechs Seiten) und Pixelvergleich.
