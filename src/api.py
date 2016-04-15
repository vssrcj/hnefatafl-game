import endpoints
from protorpc import remote
from models import Game, Player, Board
from transport_models import StringMessage, GameForm
from transport_models import PLAYER_REQUEST, PLAY_REQUEST, GAME_REQUEST
from game_checks import check_move
# from google.appengine.api import oauth
from utils import get_by_urlsafe
from ai.main import get_result
from google.appengine.api import oauth


@endpoints.api(
    name='hnefatafl',
    description='Empty',
    allowed_client_ids=[
        ("314272160250-ucrqg44c1oj9knlrfatqvqf1b3pm9819."
         "apps.googleusercontent.com")],
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
        """Creates new player"""
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')
        player = Player.query(Player.email == user.email()).get()
        if not player:
            player = endpoints.NotFoundException('Player not found')
        return player.games()

    @endpoints.method(
        response_message=GameForm,
        path='new_game',
        name='new_game',
        http_method='POST')
    def new_game(self, request):
        """Creates new game"""
        user = endpoints.get_current_user()

        if not user:
            raise endpoints.UnauthorizedException('Authorization required')

        player = Player.query(Player.email == user.email()).get()
        if not player:
            player = Player.new_player(user.email())

        game = Game.new_game(player.key)
        game.put()
        return game.to_form()

    @endpoints.method(
        request_message=GAME_REQUEST,
        response_message=GameForm,
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

        board = Board(game.board)
        get_result(board)
        game.put()
        return game.to_form()

    @endpoints.method(
        request_message=PLAY_REQUEST,
        response_message=GameForm,
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

        cell_from = request.cell_from.split(',')
        if not cell_from or len(cell_from) != 2:
            raise endpoints.BadRequestException("cell_from incorrect syntax")

        cell_to = request.cell_to.split(',')
        if not cell_to or len(cell_to) != 2:
            raise endpoints.BadRequestException("cell_to incorrect syntax")

        cell_from = [int(x) for x in cell_from]     # convert all items to int
        cell_to = [int(x) for x in cell_to]
        board = Board(game.board)
        check_move(cell_from, cell_to, board)
        game.put()
        return game.to_form()


API = endpoints.api_server([HnefataflAPI])
