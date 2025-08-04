import random
import logging
from typing import List
from .card import Card

class Deck:
    """Represents a standard deck of 52 playing cards."""
    
    def __init__(self) -> None:
        """Initialize a new deck with all 52 cards."""
        self.cards: List[Card] = []
        for value in Card.VALUES:
            for suit in Card.SUITS:
                self.cards.append(Card(value, suit))
    
    def shuffle(self) -> None:
        """Randomly shuffle all cards in the deck."""
        random.shuffle(self.cards)
    
    def deal_card(self) -> Card:
        """Deal one card from the top of the deck.
        
        Returns:
            Card: The card that was dealt
            
        Raises:
            IndexError: If the deck is empty
        """
        if not self.cards:
            logging.error("Attempted to deal from an empty deck")
            raise IndexError("Cannot deal from an empty deck")
        return self.cards.pop()
    
    def __repr__(self) -> str:
        """Return string representation of the deck.
        
        Returns:
            str: String showing all cards in the deck
        """
        return str(self.cards)
