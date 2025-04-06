import random

VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUITS = ['spades', 'clubs', 'hearts', 'diamonds']

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def calculate_points(self, total):
        if self.value in ['J', 'Q', 'K']:
            return 10
        elif self.value == 'A':
            if total <= 10:
                return 11
            else:
                return 1
        else:
            return int(value)
        
    def __repr__(self):
        return f"Card('{self.value}', '{self.suit}')"

    def __str__(self):
        return f'[{self.value} | {self.suit}]'
    


class Deck:
    def __init__(self):
        self.cards = []
        for i in VALUES:
            for j in SUITS:
                self.cards.append(Card(i, j))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        self.cards.pop()



class Hand:
    def __init__(self):
        self.cards = []



class Person:
    def __init__(self, role, name):
        self.role = role # player or dealer
        self.name = name
        self.hand = Hand()
        self.points_in_hand = 0
        self.games_won = 0

    def __str__(self):
        return self.name