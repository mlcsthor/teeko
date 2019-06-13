from teeko import utils

class Board:
    def __init__(self):
        self.playerWantToMove = False
        self.playerSelected = None

        self.state = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]

    def play(self, coord: tuple, player: int):
        (x, y) = coord

        self.state[y][x] = player

    def move(self, new_coord: tuple, player: int):
        (x, y) = self.playerSelected
        (new_x, new_y) = new_coord

        self.state[y][x] = 0
        self.state[new_y][new_x] = player

        self.cancel_selection()

    def can_play(self, coord: tuple):
        (x, y) = coord

        return self.state[y][x] is 0

    def can_choose(self, coord: tuple, player: int):
        (x, y) = coord

        return self.state[y][x] is player

    def can_move(self, new_coord: tuple):
        if not self.can_play(new_coord):
            return False

        possible_locations = self.get_possible_move_locations(self.playerSelected)

        return new_coord in possible_locations

    def set_state(self, _state):
        self.state = _state

    def print(self):
        print('\n')

        for i in range(len(self.state)):
            print(self.state[i])

        print('\n')

    def check(self):
        if self.check_for_player(1):
            print('Player 1 win !')
        elif self.check_for_player(2):
            print('Player 2 win !')

        return self.check_for_player(1) or self.check_for_player(2)

    def check_for_player(self, player: int):
        if self.check_row(player):
            return True
        elif self.check_column(player):
            return True
        else:
            return self.check_square(player)

    def check_row(self, player: int):
        victory_pattern = [player] * 4

        for i in range(len(self.state)):
            if utils.contains(victory_pattern, self.state[i]):
                return True

        return False

    def check_column(self, player: int):
        victory_pattern = [player] * 4

        for i in range(len(self.state[0])):
            column = [self.state[j][i] for j in range(len(self.state))]

            if utils.contains(victory_pattern, column):
                return True

        return False

    def check_square(self, player: int):
        i = 0
        victory_pattern = [player] * 2

        while not utils.contains(victory_pattern, self.state[i]):
            i += 1

            if i is len(self.state):
                break

        if i < len(self.state) - 1:
            coord = utils.contains(victory_pattern, self.state[i])
            coord_next = utils.contains(victory_pattern, self.state[i + 1])

            return coord == coord_next

        return False

    def select_pawn(self, coord: tuple):
        self.playerWantToMove = True
        self.playerSelected = coord

    def cancel_selection(self):
        self.playerWantToMove = False
        self.playerSelected = None

    def get_possible_move_locations(self, coord: tuple):
        (x, y) = coord

        possible_locations = [(x+1, y+1), (x+1, y-1), (x+1, y), (x-1, y+1), (x-1, y-1), (x-1, y), (x, y+1), (x, y-1)]
        locations = []

        for location in possible_locations:
            (x1, y1) = location

            if 0 <= x1 < 5 and 0 <= y1 < 5 and self.state[y1][x1] is 0:
                locations.append(location)

        return locations