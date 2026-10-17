// Mobile Navigation: Button schaltet das Menü, Escape und Klick auf einen
// Link schließen es wieder.
(function () {
  var btn = document.querySelector('[data-menu-button]');
  var nav = document.querySelector('[data-menu]');
  if (!btn || !nav) return;

  function setz(offen) {
    btn.setAttribute('aria-expanded', offen ? 'true' : 'false');
    nav.toggleAttribute('data-offen', offen);
    document.body.classList.toggle('menue-offen', offen);
  }

  btn.addEventListener('click', function () {
    setz(btn.getAttribute('aria-expanded') !== 'true');
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') {
      setz(false);
      btn.focus();
    }
  });

  nav.addEventListener('click', function (e) {
    if (e.target.closest('a')) setz(false);
  });

  window.addEventListener('resize', function () {
    if (window.innerWidth > 900) setz(false);
  });
})();

// Farbmodus-Umschalter: merkt sich die Wahl in localStorage ('ghse-theme')
// und setzt data-theme am <html>. Ohne gespeicherte Wahl folgt der Schalter
// dem System (prefers-color-scheme) – siehe Inline-Skript in baseof.html.
(function () {
  var knopf = document.querySelector('[data-theme-button]');
  if (!knopf) return;
  var text = knopf.querySelector('[data-theme-label]');

  function speicher(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }

  function merken(key, wert) {
    try { localStorage.setItem(key, wert); } catch (e) {}
  }

  function system() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function stelle(ziel, speichern) {
    document.documentElement.setAttribute('data-theme', ziel);
    if (speichern) merken('ghse-theme', ziel);
    knopf.setAttribute('data-ist', ziel === 'dark' ? 'dunkel' : 'hell');
    knopf.setAttribute('aria-pressed', ziel === 'dark' ? 'true' : 'false');
    if (text) text.textContent = ziel === 'dark' ? 'Hell' : 'Dunkel';
  }

  var gespeichert = speicher('ghse-theme');
  stelle(gespeichert === 'dark' || gespeichert === 'light' ? gespeichert : system(), false);

  knopf.addEventListener('click', function () {
    stelle(knopf.getAttribute('data-ist') === 'dunkel' ? 'light' : 'dark', true);
  });
})();

// Kopfhöhe zur Laufzeit messen. --kopfhoehe steuert scroll-margin-top und die
// Einrückung der Sprungleiste; der statische Token-Wert (7rem bzw. 4.5rem)
// entspricht aber keiner echten Kopfhöhe – die Nachtleiste hängt darunter,
// das Mobilmenü liegt als position:absolute außerhalb. Wird der Wert nicht
// gemessen, landen Ankersprungziele unter dem Kopf und sind dort verdeckt.
(function () {
  var kopf = document.querySelector('.kopf');
  if (!kopf) return;

  function setzeKopfhoehe() {
    document.documentElement.style.setProperty('--kopfhoehe', kopf.offsetHeight + 'px');
  }

  setzeKopfhoehe();
  window.addEventListener('resize', setzeKopfhoehe);
  // Schrift und Hero-Bild können die Kopfhöhe nach dem ersten Rendern ändern.
  window.addEventListener('load', setzeKopfhoehe);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(setzeKopfhoehe);
})();
