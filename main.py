import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    FONT_NAME, FONT_SIZE,
    WHITE, BLACK, TABLE_GREEN, BG_DARK_GREY, TEXTBOX_DARK_GREY, TEXTBOX_LIGHT_GREY, SHADOW,
    TEXTBOX_WIDTH, TEXTBOX_HEIGHT, TEXTBOX_X, TEXTBOX_Y, TEXTBOX_BORDER_RADIUS,
    LINE_HEIGHT, PADDING, LETTER_DELAY, MAX_TEXT_WIDTH,
    ARROW_BLINK_SPEED_MS, ARROW_SIZE, ARROW_X, ARROW_Y,
    CARD_WIDTH, CARD_HEIGHT,
    FIRST_PLAYER_CARD_X, FIRST_PLAYER_CARD_Y, PLAYER_CARD_DISPLACEMENT_X, PLAYER_CARD_DISPLACEMENT_Y, FIRST_DEALER_CARD_X, FIRST_DEALER_CARD_Y, DEALER_CARD_DISPLACEMENT_X,
    SCOREBOARD_TEXT_X, SCOREBOARD_TITLE_Y, SCOREBOARD_PLAYER_Y, SCOREBOARD_DEALER_Y,
    CARD_BACK,
    MUSIC_VOLUME, INTRO_MUSIC, MAIN_MUSIC
)
from dialogue import INTRO_DIALOGUE_LINES, HIT_OR_STAND_INPUT
from game_objects import Card, Deck, Hand, Person, TextBoxController, GameFlags, GameState, GameManager

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")
font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
clock = pygame.time.Clock()
pygame.mixer.init()

# Game data
game = GameManager()
player = Person('player')
dealer = Person('dealer')
flags = game.flags
running = True
dt = 0
now = 0

