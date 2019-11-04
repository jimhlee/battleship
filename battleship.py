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
        self.setup_boards()
        while True:
            if self.player.all_sunk:
                print('You\'ve lost.')
            elif self.bot.all_sunk:
                print('You\'ve won!')
            else:
                self.player_turn()
                self.bot_turn()

        
        

    def setup_boards(self, auto=False):
        '''
        Sets up the player and bot boards
        If auto flag is true, the player will use the automatic function
        '''
        if auto:
            self.player.auto_place()
        else:
            self.player.place_pieces()
        self.bot.place_pieces()

        # TODO: if automatic, use the convenience function in player
        # otherwise use the manual set up

    def player_turn(self):
        # TODO: Ask player for coordinates
        # TODO: check if the player hit the bot's board
        # TODO: Update both boards with the result

        hit = self.player.check_hit(self.player.safe_prompt())
        if hit:
            self.player.update_board()
            self.bot.update_board()

    def bot_turn(self):
        print(f'\nBot turn, your board is:\n\n{self.player.open_board}')
        x, y = self.bot.guess_coords(self.player.board)
        # TODO: check if the bot hit the player's board
        # TODO: Update both boards with the result
        hit = self.bot.check_hit()  
        if hit:     
            self.player.update_board()
            self.bot.update_board()
        '''
        if hit:
            player.board[x][y] = 
        '''

if __name__ == '__main__':
    bgame = BattleshipGame()
    bgame.start_game(auto=True)
