import pygame

# Initialise pygame
pygame.init()

# Screen settings
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font(None, 50)

# Clock setup
clock = pygame.time.Clock()
dt = 0

# Game constants
INTRO = 'intro'
PLAYING = 'playing'

# Game state variables
line_fully_displayed = False
arrow_blink_speed_ms = 500
arrow_last_blink = 0
arrow_visible = True

# Game control variables
running = True
game_state = INTRO

# Dialogue content
dialogue_lines = [
    "Welcome to the blackjack table!",
    "My name is The Dealer.",
    "Today, we'll playing some rounds of blackjack.",
    "No gambling though. I'm here to showcase the beauty, the artistry of this fine game.",
    "Not here to partake in the devious act of gambling.",
    "Instead...",
    "Let's play first to win 10 games!"
]

# Dialogue state variables
current_line_index = 0
typed_text = ""
text_index = 0


# Letter timing setup
letter_delay = 20
last_update = pygame.time.get_ticks()


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


def handle_intro_input(event):
    global current_line_index, typed_text, text_index, last_update, line_fully_displayed, game_state

    if event.type == pygame.KEYDOWN:
        # If full line is displayed, go to next one when key is pressed
        if line_fully_displayed:
            current_line_index += 1
            if current_line_index >= len(dialogue_lines):
                game_state = PLAYING
            else:
                typed_text = ""
                text_index = 0
                last_update = pygame.time.get_ticks()
                line_fully_displayed = False
        else:
            # Skip animation and show full line
            typed_text = dialogue_lines[current_line_index]
            line_fully_displayed = True

def handle_playing_input(event):
    pass # to fill in later

def update_intro(now):
    global typed_text, text_index, last_update, line_fully_displayed, arrow_visible, arrow_last_blink

    # Typewriter logic
    current_full_text = dialogue_lines[current_line_index]
    current_full_text_word_count = len(current_full_text)
    if not line_fully_displayed and text_index < current_full_text_word_count:
        if now - last_update > letter_delay:
            typed_text += current_full_text[text_index]
            text_index += 1
            last_update = now
        if text_index == current_full_text_word_count:
            line_fully_displayed = True

    # Arrow blink state update
    if now - arrow_last_blink > arrow_blink_speed_ms:
        arrow_visible = not arrow_visible  # flip visibility
        arrow_last_blink = now

def update_playing(now):
    pass # to fill in later

def draw_screen():
    global arrow_last_blink, arrow_visible

    # Fill background
    screen.fill((35, 35, 35))

    if game_state == INTRO:
        draw_intro()

    pygame.display.flip()

def draw_intro():
    now = pygame.time.get_ticks()

    # Text box location
    text_box_width = screen_width * 0.9
    text_box_height = screen_height * 0.2
    text_box_x = (screen_width - text_box_width) // 2
    text_box_y = screen_height - text_box_height - (screen_height // 36)
    text_box_rect = pygame.Rect(text_box_x, text_box_y, text_box_width, text_box_height)

    # Wrap text
    line_height = 40
    padding = 15
    wrapped_lines = wrap_text(typed_text, font, text_box_width - line_height)

    # Draw text box
    pygame.draw.rect(screen, (10, 10, 10), text_box_rect, border_radius=10)
    pygame.draw.rect(screen, (235, 235, 235), text_box_rect, 3, border_radius=10)

    # Display dialogue
    for i, line in enumerate(wrapped_lines):
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (text_box_x + padding, text_box_y + padding + i * line_height))

    # Draw arrow in text box
    if line_fully_displayed and current_line_index < len(dialogue_lines) - 1 and arrow_visible:
        arrow_colour = (255, 255, 255)
        arrow_size = 10
        arrow_x = text_box_x + text_box_width - 30
        arrow_y = text_box_y + text_box_height - 25
        pygame.draw.polygon(screen, arrow_colour, [
            (arrow_x, arrow_y),
            (arrow_x + arrow_size, arrow_y),
            (arrow_x + arrow_size // 2, arrow_y + arrow_size)
        ])



while running:
    dt = clock.tick(60)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == INTRO:
            handle_intro_input(event)
        elif game_state == PLAYING:
            handle_playing_input(event)

    if game_state == INTRO:
        update_intro(now)
    elif game_state == PLAYING:
        update_playing(now)

    draw_screen()

pygame.quit()