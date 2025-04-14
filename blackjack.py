from game_objects import Card, Deck, Hand, Person
from utils import dialogue_next_line, perform_endgame


def main():
    player = Person('player', 'Playerrr')
    dealer = Person('dealer', 'Dealerrr')
    
    print()
    print("Welcome to this game of blackjack! Let's deal.......")
    dialogue_next_line()
    
    while True:
        
        player.reset_hand()
        dealer.reset_hand()
        deck = Deck()
        deck.shuffle()
        
        winner = play_game(deck, player, dealer)

        winner.games_won += 1
        print(f'=====  GAME SCORE [ {player.name}: {player.games_won} | {dealer.name}: {dealer.games_won} ]  =====')
        dialogue_next_line()



def play_game(deck, player, dealer):
    # ---------------------------------------------------
    # PHASE 1: dealing
    # ---------------------------------------------------

    player.draw_card(deck)
    print()
    print(f"//// {player.name}'s hand: {player.hand}  ////")
    print ()
    dealer.draw_card(deck)
    print()
    print(f"//// {dealer.name}'s hand: {dealer.hand}  ////")
    print ()

    dialogue_next_line()

    player.draw_card(deck)
    print()
    print(f"//// {player.name}'s hand: {player.hand}  TOTAL: {player.calculate_hand_total()}  ////")
    print ()
    dealer.draw_card(deck)
    print()
    print(f"//// {dealer.name}'s hand: {dealer.hand.cards[0]}, [ *** ]  ////") # dealer's hidden card
    print ()

    # blackjack checks
    if player.hand.calculate_total() == 21:
        print()
        if dealer.hand.cards[0].value in ['J', 'Q', 'K', 'A']:
            print("Wow, a blackjack! Let's reveal the dealer's hidden card and see if I have one too....")
            dialogue_next_line()
            print(f"//// {dealer.name}'s hand: {dealer.hand}  TOTAL: {dealer.calculate_hand_total()}  ////")
            dialogue_next_line()
            if dealer.hand.calculate_total() == 21:
                perform_endgame('none', 'blackjack')
                return None
        perform_endgame(player.name, 'blackjack', dealer.name)
        return player




    # ---------------------------------------------------
    # PHASE 2: player's turn
    # ---------------------------------------------------

    # initialise player's choice of move
    move = 0

    # while player chooses a move other than stand
    while move != 's':
        print()
        print('Hit or stand?')
        print("(type 'h' to hit or 's' to stand)")
        move = input()
        print()
        if move == 'h':
            player.draw_card(deck)
            print()
            print(f"//// {player.name}'s hand: {player.hand}  TOTAL: {player.calculate_hand_total()}  ////")
            print ()
            #check if player is bust
            if player.calculate_hand_total() > 21:
                perform_endgame(dealer.name, dealer.calculate_hand_total(), player.name, player.calculate_hand_total())
                return dealer


    print('Player chose to stand')
    print()




    # ---------------------------------------------------
    # PHASE 3: dealer's turn
    # ---------------------------------------------------

    # dealer reveals card
    print("Dealer's turn.... now to reveal their hidden card....")
    dialogue_next_line()
    print()
    print(f"//// {dealer.name}'s hand: {str(dealer.hand)}  TOTAL: {str(dealer.calculate_hand_total())}  ////")
    print ()
    dialogue_next_line()

    # blackjack check
    if dealer.calculate_hand_total() == 21:
        perform_endgame(dealer.name, 'blackjack', player.name)
        return dealer


    # dealer hits until points total at least 17
    if dealer.calculate_hand_total() >= 17:
        print("Dealer must stand when they have at least 17 points.")
    else:
        print("Dealer must draw until they total at least 17 points.")
    dialogue_next_line()

    while dealer.calculate_hand_total() < 17:
        dealer.draw_card(deck)
        print()
        print(f"//// {dealer.name}'s hand: {str(dealer.hand)}  TOTAL: {str(dealer.calculate_hand_total())}  ////")
        print ()
        # check if dealer is bust
        if dealer.calculate_hand_total() > 21:
            perform_endgame(player.name, player.calculate_hand_total(), dealer.name, dealer.calculate_hand_total())
            return player
        dialogue_next_line()


    
    # ---------------------------------------------------
    # PHASE 4: reviewing hands and revealing the winner
    # ---------------------------------------------------


    print("Time to review the hands")
    dialogue_next_line()
    if player.calculate_hand_total() == dealer.calculate_hand_total():
        perform_endgame('none', player.calculate_hand_total())
        return None
    elif player.calculate_hand_total() > dealer.calculate_hand_total():
        perform_endgame(player.name, player.calculate_hand_total(), dealer.name, dealer.calculate_hand_total()) 
        return player
    else:
        perform_endgame(dealer.name, dealer.calculate_hand_total(), player.name, player.calculate_hand_total())
        return dealer


if __name__ == '__main__':
    main()


