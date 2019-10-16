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
        self.horiz = horiz
        self.x_min = x
        self.y_min = y
        self.x_max = x + self.length * (not horiz)
        self.y_max = y + self.length * horiz

    def check_hit(self, x, y):
        x_check = self.x_min <= x <= self.x_max
        y_check = self.y_min <= y <= self.y_max
        return x_check and y_check

    def apply_hit(self, x, y):
        self.pips[(x - self.x_min) + (y - self.y_min)] = True

    @property
    def is_sunk(self):
        return all(self.pips)

    def __repr__(self):
        return f'{self.name} - {self.length}'

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
        # check if it has room, if so, modify the values of grid
        for i in range(piece.length):
            # protects against trying to go past the edge
            try:
                if self.grid[x + i * (not horiz)][y + i * horiz] != 0:
                    return False
            except IndexError:
                return False
        piece.set_piece(x, y, horiz)
        for i in range(piece.length):
            self.grid[x + i * (not horiz)][y + i * horiz] = 2 
        return True

    def is_guessable(self, x, y):
        return self.grid[x][y] in [0, 2]

    def update(self, x, y, hit):
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
        piece_cfg = [
            ('Carrier', 5),
            ('Battleship', 4),
            ('Destroyer', 3),
            ('Submarine', 3),
            ('Patrol Boat', 2),
            ]
        return [Piece(name, length) for name, length in piece_cfg]

    def place_pieces(self):
        for piece in self.pieces:
            print(f'Please place the {piece.name}, requires {piece.length} spaces.')
            print(f'Your board currently looks like\n{self.open_board}')
            while True:
                x, y = self.safe_prompt()
                horiz = input('Horizontal? (t or f) ') == 't'
                print(x, y, horiz)
                placed = self.board.check_placeable(piece, x, y, horiz)
                if placed:
                    print(f'Piece succesfully played')
                    break
                print('That location did not work, please try again')
        print(f'Your final board:\n{self.open_board}')

    def safe_prompt(self):
        x = ascii_lowercase.index(input('x coordinate? (a-k) '))
        y = int(input('y coordinate? (0-9) '))
        return x, y

    def auto_place(self):
        print('Auto placing pieces')
        self.pieces = self.create_pieces()
        for piece in self.pieces:
            placed = False
            while not placed:
                placed = self.try_place(piece)
            print(f'Auto placed piece {piece.name}')
        print(f'Auto done placing, your board looks like\n{self.open_board}')

    def try_place(self, piece):
        all_combos = [(x, y, horiz) for x in range(10) for y in range(10) for horiz in (True, False)]
        random.shuffle(all_combos)
        for x, y, horiz in all_combos:
            placed = self.board.check_placeable(piece, x, y, horiz)
            if placed:
                return True

    def check_hit(self, x, y):
        for piece in self.pieces:
            is_hit = piece.check_hit(x, y)
            if not is_hit:
                continue
            piece.apply_hit(x, y)
            if piece.is_sunk:
                print(f'Your {piece.name} has been sunk')
            else:
                print(f'You have been hit')
            return True
        print('The shot missed')
        return False

    def update_board(self, x, y, hit):
        self.board.update(x, y, hit)

    @property
    def open_board(self):
        return self.board.open

    @property
    def hidden_board(self):
        return self.board.hidden

    @property
    def all_sunk(self):
        return all(piece.is_sunk for piece in self.pieces)
