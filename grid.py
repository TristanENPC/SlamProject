import numpy as np

class Word():
    def __init__(self,name0,definition0,first_letter_position0):
        '''
        name0 : str
        definition0 : str
        first_letter_position0 : tuple of two int (i,j)
        '''
        self._name = name0
        self._definition = definition0
        self._is_horizontal = True
        self._is_vertical = False
        self._length = len(name0)
        self._first_letter_position = first_letter_position0

    @property
    def name(self):
        return self._name

    @property
    def definition(self):
        return self._definition

    @property
    def is_horizontal(self):
        return self._is_horizontal

    @property
    def is_vertical(self):
        return self._is_vertical

    def change_orientation(self):
        transition = self._is_horizontal
        self._is_horizontal = self._is_vertical
        self._is_vertical = transition

    def where(self):
        '''
        It returns the place occupied by the word according to its first letter position and its orientation
        It is returned in a tuple to make the slicing on numpy array easy
        '''
        if self._is_horizontal :
            return (self._first_letter_position[0],self._first_letter_position[0]+1,self._first_letter_position[1],self._first_letter_position[1]+self._length)
        else :
            return (self._first_letter_position[0],self._first_letter_position[0]+self._length ,self._first_letter_position[1],self._first_letter_position[1]+1)


class Grid():
    def __init__(self,nb_lines,nb_columns):
        self._table = np.full((nb_lines,nb_columns),None)
        self._words = []

    @property
    def table(self):
        return self._table

    @property
    def words(self):
        return self._words









