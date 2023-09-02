const choixOui = document.querySelector('#premier-1');
const champSiOui = document.querySelector('#champ-si_premier');

choixOui.addEventListener('click', function() {
  champSiOui.style.display = 'block';
});

const choixNon = document.querySelector('#premier-2');

choixNon.addEventListener('click', function() {
  champSiOui.style.display = 'none';
});