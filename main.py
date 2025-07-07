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
player = Person('player', 'You')
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
player_turn_lines_set = False
'''endgame_lines_set = False'''

# Deal timing events
DEAL_PLAYER_1 = pygame.USEREVENT + 1
DEAL_DEALER_1 = pygame.USEREVENT + 2
DEAL_PLAYER_2 = pygame.USEREVENT + 3
DEAL_DEALER_2 = pygame.USEREVENT + 4
DEAL_DONE = pygame.USEREVENT + 5
has_started_dealing = False



# -------------------------------------
# 1. Handling inputs
# ---------------------------------------

def handle_intro_input(event):
    global game_state    
    result = textbox.handle_dialogue_input(event)
    if result == 'done' or result == 'skip':
        game_state = GameState.DEALING



def handle_dealing_input(event):
    global has_started_dealing, game_state
    if game_state == GameState.DEALING and has_started_dealing == False:
        pygame.time.set_timer(DEAL_PLAYER_1, 300, loops=1)
        pygame.time.set_timer(DEAL_DEALER_1, 600, loops=1)
        pygame.time.set_timer(DEAL_PLAYER_2, 900, loops=1)
        pygame.time.set_timer(DEAL_DEALER_2, 1200, loops=1)
        has_started_dealing = True

    if event.type == DEAL_PLAYER_1:
        player.receive_card(deck)

    elif event.type == DEAL_DEALER_1:
        dealer.receive_card(deck)

    elif event.type == DEAL_PLAYER_2:
        player.receive_card(deck)

    elif event.type == DEAL_DEALER_2:
        dealer.receive_card(deck)
        pygame.time.set_timer(DEAL_DONE, 20, loops=1)

    elif event.type == DEAL_DONE:
        print(f"//// {player.name}'s hand: {player.hand}  TOTAL: {player.calculate_hand_total()}  ////")
        game_state = GameState.PLAYER_TURN



def handle_player_turn_input(event):    
    global game_state, has_started_dealing
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_h:
            player.receive_card(deck)
        # reset hand - for testing
        if event.key == pygame.K_r:
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
    textbox.update(now)


def update_dealing(now):
    global dealing_lines_set, game_state, endgame_lines_set

    if not dealing_lines_set:
        textbox.set_lines(["..."],show_arrow=False)
        dealing_lines_set = True
    textbox.update(now)

''' if player.hand.calculate_total() == 21:
        if dealer.hand.cards[0].value in ['J', 'Q', 'K', 'A'] and not endgame_lines_set:
            print("Wow, a blackjack! Let's reveal the dealer's hidden card and see if I have one too....")
            endgame_lines_set = True
            if dealer.hand.calculate_total() == 21:
                endgame_lines_set = False
                game_state = GameState.RESOLUTION
        else:
            #perform_endgame(player.name, 'blackjack', dealer.name)
            print("Wow a blackjack!")
            player.games_won += 1
            game_state = GameState.RESOLUTION
'''
def update_player_turn(now):
    global player_turn_lines_set
    if not player_turn_lines_set:
        textbox.set_lines(HIT_OR_STAND_INPUT, show_arrow=False)
        player_turn_lines_set = True
    textbox.update(now)

def update_dealer_turn(now):
    pass

def update_resolution(now):
    global has_started_dealing, game_state, deck
    has_started_dealing = False
    player.reset_hand()
    dealer.reset_hand()
    deck = Deck()
    deck.shuffle()
    print(f'=====  GAME SCORE [ {player.name}: {player.games_won} | {dealer.name}: {dealer.games_won} ]  =====')
    game_state = GameState.DEALING




# -------------------------------------
# 3. Drawing on screen
# ---------------------------------------

def draw_playing():
    player_x, player_y = FIRST_PLAYER_CARD_X, FIRST_PLAYER_CARD_Y
    dealer_x, dealer_y = FIRST_DEALER_CARD_X, FIRST_DEALER_CARD_Y

    for i, card in enumerate(player.hand.cards):
        card.render(screen, player_x, player_y)
        player_x += PLAYER_CARD_DISPLACEMENT_X
        player_y -= PLAYER_CARD_DISPLACEMENT_Y

    for i, card in enumerate(dealer.hand.cards):
        if i == 1:
            screen.blit(CARD_BACK, (dealer_x, dealer_y))
        else:
            card.render(screen, dealer_x, dealer_y)
        dealer_x -= DEALER_CARD_DISPLACEMENT_X


def draw_screen():
    if game_state == GameState.INTRO and textbox.current_line_index < 11:
        screen.fill(BG_DARK_GREY)
    else:
        screen.fill(TABLE_GREEN)

    textbox.draw(screen)

    if game_state in [GameState.DEALING, GameState.PLAYER_TURN]:
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