from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer, pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
import shared_state


class ShopPage(QWidget):
    shop_clicked = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)

        grid = QGridLayout()
        self.setLayout(grid)

        grid.setContentsMargins(20, 20, 20, 20)
        grid.setSpacing(5)
        grid.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ---------------- BACKGROUND ----------------
        bg = QLabel(self)
        bg_pix = QPixmap("shop.png").scaled(240, 280, Qt.AspectRatioMode.KeepAspectRatio)
        bg.setPixmap(bg_pix)
        bg.lower()

        # ---------------- UI LABELS ----------------
        self.funds = QLabel(f"funds: ${shared_state.money}")
        self.display_food = QLabel(f"food: {shared_state.food}")

        grid.addWidget(self.funds, 0, 0)
        grid.addWidget(self.display_food, 0, 1)

        # ---------------- ITEMS ----------------
        self.items = {
            "free gift": 10,
            "food": 15,
            "clown nose": 35,
            "party hat": 50
        }

        for i, key in enumerate(self.items):

            btn = QPushButton(f"{key}: ${self.items[key]}")

            btn.clicked.connect(lambda _, k=key, b=btn: self.buy(k, b))

            row, col = divmod(i, 2)
            grid.addWidget(btn, row + 1, col)

    # ---------------- BUY LOGIC ----------------
    def buy(self, item, btn):
        cost = self.items[item]

        if shared_state.money < cost:
            return

        shared_state.money -= cost

        if item == "food":
            shared_state.food += 1
            self.display_food.setText(f"food: {shared_state.food}")

        self.funds.setText(f"funds: ${shared_state.money}")
        btn.setText("SOLD OUT")
        btn.setEnabled(False)