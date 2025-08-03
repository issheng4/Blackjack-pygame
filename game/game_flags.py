class GameFlags:
    def __init__(self):
        self.has_started_dealing = False
        self.dealer_second_card_visible = False
        self.player_blackjack_stage = None
        self.dealer_turn_status = None

        self.intro_lines_set = False

        self.dealing_lines_set = False

        self.player_turn_lines_set = False
        self.player_stands_lines_ready = False
        self.player_stands_lines_set = False
        self.player_bust_lines_set = False

        self.dealer_turn_lines_set = False

        self.dealer_blackjack_lines_set = False
        self.dealer_bust_lines_set = False
        self.review_hands_lines_ready = False
        self.review_hands_lines_set = False
        self.endgame_lines_ready = False
        self.player_wins_lines_set = False
        self.dealer_wins_lines_set = False
        self.game_draw_lines_set = False

    def reset(self):
        for attr in vars(self):
            setattr(self, attr, False if isinstance(getattr(self, attr), bool) else None)