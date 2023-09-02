function sauvegarderFormulaire(event) {
    var consentementCheckbox = document.getElementsByName('consentement');
    var consentementCoche = false;

    for (var i = 0; i < consentementCheckbox.length; i++) {
        if (consentementCheckbox[i].checked) {
            consentementCoche = true;
            break;
        }
    }

    if (consentementCoche) {
        // Enregistrer le formulaire
        alert("Le formulaire a été sauvegardé avec succès.");
    } else {
        // Afficher un message d'erreur
        alert("Veuillez cocher la case de consentement pour donner votre sang.");
        event.preventDefault(); // Annuler l'envoi du formulaire
    }
}