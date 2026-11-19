> **Entscheidungsstand:** Dieses Dokument ist die Analyse- und Konzeptfassung
> **vor** der Richtungsentscheidung. Der Roll hatte das „Musterbuch“
> zugewiesen und es wurde hier empfohlen. Auf Wunsch des Auftraggebers
> („Eigenständigkeit ist nicht so wichtig, es muss nur gut werden“) wurde
> stattdessen der **Wegweiser** als produktnähere Richtung gewählt und
> implementiert. Maßgeblich für die gebaute Variante sind
> `design-06-DESIGN.md`, `design-06-CRITIQUE.md` und `design-06-AUDIT.md`;
> das Musterbuch bleibt als dokumentierte Alternative erhalten.

# Design 6 – Technische Analyse und Gestaltungskonzepte

Stand: 16. November 2026  
Projekt: GHSE Emmendingen, Hugo-Website  
Arbeitsstand: `main`, HEAD `7ad5bea`, vor der ersten Design-6-Änderung

---

## 1. Technischer Architekturbericht

### 1.1 Projektstand

| Punkt | Befund |
| --- | --- |
| Repository | `github.com/MaximilianHertenstein/ghse_website_prototyp` |
| Branch | `main`, HEAD = `origin/main` = `7ad5bea` |
| Arbeitsverzeichnis vor Beginn | sauber, keine offenen Änderungen |
| Hugo | 0.169.0 extended |
| Build | erfolgreich: 88 Seiten, 460 statische Dateien, 4 Non-Page-Dateien |
| Inhalte | 131 Markdown-Dateien, 35 Layout-Dateien |
| CSS | 5 Dateien, zusammen 10.750 Zeilen |
| Schriften | 5 Theme-Ordner unter `assets/fonts/`, alle selbst gehostet |

### 1.2 Die fünf Bestandsdesigns

| Design | ID | CSS | Schriften | Standard |
| --- | --- | --- | --- | --- |
| Neobrutalismus | `neobrutalismus` | in `main.css` | Inter | nein |
| Klar | `klar` | `klar.css` | Roboto, Poppins | nein |
| Funktional | `funktional` | `funktional.css` | Hanken Grotesk | **ja** |
| Modern | `modern` | `modern.css` | Familjen Grotesk | nein |
| Lesebuch | `lesebuch` | `lesebuch.css` | Public Sans | nein |

Die Reihenfolge in `params.designs` ist Neo, Klar, Funktional, Modern,
Lesebuch. `params.design = "funktional"` ist die Auswahl ohne gespeicherte
Wahl. Der Kommentar in `hugo.toml` spricht noch von „vier
Gestaltungsvarianten“; das ist ein reiner Dokumentationsdrift, kein
funktionaler Fehler. Er wird nicht im Zuge von Design 6 korrigiert, weil
`hugo.toml` außerhalb des neuen Design-Eintrags unverändert bleiben soll.

### 1.3 Designschalter und Datenfluss

1. `hugo.toml` registriert die Designs über `params.designs` mit `id`,
   `name`, `kurz`, optional `css` und `fonts`.
2. `layouts/baseof.html` liest die Optionen als Meta-Tag, setzt
   `data-design` am `<html>` **vor dem ersten Bild** und lädt die CSS-Dateien
   aller registrierten Designs mit `resources.Get | minify | fingerprint`.
3. Die aktive Variante wird über `?design=<id>`, `localStorage`
   (`ghse-design`) oder den Standard bestimmt. `?design=` speichert nicht.
4. `layouts/_partials/stilwahl.html` erzeugt automatisch ein natives
   `<select>` – zweimal, für Leiste und Mobilmenü. Es gibt keinen
   zusätzlichen Schalter.
5. `assets/js/design.js` setzt `data-design`, speichert die Wahl, entfernt
   `?design` nach einer bewussten Wahl und synchronisiert beide Felder.
6. Der Hell-/Dunkelmodus läuft unabhängig davon über `ghse-theme`,
   `data-theme` und `assets/js/nav.js`; das frühe Inline-Skript in
   `baseof.html` verhindert das Aufblitzen.
7. `layouts/_partials/theme-button.html` liefert die beiden
   Modusschaltflächen; die Logik liegt in `nav.js`.

Für Design 6 ist **keine Änderung an diesem System nötig**. Ein Eintrag in
`params.designs`, eine CSS-Datei und bei eigener Schrift ein Schrift-Partial
genügen. Templates, `baseof.html`, `stilwahl.html`, `design.js` und `nav.js`
bleiben unangetastet.

### 1.4 Geschützte Dateien und Ausgangsstand

Der Ausgangsstand ist mit `qa/design6-guard.py --neu` eingefroren:

- **699 Dateien** unter `assets/`, `layouts/`, `content/` und `static/`
  sind per SHA-256 geschützt.
- `hugo.toml` wird semantisch geprüft: alles außerhalb `params.designs`
  muss gleich bleiben; die fünf bestehenden Einträge müssen unverändert
  und in derselben Reihenfolge stehen; höchstens ein zusätzlicher Eintrag
  `design-06` ist erlaubt.
