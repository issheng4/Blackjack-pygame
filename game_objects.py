import random
import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    FONT_NAME, FONT_SIZE,
    WHITE, BLACK, TABLE_GREEN, BG_DARK_GREY, TEXTBOX_DARK_GREY, TEXTBOX_LIGHT_GREY, SHADOW,
    TEXTBOX_WIDTH, TEXTBOX_HEIGHT, TEXTBOX_X, TEXTBOX_Y, TEXTBOX_BORDER_RADIUS,
    LINE_HEIGHT, PADDING, LETTER_DELAY, MAX_TEXT_WIDTH,
    ARROW_BLINK_SPEED_MS, ARROW_SIZE, ARROW_X, ARROW_Y,
    CARD_WIDTH, CARD_HEIGHT,
    FIRST_PLAYER_CARD_X, FIRST_PLAYER_CARD_Y, PLAYER_CARD_DISPLACEMENT_X, PLAYER_CARD_DISPLACEMENT_Y, FIRST_DEALER_CARD_X, FIRST_DEALER_CARD_Y, DEALER_CARD_DISPLACEMENT_X,
    CARD_BACK,
)
from enum import Enum

VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUITS = ['spades', 'clubs', 'hearts', 'diamonds']


class Card:
    _SUIT_SYMBOLS = {
    'spades': '♤',
    'clubs': '♧',
    'hearts': '♡',
    'diamonds': '♢'
    }  

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.image = self.load_image()
    
    def get_points(self, total):
        if self.value in ['J', 'Q', 'K']:
            return 10
        elif self.value == 'A':
            return 11 # will be adjusted to 1 later if necessary
        else:
            return int(self.value)
        
    def load_image(self):
        filename = f'assets/cards/{self.value}{self.suit[0].upper()}.png'
        try:
            raw_image = pygame.image.load(filename)
            resized_image = pygame.transform.smoothscale(raw_image, (CARD_WIDTH, CARD_HEIGHT))
            return resized_image
        except pygame.error as e:
            print(f'Error loading card image {filename}: {e}')
            return None
        
    def render(self, surface, x, y):
        if self.image:
            # Render card shadow
            shadow = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            shadow.fill(SHADOW)
            surface.blit(shadow, (x - 2, y + 2))  # offset slightly

            # Render card on top
            surface.blit(self.image, (x, y))
        
    def __repr__(self):
        return f'{self.value}{self._SUIT_SYMBOLS[self.suit]}'
        
    


class Deck:
    def __init__(self):
        self.cards = []
        for value in VALUES:
            for suit in SUITS:
                self.cards.append(Card(value, suit))
                    
    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def __repr__(self):
        return str(self.cards)



class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_total(self):
        total_points = 0
        ace_count = 0

        for card in self.cards:
            total_points += card.get_points(total_points)
            if card.value == 'A':
                ace_count += 1

        # adjusting total points for aces
        while total_points > 21 and ace_count:
            total_points -= 10
            ace_count -= 1

        return total_points

    def __repr__(self):
        return str(self.cards)
    
    @property
    def total(self):
        return self.calculate_total()


class Person:
    def __init__(self, role, name):
        self.role = role # player or dealer
        self.name = name
        self.hand = Hand()
        self.games_won = 0

    def receive_card(self, deck):
        card = deck.deal_card()
        self.hand.add_card(card)

    def calculate_hand_total(self):
        return self.hand.calculate_total()
    
    def reset_hand(self):
        self.hand = Hand()
    
    def __repr__(self):
        return self.name
    

