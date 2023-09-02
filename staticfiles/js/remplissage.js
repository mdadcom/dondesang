const numeroCnibField = document.getElementById('numero_cnib');
const nomField = document.getElementById('nom');
const prenomField = document.getElementById('prenom');
// Ajoutez des variables similaires pour les autres champs

numeroCnibField.addEventListener('input', (event) => {
    const numeroCnib = event.target.value;

    fetch(`/api/add-donneur/${collects_pk}`)
        .then(response => response.json())
        .then(data => {
            nomField.value = data.nom;
            prenomField.value = data.prenom;
            // Remplissez les autres champs avec les données du donneur
        })
        .catch(error => {
            console.error(`Une erreur s'est produite : ${error}`);
        });
});
