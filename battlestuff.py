import random
from string import ascii_lowercase, ascii_uppercase

class Piece(object):
    def __init__(self, name, length):
        self.length = length
        self.name = name
        self.pips = [False] * length

        self.horiz = None
        self.x_min, self.x_max = None, None
        self.y_min, self.y_max = None, None

    def set_piece(self, x, y, horiz):
        '''
        Sets the positional values for the piece
        '''
        # TODO: Fill in the missing positional values (10 - 12)
        pass

    def check_hit(self, x, y):
        '''
        Given a set of coordinates, check if it hit the piece
        return a boolean value of if it hit
        '''
        # TODO: Return True/False depending on whether it hit
        pass

    def apply_hit(self, x, y):
        '''
        Modifies the appropriate index in pips with True
        returns None
        '''
        # TODO: modify self.pips in the correct location
        pass

    @property
    def is_sunk(self):
        '''
        A property that checks if all the pips are hit
        '''
        # TODO: return if all values in self.pips are true
        pass

    def __repr__(self):
        # TODO: Modify how you want the pieces to appear
        pass

class Board(object):
    '''
    Your board containing your ships
    Contains the following characters:
        "-" (0) - empty space, unguessed
        "o" (1) - empty space, guessed
        "S" (2) - ship, unhit
        "X" (3) - ship, hit
    '''
    def __init__(self):
        self.grid = [[0 for _ in range(10)] for _ in range(10)]

    def check_placeable(self, piece, x, y, horiz):
        '''
        Check if the piece is placeable on the given board
        Returns True if the peice was successfully placed
        '''
        for i in range(piece.length):
            # TODO: check that all spaces the piece would occupy are free
            # if not, return False
            pass
        # we assume the piece is placeable, so we set the values
        piece.set_piece(x, y, horiz)
        for i in range(piece.length):
            # TODO: modify self.grid so that it has the correct value
            pass
        return True

    def is_guessable(self, x, y):
        '''
        Returns whether or not the x/y is a valid guess (not already guessed)
        '''
        # TODO: Fill out
        pass

    def update(self, x, y, hit):
        '''
        Updates the grid value depending on whether or not it was a hit
        '''
        # TODO: Fill out
        pass

    @property
    def open(self):
        enum = {0: '-', 1: 'o', 2: 'S', 3: 'X'}
        out_str = '  ' + ' '.join([str(x) for x in range(10)]) + '\n'
        return out_str + '\n'.join([f'{ascii_uppercase[i]} ' + ' '.join([enum[val] for val in row]) for i, row in enumerate(self.grid)])

    @property
    def hidden(self):
        enum = {0: '-', 1: 'o', 2: '-', 3: 'X'}
        out_str = '  ' + ' '.join([str(x) for x in range(10)]) + '\n'
        return out_str + '\n'.join([f'{ascii_uppercase[i]} ' + ' '.join([enum[val] for val in row]) for i, row in enumerate(self.grid)])


class Player(object):
    def __init__(self):
        self.board = Board()
        self.pieces = self.create_pieces()

    def create_pieces(self):
        '''
        Create a instance of piece for each of the 5 ships
        returns a list of pieces with names/lengths (but not placed)
        '''
        # TODO: Create 5 pieces with names/lengths and return a list
        pass

    def place_pieces(self):
        '''
        Manually place pieces via prompt
        '''
        for piece in self.pieces:
            # TODO: Show the current piece info and board
            # TODO: Until the user puts in a valid location, do the following:
            #   Prompt the user for x/y and whether the piece should be horizontal
            #   Check the board to see if it's a placeable location
            #   If it is, go to the next piece
            pass
        # TODO: display the final player board
        return

    def safe_prompt(self):
        '''
        All the classes use intergers for x/y but the board shows A-K and 0-9
            and likewise the inputs should probably use a-k and 0-9
        Correctly coerce the inputs to integers and return those x/y integers
        '''
        # TODO: read/coerce an x/y input
        pass

    def auto_place(self):
        '''
        IGNORE ME
        '''
        print('Auto placing pieces')
        self.pieces = self.create_pieces()
        for piece in self.pieces:
            placed = False
            while not placed:
                placed = self.try_place(piece)
            print(f'Auto placed piece {piece.name}')
        print(f'Auto done placing, your board looks like\n{self.open_board}')

    def try_place(self, piece):
        '''
        IGNORE ME
        '''
        all_combos = [(x, y, horiz) for x in range(10) for y in range(10) for horiz in (True, False)]
        random.shuffle(all_combos)
        for x, y, horiz in all_combos:
            placed = self.board.check_placeable(piece, x, y, horiz)
            if placed:
                return True

    def check_hit(self, x, y):
        '''
        Given a set of x/y coordinates, checks each piece to see if it was hit
        If there was a hit, does two things: 
            modifies the piece to show that there's a hit
            checks if it was just a normal hit, or if the whole shit was sunk, and reports the appropraite message
        returns True if any of the pieces were hit, otherwise False
        '''
        # TODO: Fill out
        pass

    def update_board(self, x, y, hit):
        '''
        Updates the player board with an x/y and whether it was a hit
        '''
        # TODO: Fill out
        pass

    @property
    def open_board(self):
        return self.board.open

    @property
    def hidden_board(self):
        return self.board.hidden

    @property
    def all_sunk(self):
        '''
        Returns if all the pieces are sunk
        '''
        # TODO Fill out
        pass
