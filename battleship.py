from battlebot import BattleshipBot
from battlestuff import Player

class BattleshipGame(object):
    def __init__(self):
        self.player = Player()
        self.bot = BattleshipBot()
         
    def start_game(self, auto=False):
        '''
        The main game loop
        '''
        # TODO: Call setup functions
        # TODO: Check game state
        # TODO: Let the player/bot take turns
        pass

    def setup_boards(self, auto=False):
        '''
        Sets up the player and bot boards
        If auto flag is true, the player will use the automatic function
        '''
        self.bot.place_pieces()
        # TODO: if automatic, use the convenience function in player
        # otherwise use the manual set up

    def player_turn(self):
        # TODO: Ask player for coordinates
        # TODO: check if the player hit the bot's board
        # TODO: Update both boards with the result
        pass

    def bot_turn(self):
        print(f'\nBot turn, your board is:\n\n{self.player.open_board}')
        x, y = self.bot.guess_coords(self.player.board)
        # TODO: check if the player hit the bot's board
        # TODO: Update both boards with the result
        pass

if __name__ == '__main__':
    bgame = BattleshipGame()
    bgame.start_game(auto=True)
