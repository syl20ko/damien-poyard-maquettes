/* Maquettes Damien Poyard, (c) Sylvain Caron 2026. Script commun, sans dépendance. */
(function () {
  var q = new URLSearchParams(location.search);
  if (q.get('nobar') === '1') document.documentElement.classList.add('barre-cachee');

  // Lecteur d'extrait : démonstration visuelle, un seul extrait à la fois.
  document.querySelectorAll('[data-play]').forEach(function (b) {
    b.addEventListener('click', function () {
      var on = b.getAttribute('aria-pressed') === 'true';
      document.querySelectorAll('[data-play][aria-pressed="true"]').forEach(function (o) {
        o.setAttribute('aria-pressed', 'false');
        o.setAttribute('aria-label', 'Écouter un extrait');
        var p = o.closest('[data-piste]'); if (p) p.classList.remove('joue');
      });
      if (!on) {
        b.setAttribute('aria-pressed', 'true');
        b.setAttribute('aria-label', 'Mettre en pause');
        var p = b.closest('[data-piste]'); if (p) p.classList.add('joue');
      }
    });
  });

  // Formulaires : rien n'est envoyé dans une maquette.
  document.querySelectorAll('form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var b = f.querySelector('button[type="submit"]');
      if (b) b.textContent = 'Merci, c\'est noté';
    });
  });

  // Menu mobile
  document.querySelectorAll('[data-menu]').forEach(function (b) {
    b.addEventListener('click', function () {
      var n = document.getElementById(b.getAttribute('aria-controls'));
      var open = b.getAttribute('aria-expanded') === 'true';
      b.setAttribute('aria-expanded', String(!open));
      if (n) n.classList.toggle('ouvert', !open);
    });
  });
})();
