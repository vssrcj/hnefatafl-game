import endpoints
from protorpc import remote
from models import Game, Player
from transport_models import StringMessage, GameForm
from transport_models import PLAYER_REQUEST, PLAY_REQUEST, GAME_REQUEST
from game_checks import check_move
# from google.appengine.api import oauth
from utils import get_by_urlsafe
from ai.main import get_result


@endpoints.api(name='hnefatafl', description='Empty', version='v1')
class HnefataflAPI(remote.Service):
    """Game API"""

    @endpoints.method(
        request_message=PLAYER_REQUEST,
        response_message=StringMessage,
        path='new_player',
        name='new_player',
        http_method='POST')
    def new_player(self, request):
        """Creates new player"""
        if Player.query(Player.email == request.email).get():
            raise endpoints.ConflictException("Player already exists")
        Player.new_player(request.email)
        return StringMessage(message='Player %s created!' % request.email)

    @endpoints.method(
        request_message=PLAYER_REQUEST,
        response_message=GameForm,
        path='new_game',
        name='new_game',
        http_method='POST')
    def new_game(self, request):
        """Creates new game"""
        player = Player.query(Player.email == request.email).get()
        if not player:
            raise endpoints.NotFoundException("Player not found")
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
        game = get_by_urlsafe(request.game_key, Game)
        if not game:
            raise endpoints.NotFoundException("Game not found")
        get_result(game.board)
        game.put()
        return game.to_form()

    @endpoints.method(
        request_message=PLAY_REQUEST,
        response_message=GameForm,
        path='player_move',
        name='player_move',
        http_method='POST')
    def player_move(self, request):
        game = get_by_urlsafe(request.game_key, Game)
        if not game:
            raise endpoints.NotFoundException("Game not found")

        cell_from = request.cell_from.split(',')
        if not cell_from or len(cell_from) != 2:
            raise endpoints.BadRequestException("cell_from incorrect syntax")

        cell_to = request.cell_to.split(',')
        if not cell_to or len(cell_to) != 2:
            raise endpoints.BadRequestException("cell_to incorrect syntax")

        cell_from = [int(x) for x in cell_from]
        cell_to = [int(x) for x in cell_to]
        check_move(cell_from, cell_to, game.board)
        game.put()
        return game.to_form()


API = endpoints.api_server([HnefataflAPI])
