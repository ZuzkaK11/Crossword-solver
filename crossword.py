import numpy as np
import time
############################### CLASS DEFINITION ##############################

class CrossWord():
    # Dict of possible directions {name: (delta_row, delta_col)}
    directions = {'down': (1, 0), 'right': (0, 1)}

    def __init__(self, grid):
        self.grid = grid
        self.positions = self.get_positions(grid)

    def get_positions(self, grid):
        # Computes list of all possible positions for words.
        # Each position is a touple: (start_row, start_col, length, direction),
        # and length must be at least 2, i.e. positions for a single letter
        # (length==1) are omitted.
        # Note: Currently only for 'down' and 'right' directions.
        def check_line(line):
            res = []
            start_i, was_space = 0, False
            for i in range(len(line)):
                if line[i] == '#' and was_space:
                    was_space = False
                    if i - start_i > 1:
                        res.append((start_i, i - start_i))
                elif line[i] == ' ' and not was_space:
                    start_i = i
                    was_space = True
            return res

        poss = []
        for r in range(len(grid)):
            row = grid[r]
            poss = poss + [(r, p[0], p[1], 'right') for p in check_line(row)]
        for c in range(len(grid[0])):
            column = [row[c] for row in grid]
            poss = poss + [(p[0], c, p[1], 'down') for p in check_line(column)]
        return poss

    def print_grid(self):
        # Pretty prints the crossword
        for row in self.grid:
            print(''.join(row))
    
    def grid_to_string(self):
        '''
        Zapíše krížovky ako string pre ukladanie do súboru.
        '''
        return '\n'.join(''.join(row) for row in self.grid)

    def text_at_pos(self, position):
        # Returns text actually written in specified position.
        dr, dc = self.directions[position[3]]
        r, c = position[0], position[1]
        return ''.join([self.grid[r + i * dr][c + i * dc] for i in range(position[2])])

    def write_word(self, position, word):
        # Writes word to specified position and direction.
        # Note: this method does not check whether the word can be placed into
        # specified position.
        dr, dc = self.directions[position[3]]
        r, c = position[0], position[1]
        for i in range(position[2]):
            self.grid[r + i * dr][c + i * dc] = word[i]

    def can_write_word(self, position, word):
        # Check whether the word can be placed into specified position,
        # i.e. position is empty, or all letters within the position are same
        # as those in the word.
        ### YOUR CODE GOES HERE ###
        length = position[2]
        if len(word) != length:                     # Slovo musí mať rovnakú dĺžku ako priestor
            return False
        dr, dc = self.directions[position[3]]
        r, c = position[0], position[1]
        for i in range(length):
            char = self.grid[r + i * dr][c + i * dc]
            if char != ' ' and char != word[i]:     # Ak tam už je písmeno, musí sa zhodovať
                return False
        return True


############################### SERVICE METHODS ###############################

def load_words(path):
    # Loads all words from file
    return open(path, 'r').read().splitlines()


def load_grids(path):
    # Loads empty grids from file
    raw = open(path, 'r').read().split('\n\n')
    per_rows = [grid.rstrip().split('\n') for grid in raw]
    per_char = [[list(row) for row in grid] for grid in per_rows]
    return per_char


################################### SOLVING ###################################
def preprocess_words(words):    
    """
    Predspracuje zoznam slov do slovníka, kde kľúčom je dĺžka slova a hodnotou zoznam slov. {dlzka,[slova]}
    """
    word_dict = {}
    for word in words:
        word_dict.setdefault(len(word), []).append(word)
    return word_dict

def mrv(crossword, preprocessed_words):
    """
    Vyberie pozíciu s najmenším počtom možných slov (MRV - Minimum Remaining Values).
    """
    min_pos = None                      # Najlepšia pozícia (zatiaľ neexistuje)
    min_count = np.inf                  # Počet možností pre aktuálnu najlepšiu pozíciu (nekonečne veľa na začiatku)

    for pos in crossword.positions:                         # Prechádzame všetky pozície
        count = 0
        valid_words = preprocessed_words.get(pos[2], [])    # Zoznam slov správnej dĺžky pre danú pozíciu
        for word in valid_words:                            # Pre každé slovo z vhodnej dĺžky skontrolujeme či môže byť na danej pozícií
            if crossword.can_write_word(pos, word):  
                count += 1
        if count < min_count:           # Ak je táto pozícia lepšia (má menej možností), tak aktualizujeme najlepšiu pozíciu
            min_count = count
            min_pos = pos

    return min_pos                      # Vrátime najlepšiu pozíciu