- Der Guard akzeptiert vor der Implementierung fünf Designs und nach der
  Implementierung sechs. Er ist die autoritative Prüfung für Design 6.
- Die vorhandenen Guards `qa/theme-guard.py` (681 Dateien, Stand `8a9a82a`)
  und `qa/theme5-guard.py` (692 Dateien, Stand `3aa9a4c`) laufen weiter.
  `theme5-guard.py` erwartet heute genau einen Zusatz-Eintrag
  (`lesebuch`); nach Design 6 muss seine Erwartung minimal um
  `design-06` erweitert werden. Das ist eine additive Erweiterung, keine
  Abschwächung der Dateiprüfungen. Der neue Guard deckt zusätzlich alle
  Dateien ab, die nach dem Theme-5-Stand entstanden sind.

**Referenzaufnahmen:** 150 PNG-Dateien unter
`/tmp/opencode/design6/refs` – 5 Designs × 5 Seiten × 3 Breiten
(1440/768/390) × hell/dunkel, mit SHA-256-Manifest. Seiten: Startseite,
Schulartenübersicht, Technisches Gymnasium, News, Downloads. Aufgenommen mit
reduzierter Bewegung, geladenen Schriften und Bildern, festem Viewport.

### 1.5 Vorhandene QA

| Werkzeug | Zweck | Auswirkung von Design 6 |
| --- | --- | --- |
| `qa/theme-guard.py` | 681 Dateien vor Theme 5 | unverändert lauffähig |
| `qa/theme5-guard.py` | 692 Dateien, 4 Designs + Lesebuch | Erwartung um genau einen Eintrag erweitern |
| `qa/design6-guard.py` | 699 Dateien + 5 Designs, neuer Schutzstand | neu, autoritativ |
| `qa/themes.py` | 5 Varianten × 5 Seiten × 5 Breiten | Liste um `design-06` erweitern |
| `qa/design.py` | Umschalter, Standard, Speicherung | Optionsliste um `design-06` erweitern |
| `qa/themebilder.py` | Referenzaufnahmen 5 Varianten | Liste optional um `design-06` erweitern |
| `qa/reflow.py` | alle Seiten × 11 Breiten | mit `--design design-06` prüfbar |
| `qa/layout.py` | Anker, Sprungleiste, Touch-Ziele | unverändert nutzbar |
| `qa/linkcheck.py` | interne/externe Links | unverändert nutzbar |
| `qa/kontrast.py`, `qa/kontrast_klar.py` | Kontraste Neo/Klar | unverändert; Design 6 braucht eigene Messung |

Kein vorhandener Test wird entfernt oder in seiner Prüftiefe abgeschwächt.
Design 6 bekommt zusätzlich einen Isolationstest für die neue CSS-Datei:
jeder Selektor unter `:root[data-design="design-06"]`, keine globalen
Variablen, keine Kollision bei Keyframes oder Schriftnamen.

### 1.6 Minimale Erweiterung für Design 6

Geplant sind ausschließlich neue, eindeutig zugeordnete Dateien:

```text
assets/css/design-06.css
assets/fonts/design-06/…              (nur falls die Schrift neu ist)
layouts/_partials/schriften-design06.html
design-06-DESIGN.md
qa/design6-guard.py                   (bereits angelegt)
qa/design6-baseline.json              (bereits angelegt)
qa/design6-isolation.py               (Isolationstest)
design-06-konzepte/…                  (nur Konzept, nicht Produktion)
```

In `hugo.toml` kommt genau ein Eintrag hinzu:

```toml
[[params.designs]]
  id = "design-06"
  name = "Musterbuch"
  kurz = "Muster"
  css = "css/design-06.css"
  fonts = "schriften-design06.html"
```

Die bestehende Reihenfolge, alle alten Einträge und
`params.design = "funktional"` bleiben unverändert.

### 1.7 Risiken

| Risiko | Gegenmaßnahme |
| --- | --- |
| CSS-Leck in die fünf Bestandsdesigns | Jede Regel unter `:root[data-design="design-06"]`; Isolationstest; Pixelvergleich |
| Unvollständiger Dark Mode | vollständiger Token-Satz für hell und dunkel; `data-theme` und `prefers-color-scheme` testen |
| Shared Templates werden verändert | Design 6 ist CSS-only; jede nötige Strukturänderung wird vorher vorgelegt und gestoppt |
| Schriftlizenz / Ladezeit | SIL-OFL-Schrift selbst hosten, Lizenz mitliefern, `font-display: swap`, kein Preload |
| Bestehende Tests brechen | additive Listen-Erweiterung; neue Guards; alte Prüftiefe bleibt |
| Screenshot-Vergleich durch Fonts/Bilder verfälscht | reduzierte Bewegung, `fonts.ready`, Bilder laden, fester Viewport, SHA-256 |
| `theme5-guard.py` erwartet fünf Designs | minimal um `design-06` erweitern; neuer Guard ist maßgeblich |
| Konzept wird dekorativ statt lesbar | echte Texte, echte Fotos, echte Dateidaten; keine erfundenen Muster-Nummern als Inhalt |

