import random

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
    
    def get_points(self, total):
        if self.value in ['J', 'Q', 'K']:
            return 10
        elif self.value == 'A':
            return 11 # will be adjusted to 1 later if necessary
        else:
            return int(self.value)
        
    def __repr__(self):
        return f"Card('{self.value}', '{self.suit}')"

    def __str__(self):
        return f'[ {self.value} {self._SUIT_SYMBOLS[self.suit]} ]'
    


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
    
    def __str__(self):
        return ' '.join(str(card) for card in self.cards)


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
    
    def __repr__(self):
        return self.name