# Text box
text_rect = pygame.Rect(TEXTBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
textbox = TextBoxController(font, text_rect)

# Deal timing events
DEAL_PLAYER_CARD_1 = pygame.USEREVENT + 1
DEAL_DEALER_CARD_1 = pygame.USEREVENT + 2
DEAL_PLAYER_CARD_2 = pygame.USEREVENT + 3
DEAL_DEALER_CARD_2 = pygame.USEREVENT + 4
DEAL_DONE = pygame.USEREVENT + 5
DEALER_TURN_CARD_REVEAL = pygame.USEREVENT + 6
DEALER_HIT = pygame.USEREVENT + 7
DEALER_TURN_OVER = pygame.USEREVENT + 8

# Hand for testing
MANUAL_HAND_FOR_TESTING = False
TEST_PLAYER_CARD_1 = Card('4', 'spades')
TEST_PLAYER_CARD_2 = Card('K', 'spades')
TEST_DEALER_CARD_1 = Card('Q', 'spades')
TEST_DEALER_CARD_2 = Card('A', 'spades')



# -------------------------------------
# 1. Handling inputs
# ---------------------------------------

def handle_intro_input(event):
    result = textbox.handle_dialogue_input(event)
    if result == 'done' or result == 'skip':
        game.state = GameState.RESET

def handle_reset_input(event):
    pass


def handle_dealing_input(event):
    if not flags.has_started_dealing:
        pygame.time.set_timer(DEAL_PLAYER_CARD_1, 600, loops=1)
        pygame.time.set_timer(DEAL_DEALER_CARD_1, 900, loops=1)
        pygame.time.set_timer(DEAL_PLAYER_CARD_2, 1200, loops=1)
        pygame.time.set_timer(DEAL_DEALER_CARD_2, 1500, loops=1)
        flags.has_started_dealing = True

    if MANUAL_HAND_FOR_TESTING:
        if event.type == DEAL_PLAYER_CARD_1:
            player.hand.add_card(TEST_PLAYER_CARD_1)
        elif event.type == DEAL_DEALER_CARD_1:
            dealer.hand.add_card(TEST_DEALER_CARD_1)
        elif event.type == DEAL_PLAYER_CARD_2:
            player.hand.add_card(TEST_PLAYER_CARD_2)
        elif event.type == DEAL_DEALER_CARD_2:
            dealer.hand.add_card(TEST_DEALER_CARD_2)
            pygame.time.set_timer(DEAL_DONE, 20, loops=1)

    else:
        if event.type == DEAL_PLAYER_CARD_1:
            player.receive_card(game.deck)
        elif event.type == DEAL_DEALER_CARD_1:
            dealer.receive_card(game.deck)
        elif event.type == DEAL_PLAYER_CARD_2:
            player.receive_card(game.deck)
        elif event.type == DEAL_DEALER_CARD_2:
            dealer.receive_card(game.deck)
            pygame.time.set_timer(DEAL_DONE, 20, loops=1)

    if event.type == DEAL_DONE:
        print(f"//// Player's hand: {player.hand}  TOTAL: {player.calculate_hand_total()}  ////")
        print(f"//// Dealer's hand: {dealer.hand}  TOTAL: {dealer.calculate_hand_total()}  ////")
        game.state = GameState.PLAYER_TURN



def handle_player_turn_input(event):
    if event.type != pygame.KEYDOWN:
        return

    # If bust text is active
    if flags.player_bust_lines_set:
        result = textbox.handle_dialogue_input(event)
        if result == 'done':
            game.state = GameState.RESET
        return

    # Blackjack flow
    if flags.player_blackjack_stage:
        result = textbox.handle_dialogue_input(event)
        if result == 'done':
            if flags.player_blackjack_stage == 'reveal':
                flags.player_blackjack_stage = 'resolve'
            elif flags.player_blackjack_stage == 'done':
                game.state = GameState.RESET
        return

    # If stand dialogue is active
    if flags.player_stands_lines_set:
        result = textbox.handle_dialogue_input(event)
        if result == 'done':
            game.state = GameState.DEALER_TURN
        return

    # Hit or Stand phase
    if not flags.player_stands_lines_ready:
        # Only allow progressing if the textbox is not in the hit/stand prompt
        if event.key == pygame.K_h and textbox.line_fully_displayed:
            player.receive_card(game.deck)
            print(f"//// Player's hand: {player.hand}  TOTAL: {player.hand.total}  ////")
            textbox.handle_dialogue_input(event)

        elif event.key == pygame.K_s:
            flags.player_stands_lines_ready = True

        # Restart for testing
        elif event.key == pygame.K_r:
            game.state = GameState.RESET





def handle_dealer_turn_input(event):
    if not flags.dealer_turn_status:
        flags.dealer_turn_status = 'reveal'
        pygame.time.set_timer(DEALER_TURN_CARD_REVEAL, 300, loops=1)

    elif event.type == DEALER_TURN_CARD_REVEAL:
            flags.dealer_second_card_visible = True
            dealer.hand.make_hidden_card_reveal_sound()
            print('Second card revealed')
            flags.dealer_turn_status = 'dealing_wait'
            pygame.time.set_timer(DEALER_HIT, 800, loops=1)
    
    elif event.type == DEALER_HIT and flags.dealer_turn_status in ('dealing', 'dealing_wait'):
        if dealer.hand.total < 17:
            dealer.receive_card(game.deck)
            print('Card dealt, total:', dealer.hand.total)
            flags.dealer_turn_status = 'dealing'
            pygame.time.set_timer(DEALER_HIT, 800, loops=1)
        else:
            pygame.time.set_timer(DEALER_HIT, 0)
            print('Dealer finished hitting')
            flags.dealer_turn_status = 'done'
            pygame.time.set_timer(DEALER_TURN_OVER, 20, loops=1)
    
    elif event.type == DEALER_TURN_OVER:
        game.state = GameState.RESOLUTION



def handle_resolution_input(event):    
    result = textbox.handle_dialogue_input(event)
    if result == 'done':
        if not flags.review_hands_lines_ready:
            game.state = GameState.RESET
        elif not flags.endgame_lines_ready:
            flags.endgame_lines_ready = True
        else:
            game.state = GameState.RESET








# -------------------------------------
# 2. Updating logic
# ---------------------------------------

def update_intro(now):
    if not flags.intro_lines_set:
        textbox.set_lines(INTRO_DIALOGUE_LINES)
        flags.intro_lines_set = True
    textbox.animate(now)

def update_reset(now):
    flags.reset()
    player.reset_hand()
    dealer.reset_hand()
    game.deck = Deck()
    game.deck.shuffle()
    print(f'=====  GAME SCORE [ Player: {player.games_won} | Dealer: {dealer.games_won} ]  =====')
    game.state = GameState.DEALING


def update_dealing(now):
    if not flags.dealing_lines_set:
        textbox.set_lines(["And I deal..."],show_arrow=False)
        flags.dealing_lines_set = True
    textbox.animate(now)

    
def update_player_turn(now):
    if len(player.hand.cards) == 2 and player.hand.total == 21:

        if not flags.player_blackjack_stage:
            flags.player_blackjack_stage = 'start'

        if flags.player_blackjack_stage == 'start':
            # Dealer cannot have blackjack
            if dealer.hand.cards[0].value not in ('10', 'J', 'Q', 'K', 'A'):
                textbox.set_lines(["Wow, you got a blackjack!", "Let's go again."])
                flags.player_blackjack_stage = 'done'
                player.win_game()

            else:
                # Dealer might have blackjack — wait before revealing
                textbox.set_lines(["Wow, you got a blackjack!", "But wait a moment.", "Let's see if I've got one too...", " "])
                flags.player_blackjack_stage = 'reveal'

        elif flags.player_blackjack_stage == 'reveal':
            # Wait for user to finish reading line 1
            if textbox.line_fully_displayed and textbox.current_line_index == 3:
                flags.dealer_second_card_visible = True
                if len(dealer.hand.cards) == 2 and dealer.hand.total == 21:
                    textbox.set_lines(["I have a blackjack too!", "Looks like it's a draw.", "Let's go again."])
                else:
                    textbox.set_lines(["Ah, I don't have a blackjack.", "You've won this time!", "Let's go again."])
                    player.win_game()
                flags.player_blackjack_stage = 'done'

        textbox.animate(now)
        return

    
    if player.hand.total > 21:
        # Player has bust
        if not flags.player_bust_lines_set:
            textbox.set_lines(["Ah! Looks like you've bust.", "Let's go again."])
            flags.player_bust_lines_set = True
            dealer.win_game()

    elif not flags.player_turn_lines_set:
        # Standard player turn
        textbox.set_lines(HIT_OR_STAND_INPUT, show_arrow=False)
        flags.player_turn_lines_set = True

    elif flags.player_stands_lines_ready and not flags.player_stands_lines_set:
        # Stand dialogue
        textbox.set_lines(["You stand, alright.", "Now it's my turn."])
        flags.player_stands_lines_set = True

    textbox.animate(now)





def update_dealer_turn(now):
    if not flags.dealer_turn_lines_set:
        textbox.set_lines(["I hit until I reach 17..."],show_arrow=False)
        flags.dealer_turn_lines_set = True
    textbox.animate(now)


def update_resolution(now):
    if len(dealer.hand.cards) == 2 and dealer.hand.total == 21:
        if not flags.dealer_blackjack_lines_set:
            textbox.set_lines(["Oh, I've got a blackjack!", "That's a game won for The Dealer.", "Let's go again!"])
            flags.dealer_blackjack_lines_set = True
            dealer.win_game()
         
    elif dealer.hand.total > 21:
        if not flags.dealer_bust_lines_set:
            textbox.set_lines(["Ah! Looks like I have bust.", "So you win this time.", "Another game!"])
            flags.dealer_bust_lines_set = True
            player.win_game()

    else:
        flags.review_hands_lines_ready = True

    if flags.review_hands_lines_ready and not flags.review_hands_lines_set:
        textbox.set_lines(["And now we review our hands to see who has won this time.", f"You have {player.hand.total} and I have {dealer.hand.total}."])
        flags.review_hands_lines_set = True

    elif flags.endgame_lines_ready:
        if player.hand.total > dealer.hand.total:
            if not flags.player_wins_lines_set:
                textbox.set_lines(["You win this time!", "Let's go again."])
                flags.player_wins_lines_set = True
                player.win_game()

        elif player.hand.total < dealer.hand.total:
            if not flags.dealer_wins_lines_set:
                textbox.set_lines(["I win this time!", "Let's go again."])
                flags.dealer_wins_lines_set = True
                dealer.win_game()
        
        else:
            if not flags.game_draw_lines_set:
                textbox.set_lines(["So it's a draw this time round.", "Let's go again!"])
                flags.game_draw_lines_set = True
    
    textbox.animate(now)


    




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
    player_x, player_y = FIRST_PLAYER_CARD_X, FIRST_PLAYER_CARD_Y
    dealer_x, dealer_y = FIRST_DEALER_CARD_X, FIRST_DEALER_CARD_Y

    for i, card in enumerate(player.hand.cards):
        card.render(screen, player_x, player_y)
        player_x += PLAYER_CARD_DISPLACEMENT_X
        player_y -= PLAYER_CARD_DISPLACEMENT_Y

    for i, card in enumerate(dealer.hand.cards):
        if i == 1 and not flags.dealer_second_card_visible:
            screen.blit(CARD_BACK, (dealer_x, dealer_y))
        else:
            card.render(screen, dealer_x, dealer_y)
        dealer_x -= DEALER_CARD_DISPLACEMENT_X

    draw_scoreboard()


def draw_screen():
    if game.state == GameState.INTRO and textbox.current_line_index < 11:
        screen.fill(BG_DARK_GREY)
    else:
        screen.fill(TABLE_GREEN)

    textbox.draw(screen)

    if game.state is not GameState.INTRO:
        draw_playing()

    pygame.display.flip()


def play_music():
    if game.state == GameState.INTRO:
        desired_music = INTRO_MUSIC
    else:
        desired_music = MAIN_MUSIC
    
    if game.current_music != desired_music:
        pygame.mixer.music.load(desired_music)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)
        game.current_music = desired_music




# -------------------------------------
# MAIN LOOP
# ---------------------------------------

while running:
    dt = clock.tick(60)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game.state == GameState.INTRO:
            handle_intro_input(event)
        elif game.state == GameState.RESET:
            handle_reset_input(event)
        elif game.state == GameState.DEALING:
            handle_dealing_input(event)
        elif game.state == GameState.PLAYER_TURN:
            handle_player_turn_input(event)
        elif game.state == GameState.DEALER_TURN:
            handle_dealer_turn_input(event)
        elif game.state == GameState.RESOLUTION:
            handle_resolution_input(event)


    # Update state
    if game.state == GameState.INTRO:
        update_intro(now)
    elif game.state == GameState.RESET:
        update_reset(now)
    elif game.state == GameState.DEALING:
        update_dealing(now)
    elif game.state == GameState.PLAYER_TURN:
        update_player_turn(now)
    elif game.state == GameState.DEALER_TURN:
        update_dealer_turn(now)
    elif game.state == GameState.RESOLUTION:
        update_resolution(now)

    # Music control
    play_music()


    # Render frame
    draw_screen()

pygame.quit()