### 1.8 Was Design 6 nicht tut

- Keine Änderung an den fünf bestehenden CSS-Dateien.
- Keine Änderung an Layouts, Partials, Inhalten, Bildern oder JavaScript.
- Keine neue Navigation, keine neue Auswahlmechanik, keine neue Speicherung.
- Keine neuen Inhalte, keine erfundenen Zahlen, keine Stockfotos.
- Kein Commit, kein Push, kein Deployment ohne ausdrücklichen Auftrag.
- Keine Implementierung vor der ausdrücklichen Freigabe.

---

## 2. Produktkontext

Die Website ist der öffentliche Eingang einer Schule, unter deren Dach alle
Abschlüsse möglich sind: Hauptschulabschluss, mittlere Reife,
Fachhochschulreife, Abitur, Berufsausbildung, Berufsvorbereitung und Pflege.
Acht Schularten, 27 Richtungsseiten, 49 Downloads, 10 Meldungen und 18
Service-Seiten teilen sich eine Struktur.

Die primäre Zielgruppe sind **Jugendliche am Ende der Sekundarstufe I und
ihre Eltern**. Sie kommen mit einer konkreten Frage: *Welcher Weg passt zu
mir, und was muss ich dafür tun?* Die zweite Gruppe ist die Schulgemeinschaft:
Sie braucht Krankmeldung, Stundenplan, Vertretungsplan und Unterlagen ohne
Umweg. Ausbildungsbetriebe und Partner beurteilen die Schule von außen.

Der erste Bildschirm muss deshalb vor allem **Bildungswege zeigen**. Die
Startseite ist die entscheidende Fläche; die Detailseiten müssen die Tiefe
tragen, ohne unruhig zu werden.

---

## 3. Die geprüften visuellen Welten

Vor dem Roll wurden sieben konkrete visuelle Systeme aus der Lebenswelt der
Schule entwickelt, geordnet nach Resonanz. Keine ist eine Palette auf einem
Template; jede bringt eine eigene räumliche Ordnung mit.

| # | Welt | Warum sie trägt | Wie sie aussieht | Familie |
| --- | --- | --- | --- | --- |
| 1 | **Wegweiser** – Beschilderung des Schulgebäudes | Jede Besucherin versteht „Sie stehen hier“ sofort; das Gebäude mit dem gelben Übergang ist das stärkste Ortsbild | Tiefblauer Wandverlauf, weiße Emailschilder, gelbe Pfeile, RaumNummern, Verzeichnistafel | Architektur / Signage |
| 2 | **Zeugnis** – Urkunde und Abschlussdokument | Die Schule vergibt Abschlüsse; das Dokument ist der emotionale Kern | Warmes Papier, eingravierte blaue Linien, gelbes Siegel, Guillochen, Tabellen | Amt / Dokument |
| 3 | **Werkstatt-Plakat** – Sicherheits- und Anleitungsplakat | Werkstätten, Pflege und Technik teilen die Sprache der klaren Anweisung | Gelb-schwarze Bänder, Piktogramme, Nummern, Stahlblau, kondensierte Grotesk | Industrie / Anleitung |
| 4 | **Stundenplan** – Stunden- und Vertretungsplan | Der Alltag jeder Schülerin und jedes Schülers; Farbe als Fachcode | Zeitraster, farbige Blöcke, RaumNummern, Magnete, tabellarische Ziffern | Alltag / Raster |
| 5 | **Musterbuch** – Werkstoffmuster und Materialbibliothek | Die Schule bearbeitet Stoffe und Menschen; ein Musterbuch zeigt die ganze Breite als greifbare Sammlung | Blaues Register, Papierkarten, Materialkanten, MusterNummern, Spezifikationsetiketten | Material / Sammlung |
| 6 | **Berichtsheft** – Ausbildungsnachweis | Das duale System ist ein prägendes Stück der Schule | Kariertes Papier, blauer Umschlag, Stempel, Wochenzeilen, Handschrift | Buchführung / Ausbildung |
| 7 | **Schaufenster** – Werkstattauslage | Die Schule zeigt, was entsteht; das Fenster ist ein Ort des Zeigens | Glas, Rahmen, Spotlicht, Preisschilder, warmes Holz, blaues Rückfeld | Ausstellung / Handel |

Die Kategorie liefert immer dieselbe Seite: ein großes Foto, eine
Willkommenszeile, vier Karten, News, Service, Fuß. Die Vorhersagbare
Gegenbewegung ist die geschönte Privatschule mit Stockfoto und
„Entdecke dein Potenzial“ oder die Behördenliste mit Logo und Links. Beides
wurde bewusst ausgeschlossen.

**Der Roll** hat aus dieser Liste die fünfte Welt zugewiesen:
**Musterbuch**. Die Zuweisung ist keine Empfehlung, sondern der bewusste
Gegenschnitt zur naheliegendsten Lösung. Die Reihenfolge bleibt ehrlich:
Wegweiser und Zeugnis sind für Eltern unmittelbarer lesbar; das Musterbuch
ist die eigenständigere, weniger erwartbare Welt.

