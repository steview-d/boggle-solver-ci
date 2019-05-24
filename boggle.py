from string import ascii_uppercase
from random import choice
from math import sqrt
from collections import OrderedDict

def make_grid(width, height):
    """
    Creates a grid that will hold all of the tiles
    for a boggle game
    """
    return {(row, col): choice(ascii_uppercase)
        for row in range(height)
        for col in range(width)}
        
def neighbours_of_position(coords):
    """
    Get neighbours of a given position
    """
    row = coords[0]
    col = coords[1]
    
    # Assign each of the neighbours
    # Top-left to top-right
    top_left = (row - 1, col - 1)
    top_center = (row - 1, col)
    top_right = (row - 1, col + 1)
    
    # Left to right
    left = (row, col - 1)
    right = (row, col + 1)    
    
    
    # Bottom-left to bottom-right
    bottom_left = (row + 1, col - 1)
    bottom_center = (row + 1, col)
    bottom_right = (row + 1, col + 1)    
    
    # Assigned an xy offset co-ord from current position
    return [top_left, top_center, top_right,
            left, right,
            bottom_left, bottom_center, bottom_right]
    
        
def all_grid_neighbours(grid):
    """
    Get all of the possible neighbours for each position in
    the grid
    """
    neighbours = {}
    for position in grid:
        position_neighbours = neighbours_of_position(position)
        # for every item in position_neighbours, if it is an actual grid
        # position, add it to 'neighbours' variable.
        neighbours[position] = [p for p in position_neighbours if p in grid]
        # So, every grid position now has a list of each of it's neighbours
    return neighbours
    
    
def path_to_word(grid, path):
    """
    Add all of the letters on the path to a string
    """
    return ''.join([grid[p] for p in path])


def search(grid, dictionary):
    """
    Search through the paths to locate words by matching
    strings to words in a dictionary
    """
    
    neighbours = all_grid_neighbours(grid)
    paths = []
    full_words, stems = dictionary
    
    
    def do_search(path):
        word = path_to_word(grid, path)
        if word in full_words:
            paths.append(path)
        if word not in stems:
            return
        for next_pos in neighbours[path[-1]]:
            if next_pos not in path:
                do_search(path + [next_pos])
            
    for position in grid:
        print(position)
        # Take each grid position in turn, and search from that starting point
        do_search([position])
        
    words = []
    for path in paths:
        words.append(path_to_word(grid, path))
    return set(words)
    
def get_dictionary(dictionary_file):
    """
    Load Dictionary file
    """
    full_words, stems = set(), set()
    
    with open(dictionary_file) as f:
        for word in f:
            word = word.strip().upper()
            full_words.add(word)
            
            for i in range(1, len(word)):
                stems.add(word[:i])
                
    return full_words, stems


def display_board(grid):
    grid_size = int(sqrt(len(grid)))
    
    # Initialize empty 2D array
    screen_grid = [['' for i in range(grid_size)] for j in range(grid_size)]
    sorted_grid = sorted(grid.items())
    for x in range(grid_size):
        for y in range(grid_size):
            print(x, y, grid.get((x, y)))
            screen_grid[x][y] = grid.get((x, y))
    
    for x in range(grid_size):
            print(screen_grid[x])


def main():
    """
    This is the function that will run the whole project
    """
    grid = make_grid(3, 3)
    # grid = {(0,0):'G', (0,1):'A', (0,2):'B', (0,3):'I',
    #         (1,0):'A', (1,1):'E', (1,2):'E', (1,3):'L',
    #         (2,0):'U', (2,1):'N', (2,2):'U', (2,3):'F',
    #         (3,0):'A', (3,1):'M', (3,2):'C', (3,3):'W'}
    # display_board(grid)
    dictionary = get_dictionary('words.txt')
    words = search(grid, dictionary)
    for word in words:
        print(word)
    print("Found %s words" % len(words))
    

if __name__ == "__main__":
    main()