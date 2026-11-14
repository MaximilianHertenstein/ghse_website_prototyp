// Video: erst beim Klick laden.
//
// Ein <video>-Element bringt den Mediaplayer mit – auf der Seite kostet
// das rund 200 ms Hauptthread-Zeit, auch ohne Abspielen. Deshalb steht
// am Platz des Videos zunächst nur das Vorschaubild; wer klickt, bekommt
// das Video nachgeladen und startet es.
(function () {
  var knoepfe = document.querySelectorAll('[data-video-src]');
  if (!knoepfe.length) return;

  for (var i = 0; i < knoepfe.length; i++) {
    knoepfe[i].addEventListener('click', function (e) {
      var knopf = e.currentTarget;
      var video = document.createElement('video');
      video.controls = true;
      video.autoplay = true;
      video.playsInline = true;
      video.setAttribute('playsinline', '');
      video.preload = 'auto';
      video.style.width = '100%';
      video.style.height = 'auto';
      video.style.display = 'block';
      video.style.background = '#000000';
      var quelle = document.createElement('source');
      quelle.src = knopf.getAttribute('data-video-src');
      quelle.type = 'video/mp4';
      video.appendChild(quelle);
      knopf.parentNode.replaceChild(video, knopf);
      video.play();
    });
  }
})();
