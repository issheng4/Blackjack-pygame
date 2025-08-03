from .game_flags import GameFlags
from .game_state import GameState
from .deck import Deck

class GameManager():
    def __init__(self):
        self.state = GameState.INTRO
        self.flags = GameFlags()
        self.deck = Deck()
        self.current_music = None
