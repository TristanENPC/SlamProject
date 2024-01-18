import numpy as np
import time


class Word:
    def __init__(self, name0, definition0):
        """
        name0 : str
        definition0 : str
        first_letter_position0 : tuple of two int (i, j)
        """
        self._name = name0
        self._definition = definition0
        self._is_horizontal = True
        self._is_vertical = False
        self._length = len(name0)
        self._first_letter_position = (0, 0)

    @property
    def name(self):
        return self._name

    @property
    def definition(self):
        return self._definition

    @property
    def length(self):
        return self._length

    @property
    def is_horizontal(self):
        return self._is_horizontal

    @property
    def is_vertical(self):
        return self._is_vertical

    @property
    def first_letter_position(self):
        return self._first_letter_position

    @first_letter_position.setter
    def first_letter_position(self, pos):
        self._first_letter_position = pos

    def change_orientation(self):
        transition = self._is_horizontal
        self._is_horizontal = self._is_vertical
        self._is_vertical = transition

    def set_horizontal(self):
        self._is_horizontal = True
        self._is_vertical = False

    def set_vertical(self):
        self._is_horizontal = False
        self._is_vertical = True


class Grid:
    def __init__(self, nb_lines, nb_columns):
        self._size = (nb_lines, nb_columns)
        self._table = np.full(self._size, None)  # Array representing the full grid
        self._shown_table = np.full(
            self._size, None
        )  # Array representing the grid shown to players
        self._words = []
        self._words_discovered = []
        self._letters = []

    @property
    def size(self):
        return self._size

    @property
    def table(self):
        return self._table

    @property
    def shown_table(self):
        return self._shown_table

    @property
    def words(self):
        return self._words

    @property
    def words_discovered(self):
        return self._words_discovered

    @words_discovered.setter
    def words_discovered(self,v):
        self._words_discovered = v

    @property
    def letters(self):
        return self._letters

    @letters.setter
    def letters(self,v):
        self._letters = v

    def give_grid(self, G):
        self._table = G

    def add_letter_to_shown_table(self, letter):
        for line in range(self.size[0]):
            for col in range(self.size[1]):
                if self.table[line][col] == letter:
                    self.shown_table[line][col] = letter

    def add_word_to_shown_table(self, w):
        # IL FAUT METTRE UNE ERREUR SI LE MOT N'APPARTIENT PAS A grid._words
        c = 0
        for i in range(len(self.words)):
            if self.words[i].name == w:
                word = self.words[i]
        if word.is_horizontal:
            line = word.first_letter_position[0]
            for col in range(
                word.first_letter_position[1],
                word.first_letter_position[1] + word.length,
            ):
                self.shown_table[line][col] = word.name[c]
                c += 1
        else:
            assert word.is_vertical
            col = word.first_letter_position[1]
            for line in range(
                word.first_letter_position[0],
                word.first_letter_position[0] + word.length,
            ):
                self.shown_table[line][col] = word.name[c]
                c += 1

    def display_site(self):
        '''
        It displays the grid which is an array as a str message to ease the vizualisation.
        '''
        res = '<div class="grid">'
        line_string = ''
        n,m = self.table.shape
        G = np.full((n+2,m+2),None)
        G[1:n+1,1:m+1] = self.table

        for i in range(len(self.words)):
            if self.words[i].is_horizontal :
                G[self.words[i].first_letter_position[0]+1,self.words[i].first_letter_position[1]] = str(i)
            else :
                G[self.words[i].first_letter_position[0],self.words[i].first_letter_position[1]+1] = str(i)


        for i in range(n + 2):
            res += '<div id="game-grid" class="grid">'
            for j in range(m + 2):
                cell_content = '•' if G[i, j] is None else str(G[i, j])
                cell_class = 'empty-cell' if G[i, j] is None else 'word-cell'
                res += f'<div class="{cell_class}">{cell_content}</div>'
            res += '</div>'
        return res

    def display_shown_site(self):
        '''
        It displays the grid which is an array as a str message to ease the vizualisation.
        '''
        res = '<div class="grid">'
        line_string = ''
        n,m = self.shown_table.shape
        G = np.full((n+2,m+2),None)
        G[1:n+1,1:m+1] = self.shown_table

        for i in range(len(self.words)):
            if self.words[i].is_horizontal :
                G[self.words[i].first_letter_position[0]+1,self.words[i].first_letter_position[1]] = str(i)
            else :
                G[self.words[i].first_letter_position[0],self.words[i].first_letter_position[1]+1] = str(i)


        for i in range(n + 2):
            res += '<div id="game-grid" class="grid">'
            for j in range(m + 2):
                cell_content = '•' if G[i, j] is None else str(G[i, j])
                if G[i,j] is None :
                    cell_class = 'empty-cell'
                elif str(G[i, j]).isdigit() :
                    cell_class = 'digit-cell'
                else :
                    cell_class = 'word-cell'
                res += f'<div class="{cell_class}">{cell_content}</div>'
            res += '</div>'
        return res


    def full_shown_table(self):
        """
        It fulls the grid shown to the user
        """
        n, m = self.table.shape
        for i in range(n):
            for j in range(m):
                if self.table[i, j] is not None:
                    self.shown_table[i, j] = " "

    def comparate_grids(self):
        """
        It returns true if the grid shown to the user and the grid full of words are equal
        """
        res = True
        n, m = self.table.shape
        for i in range(n):
            for j in range(m):
                if self.table[i, j] != self.shown_table[i, j]:
                    res = False
                    break
        return res

    def pull_words_final(self, l_w):
        for i in range(len(l_w)):
            self._words.append(Word(l_w[i], ""))

    def pull_letters(self):
        letters = []
        for i in range(len(self.words)):
            for j in range(len(self.words[i].name)):
                letters.append(self.words[i].name[j])
        self._letters = list(set(letters))

    def check_word_fits_in_grid_and_place_it(
        self, word, tuple_position, impossible_linkage
    ):
        """
        This function has three goals.
        The first is to check if the given word can be in the grid with a connection with the letter in position tuple_position in the grid.
        The second is to place the word in the grid if this word can integer the grid.
        The third is to return the position of the letter shared in the word.
        For example let's consider a 5x5 grid with in the left-top corner the word "tree" in horizontal position,
        if we give to this function the word "run" and the tuple_position (0,1) it will return "(True,0)" and it will place the word "run" behind the word "tree" the both sharing the same "r".
        Be carreful, the "word" argument is an objet from the class "Word" so it has its own position (vertical or horizontal),
        the checking will be effectif uniquely with the position assignated to the word. It doesn't check the both.
        """
        both_letter = self.table[tuple_position]
        if both_letter is None:
            return False
        index_letter = word.name.index(both_letter)
        letters_before = [
            word.name[i] for i in range(len(word.name)) if i < index_letter
        ]
        letters_after = [
            word.name[i] for i in range(len(word.name)) if i > index_letter
        ]

        if tuple_position in impossible_linkage:
            return False

        str_condition = ""

        if word.is_horizontal:
            for k in range(1, len(letters_before) + 1):
                if (
                    (tuple_position[1] - k < 0)
                    or (
                        self.table[tuple_position[0], tuple_position[1] - k] is not None
                        and self.table[tuple_position[0], tuple_position[1] - k]
                        != letters_before[-k]
                    )
                    or (
                        tuple_position[0] - 1 >= 0
                        and self.table[tuple_position[0] - 1, tuple_position[1] - k]
                        is not None
                        and self.table[tuple_position[0], tuple_position[1] - k]
                        != letters_before[-k]
                    )
                    or (
                        tuple_position[0] + 1 < self.table.shape[0]
                        and self.table[tuple_position[0] + 1, tuple_position[1] - k]
                        is not None
                        and self.table[tuple_position[0], tuple_position[1] - k]
                        != letters_before[-k]
                    )
                ):
                    return False
                elif self.table[tuple_position[0], tuple_position[1] - k] is not None:
                    str_condition += self.table[
                        tuple_position[0], tuple_position[1] - k
                    ]

            if (tuple_position[1] - len(letters_before) - 1 >= 0) and (
                self.table[
                    tuple_position[0], tuple_position[1] - len(letters_before) - 1
                ]
                is not None
            ):
                return False

            for k in range(len(letters_after)):
                if (
                    (tuple_position[1] + k + 1 >= self.table.shape[1])
                    or (
                        self.table[tuple_position[0], tuple_position[1] + k + 1]
                        is not None
                        and self.table[tuple_position[0], tuple_position[1] + k + 1]
                        != letters_after[k]
                    )
                    or (
                        tuple_position[0] - 1 >= 0
                        and self.table[tuple_position[0] - 1, tuple_position[1] + k + 1]
                        is not None
                        and self.table[tuple_position[0], tuple_position[1] + k + 1]
                        != letters_after[k]
                    )
                    or (
                        tuple_position[0] + 1 < self.table.shape[0]
                        and self.table[tuple_position[0] + 1, tuple_position[1] + k + 1]
                        is not None
                        and self.table[tuple_position[0], tuple_position[1] + k + 1]
                        != letters_after[k]
                    )
                ):
                    return False
                elif (
                    self.table[tuple_position[0], tuple_position[1] + k + 1] is not None
                ):
                    str_condition += self.table[
                        tuple_position[0], tuple_position[1] + k + 1
                    ]

            if (tuple_position[1] + len(letters_after) + 1 < self.table.shape[1]) and (
                self.table[
                    tuple_position[0], tuple_position[1] + len(letters_after) + 1
                ]
                is not None
            ):
                return False

            if (
                (len(letters_before) == 0)
                and (tuple_position[1] - 1 >= 0)
                and (tuple_position[1] - 1 is not None)
            ):
                return False

            for k in range(1, len(letters_before) + 1):
                self.table[tuple_position[0], tuple_position[1] - k] = letters_before[
                    -k
                ]

            for k in range(len(letters_after)):
                self.table[
                    tuple_position[0], tuple_position[1] + k + 1
                ] = letters_after[k]

        else:
            for k in range(1, len(letters_before) + 1):
                if (
                    (tuple_position[0] - k < 0)
                    or (
                        self.table[tuple_position[0] - k, tuple_position[1]] is not None
                        and self.table[tuple_position[0] - k, tuple_position[1]]
                        != letters_before[-k]
                    )
                    or (
                        tuple_position[1] - 1 >= 0
                        and self.table[tuple_position[0] - k, tuple_position[1] - 1]
                        is not None
                        and self.table[tuple_position[0] - k, tuple_position[1]]
                        != letters_before[-k]
                    )
                    or (
                        tuple_position[1] + 1 < self.table.shape[1]
                        and self.table[tuple_position[0] - k, tuple_position[1] + 1]
                        is not None
                        and self.table[tuple_position[0] - k, tuple_position[1]]
                        != letters_before[-k]
                    )
                ):
                    return False
                elif self.table[tuple_position[0] - k, tuple_position[1]] is not None:
                    str_condition += self.table[
                        tuple_position[0] - k, tuple_position[1]
                    ]

            if (tuple_position[0] - len(letters_before) - 1 >= 0) and (
                self.table[
                    tuple_position[0] - len(letters_before) - 1, tuple_position[1]
                ]
                is not None
            ):
                return False

            for k in range(len(letters_after)):
                if (
                    (tuple_position[0] + k + 1 >= self.table.shape[0])
                    or (
                        self.table[tuple_position[0] + k + 1, tuple_position[1]]
                        is not None
                        and self.table[tuple_position[0] + k + 1, tuple_position[1]]
                        != letters_after[k]
                    )
                    or (
                        tuple_position[1] - 1 >= 0
                        and self.table[tuple_position[0] + k + 1, tuple_position[1] - 1]
                        is not None
                        and self.table[tuple_position[0] + k + 1, tuple_position[1]]
                        != letters_after[k]
                    )
                    or (
                        tuple_position[1] + 1 < self.table.shape[1]
                        and self.table[tuple_position[0] + k + 1, tuple_position[1] + 1]
                        is not None
                        and self.table[tuple_position[0] + k + 1, tuple_position[1]]
                        != letters_after[k]
                    )
                ):
                    return False
                elif (
                    self.table[tuple_position[0] + k + 1, tuple_position[1]] is not None
                ):
                    str_condition += self.table[
                        tuple_position[0] + k + 1, tuple_position[1]
                    ]

            if (tuple_position[0] + len(letters_after) + 1 < self.table.shape[0]) and (
                self.table[
                    tuple_position[0] + len(letters_after) + 1, tuple_position[1]
                ]
                is not None
            ):
                return False

            if (
                (len(letters_before) == 0)
                and (tuple_position[0] - 1 >= 0)
                and (tuple_position[0] - 1 is not None)
            ):
                return False

            if str_condition == word.name:
                return False

            for k in range(1, len(letters_before) + 1):
                self.table[tuple_position[0] - k, tuple_position[1]] = letters_before[
                    -k
                ]

            for k in range(len(letters_after)):
                self.table[
                    tuple_position[0] + k + 1, tuple_position[1]
                ] = letters_after[k]

        return True


    def generate(self, words_list):
        """
        It generates an available grid with the words from words_list which means it modifies the table attribute from the grid object
        which is initially full of "None" with 10 words placed according the logical rules of a Slam grid.
        The generation is based on random so it can fail, if it occurs the methods will return a message "Error generation".
        """
        current_word = Word(" ", " ")
        impossible_positions = []

        # We search a word which has more than 6 letters fitting with the size of the grid, to be the first word
        while (
            len(current_word.name) < 7 or len(current_word.name) >= self.table.shape[1]
        ):
            random_variable = np.random.randint(len(words_list))
            current_word = words_list[random_variable]

        # This word will not appear another time in the grid
        words_list.pop(random_variable)

        # We place it in the grid horizontaly with (0,0) for the coordinate of the first letter
        for j in range(len(current_word.name)):
            self.table[0, j] = current_word.name[j]

        current_word.first_letter_position = (0, 0)
        self.words.append(current_word)

        # We use a list of numbers to choose the shared letter in the two words
        # If this letter doesn't match with all the words in the words_list we can pop it from the list and try another one
        # So the number_of_index_letters is the remaining available letters to test
        available_index_letters = [i for i in range(len(current_word.name))]
        number_of_index_letters = len(current_word.name)

        # Same trick here but for the availables words which could fit with the current one
        available_index_words = []
        number_of_index_words = 0

        # If all the letters of the current word don't allow us to put an other word in the grid
        # We want to try with the previous one placed in the grid so we have to stock this information
        index_in_grids_words = 1
        # Later, it will take the result of check_word_fits_in_grid_and_place_it
        binary = False

        # This variable has been created to avoid the following problem : I place horizontally the word "foot". The random choices to find if the word "boat" match with the word "foot" by the letter "t". The answer is positive and so it places it vertically ending with the t shared with "foot". Now same thing for "television" with "boat" by the letter "t". The answer is also positive and now we have the word footelevision which is not correct. To avoid this problem we want to stock the shared position of two placed words.
        temps_debut = time.time()
        temps_ecoule = 0

        while len(self.words) < 9 and temps_ecoule < 10:    # We can change the 9 with an other number to have more or less words in the grid
            temps_ecoule = time.time() - temps_debut

            index_in_grids_words = len(self.words)

            while (not binary) and (
                index_in_grids_words > -1
            ):  # While we haven't placed an other word and it remains words to test in the grid
                index_in_grids_words -= 1
                available_index_letters = [
                    i for i in range(len(self.words[index_in_grids_words].name))
                ]
                number_of_index_letters = len(available_index_letters)

                while (not binary) and (
                    number_of_index_letters > 0
                ):  # While we haven't placed an other word and it remains letters to test in the word
                    available_words = []
                    words_already_tried = []

                    a = np.random.randint(number_of_index_letters)
                    c = available_index_letters.pop(a)
                    number_of_index_letters -= 1

                    for i in range(len(words_list)):
                        if (
                            self.words[index_in_grids_words].name[c]
                            in words_list[i].name
                        ):
                            available_words.append(words_list[i])

                    available_index_words = [i for i in range(len(available_words))]
                    number_of_index_words = len(available_words)

                    while (not binary) and (
                        len(available_words) != len(words_already_tried)
                    ):  # While we haven't placed an other word and it remains words to test in the words_list which have a shared letter with the word in the grid
                        b = np.random.randint(number_of_index_words)
                        d = available_index_words[b]
                        current_word = available_words[d]

                        words_already_tried.append(current_word)
                        available_index_words.pop(b)
                        number_of_index_words -= 1

                        if self.words[index_in_grids_words].is_horizontal:
                            current_word.set_vertical()
                        else:
                            current_word.set_horizontal()

                        if current_word.is_horizontal:
                            binary = self.check_word_fits_in_grid_and_place_it(
                                current_word,
                                (
                                    self.words[
                                        index_in_grids_words
                                    ].first_letter_position[0]
                                    + c,
                                    self.words[
                                        index_in_grids_words
                                    ].first_letter_position[1],
                                ),
                                impossible_positions,
                            )

                            current_word.first_letter_position = (
                                self.words[index_in_grids_words].first_letter_position[
                                    0
                                ]
                                + c,
                                self.words[index_in_grids_words].first_letter_position[
                                    1
                                ]
                                - (
                                    current_word.name.index(
                                        self.words[index_in_grids_words].name[c]
                                    )
                                ),
                            )
                        else:
                            binary = self.check_word_fits_in_grid_and_place_it(
                                current_word,
                                (
                                    self.words[
                                        index_in_grids_words
                                    ].first_letter_position[0],
                                    self.words[
                                        index_in_grids_words
                                    ].first_letter_position[1]
                                    + c,
                                ),
                                impossible_positions,
                            )

                            current_word.first_letter_position = (
                                self.words[index_in_grids_words].first_letter_position[
                                    0
                                ]
                                - (
                                    current_word.name.index(
                                        self.words[index_in_grids_words].name[c]
                                    )
                                ),
                                self.words[index_in_grids_words].first_letter_position[
                                    1
                                ]
                                + c,
                            )

            if not binary:
                return False

            else:
                impossible_positions.append(
                    (
                        self.words[index_in_grids_words].first_letter_position[0] + c,
                        self.words[index_in_grids_words].first_letter_position[1],
                    )
                )
                binary = False
                self.words.append(current_word)
                words_list.remove(current_word)

        L = []
        for w in self.words:
            for i in range(len(w.name)):
                L.append(w.name[i])
        L =list(set(L))
        for l in L :
            self.letters.append(l)

        return True
