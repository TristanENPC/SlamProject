from flask import Flask, render_template, request
import game

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('SiteSlam.html')

@app.route('/executer_fonction_buzz')
def executer_fonction_buzz():
    game.jeu.choose_player()
    message = 'Quel joueur a buzzé ?'
    return message


@app.route('/executer_fonction_python')
def executer_fonction_python():
    game.jeu.load_final()
    message = game.jeu.grid.display_shown_site()
    return message

@app.route('/executer_fonction_python_start')
def executer_fonction_python_start():
    game.jeu.load_turn()
    #message = game.jeu.grid.display_shown_site()
    message = game.jeu.turn_set(game.questions)
    return message

@app.route('/traiter_formulaire', methods=['POST'])
def traiter_formulaire():

    if request.method == 'POST' and game.jeu.is_final:
        champ_texte = request.form['champ_texte']
        message = game.jeu.turn_from_final(champ_texte)
        message2 = game.jeu.grid.display_shown_site()
        return render_template('SiteSlam.html', champ_texte=champ_texte, message=message, message2=message2)

    elif request.method == 'POST' and not game.jeu.is_final:

        if game.jeu.is_choosing_player :
            try :
                champ_texte = request.form['champ_texte']
                game.jeu.player_is_playing = int(champ_texte)
                if len(game.jeu.turn_losers) == len(game.jeu.list_player) :
                    message = "Prochaine question : "+game.jeu.turn_set(game.questions)
                elif game.jeu.player_is_playing in game.jeu.turn_losers :
                    message = "Vous ne pouvez plus jouer."
                else :
                    game.jeu.guess_letter()
                    message = "Quelle est votre réponse ?"
                game.jeu.choose_player()
                score1 = game.jeu.list_player[0].points
                score2 = game.jeu.list_player[1].points
                score3 = game.jeu.list_player[2].points
            except ValueError :
                message = "Ce n'est pas un chiffre acceptable"
                game.jeu.choose_player()

            return render_template('SiteSlam.html', champ_texte=champ_texte, message=message,score1=score1,score2=score2,score3=score3)

        elif game.jeu.is_guessing_letter :
            champ_texte = request.form['champ_texte']
            game.jeu.guessed_letter = champ_texte
            message, logic, message2 = game.jeu.turn()[1],game.jeu.turn()[0],game.jeu.turn()[2]
            if logic :
                game.jeu.end_choosing_word()
                game.jeu.guess_letter()
            else :
                if message == "Aucun joueur n'a trouvé la lettre. \n Elle ne pourra donc plus être trouvée. Le tour est terminé." :
                    message = "Personne n'a trouvé, prochaine question : "+game.jeu.turn_set(game.questions)
                game.jeu.guess_letter()

            return render_template('SiteSlam.html', champ_texte=champ_texte, message=message, message2=message2)

        elif game.jeu.is_choosing_word :
            champ_texte = request.form['champ_texte']
            game.jeu.chosen_word = champ_texte
            message = game.jeu.turn_2()
            message2 = game.jeu.grid.display_shown_site()
            if message != "Veuillez entrer un choix de mot valide." and message != "Vous ne pouvez pas deviner ce mot":
                game.jeu.guess_word()
                game.jeu.end_choosing_word()
            return render_template('SiteSlam.html', champ_texte=champ_texte, message=message, message2=message2)

        elif game.jeu.is_guessing_word :
            champ_texte = request.form['champ_texte']
            game.jeu.guessed_word = champ_texte
            message = game.jeu.turn_3()+"Nouvelle question : "+game.jeu.turn_set(game.questions)
            message2 = game.jeu.grid.display_shown_site()
            game.jeu.guess_word()
            score1 = game.jeu.list_player[0].points
            score2 = game.jeu.list_player[1].points
            score3 = game.jeu.list_player[2].points
            return render_template('SiteSlam.html', champ_texte=champ_texte, message=message, message2=message2,score1=score1,score2=score2,score3=score3)

        else :
            champ_texte = request.form['champ_texte']
            message = 'Mauvaise saisie'
            message2 = game.jeu.grid.display_shown_site()
            return render_template('SiteSlam.html', champ_texte=champ_texte, message=message, message2=message2)



if __name__ == '__main__':
    app.run(debug=True)