from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QButtonGroup, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QSizePolicy, QLabel, QWidget

from GameModel import GameModel
import Settings


class GameViewQt(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(Settings.GAME_TITLE)
        self.game = GameModel()
        self.main_window_layout = QVBoxLayout()
        self.setMinimumSize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
        self.initialize_board()
        self.initialize_help()
        self.add_start_button()
        self.add_points_view()
        self.setLayout(self.main_window_layout)
        self.start_game()

    def initialize_board(self):
        frame_widget = QWidget()
        frame_widget.setFixedSize(Settings.BOARD_WIDTH, Settings.BOARD_HEIGHT)
        
        frame_layout = QHBoxLayout()
        frame_layout.addWidget(frame_widget)
        self.main_window_layout.addLayout(frame_layout)

        cards_layout = QGridLayout(frame_widget)
        cards_layout.setSpacing(0)
        self.cards = QButtonGroup()
        row_size, col_size = Settings.CARDS_LAYOUT
        for card_id in range(row_size * col_size):
            button = QPushButton()
            policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            button.setSizePolicy(policy)
            x, y = self.card_id_to_coord(card_id)
            button.setStyleSheet(Settings.Qt.REVERSE_CARD_STYLE)
            button.setText(Settings.REVERSE_CARD_MARK)
            self.cards.addButton(button, card_id)
            cards_layout.addWidget(button, y, x)
        
        self.cards.buttonPressed.connect(self.card_clicked)
        self.main_window_layout.addLayout(cards_layout)

    def initialize_help(self):
        help_layout = QVBoxLayout()
        self.help_label = QLabel(Settings.HELP_TEXT)
        self.help_label.setWordWrap(True)
        self.help_label.setFont(QFont("Arial", 12))
        self.help_label.setAlignment(QtCore.Qt.AlignJustify)

        self.help_label.setStyleSheet(Settings.Qt.HELP_STYLE)
        help_layout.addWidget(self.help_label)
        self.main_window_layout.addLayout(help_layout)

    def add_start_button(self):
        self.start_button = QPushButton(Settings.NEW_GAME_BUTTON_TEXT, self)
        self.start_button.setStyleSheet(Settings.Qt.START_BUTTON_STYLE)
        self.main_window_layout.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start_game)

    def add_points_view(self):
        points_layout = QHBoxLayout()

        points_label_key = QLabel(Settings.POINTS_LABEL)
        points_label_key.setStyleSheet(Settings.Qt.POINTS_STYLE)

        self.points_label_value = QLabel("0")
        self.points_label_value.setStyleSheet(Settings.Qt.POINTS_STYLE)

        points_layout.addWidget(points_label_key)
        points_layout.addWidget(self.points_label_value)
        self.main_window_layout.addLayout(points_layout)

    def start_game(self):
        self.start_button.setText(Settings.NEW_GAME_BUTTON_TEXT)
        self.game.restart_game()
        self.clear_board()
        self.points_label_value.setText(str(self.game.get_points()))

    def card_clicked(self, btn):
        if not self.game.is_game_runnning():
            return

        idx = self.cards.id(btn)
        x, y = self.card_id_to_coord(idx)
        if self.game.was_collected(x, y):
            return
        
        self.game.select_card(x, y)
        visible_cards = self.game.get_visible_cards()
        self.points_label_value.setText(str(self.game.get_points()))
        self.clear_board()
        self.show_cards(visible_cards)

        if self.game.is_game_finished():
            self.start_game()
        
    def clear_board(self):
        row_size, col_size = Settings.CARDS_LAYOUT
        for card_id in range(row_size * col_size):
            button = self.cards.button(card_id)
            x, y = self.card_id_to_coord(card_id)
            if self.game.was_collected(x, y):
                button.setStyleSheet(Settings.Qt.COLLECTED_CARD_STYLE)
            else:
                button.setStyleSheet(Settings.Qt.REVERSE_CARD_STYLE)
            button.setText(Settings.REVERSE_CARD_MARK)

    def show_cards(self, cards):
        for card in cards:
            x, y = card
            card_id = self.coord_to_card_id(x, y)
            button = self.cards.button(card_id)
            button.setStyleSheet(Settings.Qt.VISIBLE_CARD_STYLE)
            button.setText(str(self.game.get_card_sign(x, y)))

    def card_id_to_coord(self, number):
        row_size, _ = Settings.CARDS_LAYOUT
        return number % row_size, number // row_size

    def coord_to_card_id(self, x, y):
        row_size, _ = Settings.CARDS_LAYOUT
        return y * row_size + x