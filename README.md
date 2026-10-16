# GHSE Emmendingen – Redesign-Prototyp (Hugo + Pages CMS)

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
`static/` (ein Stylesheet, ein kleines Skript für das Mobilmenü, Inter als
selbst gehostete Variable-Font, 48 kB).

---

## 2. Seitenumfang (bewusst begrenzt)

| Bereich | Umsetzung | URL |
|---|---|---|
| A Landingpage | Hero, Faktenband, 3 Schularten, Aktuelles (5 Meldungen), Termine (9 Kalender), Berufs-/Studieninformation, Instagram (4 Beiträge + 8 Accounts), Download-CTA, Über die GHSE (6 Servicekarten), Schulleben, Partner | `/` |
| B Schularten-Übersicht | 8 Schularten, gruppiert nach Vollzeit/Teilzeit | `/schularten/` |
| C Detailseite Bildungsgang | Technisches Gymnasium (vollständig: Einleitung, Voraussetzungen, Abschlussmöglichkeiten, weiterführende Informationen, Downloads) | `/schularten/technisches-gymnasium/` |
| D Newsbereich | Liste mit 6 echten Meldungen + Detailseiten | `/news/` |
| E Downloadbereich | 16 PDFs in 4 Kategorien, je mit Titel, Beschreibung, Format, Größe | `/downloads/` |

Die übrigen 7 Schularten sind als **Kurzprofil** umgesetzt: Kurztext, Bild,
Faktenkasten und ein klar gekennzeichneter Hinweis, dass die vollständige
Detailseite Teil des späteren Umbaus ist – mit Link auf die Originalseite.
So gibt es keine toten Karten, aber auch keine vorgaukelte Vollständigkeit.

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
| Schularten-Übersicht + Kurzprofile | `https://www.ghse.de/schularten/…` (Teilzeit-/Vollzeitschularten) |
| Detailseite TG | `https://www.ghse.de/schularten/vollzeitschularten/technisches-gymnasium/` |
| News (6 Meldungen inkl. Abbildungen) | `https://www.ghse.de/presse/` bzw. `https://www.ghse.de/presse/<schlagzeile>/` |
| Downloads (Titel, Kategorien, Dateien) | `https://www.ghse.de/downloads/…`, WP-Download-Manager-Pakete |
| Kontakt, Öffnungszeiten, Service-Links | Impressum-/Footer-Angaben der Originalseite |

**Nachrichtentext:** Die Pressebeiträge der GHSE bestehen auf der Originalseite
aus Überschrift, Quelle + Datum, Teaser, Abbildung (Zeitungsausschnitt) und
externem Quellenlink. Die Detailseite zeigt genau diese Felder – es wurde
bewusst kein Text erfunden. Startseite und Newsliste zeigen dieselben
Beiträge; die Startseite listet wie im Original die fünf neuesten.

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

**Getestete Downloads** (alle `HTTP 200`, `application/pdf`, Magic-Bytes
`%PDF-` geprüft, Inhalt per `pdftotext` gegen den Titel abgeglichen):
`flyer-tg`, `flyer-sg`, `flyer-2bkik`, `flyer-2bfp`, `wochenplan-2026-27`,
`26-27-blockplan-{holz,kfz,altenpflegehilfe}`, `oberstufeninformation`,
`leitfaden-2027`, `terminuebersicht-abitur-2027`,
`bewertungstabelle-ab-abi-2021-2`, `hausordnung`, `ablaufplan-bewo`,
`bewo-bewerberleitfaden`, `einrichtung-der-ipad-leihgeraete`.
Dateien liegen lokal unter `assets/downloads/`, werden von Hugo nach
`/downloads/<datei>.pdf` veröffentlicht; Format und Größe werden bei jedem
Build aus der Datei selbst ermittelt (keine eingetippten Werte).

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
4. Collections: **Startseite** (Einzeldatei), **Schularten (Inhaltsseiten)**,
   **News**, **Downloads**.

### Redaktionsszenarien

**Neue Nachricht anlegen**
1. Collection *News* → „Add item" (Neu).
2. Felder: `title` (Überschrift), `date` (z. B. `2026-10-16`), `quelle`
   (Medium), `quelle_url` (Link zum Originalartikel), `teaser` (1–2 Sätze),
   `bild` + `bildAlt` (Upload nach `static/bilder`), bei Bedarf `body`.
3. Speichern → Hugo baut neu → die Meldung erscheint automatisch als erste
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

