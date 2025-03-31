import random

VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUITS = ['spades', 'clubs', 'hearts', 'diamonds']

# populate deck
deck = []
for i in VALUES:
    for j in SUITS:
        deck.append((i, j))


# initialise hands and scores
player_hand = []
dealer_hand = []
player_total = 0
dealer_total = 0


# function to convert value on card to a score
def value_to_score(value):
    if value in ['J', 'Q', 'K']:
        return 10
    elif value == 'A':
        return 11
    else:
        return int(value)
    
# function to display player's hand onscreen
def show_player_hand():
    print()
    print(f"////  player's hand: {str(player_hand)}  TOTAL: {str(player_total)}  ////")
    print ()

# function to display dealer's hand onscreen
def show_dealer_hand():
    print(f"////  dealer's hand: {str(dealer_hand)}  TOTAL: {str(dealer_total)}  ////")
    print()

# initialise Ace as 11 count
player_ace_as_eleven_count = 0
dealer_ace_as_eleven_count = 0





# PHASE 1: dealing


# shuffle deck
random.shuffle(deck)

# player gets 1 card (visible)
player_hand.append(deck.pop())
player_total += value_to_score(player_hand[-1][0])
### function: player ace check
if player_hand[-1][0] == 'A':
    player_ace_as_eleven_count += 1
    if player_total > 21 and player_ace_as_eleven_count:
        player_total -= 10
        player_ace_as_eleven_count -= 1

# dealer gets 1 card (visible)
dealer_hand.append(deck.pop())
dealer_total += value_to_score(dealer_hand[-1][0])
### function: dealer ace check
if dealer_hand[-1][0] == 'A':
    dealer_ace_as_eleven_count += 1
    if dealer_total > 21 and dealer_ace_as_eleven_count:
        dealer_total -= 10
        dealer_ace_as_eleven_count -= 1

# player gets 1 more card (visible)
player_hand.append(deck.pop())
player_total += value_to_score(player_hand[-1][0])
### function: player ace check
if player_hand[-1][0] == 'A':
    player_ace_as_eleven_count += 1
    if player_total > 21 and player_ace_as_eleven_count:
        player_total -= 10
        player_ace_as_eleven_count -= 1

# dealer gets 1 more card (hidden)
dealer_hand.append(deck.pop())
dealer_total += value_to_score(dealer_hand[-1][0])
### function: dealer ace check
if dealer_hand[-1][0] == 'A':
    dealer_ace_as_eleven_count += 1
    if dealer_total > 21 and dealer_ace_as_eleven_count:
        dealer_total -= 10
        dealer_ace_as_eleven_count -= 1



# show cards
show_player_hand()
# show dealer hand including hidden card
print(f"////  dealer's hand: {str(dealer_hand[0])}, [hidden card]  ////")
print()


# blackjack checks
if player_total == 21:
    if value_to_score(dealer_hand[0][0]) >= 10:
        print("Player has a blackjack?? Let's see if the dealer does too")
        print()
        show_dealer_hand()
        # if dealer has a blackjack
        if dealer_total == 21:
            print("***GAME DRAW: both the player and dealer have blackjacks!***")
            print()
            quit()
    print("***PLAYER WINS: blackjack!***")
    print()
    quit()








# PHASE 2: player's turn

# initialise player's choice of move
move = 0

# while player chooses a move other than stand
while move != 's':
    print("Hit or stick?")
    # player chooses move
    move = input("(type 'h' to hit and 's' to stick) ")
    print()
    # if player chooses to hit
    if move == 'h':
        # player receives another card
        player_hand.append(deck.pop())
        player_total += value_to_score(player_hand[-1][0])
        ### function: player ace check
        if player_hand[-1][0] == 'A':
            player_ace_as_eleven_count += 1
            if player_total > 21 and player_ace_as_eleven_count:
                player_total -= 10
                player_ace_as_eleven_count -= 1
        show_player_hand()

        # check if player is bust
        if player_total > 21:
            print("***DEALER WINS: player has bust!***")
            print()
            quit()


print('Player chose to stand')
print()






# PHASE 3: dealer's turn

# dealer reveals card
print("The dealer shall reveal their hidden card")
print()
show_dealer_hand()

# blackjack check
if dealer_total == 21:
    print("***DEALER WINS: blackjack!***")
    print()
    quit()


# dealer hits until score is at least 17
while dealer_total < 17:
    # dealer receives another card
    dealer_hand.append(deck.pop())
    dealer_total += value_to_score(dealer_hand[-1][0])
    ### function: dealer ace check
    if dealer_hand[-1][0] == 'A':
        dealer_ace_as_eleven_count += 1
        if dealer_total > 21 and dealer_ace_as_eleven_count:
            dealer_total -= 10
            dealer_ace_as_eleven_count -= 1
    show_dealer_hand()

        # check if dealer is bust
if dealer_total > 21:
    print("***PLAYER WINS: dealer has bust!***")
    print()
    quit()






# PHASE 4: reviewing hands
print("Time to review the hands")

if player_total > dealer_total:
    print(f"***PLAYER WINS: player scored {player_total} and dealer scored {dealer_total}***")
    print()
    quit()
elif player_total < dealer_total:
    print(f"***DEALER WINS: player scored {player_total} and dealer scored {dealer_total}***")
    print()
    quit()
else:
    print(f"***GAME DRAW: both player and dealer scored {player_total}***")
    print()
    quit()



