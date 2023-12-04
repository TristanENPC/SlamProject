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

    @property
    def grid(self):
        return self._grid

    @property
    def list_questions(self):
        return self._list_questions

    @property
    def list_player(self):
        return self._list_player

    def pull_grid(self, table):
        """get a grid already generated"""
        self._grid = table

    def slam(self, player):
        """
        If a player does a slam, it looks if he's right. Else he looses
        """
        self.grid.display_shown()
        number_word = int(input("Quel mot voulez-vous deviner ?"))
        answer = input("Quelle est votre réponse ?")
        points = 0

        while answer == self.grid.words[number_word].name and (
            not self.grid.comparate_grids()
        ):
            print("Bonne réponse !")

            # afficher le mot dans la grille
            word = self.grid.words[number_word]
            points += word.length
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

            self.grid.display_shown()
            number_word = int(input("Quel mot voulez-vous deviner ?"))
            answer = input("Quelle est votre réponse ?")

        if self.grid.comparate_grids():
            player.points += points
        else:
            player.points = 0
            print("Vous avez raté votre Slam")
            self.list_player.remove(player)

    def load_final(self):
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
        
    def turn(self, list_questions):
        question = list_questions[random.randrange(len(list_questions))]
        while question.answer not in self._grid._letters:
            question = list_questions[random.randrange(len(list_questions))]
        print(question.title)
        print('Appuyez sur la touche "enter" pour buzzer.')
        input()
        # 15 seconds timer to answer the question
        letter = input("Vous avez 15 secondes pour répondre une lettre.")
        if letter == question.answer:
            print("Réponse correcte!")
            self.grid.add_letter_to_shown_table(letter)
            self.grid.display_shown()
            print("Saisissez le numéro du mot que vous souhaitez deviner.")
            word_to_guess = input()
            assert type(word_to_guess) == int
            print("Voici la défintition du mot que vous souhaitez deviner :")
            print(self.words[word_to_guess].definition())
            print("Vous avez 20 secondes pour répondre un mot.")
            # 20 seconds timer to answer the question
            answer = input()
            if answer == self.words[word_to_guess].name:
                print("Réponse correcte!")
                self.grid.add_word_to_shown_table(answer)

        # if 15 seconds have passed

        # print('Vous n\'avez pas été assez rapide... \n Appuyez sur la touche "enter" pour buzzer.')

        # init_time = time.time()
        # end_time = time.time()
                    
            

    @property
    def list_player(self):
        return self._list_player

    @property
    def grid(self):
        return self._grid

    @property
    def list_questions(self):
        return self._list_questions


questions = init_questions("questions.txt")
words = init_words("mots.txt")

grid_generated = False
while not grid_generated:
    G = grid.Grid(10, 10)
    grid_generated = G.generate(words)
    G.full_shown_table()

G.display()

l_players = [player.Player("p1"), player.Player("p2"), player.Player("p3")]
jeu = Game(l_players)
jeu.pull_grid(G)
