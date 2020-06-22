import sys

from PyQt5.QtWidgets import QApplication
from GameViewQt import GameViewQt

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game_view = GameViewQt()
    game_view.show()
    sys.exit(app.exec_())