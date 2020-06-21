import sys

from PySide2.QtWidgets import QApplication
from AppScreenQt import AppScreenQt

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = AppScreenQt()
    view.show()
    sys.exit(app.exec_())