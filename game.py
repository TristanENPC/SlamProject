# TDLOG project - Roquefort Filomène - Salaün Amandine - Lagu Edouard - Riou Tristan

import grid
import player
import question

# import time
# import threading
import random

def ask_player():
    answer = input("Quelle est votre réponse ?")
    return(int(answer[0]),answer[1:])

def init_questions(repert):
    """
    It reads the document repert and it adds every questions in the document in a list.
    So the returned list contains questions. Question objects representing every question writing in the doc
    """
    list_questions = []
    with open(repert) as file:
        contents = file.readlines()
    for i in range(len(contents)):
        contents[i] = contents[i].strip()
        contents[i] = contents[i].split(" - ")
        list_questions.append(question.Question(contents[i][0], contents[i][1]))

    return list_questions


def init_words(repert):
    """
    It reads the document repert and it adds every words in the document in a list.
    So the returned list contains grid.Word objects representing every words writing in the doc
    """
    list_words = []
    list_just_words = []
    with open(repert) as file:
        contents = file.readlines()
    for i in range(len(contents)):
        contents[i] = contents[i].strip()
        contents[i] = contents[i].split(" - ")
        if not (contents[i][0] in list_just_words):
            list_words.append(grid.Word(contents[i][0], contents[i][1]))
            list_just_words.append(contents[i][0])

    list_words = set(list_words)
    return list(list_words)


def init_final_grid(repert):
    G = grid.np.full((12, 15), None)
    with open(repert) as file:
        contents = file.readlines()
    theme = contents[0][0:8]
    word_list = contents[12].split(' , ')
    word_list[-1] = word_list[-1].split('\n')[0]
    first = contents[13].split(' / ')
    orientation = contents[14].split(' , ')
    for i in range(12):
        for j in range(11, 26):
            if contents[i][j] == " ":
                G[i, j - 11] = None
            else:
                G[i, j - 11] = contents[i][j]
    return (theme, G, word_list, first, orientation)


