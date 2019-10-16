from battlebot import BattleshipBot
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
        if horiz:
            self.x_max = x + self.length
            self.y_max = y
        else:
            self.x_max = x
            self.y_max = y + self.length
        #print(f'Please place the {self.name}, requires {self.length} spaces.')
        #print('(Give the x/y coordinate of the top left portion, then either "h" for horizontal or "v" for vertical)')
        #self.x = int(input('x coordinate? '))
        #self.y = int(input('y coordinate? '))
        #orient = input('h (horizontal) or v (vertical)? ')

    def check_ship(self, x, y):
        x_check = self.x <= x <= self.x + length * self.horiz
        y_check = self.y <= y <= self.y + length * (not self.horiz)
        if x_check and y_check:
            self.pips[(x - self.x) + (y - self.y)] = True
            return True
        else:
            return False

    @property
    def positions_tuples(self):
        if self.horiz:
            return [(self.x_min + i, self.y_min, self.pips[i]) 
                        for i in range(self.length)]
        else:
            return [(self.x_min, self.y_min + i, self.pips[i]) 
                        for i in range(self.length)]

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


class Player(object):
    def __init__(self):
        self.board = Board()
        self.pieces = self.create_pieces()

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

    def create_pieces(self):
        piece_cfg = [
            ('Carrier', 5),
            ('Battleship', 4),
            ('Destroyer', 3),
            ('Submarine', 3),
            ('Patrol Boat', 2),
            ]
        return [Piece(name, length) for name, length in piece_cfg]

    def check_hit(self):
        pass

    @property
    def open_board(self):
        return self.board.open

    @property
    def hidden_board(self):
        return self.board.hidden

    @property
    def all_sunk(self):
        return all(piece.is_sunk for piece in self.pieces)

class BattleshipGame(object):
    def __init__(self):
        self.player = Player()
        self.bot = BattleshipBot()
         
    def start_game(self, auto=False):
        print('Battleship yo')
        print('The bot will now set up')
        self.bot.place_pieces()
        if auto:
            self.player.auto_place()
        else:
            self.player.place_pieces()
        i = 0
        while True:
            if i:
                break
            # player gets to try first
            if self.player.all_sunk:
                print('The bot won')
                return
            self.player_turn()

            if self.bot.all_sunk:
                print('You win')
                return
            self.bot_turn()
            i += 1

    def player_turn(self):
        print(f'Your turn, your opponents board is: ')
        print(self.bot.hidden_board)
        
        x, y = self.player.safe_prompt()
        hit = self.player.check_hit(x, y)
        if hit is None:
            print(f'You missed, idiot')
        else:
            print(f'You hit, champ')
        self.player.update_board(x, y)
        self.opponent.update_board(x, y)

    def bot_turn(self):
        pass

if __name__ == '__main__':
    bgame = BattleshipGame()
    bgame.start_game(auto=True)
