import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    INTRO, DEALING, PLAYER_TURN, DEALER_TURN, RESOLUTION,
    FONT_NAME, FONT_SIZE,
    WHITE, BLACK, TABLE_GREEN, BG_DARK_GREY, TEXTBOX_DARK_GREY, TEXTBOX_LIGHT_GREY, SHADOW,
    TEXTBOX_WIDTH, TEXTBOX_HEIGHT, TEXTBOX_X, TEXTBOX_Y, TEXTBOX_BORDER_RADIUS,
    LINE_HEIGHT, PADDING, LETTER_DELAY, MAX_TEXT_WIDTH,
    ARROW_BLINK_SPEED_MS, ARROW_SIZE, ARROW_X, ARROW_Y,
    CARD_WIDTH, CARD_HEIGHT,
    FIRST_PLAYER_CARD_X, FIRST_PLAYER_CARD_Y, PLAYER_CARD_DISPLACEMENT_X, PLAYER_CARD_DISPLACEMENT_Y, FIRST_DEALER_CARD_X, FIRST_DEALER_CARD_Y, DEALER_CARD_DISPLACEMENT_X,
    SCOREBOARD_TEXT_X, SCOREBOARD_TITLE_Y, SCOREBOARD_PLAYER_Y, SCOREBOARD_DEALER_Y,
    CARD_BACK,
)
from dialogue import INTRO_DIALOGUE_LINES, player_turn_lines, HIT_OR_STAND_INPUT
from game_objects import Card, Deck, Hand, Person, TextBoxController, GameState


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")
font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
clock = pygame.time.Clock()

# Game objects
player = Person('player', 'Player')
dealer = Person('dealer', 'The Dealer')
deck = Deck()
deck.shuffle()

# Game state
game_state = GameState.INTRO
running = True
dt = 0
now = 0

