from dataclasses import dataclass
from typing import Optional

@dataclass
class DialogueFlags:
    """Tracks the state of dialogue boxes throughout the game."""
    intro_lines_set: bool = False
    dealing_lines_set: bool = False
    player_turn_lines_set: bool = False
    dealer_turn_lines_set: bool = False
    player_stands_lines_ready: bool = False
    player_stands_lines_set: bool = False
    player_bust_lines_set: bool = False
    dealer_blackjack_lines_set: bool = False
    dealer_bust_lines_set: bool = False
    review_hands_lines_ready: bool = False
    review_hands_lines_set: bool = False
    endgame_lines_ready: bool = False
    player_wins_lines_set: bool = False
    dealer_wins_lines_set: bool = False
    game_draw_lines_set: bool = False

@dataclass
class GameFlags:
    """Controls and tracks game state through boolean flags."""
    
    def __init__(self) -> None:
        self.dealing_started: bool = False
        self.dealer_second_card_visible: bool = False
        self.player_blackjack_status: Optional[str] = None  # Can be: None, 'start', 'reveal', 'done'
        self.dealer_turn_status: Optional[str] = None  # Can be: None, 'reveal', 'dealing', 'dealing_wait', 'done'
        self.dialogue = DialogueFlags()
    
    def reset(self) -> None:
        """Reset all flags to their initial state."""
        self.dealing_started = False
        self.dealer_second_card_visible = False
        self.player_blackjack_status = None
        self.dealer_turn_status = None
        self.dialogue = DialogueFlags()
    
    def __repr__(self) -> str:
        """Return string representation for debugging."""
        return (f"GameFlags(dealing={self.dealing_started}, "
                f"dealer_card={self.dealer_second_card_visible}, "
                f"blackjack={self.player_blackjack_status}, "
                f"dealer_turn={self.dealer_turn_status})")