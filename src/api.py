import endpoints
from protorpc import remote
from models import Game, Player, Board
from transport_models import StringMessage, GameForm, PlayResult
from transport_models import PLAY_REQUEST, GAME_REQUEST

from datetime import datetime
# from google.appengine.api import oauth
from utils import get_by_urlsafe
from ai.main import ai_move
# from google.appengine.api import oauth
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(30)


@endpoints.api(
    name='hnefatafl',
    description='Empty',
    allowed_client_ids=[
        ("314272160250-ucrqg44c1oj9knlrfatqvqf1b3pm9819."
         "apps.googleusercontent.com"),
        endpoints.API_EXPLORER_CLIENT_ID  # comment out in production
        ],
    auth_level=endpoints.AUTH_LEVEL.OPTIONAL_CONTINUE,
    version='v1')
class HnefataflAPI(remote.Service):
    """Game API"""

    @endpoints.method(
        response_message=StringMessage,
        path='player_games',
        name='player_games',
        http_method='GET')
    def player_games(self, request):
        """Gets player games"""

        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')

        player = Player.query(Player.email == user.email()).get()
        if not player:
            raise endpoints.NotFoundException('Player not found')

        return player.games()

    @endpoints.method(
        response_message=GameForm,
        path='last_player_game',
        name='last_player_game',
        http_method='GET')
    def last_player_game(self, request):
        """Gets last playe games"""

        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')

        player = Player.query(Player.email == user.email()).get()
        if not player:
            raise endpoints.NotFoundException('Player not found')

        latest_game = player.latest_game()

        if latest_game:
            return latest_game
        else:
            raise endpoints.NotFoundException('No games are found')

    @endpoints.method(
        response_message=GameForm,
        path='new_game',
        name='new_game',
        http_method='POST')
    def new_game(self, request):
        """Creates new game"""
        user = endpoints.get_current_user()
        print user
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')

        player = Player.query(Player.email == user.email()).get()
        if not player:
            raise Player.new_player(user.nickname(), user.email())

        game = Game.new_game(player_key=player.key)
        game.put()
        return game.to_form()

    @endpoints.method(
        request_message=GAME_REQUEST,
        response_message=PlayResult,
        path='ai_move',
        name='ai_move',
        http_method='GET')
    def ai_move(self, request):
        """Creates new game"""
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')

        game = get_by_urlsafe(request.game_key, Game)
        if not game:
            raise endpoints.NotFoundException("Game not found")

        player = Player.query(Player.email == user.email()).get()
        if not player or player.key != game.player:
            raise endpoints.UnauthorizedException(
                'You are not the player for the game')

        if game.state == 0:
            raise endpoints.UnauthorizedException(
                'It is the player\'s turn')
        if game.state != 1:
            raise endpoints.UnauthorizedException(
                'Game already over')

        board = Board(values=game.board_values)

        ai_won, origin, destination, captures = ai_move(board=board)
        origin_value = board[destination]

        game.state = 3 if ai_won else 0

        game.modified = datetime.now()
        game.put()

        return game.get_play_result(
            origin_value, origin, destination, captures, game.state)

    @endpoints.method(
        request_message=PLAY_REQUEST,
        response_message=PlayResult,
        path='player_move',
        name='player_move',
        http_method='POST')
    def player_move(self, request):
        user = endpoints.get_current_user()

        if not user:
            raise endpoints.UnauthorizedException('Authorization required')

        game = get_by_urlsafe(request.game_key, Game)
        if not game:
            raise endpoints.NotFoundException("Game not found")

        player = Player.query(Player.email == user.email()).get()
        if not player or player.key != game.player:
            raise endpoints.UnauthorizedException(
                'You are not the player for the game')

        if game.state == 1:
            raise endpoints.UnauthorizedException(
                'It is the AI\'s turn')
        if game.state != 0:
            raise endpoints.UnauthorizedException(
                'Game already over')

        origin = (request.origin_row, request.origin_column)
        destination = (request.destination_row, request.destination_column)

        board = Board(game.board_values)

        if board.valid_player_move(origin, destination):
            raise endpoints.BadRequestException("invalid move")

        player_won, captures = board.player_move(origin, destination)
        origin_value = board[destination]

        game.state = 2 if player_won else 1

        game.modified = datetime.now()
        game.put()

        return game.get_play_result(
            origin_value, origin, destination, captures, game.state)


API = endpoints.api_server([HnefataflAPI])
