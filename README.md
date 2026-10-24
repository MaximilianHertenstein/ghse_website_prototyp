# GHSE Emmendingen – Redesign-Prototyp (Hugo + Pages CMS)

**Live:** [https://maximilianhertenstein.github.io/ghse_website_prototyp/](https://maximilianhertenstein.github.io/ghse_website_prototyp/)
[![Qualitäts-Metriken](https://github.com/MaximilianHertenstein/ghse_website_prototyp/actions/workflows/metriken.yml/badge.svg)](https://github.com/MaximilianHertenstein/ghse_website_prototyp/actions/workflows/metriken.yml)
– aktuelle Messwerte (Lighthouse, Yellow Lab Tools, Observatory) in
[METRIKEN.md](METRIKEN.md)

Klickbarer Prototyp für einen Relaunch von [www.ghse.de](https://www.ghse.de/).
Reduzierter Neobrutalismus (Grundlage: Skill `neobrutalism` aus
[bergside/awesome-design-skills](https://github.com/bergside/awesome-design-skills)),
mit echten GHSE-Inhalten, Texten, Bildern und Dokumenten.

---

## 1. Starten

Voraussetzung: Hugo **v0.146 oder neuer** (getestet mit `v0.166.0+extended`).

```bash
hugo server -D        # Entwicklung: http://localhost:1313
hugo                   # Produktionsbau nach public/
hugo server            # public/ lokal ansehen: hugo server -s public ...
python3 tools/preview-server.py   # public/ so ausliefern wie GitHub Pages
                                   # (Keep-Alive + gzip, Port 1314)
```

Es gibt keine npm-/PostCSS-Toolchain: CSS, JS und Schrift liegen fertig unter
`static/` (ein Stylesheet, ein kleines Skript für Mobilmenü und Farbmodus,
Inter als selbst gehostete Variable-Font, 48 kB).

---

## 2. Seitenumfang (bewusst begrenzt)

| Bereich | Umsetzung | URL |
|---|---|---|
| A Landingpage | Hero (eine Schaltfläche), Faktenband, 4 Schularten, Aktuelles (5 Meldungen), Termine (9 Kalender), Berufs-/Studieninformation, Instagram (4 Beiträge + 8 Accounts), Über die GHSE (4 Servicekarten), Schulleben, Partner (logobreit) | `/` |
| B Schularten-Übersicht | 8 Schularten, gruppiert nach Vollzeit/Teilzeit | `/schularten/` |
| C Detailseite Bildungsgang | Alle 8 Schularten vollständig: Einleitung, Voraussetzungen, Abschlussmöglichkeiten, weiterführende Informationen, Bilder, Downloads | `/schularten/<bildungsgang>/` |
| D Newsbereich | Liste mit 10 echten Meldungen + Detailseiten (Zeitungsscan zoombar) | `/news/` |
| E Downloadbereich | 49 Dokumente (44 PDFs, 4 ZIPs, 1 DOC) in 7 Kategorien, je mit Titel, Beschreibung, Format, Größe | `/downloads/` |
| F Service- und Schülerseiten | 15 eigene Seiten: Anfahrt, Anmeldeformulare, AV-Dual Begleitung, besser@GHSE, Beratungssystem, Fachgruppen, Krankmeldung, Nextcloud, Projekte und Software, Schulsanitätsdienst, Schulbienen, SMV, Studienfahrten, UNESCO-Aktivitäten, Vertretungsplan | `/anfahrt/`, `/smv/`, `/studienfahrten/` … |

Die übrigen 7 Schularten sind als **vollständige Detailseiten** umgesetzt:
Fließtext, Faktenkasten, Bilder und – wo vorhanden – Downloads. Damit gibt
es keine toten Karten und keinen Umweg über die Originalseite.

**Unterseiten:** Die Berufsschule führt ihre fünf Fachbereiche – Bautechnik,
Elektrotechnik, Holztechnik, Kraftfahrzeugtechnik, Metalltechnik – als
eigene Seiten unter `/schularten/berufsschule/<bereich>/`. Sie gehören zur
Berufsschule und tragen deshalb `karte: "nein"`: eigene Detailseite, aber
keine eigene Karte auf der Schularten-Übersicht, die zeigt weiter genau die
acht Bildungsgänge. Erreichbar sind sie über die fünf Überschriften unter
„Die fünf Bereiche" auf der Berufsschule-Seite.

**Bildinhalte als Text:** Mehrere Originalseiten liefern ihren Inhalt als
Bild statt als Text – die SMV-Folie, der Flyer des Schulsanitätsdienstes,
die Tabelle des Beratungssystems und die „Stimmen Ehemaliger" des TG. Alle
vier stehen auf den neuen Seiten als Bild **und** als mitlesbarer Text
drunter (Namen, Räume, Termine, Zitate unverändert übernommen); wer das
Bild nicht lesen kann oder will, verliert keine Information.

**Bewusst kein Autolinking:** Adressen im Fließtext („www.safethechildren.de",
„livec.com") bleiben Text, wie auf der Originalseite – mehrere davon zeigen
längst ins Leere. `markup.goldmark.extensions.linkify` ist deshalb ab-
geschaltet; Links entstehen nur noch aus ausgeschriebenen Markdown-Zielen,
und genau die prüft `qa/extlinkcheck.py`.

**Nicht Teil des Prototyps:** vollständige URL-/Content-Migration, kompletter
Serviceersatz, Buchungssystem, produktives Consent-Management, Hosting-
und Deployment-Konfiguration. Die Architektur (Hugo-Layouts, Sections,
`.pages.yml`) lässt sich später ohne Umbau erweitern.

---

## 3. Quellen der Originalinhalte

Inhalte wurden von den unten stehenden Seiten der Originalseite übernommen
(Texte unverändert bzw. für Karten/Teaser gekürzt), Bilder und PDFs in den
Projektordner geladen und einzeln geprüft.

| Demo-Inhalt | Quelle |
|---|---|
| Hero, Fakten, Karten-Titel | `https://www.ghse.de/`, `https://www.ghse.de/die-ghse/` |
| Aktuelles (5 Meldungen inkl. Abbildungen) | `https://www.ghse.de/` (Abschnitt „Aktuelles") bzw. `https://www.ghse.de/presse/<schlagzeile>/` |
| Termine (Einleitung, 9 Kalender-Links) | `https://www.ghse.de/` (Abschnitt „Termine") → öffentliche Nextcloud-Kalender der GHSE |
| Berufs- und Studieninformation | `https://www.ghse.de/` (Abschnitt „Berufs- und Studieninformation") → Einzelbeiträge der Originalseite |
| Instagram (Einleitung, 8 Accounts, 4 Beiträge) | `https://www.ghse.de/` (Abschnitt „Die GHSE bei Instagram") → `instagram.com/ghse_emmendingen` |
| Schüler/innen – Schulleben – Lehrer/innen | `https://www.ghse.de/schueler-schulleben-lehrer/` |
| Partner-Logostreifen | `https://www.ghse.de/` (Abschnitt „Partner") |
| Schularten-Übersicht + Detailseiten | `https://www.ghse.de/schularten/…` (Teilzeit-/Vollzeitschularten) |
| Detailseite TG | `https://www.ghse.de/schularten/vollzeitschularten/technisches-gymnasium/` |
| News (10 Meldungen inkl. Abbildungen) | `https://www.ghse.de/presse/` bzw. `https://www.ghse.de/presse/<schlagzeile>/` |
| Downloads (Titel, Kategorien, Dateien) | `https://www.ghse.de/downloads/…`, WP-Download-Manager-Pakete |
| Kontakt, Öffnungszeiten, Service-Links | Impressum-/Footer-Angaben der Originalseite |
| Service- und Schülerseiten (15) | `https://www.ghse.de/anfahrt/`, `/schulbienen/`, `/schulsanitaetsdienst/`, `/schueler/smv/`, `/schueler/beratung/`, `/schueler/av-dual-begleitung/`, `/schueler/vertretungsplan/`, `/schueler/besserghse-de/`, `/schueler/online-abmelden/`, `/nextcloud/`, `/unsere-schule/organisatorisches/fachgruppen/`, `/downloads/studienfahrten/`, `/downloads/projekte-software/`, `/downloads/anmeldeformulare/`, `/unesco/unesco-aktivitaeten/` |

**Nachrichtentext:** Die Pressebeiträge der GHSE bestehen auf der Originalseite
aus Überschrift, Quelle + Datum, Teaser, Abbildung(en) (Zeitungsausschnitte)
und externem Quellenlink – ohne Fließtext. Die Detailseite zeigt genau diese
Felder; es wurde bewusst kein Text erfunden. Die Vollständigkeit wurde gegen
die Presse-Sitemap von ghse.de geprüft (160 Beiträge): alle zehn Beiträge mit
Pressedatum vom 30.06.2026 bis 07.10.2026 sind übernommen, vier davon wurden
dabei nachträglich ergänzt. Meldungen ohne Teaser („Besuch aus China",
drei Abbildungen) und ohne Abbildung („Von Pädagogik bis Physik prämiert")
sind in Templates und CMS-Feldern abgedeckt. Startseite und Newsliste zeigen
dieselben Beiträge; die Startseite listet wie im Original die fünf neuesten.

**Instagram:** Die GHSE betreibt auf ihrer Startseite einen Feed mit acht
Accounts und vier aktuellen Beiträgen. Der Originalseite lädt diese Beiträge
per JavaScript nach; im Prototyp liegen die vier Bilder statisch unter
`static/bilder/insta-*.webp` (aus den öffentlichen Embed-Seiten der Beiträge
gelesen) und werden mit der Kurzfassung der Bildunterschrift verlinkt –
ohne Einbettung, ohne Drittanbieter-Skript. Für eine spätere Laufzeit muss
dieser Block einmalig aktualisiert werden; die acht Account-Links bleiben
jederzeit aktuell.

**Kleinere Textkorrekturen** (dokumentiert, weil das Original fehlerhaft ist):
„Badischen Zeitung" → „Badische Zeitung" (Quellenlabel), „Die Einjährige
Berufsfachschulen sind…" → „Die Einjährigen Berufsfachschulen sind…".

**Bildnachweise:** Logo, Gebäudeaufnahme, Schulartbilder und Presseabbildungen
stammen von `www.ghse.de` (Theme „ziegenhagel", Uploads). Für den internen
Prototyp referenziert; eine Veröffentlichung braucht die Freigabe der Schule.

**Partner-Logostreifen:** Der Prototyp nutzt die aktuelle Fassung von ghse.de
(1023×494 px, sieben Logos, Upload 2025). Auf der vollen Containerbreite
(1180 px) wird die Datei minimal hochskaliert – bewusst zugunsten der
inhaltlichen Aktualität; das größere Original von 2023 (2116×1014 px) zeigt
ein inzwischen entferntes „Approved Test Centre"-Logo und wird deshalb nicht
verwendet.

**Getestete Downloads** (jeweils `HTTP 200`, MIME-Typ und Magic-Bytes
geprüft, Inhalt per `pdftotext` gegen den Titel abgeglichen): zunächst die
16 Dateien der vier Startkategorien (`flyer-tg`, `flyer-sg`, `flyer-2bkik`,
`flyer-2bfp`, `wochenplan-2026-27`, `26-27-blockplan-{holz,kfz,altenpflegehilfe}`,
`oberstufeninformation`, `leitfaden-2027`, `terminuebersicht-abitur-2027`,
`bewertungstabelle-ab-abi-2021-2`, `hausordnung`, `ablaufplan-bewo`,
`bewo-bewerberleitfaden`, `einrichtung-der-ipad-leihgeraete`), danach die
vollständige Ablösung des WP-Download-Managers: heute 49 Dateien, das
vollständige Verzeichnis mit Titel, Beschreibung, Kategorie und Dateiname
steht in `content/downloads/`. Dateien liegen lokal unter
`assets/downloads/` und werden von Hugo nach `/downloads/<datei>` veröf-
fentlicht; Format und Größe ermittelt der Build bei jedem Lauf aus der
Datei selbst (keine eingetippten Werte).

**Wichtig:** Assets ohne passenden Eintrag in `content/downloads/` werden
nicht veröffentlicht – das gilt besonders für die drei Projekt-ZIPs
(ClipClick 53 MB, Papiercomputer 0,5 MB, Vokabeltrainer 1,9 MB). Sie liegen
bewusst im Repository, weil die Originalseite sie verlinkt und die Links
nach dem Cutover sonst ins Leere liefen; ihre Kategorie heißt „Projekte &amp;
Software".

---

## 4. Pages CMS einrichten

Die Konfiguration liegt in [`.pages.yml`](.pages.yml) (Feldnamen entsprechen
exakt den Front-Matter-Schlüsseln der Templates; keine Felder, die im Frontend
nicht verwendet werden).

1. Repository (dieser Ordner) auf GitHub/GitLab ablegen.
2. <https://pagescms.org> öffnen → Installation/„Quick start" → Provider und
   Repo wählen, `pages.yml` bzw. `.pages.yml` als Config-Datei angeben.
3. Media-Quellen prüfen – sie sind bereits gesetzt:
   * **Bilder:** `static/bilder` → geschrieben als `/bilder/…`
   * **Dokumente:** `assets/downloads` → geschrieben als `/downloads/…`
4. Collections (33 Stück unter `content`): **Startseite** (Einzeldatei),
   **Schularten (Inhaltsseiten)**, **News** und **Downloads** als
   Ordner-Sammlungen, dazu jede weitere Seite einzeln – einschließlich der
   achtzehn Einzelseiten im Wurzelverzeichnis von `content/` (Impressum,
   Datenschutz, Safer Space und die fünfzehn Service- und Schülerseiten,
   die mit der Ablösung der Originalseite dazukamen). Jede Sammlung bietet
   `title`, `description` und `body`; Studienfahrten und Projekte und
   Software zusätzlich das `bilder`-Raster für ihre Fotoläufe. Prüfbar mit
   jedem YAML-Parser: fehlt einer `content/*.md`-Datei eine Sammlung, kann
   die Redaktion sie nicht bearbeiten.

### Redaktionsszenarien

**Neue Nachricht anlegen**
1. Collection *News* → „Add item" (Neu).
2. Felder: `title` (Überschrift), `date` (z. B. `2026-10-16`), `quelle`
   (Medium), `teaser` (1–2 Sätze), `bild` + `bildAlt` (Upload nach
   `static/bilder`), bei weiteren Abbildungen `bild2`/`bild2Alt` und
   `bild3`/`bild3Alt`, bei Bedarf `body`. `teaser` und `bild` sind
   optional – fehlen sie, rendert die Meldung ohne Lead beziehungsweise
   ohne Abbildung (wie bei „Von Pädagogik bis Physik prämiert"). Ein
   Quellenlink (`quelle_url`) gibt es bewusst nicht mehr: die Quelle
   erscheint als Klartext unter dem Beitrag, die Meldung steht
   vollständig auf dieser Website.
3. Optional: eine vergrößerte Variante `<name>-gross.<endung>` neben das Bild
   legen – die Meldungsseite nutzt sie automatisch für `srcset` und den
   Zoom-Link (sonst wird die eingebettete Datei verlinkt).
4. Speichern → Hugo baut neu → die Meldung erscheint automatisch als erste
   Karte auf der Startseite und in der News-Übersicht (Sortierung nach Datum).

**PDF ersetzen bzw. ergänzen**
1. Collection *Downloads* → Eintrag öffnen → Feld **Datei (PDF)** ersetzen
   (gleicher Dateiname überschreibt die Datei in `assets/downloads/`).
2. Titel/Beschreibung bei Bedarf anpassen; die Kategorie bestimmt die
   Gruppierung, `weight` die Reihenfolge innerhalb der Kategorie.
3. Format und Dateigröße erscheinen automatisch – sie werden beim Build aus
   der Datei gelesen, ein Nachtragen ist nicht nötig.
4. Für eine **neue** Kategorie: Wert in `.pages.yml` unter
   `downloads → kategorie → values` ergänzen; die Gruppierung auf
   `/downloads/` sortiert sich selbst (alphabetisch über die Verteilung).

**Service- oder Schülerseite bearbeiten**
1. Die passende Sammlung öffnen (z. B. *SMV (Schüler)*,
   *Studienfahrten (Schüler und Downloads)*, *Impressum (Rechtliches)*).
2. `title` und `description` ergeben Überschrift und Lead der Seite,
   `body` ist der Fließtext. Die Bausteine `{{< bild >}}` und
   `{{< bilder >}}` bleiben darin stehen, wo sie stehen: der erste holt
   sein Bild aus `static/bilder`, der zweite aus dem `bilder`-Raster
   gleich im Front Matter.
3. Beim Raster jedes Element mit Bild und Bildunterschrift füllen. Wie
   viele Einträge ein Lauf hat, ist nirgends festgeschrieben – das Raster
   rechnet seine Spalten aus der Anzahl.

---

## 5. Technischer Aufbau

```
.github/workflows/  deploy.yml (Pages-Pipeline: Hugo-Bau + Veröffentlichung)
content/            _index.md (Landingpage), schularten/, news/, downloads/
                    und 18 Einzelseiten im Wurzelverzeichnis (Service,
                    Schüler, Rechtliches, Mint, UNESCO)
layouts/            baseof.html, home.html, 404.html
  _partials/        header, footer, karte-schulart, karte-news, zeile-download
  news/             section.html, page.html
  schularten/       section.html, page.html
  downloads/        section.html
assets/downloads/   Original-PDFs (Hugo veröffentlicht sie als /downloads/*.pdf)
static/             css/main.css, js/nav.js, fonts/, bilder/, favicon.svg
tools/              preview-server.py (Mess-Server: Keep-Alive + gzip wie GitHub Pages)
public/             gebaute Website (nicht eingecheckt, siehe .gitignore)
recherche/          Roh-Extrakte der Originalseite (Arbeitsstand, nicht eingecheckt)
```

* **Komponenten:** Kopf-/Fußleiste, Karten (Schulart, News) und Download-Zeile
  existieren je einmal und werden von Startseite, Übersichten und Detailseiten
  wiederverwendet.
* **Pfade:** Interne Links, Bildpfade und Datei-Downloads laufen durch
  `relURL`/`relPermalink` – die Ausgabe funktioniert unter `/` und unter
  `/<repo>/` ohne Änderung an den Vorlagen.
* **Front Matter ↔ CMS:** `title`, `description`, `kategorie`, `kurz`,
  `abschluss`, `bild`, `bildAlt`, `bilder`, `bild2`, `bild2Alt`, `bild3`,
  `bild3Alt`, `date`, `quelle`, `quelle_url`,
  `teaser`, `beschreibung`, `datei`, `weight` – überall verwendet.
  Nur `downloads` (verwandte Dokumente der TG-Seite) ist reines Hugo-Feld.
* **Strukturierung:** Inhalte sind getrennte Markdown-Dateien mit Schlüssel-
  werten; Kategorien und Gruppen entstehen aus den Daten, nicht aus der Vorlage.

### Farbmodus (Hell/Dunkel)

Hugo selbst kann keinen Dark Mode – ein statischer Generator kennt keine
Nutzereinstellung. Umgesetzt ist deshalb der Standardweg für statische
Websites: CSS `prefers-color-scheme` plus ein Umschalten per JavaScript.

* Semantische Tokens in `:root` (`--schrift`, `--flaeche`, `--papier`,
  `--rand`, `--link`, `--schatten-farbe`, `--streifen` …). Die Komponenten
  referenzieren nur diese Tokens; der dunkle Satz ersetzt Werte, nicht Regeln.
* Der dunkle Satz steht zweimal: in `@media (prefers-color-scheme: dark)`
  (ohne gespeicherte Wahl, `:root:not([data-theme="light"])`) und unter
  `:root[data-theme="dark"]` für die gespeicherte Wahl. Bewusste
  Vereinfachung ohne Präprozessor.
* Schalter im Kopf (`.modusknopf`, Sonne/Mond, `aria-pressed`); die Wahl
  liegt in `localStorage` (`ghse-theme`), ein Inline-Skript in `baseof.html`
  setzt sie vor dem Rendern (kein Aufblitzen). Ohne gespeicherte Wahl folgt
  die Seite dem System (`prefers-color-scheme`).
* Gelbe Flächen behalten in beiden Modi dunkle Schrift (`--tinte`), das Logo
  wird im Dunkeln weiß ausgegeben, Marker hinter `<strong>` abgeschwächt.
* `@media print` setzt alle Tokens auf Hell zurück – ausgedruckt wird nie
  die dunkle Variante.

---

## 6. Qualitätssicherung

* Semantische Struktur: `header/nav/main/footer`, genau eine `h1` je Seite,
  Überschriften-Hierarchie, `figure/figcaption`, `time`, `address`.
* WCAG 2.2 AA im Blick: Sprungmarke „Direkt zum Inhalt", sichtbare
  Fokusringe (`:focus-visible`, orange), `aria-expanded`/`aria-controls` am
  Mobilmenü, `aria-current="page"` in der Navigation, Alt-Texte für alle
  Bilder (Bilder einzeln betrachtet und beschrieben), Farben auf Kontrast
  geprüft – `qa/kontrast.py` rechnet alle Tokenpaare in Hell **und** Dunkel
  durch (37 Paare, kleinster Textwert 4,87:1 für den Kicker auf Papier,
  alle Paare bestehen),
  Touch-Ziele ≥ 44 px, `prefers-reduced-motion` respektiert.
* Responsive: Breakpoints 1000/900/640 px – Karten- und Zeilenraster stapeln
  sich, Navigation wird zum Aufklappmenü, Download-Zeilen werden zu
  Vollbreiten-Karten mit großem Button. Nachgemessen wird das mit
  `qa/layout.py` (Ankersprung unter Kopf **und** Sprungleiste, Kopfhöhe,
  Touch-Ziele an 1440/640/390 px) und `qa/reflow.py` (55 Seiten × 11 Breiten
  = 605 Kombinationen, 0 Probleme – nichts bricht horizontales Scrollen
  aus).
* Links: alle internen Ziele geprüft (`qa/linkcheck.py`) – 55 HTML-Seiten
  sowie alle eingebundenen Bilder, Schriften und Dokumente (3419 Ziele
  gesamt, keine Fehlschläge, einschließlich der Sprungziele der Download-
  Kategorien). Die 59 externen Links prüft `qa/extlinkcheck.py` einzeln:
  keiner ist nachweisbar tot – darunter die 9 öffentlichen Nextcloud-
  Terminkalender, 12 Instagram-Links (8 Accounts, 4 Beiträge), BewO,
  Moodle, OSM, WebUntis, die alte Nextcloud-Speicherfreigabe,
  Impressum/Datenschutz und die Berufsinformations-Beiträge. Zwei Domains
  (`bauen-hat-zukunft.de`, `berufe-lexikon.de`) sperren die Messumgebung
  und werden deshalb als „lebend, aber gesperrt" geführt; ein dritter Link,
  `softatomos.com/kane/` (Projektseite von VplanTouch), zeigt ins Leere und
  steht deshalb als Klartext im Text, nicht als Link.
* Lighthouse: Performance mobil **98–100** (Startseite 99, News-Übersicht 99,
  Meldungsseiten 98–100, Download- und Schulartseiten 99–100), Desktop
  **100** (LCP 0,4–0,5 s); nach dem Dark-Mode-Einbau stichprobenartig
  neu gemessen: Startseite mobil 98 / Desktop 100, Download-Seite mobil 100,
  Meldungsseite mobil 99 – Accessibility und SEO jeweils 100. Best Practices
  überall 100 außer der Seite „Besuch aus China" (96): Der dortige
  Zeitungsausschnitt ist auf ghse.de nur 360 px breit, das Audit
  `image-size-responsive` moniert genau diese Auflösung – hochskalieren
  würde nur weichzeichnen, daher bleibt es bei der ehrlichen Quelldatei.
  Die beiden Hochformat-Scans stagnieren bei 98, weil ihr scharfes
  Zoom-Bild (171/188 KB) automatisch mitgeladen wird – scharf ist hier der
  bessere Deal. Gemessen wurde gegen `tools/preview-server.py`, der wie
  GitHub Pages mit Keep-Alive und gzip antwortet – das mitgelieferte
  `python3 -m http.server` verkettet Anfragen nicht und bläht damit jedes
  Ergebnis künstlich auf.
* Lighthouse nach dem Migrationsstand (15 neue Seiten, 49 Dokumente, keine
  Links mehr auf die Originalseite): mobil Startseite 98, Download-Seite 99,
  UNESCO-Aktivitäten 99 (38 KB HTML), Projekte und Software 99,
  Studienfahrten 99 – Accessibility, Best Practices und SEO jeweils 100,
  TBT überall 0 ms.
* News-Lesbarkeit: Der Zeitungsscan bricht auf Detailseiten breiter als die
  Textspalte aus (bis 1048 px), wird aber nie über die Quellauflösung hinaus
  vergrößert – `srcset` liefert je Display die passende Datei, die
  Originalauflösung liegt als `<name>-gross.webp` vor und liegt hinter der
  „Vergrößern"-Plakette zum Zoomen in einem neuen Tab. Die Plakette hängt
  unter der Bildkante und verdeckt beim Lesen keine Textzeile;
  Bilderunterschriften sind auf 700 px Zeilenlänge begrenzt, Fließtexte
  trennen silbentrennend (`hyphens: auto`). Dazu Druck-Styles für Artikel
  und Downloads sowie durchgehende Hover-/Fokus-Zustände für Karten.
* Performance-Optimierungen: alle Inhaltsbilder als WebP (die 18 Bilder der
  Startseite von 1738 KB auf 998 KB, davon lädt Lighthouse im mobilen Lauf
  447 KiB, der Rest lädt lazy unterhalb des Bildschirms), passend zur
  Anzeigegröße skaliert (Mobil: 384 CSS-px × 1,75 DPR), Hero auf 4:3
  beschnitten, weil die CSS-Box (`aspect-ratio: 4/3`, `object-fit: cover`)
  die Seiten ohnehin abschneidet, Hero-Preload im `<head>`, `imageConfig`
  liefert für jedes Bild echte `width/height`-Maße (verhindert
  Layoutverschiebungen).
  Bewusst nicht optimiert: der Hero ließe sich mit ~20 KB auf 100 bringen,
  wäre dann aber auf hochauflösenden Displays sichtbar weicher – 99 mit
  scharfem Bild ist hier der bessere Deal.
* Automatische Messwerte: Der Workflow
  [.github/workflows/metriken.yml](.github/workflows/metriken.yml) misst
  wöchentlich montags (zusätzlich manuell unter „Actions" →
  „Qualitäts-Metriken" → „Run workflow") gegen die Live-Seite und schreibt
  die Ergebnisse nach [METRIKEN.md](METRIKEN.md) zurück:
  **GL** – Google Lighthouse, Durchschnitt der vier Kategorien aus einem
  mobilen Lauf;
  **YL** – Yellow Lab Tools Gesamtscore über dessen Public API
  (Anti-Flood: max. 12 Läufe je 24 Stunden, der wöchentliche Rhythmus
  bleibt weit darunter);
  **MO** – MDN/Mozilla Observatory, gelaufen als CLI
  (`@mdn/mdn-http-observatory`), denn dessen API-Variante kennt keine
  Unterpfade und scheitert am Host `maximilianhertenstein.github.io`
  sonst mit 404 an der Seitenwurzel.
  Die Lighthouse- und Observatory-JSONs landen als Artefakt im jeweiligen
  Workflow-Lauf. Fällt ein Dienst aus (Quota, Warteschlange, Umbau), wird
  die betroffene Metrik als „n/a" mit Grund eingetragen, statt den Lauf
  abzubrechen. Die Observatory-Note fällt dauerhaft mittelmäßig aus, weil
  die Sicherheits-Header von GitHub Pages zentral gesetzt werden – im
  Repository lässt sich daran nichts drehen.

---

## 7. Veröffentlichung auf GitHub Pages

Die Website ist auf einen Unterverzeichnis-Aufruf ausgelegt
(`https://<benutzer>.github.io/<repo>/`): alle internen Links, Bildpfade und
Datei-Downloads werden mit `relURL` bzw. `relPermalink` erzeugt und tragen
damit automatisch den richtigen Basispfad – lokal unter `/` genauso wie im
Unterverzeichnis.

Der Workflow [.github/workflows/deploy.yml](.github/workflows/deploy.yml)
baut bei jedem Push nach `main` mit Hugo **0.166.0 (extended)** und stellt
`public/` über die offiziellen Pages-Actions bereit. Er berechnet die
Zieladresse selbst: Repos, die auf `<benutzer>.github.io` enden, landen unter
der Domain-Wurzel, alle anderen unter `/<repo>/`.

Der Workflow [.github/workflows/metriken.yml](.github/workflows/metriken.yml)
misst zusätzlich wöchentlich gegen die Live-Seite und aktualisiert
[METRIKEN.md](METRIKEN.md) (Abschnitt 6); sein Commit trägt `[skip ci]`,
damit kein neuer Deploy entsteht.

### Einmalig einrichten

1. Repository anlegen (Name frei wählbar, z. B. `ghse-prototyp`).
2. Projekt committen und schieben:

   ```bash
   git init -b main
   git add .
   git commit -m "GHSE-Redesign-Prototyp"
   git remote add origin git@github.com:<benutzer>/<repo>.git
   git push -u origin main
   ```

3. Im Repository: **Settings → Pages → Build and deployment → Source:
   „GitHub Actions"** auswählen.
4. Nach dem ersten Lauf unter
   `https://<benutzer>.github.io/<repo>/` erreichbar.

**Hinweis:** `public/` liegt in der `.gitignore` – die Ausgabe entsteht immer
frisch in der Pipeline. Einen lokalen Produktionscheck gibt es weiterhin mit
`hugo && python3 -m http.server -d public 1314`.

**Spätere Inhaltsänderungen** laufen ohne Git über das mit eingebundene
[Pages CMS](https://pagescms.org): Es schreibt direkt ins Repository, der
Push startet die Pipeline automatisch neu.

---

## 8. Offene Punkte

1. **Presse-Meldungen ohne Volltext:** Solange ghse.de nur Teaser + Abbildung
   + Quellenlink liefert, bleibt die Detailseite bei diesen Feldern. Sobald
   Volltexte gepflegt werden, ist das `body`-Feld im CMS bereits angebunden.
2. **Bildfreigabe:** Bilder/PDFs sind für den internen Prototyp eingebunden;
   vor einer Veröffentlichung braucht die GHSE die Freigabe (Urheberrecht
   regionaler Zeitungen bei den Presseabbildungen!).
3. **Kein Verweis mehr auf die Originalseite:** Alle 23 Menüziele sind auf
   eigene Seiten, Anker oder die echten Dienste (WebUntis, Moodle, Shop,
   OSM, alter Nextcloud-Speicher) umgebucht; `grep -rho … ghse\.de` über
   `public/` liefert ausgeliefert nur noch `https://ghse.de/iserv/` – der
   IServ-Dienstpfad als Dienstadresse. Auch die Hinweisblöcke „Prototyp",
   der „Originalseite"-Link im Fuß, der Prototyp-Hinweis unter dem
   Copyright und die Quellen-URLs der zehn Pressemeldungen sind entfernt
   (die Quellenangabe selbst bleibt als Klartext im Bildtext stehen). Der
   Kultusportal-Deep-Link der Originalseite (404, Portal umgezogen) zeigt
   weiterhin auf die geprüfte Startseite des Kultusministeriums.
4. **Kein echtes Consent-/Analytics-Setup:** Das Original betreibt ein
   Cookie-Consent-Modul; im Prototyp bewusst entfallen (außerhalb des Umfangs).
5. **Instagram-Feed ist ein Standbild:** Der Abschnitt zeigt vier konkrete
   Beiträge mit lokalen Bildern statt eines Live-Feeds. Bei Laufzeit müsste
   er regelmäßig aktualisiert werden (oder das Original per JS/Server nachladen).
6. **Ponytail-Hinweis:** Es wurde absichtlich nur das gebaut, was die
   Demo braucht – kein Taxonomie-/Blog-System, kein Pagination-Layout, keine
   Social-Media-Einbettung, kein SVG-Sprite-Katalog.