class Game:
    def __init__(self, list_player0):
        """
        list_player0 : list with objects from player class
        """
        self._list_player = list_player0
        self._grid = None
        self._list_questions = []
        self._all_players_answered = False
        self._is_final = False
        self._is_choosing_player = False
        self._player_is_playing = 10
        self._is_guessing_letter = False
        self._guessed_letter = ''
        self._current_question = ''
        self._is_choosing_word = False
        self._chosen_word = ''
        self._is_guessing_word = False
        self._guessed_word = ''
        self._turn_losers = []
        self._SomeoneWantsSlaming = False
        self._isSomeoneSlaming = False
        self._SomeoneBuzzed = False
        self._EndTurn = False
        
    @property
    def EndTurn(self):
        return self._EndTurn
        
    def InverseEndTurn(self):
        self._EndTurn = not self.EndTurn

    @property
    def SomeoneBuzzed(self):
        return self._SomeoneBuzzed
        
    def InverseSomeoneBuzzed(self):
        self._SomeoneBuzzed = not self.SomeoneBuzzed
    
    @property
    def SomeoneWantsSlaming(self):
        return self._SomeoneWantsSlaming
        
    def SomeoneWantsSlam(self):
        self._SomeoneWantsSlaming = not self.SomeoneWantsSlaming
        
    @property
    def isSomeoneSlaming(self):
        return self._isSomeoneSlaming
        
    def isSomeoneSlam(self):
        self._isSomeoneSlaming = not self.isSomeoneSlaming
        
    @property
    def turn_losers(self):
        return self._turn_losers
        
    @turn_losers.setter
    def turn_losers(self,v):
        self._turn_losers = v
        
    @property
    def is_guessing_word(self):
        return self._is_guessing_word
        
    @property
    def guessed_word(self):
        return self._guessed_word
        
    @guessed_word.setter
    def guessed_word(self,v):
        self._guessed_word = v
        
    @property
    def chosen_word(self):
        return self._chosen_word
        
    @chosen_word.setter
    def chosen_word(self,v):
        self._chosen_word = v
        
    @property
    def is_choosing_word(self):
        return self._is_choosing_word
        
    @property
    def current_question(self):
        return self._current_question
        
    @current_question.setter
    def current_question(self,v):
        self._current_question = v
        
    @property
    def player_is_playing(self):
        return self._player_is_playing
        
    @property
    def is_guessing_letter(self):
        return self._is_guessing_letter
        
    @player_is_playing.setter
    def player_is_playing(self,v):
        self._player_is_playing = v
        
    @property
    def guessed_letter(self):
        return self._guessed_letter
        
    @guessed_letter.setter
    def guessed_letter(self,v):
        self._guessed_letter = v

    @property
    def is_choosing_player(self):
        return self._is_choosing_player
        
    @property
    def is_final(self):
        return self._is_final

    @property
    def grid(self):
        return self._grid

    @property
    def list_questions(self):
        return self._list_questions

    @property
    def list_player(self):
        return self._list_player
        
    def become_final(self):
        self._is_final = True
        
    def choose_player(self):
        self._is_choosing_player = not self.is_choosing_player
        
    def guess_letter(self):
        self._is_guessing_letter = not self.is_guessing_letter
        
    def guess_word(self):
        self._is_guessing_word = not self.is_guessing_word
        
    def end_choosing_word(self):
        self._is_choosing_word = not self.is_choosing_word

    def pull_grid(self, table):
        """get a grid already generated"""
        self._grid = table
        
    def check_slam(self, player, word_nb, word_name):
        if self.grid.words[word_nb].name == word_name and word_nb not in self.grid.words_discovered :
            self.grid.words_discovered.append(word_nb)
            self.list_player[player].points = self.list_player[player].points+len(word_name)
            word = self.grid.words[word_nb]
            if word.is_horizontal:
                for j in range(
                    word.first_letter_position[1],
                    word.first_letter_position[1] + word.length,
                ):
                    self.grid.shown_table[
                        word.first_letter_position[0], j
                    ] = self.grid.table[word.first_letter_position[0], j]
            if word.is_vertical:
                for i in range(
                    word.first_letter_position[0],
                    word.first_letter_position[0] + word.length,
                ):
                    self.grid.shown_table[
                        i, word.first_letter_position[1]
                    ] = self.grid.table[i, word.first_letter_position[1]]
            message = "Bonne réponse ! Ensuite ?"
        elif self.grid.words[word_nb].name == word_name and word_nb in self.grid.words_discovered :
            message = "Ce mot a déjà était trouvé. Essayez un autre."
        else :
            message = "perdu"
        return message

    def load_turn(self) :
        grid_generated = False
        while not grid_generated:
            G = grid.Grid(10, 10)
            grid_generated = G.generate(words)
            G.full_shown_table()
        jeu.pull_grid(G)
            
    def turn_set(self, list_questions):
        self.turn_losers = []
        self.current_question = list_questions[random.randrange(len(list_questions))]
        while self.current_question.answer not in self.grid.letters:
            self.current_question = list_questions[random.randrange(len(list_questions))]
        return(self.current_question.title)
        
    def turn(self):
        
        p = self.player_is_playing
        letter = self.guessed_letter
        question = self.current_question
        
        if letter != question.answer:
            l = self.turn_losers
            l.append(p)
            self.turn_losers = list(set(l))
            m = self.grid.display_shown_site()
            
            if len(self.turn_losers) == len(self.list_player):
                l = self.grid.letters
                for i in range(len(l)):
                    if l[i] == question.answer :
                        l.remove(l[i])
                        break
                self.grid.letters = l
                
                return(False,"Aucun joueur n'a trouvé la lettre. \n Elle ne pourra donc plus être trouvée. Le tour est terminé.",m)
            
            return(False,"Mauvaise réponse du joueur"+str(self.player_is_playing)+" Les autres peut-être ? "+self.current_question.title,m)

        assert (letter == question.answer)
        self.grid.add_letter_to_shown_table(letter)
        l = self.grid.letters
        for i in range(len(l)):
            if l[i] == question.answer :
                l.remove(l[i])
                break
        self.grid.letters = l
        m = self.grid.display_shown_site()
        return(True,"Réponse correcte! Quel mot veux-tu deviner ?",m)
        
    def turn_2(self):
        p = self.player_is_playing
        letter = self.guessed_letter
        try :
            word_to_guess = int(self.chosen_word)
        except ValueError :
            return("Veuillez entrer un choix de mot valide.")
        assert type(word_to_guess) == int
        if letter not in self.grid.words[word_to_guess].name or word_to_guess in self.grid.words_discovered:
            return ("Vous ne pouvez pas deviner ce mot")
        return("Voici la défintition du mot que vous souhaitez deviner : "+self.grid.words[word_to_guess].definition+" Vous avez 20 secondes pour répondre un mot.")
        
    def turn_3(self):
        answer = self.guessed_word
        word_to_guess = int(self.chosen_word)
        p = self.player_is_playing
        if answer == self.grid.words[word_to_guess].name :
            self.grid.add_word_to_shown_table(answer)
            self.grid.words_discovered.append(word_to_guess)
            
            self.list_player[p].points = self.list_player[p].points+len(answer)
            return("Réponse correcte!")
            
        else :
            return("Mauvaise réponse...")
        


        
        
    def load_final(self):
        self.become_final()
        # On charge la grille de la finale
        theme,final_grid,w_l,f_p,ori = init_final_grid('final.txt') # theme = le thème de la grille, final_grid = matrice représentant la grille, w_l = liste des mots dans la grille, f_p = position des premières lettres de chaque mot, ori = orientation des mots dans la grille
        print('Voici votre thème : ',theme)
        self._grid = grid.Grid(final_grid.shape[0],final_grid.shape[1])
        self.grid.give_grid(grid.np.array(final_grid))
        self.grid.full_shown_table()
        self.grid.pull_words_final(w_l)
        for i in range(len(self.grid.words)):
            self.grid.words[i].first_letter_position = (
                int(f_p[i][1:3]),
                int(f_p[i][4:6]),
            )
            if ori[i] == "v":
                self.grid.words[i].change_orientation()
        self.grid.pull_letters()        
        # [A CHANGER] Il faut demander les lettres à l'utilisateur, pour l'instant ça choisit les 6 premières de la liste des lettres
        given_letters = self.grid.letters[:6]
        
        # On charge la grille de la finale à montrer au joueur
        for i in range(final_grid.shape[0]):
            for j in range(final_grid.shape[1]):
                if self.grid.table[i,j] in given_letters :
                    self.grid.shown_table[i,j] = self.grid.table[i,j]
                
    def turn_from_final(self,champ_texte):
        if not champ_texte[0].isdigit() :
            return("Mauvaise saisie !")
        number_word = int(champ_texte[0])
        answer = champ_texte[1:]
        if answer==self.grid.words[number_word].name :
            message2 = "Bonne réponse !"
            word = self.grid.words[number_word]
            if word.is_horizontal:
                for j in range(
                    word.first_letter_position[1],
                    word.first_letter_position[1] + word.length,
                ):
                    self.grid.shown_table[
                        word.first_letter_position[0], j
                    ] = self.grid.table[word.first_letter_position[0], j]
            if word.is_vertical:
                for i in range(
                    word.first_letter_position[0],
                    word.first_letter_position[0] + word.length,
                ):
                    self.grid.shown_table[
                        i, word.first_letter_position[1]
                    ] = self.grid.table[i, word.first_letter_position[1]]
        else:
            message2 = "Mauvaise réponse !"
        return message2
         
         
            
    def final_turn(self):
        
        self.load_final()
        
        # On lance la finale        
        print('Et voici votre grille : ')
        self.grid.display_shown_site()
        print('Vous avec 1 minute')
        temps_debut = grid.time.time()
        temps_ecoule = 0
        
        while (not self.grid.comparate_grids()) and temps_ecoule < 60:
            number_word, answer = ask_player()
            if answer==self.grid.words[number_word].name :
                print("Bonne réponse !")
                word = self.grid.words[number_word]
                if word.is_horizontal:
                    for j in range(
                        word.first_letter_position[1],
                        word.first_letter_position[1] + word.length,
                    ):
                        self.grid.shown_table[
                            word.first_letter_position[0], j
                        ] = self.grid.table[word.first_letter_position[0], j]
                if word.is_vertical:
                    for i in range(
                        word.first_letter_position[0],
                        word.first_letter_position[0] + word.length,
                    ):
                        self.grid.shown_table[
                            i, word.first_letter_position[1]
                        ] = self.grid.table[i, word.first_letter_position[1]]
            else:
                print("Non")
                
            self.grid.display_shown()
            temps_ecoule = grid.time.time() - temps_debut

        if self.grid.comparate_grids() :
            print('Bravo')
        else :
            print('Temps écoulé !')


questions = init_questions("questions.txt")
words = init_words("mots.txt")
l_players = [player.Player("p1"), player.Player("p2"), player.Player("p3")]
jeu = Game(l_players)

