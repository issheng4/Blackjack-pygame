from typing import Optional
from .game_flags import GameFlags
from .game_state import GameState
from .deck import Deck

class GameManager:
    """Manages global game state, flags, and deck operations."""

    def __init__(self) -> None:
        self.state: GameState = GameState.INTRO
        self.flags: GameFlags = GameFlags()
        self.deck: Deck = Deck()
        self.current_music: Optional[str] = None  # Path or ID for background music
