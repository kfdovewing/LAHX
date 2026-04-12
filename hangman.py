import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QPushButton, QLineEdit, QHBoxLayout
)
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt


# word list
WORD_LIST = ["rhythm", "crypt", "myth", "lynx", "nymph",
    "sphinx", "pneumonia", "mnemonic", "xylophone", "quartz",
    "jazzy", "fizz", "buzz", "jazz", "quiz",
    "awkward", "bagpipes", "buffoon", "blizzard", "jackpot",
    "kiosk", "waltz", "fjord", "gazebo", "vortex",
    "zigzag", "zephyr", "oxidize", "pixel", "puzzle",
    "subway", "cryptic", "transcript", "vivid", "bizarre",
    "jigsaw", "twelfth", "strength", "scratch", "scratchy",
    "haphazard", "convoluted", "awkwardly", "buzzing", "fizzing"]

ALPHABET = list("abcdefghijklmnopqrstuvwxyz")


class Hangman(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hangman")
        self.setGeometry(100, 100, 600, 400)

        # game state
        self.secret_word = random.choice(WORD_LIST)
        self.length = len(self.secret_word)
        self.lives = 6
        self.prev_guess = []
        self.display_word = ["_"] * self.length

        # UI

        main_layout = QVBoxLayout()

        # 🟦 TOP: drawing area
        self.canvas = Canvas(self)
        self.canvas.setMinimumHeight(300)
        main_layout.addWidget(self.canvas)

        # 🟨 BOTTOM: UI
        ui_layout = QVBoxLayout()

        # word display
        self.label = QLabel(" ".join(self.display_word))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 28px; margin: 10px;")
        ui_layout.addWidget(self.label)

        # input row
        input_layout = QHBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter a letter...")
        input_layout.addWidget(self.input)

        self.button = QPushButton("Guess")
        self.button.clicked.connect(self.guess)
        input_layout.addWidget(self.button)

        ui_layout.addLayout(input_layout)

        # message
        self.message = QLabel("")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ui_layout.addWidget(self.message)

        main_layout.addLayout(ui_layout)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #828e94;")

    # 🎯 Guess logic
    def guess(self):
        user_guess = self.input.text().lower()
        self.input.clear()

        if len(user_guess) != 1 or user_guess not in ALPHABET:
            self.message.setText("Invalid letter")
            return

        if user_guess in self.prev_guess:
            self.message.setText("Already guessed")
            return

        self.prev_guess.append(user_guess)

        if user_guess in self.secret_word:
            self.message.setText("Correct!")

            for i, letter in enumerate(self.secret_word):
                if letter == user_guess:
                    self.display_word[i] = user_guess

        else:
            self.message.setText("Wrong!")
            self.lives -= 1

        self.label.setText(" ".join(self.display_word))
        self.update()  # redraw hangman

        # win/lose
        if "_" not in self.display_word:
            self.message.setText("YOU WIN")
            self.button.setEnabled(False)

        elif self.lives == 0:
            self.message.setText(f"YOU LOST: {self.secret_word}")
            self.button.setEnabled(False)

    # 🎨 Drawing hangman
class Canvas(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.black, 3)
        painter.setPen(pen)

        # gallows
        painter.drawLine(50, 250, 200, 250)
        painter.drawLine(100, 250, 100, 50)
        painter.drawLine(100, 50, 250, 50)
        painter.drawLine(250, 50, 250, 80)

        lives = self.game.lives

        if lives <= 5:
            painter.drawEllipse(225, 80, 50, 50)
        if lives <= 4:
            painter.drawLine(250, 130, 250, 200)
        if lives <= 3:
            painter.drawLine(250, 150, 220, 180)
        if lives <= 2:
            painter.drawLine(250, 150, 280, 180)
        if lives <= 1:
            painter.drawLine(250, 200, 220, 240)
        if lives <= 0:
            painter.drawLine(250, 200, 280, 240)

app = QApplication(sys.argv)
window = Hangman()
window.show()
sys.exit(app.exec())