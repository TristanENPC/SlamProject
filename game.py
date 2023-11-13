# TDLOG project - Roquefort Filomène - Salaün Amandine - Lagu Edouard - Riou Tristan

import grid
import player
import question
import time

def init_questions(repert):
    '''
    It reads the document repert and it adds every questions in the document in a list.
    So the returned list contains question.Question objects representing every question writing in the doc
    '''
    list_questions = []
    with open(repert) as file :
        contents = file.readlines()
    for i in range(len(contents)):
        contents[i] = contents[i].strip()
        contents[i] = contents[i].split(' - ')
        list_questions.append(question.Question(contents[i][0],contents[i][1]))

    return list_questions

def init_words(repert):
    '''
    It reads the document repert and it adds every words in the document in a list.
    So the returned list contains grid.Word objects representing every words writing in the doc
    '''
    list_words = []
    list_just_words = []
    with open(repert) as file :
        contents = file.readlines()
    for i in range(len(contents)):
        contents[i] = contents[i].strip()
        contents[i] = contents[i].split(' - ')
        if not (contents[i][0] in list_just_words) :
            list_words.append(grid.Word(contents[i][0],contents[i][1]))
            list_just_words.append(contents[i][0])

    list_words = set(list_words)
    return list(list_words)


class Game():
    def __init__(self,list_player0):
        '''
        list_player0 : list with objects from player class
        '''
        self._list_player = list_player0
        self._grid = None
        self._list_questions = []
        self._all_players_answered = False
        
    def slam(self,player):
        '''
        If a player does a slam, it looks if he's right. Else he looses
        '''
        self.grid.display()
        number_word = input("Quel mot voulez-vous deviner ?")
        answer = input("Quelle est votre réponse ?")
        while (answer==self.grid.words[number_word] and self.grid.shown_table != self.grid.table):
            print("Bonne réponse !")
            #afficher le mot dans la grille 
            number_word
            answer
            if time.sleep(15):
                print("Vous avez mis trop de temps à répondre")
                break
        if self.grid.shown_table == self.grid.table:
            player.points += 0 #mettre le bon nombre de points
        else:
            player.points = 0
            self.list_player.remove(player)
        
        
        
        


    @property
    def list_player(self):
        return self._list_player

    @property
    def grid(self):
        return self._grid

    @property
    def list_questions(self):
        return self._list_questions

questions = init_questions('questions.txt')
words = init_words('mots.txt')

grid_generated = False
while not grid_generated :
    G = grid.Grid(10,10)
    grid_generated = G.generate(words)

G.display()
