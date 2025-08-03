from enum import Enum

class GameState(Enum):
    INTRO = 0
    RESET = 1
    DEALING = 2
    PLAYER_TURN = 3
    DEALER_TURN = 4
    RESOLUTION = 5