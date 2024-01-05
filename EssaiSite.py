pip install flask

from flask import Flask, render_template, request
import game

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('SiteSlam.html')

@app.route('/executer_fonction_python')
def executer_fonction_python():
    # Exécutez la fonction Python ici (dans votre cas, imprimez 'hello world')
    if champ_texte == 'papillon' :
        message = 'papillon'
    else :
        game.jeu.load_final()
        message = game.jeu.grid.display_shown_site()
    return message

@app.route('/traiter_formulaire', methods=['POST'])
def traiter_formulaire():
    global champ_texte
    if request.method == 'POST':
        champ_texte = request.form['champ_texte']
        return render_template('SiteSlam.html', champ_texte=champ_texte)

if __name__ == '__main__':
    app.run(debug=True)