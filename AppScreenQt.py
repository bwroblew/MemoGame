from PySide2 import QtCore
from PySide2.QtCore import QTimer
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QVBoxLayout, QGridLayout, QProgressBar, QPushButton, \
    QSizePolicy, QButtonGroup, QHBoxLayout, QLabel, QWidget
from qtpy import QtWidgets

from AppModel import AppModel

import Settings


class AppScreenQt(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.game = AppModel()
        self.mainLayout = QVBoxLayout()
        self.setMinimumSize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
        self._boardSetUp()
        self._OverviewSetUp()
        self._startButtonSetUp()
        self._statsSetUp()
        self.setLayout(self.mainLayout)

    def _OverviewSetUp(self):
        style =   """ 
        border: 2px solid gray;
        padding: 0 15px;
        background: gray;
        color: white;"""
        overviewLayout = QVBoxLayout()
        self.overview = QLabel("Zdobywaj punkty poprzez odkrywanie i łączenie w pary kart z takimi samymi liczbami!"
        " Gra ma na celu trening pamięci i koncentracji, dlatego nie jest w niej liczony czas!"
        " Nie spiesz się! Gdy połączysz ze sobą wszystie karty, gra rozpocznie się ponownie.")
        self.overview.setWordWrap(True)
        font = QFont("Arial", 12)
        self.overview.setFont(font)
        self.overview.setAlignment(QtCore.Qt.AlignJustify)

        self.overview.setStyleSheet(style)
        overviewLayout.addWidget(self.overview)
        self.mainLayout.addLayout(overviewLayout)

    def _statsSetUp(self):
        style =   """ 
        text-align: center;
        border: 2px solid gray;
        background: green;
        color: white;"""
        self.stats = QHBoxLayout()

        self.scoreStatic = QLabel("Znalezione pary:")
        self.scoreStatic.setMaximumHeight(40)
        self.scoreStatic.setStyleSheet(style)

        self.score = QLabel("0")
        self.score.setMaximumHeight(40)
        self.score.setStyleSheet(style)

        self.stats.addWidget(self.scoreStatic)
        self.stats.addWidget(self.score)
        self.mainLayout.addLayout(self.stats)

    def _startButtonSetUp(self):
        style =   """ 
        border: 2px solid gray;
        background: green;
        color: white;"""
        self.startButton = QPushButton('Nowa gra', self)
        self.startButton.setStyleSheet(style)
        self.startButton.setMaximumHeight(40)
        self.mainLayout.addWidget(self.startButton)
        self.startButton.clicked.connect(self._onButtonStart)

    def card_id_to_coord(self, number):
        row_size, _ = Settings.CARDS_LAYOUT
        return number % row_size, number // row_size

    def coord_to_card_id(self, x, y):
        row_size, _ = Settings.CARDS_LAYOUT
        return y * row_size + x

    def _boardSetUp(self):
        self.frameWidget = QWidget()
        self.frameLayout = QHBoxLayout()
        self.frameLayout.addStretch()
        self.frameWidget.setFixedSize(Settings.BOARD_WIDTH, Settings.BOARD_HEIGHT)
        self.frameLayout.addWidget(self.frameWidget)
        self.frameLayout.addStretch()
        self.mainLayout.addLayout(self.frameLayout)

        self.cardsGrid = QGridLayout(self.frameWidget)
        self.cardsGrid.setSpacing(0)
        self.cards = QButtonGroup()
        self.cardsGrid
        row_size, col_size = Settings.CARDS_LAYOUT
        for card_id in range(row_size * col_size):
            newButton = QPushButton()
            policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            newButton.setSizePolicy(policy)
            x, y = self.card_id_to_coord(card_id)
            newButton.setStyleSheet("background-color: {}".format(Settings.CARD_REVERSE_COLOR))
            newButton.setText("X")
            self.cards.addButton(newButton, card_id)
            self.cardsGrid.addWidget(newButton, y, x)
        
        self.cards.setExclusive(True)
        self.cards.buttonPressed.connect(self._onCardClick)
        self.mainLayout.addLayout(self.cardsGrid)

    def _onButtonStart(self):
        # if not self.game.is_game_runnning():
        #     return
        self.startButton.setText("Nowa gra")
        self.game.restart_game()
        self.clear_board()
        self.score.setText(str(self.game.get_points()))

    def _onCardClick(self, btn):
        if not self.game.is_game_runnning():
            return
        idx = self.cards.id(btn)
        x, y = self.card_id_to_coord(idx)
        if self.game.was_collected(x, y):
            return
        self.game.select_card(x, y)
        visible_cards = self.game.get_visible_cards()
        self.score.setText(str(self.game.get_points()))
        self.clear_board()
        self.show_cards(visible_cards)
        if self.game.is_game_finished():
            self._onButtonStart()
        
    def clear_board(self):
        row_size, col_size = Settings.CARDS_LAYOUT
        for card_id in range(row_size * col_size):
            button = self.cards.button(card_id)
            x, y = self.card_id_to_coord(card_id)
            if self.game.was_collected(x, y):
                button.setStyleSheet("background-color: {}".format(Settings.COLLECTED_CARD_COLOR))
            else:
                button.setStyleSheet("background-color: {}".format(Settings.CARD_REVERSE_COLOR))
            button.setText("X")

    def show_cards(self, cards):
        for card in cards:
            x, y = card
            card_id = self.coord_to_card_id(x, y)
            button = self.cards.button(card_id)
            button.setStyleSheet("background-color: {}".format(Settings.VISIBLE_CARD_COLOR))
            button.setText(str(self.game.get_card_sign(x, y)))
