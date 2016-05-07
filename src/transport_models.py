""" asdf """
from protorpc import messages
import endpoints


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    key = messages.StringField(1)
    player_email = messages.StringField(2)
    board = messages.StringField(3)
    state = messages.IntegerField(4)


class StringMessage(messages.Message):
    """Single outbound string message"""
    message = messages.StringField(1)


class GameShortForm(messages.Message):
    """Single outbound string message"""
    key = messages.StringField(1)
    state = messages.IntegerField(2)
    player_email = messages.StringField(3)


class PlayerScore(messages.Message):
    email = messages.StringField(1)
    win_percentage = messages.FloatField(2)
    games_played = messages.IntegerField(3)


class PlayerScores(messages.Message):
    players = messages.MessageField(PlayerScore, 1, repeated=True)


class PlayerGames(messages.Message):
    games = messages.MessageField(GameShortForm, 1, repeated=True)


class PlayResult(messages.Message):
    origin_value = messages.IntegerField(1)
    origin = messages.StringField(2)
    destination = messages.StringField(3)
    captures = messages.StringField(4)
    game_state = messages.IntegerField(5)


GAME_REQUEST = endpoints.ResourceContainer(
    game_key=messages.StringField(1))

PLAY_REQUEST = endpoints.ResourceContainer(
    game_key=messages.StringField(1, required=True),
    origin_row=messages.IntegerField(2, required=True),
    origin_column=messages.IntegerField(3, required=True),
    destination_row=messages.IntegerField(4, required=True),
    destination_column=messages.IntegerField(5, required=True))
