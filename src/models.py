"""A setuptools-based script for installing Pulp Smash. """

from google.appengine.ext import ndb

from transport_models import GameForm

from datetime import datetime
import copy

class Player(ndb.Model):
    email = ndb.StringProperty(required=True)

    @classmethod
    def new_player(cls, email):
        player = Player(email=email)
        player.put()


class Game(ndb.Model):
    """
    Game object

    player: The current player object
    board:  An array to represent each cell of the board
                0: Empty
                1: Player's piece
                2: AI's piece
                3: Player's immovable piece
                4: AI's immovable piece
    state:  The state of the current game
                0: Player's turn
                1: AI's turn
                2: Player won
                3: AI won
    """
    player = ndb.KeyProperty(required=True, kind=Player)
    board = ndb.PickleProperty(required=True)
    state = ndb.IntegerProperty(required=True)
    created = ndb.DateTimeProperty(required=True)
    modified = ndb.DateTimeProperty(required=True)

    @classmethod
    def new_game(cls, player_key):
        game = Game(
            player=player_key,
            board=[[0 for x in range(9)] for x in range(9)],
            # board=[[0 for x in range(9)] for x in range(9)],
            state=1,
            created=datetime.now(),
            modified=datetime.now()
        )
        for y in range(9):
            for x in range(9):
                if ((y in (0, 8) and x in (3, 4, 5)) or
                        (x in (0, 8) and y in (3, 4, 5)) or
                        (x == 4 and y in (1, 7)) or
                        (y == 4 and x in (1, 7))):
                        game.board[y][x] = 1
                elif ((x == 4 and y in (2, 3, 5, 6)) or
                        (y == 4 and x in (2, 3, 5, 6))):
                        game.board[y][x] = 2
                elif x == 4 and y == 4:
                    game.board[4][4] = 3
        game.put()
        return game

    def to_form(self):
        return GameForm(
            key=self.key.urlsafe(),
            player_email=self.player.get().email,
            board=str(self.board),
            state=self.state
        )

    def set_board_value(self, cell, value):
        self.board[cell/9][cell % 9] = value

    def get_board_value(self, row, column):
        if row < 0 or row > 8 or column < 0 or column > 8:
            return None
        else:
            return self.board[row][column]

    def get_king(self):
        for position, value in self.board:
            if value == 3:
                return (position/9, position % 9)

    def get_board_copy(self):
        return copy.deepcopy(self.board)

    def can_move(self, piece, target):
        if not self.get_board_value(target) or not self.get_board_value(piece):
            return False
        if piece[0] == target[0]:           # same row
            if piece[1] < target[1]:        # test right
                right = piece[1]/9*9+8
                test = target[1] + 1
                while test <= right:
                    if self.board[test] != 0:
                        return False
                    test += 1
                return True
            elif piece[1] > target[1]:      # test left
                left = piece[1]/9*9
                test = target[1] - 1
                while test >= left:
                    if self.board[test] != 0:
                        return False
                    test -= 1
                return True
            else:                           # same square
                return True
        elif piece[1] == target[1]:         # same column
            if piece[0] > target[0]:        # test top
                top = piece[0] % 9
                test = target[0] - 9
                while test > top:
                    if self.board[test] != 0:
                        return False
                    test -= 9
                return True
            elif piece[0] < target[0]:      # test bottom
                bottom = piece[0] % 9 + 72
                test = target[0] + 9
                while test > bottom:
                    if self.board[test] != 0:
                        return False
                    test += 9
                return True
