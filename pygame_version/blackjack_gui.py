import pygame

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


pygame.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font(None, 50)
clock = pygame.time.Clock()
running = True
line_fully_displayed = False
dt = 0

# Dialogue content
dialogue_lines = [
    "Welcome to the blackjack table!",
    "My name is The Dealer. What's yours?",
    "...",
    "Oh, that's a lovely name.",
    "So, you, we'll playing some rounds of blackjack here today.",
    "No gambling though. I'm here to showcase the beauty, the artistry of this fine game.",
    "Not here to partake in the devious act of gambling.",
    "Instead...",
    "Let's play first to win 10 games!"
]

current_line_index = 0
typed_text = ""
text_index = 0


# Letter timing setup
letter_delay = 20
last_update = pygame.time.get_ticks()


while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # If full line is displayed, go to next one when key is pressed
            if line_fully_displayed:
                current_line_index += 1
                """if current_line_index >= len(dialogue_lines):
                    run the main game
                    else:"""
                typed_text = ""
                text_index = 0
                last_update = pygame.time.get_ticks()
                line_fully_displayed = False
            else:
                # Skip animation and show full line
                typed_text = dialogue_lines[current_line_index]
                line_fully_displayed = True

    # Typewriter logic
    now = pygame.time.get_ticks()
    current_full_text = dialogue_lines[current_line_index]
    current_full_text_word_count = len(current_full_text)
    if not line_fully_displayed and text_index < current_full_text_word_count:
        if now - last_update > letter_delay:
            typed_text += current_full_text[text_index]
            text_index += 1
            last_update = now
        if text_index == current_full_text_word_count:
            line_fully_displayed = True


    # Fill background
    screen.fill((35, 35, 35))

    # Draw text box
    text_box_width = screen_width * 0.9
    text_box_height = screen_height * 0.2
    text_box_x = (screen_width - text_box_width) // 2
    text_box_y = screen_height - text_box_height - (screen_height // 36)

    text_box_rect = pygame.Rect(text_box_x, text_box_y, text_box_width, text_box_height)

    pygame.draw.rect(screen, (10, 10, 10), text_box_rect, border_radius=10)
    pygame.draw.rect(screen, (235, 235, 235), text_box_rect, 3, border_radius=10)


    # Wrap the typed text
    line_height = 40
    padding = 15
    wrapped_lines = wrap_text(typed_text, font, text_box_width - line_height)
    for i, line in enumerate(wrapped_lines):
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (text_box_x + padding, text_box_y + padding + i * line_height))



    pygame.display.flip()


pygame.quit()