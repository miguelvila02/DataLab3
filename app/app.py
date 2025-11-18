import sys
from PyQt5.QtGui import QPalette, QColor, QIcon, QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class PagInit(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Premier League Match Predictor")
        label = QLabel("Welcome to the Premier League Match Predictor!")
        label.setAlignment(Qt.AlignCenter)
        label.setMargin(10)
        self.setCentralWidget(label)
        self.show()

        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)


app = QApplication([])
window = PagInit()
window.show()
app.exec_()