---

## 4. Zugewiesene Richtung: Musterbuch

### 4.1 Idee

**Die GHSE als Musterbuch ihrer Arbeitsfelder.** Ein Musterbuch ist kein
Katalog und keine Broschüre. Es ist ein Register aus greifbaren Proben:
Jede Probe hat eine Nummer, einen Werkstoff, eine Herkunft, eine
Eigenschaft und eine Verwendung. Die Schule ist genauso: acht Felder, die
man nicht abstrakt beschreiben kann, sondern zeigen muss – Metall, Holz,
Elektro, Fahrzeug, Ernährung/Textil, Pflege, Wissen, Ankommen.

Blau ist der **Einband und das Register**, Papier ist die **Seite**, Gelb und
Orange sind die **Materialkanten und Signalmarken**. Die Startseite ist das
aufgeschlagene Musterbrett: das Schulgebäude als Probe 00, die fünf
Abschlüsse als Griffregister, die Schularten als Musterkarten. Die
Innenseiten sind Spezifikationsblätter: ruhige Lesespalte, klare Etiketten,
echte Fotos, echte Dateidaten.

Das ist keine weitere Karten-Website. Die Karte ist hier ein **Muster**:
gelocht, etikettiert, mit Kante, Nummer und Herkunft. Die Startseite ist
kein Split-Hero mit Kartenreihe, sondern ein **Brett**, auf dem die Schule
liegt.

### 4.2 Farbwelt

Die vier Originalfarben bleiben unverändert und sind die Anker:

| Rolle | Original | Verwendung |
| --- | --- | --- |
| GHSE Dunkelblau | `#222D71` | Einband, Register, Überschriften, Primärflächen |
| GHSE Blau | `#006AB4` | Verlaufspol, Links, aktive Flächen, Fokus auf Papier |
| GHSE Orange | `#EE7330` | Materialkante, „Sie sind hier“, Signal, Hover |
| GHSE Gelb | `#F6DC56` | Griffregister, Etiketten, Fokus auf Blau, Marke |

Erweitertes Blauspektrum (abgeleitet, dokumentiert):

| Token | Wert | Verwendung |
| --- | --- | --- |
| `--d6-blue-950` | `#080F26` | tiefster Grund, Dunkelmodus |
| `--d6-blue-900` | `#101A4A` | Einbandgrund, Kopfleiste |
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

Papier und Tinte:

| Token | Hell | Dunkel | Verwendung |
| --- | --- | --- | --- |
| `--d6-paper` | `#F4F1E8` | `#0C1220` | Seitengrund |
| `--d6-paper-2` | `#E9E4D6` | `#111A2C` | Bänder, Register |
| `--d6-card` | `#FBF9F2` | `#131C2E` | Musterkarten, Etiketten |
| `--d6-ink` | `#14171C` | `#F2EFE6` | Text, Überschriften |
| `--d6-ink-soft` | `#4B5058` | `#B9C3D6` | Zweittext, Daten |
| `--d6-line` | `#C9C2B2` | `#2A3852` | Haarlinien, Rahmen |
| `--d6-line-strong` | `#A39A86` | `#3B4C6B` | bedienbare Ränder |

Akzente und Funktion:

| Token | Hell | Dunkel | Verwendung |
| --- | --- | --- | --- |
| `--d6-orange` | `#EE7330` | `#EE7330` | Materialkante, Signal |
| `--d6-orange-text` | `#A8430F` | `#F09A6B` | Orangetext mit AA |
| `--d6-yellow` | `#F6DC56` | `#F6DC56` | Griffregister, Fokus auf Blau |
| `--d6-yellow-soft` | `#FBEFA8` | `#3A3316` | Hinweisfläche |
| `--d6-success` | `#1F6B45` | `#7FD3A8` | Erfolg |
| `--d6-warning` | `#8A4B00` | `#F3B562` | Warnung |
| `--d6-danger` | `#A32A1A` | `#F09A8C` | Fehler |

**Verläufe** (nur dort, wo sie Hierarchie tragen, nie hinter Fließtext ohne
Kontrastprüfung):

```css
--d6-binder: linear-gradient(135deg, #101A4A 0%, #18245C 26%,
             #222D71 50%, #174C96 76%, #006AB4 100%);
--d6-binder-dark: linear-gradient(135deg, #070D1C 0%, #0B1638 40%,
                  #10254D 100%);
--d6-band: linear-gradient(90deg, #222D71 0%, #006AB4 62%,
            #EE7330 100%);
```

Der Binder-Verlauf trägt den Hero, den Fuß und die Primäraktion. Das
schmale Band `--d6-band` erscheint nur als 4–8 px starke Kante an
Abschnittswechseln, nie als Textgrund. Kein Regenbogen, kein Glow.

### 4.3 Typografie

**Archivo** (variabel, `wght 100–900`, `wdth 62–125`, SIL OFL,
selbst gehostet). Eine einzige Familie mit zwei Achsen:

