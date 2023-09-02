document.querySelector('#numero_cnib').addEventListener('change', function() {
    APP_ROOT = '';
        let numeroCnib = this.value;
        let xhr = new XMLHttpRequest();
        xhr.open('GET', `${APP_ROOT}/add-donneur/${collects_pk}/?numero_cnib=${numeroCnib}`);
        xhr.onload = function() {
            if (xhr.status === 200) {
                let donneur = JSON.parse(xhr.responseText);
                if (donneur !== null) {
                    document.querySelector('#nom').value = donneur.nom;
                    document.querySelector('#prenom').value = donneur.prenom;
                    // remplir les autres champs du formulaire
                }
            } else {
                console.log('Erreur : ' + xhr.status);
            }
        };
        xhr.send();
    });