---

## 5. Technischer Aufbau

```
.github/workflows/  deploy.yml (Pages-Pipeline: Hugo-Bau + Veröffentlichung)
content/            _index.md (Landingpage), schularten/, news/, downloads/
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
  `abschluss`, `bild`, `bildAlt`, `extern`, `date`, `quelle`, `quelle_url`,
  `teaser`, `beschreibung`, `datei`, `weight` – überall verwendet.
  Nur `downloads` (verwandte Dokumente der TG-Seite) ist reines Hugo-Feld.
* **Strukturierung:** Inhalte sind getrennte Markdown-Dateien mit Schlüssel-
  werten; Kategorien und Gruppen entstehen aus den Daten, nicht aus der Vorlage.

---

## 6. Qualitätssicherung

* Semantische Struktur: `header/nav/main/footer`, genau eine `h1` je Seite,
  Überschriften-Hierarchie, `figure/figcaption`, `time`, `address`.
* WCAG 2.2 AA im Blick: Sprungmarke „Direkt zum Inhalt", sichtbare
  Fokusringe (`:focus-visible`, orange), `aria-expanded`/`aria-controls` am
  Mobilmenü, `aria-current="page"` in der Navigation, Alt-Texte für alle
  Bilder (Bilder einzeln betrachtet und beschrieben), Farben auf Kontrast
  geprüft (Tinte/Papier ≈ 17:1, Weiß/Nachtblau ≈ 12:1, Tinte/Gelb ≈ 12:1),
  Touch-Ziele ≥ 44 px, `prefers-reduced-motion` respektiert.
* Responsive: Breakpoints 1000/900/640 px – Karten- und Zeilenraster stapeln
  sich, Navigation wird zum Aufklappmenü, Download-Zeilen werden zu
  Vollbreiten-Karten mit großem Button.
* Links: 62 interne Seitenziele sowie alle eingebundenen Bilder, Schriften
  und PDFs geprüft (344 Ziele gesamt, alle vorhanden), 52 externe
  Links alle `HTTP 200` – darunter die 9 öffentlichen Nextcloud-Terminkalender,
  12 Instagram-Links (8 Accounts, 4 Beiträge), BewO, Moodle, OSM,
  Impressum/Datenschutz und die Berufsinformations-Beiträge.
* Lighthouse: Performance mobil **99** (LCP 2,0 s, CLS 0, TBT 30 ms),
  Desktop **100** (LCP 0,4 s); Accessibility, Best Practices und SEO
  überall 100. Gemessen wurde gegen `tools/preview-server.py`, der wie
  GitHub Pages mit Keep-Alive und gzip antwortet – das mitgelieferte
  `python3 -m http.server` verkettet Anfragen nicht und bläht damit jedes
  Ergebnis künstlich auf.
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
2. **Weitere Schularten als Detailseiten:** Die 7 Kurzprofile brauchen nur
   `extern` leer setzen und den Inhalt aus dem Original übernehmen – die
   Vorlage rendert den Volltext automatisch.
3. **Bildfreigabe:** Bilder/PDFs sind für den internen Prototyp eingebunden;
   vor einer Veröffentlichung braucht die GHSE die Freigabe (Urheberrecht
   regionaler Zeitungen bei den Presseabbildungen!).
4. **Verlinkung ins Original:** Service-, Rechts- und Detaillinks zeigen
   weiterhin auf ghse.de – ein Schritt der später durch eigene Seiten
   ersetzt wird. Der Kultusportal-Deep-Link der Originalseite (404, Portal
   umgezogen) wurde durch die geprüfte Startseite des Kultusministeriums
   ersetzt.
5. **Kein echtes Consent-/Analytics-Setup:** Das Original betreibt ein
   Cookie-Consent-Modul; im Prototyp bewusst entfallen (außerhalb des Umfangs).
6. **Instagram-Feed ist ein Standbild:** Der Abschnitt zeigt vier konkrete
   Beiträge mit lokalen Bildern statt eines Live-Feeds. Bei Laufzeit müsste
   er regelmäßig aktualisiert werden (oder das Original per JS/Server nachladen).
7. **Ponytail-Hinweis:** Es wurde absichtlich nur das gebaut, was die
   Demo braucht – kein Taxonomie-/Blog-System, kein Pagination-Layout, keine
   Social-Media-Einbettung, kein SVG-Sprite-Katalog.
