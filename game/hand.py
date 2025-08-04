import pygame
from typing import List
from .constants import Audio
from .card import Card

class Hand:
    """Represents a collection of cards held by a player or dealer."""

    def __init__(self) -> None:
        self.cards: List[Card] = []
        self.card_draw_sound: pygame.mixer.Sound = pygame.mixer.Sound(Audio.CARD_DRAW)
        self.card_draw_sound.set_volume(Audio.CARD_DRAW_VOLUME)

    def add_card(self, card: Card) -> None:
        """Adds a card to the hand and plays the draw sound."""
        self.cards.append(card)
        self.card_draw_sound.play()

    def calculate_total(self) -> int:
        """Returns the total point value of the hand, handling Aces as 1 or 11."""
        total_points = 0
        ace_count = 0

        for card in self.cards:
            total_points += card.get_points()
            if card.value == 'A':
                ace_count += 1

        while total_points > 21 and ace_count:
            total_points -= 10
            ace_count -= 1

        return total_points

    def make_hidden_card_reveal_sound(self) -> None:
        """Plays the draw sound (e.g. when a hidden dealer card is revealed)."""
        self.card_draw_sound.play()

    def __repr__(self) -> str:
        return f"Hand({self.cards})"

    @property
    def total(self) -> int:
        """Returns the total hand value."""
        return self.calculate_total()
