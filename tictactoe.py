import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMessageBox
from PyQt6.QtGui import QIcon
import shared_state


class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setFixedSize(300, 300)

        self.current_player = "X" 
        self.board = [["" for _ in range(3)] for _ in range(3)]

        self.layout = QGridLayout()
        self.buttons = [[QPushButton() for _ in range(3)] for _ in range(3)]

        for row in range(3):
            for col in range(3):
                button = self.buttons[row][col]
                button.setFixedSize(90, 90)
                button.clicked.connect(lambda _, r=row, c=col: self.make_move(r, c))
                self.layout.addWidget(button, row, col)

        self.setLayout(self.layout)

    def make_move(self, row, col):
        if self.board[row][col] != "":
            return

        self.board[row][col] = self.current_player

        if self.current_player == "X":
            self.buttons[row][col].setIcon(QIcon("assets/x.png"))
        else:
            self.buttons[row][col].setIcon(QIcon("assets/o.png"))

        self.buttons[row][col].setIconSize(self.buttons[row][col].size())

        if self.check_winner():
            QMessageBox.information(self, "Game Over", f"Player {self.current_player} wins!")
            self.reset_game()
            return

        if self.is_draw():
            QMessageBox.information(self, "Game Over", "It's a draw!")
            self.reset_game()
            return

        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        # Rows
        for row in self.board:
            if row[0] == row[1] == row[2] != "":
                return True

        # Columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                return True

        # Diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True

        return False

    def is_draw(self):
        for row in self.board:
            if "" in row:
                return False
        return True

    def reset_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]

        for row in range(3):
            for col in range(3):
                self.buttons[row][col].setIcon(QIcon())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TicTacToe()
    window.show()
    sys.exit(app.exec())
