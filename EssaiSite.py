from flask import Flask, render_template, request
import game

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('SiteSlam.html')

@app.route('/executer_fonction_python')
def executer_fonction_python():
    game.jeu.load_final()
    message = game.jeu.grid.display_shown_site()
    return message

@app.route('/traiter_formulaire', methods=['POST'])
def traiter_formulaire():

    if request.method == 'POST':
        champ_texte = request.form['champ_texte']
        message2 = game.jeu.turn_from_final(champ_texte)
        message = game.jeu.grid.display_shown_site()
        return render_template('SiteSlam.html', champ_texte=champ_texte, message=message, message2=message2)

if __name__ == '__main__':
    app.run(debug=True)