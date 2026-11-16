# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

**Primär (vom Auftraggeber bestätigt):** Jugendliche am Ende der Sekundarstufe I und ihre Eltern. Sie prüfen, welche Schulart, welcher Abschluss und welcher Weg zur GHSE passt – oft zum ersten Mal, oft auf dem Telefon, oft ohne Vorwissen über das deutsche Schulsystem.

**Weitere bestätigte Zielgruppen:** aktuelle Schülerinnen und Schüler, deren Eltern und Lehrkräfte (Service, Termine, Downloads, Krankmeldung), Ausbildungsbetriebe und Kooperationspartner (duale Ausbildung, Praxisphasen), Studieninteressierte sowie Besucherinnen und Besucher, die einzelne Themen wie UNESCO, Erasmus+ oder Schulentwicklung suchen.

## Product Purpose

Die Website macht die GHSE als eine Schule sichtbar, unter deren Dach alle Abschlüsse möglich sind: vom Hauptschulabschluss über die mittlere Reife und die Fachhochschulreife bis zum Abitur, dazu Berufsausbildung, Berufsvorbereitung und Pflege. Sie erklärt Bildungswege, stellt die Schularten und ihre Richtungen vor, beantwortet organisatorische Fragen und führt zu Anmeldung, Service und Downloads. Erfolg heißt: Eine Familie versteht in kurzer Zeit, welche Wege es gibt und welcher zu ihr passt; ein Mitglied der Schulgemeinschaft findet Krankmeldung, Stundenplan, Vertretungsplan und Unterlagen ohne Umweg.

## Positioning

Keine andere Schule der Region führt gewerbliche, hauswirtschaftliche, sozialpflegerische und gymnasiale Bildung in dieser Breite unter einem Dach. Diese Breite ist kein Nebeneffekt, sondern der eigentliche Wert: Acht Schularten und alle Abschlüsse an einem Ort, mit echten Werkstätten, Pflegepraxis und gymnasialer Oberstufe. Die Gestaltung muss diese Gleichzeitigkeit tragen, ohne einen einzelnen Fachbereich zum Gesicht der ganzen Schule zu machen.

## Operating Context

- Schulalltag mit Stundenplan, Vertretungsplan, Krankmeldung, Terminen und Downloads; die Website ist der öffentliche Eingang, nicht das Lernmanagementsystem.
- Schularten gliedern sich in Vollzeit- und Teilzeitschularten; die Berufsschule führt fünf Fachbereiche, die Pflege fünf Richtungen, die Gymnasien mehrere Laufbahnen.
- Inhalte stammen aus dem bestehenden Auftritt und werden redaktionell über Pages CMS gepflegt. Bilder sind echte GHSE-Aufnahmen, keine Stockmotive. Texte werden nicht neu erfunden.
- Die Website ist statisch mit Hugo gebaut und wird über GitHub Pages veröffentlicht. Es gibt keine Serverlogik, keine Anmeldung und keine Datenbank.
- Sechs Gestaltungsvarianten derselben Seiten und derselben URLs; die Auswahl ist eine reine Darstellungswahl und wird im Browser gespeichert.

## Capabilities and Constraints

- Hugo 0.169 mit gemeinsamen Layouts und Partials; Inhalte, URLs, Navigation, Formulare und Verlinkungen bleiben unverändert.
- Designvarianten werden über `params.designs` in `hugo.toml` registriert, über `data-design` am `<html>` aktiviert und über `localStorage` (`ghse-design`) sowie `?design=<id>` gewählt. Die Standardauswahl bleibt `funktional`.
- Neue Variante als zusätzliche CSS-Datei, deren Regeln ausschließlich unter `:root[data-design="design-06"]` stehen; Hell- und Dunkelmodus müssen vollständig definiert sein.
- Keine Änderung an den fünf bestehenden Designs, ihren CSS-Dateien, Layouts, Inhalten oder Assets.
- Schriften selbst hosten, keine externen Font-CDNs; Ladeverhalten und Fallbacks beachten.
- Ziel: WCAG 2.2 AA, Tastaturbedienbarkeit, sichtbare Fokuszustände, mindestens 24 × 24 px große Ziele (44 px für primäre Aktionen), kein horizontaler Überlauf von 320 bis 1440 px.
- Keine erfundenen Inhalte, Zahlen, Zitate oder Partner; keine neuen kommerziellen Versprechen.

