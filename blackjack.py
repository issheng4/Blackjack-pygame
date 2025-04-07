from game_objects import Card, Deck, Hand, Person


# initialise class variables
player = Person('player', 'Playerrr')
dealer = Person('dealer', 'Dealerrr')
deck = Deck()



# helper functions:

 
def dialogue_next_line():
    '''player presses enter key to continue'''
    print()
    input('(press enter to continue.....)')
    print()


def perform_endgame(winner, winner_points, loser=0, loser_points=0):
    print()    
    if winner == 'none':
        print('*** GAME DRAW ***')
        print(f"both the player and dealer have {winner_points}!")
        print()
        print()
        quit()
    
    print(f'*** {winner.upper()} WINS ***')

    if winner_points == 'blackjack':
        print(f'{winner} got a blackjack!')
        print()
        print()
        quit()
    if loser_points > 21:
        print(f'{loser} went bust!')
        print()
        print()
        quit()
    print(f'{winner} has {winner_points} // {loser} has {loser_points}')
    print()
    print()
    quit()



""" # may implement this back in
def show_player_hand():
    '''display player's hand onscreen'''
    print()
    print(f"////  player's hand: {str(player_hand)}  TOTAL: {str(player_total)}  ////")
    print ()


def show_dealer_hand():
    '''display dealer's hand onscreen'''
    print(f"////  dealer's hand: {str(dealer_hand)}  TOTAL: {str(dealer_total)}  ////")
    print()
"""



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
    if dealer.hand.calculate_total() == 21:
        perform_endgame('none', 'blackjack')
    perform_endgame(player.name, 'blackjack', dealer.name)





# PHASE 2: player's turn

# initialise player's choice of move
move = 0

# while player chooses a move other than stand
while move != 's':
    print()
    print('Hit or stick?')
    print("(type 'h' to hit or 's' to stick)")
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



