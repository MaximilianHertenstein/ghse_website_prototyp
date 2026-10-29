# GHSE Emmendingen – Redesign (Hugo + Pages CMS)

**Live:** [https://maximilianhertenstein.github.io/ghse_website_prototyp/](https://maximilianhertenstein.github.io/ghse_website_prototyp/)
[![Qualitäts-Metriken](https://github.com/MaximilianHertenstein/ghse_website_prototyp/actions/workflows/metriken.yml/badge.svg)](https://github.com/MaximilianHertenstein/ghse_website_prototyp/actions/workflows/metriken.yml)
– aktuelle Messwerte (Lighthouse, Yellow Lab Tools, Observatory) in
[METRIKEN.md](METRIKEN.md)

Neubau von [www.ghse.de](https://www.ghse.de/) mit Hugo, gedacht als
vollständige Ablöse des Originals – nicht als Demo.
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

Die Instagram-Karten auf der Startseite frischt
`python3 tools/instagram.py` auf: Es liest die neuesten Beiträge des
Schulaccounts, legt die Bilder als WebP unter `static/bilder/` ab und
aktualisiert die Liste `insta_beitraege` in `content/_index.md`. Für neue
Beiträge trägt es einen Platzhalter als `bildAlt` ein und weist darauf
zurück – die Bildbeschreibung bitte vor dem Build ergänzen (genau
hinschauen, was zu sehen ist).

---

## 2. Seitenumfang (bewusst begrenzt)

| Bereich | Umsetzung | URL |
|---|---|---|
| A Landingpage | Hero (Schulnamen-Badge, Abschluss-Chips), 4 Schularten, Instagram (4 Beiträge + 8 Accounts), Aktuelles (3 Meldungen + Link auf alle), Termine (9 Kalender), Service (4 Karten), Schulleben, Partner (logobreit); Berufs-/Studieninformation nur bei aktuellen Terminen (Momentan-Ausblendung, siehe §3) | `/` |
| B Schularten-Übersicht | 8 Schularten, gruppiert nach Vollzeit/Teilzeit | `/schularten/` |
| C Detailseite Bildungsgang | Alle 8 Schularten vollständig: Einleitung, Voraussetzungen, Abschlussmöglichkeiten, weiterführende Informationen, Bilder, Downloads | `/schularten/<bildungsgang>/` |
| D Newsbereich | Liste mit 10 echten Meldungen + Detailseiten (Zeitungsscan zoombar) | `/news/` |
| E Downloadbereich | 49 Dokumente (44 PDFs, 4 ZIPs, 1 DOC) in 7 Kategorien, je mit Titel, Beschreibung, Format, Größe | `/downloads/` |
| F Service- und Schülerseiten | 18 eigene Seiten: Anfahrt, Anmeldeformulare, AV-Dual Begleitung, besser@GHSE, Beratungssystem, Fachgruppen, Infoveranstaltung, Krankmeldung, Nextcloud, Oberstufeninformationen, Projekte und Software, Schulsanitätsdienst, Schulbienen, Schulsozialarbeit, SMV, Studienfahrten, UNESCO-Aktivitäten, Vertretungsplan | `/anfahrt/`, `/smv/`, `/studienfahrten/`, `/oberstufeninformationen/`, `/infoveranstaltung/` … |
| G Themenseiten | 2 weitere Seiten mit eigener Quelle: UNESCO („Was heißt UNESCO-Projektschule?") und Erasmus+ | `/unesco/`, `/erasmus/` |

Die übrigen 7 Schularten sind als **vollständige Detailseiten** umgesetzt:
Fließtext, Faktenkasten, Bilder und – wo vorhanden – Downloads. Damit gibt
es keine toten Karten und keinen Umweg über die Originalseite.

**Unterseiten:** Die Schularten gliedern sich wie im Original in Richtungen,
jede mit eigener Seite und eigenem Wortlaut. Die Berufsschule führt ihre fünf
Fachbereiche – Bautechnik, Elektrotechnik, Holztechnik, Kraftfahrzeugtechnik,
Metalltechnik – unter `/schularten/berufsschule/<bereich>/`. Sie gehören zur
Berufsschule und tragen deshalb `karte: "nein"`: eigene Detailseite, aber
keine eigene Karte auf der Schularten-Übersicht, die zeigt weiter genau die
acht Bildungsgänge. Erreichbar sind sie über die fünf Überschriften unter
„Die fünf Bereiche" auf der Berufsschule-Seite. Die übrigen Schularten
führen ihre Richtungen ebenso als Unterseiten:

| Schulart | Unterseiten | Pfad |
|---|---|---|
| Pflege | 5 (Generalistische Pflegeausbildung, dreijährige Berufsfachschule für Altenpflege, zweijährige und einjährige Berufsfachschule Altenpflegehilfe, berufspädagogische Zusatzqualifikation) | `/schularten/pflege/<richtung>/` |
| Sozialwissenschaftliches Gymnasium | 2 (sechs- und dreijährig) | `/schularten/sozialwissenschaftliches-gymnasium/<laufzeit>/` |
| Zweijährige Berufsfachschulen | 4 (Metalltechnik, Elektrotechnik, Hauswirtschaft und Ernährung, Gesundheit und Pflege) | `/schularten/zweijahrige-berufsfachschulen/<richtung>/` |
| Einjährige Berufsfachschulen | 3 (Metalltechnik, Holztechnik, Fahrzeugtechnik) | `/schularten/einjahrige-berufsfachschulen/<richtung>/` |
| Technisches Gymnasium | 3 (Informationstechnik, Mechatronik/Technik, Technik und Management) | `/schularten/technisches-gymnasium/<richtung>/` |
| Berufsschule | 5 (Bautechnik, Elektrotechnik, Holztechnik, Kraftfahrzeugtechnik, Metalltechnik) | `/schularten/berufsschule/<bereich>/` |
| Berufsvorbereitung | 4 (AV-Dual, BVE, VABKF, VABO) | `/schularten/berufsvorbereitende-schularten/<angebot>/` |

Das zweijährige Berufskolleg für Informationstechnische Assistentinnen und
Assistenten hat wie im Original keine Untertafel. Insgesamt 26 Unterseiten;
jede trägt ein Bild des jeweiligen Schwerpunkts und, wo vorhanden, den
Flyer des Bildungsgangs. Die Übersichtsseite jedes Bildungsgangs stellt die
Richtungen mit je einem Bild voran – dieselben Aufnahmen, die das Original an
dieselben Stellen zeigt.

**Bildinhalte als Text:** Mehrere Originalseiten liefern ihren Inhalt als
Bild statt als Text – die SMV-Folie, der Flyer des Schulsanitätsdienstes,
die Tabelle des Beratungssystems und die „Stimmen Ehemaliger" des TG. Alle
vier stehen auf den neuen Seiten als Bild **und** als mitlesbarer Text
drunter (Namen, Räume, Termine, Zitate unverändert übernommen); wer das
Bild nicht lesen kann oder will, verliert keine Information.

**Bewusst kein Autolinking:** bloße Adressangaben im Fließtext werden nicht
automatisch verlinkt; `markup.goldmark.extensions.linkify` ist abgeschaltet.
Links entstehen nur über ausgeschriebene Markdown-Ziele – genau die prüft
`qa/extlinkcheck.py`. Wo das Original Adressen verlinkt, verlinken wir mit;
zwei Ziele sind inzwischen tot („www.muetze-voll-leben.de" und
softatomos.com/kane/, Domains weg) und stehen deshalb als reiner Text –
ebenso der Sea-Shepherd-Verweis, der im Original auf den alten
vorgelagerten Server zeigt.

**Bis zur Ablöse des Originals offen:** die Migration der alten URLs
(Weiterleitungen der ghse.de-Pfade, siehe Abschnitt 8, Punkt 7),
vollständiger Serviceersatz (IServ bleibt als Dienst stehen) und
Buchungssystem. Die Architektur (Hugo-Layouts, Sections,
`.pages.yml`) lässt sich dafür ohne Umbau erweitern.

---

## 3. Quellen der Originalinhalte

Inhalte wurden von den unten stehenden Seiten der Originalseite übernommen
(Texte unverändert bzw. für Karten/Teaser gekürzt), Bilder und PDFs in den
Projektordner geladen und einzeln geprüft.

| Inhalt | Quelle |
|---|---|
| Hero, Fakten, Karten-Titel | `https://www.ghse.de/`, `https://www.ghse.de/die-ghse/` |
| Aktuelles (5 Meldungen inkl. Abbildungen) | `https://www.ghse.de/` (Abschnitt „Aktuelles") bzw. `https://www.ghse.de/presse/<schlagzeile>/` |
| Termine (Einleitung, 9 Kalender-Links) | `https://www.ghse.de/` (Abschnitt „Termine") → öffentliche Nextcloud-Kalender der GHSE |
| Berufs- und Studieninformation (Startseite) | `https://www.ghse.de/` (Abschnitt „Berufs- und Studieninformation") → Einzelbeiträge; nur Einträge mit Zukunftsdatum erscheinen, die drei Aufzeichnungs-Einträge von 2024 sind ausgeblendet |
| Instagram (Einleitung, 8 Accounts, 4 Beiträge) | `https://www.ghse.de/` (Abschnitt „Die GHSE bei Instagram") → `instagram.com/ghse_emmendingen` |
| Schüler/innen – Schulleben – Lehrer/innen | `https://www.ghse.de/schueler-schulleben-lehrer/` (Aufzeichnung `recherche/quellen/schueler-schulleben-lehrer.html`) |
| MINT | `https://www.ghse.de/mint/` (Aufzeichnung `recherche/quellen/mint.html`) |
| Berufsinformation | `https://www.ghse.de/berufsinformation/` (Aufzeichnung `recherche/quellen/berufsinformation.html`) |
| Förderverein | `https://www.ghse.de/unsere-schule/ueber-uns/foerderverein-2/` (Aufzeichnung `recherche/quellen/foerderverein.html`) |
| Partner-Logostreifen | `https://www.ghse.de/` (Abschnitt „Partner") |
| Schularten-Übersicht + Detailseiten | `https://www.ghse.de/schularten/…` (Teilzeit-/Vollzeitschularten) |
| Schularten im Wortlaut (29 Seiten) | `https://www.ghse.de/schularten/…` – Aufzeichnungen `recherche/quellen/schulart-*.html`: Pflege (6), Sozialwissenschaftliches Gymnasium (3), zweijährige Berufsfachschulen (5), einjährige Berufsfachschulen (4), Technisches Gymnasium (4), Berufsschule (6), zweijähriges Berufskolleg (1) |
| Detailseite TG | `https://www.ghse.de/schularten/vollzeitschularten/technisches-gymnasium/` |
| Berufsvorbereitung: AV-Dual, VABO, VABKF, BVE | `https://www.ghse.de/schularten/vollzeitschularten/berufsvorbereitung/` samt vier Untertafeln (Aufzeichnungen `recherche/quellen/berufsvorbereitung.html`, `bv-av-dual.html`, `bv-vabo.html`, `bv-vabkf.html`, `bv-bve.html`) |
| News (10 Meldungen inkl. Abbildungen) | `https://www.ghse.de/presse/` bzw. `https://www.ghse.de/presse/<schlagzeile>/` |
| Downloads (Titel, Kategorien, Dateien) | `https://www.ghse.de/downloads/…`, WP-Download-Manager-Pakete |
| Oberstufeninformationen | `https://www.ghse.de/schueler/oberstufeninformationen/` (Aufzeichnung `recherche/oberstufeninformationen-roh.md`) |
| Infoveranstaltung | `https://www.ghse.de/infoveranstaltung/` (Aufzeichnung `recherche/infoveranstaltung-roh.md`) |
| Kontakt, Öffnungszeiten, Service-Links | Impressum-/Footer-Angaben der Originalseite |
| Service- und Schülerseiten (16) | `https://www.ghse.de/anfahrt/`, `/schulbienen/`, `/schulsanitaetsdienst/`, `/schueler/smv/`, `/schueler/beratung/`, `/schueler/beratung-2/`, `/schueler/av-dual-begleitung/`, `/schueler/vertretungsplan/`, `/schueler/besserghse-de/`, `/online-abmelden/`, `/nextcloud/`, `/unsere-schule/organisatorisches/fachgruppen/`, `/downloads/studienfahrten/`, `/downloads/projekte-software/`, `/downloads/anmeldeformulare/`, `/unesco/unesco-aktivitaeten/` |
| UNESCO-Einstiegsseite | `https://www.ghse.de/unesco/was-heisst-unesco-projektschule/` |
| Erasmus+ | `https://www.ghse.de/ghse-emmendingen-ist-erasmus-akkreditiert-europa-erleben/` |
| Die GHSE | `https://www.ghse.de/die-ghse/` (Aufzeichnung `recherche/quellen/die-ghse.html`, Stand 9. Dezember 2025) |
| Safer Space | eigene Aufzeichnung (`recherche/saferspace-roh.md`, ohne Seiten-URL erfasst) |
| BewO (Bewerbung online) | `https://www.ghse.de/bewo/` (Aufzeichnung `recherche/bewo-roh.md`) |
| Praktikum für Studierende | `https://www.ghse.de/praktikum-fuer-studierende/` (Aufzeichnung `recherche/praktikum-fuer-studierende-roh.md`) |
| Impressum und Datenschutz | `https://www.ghse.de/impressum/`, `https://www.ghse.de/datenschutz/` (Aufzeichnung als Markdown) |

**Nachrichtentext:** Die Pressebeiträge der GHSE bestehen auf der Originalseite
aus Überschrift, Quelle + Datum, Teaser, Abbildung(en) (Zeitungsausschnitte)
und externem Quellenlink – ohne Fließtext. Die Detailseite zeigt genau diese
Felder; es wurde bewusst kein Text erfunden. Die Vollständigkeit wurde gegen
die Presse-Sitemap von ghse.de geprüft (160 Beiträge): alle zehn Beiträge mit
Pressedatum vom 30.06.2026 bis 07.10.2026 sind übernommen, vier davon wurden
dabei nachträglich ergänzt. Meldungen ohne Teaser („Besuch aus China",
drei Abbildungen) und ohne Abbildung („Von Pädagogik bis Physik prämiert")
sind in Templates und CMS-Feldern abgedeckt. Startseite und Newsliste zeigen
dieselben Beiträge; die Startseite listet die drei neuesten plus einen
Link auf alle Meldungen.

**Instagram:** Die GHSE betreibt auf ihrer Startseite einen Feed mit acht
Accounts und vier aktuellen Beiträgen. Die Originalseite lädt diese Beiträge
per JavaScript nach; hier liegen die vier Bilder statisch unter
`static/bilder/insta-*.webp` (aus den öffentlichen Embed-Seiten der Beiträge
gelesen) und werden mit der Kurzfassung der Bildunterschrift verlinkt –
ohne Einbettung, ohne Drittanbieter-Skript. Zum Auffrischen dient
`python3 tools/instagram.py` (Abschnitt 1); die acht Account-Links bleiben
jederzeit aktuell.

**Kleinere Textkorrekturen** (dokumentiert, weil das Original fehlerhaft ist):
„Badischen Zeitung" → „Badische Zeitung" (Quellenlabel), „Die Einjährige
Berufsfachschulen sind…" → „Die Einjährigen Berufsfachschulen sind…".

Für die vierunddreißig Seiten mit eigener Quelle – die zwanzig Service-,
Schüler- und Themenseiten (darunter die Oberstufeninformationen und die
Infoveranstaltung), die vier Untertafeln der Berufsvorbereitung
sowie Die GHSE, MINT, Schulleben, Förderverein, Berufsinformation, BewO,
Praktikum, Impressum, Datenschutz und Safer Space –
gilt dieselbe Regel: jedes Wort steht so, wie die Quelle es schreibt, nur wo
diese offensichtlich fehlerhaft ist, wird richtig gestellt.
Diese Fälle sind es, jeder einzelne gegen die Originalseite nachgeprüft
(siehe Abschnitt 6, `qa/paare.py`):

*UNESCO-Aktivitäten:* „UNSECO" → „UNESCO", „Kathastrophe" → „Katastrophe",
„30ten mal" → „30. Mal", „Mittepunkt." → „Mittelpunkt.",
„Unesco-Projektetage" → „UNESCO-Projektstage", „engagiereN" → „engagieren",
„Flash Mop" → „Flashmob", „einen ein Scheck" → „einen Scheck",
„berichtete/" → „berichtete", „Januar. 2018" → „Januar 2018",
„UNESCO- Projekte" → „UNESCO-Projekte", „Welterbe- Erde/" → „Welterbe-Erde /",
„2 BFH2" → „2BFH2", „2 BFP2-Klassen" → „2BFP2-Klassen", „u. a." →
„unter anderem", „z.B." → „zum Beispiel", „versch." → „verschiedenen",
„span." → „spanischen", „verg." → „vergangenen", „Leitg." → „Leitung",
„13.ten Klassen" → „13. Klassen", „Hausw. Verantw." → „Hauswirtschaft
verantwortlich", „UNESCO Projektschule" → „UNESCO-Projektschule",
„UNESCO – Regionaltagung" → „UNESCO-Regionaltagung" (zweimal),
„UNESCO Aktivitäten im 2. Halbjahr-an" → „UNESCO-Aktivitäten im 2. Halbjahr
an" (Linktext des zweiten Berichts in der Download-Liste), „08.März" →
„08. März",
„14.12 – 19.12. 2003" → „14.12. – 19.12.2003" und „2.7 – 5.7. 2003" →
„2.7. – 5.7.2003" (Datumsbereiche), „stattgafunden." → „stattgefunden.".
„Monika Bre" → „Monika Bresch": der Name
ist auf der Originalseite an der Zeilenkante abgeschnitten und steht zweimal
vollständig auf derselben Seite. Dazu die Umbruch- und Bindestrichrestaurie-
rungen, die jede Seite mitbringt, wenn Zeilenenden hart umgebrochen waren
(„KFZ- Abteilung-" → „KFZ-Abteilung", „GHSE- Combo" → „GHSE-Combo",
„Tschernobyl Gedenktag-" → „Tschernobyl-Gedenktag", „DM-Markt Kette" →
„DM-Markt-Kette", „UNESCO Arbeit" → „UNESCO-Arbeit", „Relax Bank" →
„Relax-Bank", „SG10 Spanisch-Kurses" → „SG10-Spanisch-Kurses",
„Französisch Fachschaft" → „Französisch-Fachschaft"). Zwei Einträge fehlen
bewusst, weil die Quelle sie doppelt führt: unter „2007/2008" stand
„Baumpflanzaktion zum Weltfriedenstag" zweimal, dieselbe Zeile noch einmal
nach „Internationales Polarjahr – Klimawandel"; und der Reiter „2022/2023"
steht dort zweimal mit demselben Text, sein Inhalt – „2022/2023 Die
Regionaltagung der UNESCO-Projektschulen Baden-Württemberg mit aktuell 34
Bildungseinrichtungen …" und alles, was darunter in diesem Reiter folgt –
steht bei uns genau einmal. Zwei Stellen bleiben unangetastet, weil sie
Original sind und kein Tippfehler: das „???" beim Musikzugprojekt (Mai 2016)
und „kommt noch" (Schuljahr 2020/2021, das die Quelle offen hält).

*Projekte und Software:* „Hall of fame" → „Hall of Fame", „Java Runtime
EnvironmentTM" → „Java Runtime Environment", „dass sie das Java Runtime
Environment … installiert" → „dass Sie …" (zweimal), „TG Informationstechnik
des TG" → „TG Informationstechnik", „z.B." → „zum Beispiel", „voraus. Abi-
Jhg." → „voraussichtlicher Abiturjahrgang" und „Abi-Jhg." → „Abiturjahrgang"
(Abkürzungen ausgeschrieben). Ein Tensewechsel mit Begründung: „sind … zu
finden" → „waren … zu finden", weil das Projekt unter `softatomos.com/kane/`
nicht mehr erreichbar ist – die Domain löst beim Nachprüfen gar nicht mehr
auf (NXDOMAIN, im Gegensatz zu `ghse.de`). Die tote Adresse bleibt bewusst
als Klartext im Text stehen, ohne Link: Sie ist Teil der Projektdokumentation
und führte nach dem Cutover sonst ins Leere.

*Vertretungsplan:* „verschiendenen" → „verschiedenen", „große Monitor" →
„große Monitore". Außerdem zeigt der Satzanfang nicht mehr die Adresse
„Unter https://www.ghse.de/ekb", sondern „Im WebUntis" – das Original zeigt
diese Adresse als Linktext und schickt schon selbst weiter auf
`erato.webuntis.com/WebUntis`, das Ziel ist also unverändert; als sichtbarer
Text bleibt nur die Adresse, die auch das Ziel ist.

*Fachgruppen:* „unter Anderem" → „unter anderem".

*Beratungssystem:* „Beratungslehrer innen" → „Beratungslehrerinnen" (im
Original durch ein Tag mitten im Wort getrennt).

*Schulsozialarbeit:* „Schülerinennen" → „Schülerinnen" (Tippfehler der
Vorlage) und „zuständig für" → „Zuständig für" als Satzanfang. Der
Kastentitel „Schulsozialarbeit" steht im Original fünfmal, jedes Mal direkt
vor dem Namen („Schulsozialarbeit Luzia Bindner", „Schulsozialarbeit Kolja
Chmieliczek" …); bei uns heißt der Block nur einmal so und die Namen stehen
fett – Räume, Durchwahlen und Klassen bleiben unverändert.

*UNESCO-Einstiegsseite („Was heißt UNESCO-Projektschule?"):* „exclusiv" →
„exklusiv", „mit zu machen" → „mitzumachen", „Donnerstag Nachmittag." →
„Donnerstagnachmittag.", „z.B." → „zum Beispiel" (zweimal) und der Linktext
„Email" → „E-Mail", weil die Seite sonst ohne Angabe darauf verweist.

*AV-Dual Begleitung:* Der Titel heißt wie im Original „AV-Dual Begleitung",
im Fließtext steht die Bezeichnung einheitlich, während das Original sie
dreifach mischt („AV-Dual Begleitung", „AV-dual Begleitung",
„AV-dual-Begleitung"). Gleiches gilt für die Angebotsüberschrift: das
Original schreibt „Angebote für AV-dual Schülerinnen und Schüler", bei uns
steht die Zusammensetzung mit Bindestrich („AV-dual-Schülerinnen"). Die
Großschreibung von „Du" und „Dir" in den beiden
Sätzen an die Eltern steht genauso im Original und wurde nicht angeglichen.

*Schulsanitätsdienst und SMV:* Diese beiden Seiten bestehen im Original aus
einem Bild; was darauf steht, steht bei uns als Text darunter (Abschnitt 2).
Übernommen wurde wörtlich, geglättet nur die Trennstriche der Grafik
(„Ersten – Hilfe" → „Ersten Hilfe", „Erste – Hilfe Kursen" →
„Erste-Hilfe-Kursen").

*Die GHSE:* „allgemeinenen" → „allgemeinen", „Namen" → „Name" (Grammatik)
und „AV dual" → „AV-Dual", weil die Quelle die Verbundform einmal mit und
einmal ohne Bindestrich schreibt.

*BewO:* „vorläufigen Zu- oder Absage" → „vorläufige Zu- oder Absage" und
„vorläufige Zu- oder Absagen" → „vorläufige Zu- oder Absage" (die Quelle
mischt Einzahl und Mehrzahl), „Niveaum" → „Niveau", „Bewo- Infoblatt" →
„BewO-Infoblatt", „z.B." → „z. B."; in der Ansprechpartner-Liste
„Ansprechpartner sind für das Technische Gymnasium" → „Technisches
Gymnasium" und „das Sozialwissenschaftlich Gymnasium" → „das
Sozialwissenschaftliches Gymnasium" (Grammatik), außerdem das „2BKI" →
„Berufskolleg für Informations- und Kommunikationstechnik", wie der
Bildungsgang auf seiner Schulartseite heißt.

*Praktikum:* „nahe zu" → „nahezu", „zahleichen" → „zahlreichen",
„allgemein bildender" und „allgemein bildenden" → „allgemeinbildender" und
„allgemeinbildenden", „z. Zt. Herr Michael Feißt, Frau Annina Schäfer" →
„zurzeit Herrn Michael Feißt und Frau Annina Schäfer" (Dativ nach „durch",
dazu „und" statt Komma). Der Seitentitel trägt wieder die volle
Quellenüberschrift „Praxissemester oder Orientierungspraktikum an den GHSE".

*Datenschutz:* „Rechtsanwälteerstellt." → „Rechtsanwälte erstellt." – im
Original verschluckt die Verlinkung der Kanzlei das Leerzeichen.

*MINT:* „Unsere Angebote und Aktion" → „Unsere Angebote und Aktionen"
(in der Quellenüberschrift ist das „en" abgeschnitten), „Pflichfach" →
„Pflichtfach" (zweimal, Tippfehler), „zahlreiche Preis und Platzierungen" →
„zahlreiche Preise und Platzierungen", „in praktischen Bereich" → „im
praktischen Bereich", „des Sozialwissenschaftlichen Gymnasium" → „… des
Sozialwissenschaftlichen Gymnasiums", „richten sich an Jugendlichen und
junge Erwachsene" → „… an Jugendliche …" und „in einem Ausbildungsberufe" →
„in einem Ausbildungsberuf" (Grammatik), „z.B." → „z. B.". Die beiden
Zwischenüberschriften tragen wieder die Kurzformen der Quelle („2-jährige
Berufsfachschule", „1-jährige Berufsfachschule – Technik pur").

*Förderverein:* „1.Vorsitz" und „2.Vorsitz" → „1. Vorsitz" und
„2. Vorsitz" (fehlende Leerzeichen), „Beitritterklärung" →
„Beitrittserklärung" (Tippfehler).

*Berufsinformation:* „an anderen Schule" → „an anderen Schulen", „auf den
Jobstartbörse" → „auf der Jobstartbörse", „des Hochschulteam der Agentur
für Arbeit" → „des Hochschulteams …" (Grammatik), „des 6jährigen SG" →
„des 6-jährigen SG" (Trennstrich). Die Anrede „SchülerInnen" des Originals
steht als „Schülerinnen und Schüler" (Geschlechterform nach Absprache).

*Geschlechterform (Beschluss):* Im Bestand steht die volle Form — wo die
Quelle den Stern nutzt, bleibt das als beabsichtigte Abweichung stehen:
„Schüler*innen" → „Schülerinnen und Schüler" (MINT, Förderverein,
unsere-schule, VABKF), „Beratungslehrer*innen" → „Beratungslehrerinnen und
Beratungslehrer" und „Lehrer*innen und Mitschüler*innen" → „Lehrerinnen
und Lehrern sowie Mitschülerinnen und Mitschülern" (Beratungssystem),
„die Sozialarbeiter*innen" → „die Sozialarbeiterinnen und Sozialarbeiter"
(VABKF), „Schüler*innen und Lehrkräfte" → „Schülerinnen und Schüler sowie
Lehrkräfte", „Mobilitäten für Schüler*innen" → „… für Schülerinnen und
Schüler" und „Kolleg*innen" → „Kolleginnen und Kollegen" (Erasmus+),
„Mitschüler*innen" → „Mitschülerinnen und Mitschülern" (Schulsanitätsdienst).

*Berufsvorbereitende Schularten (Übersichts- und vier Detailseiten):* die
vier Untertafeln (AV-Dual, VABO, VABKF, BVE) führen als eigene Seiten mit
dem vollen Quellwortlaut; die Übersichtsseite ergänzt den Einleitungssatz
mit den vier Links und je einen „Mehr erfahren"-Verweis wie die
Kacheln der Quelle (die VABKW-Kachel zeigt wie im Original auf die
Kooperationsschule fbs-emmendingen.de). Korrekturen: „Berufvorbereitende
Einrichtung" → „Berufsvorbereitende Einrichtung" (Tippfehler der
Quellenüberschrift), „Deutschkenntnis-sen" → „Deutschkenntnissen"
(Zeilentrennung), „SBBZabgeschlossen" → „SBBZ abgeschlossen" und
„KooperationF" → „Kooperation F" (in der Quelle zusammengerückt),
„V= VorqualifizierungsjahrA= ArbeitB= BerufK= mit einem SBBZ" als
Listenpunkte auseinandergezogen, das abgerutschte „l" hinter der FAQ-Frage
„Was gefällt den Schüler*innen am VABKF?" entfernt; die FAQ führt die
Frage „Wie sieht es mit Englisch aus?" doppelt, wie die Quelle,
„wesentlichen Unterstützungsbedarf, der … nicht
zulässt" → „wesentlicher Unterstützungsbedarf …" (Grammatik),
„entwickeln die jugendlichen" → „die Jugendlichen" (Großschreibung),
„von 7.45 Uhr – 15.00" → „… – 15.00 Uhr" (fehlendes „Uhr"). Die
„Impressionen"-Galerien der vier Detailseiten sind noch nicht übernommen;
je ein Bild des Bildungsgangs steht auf der Übersichtsseite.

*Schularten im Wortlaut (29 Seiten):* Übersicht und Untertafeln aller
Bildungsgänge sind aus den Originalseiten übernommen (Aufzeichnungen
`recherche/quellen/schulart-*.html`, Bilder über
`python3 tools/schularten-bilder.py` als WebP unter
`static/bilder/schularten/`). Die Struktur folgt der Vorlage: Pflege (eine
Übersicht mit fünf Wegen), Sozialwissenschaftliches Gymnasium (Übersicht,
6-jähriges und 3-jähriges SG), zweijährige Berufsfachschulen (Übersicht,
Metalltechnik, Elektrotechnik, Hauswirtschaft und Ernährung, Gesundheit und
Pflege), einjährige Berufsfachschulen (Übersicht, Metalltechnik,
Holztechnik, Fahrzeugtechnik), Technisches Gymnasium (Übersicht,
Informationstechnik, Mechatronik/Technik, Technik und Management),
Berufsschule (Übersicht, Bautechnik, Elektrotechnik, Holztechnik,
Kraftfahrzeugtechnik, Metalltechnik) und das zweijährige Berufskolleg für
Informationstechnische Assistentinnen und Assistenten. Die FAQ-Akkordeons
der Vorlage stehen bei uns als Überschrift mit Antwort darunter, die
Bildunterschriften der Galerien als Bildunterschrift. Korrekturen an der
Vorlage: „machen.Außerdem" → „machen. Außerdem" (2BFAHM),
„Bäumepflanzen in Palenstina" → „… in Palästina" (TG),
„maßgebend.D.h." → „maßgebend. D.h." und „Landkreis.Es" → „Landkreis. Es"
(Berufsschule) – das sind die einzigen drei Stellen, an denen zwei Sätze im
Original ohne Abstand in einem Textfeld stehen; außerdem
„Die Einjährige Berufsfachschulen sind…" → „Die Einjährigen Berufsfachschulen
sind…" (siehe oben). Die Seitentitel der Untertafeln nennen den
Schwerpunkt ausgeschrieben („Metalltechnik (2BFM)", „TG Informationstechnik",
„Berufsschule: Bautechnik"), weil die Vorlage dort nur die Kurzform
verwendet; die Menüpunkte tragen weiterhin die Bezeichnungen der
Navigationsleiste. Die Übersichtsseiten der zweijährigen und einjährigen
Berufsfachschulen stellen jede Richtung mit dem Bild voran, das das Original
an derselben Stelle zeigt (`2bfe`, `2bfh2`, `2bfm-1`, `2bfp2` bzw. `1bfm`,
`1bfz`, `1bfr`). Wo die Seitenleiste sonst das gleiche Foto zeigte, steht
dort eine andere Aufnahme derselben Sammlung (`2bfp-2` bzw. `1bfz-1`); im
Fließtext bleiben ausschließlich die Originalbilder.

*Oberstufeninformationen:* Die Seite
`https://www.ghse.de/schueler/oberstufeninformationen/` (Aufzeichnung
`recherche/oberstufeninformationen-roh.md`) ist als eigene Seite unter
`/oberstufeninformationen/` übernommen: die sieben Überschriften des
Originals, der Link zum Universalnotenrechner, die beiden Verweise auf die
offiziellen Infos des Ministeriums und der Satz „Keine Downloads gefunden!"
unter dem Abiturjahrgang 2029 stehen im Wortlaut. Die Dokumente sind die
aus der Sammlung (22 Einträge wie im Original); jede Zeile zeigt Titel,
Kurzbeschreibung, Format und Größe. Zwei Abweichungen: der Seitentitel
„Oberstufeninformationen" (das Original beginnt im Text mit
„Informationen für die Oberstufe des Beruflichen Gymnasiums", führt die
Seite im Menü aber unter derselben Bezeichnung), und der Eintrag
„Leitfaden zum Abi 2028" – das Paket auf dem Originalserver trägt keine
Datei mehr, der Download antwortet mit „No file is attached with this
package!"; bei uns steht an der Stelle der Hinweis „Die Datei zum
Leitfaden zum Abi 2028 ist derzeit nicht verfügbar." Die Zeilen
„1 Datei(en) … KB Download" des Download-Managers fehlen hier wie auf der
Download-Seite (der Build rechnet Größe und Format aus der Datei selbst).

*Infoveranstaltung:* Die Seite `https://www.ghse.de/infoveranstaltung/`
(Aufzeichnung `recherche/infoveranstaltung-roh.md`) ist mit ihrem Wortlaut
übernommen: die Überschrift „Infoveranstaltungen@ghse 2023", der
Einladungstext, das Programm des Tages der offenen Tür mit derselben
Verschachtelung der Aufzählungen, die Liste der Schularten für den Infoabend
und der Schlusssatz „Wir freuen uns auf Ihren Besuch." Zwei Abweichungen:
der Seitentitel „Infoveranstaltung" (das Original beginnt im Text mit der
Überschrift „Infoveranstaltungen@ghse 2023"), und die beiden Links des
Originals auf seine eigenen Veranstaltungsseiten – „bitte hier anmelden"
(Tag der offenen Tür) und „Infoabend für die meisten Schularten" – stehen
als Klartext im Text, nicht als Link: die erste Seite leitet nur noch auf
die Startseite um, die zweite auf eine leere Seite (siehe Abschnitt 8,
Punkt 3). Das Original führt die Seite in keinem Menü; bei uns steht sie
unter „Anmeldung", damit sie erreichbar bleibt.

**Abweichungen, die keine Textkorrekturen sind** (jeweils mit Begründung):
die Meta-Beschreibungen, weil das Original auf jeder Seite denselben
Baustein-Text führt („Gewerbliche und Hauswirtschaftlich-Sozialpflegerische
Schulen Emmendingen (GHSE)") und keine seitenbezogene Beschreibung kennt;
die Einbettungen, die zu einfachen Links werden (die OpenStreetMap-Karte der
Anfahrtseite, die Live-Waage der Schulbienen mit identischem Ziel);
die Sprungmarke auf die beiden PDF-Berichte der UNESCO-Seite („Die Berichte
des Schuljahres als PDF:") als Überschrift für vier Original-Dateien;
der Linktext auf der Anmeldeformularseite ohne `https://`, wobei das Ziel
`ghse.schulanmeldungen.com` dasselbe wie im Original ist;
vier Überschriften, die ein Wort aus dem Originalsatz über genau den Satz
stellen, der dort ohne Überschrift steht: „Trägerschaft" auf AV-Dual und
Schulsozialarbeit, „Veranstaltungen" und „Koordinatorinnen" auf der
UNESCO-Einstiegsseite;
vier Zwischenüberschriften auf der Seite Die GHSE, die die Fettlabels und
Foliensätze der Quelle als Überschrift führen („Eine Schule und für viele
gleichzeitig viele Schulen", „Gewerblich geprägt ist ein Großteil unserer
Schule", „Hauswirtschaftlich ist die Schule seit 1993", „Sozialpflegerisch");
fünf Seitenüberschriften, weil die Vorlage ihre Hero-Überschrift nicht als
`title` führt – bei uns steht dieselbe Zeile im `<h1>` und im Browser-Titel:
„Anfahrt an die GHSE", „Willkommen bei der AV-Dual Begleitung", „Beratung",
„Projektarbeiten/Software", „Vertretungsplan der GHSE";
die Seitenüberschriften „Impressum" und „Datenschutz", weil die Quelle dort
ohne Seitenüberschrift mit dem Schulnamen bzw. mit der Zwischenüberschrift
„Datenschutzerklärung" beginnt, und drei Zwischenüberschriften auf der
BewO-Seite
(„Sicherer Schulplatz", „Fast sicherer Schulplatz", „Ansprechpartner"), die
je eine Liste einleiten, welche die Quelle ohne Überschrift führt – die
letzte ersetzt den Listenauftakt „Ansprechpartner sind für das";
die beiden BewO-Linktexte, die in der Quelle die volle Adresse nennen
(`https://bewo.kultus-bw.de/,Lde/Startseite/BewO` und
`https://bewo.kultus-bw.de/,Lde/Startseite/BewO/Downloads`) und bei uns als
Domain stehen, sowie der Sekretariatsverweis, der statt der damaligen
kasserver-Adresse auf die eigene Seite zeigt (nur das Ziel, der Text bleibt);
vier Menülabels, die wieder so geschrieben sind wie in der Navigationsleiste
der Vorlage („2-jähriges Berufskolleg für Informationstechnische Assistenten",
„Unesco Aktivitäten", „Was heißt UNESCO Projektschule?", „Projekte/Software");
drei Menüpunkte weichen davon ab, weil der Punkt sonst zu lang wird oder die
Seite anders heißt als er: „Schülerinnen, Schulleben, Lehrerinnen" (Vorlage
„SchülerInnen – Schulleben – LehrerInnen", das ist der Seitentitel),
„Anmeldung" (Vorlage „An der Schule anmelden") und „für Berufliches
Gymnasium, BK und 2BF (BewO)" (Vorlage „für das Berufliches Gymnasium, BK,
2BF (BewO)"); und die Download-Listen, weil das Original
Dateianzahl und Dateigröße als eigenen Text neben jedem Titel führt
(„1 Datei(en) 53.19 MB Download") beziehungsweise auf der
UNESCO-Einstiegsseite eine Tabelle („Anhänge Datei Beschreibung Jahresschrift
2016"). Bei uns steht dort nur Titeltext, ohne die Größenangaben dazwischen:
„Downloads Projektarbeit (TGI): ClipClick Projektarbeiten (TGI):
Papiercomputer Projektarbeiten (TGI): Vokabeltrainer" auf der Projektseite,
„Regelungen bei Schulveranstaltungen Angebote für Studienfahrten" auf
Studienfahrten. Größe und Format ermittelt der Build aus der Datei selbst
(Abschnitt 3, „Getestete Downloads").

**Seiten ohne Wortpaar:** Die Startseite und „Unsere Schule" sind
Zusammensetzungen mehrerer Originalseiten und werden nicht paarweise
geprüft. Die Startseite führt neun Abschnitte, deren jede ihre Quelle in
der Tabelle oben hat (Aktuelles und Berufsinformation als Auszüge der
jeweiligen Originalseiten); „Unsere Schule" fasst fünf Ursprungsseiten
zusammen (Aufzeichnungen unter `recherche/quellen/`: `unsere-schule.html`
mit den Öffnungszeiten, `-organigram.html`, `-schulleitungsteam.html`,
`-sekretariat.html`, `-leitbild.html`) und formatiert sie um: Tabellen
sind Fließtext geworden (die Öffnungszeiten „07 30 12 00" stehen als
„7.30 bis 12.00 Uhr"), Abkürzungen sind ausgeschrieben („2-jähr. BFS" →
„Zweijährige Berufsfachschule", „TG SG" → „Technisches Gymnasium,
Sozialwissenschaftliches Gymnasium"), die Bilder tragen eigene
Beschreibungen (deshalb der Satz über die 24 Fachschaften, der zur
Organigramm-Beschreibung gehört), und die ÖPR-Mitglieder des
Schulleitungsteams sind in die Liste aufgenommen.

**Weitere beabsichtigte Abweichungen:**
der Seitentitel „MINT-freundliche Schule", weil die Originalseite ohne
eigene Überschrift beginnt (das Menü heißt dort wie bei uns „MINT");
der Seitentitel „Förderverein" als Menülabel, wo das Original
„Der Förderverein der GHSE" schreibt, dazu der Einleitungssatz „… e. V.
unterstützt die Schule und ihre Schülerinnen und Schüler." als kurze
Einordnung, deren Inhalt die Aufgabenliste der Quelle selbst führt;
auf der Schulleben-Seite der Kasten „Neueste Beiträge" der Originalseite
(„ghse.de Neueste Beiträge Universität Tübingen Aktionswoche zur
Studienorientierung 13.-17. Mai 2024, Tag der offenen Tür …"), der bei uns
nicht wiederholt wird, weil die Meldungen unter `/news/` leben;
auf der Berufsinformationsseite der „Aktuelles"-Kasten und der Abschnitt
„Externe Angebote" der Originalseite (23 terminierte Angebote externer
Hochschulen und Arbeitgeber, Stand der Aufzeichnung 2024), die aus demselben
Grund nicht übernommen sind, sowie der Moodle-Verweis: die
Terminbuchung zeigt auf die Instanz `04102015300.moodle.bw.schule/` statt
in die stillgelegte Dienstadresse, der Deep-Link
„unter dem Link https://moodle.ghse.de/moodle/mod/scheduler/view.php?id=10929"
entfällt, der Einschreibeschlüssel bleibt.

**Bildnachweise:** Logo, Gebäudeaufnahme, Schulartbilder und Presseabbildungen
stammen von `www.ghse.de` (Theme „ziegenhagel", Uploads). Eingebunden als
Arbeitsstand; vor der Ablöse von www.ghse.de braucht die Schule die
Freigabe (Urheberrecht der regionalen Zeitungen bei den Presseabbildungen).
Vier Wappen der Träger und Förderer liegen zusätzlich als eigene Dateien
darunter (`landratsamt-emmendingen.webp`, `kvjs-logo.webp`,
`ministerium-wirtschaft-arbeit-tourismus.webp`,
`ministerium-soziales-gesundheit-integration.webp`): sie stehen über dem
Förderabsatz auf AV-Dual Begleitung und Schulsozialarbeit, mit leerem
`alt`-Attribut wie im Original.

**Partner-Logostreifen:** Diese Fassung nutzt die aktuelle Fassung von ghse.de
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
   Ordner-Sammlungen, dazu jede weitere Seite einzeln – die 28 Einzelseiten
   im Wurzelverzeichnis von `content/`: die 16 Service- und Schülerseiten,
   UNESCO und Erasmus+, Impressum und Datenschutz, Safer Space sowie Die
   GHSE, Unsere Schule, MINT, Schüler/innen – Schulleben, Förderverein, BewO
   und Praktikum. Jede Sammlung bietet
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
                    instagram.py (neueste Instagram-Beiträge in _index.md holen)
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
* Alle Abschnitte liegen auf derselben Papierfläche; Gelb, Orange und Blau
  sind Akzente (Aktionen, Kicker, Kategorien, Links). Gelb füllt nur noch
  einzelne Komponenten wie `.kasten--gelb` oder Schaltflächen, keine ganzen
  Seitenbänder.
* Die Akzentfarben stehen so im GHSE-Logo (`static/bilder/logo-zeichen.webp`,
  aus der Logo-Vorlage übernommen):
  Gelb `#F8DC54`, Orange `#EC7030`, Blau `#1060A0` aus dem helleren Teil des
  Logo-Verlaufs – das dunkle Navy des Verlaufs bleibt bewusst unbenutzt.
  `qa/kontrast.py` liest die Tokens direkt aus `static/css/main.css` und
  prüft beide Farbmodi gegen diese Werte.
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
  Mobilmenü und an den einklappbaren Kategorien, `aria-current="page"` in
  der Navigation, Alt-Texte für alle
  Bilder (Bilder einzeln betrachtet und beschrieben), Farben auf Kontrast
  geprüft – `qa/kontrast.py` liest die Tokens direkt aus dem Stylesheet und
  rechnet alle Paare in Hell **und** Dunkel durch (19 Paare je Modus,
  kleinster Textwert 5,46:1 für den Kicker auf Papier,
  alle Paare bestehen),
  Touch-Ziele ≥ 44 px, `prefers-reduced-motion` respektiert.
* Responsive: Breakpoints 1199/1000/900/640/560 px – Karten- und Zeilenraster
  stapeln sich, unter 1200 px wird die Navigation zum Aufklappmenü, das
  zunächst nur die Kategorien zeigt; ein Pfeil klärt die Untertafel der
  getippten Kategorie auf und zu (die aktuelle Sektion steht offen),
  Download-Zeilen werden zu Vollbreiten-Karten mit großem Button. Nachgemessen
  wird das mit `qa/layout.py` (Ankersprung unter Kopf **und** Sprungleiste,
  Kopfhöhe, Touch-Ziele an 1440/640/390 px) und `qa/reflow.py` (79 Seiten ×
  11 Breiten = 869 Kombinationen, 0 Probleme – nichts bricht horizontales
  Scrollen aus). Dieselben drei Prüfungen laufen zusätzlich gegen einen Bau
  mit `--baseURL /ghse_website_prototyp/` (`qa/unterpfad.py`) – dort sind
  Schriften und alle Inhalts-Links fürchterlich schnell kaputt, weil die
  Seite unter dem GitHub-Pages-Unterpfad liegt und ein Pfad ohne `relURL`
  (Schriftquelle, zwei Schaltflächen-Ziele, alle Markdown-Links der
  Inhalte) unsichtbar unter "/" ins Leere lief; ein Render-Hook
  (`layouts/_default/_markup/render-link.html`) schreibt sie um.
* Links: alle internen Ziele geprüft (`qa/linkcheck.py`) – alle 80
  HTML-Dateien (79 Seiten plus `404.html`) sowie alle eingebundenen Bilder,
  Schriften und Dokumente (5100 Ziele gesamt, keine Fehlschläge,
  einschließlich der Sprungziele der Download-Kategorien). Die 59 externen Links prüft `qa/extlinkcheck.py` einzeln:
  keiner ist nachweisbar tot – darunter die 9 öffentlichen Nextcloud-
  Terminkalender, 12 Instagram-Links (8 Accounts, 4 Beiträge), BewO,
  Moodle, OSM, WebUntis, die alte Nextcloud-Speicherfreigabe,
  Impressum/Datenschutz und die Berufsinformations-Beiträge. Zwei Domains
  (`bauen-hat-zukunft.de`, `berufe-lexikon.de`) sperren die Messumgebung
  und werden deshalb als „lebend, aber gesperrt" geführt; ein dritter Link,
  `softatomos.com/kane/` (Projektseite von VplanTouch), zeigt ins Leere und
  steht deshalb als Klartext im Text, nicht als Link.
* Worttreue gegen die Vorlage: alle Seiten mit eigener Quelle werden Wort für
  Wort gegen ihre Originalseite geprüft – `qa/treue.py`
  vergleicht die Folge der Wörter (Kopf-, Navigations- und Fußblock der
  Vorlage fallen raus, ebenso der Adress- und Öffnungszeitblock, den die
  Vorlage auf jeder Seite mitschleift) und zählt reine Satzzeichen- und
  Trennstrich-Anpassungen getrennt, `qa/satzpruefung.py` zeigt für einzelne
  Sätze das passende Stück der Quelle und nur die abweichenden Wörter.
  Sechsundfünfzig Quellseiten liegen als HTML unter `recherche/quellen/` (64
  Aufzeichnungen insgesamt), sieben
  als Text (Impressum, Datenschutz, BewO, Praktikum, Safer Space,
  Oberstufeninformationen, Infoveranstaltung), damit die
  Prüfung nicht bei jedem Lauf ins Netz muss; die Zuordnung der
  dreiundsechzig Quellpaare ist explizit, weil Datei- und Seitennamen sich
  nicht decken (`schulsozialarbeit` liegt unter
  `/schueler/beratung-2/`), und `qa/paare.py` läuft alle Paare auf einmal
  durch und gleicht den Befund gegen Abschnitt 3 dieser Datei ab – ohne
  offene Stelle meldet es „davon 0 nicht zitiert" und Beendigungscode 0,
  sonst die Stellen, die noch fehlen. Der Lauf zählt derzeit 181
  Abweichungen, jede in Abschnitt 3 belegt. Erster Lauf dieser Prüfung hat
  vier stille Textänderungen und einen erfundenen Absatz gefunden, ein
  späterer noch einen erfundenen Satz und zwei Überschriften ohne Vorlage
  (die Details stehen in Abschnitt 3) – seither ist der Befund null. Beim
  Ausbau auf die fünf Textquellen und die Seite Die GHSE kam eine erfundene
  Adresse auf der Datenschutzseite ans Licht (die Anschrift des
  Landesbeauftragten, die die Quelle nicht führt), auf der BewO-Seite
  mehrere Umformulierungen („Bewerber" zu „Bewerberinnen und Bewerber",
  eingeschobenes „Uhr", zusammengezogene Listen) – alles zurück auf den
  Quellwortlaut. Was die Prüfung weiter meldet, sind die dort
  dokumentierten beabsichtigten Abweichungen, Baustein-Aufrufe und
  Linkadressen sowie zwei Restfetzen der Vorlage im Quelltext
  („Anfahrt Maps Anrufen Krank", „Uhr"), die aus zu kurzen Wortgruppen
  bestehen, um sie wie den übrigen Kopf- und Fußblock zu filtern, und die
  Aufzeichnungsvermerke der Textquellen („QUELLE saferspace", der
  Word-Kopf „Normal 0 21 false …") – `qa/paare.py` lässt sie als bekannt weg.
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
* Lighthouse nach dem Ausbau der Schularten (Lighthouse 13.5, mobil, gegen
  `tools/preview-server.py`): Startseite 99, Schularten-Übersicht 99,
  zweijährige Berufsfachschulen 99, Metalltechnik (2BFM) 100, Unsere Schule
  100, News-Übersicht 100 – Accessibility, Best Practices und SEO jeweils
  100, Bildspringen (CLS) überall 0. Zwei Befunde hat diese Messung
  aufgedeckt und beide sind behoben: der Menüknopf der Mobilnavigation
  verlor auf kleinen Bildschirmen seinen Namen (das Wort war mit
  `display: none` auch für Screenreader weg – jetzt nur visuell versteckt),
  und die Karten-Aktion („Mehr erfahren") war in der Akzentfarbe gesetzt
  (Gelb auf Weiß 1,36:1, Orange 3,03:1 – die Farbe trägt jetzt den
  Unterstrich, der Text bleibt schwarz).
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

## 8. Offene Punkte und getroffene Entscheidungen

1. **Presse-Meldungen ohne Volltext:** Solange ghse.de nur Teaser + Abbildung
   + Quellenlink liefert, bleibt die Detailseite bei diesen Feldern. Sobald
   Volltexte gepflegt werden, ist das `body`-Feld im CMS bereits angebunden.
2. **Bildfreigabe (erledigt):** Die GHSE hält die Freigaben für den
   www.ghse.de-Bestand; was dort veröffentlicht ist, ist freigegeben —
   die Einbindung von Bildern und PDFs ist damit für die Ablöse gedeckt.
3. **Kein Verweis mehr auf die Originalseite:** Alle 54 zieltragenden
   Menüeinträge (von 59 insgesamt; fünf sind reine Zwischenüberschriften)
   sind auf eigene Seiten, Anker oder die echten Dienste (WebUntis, Moodle,
   Shop, OSM, alter Nextcloud-Speicher) umgebucht; `grep -rho … ghse\.de` über
   `public/` liefert ausgeliefert nur noch `https://ghse.de/iserv/` – der
   IServ-Dienstpfad als Dienstadresse. Auch die Hinweisblöcke „Prototyp",
   der „Originalseite"-Link im Fuß, der Prototyp-Hinweis unter dem
   Copyright und die Quellen-URLs der zehn Pressemeldungen sind entfernt
   (die Quellenangabe selbst bleibt als Klartext im Bildtext stehen). Der
   Kultusportal-Deep-Link der Originalseite (404, Portal umgezogen) zeigt
   weiterhin auf die geprüfte Startseite des Kultusministeriums.
4. **Kein Tracking (entschieden):** Kein Analytics, kein Consent-Modul —
   ohne Tracking ist keine Einwilligung nötig; der Kopf bleibt dadurch
   auch schneller. Falls die Schule später doch Analysen will, ist der
   Punkt wieder offen.
5. **Instagram-Feed ist ein Standbild:** Der Abschnitt zeigt vier konkrete
   Beiträge mit lokalen Bildern statt eines Live-Feeds. Zum Auffrischen
   dient `python3 tools/instagram.py` (neueste Beiträge holen, Bilder als
   WebP ablegen, `insta_beitraege` in `_index.md` ersetzen; neue
   Bildbeschreibungen ergänzt der Hinweis in Abschnitt 1). Beschluss: das
   Skript bleibt der Weg — zu klären ist noch, wer es bei der GHSE
   regelmäßig (z. B. monatlich) ausführt.
6. **Bewusst nicht gebaut:** kein Taxonomie-/Blog-System, kein
   Pagination-Layout, keine Social-Media-Einbettung, kein SVG-Sprite-Katalog
   – die Ablöse braucht davon nichts; Erweiterungen sind über die
   Sammlungen in `.pages.yml` ohne Umbau möglich.
7. **Deployment zur Ablöse (entschieden):** Die Seite läuft weiter auf
   GitHub Pages. Geplant ist eine ergänzende FTP-Übertragung vom
   GitHub-Workflow auf den all-inkl-Server der GHSE; mit der eingetragenen
   Domain löst dieser Stand dann www.ghse.de ab. Weiterleitungen der alten
   ghse.de-Pfade (Abschnitt 2, „Bis zur Ablöse offen") sind mit dem Umzug
   auf dem all-inkl-Server einzurichten.
