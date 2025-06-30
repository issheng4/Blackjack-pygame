import random
import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    INTRO, DEALING, PLAYER_TURN, DEALER_TURN, RESOLUTION,
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
        return f"Card('{self.value}', '{self.suit}')"
    


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
    def __init__(self, font, rect, lines, letter_delay=LETTER_DELAY, blink_speed=ARROW_BLINK_SPEED_MS, padding=PADDING, line_height=LINE_HEIGHT, border_radius=TEXTBOX_BORDER_RADIUS):
        self.font = font
        self.rect = rect
        self.lines = lines

        self.letter_delay = letter_delay
        self.blink_speed = blink_speed
        self.padding = padding
        self.line_height = line_height
        self.border_radius = border_radius

        # Animation state
        self.current_line_index = 0
        self.typed_text = ""
        self.char_index = 0
        self.last_update = 0
        
        # Arrow state
        self.arrow_visible = True
        self.arrow_last_blink = 0

        self.line_fully_displayed = False

    def wrap_text(self, text, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())
        return lines
    
    def update(self, now):
        full_text = self.lines[self.current_line_index]
        if not self.line_fully_displayed and self.char_index < len(full_text):
            if now - self.last_update > self.letter_delay:
                self.typed_text += full_text[self.char_index]
                self.char_index += 1
                self.last_update = now
            if self.char_index == len(full_text):
                self.line_fully_displayed = True

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
    
    def handle_hit_or_stand_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                Person().receive_card()
            elif event.key == pygame.K_s:
                pass

    def draw(self, surface):
        pygame.draw.rect(surface, TEXTBOX_DARK_GREY, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, TEXTBOX_LIGHT_GREY, self.rect, 3, border_radius=self.border_radius)

        lines = self.wrap_text(self.typed_text, self.rect.width - self.padding)
        x_offset = self.rect.x + self.padding
        y_offset = self.rect.y + self.padding
        for i, line in enumerate(lines):
            surface.blit(self.font.render(line, True, WHITE), (x_offset, y_offset + i * self.line_height))

        if self.line_fully_displayed and self.arrow_visible:
            pygame.draw.polygon(surface, WHITE, [
                (ARROW_X, ARROW_Y),
                (ARROW_X + ARROW_SIZE, ARROW_Y),
                (ARROW_X + ARROW_SIZE // 2, ARROW_Y + ARROW_SIZE)
            ])


class GameState(Enum):
    INTRO = 0
    DEALING = 1
    PLAYER_TURN = 2
    DEALER_TURN = 3
    RESOLUTION = 4