| Rolle | Schnitt | Größe | Zeile | Einsatz |
| --- | --- | --- | --- | --- |
| Display / H1 | 800, `wdth 118` | `clamp(3.2rem, 6vw, 5.2rem)` | 0,94 | Startseite, Seitenkopf |
| H2 | 800, `wdth 112` | `clamp(2rem, 3.4vw, 2.9rem)` | 1,0 | Abschnitte |
| H3 | 700, `wdth 106` | 1,15–1,45 rem | 1,08 | Musterkarten |
| Fließtext | 400, `wdth 100` | 1,0625 rem | 1,65 | Lesespalte |
| Labels | 700, `wdth 100` | 0,6875 rem | 1,4 | Etiketten, Register |
| Daten | 600, tabellarisch | 0,8125 rem | 1,4 | Datum, Größe, Nummer |

Die Breitenachse ist der eigentliche Charakter: displayweit und
registereng, ohne zweite Schrift. Fallback:
`"Archivo", "Arial Narrow", "Helvetica Neue", Arial, sans-serif`.
Kein externer Font-Dienst, `font-display: swap`, kein Preload.

### 4.4 Erster Bildschirm

**Das Musterbrett.** Kein zentriertes Hero, kein Text-Bild-Split mit
Kartenreihe darunter.

- **Grund:** der Binder-Verlauf, darüber ein feines 48-px-Messraster, das
  nach links und rechts ausblendet.
- **Links (6 Spalten):** eine schmale Papierzeile mit dem Schulnamen;
  darunter die H1 „Wir machen Schule für alle“ in displayweitem Archivo,
  dreizeilig; der Leitsatz; die Terminnotiz als Papierzettel mit oranger
  Kante; die fünf Abschlüsse als Griffregister (Papieretiketten mit
  farbigem Quadrat, 42–44 px hoch). Das Wort „Musterbuch“ steht im
  Umschalter; die Komposition trägt die Idee, kein zusätzliches Etikett.
- **Rechts (6 Spalten):** das Schulgebäude als **Musterplatte 00** – ein
  Papierbogen mit Lochung, 4:3-Foto, gelber Kante und einer Bildzeile
  „Muster 00 · Schulgebäude / Jahnstr. 12–14“. Der Bogen sitzt leicht
  versetzt auf dem Brett, ohne Drehung, ohne weichen Schatten.
- **Fuß des Bretts:** „Muster 01–08 · Werkstätten, Pflege, Gymnasium,
  Berufsschule“ und „Register ↓“; darunter die Papierseite mit dem
  Schularten-Register.
- **Primäre Handlung:** die fünf Abschlussmarken sind echte Links; die
  erste sichtbare Aktion ist „Hauptschulabschluss“, die stärkste ist
  „Abitur“. Die zweite Aktion ist „Alle Schularten“ im Register darunter.
  Es wird keine neue Funktion erfunden; die vorhandenen Links tragen die
  Handlung.

Auf 390 px: Schulname, H1, Leitsatz, Terminnotiz, Griffregister, dann die
Musterplatte. Die Platte beginnt noch im ersten Bildschirm; der Fold zeigt
Foto und Kante, nicht nur Text.

### 4.5 Seitenarchitektur

| Seite | Umsetzung |
| --- | --- |
| Startseite | Musterbrett, Register der vier gezeigten Schularten, Instagram als „Ansichtskarten“, Aktuelles als „Notizen“, Termine als blaues Registerband, Service als „Merkblätter“, Schulleben als „Tafeln“, Partner als „Nachweise“, Fuß als „Register“ |
| Schulartenübersicht | zwei Schubladen (Vollzeit/Teilzeit), Gruppenkopf als Registerlasche mit Anzahl, Musterkarten mit Kategoriekante |
| Schulart-Detailseite | Spezifikationsblatt: Brotkrumen als Wegzeile, H1 als MusterName, Lead als Eigenschaftstext, Lesespalte 68ch, Sidebar als gelbes Spezifikationsetikett, Galerie als Tafeln, Downloads als Anlagen |
| News | Notizen mit Datum/Source-Stempel; Bildkarten als blauer Block mit gelber Oberkante, Textkarten als Papierzettel |
| News-Detail | Artikelblatt mit blauem Kopf, Zeitungsausschnitt-Etikett, Bildtafeln mit captions, Quellenzeile |
| Downloads | Registerleiste als blaue Schublade, Zeilen als Dokumente mit Format/Größe-Etikett und klarem Download |
| Service / Themenseiten | Lesespalte auf Papier, Hinweise als Merkblätter, Tabellen als Spezifikationstabellen |
| 404 | leeres Registerblatt mit Weg zurück |

### 4.6 Komponenten

- **Musterkarte:** Papier, 1-px-Linie, Lochung oben, Materialkante links
  (Gelb = Vollzeit, Orange = Teilzeit), Kategorieetikett, Titel, Text,
  „Muster ansehen“ mit Pfeil. Hover: 4 px anheben, Kante wächst, Pfeil
  wandert; `prefers-reduced-motion` schaltet die Bewegung ab.
