from enum import Enum

class GameState(str, Enum):
    """Enumeration for the different states of the game."""
    INTRO = "intro"
    RESET = "reset"
    DEALING = "dealing"
    PLAYER_TURN = "player_turn"
    DEALER_TURN = "dealer_turn"
    RESOLUTION = "resolution"