def solve(crossword, words):
    # Fill the empty spaces in crossword with words
    ### YOUR CODE GOES HERE ###
    preprocessed_words = preprocess_words(words) # Predspracujem si všetky slová do slovníka, kde kľúčom je dĺžka slova a hodnotou zoznam slov.

    def backtrack(crossword, words):
        if not crossword.positions:  # Ak už nemáme žiadne voľné pozície, krížovka je dokončená
            return True
        
        # Heuristika MRV - vyberiem pozíciu, ktorá ma najmenší počet možných slov, aby som čo najskôr došla do konečného stavu
        position = mrv(crossword, preprocessed_words)

        # Získame slová správnej dĺžky pre danú pozíciu
        valid_words = preprocessed_words.get(position[2], [])

        # Vyfiltrujem len tie slová, ktoré môžem zapísať do krížovky
        possible_words = []
        for word in valid_words:
            if crossword.can_write_word(position, word):
                possible_words.append(word)
        crossword.print_grid()
        for word in possible_words:
            original_text = crossword.text_at_pos(position)

            # Zapíšeme slovo a odstránime pozíciu zo zoznamu
            crossword.write_word(position, word)
            crossword.positions.remove(position)

            # Rekurzia
            if backtrack(crossword, words):
                return True

            # Obnovíme pôvodný text a pridáme pozíciu späť
            crossword.write_word(position, original_text)
            crossword.positions.append(position)

        return False
    
    if backtrack(crossword, words):
        return True
    return False

################################ SAVE OUTPUT #################################

def save_solved_grids(grids, times, points_tracker, path):
    """
    Zapíše vyriešené krížovky do súboru po každej vyriešenej krížovke.
    """
    with open(path, 'w') as file:
        for i, (grid, time_taken, points_so_far) in enumerate(zip(grids, times, points_tracker)):
            file.write(f"Crossword {i + 1}:\n")
            file.write(grid)
            file.write(f"\nTime taken: {time_taken:.2f} seconds\n")
            file.write(f"\nTotal time: {sum(times[:i+1])/60:.2f} min\n")
            file.write(f"Points so far: {points_so_far:.2f}\n")
            file.write('\n\n')

################################ MAIN PROGRAM #################################

if __name__ == "__main__":
    ## Load data:
    words = load_words('words.txt')
    grids = load_grids('krizovky.txt')

    ## Examples:
    dummy_grid = [list(s) for s in ['########', '#      #', '#      #', '#      #', '###    #', '#      #', '########']]
    cw = CrossWord(dummy_grid)
    cw.print_grid()  # empty grid
    print('Positions: ' + str(cw.positions))
    cw.write_word((2, 1, 5, 'right'), 'hello')
    cw.write_word((1, 5, 5, 'down'), 'world')
    cw.write_word((4, 3, 4, 'right'), 'milk')
    cw.print_grid()  # 3 words already filled in
    print('Text at position (1,4) down: "' + cw.text_at_pos((1, 4, 5, 'down')) + '"\n\n\n')

    points = [0.5, 1, 1.5, 1.5, 1.5, 2, 2, 2, 2, 2]
    points_so_far = 0
    # Solve crosswords (the last one is a bonus)
    # instead of range(len(grids)) specify in which order do you want your crosswords to be tested
    times = []
    solved_grids = []
    points_tracker = []  # This will store points after each solved crossword

    # Solve crosswords (the last one is a bonus)
    for i in range(len(grids)):
        i=9
        print('==== Crossword No.' + str(i + 1) + ' ====')
        cw = CrossWord(grids[i])
        print(cw.positions)

        start_time = time.time()  
        solve(cw, words)
        end_time = time.time()  

        elapsed_time = end_time - start_time  
        print(f'Time taken to solve Crossword No.{i + 1}: {elapsed_time:.2f} seconds')

        solved_grids.append(cw.grid_to_string())
        cw.print_grid()

        points_so_far += points[i]
        points_tracker.append(points_so_far)
        print(f'Given all the solved crosswords are correct, you have so far {points_so_far} points!')

        times.append(elapsed_time)

        # Ulozenie do suboru
        save_solved_grids(solved_grids, times, points_tracker, 'krizovky_out3.txt')
        
    
