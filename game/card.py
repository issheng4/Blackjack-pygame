import logging
import pygame
from typing import Optional, ClassVar
from .constants import Colours

class Card:
    """Represents a playing card with value, suit and visual representation."""
    
    # Card dimensions
    WIDTH: float = 500/4.4
    HEIGHT: float = 726/4.4
    
    VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    SUITS = ['spades', 'clubs', 'hearts', 'diamonds']
    _SUIT_SYMBOLS = {
        'spades': '♤',
        'clubs': '♧',
        'hearts': '♡',
        'diamonds': '♢'
    }

    # Class-level card back image
    _CARD_BACK: ClassVar[pygame.Surface] = pygame.transform.smoothscale(
        pygame.image.load("assets/cards/back.png"),
        (WIDTH, HEIGHT)
    )

    @classmethod
    def get_card_back(cls) -> pygame.Surface:
        """Returns the card back image."""
        return cls._CARD_BACK

    def __init__(self, value: str, suit: str) -> None:
        """Initialize a card with value and suit.
        
        Args:
            value: Card value (A, 2-10, J, Q, K)
            suit: Card suit (spades, clubs, hearts, diamonds)
            
        Raises:
            ValueError: If invalid value or suit provided
        """
        if value not in self.VALUES:
            raise ValueError(f"Invalid card value: {value}")
        if suit not in self.SUITS:
            raise ValueError(f"Invalid card suit: {suit}")
            
        self.value: str = value
        self.suit: str = suit
        self._image: Optional[pygame.Surface] = self._load_image()
    
    def get_points(self) -> int:
        """Returns the point value of the card."""
        if self.value in ['J', 'Q', 'K']:
            return 10
        elif self.value == 'A':
            return 11  # will be adjusted to 1 later if necessary
        return int(self.value)
        
    def _load_image(self) -> Optional[pygame.Surface]:
        """Loads and returns the card's image."""
        filename = f'assets/cards/{self.value}{self.suit[0].upper()}.png'
        try:
            raw_image = pygame.image.load(filename)
            return pygame.transform.smoothscale(raw_image, (self.WIDTH, self.HEIGHT))
        except pygame.error as e:
            logging.error(f'Error loading card image {filename}: {e}')
            return None
        
    def render(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Renders the card with shadow effect at the specified position."""
        if self._image:
            # Render card shadow
            shadow = pygame.Surface(self._image.get_size(), pygame.SRCALPHA)
            shadow.fill(Colours.SHADOW)
            surface.blit(shadow, (x - 2, y + 2))
            
            # Render card on top
            surface.blit(self._image, (x, y))
        
    def __repr__(self) -> str:
        return f'{self.value}{self._SUIT_SYMBOLS[self.suit]}'