import numpy as np
import time
import grid
class YourClass:
    def __init__(self, rows, columns):
        self.table = np.full((rows, columns), None)
        self.words = []

    def generate(self,words_list):
        '''
        It generates an available grid with the words from words_list which means it modifies the table attribute from the grid object which is initially full of "None" with 10 words placed according the logical rules of a Slam grid. The generation is based on random so it can fail, if it occurs the methods will return a message "Error generation".
        '''
        current_word = grid.Word(' ',' ')
        impossible_positions = []

        # We search a word which has more than 6 letters fitting with the size of the grid, to be the first word
        while len(current_word.name) < 7 or len(current_word.name) >= self.table.shape[1]:
            random_variable = np.random.randint(len(words_list))
            current_word = words_list[random_variable]

        # This word will not appear another time in the grid
        words_list.pop(random_variable)

        # We place it in the grid horizontaly with (0,0) for the coordinate of the first letter
        for j in range(len(current_word.name)):
            self.table[0,j] = current_word.name[j]

        current_word.first_letter_position = (0,0)
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

            while (not binary) and (index_in_grids_words > -1) : # While we haven't placed an other word and it remains words to test in the grid

                index_in_grids_words -= 1
                available_index_letters = [i for i in range(len(self.words[index_in_grids_words].name))]
                number_of_index_letters = len(available_index_letters)

                while (not binary) and (number_of_index_letters > 0) : # While we haven't placed an other word and it remains letters to test in the word

                    available_words = []
                    words_already_tried = []

                    a = np.random.randint(number_of_index_letters)
                    c = available_index_letters.pop(a)
                    number_of_index_letters -= 1

                    for i in range(len(words_list)):
                        if self.words[index_in_grids_words].name[c] in words_list[i].name :
                            available_words.append(words_list[i])

                    available_index_words = [i for i in range(len(available_words))]
                    number_of_index_words = len(available_words)

                    while (not binary) and (len(available_words) != len(words_already_tried)) : # While we haven't placed an other word and it remains words to test in the words_list which have a shared letter with the word in the grid

                        b = np.random.randint(number_of_index_words)
                        d = available_index_words[b]
                        current_word = available_words[d]

                        words_already_tried.append(current_word)
                        available_index_words.pop(b)
                        number_of_index_words -= 1

                        if self.words[index_in_grids_words].is_horizontal :
                            current_word.set_vertical()
                        else :
                            current_word.set_horizontal()

                        if current_word.is_horizontal :
                            binary = self.check_word_fits_in_grid_and_place_it(current_word,(self.words[index_in_grids_words].first_letter_position[0]+c,self.words[index_in_grids_words].first_letter_position[1]),impossible_positions)

                            current_word.first_letter_position = (self.words[index_in_grids_words].first_letter_position[0]+c,self.words[index_in_grids_words].first_letter_position[1]-(current_word.name.index(self.words[index_in_grids_words].name[c])))
                        else :
                            binary = self.check_word_fits_in_grid_and_place_it(current_word,(self.words[index_in_grids_words].first_letter_position[0],self.words[index_in_grids_words].first_letter_position[1]+c),impossible_positions)

                            current_word.first_letter_position = (self.words[index_in_grids_words].first_letter_position[0]-(current_word.name.index(self.words[index_in_grids_words].name[c])),self.words[index_in_grids_words].first_letter_position[1]+c)

            if not binary :
                return False

            else :
                impossible_positions.append((self.words[index_in_grids_words].first_letter_position[0]+c,self.words[index_in_grids_words].first_letter_position[1]))
                binary = False
                self.words.append(current_word)
                words_list.remove(current_word)
        return True



    def display_grid(self):
        for row in self.table:
            print(" ".join(str(cell) if cell is not None else ' ' for cell in row))

# Utilisation
rows = 10
columns = 10
your_instance = YourClass(rows, columns)
words_list = ["python", "programmation", "grille", "mot", "fleche", "horizontal", "vertical", "agencement", "exemple", "simple", "projet", "interconnexion"]

success = your_instance.generate(words_list)

if success:
    your_instance.display_grid()
else:
    print("Error generating crossword.")