- **Musterplatte:** Papierbogen, 12 px Rand, 1-px-Linie, gelbe Kante,
  Bildzeile; kein Schatten, keine Drehung.
- **Griffregister:** Papieretiketten mit farbigem Quadrat; 44 px hoch;
  Hover Gelb; Fokus 3 px Orange auf Papier, 3 px Gelb auf Blau.
- **Terminnotiz:** Papier, orange Kante, Datum in displayweiter Schrift,
  kleine Zeile „Nächster Termin“.
- **Spezifikationsetikett:** gelbe Karte mit blauem Kopf, Faktenzeile,
  Kontaktzeile, Lochung; die Sidebar der Schulartseite.
- **Dokumentzeile:** Papierzeile, links Format/Größe, Mitte Titel und
  Beschreibung, rechts Download; keine Tabelle, keine Karte.
- **Notizkarte:** blauer Block für Bildmeldungen, Papier für Textmeldungen;
  Datum und Quelle als Stempelzeile.
- **Registerleiste:** kleine Überschrift, Haarlinie, Anzahl; keine
  Versalienflut.
- **Fuß:** Binder-Verlauf, vier Papierspalten, gelbe Titel, weiße Links,
  gelbe Oberkante.

### 4.7 Interaktion und Zustände

- Ein einziges Bewegungsmuster: **die Probe wird angehoben**. 4 px, 180 ms,
  ease-out; Kante 4→8 px; Pfeil 4 px. Keine Scroll-Animation, kein Parallax,
  kein Auto-Play.
- Fokus: 3 px Orange mit 2 px Offset auf Papier; 3 px Gelb auf Blau.
  Nie nur ein Farbwechsel.
- Hover: Fläche wechselt auf Gelb oder Kante wächst; Text bleibt lesbar.
- Aktiv/aktuell: gelbe Registerlasche, blaue Schrift; `aria-current`
  bleibt unangetastet.
- Dark Mode: gleiche Regeln, aber Papier wird tiefes Blaugrau, Tinte warmes
  Weiß, die Kante bleibt gelb/orange; Text auf Gelb bleibt dunkel.
- Reduced Motion: alle Transforms und Übergänge aus; Zustände bleiben über
  Farbe, Rand und Text sichtbar.
- Tastatur: die vorhandene Reihenfolge bleibt; keine visuelle Umordnung,
  die von der DOM-Reihenfolge abweicht.

### 4.8 Responsive Regeln

| Breite | Verhalten |
| --- | --- |
| ≥ 1200 px | volle Kopfzeile, Hero 6/6, Register 2 Spalten, Sidebar 300 px |
| 900–1199 px | Kopfzeile bricht in das vorhandene Menü; Hero 1 Spalte, Platte max. 640 px; Register 2 Spalten |
| 640–899 px | Register 1 Spalte, Karten volle Breite; Sidebar wandert vor den Text (vorhandenes Markup) |
| ≤ 639 px | kompakter Kopf, H1 `clamp(2.9rem, 14vw, 4.2rem)`, Griffregister umbrechen, Platte volle Breite, keine Überläufe bei 320 px |
| ≤ 400 px | Beschriftungen 0,625 rem, aber nie unter 14 px für Fließtext; Ziele bleiben 44 px |

### 4.9 Barrierefreiheit

- Kontraste werden mit `qa/themes.py` und einem neuen Design-6-Kontrastlauf
  in beiden Modi geprüft; Richtwerte: Tinte/Papier ≥ 12:1,
  Zweittext/Papier ≥ 7:1, Weiß/Navy ≥ 10:1, Weiß/Blau ≥ 5:1,
  Gelb/Navy ≥ 8:1, Tinte/Gelb ≥ 12:1.
- Orange `#EE7330` wird nicht für kleinen Fließtext verwendet; dafür
  `#A8430F` (hell) bzw. `#F09A6B` (dunkel).
- Fokusringe auf allen Flächen, auch auf dem Verlauf; nie `outline: none`
  ohne Ersatz.
- Keine Information nur über die Materialkante; die Kategorie steht als
  Text im Etikett.
- Die Lochung und die Messraster sind rein dekorativ; sie tragen keine
  Bedeutung.
- Echte `alt`-Texte bleiben; die Bildzeile ist eine zusätzliche visuelle
  Beschriftung, keine Ersatzbeschreibung.
- Reduced Motion, `text-wrap: balance`/`pretty`, `hyphens: auto` im
  Fließtext; keine automatischen Bewegungen.
- Die vorhandene Sprungmarke, Menülogik, `aria-expanded`, `aria-current`
  und der Modusschalter bleiben unverändert.

### 4.10 Abgrenzung zu den fünf Bestandsdesigns

