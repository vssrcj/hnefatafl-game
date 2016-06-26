""" This file contains all the endpoints for the App Engine APIs """

import endpoints
from protorpc import remote

from models import Game, Player, Board
from transport_models import (
    PlayerScore, PlayerScores, GameForm, PlayResult, PlayerGames, PlayResults,
    StringMessage, PLAY_REQUEST, GAME_REQUEST)

from game_utils import attacker_cell_score, MAX_SCORE

from utils import get_by_urlsafe

from ai import ai_move

from google.appengine.api import urlfetch

# Otherwize give timeout exception
urlfetch.set_default_fetch_deadline(30)


@endpoints.api(
    name='hnefatafl',
    description='',
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
        response_message=PlayerGames,
        path='player_games',
        name='player_games',
        http_method='GET')
    def player_games(self, request):
        """Gets all games of the current player"""

        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')

        player = Player.query(Player.email == user.email()).get()
        if not player:
            raise endpoints.NotFoundException('Player not found')

        return PlayerGames(
            games=[game.to_short_form() for game in player.games()]
        )

    @endpoints.method(
        response_message=GameForm,
        path='last_player_game',
        name='last_player_game',
        http_method='GET')
    def last_player_game(self, request):
        """Gets the last played game of the current player"""

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
        response_message=PlayerScores,
        path='player_rankings',
        name='player_rankings',
        http_method='GET')
    def player_rankings(self, request):
        """Ranks all players by win percentage, then by games played"""
        return PlayerScores(
            players=[
                PlayerScore(
                    email=player[2],
                    win_percentage=player[0],
                    games_played=player[1]
                ) for player in Player.rankings()
            ]
        )

    @endpoints.method(
        response_message=GameForm,
        path='new_game',
        name='new_game',
        http_method='POST')
    def new_game(self, request):
        """Creates a new game"""
        user = endpoints.get_current_user()
        print user
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')

        player = Player.query(Player.email == user.email()).get()
        if not player:
            player = Player.new_player(user.nickname(), user.email())

        game = Game.new_game(player_key=player.key)
        game.put()
        return game.to_form()

    @endpoints.method(
        request_message=GAME_REQUEST,
        response_message=PlayResults,
        path='game_history',
        name='game_history',
        http_method='GET')
    def game_history(self, request):
        """Get the history of a game, ranked from old to new"""
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

        return PlayResults(
            results=[
                PlayResult(
                    origin_value=move[0],
                    origin=str(move[1]),
                    destination=str(move[2]),
                    captures=str(move[3]),
                    game_state=move[4]
                ) for move in game.moves
            ]
        )

    @endpoints.method(
        request_message=GAME_REQUEST,
        response_message=PlayResult,
        path='ai_move',
        name='ai_move',
        http_method='PUT')
    def ai_move(self, request):
        """Instruct the AI to make a move"""
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
            raise endpoints.ForbiddenException(
                'It is the player\'s turn')
        if game.state != 1:
            raise endpoints.ForbiddenException(
                'Game already over')

        board = Board(values=game.board_values)

        ai_won, origin, destination, captures = ai_move(board=board)

        origin_value = game.add_move(
            board, False, ai_won, origin, destination, captures)

        return game.get_play_result(
            origin_value, origin, destination, captures, game.state)

    @endpoints.method(
        request_message=PLAY_REQUEST,
        response_message=PlayResult,
        path='player_move',
        name='player_move',
        http_method='PUT')
    def player_move(self, request):
        """Make a move"""

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
            raise endpoints.ForbiddenException(
                'It is the AI\'s turn')
        if game.state != 0:
            raise endpoints.ForbiddenException(
                'Game already over')

        origin = (request.origin_row, request.origin_column)
        destination = (request.destination_row, request.destination_column)

        board = Board(game.board_values)

        if not board.valid_player_move(origin, destination):
            raise endpoints.BadRequestException("invalid move")

        score, captures = attacker_cell_score(board, destination)
        player_won = True if score == MAX_SCORE else None

        origin_value = game.add_move(
            board, True, player_won, origin, destination, captures)

        return game.get_play_result(
            origin_value, origin, destination, captures, game.state)

    @endpoints.method(
        request_message=GAME_REQUEST,
        response_message=StringMessage,
        path='cancel_game',
        name='cancel_game',
        http_method='PUT')
    def cancel_game(self, request):
        """Cancels a game"""
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

        game.cancel()
        return StringMessage(message="Successfully cancelled")

API = endpoints.api_server([HnefataflAPI])
