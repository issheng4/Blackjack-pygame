import random
import pygame
from constants import CARD_WIDTH, CARD_HEIGHT

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
            resized_image = pygame.transform.scale(raw_image, (CARD_WIDTH, CARD_HEIGHT))
            return resized_image
        except pygame.error as e:
            print(f'Error loading card image {filename}: {e}')
            return None
        
    def draw(self, surface, x, y):
        if self.image:
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

    def draw_card(self, deck):
        card = deck.deal_card()
        self.hand.add_card(card)

    def calculate_hand_total(self):
        return self.hand.calculate_total()
    
    def reset_hand(self):
        self.hand = Hand()
    
    def __repr__(self):
        return self.name
