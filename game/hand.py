import pygame
from .constants import Audio

class Hand:
    def __init__(self):
        self.cards = []
        self.card_draw_sound = pygame.mixer.Sound(Audio.CARD_DRAW)
        self.card_draw_sound.set_volume(Audio.CARD_DRAW_VOLUME)

    def add_card(self, card):
        self.cards.append(card)
        self.card_draw_sound.play()

    def calculate_total(self):
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
    
    def make_hidden_card_reveal_sound(self):
        self.card_draw_sound.play()

    def __repr__(self):
        return str(self.cards)
    
    @property
    def total(self):
        return self.calculate_total()
