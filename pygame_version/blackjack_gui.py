import pygame

pygame.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font(None, 50)
clock = pygame.time.Clock()
running = True
dt = 0

# Dialogue text setup
full_text = "Welcome to the blackjack table!"
typed_text = ""
text_index = 0

# Letter timing setup
letter_delay = 30
last_update = pygame.time.get_ticks()


while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Typewriter effect
    now = pygame.time.get_ticks()
    if text_index < len(full_text) and now - last_update > letter_delay:
        typed_text += full_text[text_index]
        text_index += 1
        last_update = now

    # Fill background
    screen.fill((35, 35, 35))

    # Drawing the text box
    text_box_width = screen_width * 0.9
    text_box_height = screen_height * 0.2
    text_box_x = (screen_width - text_box_width) // 2
    text_box_y = screen_height - text_box_height - 20

    text_box_rect = pygame.Rect(text_box_x, text_box_y, text_box_width, text_box_height)

    pygame.draw.rect(screen, (10, 10, 10), text_box_rect, border_radius=10)
    pygame.draw.rect(screen, (235, 235, 235), text_box_rect, 3, border_radius=10)


    # Text positions
    text_margin = 15  # margin inside the box
    text_x = text_box_x + text_margin
    text_y = text_box_y + text_margin

    rendered_text = font.render(typed_text, True, (245, 245, 245))
    screen.blit(rendered_text, (text_x,text_y))
    pygame.display.flip()


pygame.quit()