import sys
from PyQt5.QtWidgets import QApplication
from play_match_window import play_match_window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = play_match_window()
    window.show()
    sys.exit(app.exec_())