function envoyerRequete() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/executer_fonction_python", true);

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // Update the content of the grid with the response received from the server
            document.getElementById('message').innerHTML = xhr.responseText;
        }
    };

    xhr.send();
}

function envoyerRequeteStart() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/executer_fonction_python_start", true);

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            window.location.href = '/base';
        }
    };

    xhr.send();
}

function envoyerBuzz() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/executer_fonction_buzz", true);

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // Mettez à jour le contenu de la grille avec la réponse reçue du serveur
            document.getElementById('message').innerHTML = xhr.responseText;
        }
    };

    xhr.send();
}

