import pygame
from typing import Literal
from .constants import Audio
from .hand import Hand
from .deck import Deck

RoleType = Literal["player", "dealer"]

class Person:
    """Represents a player or dealer in the blackjack game."""

    def __init__(self, role: RoleType) -> None:
        if role not in ("player", "dealer"):
            raise ValueError("Role must be 'player' or 'dealer'")

        self.role: RoleType = role
        self.hand: Hand = Hand()
        self.games_won: int = 0

        sound_file = Audio.PLAYER_WIN if self.role == "player" else Audio.DEALER_WIN
        self.win_sound: pygame.mixer.Sound = pygame.mixer.Sound(sound_file)
        self.win_sound.set_volume(Audio.GAME_WIN_VOLUME)

    def receive_card(self, deck: Deck) -> None:
        """Receives a card dealt from the deck and adds to the player's hand."""
        card = deck.deal_card()
        self.hand.add_card(card)

    def reset_hand(self) -> None:
        """Clears the current hand and prepares for a new round."""
        self.hand = Hand()

    def win_game(self) -> None:
        """Increments win count and plays win sound."""
        self.games_won += 1
        self.win_sound.play()

    def __repr__(self) -> str:
        return f"Person role='{self.role}' total={self.hand.total} wins={self.games_won}"
