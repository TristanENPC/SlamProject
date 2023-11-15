# TDLOG project - Roquefort Filomène - Salaün Amandine - Lagu Edouard - Riou Tristan

import grid
import player
import question
import time
import threading

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
    
def init_final_grid(repert):
    G = grid.np.full((12,15),None)
    with open(repert) as file :
        contents = file.readlines()
    theme = contents[0][0:8]
    word_list = contents[12].split(' , ')
    first = contents[13].split(' / ')
    orientation = contents[14].split(' , ')
    for i in range(12):
        for j in range(11,26):
            if contents[i][j] == ' ':
                G[i,j-11] = None
            else :
                G[i,j-11] = contents[i][j]
    return(theme,G,word_list,first,orientation)
        

class Game():
    def __init__(self,list_player0):
        '''
        list_player0 : list with objects from player class
        '''
        self._list_player = list_player0
        self._grid = None
        self._list_questions = []
        self._all_players_answered = False
        
    def pull_grid(self,table):
        ''' get a grid already generated'''
        self._grid = table
        
    def slam(self,player):
        '''
        If a player does a slam, it looks if he's right. Else he looses
        '''
        self.grid.display_shown()
        number_word = int(input("Quel mot voulez-vous deviner ?"))
        answer = input("Quelle est votre réponse ?")
        points=0
        
        while (answer==self.grid.words[number_word].name and (not self.grid.comparate_grids())):
            
            print("Bonne réponse !")

            #afficher le mot dans la grille 
            word=self.grid.words[number_word]
            points+=word.length
            if word.is_horizontal :
                for j in range(word.first_letter_position[1],word.first_letter_position[1]+word.length):
                    self.grid.shown_table[word.first_letter_position[0],j]=self.grid.table[word.first_letter_position[0],j]
            if word.is_vertical :
                for i in range(word.first_letter_position[0],word.first_letter_position[0]+word.length):
                    self.grid.shown_table[i,word.first_letter_position[1]]=self.grid.table[i,word.first_letter_position[1]]
                    
            self.grid.display_shown()        
            number_word = int(input("Quel mot voulez-vous deviner ?"))
            answer = input("Quelle est votre réponse ?")
            
        if self.grid.comparate_grids():
            player.points += points 
        else:
            player.points = 0
            print('Vous avez raté votre Slam')
            self.list_player.remove(player)
            
    def final_turn(self):
        
        theme,final_grid,w_l,f_p,ori = init_final_grid('final.txt')
        print('Voici votre thème : ',theme)
        self._grid = grid.Grid(final_grid.shape[0],final_grid.shape[1])
        print(final_grid)
        self.grid.give_grid(grid.np.array(final_grid))
        self.grid.full_shown_table()
        self.grid.pull_words_final(w_l)
        for i in range(len(self.grid.words)):
            self.grid.words[i].first_letter_position = (int(f_p[i][1:3]),int(f_p[i][4:6]))
            if ori[i] == 'v' :
                self.grid.words[i].change_orientation()
        self.grid.pull_letters()
        given_letters = self.grid.letters[:6]
        
        
        for i in range(final_grid.shape[0]):
            for j in range(final_grid.shape[1]):
                if self.grid.table[i,j] in given_letters :
                    self.grid.shown_table[i,j] = self.grid.table[i,j]
                
        print('Et voici votre grille : ')
        self.grid.display_shown()
        print('Vous avec 1 minute')

        number_word = int(input("Quel mot voulez-vous deviner ?"))
        answer = input("Quelle est votre réponse ?")
        
        while (not self.grid.comparate_grids()):
            if answer==self.grid.words[number_word].name :
                print("Bonne réponse !")
                word=self.grid.words[number_word]
                if word.is_horizontal :
                    for j in range(word.first_letter_position[1],word.first_letter_position[1]+word.length):
                        self.grid.shown_table[word.first_letter_position[0],j]=self.grid.table[word.first_letter_position[0],j]
                if word.is_vertical :
                    for i in range(word.first_letter_position[0],word.first_letter_position[0]+word.length):
                        self.grid.shown_table[i,word.first_letter_position[1]]=self.grid.table[i,word.first_letter_position[1]]
            else :
                print("Non")
                    
            self.grid.display_shown()        
            number_word = int(input("Quel mot voulez-vous deviner ?"))
            answer = input("Quelle est votre réponse ?")
            
        print('fin jeu')
        
             
    #def turn(self):
        

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
    G.full_shown_table()

G.display()

l_players = [player.Player('p1'),player.Player('p2'),player.Player('p3')]
jeu = Game(l_players)
jeu.pull_grid(G)






