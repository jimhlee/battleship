from battlebot import BattleshipBot
from battlestuff import Player

class BattleshipGame(object):
    def __init__(self):
        self.player = Player()
        self.bot = BattleshipBot()
         
    def start_game(self, auto=False):
        self.setup_boards(auto)
        while True:
            if self.player.all_sunk:
                print('You\'ve lost.')
            elif self.bot.all_sunk:
                print('You\'ve won!')
            else:
                self.player_turn()
                self.bot_turn()

    def setup_boards(self, auto=False):
        if auto:
            self.player.auto_place()
        else:
            self.player.place_pieces()
        self.bot.place_pieces()

    def player_turn(self):
        print(f'\nThe bot\'s board looks like this:\n\n{self.bot.hidden_board}')
        x, y = self.player.safe_prompt()
        hit = self.bot.check_hit(x, y)
        self.bot.update_board(x, y, hit)

    def bot_turn(self):
        print(f'\nBot turn, your board is:\n\n{self.player.open_board}')
        x, y = self.bot.guess_coords(self.player.board)
        hit = self.player.check_hit(x, y)
        self.player.update_board(x, y, hit)

if __name__ == '__main__':
    bgame = BattleshipGame()
    bgame.start_game(auto=True)