# Text box
text_rect = pygame.Rect(TEXTBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
textbox = TextBoxController(font, text_rect)

# Dialogue flags
intro_lines_set = False
dealing_lines_set = False
blackjack_stage = 'not_started'
player_turn_lines_set = False
player_stands_lines_ready = False
player_stands_lines_set = False
player_bust_lines_ready = False
player_bust_lines_set = False
resolution_lines_set = False
dealer_second_card_hiden = True

# Deal timing events
DEAL_PLAYER_1 = pygame.USEREVENT + 1
DEAL_DEALER_1 = pygame.USEREVENT + 2
DEAL_PLAYER_2 = pygame.USEREVENT + 3
DEAL_DEALER_2 = pygame.USEREVENT + 4
DEAL_DONE = pygame.USEREVENT + 5
has_started_dealing = False

manual_hand_input_for_testing = True



# -------------------------------------
# 1. Handling inputs
# ---------------------------------------

def handle_intro_input(event):
    global game_state    
    result = textbox.handle_dialogue_input(event)
    if result == 'done' or result == 'skip':
        game_state = GameState.DEALING



def handle_dealing_input(event):
    global has_started_dealing, game_state, manual_hand_input_for_testing
    if game_state == GameState.DEALING and has_started_dealing == False:
        pygame.time.set_timer(DEAL_PLAYER_1, 300, loops=1)
        pygame.time.set_timer(DEAL_DEALER_1, 600, loops=1)
        pygame.time.set_timer(DEAL_PLAYER_2, 900, loops=1)
        pygame.time.set_timer(DEAL_DEALER_2, 1200, loops=1)
        has_started_dealing = True

    if manual_hand_input_for_testing == False:
        if event.type == DEAL_PLAYER_1:
            player.hand.add_card(Card('A', 'spades'))

        elif event.type == DEAL_DEALER_1:
            dealer.hand.add_card(Card('Q', 'spades'))

        elif event.type == DEAL_PLAYER_2:
            player.hand.add_card(Card('K', 'spades'))

        elif event.type == DEAL_DEALER_2:
            dealer.hand.add_card(Card('10', 'spades'))
            pygame.time.set_timer(DEAL_DONE, 20, loops=1)

    else:
        if event.type == DEAL_PLAYER_1:
            player.receive_card(deck)

        elif event.type == DEAL_DEALER_1:
            dealer.receive_card(deck)

        elif event.type == DEAL_PLAYER_2:
            player.receive_card(deck)

        elif event.type == DEAL_DEALER_2:
            dealer.receive_card(deck)
            pygame.time.set_timer(DEAL_DONE, 20, loops=1)

    if event.type == DEAL_DONE:
        print(f"//// {player.name}'s hand: {player.hand}  TOTAL: {player.calculate_hand_total()}  ////")
        print(f"//// {dealer.name}'s hand: {dealer.hand}  TOTAL: {dealer.calculate_hand_total()}  ////")
        game_state = GameState.PLAYER_TURN



def handle_player_turn_input(event):
    global game_state, player_stands_lines_ready, player_stands_lines_set
    global player_turn_lines_set, player_bust_lines_set, blackjack_stage

    if event.type != pygame.KEYDOWN:
        return

    # If bust text is active
    if player_bust_lines_set:
        result = textbox.handle_dialogue_input(event)
        if result == 'done':
            game_state = GameState.RESOLUTION
        return

    # Blackjack flow
    if blackjack_stage != 'not_started':
        result = textbox.handle_dialogue_input(event)
        if result == 'done':
            if blackjack_stage == 'reveal':
                blackjack_stage = 'resolve'
            elif blackjack_stage == 'done':
                game_state = GameState.RESOLUTION
        return

    # If stand dialogue is active
    if player_stands_lines_set:
        result = textbox.handle_dialogue_input(event)
        if result == 'done':
            game_state = GameState.DEALER_TURN
        return

    # Hit or Stand phase
    if not player_stands_lines_ready:
        # Only allow progressing if the textbox is not in the hit/stand prompt
        if event.key == pygame.K_h and textbox.line_fully_displayed:
            player.receive_card(deck)
            print(f"//// {player.name}'s hand: {player.hand}  TOTAL: {player.hand.total}  ////")
            textbox.handle_dialogue_input(event)

        elif event.key == pygame.K_s:
            player_stands_lines_ready = True

        elif event.key == pygame.K_r:
            game_state = GameState.RESOLUTION




            
        

def handle_dealer_turn_input(event):    
    pass

def handle_resolution_input(event):    
    pass






# -------------------------------------
# 2. Updating logic
# ---------------------------------------

def update_intro(now):
    global intro_lines_set
    if not intro_lines_set:
        textbox.set_lines(INTRO_DIALOGUE_LINES)
        intro_lines_set = True
    textbox.animate(now)


def update_dealing(now):
    global dealing_lines_set, game_state

    if not dealing_lines_set:
        textbox.set_lines(["And I deal..."],show_arrow=False)
        dealing_lines_set = True
    textbox.animate(now)

    
def update_player_turn(now):
    global blackjack_stage, game_state, dealer_second_card_hiden, player_bust_lines_set, player_turn_lines_set, player_stands_lines_set

    if len(player.hand.cards) == 2 and player.hand.total == 21:

        if blackjack_stage == 'not_started':
            blackjack_stage = 'start'

        if blackjack_stage == 'start':
            # Dealer cannot have blackjack
            if dealer.hand.cards[0].value not in ['10', 'J', 'Q', 'K', 'A']:
                textbox.set_lines(["Wow, you got a blackjack!", "Let's go again."])
                blackjack_stage = 'done'
                player.games_won += 1

            else:
                # Dealer might have blackjack — wait before revealing
                textbox.set_lines(["Wow, you got a blackjack!", "Let's see if I've got one too...", " "])
                blackjack_stage = 'reveal'

        elif blackjack_stage == 'reveal':
            # Wait for user to finish reading line 1
            if textbox.line_fully_displayed and textbox.current_line_index == 2:
                dealer_second_card_hiden = False
                if len(dealer.hand.cards) == 2 and dealer.hand.total == 21:
                    textbox.set_lines(["I have a blackjack too!", "Looks like it's a draw.", "Let's go again."])
                else:
                    textbox.set_lines(["Ah, I don't have a blackjack.", "You've won this time!", "Let's go again."])
                    player.games_won += 1
                blackjack_stage = 'done'

        textbox.animate(now)
        return

    
    if player.hand.total > 21:
        # Player has bust
        if not player_bust_lines_set:
            textbox.set_lines(["Ah! Looks like you've bust.", "Let's go again."])
            player_bust_lines_set = True
            dealer.games_won += 1

    elif not player_turn_lines_set:
        # Standard player turn
        textbox.set_lines(HIT_OR_STAND_INPUT, show_arrow=False)
        player_turn_lines_set = True

    elif player_stands_lines_ready and not player_stands_lines_set:
        # Stand dialogue
        textbox.set_lines(["You stand, alright.", "Now it's my turn."])
        player_stands_lines_set = True

    textbox.animate(now)





def update_dealer_turn(now):
    print("Dealer turn, yay")

def game_reset():
    global game_state, deck, intro_lines_set, dealing_lines_set, blackjack_stage, player_turn_lines_set, resolution_lines_set, player_stands_lines_ready, player_stands_lines_set, player_bust_lines_set, player_bust_lines_ready, dealer_second_card_hiden
    intro_lines_set = False
    dealing_lines_set = False
    blackjack_stage = 'not_started'
    player_turn_lines_set = False
    player_stands_lines_ready = False
    player_stands_lines_set = False
    player_bust_lines_ready = False
    player_bust_lines_set = False
    resolution_lines_set = False
    dealer_second_card_hiden = True
    player.reset_hand()
    dealer.reset_hand()
    deck = Deck()
    deck.shuffle()
    print(f'=====  GAME SCORE [ {player.name}: {player.games_won} | {dealer.name}: {dealer.games_won} ]  =====')
    game_state = GameState.DEALING

def update_resolution(now):
    global has_started_dealing, game_state, deck, resolution_lines_set
    has_started_dealing = False

    if not resolution_lines_set:
        textbox.set_lines(["..."],show_arrow=False)
        resolution_lines_set = True
    textbox.animate(now)

    if resolution_lines_set:
        game_reset()
    




# -------------------------------------
# 3. Drawing on screen
# ---------------------------------------

def draw_scoreboard():
    scoreboard_title = font.render(f"Games Won", True, WHITE)
    scoreboard_player = font.render(f"Player: {player.games_won}", True, WHITE)
    scoreboard_dealer = font.render(f"Dealer: {dealer.games_won}", True, WHITE)

    screen.blit(scoreboard_title, (SCOREBOARD_TEXT_X, SCOREBOARD_TITLE_Y))
    screen.blit(scoreboard_player, (SCOREBOARD_TEXT_X, SCOREBOARD_PLAYER_Y))
    screen.blit(scoreboard_dealer, (SCOREBOARD_TEXT_X, SCOREBOARD_DEALER_Y))




def draw_playing():
    global dealer_second_card_hiden
    player_x, player_y = FIRST_PLAYER_CARD_X, FIRST_PLAYER_CARD_Y
    dealer_x, dealer_y = FIRST_DEALER_CARD_X, FIRST_DEALER_CARD_Y

    for i, card in enumerate(player.hand.cards):
        card.render(screen, player_x, player_y)
        player_x += PLAYER_CARD_DISPLACEMENT_X
        player_y -= PLAYER_CARD_DISPLACEMENT_Y

    for i, card in enumerate(dealer.hand.cards):
        if i == 1 and dealer_second_card_hiden:
            screen.blit(CARD_BACK, (dealer_x, dealer_y))
        else:
            card.render(screen, dealer_x, dealer_y)
        dealer_x -= DEALER_CARD_DISPLACEMENT_X

    draw_scoreboard()


def draw_screen():
    if game_state == GameState.INTRO and textbox.current_line_index < 11:
        screen.fill(BG_DARK_GREY)
    else:
        screen.fill(TABLE_GREEN)

    textbox.draw(screen)

    if game_state in [GameState.DEALING, GameState.PLAYER_TURN, GameState.DEALER_TURN, GameState. RESOLUTION]:
        draw_playing()

    pygame.display.flip()




# -------------------------------------
# MAIN LOOP
# ---------------------------------------

while running:
    dt = clock.tick(60)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == GameState.INTRO:
            handle_intro_input(event)
        elif game_state == GameState.DEALING:
            handle_dealing_input(event)
        elif game_state == GameState.PLAYER_TURN:
            handle_player_turn_input(event)
        elif game_state == GameState.DEALER_TURN:
            handle_dealer_turn_input(event)
        elif game_state == GameState.RESOLUTION:
            handle_resolution_input(event)

    # Update state
    if game_state == GameState.INTRO:
        update_intro(now)
    elif game_state == GameState.DEALING:
        update_dealing(now)
    elif game_state == GameState.PLAYER_TURN:
        update_player_turn(now)
    elif game_state == GameState.DEALER_TURN:
        update_dealer_turn(now)
    elif game_state == GameState.RESOLUTION:
        update_resolution(now)

    # Render frame
    draw_screen()

pygame.quit()