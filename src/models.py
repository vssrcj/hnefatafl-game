"""A setuptools-based script for installing Pulp Smash. """

from google.appengine.ext import ndb

from transport_models import GameForm, GameShortForm, PlayResult

from datetime import datetime
import copy


BOARD_WIDTH = 9
BOARD_HEIGHT = 9
ATTACKERS = [
    (0, 3), (0, 4), (0, 5), (1, 4),
    (3, 0), (4, 0), (5, 0), (4, 1),
    (3, 8), (4, 8), (5, 8), (4, 7),
    (8, 3), (8, 4), (8, 5), (7, 4)]
DEFENDERS = [
    (2, 4), (3, 4), (4, 5), (4, 6), (5, 4), (6, 4), (4, 2), (4, 3)
]
KING = (4, 4)


class Player(ndb.Model):
    email = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)

    @classmethod
    def new_player(cls, name, email):
        player = Player(name=name, email=email)
        player.put()
        return player

    def games(self):
        games = []
        for game in Game.query(Game.player == self.key, Game.state.IN([0, 1]))\
                        .order(-Game.modified):
            games.append(game)

        return games

    def latest_game(self):
        games = Game.query(Game.player == self.key).order(-Game.modified)
        game = games.fetch(1)
        if game:
            return game[0].to_form()
        else:
            return None

    @classmethod
    def rankings(cls):
        players = Player.query()
        scores = []
        for player in players:
            wins = losses = games = 0
            for game in player.games():
                games += 1
                state = game.state
                if state == 2:
                    wins += 1
                    losses += 1
            win_percentage = float(wins)/(wins + losses) \
                if (wins or losses) else float(0)

            scores.append((win_percentage, games, player.email))
        scores.sort(key=lambda x: (-x[0], x[1]))
        return scores


class Board():
    def __init__(self, values):
        self.values = values
        self.current = 0
        self.max = len(values)

    def __iter__(self):
        return self

    def __getitem__(self, cell):
        y, x = cell
        if y < 0 or y >= BOARD_HEIGHT or x < 0 or x >= BOARD_WIDTH:
            return None
        else:
            return self.values[y][x]

    def __setitem__(self, cell, value):
        self.values[cell[0]][cell[1]] = value

    def next(self):
        if self.current == self.max:
            raise StopIteration
        else:
            self.current += 1
            return self.values[self.current-1]

    def copy(self):
        values = copy.deepcopy(self.values)
        return Board(values)

    def row_length(self, row):
        return len(self.values[row])

    def valid_player_move(self, origin, destination):
        if self[origin] != 1 or origin == destination:
            return False
        directions = ((-1, 0), (1, 0), (0, 1), (0, -1))
        for direction in directions:
            check = copy.deepcopy(origin)
            while True:
                check = (check[0] + direction[0], check[1] + direction[1])

                if check == destination:
                    return True
                if self[check] != 0:
                    break

        return False


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
                4: Cancelled
    """
    player = ndb.KeyProperty(required=True, kind=Player)
    board_values = ndb.PickleProperty(required=True)
    state = ndb.IntegerProperty(required=True)
    created = ndb.DateTimeProperty(required=True)
    modified = ndb.DateTimeProperty(required=True)
    moves = ndb.PickleProperty(required=True)

    @classmethod
    def new_game(cls, player_key):
        game = Game(
            player=player_key,
            board_values=[
                [0 for x in range(BOARD_WIDTH)] for x in range(BOARD_HEIGHT)
            ],
            state=1,
            created=datetime.now(),
            modified=datetime.now(),
            moves=[]
        )
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if (y, x) in ATTACKERS:
                    game.board_values[y][x] = 1
                elif (y, x) in DEFENDERS:
                    game.board_values[y][x] = 2
                elif (y, x) == KING:
                    game.board_values[y][x] = 3
        game.put()
        return game

    def cancel(self):
        self.state = 4

    def to_form(self):
        return GameForm(
            key=self.key.urlsafe(),
            player_email=self.player.get().email,
            board=str(self.board_values),
            state=self.state
        )

    def to_short_form(self):
        return GameShortForm(
            key=self.key.urlsafe(),
            player_email=self.player.get().email,
            state=self.state
        )

    def add_move(self, board, player, won, origin, destination, captures):
        if captures:
            for cell in captures:
                board[cell] = 0

        origin_value = board[origin]
        board[origin] = 0
        board[destination] = origin_value

        if player:
            self.state = 2 if won else 1
        else:
            self.state = 3 if won else 0
        self.moves.append(
            (origin_value, origin, destination, captures, self.state))
        self.modified = datetime.now()
        self.put()
        return origin_value

    @classmethod
    def get_play_result(
        cls, origin_value, origin, destination, captures, game_state
    ):
        return PlayResult(
            origin_value=origin_value,
            origin=str(origin[0]) + ',' + str(origin[1]),
            destination=str(destination[0]) + ',' + str(destination[1]),
            captures=str(captures),
            game_state=game_state)

    def get_board(self):
        return Board(values=self.board)
