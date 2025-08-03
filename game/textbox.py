import pygame
from typing import List
from .constants import Display, Colours

class TextBox:
    """Handles the display and animation of dialogue text."""
    
    # Text box dimensions (calculated from display size)
    WIDTH: int = int(Display.WIDTH * 0.9)  # 1152
    HEIGHT: int = int(Display.HEIGHT * 0.2)  # 144
    X: int = (Display.WIDTH - WIDTH) // 2  # 64
    Y: int = Display.HEIGHT - HEIGHT - (Display.HEIGHT // 36)  # 556
    
    # Text box styling
    BORDER_RADIUS: int = 10
    LINE_HEIGHT: int = 38
    PADDING: int = 18
    MAX_WIDTH: int = WIDTH - LINE_HEIGHT
    
    # Animation settings
    LETTER_DELAY: int = 10
    ARROW_BLINK_MS: int = 500
    ARROW_SIZE: int = 10
    ARROW_X: int = X + WIDTH - 30
    ARROW_Y: int = Y + HEIGHT - 25

    def __init__(self, font: pygame.font.Font, rect: pygame.Rect = None):
        """Initialize text box with optional custom rectangle."""
        self.font = font
        self.rect = rect or pygame.Rect(self.X, self.Y, self.WIDTH, self.HEIGHT)

        # Display state
        self.lines = []
        self.current_line_index = 0
        self.typed_text = ""
        self.char_index = 0
        self.last_update = 0
        self.line_fully_displayed = False
    
        # Arrow state
        self.arrow_visible = True
        self.arrow_last_blink = 0

    def set_lines(self, lines: List[str], show_arrow: bool = True):
        """Set the lines of text to display in the text box."""
        self.lines = lines
        self.current_line_index = 0
        self.typed_text = ""
        self.char_index = 0
        self.line_fully_displayed = False
        self.last_update = pygame.time.get_ticks()
        self.show_arrow = show_arrow
        

    def wrap_text(self, text: str) -> List[str]:
        """Wrap the text to fit within the text box width."""
        max_width = self.rect.width - 2 * self.PADDING
        words = text.split(" ")
        wrapped_lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                wrapped_lines.append(current_line.strip())
                current_line = word + " "
        wrapped_lines.append(current_line.strip())
        return wrapped_lines
    
    def animate(self, now: int):
        """Animate the text typing and arrow blinking."""
        full_text = self.lines[self.current_line_index]
        if self.current_line_index < len(self.lines):
            if not self.line_fully_displayed and self.char_index < len(full_text):
                if now - self.last_update > self.LETTER_DELAY:
                    self.typed_text += full_text[self.char_index]
                    self.char_index += 1
                    self.last_update = now
                if self.char_index == len(full_text):
                    self.line_fully_displayed = True

        # Blink arrow
        if now - self.arrow_last_blink > self.ARROW_BLINK_MS:
            self.arrow_visible = not self.arrow_visible
            self.arrow_last_blink = now

    def handle_dialogue_input(self, event: pygame.event.Event):
        """Handle user input for advancing dialogue."""
        if event.type == pygame.KEYDOWN:
            # Handle ESC key to skip dialogue
            if event.key == pygame.K_ESCAPE:
                return 'skip'
            
            if self.line_fully_displayed:
                self.current_line_index += 1
                if self.current_line_index >= len(self.lines):
                    return 'done'
                else:
                    self.typed_text = ""
                    self.char_index = 0
                    self.line_fully_displayed = False
                    self.last_update = pygame.time.get_ticks()
            else:
                self.typed_text = self.lines[self.current_line_index]
                self.char_index = len(self.typed_text)
                self.line_fully_displayed = True
        return 'continue'
    
    def draw(self, surface: pygame.Surface):
        """Draw the text box and its contents on the given surface."""
        pygame.draw.rect(surface, Colours.TEXTBOX_DARK, self.rect, border_radius=self.BORDER_RADIUS)
        pygame.draw.rect(surface, Colours.TEXTBOX_LIGHT, self.rect, 3, border_radius=self.BORDER_RADIUS)

        wrapped_lines = self.wrap_text(self.typed_text)
        x_offset = self.rect.x + self.PADDING
        y_offset = self.rect.y + self.PADDING

        for i, line in enumerate(wrapped_lines):
            surface.blit(self.font.render(line, True, Colours.WHITE), (x_offset, y_offset + i * self.LINE_HEIGHT))

        if self.line_fully_displayed and self.arrow_visible and self.show_arrow:
            pygame.draw.polygon(surface, Colours.WHITE, [
                (self.ARROW_X, self.ARROW_Y),
                (self.ARROW_X + self.ARROW_SIZE, self.ARROW_Y),
                (self.ARROW_X + self.ARROW_SIZE // 2, self.ARROW_Y + self.ARROW_SIZE)
            ])