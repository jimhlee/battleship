from battlebot import BattleshipBot
from battlestuff import Player

class BattleshipGame(object):
    def __init__(self):
        self.player = Player()
        self.bot = BattleshipBot()
         
    def start_game(self, auto=False):
        print('Battleship yo')
        self.setup_boards(auto)
        while True:
            # player gets to try first
            if self.player.all_sunk:
                print('The bot won')
                return
            self.player_turn()

            if self.bot.all_sunk:
                print('You win')
                return
            #self.bot_turn()

    def setup_boards(self, auto=False):
        print('The bot will now set up')
        self.bot.place_pieces()
        if auto:
            print('Setting up pieces for player automatically')
            self.player.auto_place()
        else:
            self.player.place_pieces()
        print(f'\n\n{bgame.bot.open_board}\n\n')

    def player_turn(self):
        print(f'Your turn, your opponents board is:\n\n{self.bot.hidden_board}')
        x, y = self.player.safe_prompt()
        hit = self.bot.check_hit(x, y)
        self.player.update_board(x, y, hit)
        self.bot.update_board(x, y, hit)

    def bot_turn(self):
        print(f'\nBot turn, your board is:\n\n{self.player.open_board}')
        x, y = self.bot.guess_coords(self.player.board)
        hit = self.player.check_hit(x, y)
        self.player.update_board(x, y, hit)
        self.bot.update_board(x, y, hit)

if __name__ == '__main__':
    bgame = BattleshipGame()
    bgame.start_game(auto=True)