class TextBoxController:
    def __init__(self, font, rect, letter_delay=LETTER_DELAY, blink_speed=ARROW_BLINK_SPEED_MS, padding=PADDING, line_height=LINE_HEIGHT, border_radius=TEXTBOX_BORDER_RADIUS):
        self.font = font
        self.rect = rect

        self.letter_delay = letter_delay
        self.blink_speed = blink_speed
        self.padding = padding
        self.line_height = line_height
        self.border_radius = border_radius
    

        # Display state
        self.lines = []
        self.current_line_index = 0
        self.typed_text = ""
        self.char_index = 0
        self.last_update = 0
        self.line_fully_displayed = False
    
        # Arrow state
        self.arrow_visible = True
        self.arrow_last_blink = 0

    def set_lines(self, lines, show_arrow=True):
        self.lines = lines
        self.current_line_index = 0
        self.typed_text = ""
        self.char_index = 0
        self.line_fully_displayed = False
        self.last_update = pygame.time.get_ticks()
        self.show_arrow = show_arrow
        

    def wrap_text(self, text):
        max_width = self.rect.width - 2 * self.padding
        words = text.split(" ")
        wrapped_lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                wrapped_lines.append(current_line.strip())
                current_line = word + " "
        wrapped_lines.append(current_line.strip())
        return wrapped_lines
    
    def animate(self, now):
        full_text = self.lines[self.current_line_index]
        if self.current_line_index < len(self.lines):
            if not self.line_fully_displayed and self.char_index < len(full_text):
                if now - self.last_update > self.letter_delay:
                    self.typed_text += full_text[self.char_index]
                    self.char_index += 1
                    self.last_update = now
                if self.char_index == len(full_text):
                    self.line_fully_displayed = True

        # Blink arrow
        if now - self.arrow_last_blink > self.blink_speed:
            self.arrow_visible = not self.arrow_visible
            self.arrow_last_blink = now

    def handle_dialogue_input(self, event):
        if event.type == pygame.KEYDOWN:
            # Handle ESC key to skip dialogue
            if event.key == pygame.K_ESCAPE:
                return 'skip'
            
            if self.line_fully_displayed:
                self.current_line_index += 1
                if self.current_line_index >= len(self.lines):
                    return 'done'
                else:
                    self.typed_text = ""
                    self.char_index = 0
                    self.line_fully_displayed = False
                    self.last_update = pygame.time.get_ticks()
            else:
                self.typed_text = self.lines[self.current_line_index]
                self.char_index = len(self.typed_text)
                self.line_fully_displayed = True
        return 'continue'
    
    def draw(self, surface):
        pygame.draw.rect(surface, TEXTBOX_DARK_GREY, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, TEXTBOX_LIGHT_GREY, self.rect, 3, border_radius=self.border_radius)

        wrapped_lines = self.wrap_text(self.typed_text)
        x_offset = self.rect.x + self.padding
        y_offset = self.rect.y + self.padding

        for i, line in enumerate(wrapped_lines):
            surface.blit(self.font.render(line, True, WHITE), (x_offset, y_offset + i * self.line_height))

        if self.line_fully_displayed and self.arrow_visible and self.show_arrow:
            pygame.draw.polygon(surface, WHITE, [
                (ARROW_X, ARROW_Y),
                (ARROW_X + ARROW_SIZE, ARROW_Y),
                (ARROW_X + ARROW_SIZE // 2, ARROW_Y + ARROW_SIZE)
            ])


class GameFlags:
    def __init__(self):
        self.has_started_dealing = False
        self.dealer_second_card_visible = False
        self.player_blackjack_stage = None
        self.dealer_turn_status = None

        self.intro_lines_set = False

        self.dealing_lines_set = False

        self.player_turn_lines_set = False
        self.player_stands_lines_ready = False
        self.player_stands_lines_set = False
        self.player_bust_lines_set = False

        self.dealer_turn_lines_set = False

        self.dealer_blackjack_lines_set = False
        self.dealer_bust_lines_set = False
        self.review_hands_lines_ready = False
        self.review_hands_lines_set = False
        self.endgame_lines_ready = False
        self.player_wins_lines_set = False
        self.dealer_wins_lines_set = False
        self.game_draw_lines_set = False

    def reset(self):
        for attr in vars(self):
            setattr(self, attr, False if isinstance(getattr(self, attr), bool) else None)
        

class GameState(Enum):
    INTRO = 0
    RESET = 1
    DEALING = 2
    PLAYER_TURN = 3
    DEALER_TURN = 4
    RESOLUTION = 5

class GameManager():
    def __init__(self):
        self.state = GameState.INTRO
        self.flags = GameFlags()
        self.deck = Deck()