| Bestand | Was Musterbuch bewusst nicht übernimmt |
| --- | --- |
| Neo | keine schwarzen Konturen, keine harten Versätze, keine Sticker, kein Gelb als ganze Fläche |
| Klar | kein hellblaues Weißraum-Raster, keine runden Karten, keine Roboto/Poppins |
| Funktional | kein Schwarzweiß-Handbuch, keine 1-px-Kästen ohne Material, keine Inter/Hanken |
| Modern | keine weißen Karten auf hellem Blau, keine weichen Schatten, keine Familjen Grotesk |
| Lesebuch | keine Serif, kein fester linker Rücken, kein Buchrücken, keine Papier-Graugrün-Stimmung |

Die Eigenständigkeit liegt in der **Sammlungslogik**: ein blaues Register,
Papierproben, Materialkanten, Lochungen und Spezifikationsetiketten. Auf den
ersten Blick unterscheidet sich das von allen fünf durch das Musterbrett und
die displayweite Archivo-Schrift.

### 4.11 Ehrliche Risiken

- **Die Metapher kann kippen.** Musterkarten, Lochungen und Nummern sind
  schnell Dekoration. Sie funktionieren nur, wenn sie echte Kategorien,
  echte Fotos und echte Dateidaten tragen. Keine erfundenen „Muster 07“-
  Nummern als Inhalt; die Nummern sind reine Ordnung.
- **Die Materialkante kann zum Systemzwang werden.** Nicht jede Karte
  braucht eine andere Farbe. Zwei Kategorien (Vollzeit/Teilzeit) reichen;
  Gelb und Orange sind die einzigen Kanten.
- **Die warme Papierfläche kann bieder wirken.** Die displayweite Archivo,
  das Messraster und der harte blaue Einband halten dagegen. Kein Creme-
  Nostalgie-Look, keine Serif.
- **Der Kontrast auf dem Verlauf.** Text steht nur auf dem dunklen Teil des
  Verlaufs oder auf Papier; die hellen Verlaufszonen tragen keine kleine
  Schrift.
- **Die Startseite ist voll.** Schulname, H1, Leitsatz, Termin, fünf
  Abschlüsse und ein großes Foto. Das ist gewollt, aber es muss auf 390 px
  klar bleiben; die Skizze zeigt, dass es funktioniert, wenn der Schulname
  als schmale Zeile und nicht als großer Kasten erscheint.

---

## 5. Die Alternative: Wegweiser (Impeccable’s Pick)

**Welt:** die Beschilderung des Schulgebäudes. Das Gebäude mit dem gelb
markierten Übergang ist das stärkste Ortsbild der GHSE; ein Wegweiser ist
die direkteste Antwort auf „Wo bin ich, und wo muss ich hin?“.

**Erster Bildschirm:** eine tiefblaue Wand mit weißen Emailschildern. Links
das „Sie stehen hier“-Panel mit Schulname, H1, Leitsatz und den fünf
Abschlüssen als Zielzeilen; rechts das Gebäude als Sichtfenster; darunter
das Verzeichnis der Schularten als echte Tafel. Ein gelber Pfeil verbindet
„Sie stehen hier“ mit dem Verzeichnis. Die Skizze zeigt acht Ziele; das
vorhandene Markup hat auf der Startseite vier Karten und auf `/schularten/`
alle acht. Die Umsetzung nutzt die vier vorhandenen Karten als Ziele und
verlinkt auf das vollständige Verzeichnis – dafür ist keine Template-
Änderung nötig.

**Typografie:** Archivo in normaler Breite, Versalien für Schilder,
tabellarische Ziffern für Raum- und Datumsangaben. Keine displayweite
Schrift; die Schilder tragen die Ordnung.

**Farben:** derselbe GHSE-Blauverlauf, aber Weiß und Gelb dominieren die
Flächen; Orange markiert „Sie stehen hier“. Das ist näher an der
Alltagssprache der Schule und sofort lesbar.

**Stärken:** höchste Orientierungsleistung; Eltern verstehen die fünf
Abschlüsse und die acht Wege ohne Erklärung; das Gebäude ist ein echter,
lokaler Anker; die Skizze funktioniert auf 390 px sehr gut.

**Risiken:** Wegweiser ist für Schulen naheliegend und kann wie ein
Behörden- oder Verkehrssystem wirken. Die Wärme muss aus den echten Fotos
und der Typografie kommen, nicht aus Dekoration. Die Verzeichnistafel darf
nicht zu einer gewöhnlichen Linkliste werden.

**Warum als Pick:** Es ist die Richtung mit der höchsten unmittelbaren
Lesbarkeit für die primäre Zielgruppe und der stärksten lokalen Bindung.
Sie ist weniger eigenständig als das Musterbuch, aber sie ist die sichere
Wahl, wenn die Startseite vor allem Klarheit leisten soll.

---

## 6. Challenger-Verdicts

Die sechs vom Roll gedealten Fremdwelten wurden mit der GHSE verschmolzen
und an zwei Achsen gemessen: **Identifikation der Zielgruppe** und
**Klarheit des Produkts**. Keine hat beide Achsen gewonnen.

