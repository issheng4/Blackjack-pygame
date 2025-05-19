import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    INTRO, DEALING, PLAYER_TURN, DEALER_TURN, RESOLUTION,
    FONT_NAME, FONT_SIZE,
    WHITE, BLACK, TABLE_GREEN, BG_DARK_GREY, TEXTBOX_DARK_GREY, TEXTBOX_LIGHT_GREY,
    TEXTBOX_WIDTH, TEXTBOX_HEIGHT, TEXTBOX_X, TEXTBOX_Y, TEXTBOX_BORDER_RADIUS,
    LINE_HEIGHT, PADDING, LETTER_DELAY,
    ARROW_BLINK_SPEED_MS, ARROW_SIZE, ARROW_X, ARROW_Y,
    FIRST_PLAYER_CARD_X, FIRST_PLAYER_CARD_Y, PLAYER_CARD_DISPLACEMENT_X, PLAYER_CARD_DISPLACEMENT_Y, FIRST_DEALER_CARD_X, FIRST_DEALER_CARD_Y, DEALER_CARD_DISPLACEMENT_X,
    CARD_BACK,
)
from dialogue import INTRO_DIALOGUE_LINES
from game_objects import Card, Deck, Hand, Person


# Initialise pygame
pygame.init()

# Initialise persons and deck
player = Person('player', 'You')
dealer = Person('dealer', 'The Dealer')
deck = Deck()
deck.shuffle()

# Screen settings
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

# Clock setup
clock = pygame.time.Clock()
dt = 0

# Game state variables
line_fully_displayed = False
arrow_last_blink = 0
arrow_visible = True

# Game control variables
running = True
game_state = INTRO


# Dialogue state variables
current_line_index = 0
typed_text = ""
text_index = 0


# Letter timing setup
last_update = pygame.time.get_ticks()

# Dealing timing and event setup
DEAL_PLAYER_1 = pygame.USEREVENT + 1
DEAL_DEALER_1 = pygame.USEREVENT + 2
DEAL_PLAYER_2 = pygame.USEREVENT + 3
DEAL_DEALER_2 = pygame.USEREVENT + 4
has_started_dealing = False

# Initialise initial card positions
player_x, player_y = FIRST_PLAYER_CARD_X, FIRST_PLAYER_CARD_Y
dealer_x, dealer_y = FIRST_DEALER_CARD_X, FIRST_DEALER_CARD_Y




def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        test_line_width = font.size(test_line)[0]
        if test_line_width < max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return lines


# -------------------------------------
# 1. Handling inputs
# ---------------------------------------

def handle_intro_input(event):
    global current_line_index, typed_text, text_index, last_update, line_fully_displayed, game_state

    if event.type == pygame.KEYDOWN:
        # If full line is displayed, go to next one when key is pressed
        if line_fully_displayed:
            current_line_index += 1
            if current_line_index >= len(INTRO_DIALOGUE_LINES):
                game_state = DEALING

            else:
                typed_text = ""
                text_index = 0
                last_update = pygame.time.get_ticks()
                line_fully_displayed = False
        else:
            # Skip animation and show full line
            typed_text = INTRO_DIALOGUE_LINES[current_line_index]
            line_fully_displayed = True
        
        # Skip intro with esc key
        if event.key == pygame.K_ESCAPE and game_state == INTRO:
            game_state = DEALING



def handle_playing_input(event):
    global has_started_dealing
    if game_state == DEALING and has_started_dealing == False:
        pygame.time.set_timer(DEAL_PLAYER_1, 10, loops=1)
        pygame.time.set_timer(DEAL_DEALER_1, 410, loops=1)
        pygame.time.set_timer(DEAL_PLAYER_2, 810, loops=1)
        pygame.time.set_timer(DEAL_DEALER_2, 1210, loops=1)
        has_started_dealing = True



# -------------------------------------
# 2. Updating logic
# ---------------------------------------

