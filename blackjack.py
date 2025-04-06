import random

VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUITS = ['spades', 'clubs', 'hearts', 'diamonds']

# populate deck
deck = []
for i in VALUES:
    for j in SUITS:
        deck.append((i, j))


# initialise player variables
player_name = 'player'
player_hand = []
player_total = 0
player_ace_eleven_count = 0

# initialise dealer variables
dealer_name = 'dealer'
dealer_hand = []
dealer_total = 0
dealer_ace_eleven_count = 0




# helper functions:

def receive_card(deck, hand, total, ace_as_eleven_count):
    '''person receives card, including adding onto points and ace check'''
 
    def value_to_points(value):
        '''convert value on card to points'''
        if value in ['J', 'Q', 'K']:
            return 10
        elif value == 'A':
            return 11
        else:
            return int(value)
        
    def update_ace_status(card, ace_as_eleven_count, total):
        '''determine whether an Ace should score 1 or 11'''
        if card == 'A':
            ace_as_eleven_count += 1
            if total > 21 and ace_as_eleven_count:
                total -= 10
                ace_as_eleven_count -= 1
        return ace_as_eleven_count, total
    
    hand.append(deck.pop())
    card = hand[-1][0]
    total += value_to_points(card)
    ace_as_eleven_count, total = update_ace_status(card, ace_as_eleven_count, total)
    return deck, hand, total, ace_as_eleven_count

 
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
random.shuffle(deck)

deck, player_hand, player_total, player_ace_eleven_count = receive_card(deck, player_hand, player_total, player_ace_eleven_count)
print()
print(f"//// {player_name}'s hand: {str(player_hand)}  ////")
print ()
deck, dealer_hand, dealer_total, dealer_ace_eleven_count = receive_card(deck, dealer_hand, dealer_total, dealer_ace_eleven_count)
print()
print(f"//// {dealer_name}'s hand: {str(dealer_hand)}  ////")
print ()

dialogue_next_line()

deck, player_hand, player_total, player_ace_eleven_count = receive_card(deck, player_hand, player_total, player_ace_eleven_count)
print()
print(f"//// {player_name}'s hand: {str(player_hand)}  TOTAL: {str(player_total)}  ////")
print ()
deck, dealer_hand, dealer_total, dealer_ace_eleven_count = receive_card(deck, dealer_hand, dealer_total, dealer_ace_eleven_count)
print()
print(f"//// {dealer_name}'s hand: [{str(dealer_hand[0])}, (hidden card)]  ////")
print ()

# blackjack checks
if player_total == 21:
    if dealer_total == 21:
        perform_endgame('none', 'blackjack')
    perform_endgame(player_name, 'blackjack', dealer_name)





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
        deck, player_hand, player_total, player_ace_eleven_count = receive_card(deck, player_hand, player_total, player_ace_eleven_count)
        print()
        print(f"//// {player_name}'s hand: {str(player_hand)}  TOTAL: {str(player_total)}  ////")
        print ()
        #check if player is bust
        if player_total > 21:
            perform_endgame(dealer_name, dealer_total, player_name, player_total)


print('Player chose to stand')
print()



# PHASE 3: dealer's turn

# dealer reveals card
print("Dealer's turn.... now to reveal their hidden card....")
dialogue_next_line()
print()
print(f"//// {dealer_name}'s hand: {str(dealer_hand)}  TOTAL: {str(dealer_total)}  ////")
print ()
dialogue_next_line()

# blackjack check
if dealer_total == 21:
    perform_endgame(dealer_name, 'blackjack', player_name)


# dealer hits until points total at least 17
if dealer_total >= 17:
    print("Dealer must stand when they have at least 17 points.")
else:
    print("Dealer must draw until they total at least 17 points.")
dialogue_next_line()

while dealer_total < 17:
    deck, dealer_hand, dealer_total, dealer_ace_eleven_count = receive_card(deck, dealer_hand, dealer_total, dealer_ace_eleven_count)
    print()
    print(f"//// {dealer_name}'s hand: {str(dealer_hand)}  TOTAL: {str(dealer_total)}  ////")
    print ()
    # check if dealer is bust
    if dealer_total > 21:
        perform_endgame(player_name, player_total, dealer_name, dealer_total)
    dialogue_next_line()





# PHASE 4: reviewing hands and revealling the winner
print("Time to review the hands")
dialogue_next_line()
if player_total == dealer_total:
    perform_endgame('none', player_total)
elif player_total > dealer_total:
    perform_endgame(player_name, player_total, dealer_name, dealer_total) 
else:
    perform_endgame(dealer_name, dealer_total, player_name, player_total)



