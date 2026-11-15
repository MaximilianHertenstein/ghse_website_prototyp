/* Gestaltungsvarianten: Neo (Standard) und weitere Themes.
   Die Auswahl steht als data-design am <html>, wird im Kopf-Skript vor dem
   ersten Bild gesetzt und hier über die Menüs geändert. Ein weiteres Theme
   braucht nur einen Eintrag in hugo.toml und seine eigene CSS-Datei; dieses
   Skript bleibt unverändert. */
(function () {
  var wurzel = document.documentElement;
  var standard = 'neobrutalismus';
  var meta = document.querySelector('meta[name="design-default"]');
  if (meta && meta.content) standard = meta.content;
  var schalter = [].slice.call(document.querySelectorAll('[data-stilwahl]'));

  function aktuell() {
    return wurzel.getAttribute('data-design') || standard;
  }

  function setzen(wahl, speichern) {
    if (!wahl) wahl = standard;
    wurzel.setAttribute('data-design', wahl);
    schalter.forEach(function (feld) {
      if (feld.value !== wahl) feld.value = wahl;
    });
    if (speichern) {
      try { localStorage.setItem('ghse-design', wahl); } catch (e) {}
      // Eine Theme-Angabe in der Adresse gilt nur für diesen Aufruf.
      try {
        var url = new URL(location.href);
        if (url.searchParams.has('design')) {
          url.searchParams.delete('design');
          history.replaceState(null, '', url.pathname + url.search + url.hash);
        }
      } catch (e) {}
    }
  }

  schalter.forEach(function (feld) {
    feld.value = aktuell();
    feld.addEventListener('change', function () { setzen(feld.value, true); });
  });

  window.addEventListener('storage', function (ereignis) {
    if (ereignis.key === 'ghse-design') setzen(ereignis.newValue, false);
  });
})();
