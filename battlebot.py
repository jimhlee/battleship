import random
from string import ascii_uppercase
from battlestuff import Board, Piece

class BattleshipBot(object):
    def __init__(self):
        self.board = Board()
        self.pieces = None
        self.last_hit = []

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
        return [Piece(name, length) for name, length in piece_cfg]

    def try_place(self, piece):
        all_combos = [(x, y, horiz) for x in range(10) for y in range(10) for horiz in (True, False)]
        random.shuffle(all_combos)
        for x, y, horiz in all_combos:
            placed = self.board.check_placeable(piece, x, y, horiz)
            if placed:
                return True

    def guess_coords(self, board):
        all_combos = [(x, y) for x in range(10) for y in range(10)]
        random.shuffle(all_combos)
        for x, y in all_combos:
            valid = board.is_guessable(x, y)
            if valid:
                print(f'Bot guesses {ascii_uppercase[x]}, {y}')
                return x, y
        raise Exception('Somehow you have no guesses')

    def check_hit(self, x, y):
        smart_x = range(x-1, x+2)
        smart_y = range(y-1, y+2)
        smart_range = [random.choice(smart_x), random.choice(smart_y)]
        for piece in self.pieces:
            is_hit = piece.check_hit(x, y)
            if self.last_hit:
                random.choice(smart_range)
                pass
            if not is_hit:
                self.last_hit = []
                continue
            piece.apply_hit(x, y)
            self.last_hit = True
            if piece.is_sunk:
                print(f'Bot {piece.name} has been sunk')
            else:
                print(f'Bot has been hit')
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


if __name__ == '__main__':
    bbot = BattleshipBot()
    bbot.place_pieces()
    print(bbot.open_board)
    print('\n\n')
    print(bbot.hidden_board)
