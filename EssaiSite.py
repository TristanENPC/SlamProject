from flask import Flask, render_template, request, Response
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
    game.jeu.InverseSomeoneBuzzed()
    game.jeu.turn_set(game.questions)
    return render_template('SiteSlam2.html')


@app.route('/base')
def base():
    message = game.jeu.current_question.title
    message2 = game.jeu.grid.display_shown_site()
    return render_template('SiteSlam2.html', message=message, message2=message2)


@app.route('/traiter_formulaire', methods=['POST'])
def traiter_formulaire():

    if request.method == 'POST' and game.jeu.is_final:
        champ_texte = request.form['champ_texte']
        message = game.jeu.turn_from_final(champ_texte)
        message2 = game.jeu.grid.display_shown_site()
        game.jeu.InverseEndTurn()

        return render_template('SiteSlam2.html', champ_texte=champ_texte, message=message, message2=message2)

    elif request.method == 'POST' and not game.jeu.is_final and not game.jeu.SomeoneBuzzed:
        message = game.jeu.current_question.title
        message2 = game.jeu.grid.display_shown_site()
        score1 = game.jeu.list_player[0].points
        score2 = game.jeu.list_player[1].points
        score3 = game.jeu.list_player[2].points
        return render_template('SiteSlam2.html', champ_texte=champ_texte, message=message,message2=message2,score1=score1,score2=score2,score3=score3)

    elif request.method == 'POST' and not game.jeu.is_final and game.jeu.SomeoneBuzzed:

        if game.jeu.grid.comparate_grids():
            l_inter = []
            for i in range(len(game.jeu.list_player)):
                l_inter.append(game.jeu.list_player[i].points)
            l_inter_arr = game.grid.np.array(l_inter)
            indice = game.grid.np.argmin(l_inter_arr)
            game.jeu.list_player[indice].points = 'Eliminate'
            game.jeu.list_player[indice].block()

        if game.jeu.is_choosing_player:
            try:
                champ_texte = request.form['champ_texte']

                if int(champ_texte) < len(game.jeu.list_player):
                    game.jeu.player_is_playing = int(champ_texte)

                    if len(game.jeu.turn_losers) == len(game.jeu.list_player) :
                        message = "Prochaine question : "+game.jeu.turn_set(game.questions)
                    elif game.jeu.player_is_playing in game.jeu.turn_losers or game.jeu.list_player[game.jeu.player_is_playing].is_blocked :
                        message = "Vous ne pouvez plus jouer. Les autres peut-être ? "+game.jeu.current_question.title
                    else :
                        game.jeu.guess_letter()
                        message = game.jeu.current_question.title + " Quelle est votre réponse ?"
                    game.jeu.choose_player()
                else :
                    message = "Ce n'est pas un chiffre acceptable. Veuillez entrer le numéro du joueur"

            except ValueError :
                message = "Ce n'est pas un chiffre acceptable. Veuillez entrer le numéro du joueur"

            message2 = game.jeu.grid.display_shown_site()
            score1 = game.jeu.list_player[0].points
            score2 = game.jeu.list_player[1].points
            score3 = game.jeu.list_player[2].points

            return render_template('SiteSlam2.html', champ_texte=champ_texte, message=message,message2=message2,score1=score1,score2=score2,score3=score3)

        elif game.jeu.is_guessing_letter:
            champ_texte = request.form['champ_texte']
            game.jeu.guessed_letter = champ_texte
            message, logic, message2 = game.jeu.turn()[1],game.jeu.turn()[0], game.jeu.turn()[2]
            score1 = game.jeu.list_player[0].points
            score2 = game.jeu.list_player[1].points
            score3 = game.jeu.list_player[2].points
            if logic:
                game.jeu.end_choosing_word()
                game.jeu.guess_letter()
            else:
                if message == "Aucun joueur n'a trouvé la lettre. \n Elle ne pourra donc plus être trouvée. Le tour est terminé." :
                    message = "Personne n'a trouvé, prochaine question : "+game.jeu.turn_set(game.questions)
                game.jeu.guess_letter()

            return render_template('SiteSlam2.html', champ_texte=champ_texte, message=message, message2=message2, score1=score1, score2=score2, score3=score3)

        elif game.jeu.is_choosing_word:
            score1 = game.jeu.list_player[0].points
            score2 = game.jeu.list_player[1].points
            score3 = game.jeu.list_player[2].points
            champ_texte = request.form['champ_texte']
            game.jeu.chosen_word = champ_texte
            message = game.jeu.turn_2()
            message2 = game.jeu.grid.display_shown_site()
            if message != "Veuillez entrer un choix de mot valide." and message != "Vous ne pouvez pas deviner ce mot":
                game.jeu.guess_word()
                game.jeu.end_choosing_word()
            return render_template('SiteSlam2.html', champ_texte=champ_texte, message=message, message2=message2, score1=score1, score2=score2, core3=score3)

        elif game.jeu.is_guessing_word :
            champ_texte = request.form['champ_texte']
            game.jeu.guessed_word = champ_texte
            message = game.jeu.turn_3()+" Quelqu'un veut Slamer ? Répondre le numéro du joueur ou non"
            message2 = game.jeu.grid.display_shown_site()
            game.jeu.guess_word()
            game.jeu.SomeoneWantsSlam()
            score1 = game.jeu.list_player[0].points
            score2 = game.jeu.list_player[1].points
            score3 = game.jeu.list_player[2].points
            return render_template('SiteSlam2.html', champ_texte=champ_texte, message=message, message2=message2,score1=score1,score2=score2,score3=score3)

        elif game.jeu.SomeoneWantsSlaming :
            champ_texte = request.form['champ_texte']
            score1 = game.jeu.list_player[0].points
            score2 = game.jeu.list_player[1].points
            score3 = game.jeu.list_player[2].points
            if champ_texte == "non" :
                message = "Nouvelle question : "+game.jeu.turn_set(game.questions)
                game.jeu.SomeoneWantsSlam()

            elif champ_texte.isdigit() and int(champ_texte) < len(game.jeu.list_player) and not game.jeu.list_player[int(champ_texte)].is_blocked :
                game.jeu.isSomeoneSlam()
                message = "SLAAAAM du joueur "+champ_texte+" Rentrez les mots sous ce format 0reponse"
                game.jeu.player_is_playing = int(champ_texte)
                game.jeu.SomeoneWantsSlam()

            else :
                message = "Veuillez rentrer quelque chose de valide. Soit non soit un numéro de joueur"

            message2 = game.jeu.grid.display_shown_site()

            return render_template('SiteSlam2.html', champ_texte=champ_texte, message=message, message2=message2, score1=score1,score2=score2,score3=score3)


        elif game.jeu.isSomeoneSlaming :

            champ_texte = request.form['champ_texte']
            try :
                message = game.jeu.check_slam(game.jeu.player_is_playing,int(champ_texte[0]),champ_texte[1:])
            except ValueError :
                message = "Veuillez entrer la réponse sous le format 0reponse"
            message2 = game.jeu.grid.display_shown_site()

            if message == 'perdu' :
                game.jeu.list_player[0].points = 0
                game.jeu.list_player[1].points = 0
                game.jeu.list_player[2].points = 0
                game.jeu.list_player[game.jeu.player_is_playing].points = 'Eliminate'
                game.jeu.list_player[game.jeu.player_is_playing].block()
                game.jeu.isSomeoneSlam()
                game.jeu.InverseEndTurn()
                message = "On perd malheureusement le joueur "+str(game.jeu.player_is_playing) + ". Entrer SUITE pour passer à la manche suivante"

            elif game.jeu.grid.comparate_grids() :
                game.jeu.list_player[0].points = 0
                game.jeu.list_player[1].points = 0
                game.jeu.list_player[2].points = 0
                l_inter = []
                for i in range(len(game.jeu.list_player)):
                    l_inter.append(game.jeu.list_player[i].points)
                l_inter_arr = game.grid.np.array(l_inter)
                indice = game.grid.np.argmin(l_inter_arr)
                game.jeu.list_player[indice].points = 'Eliminate'
                game.jeu.list_player[indice].block()
                message += 'Très beau Slam ! On perd malheureusement le joueur '+ str(indice) + " Entrer SUITE pour passer à la manche suivante"
                game.jeu.isSomeoneSlam()
                game.jeu.InverseEndTurn()

            score1 = game.jeu.list_player[0].points
            score2 = game.jeu.list_player[1].points
            score3 = game.jeu.list_player[2].points

            return render_template('SiteSlam2.html', champ_texte=champ_texte, message=message, message2=message2,score1=score1,score2=score2,score3=score3)

        elif game.jeu.EndTurn :
            champ_texte = request.form['champ_texte']
            if champ_texte == "SUITE" :
                game.jeu.NumTurn = game.jeu.NumTurn+1
                if game.jeu.NumTurn == 2 :
                    game.jeu.InverseEndTurn()
                    game.jeu.load_turn()
                    message = game.jeu.turn_set(game.questions)
                else :
                    game.jeu.InverseEndTurn()
                    game.jeu.load_final()
                    game.jeu.become_final()
                    message = 'Trouvez les mots dans la grille. Utilisez le format : 0reponse'
            else :
                message = "Entrer SUITE pour passer à la manche suivante"
            message2 = game.jeu.grid.display_shown_site()
            score1 = game.jeu.list_player[0].points
            score2 = game.jeu.list_player[1].points
            score3 = game.jeu.list_player[2].points
            return render_template('SiteSlam2.html', champ_texte=champ_texte, message=message, message2=message2,score1=score1,score2=score2,score3=score3)



        else :
            champ_texte = request.form['champ_texte']
            message = 'Mauvaise saisie, Réessayez'
            message2 = game.jeu.grid.display_shown_site()
            return render_template('SiteSlam2.html', champ_texte=champ_texte, message=message, message2=message2)



if __name__ == '__main__':
    app.run(debug=True)
