import random
from string import ascii_uppercase
from battlestuff import Board, Piece

class BattleshipBot(object):
    def __init__(self):
        self.board = Board()
        self.pieces = None
        self.last_hit = None
        self.fancy_set = set()

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
        if self.fancy_set:
            return self.smart_guess(self.fancy_set)
        if self.last_hit:
            return self.smart_guess(board)
        all_combos = [(x, y) for x in range(10) for y in range(10)]
        random.shuffle(all_combos)
        for x, y in all_combos:
            valid = board.is_guessable(x, y)
            if valid:
                print(f'Bot guesses {ascii_uppercase[x]}, {y}')
                return x, y
        raise Exception('Somehow you have no guesses')

    def smart_guess(self, board):
        x, y = self.last_hit
        deltas = [(0,1),(0,-1),(1,0),(-1,0)]
        smart_range = {(x+i, y+j) for (i, j) in deltas}
        random.shuffle(smart_range)
        self.fancy_set += smart_range
        for a, b in self.fancy_set:
            valid = board.is_guessable(a, b)
            if valid:
                self.fancy_set.remove(a, b)
                # can i remove the elements from the set here before returning?
                # i don't think so, need them to carry over
                return a, b


    def check_hit(self, x, y):
        for piece in self.pieces:
            is_hit = piece.check_hit(x, y)
            if not is_hit:
                continue
            piece.apply_hit(x, y)
            self.last_hit = True
            self.hit_coords = (x,y)
            if piece.is_sunk:
                print(f'Bot {piece.name} has been sunk')
            else:
                print(f'Bot has been hit')
            return True
        print('The shot missed')
        self.last_hit = None
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

# TODO: each time there's a hit, create a new SET(new term) and then select coords
# from that set until that set is completely gone. 