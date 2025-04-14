def dialogue_next_line():
    '''player presses enter key to continue'''
    print()
    input('(press enter to continue.....)')
    print()


def perform_endgame(winner, winner_points, loser=None, loser_points=None):
    print() 

    if winner == 'none':
        print('*** GAME DRAW ***')
        print(f"both the player and dealer have {winner_points}!")

    elif winner_points == 'blackjack':
        print(f'*** {winner.upper()} WINS ***')
        print(f'{winner} got a blackjack!')

    elif loser_points > 21:
        print(f'*** {winner.upper()} WINS ***')
        print(f'{loser} went bust!')

    else:
        print(f'*** {winner.upper()} WINS ***')
        print(f'{winner} has {winner_points} // {loser} has {loser_points}')
    
    
    print()
    print('Lets go again!')
    dialogue_next_line()
    return



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
