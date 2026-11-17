/* Nur für „Lesebuch“: Die Dienstleiste des gemeinsamen Templates steht im
   DOM vor dem Logo. Seit die Navigation als Kopfleiste über der Seite liegt,
   bleibt diese Reihenfolge in allen Breiten bestehen; es gibt keine
   Umsortierung mehr. Der Guard sorgt dafür, dass nur „Lesebuch“ etwas tut. */
(function () {
  if (document.documentElement.getAttribute('data-design') !== 'lesebuch') return;
  var kopf = document.querySelector('.kopf');
  var leiste = document.querySelector('.leiste');
  if (kopf && leiste && kopf.firstElementChild !== leiste) {
    kopf.insertBefore(leiste, kopf.firstElementChild);
  }
})();
