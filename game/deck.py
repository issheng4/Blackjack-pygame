import random
from .card import Card

class Deck:
    def __init__(self):
        self.cards = []
        for value in Card.VALUES:
            for suit in Card.SUITS:
                self.cards.append(Card(value, suit))
                    
    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def __repr__(self):
        return str(self.cards)