## Brand Commitments

- Name: Gewerbliche und Hauswirtschaftlich-Sozialpflegerische Schulen Emmendingen, kurz GHSE Emmendingen.
- Das GHSE-Zeichen und die Wortmarke bleiben unverändert.
- Verbindliche GHSE-Farben: Dunkelblau `#222D71` (34, 45, 113), Blau `#006AB4` (0, 106, 180), Orange `#EE7330` (238, 115, 48), Gelb `#F6DC56` (246, 220, 86). Das Blauspektrum zwischen und um die beiden Blauanker ist frei nutzbar; die vier Originalwerte bleiben unverändert erhalten.
- Ton: sachlich, direkt, menschlich, ohne Werbesprache. Die Schule spricht über das, was sie tut, nicht über Superlative.
- Echte GHSE-Fotografie und das Schulgebäude mit dem gelb markierten Übergang sind zentrale, wiedererkennbare Assets.

## Evidence on Hand

- 88 gebaute Seiten mit echten Inhalten: Startseite, Schulartenübersicht, acht Schulart-Detailseiten mit 27 Richtungsseiten, Newsbereich mit 10 Meldungen und Zeitungsscans, 49 Downloads in sieben Kategorien, 18 Service- und Schülerseiten, UNESCO- und Erasmus+-Themenseiten.
- Echte Fotografien unter `static/bilder/` (Schulgebäude, Werkstätten, Pflege, Unterricht, Schulleben, Partnerlogos, Instagram-Beiträge).
- Fünf vollständige, funktionierende Gestaltungsvarianten als Vergleichs- und Abgrenzungsmaterial.
- Umfangreiche QA-Werkzeuge unter `qa/` (Kontrast, Layout, Reflow, Linkcheck, Theme-Schutz, Referenzaufnahmen).
- Keine erfundenen Testimonials, keine Benchmarks, keine erfundenen Ausbildungsbetriebe.

## Product Principles

1. **Die Breite zuerst.** Jede Gestaltung muss die Gleichzeitigkeit von Werkstatt, Pflege, Berufsschule und Gymnasium zeigen; kein Fachbereich darf die Schule allein vertreten.
2. **Der Weg ist das Produkt.** Besucherinnen und Besucher suchen keinen Katalog, sondern ihren nächsten Schritt. Bildungswege, Abschlüsse und Anschlüsse müssen schneller verständlich sein als die Organisation dahinter.
3. **Service ohne Reibung.** Krankmelden, Stundenplan, Vertretungsplan und Downloads sind keine Nebensache; sie müssen auch an einem hektischen Schultag in wenigen Sekunden erreichbar sein.
4. **Echte Schule, keine Kulisse.** Reale Fotografie, reale Texte, reale Menschen. Gestaltung darf inszenieren, aber nichts behaupten, was die Schule nicht ist.
5. **Ruhe trotz Größe.** Die Schule ist groß und vielseitig; die Website darf deshalb nicht laut werden. Hierarchie, Typografie und Rhythmus übernehmen die Orientierung.

## Accessibility & Inclusion

WCAG 2.2 AA ist verbindlich. Besonders zu beachten: Kontraste in beiden Farbmodi, sichtbare Fokusringe auf allen Flächen und Verläufen, vollständige Tastaturbedienung von Navigation, Untermenüs und Umschaltern, keine Information allein über Farbe, respektierte reduzierte Bewegung, lesbare Zeilenlängen und Schriftgrößen, keine horizontale Überlaufgefahr bei 320 px.
