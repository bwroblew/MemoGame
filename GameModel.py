import random

import Settings

class GameModel:
    def __init__(self):
        self.card_selected = None
        self.game_started = False
        self.board = None
        self.collected = None
        self.points = 0
        self.max_points = None

    def place_cards(self):
        row_size, col_size = Settings.CARDS_LAYOUT
        cards_num = row_size * col_size
        assert cards_num % 2 == 0
        different_cards_num = cards_num // 2
        self.max_points = different_cards_num
        signs = [sign for sign in range(1, different_cards_num+1)] * 2
        random.shuffle(signs)

        self.board = []
        self.collected = []
        for col in range(col_size):
            row = []
            for cell in range(row_size):
                sign = signs.pop()
                row.append(sign)
            self.board.append(row)
            self.collected.append([False for _ in range(row_size)])

    def restart_game(self):
        self.game_started = True
        self.points = 0
        self.place_cards()

    def get_card_sign(self, x, y):
        assert len(self.board) > 0
        return self.board[y][x]

    def add_point(self):
        self.points += 1

    def get_points(self):
        return self.points

    def is_game_runnning(self):
        return self.game_started

    def is_game_finished(self):
        if self.points == self.max_points:
            return True
        return False

    def select_card(self, x, y):
        if self.card_selected == (x, y) or self.was_collected(x, y):
            return False
        self.visible_cards = []
        if self.card_selected is None:
            self.card_selected = (x, y)
            self.visible_cards.append(self.card_selected)
        else:
            self.visible_cards.append(self.card_selected)
            self.visible_cards.append((x, y))
            if self.get_card_sign(*self.card_selected) == self.get_card_sign(x, y):
                self.add_point()
                self.collect(*self.card_selected)
                self.collect(x, y)
            self.card_selected = None

    def get_visible_cards(self):
        return self.visible_cards

    def collect(self, x, y):
        self.collected[y][x] = True

    def was_collected(self, x, y):
        return self.collected[y][x]