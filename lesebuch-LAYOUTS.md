# Lesebuch – Layoutprüfung aller Seitenvorlagen

Prüfung von Theme 5 gegen die Skills aus
[jakubkrehel/skills](https://github.com/jakubkrehel/skills):
`better-interface`, `better-accessibility`, `better-layout`,
`better-typography`, `better-colors`, `better-ui` (Fassung im Projekt unter
`.agents/skills/`). Die vier bestehenden Varianten waren nicht Teil der
Überarbeitung; ihre Unverändertheit ist separat belegt
(`qa/theme5-guard.py`, `qa/themebilder.py`).

## Umfang

| Vorlage | Seiten | Geprüft |
| --- | --- | --- |
| `home.html` | Startseite | 1440/1024/390, hell/dunkel, 320 px, 200 % Zoom |
| `news/section.html` | `/news/` | 1440/1024/390, hell/dunkel |
| `news/page.html` | Meldungen mit Zeitungsscan | 1440/1024/390, hell/dunkel |
| `schularten/section.html` | `/schularten/`, Unterseiten | 1440/1024/390 |
| `schularten/page.html` | Schulart mit Randnote | 1440/1024/390, hell/dunkel |
| `downloads/section.html` | `/downloads/` | 1440/1024/390, hell/dunkel |
| `_default/single.html` | Prosa (u. a. `/die-ghse/`, `/berufsinformation/`, `/anmeldeformulare/`) | 1440/1024/390 |
| `404.html` | Fehlerseite | 1440/390 |
| Shortcodes | `bild`, `bilder`, `downloads`, `hinweis`, `karten`, `mehr`, `video`, `werte` | auf den Seiten oben sowie `/unsere-schule/`, `/technik-und-management/` |
| Chrome | Kopf/Rücken, Menü, Stilwahl, Fuß, Fokus | 1440/1024/390, Tastatur, hell/dunkel |

Nicht anwendbar: Formulare (die Website hat keine), Datenvisualisierung,
RTL-Oberfläche (keine `dir="rtl"`-Seite), native Apps.

## Behobene Befunde

| Schwere | Ort | Vorher | Nachher | Warum |
| --- | --- | --- | --- | --- |
| HIGH | `lesebuch.css` (Krankmelden, Sprungmarke) | Gelbe Fläche mit `--lb-tinte`; im Dunkelmodus hell auf gelb, 1,17:1 | `--lb-auf-gelb: #171b18` in beiden Modi, 12,67:1 | 1.4.3 AA; der wichtigste CTA war im Dunkelmodus unlesbar |
| HIGH | `.kopf` (Rücken) | `order` schob die Serviceleiste visuell nach unten, die Tastatur lief ihr zuvor (11 Stopps vor dem ersten Kapitel) | Serviceleiste ab 1200 px ausgeblendet; Modus, CTA, Schnellzugriffe, Stilwahl und Verzeichnis stehen in DOM-Reihenfolge | 2.4.3; visuelle und Fokus-Reihenfolge sind jetzt identisch, ohne DOM-Umbau |
| MEDIUM | `lesebuch.css` (Fuß) | Kurze Seiten ließen den Fuß mitten im Fenster stehen | `body` als Flex-Spalte mit `min-height: 100svh`, `main { flex: 1 }` | Seiten wie `/anmeldeformulare/` enden jetzt am unteren Rand |
| MEDIUM | `.sprungleiste` mobil | Scroll-Snap zog die Liste unter das stehende „Kategorie“-Label; die erste Kategorie war angeschnitten | Kein Snap, Label bleibt sticky, dünner Scrollbalken | Inhalt war hinter dem Label nicht lesbar (better-layout: versteckter Inhalt braucht eine sichtbare Spur) |
| MEDIUM | `.fliesstext`, `.zeile__beschreibung` | 91–93 Zeichen pro Zeile bei 1440 px | 60ch im Fließtext, 55ch in Download-Zeilen; gemessen 653 px / 17,44 px | better-typography: 60–75 Zeichen; Detector jetzt 0 Befunde |
| MEDIUM | `.linkpfeil` | „ORGANIGRAMM VERGRÖSSERN“ in Versalien mit oranger 4-px-Kante | Satzcase, Public Sans 500, blaue Unterstreichung | Der Shortcode-Link fiel als einziger aus der Theme-Sprache |
| MEDIUM | `.kasten__kontakt` | Schwarze 3-px-Kante quer durch die Randnote | 1-px-Haarlinie in der Papierfarbe | Die Kante schnitt „Alle Downloads“ an |
| MEDIUM | Bildrahmen | Getönte Papierfarbe als Rahmen | `--lb-bildrand` (`rgba(0,0,0,.12)` hell, `rgba(255,255,255,.16)` dunkel) | better-ui: Inhaltsbilder mit reinem Schwarz/Weiß-Outline, kein Farbstich |
| LOW | `.seitenkopf .einleitung` | Haupt-CSS: 40ch, ohne Theme-Stimme | 52ch, Piazzolla 1,15–1,35 rem | Seitenköpfe aus Schularten/Prosa lesen sich wie der Leitsatz |
| LOW | `.werte` (Leitbild) | Fünf Regenbogenfarben als Quadrate | Blau/Gelb des Themes; „Vielfalt“ als geteilte Fläche | Farbe bleibt Zusatz, die Labels tragen die Bedeutung |
| LOW | `.video` | Schwarzer Rahmen, gelber Kreis, harter Schatten | Papier-Tafel, blaues Abspielquadrat, kein Schatten | Video ist eine Tafel wie die Bilder |
| LOW | `.partnergitter__kachel` | Hover auf einer nicht interaktiven Kachel | Hover entfernt | better-ui: kein Hover auf statischen Elementen |
| LOW | `.fliesstext strong` | 700 neben 400/500/600 | 600; drei Gewichte (400/500/600) | Ruhigere Gewichtsstaffel, Emphasis bleibt |
| LOW | Skip-Link | Blauer Ring auf blauem Rücken (1,23:1) | Gelber Ring auf dem Rücken | 1.4.11; der Fokusring ist auch am ersten Stopp sichtbar |
| LOW | `html` | Kein `scroll-padding` | `scroll-padding-block-start: calc(--kopfhoehe + .5rem)` | Fokus und Anker landen nicht unter dem klebenden Kopf |
| LOW | Rücken | Kein sichtbarer Hinweis auf weiteren Inhalt | Dünner Scrollbalken + weiche Kante unten | better-layout: versteckter Inhalt braucht eine Spur |

## Bewusste Entscheidungen

- **Schulname als Impressum-Zeile:** `.hero__marke` steht im DOM vor dem
  Titel (für Screenreader und die Faktenlage richtig), wird aber unter dem
  Abschlussverzeichnis gezeigt (`order: 5`). Hallmark-Gate 58 verbietet drei
  Textblöcke vor den Aktionen; der Name ist kein Einstiegstext, sondern eine
  Impressum-Zeile. Der Eingriff ist nicht fokussierbar und ändert die
  Tastaturreihenfolge nicht.
- **Haarlinien als Gruppen:** Das Buch trägt seine Ordnung über Linien und
  Abstände; die Abstände zwischen Kapiteln sind trotzdem mindestens doppelt
  so groß wie die innerhalb eines Kapitels. Die Linien sind Verzeichnis-
  und Tabellengrammatik, keine Dekoration.
- **Partnerlogos bleiben im Dunkelmodus auf hellem Grund:** Die Logos sind
  fremde Marken; ein dunkler Grund würde dunkle Wortmarken verschlucken.
- **Adresse im Fuß statt im Rücken:** Mit der DOM-Reihenfolge (better-layout)
  entfällt die obere Serviceleiste; Kontakt und Öffnungszeiten stehen
  vollständig im Kolophon.
- **Untermenüs über den Pfeil:** Sie klappen im Rücken auf, statt als Karte
  zu schweben; das hält die Spalte ohne Überlauf und ohne Hover-Zwang.

## Nicht vom Theme lösbar

- `Schüler`-Link mit leerem `href` im gemeinsamen Menü (Template).
- Leerzeichen vor dem Punkt in `/schularten/` (Inhalt).
- Der Zeitungsscan im Artikel ist auf 330 px nicht lesbar; der
  „Vergrößern“-Link öffnet die volle Auflösung (Inhalt).
- Drei Schulleben-Fotos ohne Bildunterschrift/Link (Inhalt).
- `aria-labelledby` der Untermenüknöpfe nennt den gesamten Tafeltext
  (gemeinsames `header.html`, würde alle vier Varianten ändern).
- Zwei Download-Taxonomien (Rücken-Untermenü und Register) aus dem
  gemeinsamen Menü/der Seite; das Theme markiert nur den Sprung.

## Verifikation

| Prüfung | Ergebnis |
| --- | --- |
| `qa/themes.py` | 5 Varianten × 5 Seiten × 5 Breiten = 125, **0 Befunde** |
| `qa/layout.py --design lesebuch` | **0** |
| `qa/layout.py` (Einstieg Funktional) | **0** |
| `qa/reflow.py --design lesebuch` | 902 Kombinationen, **0** |
| `qa/reflow.py` | 902 Kombinationen, **0** |
| Unterpfad `qa/../…` (Theme 5) | Linkcheck 0, Reflow 902/0, Layout 0 |
| `qa/design.py` | fünf Optionen, Speicherung, `?design=…`: **OK** |
| `qa/theme5-guard.py` | 692 Dateien, vier Designs additiv: **OK** |
| `qa/themebilder.py` | 72 Aufnahmen der vier Bestands-Themes **pixelgleich** |
| `qa/linkcheck.py` | 5.767 Ziele, **0** |
| Impeccable `detect` | 7 Seiten × 2 Breiten, **0 Befunde** |
| Hallmark `sloplint` | **0 FAIL**, 2 begründete Waivers, 1 Note |
| Tastatur | Skip → Logo → Modus → CTA → Schnellzugriffe → Stil → Verzeichnis; Fokusring überall sichtbar |
| Dunkelmodus | CTA 12,67:1, Fließtext 15:1, Links 10:1 |

**Ergebnis:** Keine offenen HIGH-Befunde. Die verbleibenden Punkte sind
Inhalts- oder Template-Eigentümerschaft (nicht Theme 5) oder bewusste
Entscheidungen oben.
