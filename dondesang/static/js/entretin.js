document.addEventListener('DOMContentLoaded', function() {
  var medicamentRadio = document.getElementsByName('medicament');

  function toggleChampSi() {
      var champSi = document.getElementById('champ-si');
      
      if (medicamentRadio[0].checked) {
          champSi.style.display = 'block';
      } else {
          champSi.style.display = 'none';
      }
  }

  for (var i = 0; i < medicamentRadio.length; i++) {
      medicamentRadio[i].addEventListener('change', toggleChampSi);
  }
});