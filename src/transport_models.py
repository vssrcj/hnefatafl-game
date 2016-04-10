""" asdf """
from protorpc import messages
import endpoints


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    key = messages.StringField(1, required=True)
    player_email = messages.StringField(2, required=True)
    board = messages.StringField(3, required=True)
    state = messages.IntegerField(4, required=True)


class StringMessage(messages.Message):
    """Single outbound string message"""
    message = messages.StringField(1, required=True)


class MoveMessage(messages.Message):
    cell_1_x = messages.IntegerField(1)
    cell_1_y = messages.IntegerField(2)
    cell_2_x = messages.IntegerField(3)
    cell_2_y = messages.IntegerField(4)
    state = messages.IntegerField(5)


class ReturnMessage(messages.Message):
    """

        game_over:  0: not over
                    1: player won
                    2: AI won
    """
    game_over = messages.IntegerField(1, required=True)
    sacrifice = messages.BooleanField(2, required=True)
    cell_1 = messages.IntegerField(3, required=True)
    cell_2 = messages.IntegerField(4, required=True)


PLAYER_REQUEST = endpoints.ResourceContainer(
    email=messages.StringField(1))

GAME_REQUEST = endpoints.ResourceContainer(
    game_key=messages.StringField(1))

PLAY_REQUEST = endpoints.ResourceContainer(
    game_key=messages.StringField(1, required=True),
    cell_from=messages.StringField(2, required=True),
    cell_to=messages.StringField(3, required=True))
