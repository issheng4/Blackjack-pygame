from dataclasses import dataclass
from typing import Tuple
import pygame

@dataclass(frozen=True)
class Display:
    """Screen dimensions and basic display settings."""
    WIDTH: int = 1280
    HEIGHT: int = 720
    FONT_NAME: str = 'lucidaconsole'
    FONT_SIZE: int = 30
    FONT_SIZE_SMALL: int = 24
    BACKGROUND = pygame.image.load("assets/table.png")

@dataclass(frozen=True)
class Colours:
    """Colour definitions in (R,G,B) or (R,G,B,A) format."""
    WHITE: Tuple[int, ...] = (255, 255, 255)
    BLACK: Tuple[int, ...] = (0, 0, 0)
    TABLE_GREEN: Tuple[int, ...] = (22, 79, 40)
    BG_DARK_GREY: Tuple[int, ...] = (30, 30, 30)
    TEXTBOX_DARK: Tuple[int, ...] = (10, 10, 10)
    TEXTBOX_LIGHT: Tuple[int, ...] = (235, 235, 235)
    SHADOW: Tuple[int, ...] = (0, 0, 0, 15)


@dataclass(frozen=True)
class CardLayout:
    """Card positioning.""" 
    # Player card positioning
    PLAYER_FIRST_X: int = 390
    PLAYER_FIRST_Y: int = 370
    PLAYER_OFFSET_X: int = 25
    PLAYER_OFFSET_Y: int = 29
    
    # Dealer card positioning
    DEALER_FIRST_X: int = 1050
    DEALER_FIRST_Y: int = 30
    DEALER_OFFSET_X: int = 130
    DEALER_OFFSET_Y: int = 0

@dataclass(frozen=True)
class Audio:
    """Audio file paths and volume settings."""
    MUSIC_VOLUME: float = 0.5
    CARD_DRAW_VOLUME: float = 0.3
    GAME_WIN_VOLUME: float = 0.7
    
    INTRO_MUSIC: str = "assets/music/intro.mp3"
    MAIN_MUSIC: str = "assets/music/main.mp3"
    CARD_DRAW: str = "assets/sounds/card_draw.wav"
    PLAYER_WIN: str = "assets/sounds/player_game_won.wav"
    DEALER_WIN: str = "assets/sounds/dealer_game_won.wav"

@dataclass(frozen=True)
class Scoreboard:
    """Scoreboard positioning."""
    TEXT_X: int = 20
    TITLE_Y: int = 30
    PLAYER_Y: int = 60
    DEALER_Y: int = 90
    


