import pygame
from .constants import Audio
from .hand import Hand

class Person:
    def __init__(self, role):
        if role not in ('player', 'dealer'):
            raise ValueError("Role must be 'player' or 'dealer'")
        
        self.role = role
        self.hand = Hand()
        self.games_won = 0

        if self.role == 'player':
            self.win_sound = pygame.mixer.Sound(Audio.PLAYER_WIN)
        else:
            self.win_sound = pygame.mixer.Sound(Audio.DEALER_WIN)
        self.win_sound.set_volume(Audio.GAME_WIN_VOLUME)

    def receive_card(self, deck):
        card = deck.deal_card()
        self.hand.add_card(card)

    def calculate_hand_total(self):
        return self.hand.calculate_total()
    
    def reset_hand(self):
        self.hand = Hand()
    
    def win_game(self):
        self.games_won += 1
        self.win_sound.play()
    
    def __repr__(self):
        return self.role
