function envoyerRequete() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/executer_fonction_python", true);

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // Mettez à jour le contenu de la grille avec la réponse reçue du serveur
            document.getElementById('message').innerHTML = xhr.responseText;
        }
    };

    xhr.send();
}

// Variable pour suivre si le bouton START a été cliqué
var startButtonClicked = false;

function envoyerRequeteStart() {
    // Vérifiez si le bouton a déjà été cliqué
    if (!startButtonClicked) {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/executer_fonction_python_start", true);

        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                // Mettez à jour le contenu de la grille avec la réponse reçue du serveur
                document.getElementById('message').innerHTML = xhr.responseText;

                // Masquer le bouton après avoir reçu la réponse
                var startButton = document.getElementById("test");
                startButton.style.display = "none";

                // Mettez à jour la variable pour indiquer que le bouton a été cliqué
                startButtonClicked = true;
            }
        };

        xhr.send();
    }
}

function envoyerBuzz() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/executer_fonction_buzz", true);

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // Mettez à jour le contenu de la grille avec la réponse reçue du serveur
            document.getElementById('message2').innerHTML = xhr.responseText;
        }
    };

    xhr.send();
}
