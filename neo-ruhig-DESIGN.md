# GHSE – Gestaltungsvariante „Neo Ruhig“ (Theme 7)

Siebte Gestaltung derselben Website. Keine neue Designwelt, sondern die
ruhige Fassung von **Neobrutalismus**: gleiche Farben, gleiche Kontraste,
gleiche Schriften, gleiche Rahmen und Schatten – aber ohne jede Schräglage.

## 1. Konzept

Neobrutalismus ist laut, direkt und plakativ. Seine Unruhe entsteht weniger
durch Farbe oder Schrift als durch gekippte Flächen: schief stehende
Hero-Chips, ein gedrehtes Titelfoto, wechselnd geneigte Sticker und
Fotoreihen. „Neo Ruhig“ nimmt diese Kippungen heraus. Die Seite behält den
GHSE-Gelb/Orange/Blau-Kontrast, die schwarzen Konturen, die harten Schatten
und Inter – sie steht nur gerade.

Daraus folgen alle Entscheidungen:

- **Eine Ableitung, kein Gegenentwurf:** Die Variante erbt sämtliche Regeln
  aus `main.css`. Es gibt keine eigenen Farben, keine eigene Typografie und
  keine neuen Komponenten.
- **Nur Begradigung:** `assets/css/neo-ruhig.css` setzt ausschließlich
  `transform: none` für die vorher gedrehten Elemente. Jede Regel ist auf
  `:root[data-design="neo-ruhig"]` begrenzt.
- **Neobrutalismus bleibt unangetastet:** `main.css` und damit die Variante
  `neobrutalismus` werden nicht verändert. Beide sind getrennte Optionen im
  Umschalter.
- **Keine Serifenschrift:** Wie alle Varianten außer Lesebuch bleibt
  „Neo Ruhig“ serifenlos. Lesebuch behält Piazzolla und Public Sans.

## 2. Was geradegestellt wird

| Element | Vorher | Jetzt |
| --- | --- | --- |
| Akzent-Chip | −1,2° | 0° |
| Marken-Etikett | −1,5° | 0° |
| Hero-Schnellzugriffe | abwechselnd ±1,2° | 0° |
| Hero-Titelfoto | −1,2° | 0° |
| Instagram-Plaketten | −6°, +5°, −4° | 0° |
| Schulleben-Fotoreihe | abwechselnd ±1° | 0° |

Unverändert bleiben:

- die GHSE-Farbtokens und alle Kontrastwerte,
- Inter als einzige Schrift,
- Rahmen, harte Offset-Schatten, Versalien und Hover-Bewegungen,
- Raster, Abstände, Inhalte und Templates.

Der Pfeil im mobilen Menü dreht sich weiterhin um 180°, wenn ein Kapitel
aufklappt. Das ist eine Richtungsanzeige, keine Schräglage.

## 3. Technische Isolation

- Neue Datei `assets/css/neo-ruhig.css`; jede Regel beginnt mit
  `:root[data-design="neo-ruhig"]`.
- Keine Änderung an `main.css`, `klar.css`, `funktional.css`, `modern.css`,
  `lesebuch.css` oder `design-06.css`.
- Keine neue Schrift und kein Schrift-Partial; Inter wird bereits von
  `main.css` definiert.
- `hugo.toml` erhält ausschließlich einen weiteren `[[params.designs]]`-
  Eintrag am Ende der Liste.
- `qa/neo-ruhig-isolation.py` prüft, dass die Datei nur `transform: none`
  enthält und keine Fremdreferenzen oder Schriftüberschreibungen mitbringt.
- `qa/design6-guard.py` und `qa/theme5-guard.py` erlauben den neuen Eintrag
  additiv; alle bestehenden Dateien bleiben über Prüfsummen geschützt.

## 4. Qualitätssicherung

- `qa/themes.py` prüft alle sieben Varianten auf Überlauf und die neue
  Variante zusätzlich auf null Drehungen in allen getesteten Breiten.
- `qa/design.py` prüft Auswahl, Speicherung, Neuladen und `?design=…`.
- `qa/layout.py`, `qa/reflow.py` und `qa/linkcheck.py` laufen unverändert.
- Screenshots und Sichtprüfung: Startseite, Downloads, Schulart-Seite,
  News und 404 in hell und dunkel.
