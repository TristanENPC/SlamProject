# TDLOG project - Roquefort Filomène - Salaün Amandine - Lagu Edouard - Riou Tristan

import grid
import player
import question

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
    with open(repert) as file :
        contents = file.readlines()
    for i in range(len(contents)):
        contents[i] = contents[i].strip()
        contents[i] = contents[i].split(' - ')
        list_words.append(grid.Word(contents[i][0],contents[i][1]))

    return list_words


class Game():
    def __init__(self,list_player0):
        '''
        list_player0 : list with objects from player class
        '''
        self._list_player = list_player0
        self._grid = None
        self._list_questions = []
        self._all_players_answered = False

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
G = grid.Grid(10,10)
G.generate(words)
G.display()
