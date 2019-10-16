import random
from string import ascii_uppercase

class BotPiece(object):
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
        if horiz:
            self.x_max = x + self.length
            self.y_max = y
        else:
            self.x_max = x
            self.y_max = y + self.length

    def check_ship(self, x, y):
        x_check = self.x <= x <= self.x + length * (not self.horiz)
        y_check = self.y <= y <= self.y + length * self.horiz
        if x_check and y_check:
            self.pips[(x - self.x) + (y - self.y)] = True
            return True
        else:
            return False

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


class BattleshipBot(object):
    def __init__(self):
        self.board = Board()
        self.pieces = None

    def place_pieces(self):
        print(f'Bot is creating pieces')
        self.pieces = self.create_pieces()
        for piece in self.pieces:
            placed = False
            while not placed:
                placed = self.try_place(piece)
            print(f'Bot has placed piece {piece.name}')
        print('Bot is done placing')

    def create_pieces(self):
        piece_cfg = [
            ('Carrier', 5),
            ('Battleship', 4),
            ('Destroyer', 3),
            ('Submarine', 3),
            ('Patrol Boat', 2),
            ]
        return [BotPiece(name, length) for name, length in piece_cfg]

    def try_place(self, piece):
        all_combos = [(x, y, horiz) for x in range(10) for y in range(10) for horiz in (True, False)]
        random.shuffle(all_combos)
        for x, y, horiz in all_combos:
            placed = self.board.check_placeable(piece, x, y, horiz)
            if placed:
                return True

    @property
    def open_board(self):
        return self.board.open

    @property
    def hidden_board(self):
        return self.board.hidden

    @property
    def all_sunk(self):
        return all(piece.is_sunk for piece in self.pieces)


if __name__ == '__main__':
    bbot = BattleshipBot()
    bbot.place_pieces()
    print(bbot.open_board)
    print('\n\n')
    print(bbot.hidden_board)
