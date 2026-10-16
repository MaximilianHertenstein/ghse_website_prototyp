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
