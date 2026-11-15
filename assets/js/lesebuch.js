/* Nur für „Lesebuch“: Die Dienstleiste des gemeinsamen Templates steht im
   DOM vor dem Logo. Ab 1200 px wandert sie ans Ende des Rückens, damit
   Darstellung und Tastatur derselben Reihenfolge folgen (Logo, Aktion,
   Schnellzugriffe, Verzeichnis, Ansicht). Unter 1200 px bleibt sie die
   obere Leiste. Das Partial wird für alle Varianten ausgeliefert; der
   Guard sorgt dafür, dass nur „Lesebuch“ etwas tut. */
(function () {
  if (document.documentElement.getAttribute('data-design') !== 'lesebuch') return;
  var mq = window.matchMedia('(min-width: 1200px)');

  function ordne() {
    var kopf = document.querySelector('.kopf');
    var leiste = document.querySelector('.leiste');
    if (!kopf || !leiste) return;
    if (mq.matches) {
      if (kopf.lastElementChild !== leiste) kopf.appendChild(leiste);
    } else if (kopf.firstElementChild !== leiste) {
      kopf.insertBefore(leiste, kopf.firstElementChild);
    }
  }

  function start() {
    ordne();
    if (mq.addEventListener) mq.addEventListener('change', ordne);
    else if (mq.addListener) mq.addListener(ordne);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
