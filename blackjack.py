from game_objects import Card, Deck, Hand, Person
from utils import dialogue_next_line, perform_endgame


# initialise class variables
player = Person('player', 'Playerrr')
dealer = Person('dealer', 'Dealerrr')
deck = Deck()


def main():

    # PHASE 1: dealing

    print()
    print()
    print("Welcome to this game of blackjack! Let's deal....")
    dialogue_next_line()


    # shuffle deck
    deck.shuffle()
    print(deck)

    player.draw_card(deck)
    print(player.hand)
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
        if dealer.hand.calculate_total() == 21:
            perform_endgame('none', 'blackjack')
        perform_endgame(player.name, 'blackjack', dealer.name)





    # PHASE 2: player's turn

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


    print('Player chose to stand')
    print()



    # PHASE 3: dealer's turn

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
        dialogue_next_line()





    # PHASE 4: reviewing hands and revealling the winner
    print("Time to review the hands")
    dialogue_next_line()
    if player.calculate_hand_total() == dealer.calculate_hand_total():
        perform_endgame('none', player.calculate_hand_total())
    elif player.calculate_hand_total() > dealer.calculate_hand_total():
        perform_endgame(player.name, player.calculate_hand_total(), dealer.name, dealer.calculate_hand_total()) 
    else:
        perform_endgame(dealer.name, dealer.calculate_hand_total(), player.name, player.calculate_hand_total())


if __name__ == '__main__':
    main()