| Challenger | Verdikt | Begründung | Übernommene Disziplin |
| --- | --- | --- | --- |
| Jacquard-Brokat aus Lochkarten | declined | Textil-/Modewelt, nicht die Breite der Schule; das Gewebe erklärt keine acht Schularten | strenge Zeilenlogik, tiefer Mitternachtsgrund, Gelb als Struktur statt Streuung |
| Irisierende Wolkenkante | declined | zu ätherisch, zu blass, zu weit von der Arbeitswelt; das Spektrum bleibt eine Metapher | ein durchgehendes Spektralband für die Abschlussleiter |
| Seedbed-Lobes (grüne Fläche, weiße Kapseln) | declined | bekannte Startup-Anmutung; junge Zielgruppe ja, GHSE-Breite nein | eine gesättigte GHSE-Blaufläche, auf der die Papieretiketten schweben |
| Gereister Pass | declined | Reisemetapher muss erklärt werden; Burgund/Gold liegt neben der GHSE-Welt | kumulative Einträge und amtliche Marken für die Abschlussleiste |
| Dunkelkammer-Belichtungsprotokoll | declined | Operate-Werkzeug als Kostüm; Fotografie ist kein GHSE-Feld | Tonleiter und Schraffur als Hierarchie ohne Farbe |
| Nixie-Röhrenzähler | declined | Tech-Kostüm, dunkel glühend, schließt Pflege und Gymnasium aus | feste Datenpositionen und tabellarische Ziffern |

Die abgelehnten Welten werden nicht als vollwertige Karten geführt; ihre
Disziplin ist in das Musterbuch eingewandert. Nichts davon ist als Motiv
kopiert.

---

## 7. Empfehlung

**Ich empfehle das Musterbuch.**

Begründung:

1. **Es erzählt die GHSE, nicht eine Abteilung.** Die Schule ist gerade
   nicht nur Werkstatt, nicht nur Pflege, nicht nur Gymnasium. Die
   Materiallogik kann alle acht Felder gleichwertig zeigen, ohne ein Foto
   zum Gesicht der ganzen Schule zu machen.
2. **Es ist die eigenständigste Welt.** Wegweiser, Zeugnis und Stundenplan
   sind gute, aber erwartbare Schulmetaphern. Das Musterbuch hat eine
   eigene räumliche Ordnung: Brett, Probe, Kante, Etikett, Register.
3. **Es trägt die GHSE-Farben strukturell.** Der blaue Einband ist der
   Verlauf; Gelb und Orange sind Materialkanten und Griffregister, keine
   Dekoration. Die vier Originalfarben bleiben unverändert.
4. **Es funktioniert auf allen Seitentypen.** Die Startseite ist ein Brett;
   die Detailseite ist ein Spezifikationsblatt; News sind Notizen;
   Downloads sind Anlagen. Das System ist nicht nur ein Hero.
5. **Es bleibt lesbar.** Die Lesespalte ist ruhig, die Typografie eine
   einzige Familie mit zwei Achsen, die Farbe trägt Hierarchie, nicht
   Atmosphäre.

Die ehrliche Gegenprobe: Das Musterbuch ist am ersten Bildschirm weniger
selbsterklärend als der Wegweiser. Wer in fünf Sekunden nur „Welche
Schularten gibt es?“ beantworten will, findet beim Wegweiser schneller
hinein. Das Musterbuch belohnt den zweiten Blick und die längere
Beschäftigung; genau das ist bei einer Schule mit acht Wegen und 27
Richtungen die richtige Investition.

---

## 8. Entscheidung

Die Auswahl ist eine Richtungsentscheidung, **keine Implementierungsfreigabe**.
Nach der Wahl wird der Direction Contract geschrieben und erneut angehalten.

Mögliche Entscheidungen:

1. **Musterbuch** (zugewiesen, empfohlen)
2. **Wegweiser** (Impeccable’s Pick, die sichere Alternative)
3. **Eine verworfene Richtung trotzdem prüfen** (Zeugnis, Werkstatt-Plakat,
   Stundenplan, Berichtsheft oder Schaufenster)
4. **Neue Runde** (Re-Roll; alle bisher gezeigten Richtungen entfallen)
5. **Die bewährte Schulwebsite** (ruhige Tür, nicht empfohlen; erfüllt die
   geforderte Eigenständigkeit nicht)

Die Konzeptskizzen liegen unter `design-06-konzepte/`:
`musterbuch.html`, `wegweiser.html` und `shots/`.

---

## 9. Verfahrensnotiz

Der offizielle Impeccable-Direction-Roll wurde ausgeführt
(`concept-seed --scope direction --mode persuade`). Zugewiesen wurde
Kandidat 5 der eigenen, nach Resonanz geordneten Liste. Die
Seed-Referenz für den späteren Direction Contract lautet
`seed:260e25ab6884aefe`.

Die lokale Impeccable-Entscheidungsseite wurde nicht als blockierende
Browser-Seite gestartet; die Auswahl läuft über das strukturierte
Fragewerkzeug dieses Agenten. Die Konzeptkarten und Skizzen sind als
Dateien vorhanden. Das ist der im Workflow vorgesehene Fallback, kein
übersprungener Schritt.
