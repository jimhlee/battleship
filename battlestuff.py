import random
from string import ascii_lowercase, ascii_uppercase

class Piece(object):
    def __init__(self, name, length):
        self.length = length
        self.name = name
        self.pips = 0
        self.horiz = None
        self.x_min, self.x_max = None, None
        self.y_min, self.y_max = None, None

    def set_piece(self, x, y, horiz):
        '''
        Sets the positional values for the piece
        '''
        if horiz:
            self.x_min = x
            self.x_max = x + self.length - 1 
            self.y_min = y
            self.y_max = self.y_min
        else:
            self.y_min = y
            self.y_max = y + self.length - 1
            self.x_min = x
            self.x_max = self.x_min

    def check_hit(self, x, y):
        '''
        Given a set of coordinates, check if it hit the piece
        return a boolean value of if it hit
        '''
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max
        # if self.horiz:
        #     for i in range(self.y_min, self.y_max):
        #         if i == y:
        #             return True
        # elif not self.horiz:
        #     for i in range(self.x_min, self.x_max):
        #         if i == x:
        #             return True
        # else:
        #     return False


    def apply_hit(self, x, y):  
        '''
        Modifies the appropriate index in pips with True
        returns None
        '''
        # TODO: modify self.pips in the correct location
        # TODO: sync the hit between the x,y and the pip location
        # for i in self.pips:
        #     if self.pips[i] == False:
        #         self.pips[i] = True
        self.pips += 1

    @property
    def is_sunk(self):
        '''
        A property that checks if all the pips are hit
        '''
        # TODO: return if all values in self.pips are true
        return self.pips == self.length

    def __repr__(self):
        # TODO: Modify how you want the pieces to appear
        # TODO: print statement(f string with attributes)
        return (f'{self.name}, Length:{self.length}')
        

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
        Returns True if the piece was successfully placed
        '''
        # this part is check to make sure the board has enough space to place the pieces
        if horiz:
            if y + piece.length > 10:
                print('Cannot place there, not enough space')
                return False
        else:
            if x + piece.length > 10:
                print('Cannot place there, not enough space')
                return False

        for i in range(piece.length):
            if horiz:
                if self.grid[x][y + 1] != 0:
                    return False
            else:
                if self.grid[x + 1][y] != 0:
                    return False
        
        piece.set_piece(x, y, horiz)

        for i in range(piece.length):
            # TODO: modify self.grid so that it has the correct value
            if piece.horiz:
                self.grid[x][y + i] = 2
            else:
                self.grid[x + i][y] = 2
        return True

    def is_guessable(self, x, y):
        '''
        Returns whether or not the x/y is a valid guess (not already guessed)
        '''
        # TODO: Fill out
        #  (a == 1 or a == 2) is the same as (a in [1,2])
        return self.grid[x][y] in [0, 2]

    def update(self, x, y, hit):
        '''
        Updates the grid value depending on whether or not it was a hit
        '''
        # TODO: Fill out, just calls the other one
        # if hit:
        #     self.grid[x][y] = 3
        # else:
        #     self.grid[x][y] = 1
        self.grid[x][y] = 3 if hit else 1

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
        piece_cfg = [
            ('Carrier', 5),
            ('Battleship', 4),
            ('Destroyer', 3),
            ('Submarine', 3),
            ('Patrol Boat', 2),
            ]
        
        # if you see an easy loop, it can be turned into a list comp
        # easy means one line or so
        # ship_list = []
        # for name, length in piece_cfg:
        #     ship_list.append(Piece(name, length))

        return [Piece(name, length) for name, length in piece_cfg] 
          
        # destroyer = Piece('Destroyer', 2)
        # submarine = Piece('Submarine', 3)
        # cruiser = Piece('Cruiser', 3)
        # battleship = Piece('Battleship', 4)
        # carrier = Piece('Carrier', 5)
        # ship_list.append(destroyer)
        # ship_list.append(submarine)
        # ship_list.append(cruiser)
        # ship_list.append(battleship)
        # ship_list.append(carrier)
        # return ship_list

    def place_pieces(self):
        '''
        Manually place pieces via prompt
        ''' 
        for piece in self.pieces:
            # TODO: Show the current piece info and board
            # TODO: Until the user puts in a valid location, do the following:
            #   SafePrompt the user for x/y and whether the piece should be horizontal
            #   Check the board to see if it's a placeable location
            #   If it is, go to the next piece
            # while true until they find a valid location for the next piece
            while True:
                print(self.open_board)
                print(f'Where would you like to place your {piece}?')
                x, y = self.safe_prompt()
                horiz = input('Would you like this ship to be horizontal?(y/n)') == 'y'
                self.board.check_placeable(piece, x, y, horiz)
                # TODO: has a piece been successfully been placed?
                break
        # TODO: display the final player board
        print(self.open_board)
        print('This is your final board')
        return

    def safe_prompt(self):
        '''
        All the classes use intergers for x/y but the board shows A-K and 0-9
            and likewise the inputs should probably use a-k and 0-9
        Correctly coerce the inputs to integers and return those x/y integers
        '''
        # TODO: read/coerce an x/y input
        while True:
            prompt = input(f'Please input coordinates. (Use a-k(lowercase only), and 0-9)')
            real_x = int(ascii_lowercase.index(prompt[0]))
            real_y = int(prompt[1])
            if self.board.is_guessable(real_x, real_y):
                return real_x, real_y
            else:
                break

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
        for piece in self.pieces:
            is_hit = piece.check_hit(x, y)
            # TODO: will never make it past first piece
            # TODO: update board goes somwhere in here
            if is_hit:
                print(f'Hit! The enemy\'s {piece.name} was hit!')
                piece.apply_hit(x, y)
                if piece.is_sunk():
                    print(f'You sunk the enemy\'s {piece.name}!')
                return True
            else: 
                return False

    def update_board(self, x, y, hit):
        '''
        Updates the player board with an x/y and whether it was a hit
        '''
        self.board.update(x, y, hit)
        
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
        return all([piece.is_sunk for piece in self.pieces])