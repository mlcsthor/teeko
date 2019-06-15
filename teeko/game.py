from .board import *
from .interface import *
from .ai import *
import time

class Game:
    def __init__(self, ui: bool):
        self.mode = None
        self.board = Board()
        self.turn = 0
        self.player = 1
        self.interface = None
        self.game_launched = False
        self.playerAI_1 = None
        self.playerAI_2 = None

        if ui:
            Interface(self)
        else:
            self.play()

    def reset(self):
        self.board = Board()
        self.turn = 0
        self.player = 1
        self.interface.clear_board()
        self.game_launched = False

    def set_interface(self, interface: Interface):
        self.interface = interface

    def launch_game_pvp(self):
        self.mode = 0
        self.reset()
        self.game_launched = True

    def launch_game_pvai(self):
        self.mode = 1
        self.reset()
        self.playerAI_2 = AI(self, 2, 3)
        self.game_launched = True

    def launch_game_aivai(self):
        self.mode = 2
        self.reset()
        self.playerAI_1 = AI(self, 1, 3)
        self.playerAI_2 = AI(self, 2, 3)
        while self.is_not_over():
            time.sleep(1)

            if self.turn%2 == 0:
                self.playerAI_1.play_minmax()
                self.next_turn()
            else:
                self.playerAI_2.play_minmax()
                self.next_turn()

    def set_state(self, state: list):
        self.board.set_state(state)

    def check(self):
        if self.board.check_for_player(self.player):
            self.game_launched = False
            self.interface.show_winner()

    def is_not_over(self):
        return not self.board.check()

    def is_placement_phase(self):
        return self.turn < 8
    
    def play(self):
        print('Player ' + str(self.player) + ' begins ! \n')

        self.board.print()

        while self.is_not_over():
            if self.turn < 8:
                self.play_placement()
            else:
                self.play_moving()

            self.next_turn()

    def play_placement(self):
        print('Player ' + str(self.player) + '\'s turn ! (Placement - Turn ' + str(self.turn + 1) + ')')

        (x, y) = utils.input_coordinates(1, len(self.board.state))

        while not self.board.can_play((x, y)):
            print('You can\'t play here !')
            (x, y) = utils.input_coordinates(1, len(self.board.state))

        self.board.play((x, y), self.player)

    def play_moving(self):
        print('Player ' + str(self.player) + '\'s turn ! (Moving - Turn ' + str(self.turn + 1) + ')')

        (x, y) = utils.input_coordinates(1, len(self.board.state))

        while not self.board.can_choose((x, y), self.player):
            print('You can\'t choose that !')
            (x, y) = utils.input_coordinates(1, len(self.board.state))

        self.board.select_pawn((x, y))

        print('Enter the new coordinates')
        (new_x, new_y) = utils.input_coordinates(1, len(self.board.state))

        while not self.board.can_move((new_x, new_y)):
            print('You can\'t move here !')
            (new_x, new_y) = utils.input_coordinates(1, len(self.board.state))

        self.board.move((new_x, new_y), self.player)

    def next_player(self):
        self.player = 1 if self.player is 2 else 2

    def next_turn(self):
        print("Next Turn")
        self.interface.show_game()

        if not self.interface:
            self.board.print()

        self.check()

        self.next_player()

        self.turn += 1
        
        if self.mode == 1 and self.player == 2 and self.is_not_over():
            self.game_launched = False
            self.playerAI_2.play_minmax()
            self.game_launched = True
            self.next_turn()
