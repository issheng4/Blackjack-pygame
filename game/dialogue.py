from dataclasses import dataclass

@dataclass(frozen=True)
class DialogueStrings:
    """Game dialogue organized by game state."""
    
    class Intro:
        """Introduction sequence dialogue."""
        SEQUENCE = [
            "Welcome to Blackjack!",
            "My name is The Dealer.",
            "Today, we'll be playing some rounds of blackjack.",
            "No gambling though. I'm here to showcase the beauty, the artistry of this fine card game.",
            "Not here to partake in the devious act of gambling.",
            "Instead...",
            "We can track the number of games each of us have won.",
            "Are you familiar with the rules?",
            "...",
            "Well... let me give you a rundown on them anyway.",
            "Let's bring the table in.",
            "...", # table appears on screen
            "There we go.",
            "The rules are simple.",
            "The aim of the game is to beat me, The Dealer.",
            "Your goal is to get as close to 21 as possible, by totalling the value of the cards in your hand.",
            "Face cards are worth 10, and aces are worth either 1 or 11.",
            "You'll start with two cards.",
            "You can hit to take another card, or stand to keep what you've got.",
            "But no going over 21, otherwise you go bust and lose.",
            "Now for me, The Dealer.",
            "I also get 2 cards at the start, one of them hidden at first.",
            "But when it is my turn, I reveal the card and need to hit until I reach at least 17.",
            "Oh, one more thing.",
            "If you get an ace and a ten-value card straight away, that's a blackjack, and you win!",
            "Well.. unless I also get a blackjack... then it's a draw.",
            "...",
            "Finally, in case you're interested...",
            "We're playing with a single deck of cards, and I shuffle it before each game.",
            "So, no counting cards here.",
            "...",
            "Anywhom...",
            "Let's play!"
        ]
    
    class Dealing:
        """Dealing phase dialogue."""
        BASIC = ["And I deal..."]
        PLAYER_BLACKJACK = ["Wow, you got a blackjack!", "Let's go again."]
        PLAYER_BLACKJACK_DEALER_CHECK = ["Wow, you got a blackjack!", "But wait a moment.", 
                                "Let's see if I've got one too...", " "]
        DEALER_ALSO_BLACKJACK = ["I have a blackjack too!", "Looks like it's a draw.", 
                                "Let's go again."]
        DEALER_NO_BLACKJACK = ["Ah, I don't have a blackjack.", "You've won this time!", 
                              "Let's go again."]
    
    class PlayerTurn:
        """Player turn dialogue."""
        HIT_OR_STAND = [
            "Your turn. Press [H] to hit or [S] to stand.",
            "Good choice. Press [H] to hit or [S] to stand.",
            "Nice. Press [H] to hit or [S] to stand.",
            "Getting a lot of cards. Press [H] to hit or [S] to stand.",
            "Now, now. Press [H] to hit or [S] to stand.",
            "Crikey. Press [H] to hit or [S] to stand.",
            "This is getting a bit silly. Press [H] to hit or [S] to stand."
            "Still going? Press [H] to hit or [S] to stand.",
            "Have you broken the game?? There is a 1 in 15 billion chance of this perfect set of cards appearing.",
            "Okay."
        ]
        BUST = ["Ah! Looks like you've bust.", "Let's go again."]
        STAND = ["You stand, alright.", "Now it's my turn."]
    
    class DealerTurn:
        """Dealer turn dialogue."""
        START = ["I hit until I reach 17..."]
        WINS_BLACKJACK = ["Oh, I've got a blackjack!", "That's a game won for The Dealer.", 
                         "Let's go again!"]
        BUST = ["Ah! Looks like I have bust.", "So you win this time.", "Another game!"]
    
    class Resolution:
        """Game resolution dialogue."""
        REVIEW_TEMPLATE = ["And now we review our hands to see who has won this time.", 
                          "You have {} and I have {}."]
        PLAYER_WINS = ["You win this time!", "Let's go again."]
        DEALER_WINS = ["I win this time!", "Let's go again."]
        DRAW = ["So it's a draw this time round.", "Let's go again."]


