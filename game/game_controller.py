import logging
import pygame
from .constants import Display, Colours, CardLayout, Audio, Scoreboard
from .dialogue import *
from .game_manager import GameManager
from .game_state import GameState
from .person import Person
from .deck import Deck
from .textbox import TextBox
from .card import Card

class GameController:
    """Controls the game loop and coordinates game components."""
    def __init__(self):
        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((Display.WIDTH, Display.HEIGHT))
        pygame.display.set_caption("Blackjack")
        self.font = pygame.font.SysFont(Display.FONT_NAME, Display.FONT_SIZE)
        self.font_small = pygame.font.SysFont(Display.FONT_NAME, Display.FONT_SIZE_SMALL)
        self.clock = pygame.time.Clock()
        pygame.mixer.init()

        # Game components
        self.game_manager = GameManager()
        self.game_state = GameState.INTRO
        self.player = Person('player')
        self.dealer = Person('dealer')
        self.flags = self.game_manager.flags
        self.textbox = TextBox(
            self.font,
            pygame.Rect(
                TextBox.X,
                TextBox.Y,
                TextBox.WIDTH,
                TextBox.HEIGHT
            )
        )

        # Game timing events
        self.DEAL_PLAYER_CARD_1 = pygame.USEREVENT + 1
        self.DEAL_DEALER_CARD_1 = pygame.USEREVENT + 2
        self.DEAL_PLAYER_CARD_2 = pygame.USEREVENT + 3
        self.DEAL_DEALER_CARD_2 = pygame.USEREVENT + 4
        self.DEAL_DONE = pygame.USEREVENT + 5
        self.DEALER_TURN_CARD_REVEAL = pygame.USEREVENT + 6
        self.DEALER_HIT = pygame.USEREVENT + 7
        self.DEALER_TURN_OVER = pygame.USEREVENT + 8

        # Hand for testing
        self.MANUAL_HAND_FOR_TESTING: bool = False
        self.TEST_PLAYER_CARD_1: Card = Card('A', 'spades')
        self.TEST_PLAYER_CARD_2: Card = Card('9', 'spades')
        self.TEST_DEALER_CARD_1: Card = Card('A', 'spades')
        self.TEST_DEALER_CARD_2: Card = Card('A', 'spades')

    def handle_events(self) -> bool:
        """Handles all pygame events. Returns False if game should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Quit event received. Exiting game.")
                return False
            
            state_handlers = {
                GameState.INTRO: self.handle_intro_input,
                GameState.RESET: self.handle_reset_input,
                GameState.DEALING: self.handle_dealing_input,
                GameState.PLAYER_TURN: self.handle_player_turn_input,
                GameState.DEALER_TURN: self.handle_dealer_turn_input,
                GameState.RESOLUTION: self.handle_resolution_input
            }
            handler = state_handlers.get(self.game_manager.state)
            if handler:
                handler(event)
        return True

    def update(self, now: int) -> None:
        """Update game state."""
        state_updaters = {
            GameState.INTRO: self.update_intro,
            GameState.RESET: self.update_reset,
            GameState.DEALING: self.update_dealing,
            GameState.PLAYER_TURN: self.update_player_turn,
            GameState.DEALER_TURN: self.update_dealer_turn,
            GameState.RESOLUTION: self.update_resolution
        }
        updater = state_updaters.get(self.game_manager.state)
        if updater:
            updater(now)
        self.update_music()

    def run(self) -> None:
        """Main game loop."""
        running = True
        while running:
            dt = self.clock.tick(60)
            now = pygame.time.get_ticks()
            
            running = self.handle_events()
            self.update(now)
            self.draw_screen()

        pygame.quit()

    def handle_intro_input(self, event: pygame.event.Event) -> None:
        """Handles input during the intro dialogue."""
        result: str = self.textbox.handle_dialogue_input(event)
        if result in ('done', 'skip'):
            self.game_manager.state = GameState.RESET

    def handle_reset_input(self, event: pygame.event.Event) -> None:
        """Handles input during the reset phase."""
        pass

    def handle_dealing_input(self, event: pygame.event.Event) -> None:
        """Handles input during the dealing phase."""
        if not self.flags.has_started_dealing:
            pygame.time.set_timer(self.DEAL_PLAYER_CARD_1, 600, loops=1)
            pygame.time.set_timer(self.DEAL_DEALER_CARD_1, 900, loops=1)
            pygame.time.set_timer(self.DEAL_PLAYER_CARD_2, 1200, loops=1)
            pygame.time.set_timer(self.DEAL_DEALER_CARD_2, 1500, loops=1)
            self.flags.has_started_dealing = True
            logging.info("Starting initial deal")

        if self.MANUAL_HAND_FOR_TESTING:
            if event.type == self.DEAL_PLAYER_CARD_1:
                self.player.hand.add_card(self.TEST_PLAYER_CARD_1)
            elif event.type == self.DEAL_DEALER_CARD_1:
                self.dealer.hand.add_card(self.TEST_DEALER_CARD_1)
            elif event.type == self.DEAL_PLAYER_CARD_2:
                self.player.hand.add_card(self.TEST_PLAYER_CARD_2)
            elif event.type == self.DEAL_DEALER_CARD_2:
                self.dealer.hand.add_card(self.TEST_DEALER_CARD_2)
                pygame.time.set_timer(self.DEAL_DONE, 20, loops=1)
        else:
            try:
                if event.type == self.DEAL_PLAYER_CARD_1:
                    self.player.receive_card(self.game_manager.deck)
                    logging.debug(f"Player card 1: {self.player.hand.cards[-1]}")  # Debug level for individual cards
                elif event.type == self.DEAL_DEALER_CARD_1:
                    self.dealer.receive_card(self.game_manager.deck)
                    logging.debug(f"Dealer card 1: {self.dealer.hand.cards[-1]}")
                elif event.type == self.DEAL_PLAYER_CARD_2:
                    self.player.receive_card(self.game_manager.deck)
                    logging.debug(f"Player card 2: {self.player.hand.cards[-1]}")
                elif event.type == self.DEAL_DEALER_CARD_2:
                    self.dealer.receive_card(self.game_manager.deck)
                    logging.debug(f"Dealer card 2: {self.dealer.hand.cards[-1]}")
                    pygame.time.set_timer(self.DEAL_DONE, 20, loops=1)
            except Exception as e:
                logging.error(f"Error during dealing phase: {e}")
                self.game_manager.state = GameState.RESET
                return

        if event.type == self.DEAL_DONE:
            logging.info(f"Initial deal complete - Player: {self.player.hand} ({self.player.hand.total}) | Dealer: [{self.dealer.hand.cards[0]}, ?]")
            self.game_manager.state = GameState.PLAYER_TURN

    def handle_player_turn_input(self, event: pygame.event.Event) -> None:
        """Handles input during the player's turn."""
        if event.type != pygame.KEYDOWN:
            return

        # Handle bust, blackjack, and stand cases with minimal logging
        if self.flags.player_bust_lines_set or self.flags.player_blackjack_stage or self.flags.player_stands_lines_set:
            result: str = self.textbox.handle_dialogue_input(event)
            if result == 'done':
                if self.flags.player_bust_lines_set:
                    logging.info("Player bust - Dealer wins")
                self.game_manager.state = GameState.RESET if not self.flags.player_stands_lines_set else GameState.DEALER_TURN
            return

        # Hit or Stand phase
        if not self.flags.player_stands_lines_ready and self.textbox.line_fully_displayed:
            if event.key == pygame.K_h:
                try:
                    self.player.receive_card(self.game_manager.deck)
                    self.textbox.handle_dialogue_input(event)
                    logging.info(f"Player hits - Hand: {self.player.hand} ({self.player.hand.total})")
                except Exception as e:
                    logging.error(f"Error hitting: {e}")
            elif event.key == pygame.K_s:
                self.flags.player_stands_lines_ready = True
                logging.info(f"Player stands - Final hand: {self.player.hand} ({self.player.hand.total})")

    def handle_dealer_turn_input(self, event: pygame.event.Event) -> None:
        """Handles input during the dealer's turn."""
        if not self.flags.dealer_turn_status:
            self.flags.dealer_turn_status = 'reveal'
            pygame.time.set_timer(self.DEALER_TURN_CARD_REVEAL, 300, loops=1)
        elif event.type == self.DEALER_TURN_CARD_REVEAL:
            self.flags.dealer_second_card_visible = True
            self.dealer.hand.make_hidden_card_reveal_sound()
            logging.info(f"Dealer's full hand revealed: {self.dealer.hand} ({self.dealer.hand.total})")
            self.flags.dealer_turn_status = 'dealing_wait'
            pygame.time.set_timer(self.DEALER_HIT, 800, loops=1)
        elif event.type == self.DEALER_HIT and self.flags.dealer_turn_status in ('dealing', 'dealing_wait'):
            if self.dealer.hand.total < 17:
                try:
                    self.dealer.receive_card(self.game_manager.deck)
                    logging.info(f"Dealer hits - Hand: {self.dealer.hand} ({self.dealer.hand.total})")
                except Exception as e:
                    logging.error(f"Error: {e}")
                self.flags.dealer_turn_status = 'dealing'
                pygame.time.set_timer(self.DEALER_HIT, 800, loops=1)
            else:
                pygame.time.set_timer(self.DEALER_HIT, 0)
                self.flags.dealer_turn_status = 'done'
                pygame.time.set_timer(self.DEALER_TURN_OVER, 20, loops=1)
        elif event.type == self.DEALER_TURN_OVER:
            self.game_manager.state = GameState.RESOLUTION

    def handle_resolution_input(self, event: pygame.event.Event) -> None:
        """Handles input during the resolution phase."""
        result: str = self.textbox.handle_dialogue_input(event)
        if result == 'done':
            if not self.flags.review_hands_lines_ready:
                logging.info("Resolution dialogue finished. Resetting game state.")
                self.game_manager.state = GameState.RESET
            elif not self.flags.endgame_lines_ready:
                self.flags.endgame_lines_ready = True
            else:
                logging.info("Endgame dialogue finished. Resetting game state.")
                self.game_manager.state = GameState.RESET

    def update_intro(self, now: int) -> None:
        """Updates the intro dialogue animation."""
        if not self.flags.intro_lines_set:
            self.textbox.set_lines(INTRO_DIALOGUE)
            self.flags.intro_lines_set = True
            logging.info("Intro dialogue set.")
        self.textbox.animate(now)

    def update_reset(self, now: int) -> None:
        """Resets the game state and shuffles the deck."""
        self.flags.reset()
        self.player.reset_hand()
        self.dealer.reset_hand()
        self.game_manager.deck = Deck()
        self.game_manager.deck.shuffle()
        logging.info(f"Game reset. Score [Player: {self.player.games_won} | Dealer: {self.dealer.games_won}]")
        self.game_manager.state = GameState.DEALING

    def update_dealing(self, now: int) -> None:
        """Updates the dealing phase animation."""
        if not self.flags.dealing_lines_set:
            self.textbox.set_lines(DEALING_TEXT, show_arrow=False)
            self.flags.dealing_lines_set = True
            logging.info("Dealing dialogue set.")
        self.textbox.animate(now)

    def update_player_turn(self, now: int) -> None:
        """Updates the player's turn logic and dialogue."""
        if len(self.player.hand.cards) == 2 and self.player.hand.total == 21:
            if not self.flags.player_blackjack_stage:
                self.flags.player_blackjack_stage = 'start'
            if self.flags.player_blackjack_stage == 'start':
                # Dealer cannot have blackjack
                if self.dealer.hand.cards[0].value not in ('10', 'J', 'Q', 'K', 'A'):
                    self.textbox.set_lines(PLAYER_BLACKJACK_WIN)
                    self.flags.player_blackjack_stage = 'done'
                    self.player.win_game()
                    logging.info("Player wins with blackjack.")
                else:
                    self.textbox.set_lines(PLAYER_BLACKJACK_DEALER_CHECK)
                    self.flags.player_blackjack_stage = 'reveal'
                    logging.info("Player blackjack, checking dealer for blackjack.")
            elif self.flags.player_blackjack_stage == 'reveal':
                if self.textbox.line_fully_displayed and self.textbox.current_line_index == 3:
                    self.flags.dealer_second_card_visible = True
                    if len(self.dealer.hand.cards) == 2 and self.dealer.hand.total == 21:
                        self.textbox.set_lines(DEALER_ALSO_BLACKJACK)
                        logging.info("Dealer also has blackjack. Draw.")
                    else:
                        self.textbox.set_lines(DEALER_NO_BLACKJACK)
                        self.player.win_game()
                        logging.info("Player wins, dealer does not have blackjack.")
                    self.flags.player_blackjack_stage = 'done'
            self.textbox.animate(now)
            return
        if self.player.hand.total > 21:
            if not self.flags.player_bust_lines_set:
                self.textbox.set_lines(PLAYER_BUST)
                self.flags.player_bust_lines_set = True
                self.dealer.win_game()
                logging.info("Player bust. Dealer wins.")
        elif not self.flags.player_turn_lines_set:
            self.textbox.set_lines(HIT_OR_STAND_INPUT, show_arrow=False)
            self.flags.player_turn_lines_set = True
            logging.info("Player turn dialogue set.")
        elif self.flags.player_stands_lines_ready and not self.flags.player_stands_lines_set:
            self.textbox.set_lines(PLAYER_STANDS)
            self.flags.player_stands_lines_set = True
            logging.info("Player stands dialogue set.")
        self.textbox.animate(now)

    def update_dealer_turn(self, now: int) -> None:
        """Updates the dealer's turn logic and dialogue."""
        if not self.flags.dealer_turn_lines_set:
            self.textbox.set_lines(DEALER_TURN_START, show_arrow=False)
            self.flags.dealer_turn_lines_set = True
            logging.info("Dealer turn dialogue set.")
        self.textbox.animate(now)

    def update_resolution(self, now: int) -> None:
        """Updates the resolution phase logic and dialogue."""
        if len(self.dealer.hand.cards) == 2 and self.dealer.hand.total == 21:
            if not self.flags.dealer_blackjack_lines_set:
                self.textbox.set_lines(DEALER_WINS_BLACKJACK)
                self.flags.dealer_blackjack_lines_set = True
                self.dealer.win_game()
                logging.info("Dealer wins with blackjack")
        elif self.dealer.hand.total > 21:
            if not self.flags.dealer_bust_lines_set:
                self.textbox.set_lines(DEALER_BUST)
                self.flags.dealer_bust_lines_set = True
                self.player.win_game()
                logging.info("Dealer bust. Player wins.")
        else:
            self.flags.review_hands_lines_ready = True
        if self.flags.review_hands_lines_ready and not self.flags.review_hands_lines_set:
            review_text = [
                REVIEW_HANDS_TEMPLATE[0],
                REVIEW_HANDS_TEMPLATE[1].format(self.player.hand.total, self.dealer.hand.total)
            ]
            self.textbox.set_lines(review_text)
            self.flags.review_hands_lines_set = True
            logging.info("Reviewing hands.")
        elif self.flags.endgame_lines_ready:
            if self.player.hand.total > self.dealer.hand.total:
                if not self.flags.player_wins_lines_set:
                    self.textbox.set_lines(PLAYER_WINS_HAND)
                    self.flags.player_wins_lines_set = True
                    self.player.win_game()
                    logging.info(f"Player wins {self.player.hand.total} vs {self.dealer.hand.total}")
            elif self.player.hand.total < self.dealer.hand.total:
                if not self.flags.dealer_wins_lines_set:
                    self.textbox.set_lines(DEALER_WINS_HAND)
                    self.flags.dealer_wins_lines_set = True
                    self.dealer.win_game()
                    logging.info(f"Dealer wins {self.dealer.hand.total} vs {self.player.hand.total}")
            else:
                if not self.flags.game_draw_lines_set:
                    self.textbox.set_lines(GAME_DRAW)
                    self.flags.game_draw_lines_set = True
                    logging.info("Game is a draw.")
        self.textbox.animate(now)

    # Add draw methods
    def draw_scoreboard(self) -> None:
        """Draws the scoreboard on the screen."""
        scoreboard_title = self.font_small.render("Games Won:", True, Colours.WHITE)
        scoreboard_player = self.font_small.render(f"PLAYER: {self.player.games_won}", True, Colours.WHITE)
        scoreboard_dealer = self.font_small.render(f"DEALER: {self.dealer.games_won}", True, Colours.WHITE)
        self.screen.blit(scoreboard_title, (Scoreboard.TEXT_X, Scoreboard.TITLE_Y))
        self.screen.blit(scoreboard_player, (Scoreboard.TEXT_X, Scoreboard.PLAYER_Y))
        self.screen.blit(scoreboard_dealer, (Scoreboard.TEXT_X, Scoreboard.DEALER_Y))

    def draw_playing(self) -> None:
        """Draws the cards during play."""
        player_x, player_y = CardLayout.PLAYER_FIRST_X, CardLayout.PLAYER_FIRST_Y
        dealer_x, dealer_y = CardLayout.DEALER_FIRST_X, CardLayout.DEALER_FIRST_Y
        for i, card in enumerate(self.player.hand.cards):
            card.render(self.screen, player_x, player_y)
            player_x += CardLayout.PLAYER_OFFSET_X
            player_y -= CardLayout.PLAYER_OFFSET_Y
        for i, card in enumerate(self.dealer.hand.cards):
            if i == 1 and not self.flags.dealer_second_card_visible:
                self.screen.blit(Card.get_card_back(), (dealer_x, dealer_y))
            else:
                card.render(self.screen, dealer_x, dealer_y)
            dealer_x -= CardLayout.DEALER_OFFSET_X

    def draw_screen(self) -> None:
        """Draws the entire game screen."""
        if self.game_manager.state == GameState.INTRO and self.textbox.current_line_index < 11:
            self.screen.fill(Colours.BG_DARK_GREY)
        else:
            self.screen.blit(Display.BACKGROUND, (0, 0))
            self.draw_scoreboard()
        self.textbox.draw(self.screen)
        if self.game_manager.state is not GameState.INTRO:
            self.draw_playing()
        pygame.display.flip()

    def update_music(self) -> None:
        """Plays the appropriate background music for the current game state."""
        if self.game_manager.state == GameState.INTRO:
            desired_music = Audio.INTRO_MUSIC
        else:
            desired_music = Audio.MAIN_MUSIC
        if self.game_manager.current_music != desired_music:
            try:
                pygame.mixer.music.load(desired_music)
                pygame.mixer.music.set_volume(Audio.MUSIC_VOLUME)
                pygame.mixer.music.play(-1)
                self.game_manager.current_music = desired_music
                logging.info(f"Playing music: {desired_music}")
            except Exception as e:
                logging.error(f"Error playing music: {e}")

    def __repr__(self) -> str:
        """Returns string representation of current game state."""
        return (f"GameController(state={self.game_manager.state}, "
                f"player={self.player}, dealer={self.dealer}, "
                f"flags={self.flags})")