def update_intro(now):
    global typed_text, text_index, last_update, line_fully_displayed, arrow_visible, arrow_last_blink

    # Typewriter logic
    current_full_text = INTRO_DIALOGUE_LINES[current_line_index]
    current_full_text_word_count = len(current_full_text)
    if not line_fully_displayed and text_index < current_full_text_word_count:
        if now - last_update > LETTER_DELAY:
            typed_text += current_full_text[text_index]
            text_index += 1
            last_update = now
        if text_index == current_full_text_word_count:
            line_fully_displayed = True

    # Arrow blink state update
    if now - arrow_last_blink > ARROW_BLINK_SPEED_MS:
        arrow_visible = not arrow_visible  # flip visibility
        arrow_last_blink = now

initial_deal_done = False
def update_dealing(now):
    pass





# -------------------------------------
# 3. Drawing on screen
# ---------------------------------------


def draw_screen():
    global arrow_last_blink, arrow_visible

    # Fill background
    if current_line_index < 11:
        screen.fill(BG_DARK_GREY)
    # Change screen to table view once dealer says the line "Let's bring the table in"
    else:
        screen.fill(TABLE_GREEN)

    if game_state == DEALING:
        screen.fill(TABLE_GREEN)

    # Text box location
    text_box_rect = pygame.Rect(TEXTBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)

    # Wrap text
    wrapped_lines = wrap_text(typed_text, font, TEXTBOX_WIDTH - LINE_HEIGHT)

    # Draw text box
    pygame.draw.rect(screen, TEXTBOX_DARK_GREY, text_box_rect, border_radius=TEXTBOX_BORDER_RADIUS)
    pygame.draw.rect(screen, TEXTBOX_LIGHT_GREY, text_box_rect, 3, border_radius=TEXTBOX_BORDER_RADIUS)

    # Display dialogue
    x_offset = TEXTBOX_X + PADDING
    y_offset = TEXTBOX_Y + PADDING
    for i, line in enumerate(wrapped_lines):
        text_surface = font.render(line, True, WHITE)
        screen.blit(text_surface, (x_offset, y_offset + i * LINE_HEIGHT))

    # Draw arrow in text box
    if line_fully_displayed and arrow_visible: # and maybe tbd current_line_index < len(INTRO_DIALOGUE_LINES) - 1
        pygame.draw.polygon(screen, WHITE, [
            (ARROW_X, ARROW_Y),
            (ARROW_X + ARROW_SIZE, ARROW_Y),
            (ARROW_X + ARROW_SIZE // 2, ARROW_Y + ARROW_SIZE)
        ])

    if game_state == INTRO:
        draw_intro()
    elif game_state == DEALING:
        draw_playing()

    pygame.display.flip()

def draw_intro():
    pass


def draw_playing():
    player_x, player_y = FIRST_PLAYER_CARD_X, FIRST_PLAYER_CARD_Y
    dealer_x, dealer_y = FIRST_DEALER_CARD_X, FIRST_DEALER_CARD_Y

    for i, card in enumerate(player.hand.cards):
        card.draw(screen, player_x, player_y)
        player_x += PLAYER_CARD_DISPLACEMENT_X
        player_y -= PLAYER_CARD_DISPLACEMENT_Y

    for i, card in enumerate(dealer.hand.cards):
        if i == 1:
            screen.blit(CARD_BACK, (dealer_x, dealer_y))
        else:
            card.draw(screen, dealer_x, dealer_y)
        dealer_x -= DEALER_CARD_DISPLACEMENT_X




    





while running:
    dt = clock.tick(60)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == INTRO:
            handle_intro_input(event)
        elif game_state == DEALING:
            handle_playing_input(event)
            if event.type == DEAL_PLAYER_1:
                player.draw_card(deck)

            elif event.type == DEAL_DEALER_1:
                dealer.draw_card(deck)

            elif event.type == DEAL_PLAYER_2:

                player.draw_card(deck)

            elif event.type == DEAL_DEALER_2:
                dealer.draw_card(deck)

    if game_state == INTRO:
        update_intro(now)
    elif game_state == DEALING:
        update_dealing(now)
        

    draw_screen()

pygame.quit()