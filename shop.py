import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Shop")
window.setGeometry(100, 100, 500, 300)

grid = QGridLayout()
window.setLayout(grid)


# shop background
bg = QLabel(window)
bg_pix = QPixmap("shop.png")

bg_pix = bg_pix.scaled(
    window.size(),
    Qt.AspectRatioMode.KeepAspectRatio,
    Qt.TransformationMode.SmoothTransformation
)

bg.setPixmap(bg_pix)
bg.setGeometry(0, 0, 400, 300)
bg.lower()

window.showMaximized()


funds = QLabel(f"funds: ${shared_state.money}")
display_food = QLabel(f"food: {shared_state.food}")

grid.addWidget(funds, 0, 0)
grid.addWidget(display_food, 0, 1)


items = {
    "free gift": -10,
    "food": 15,
    "clown nose": 35,
    "party hat": 50
}

#checks if you have enough money
def buy_item(items, index_list, i, total):
    index = index_list[i]
    cost = items[index]

    if total < cost:
        invalid = QLabel("Not enough money!")
        grid.addWidget(invalid, 2, 0)
        QTimer.singleShot(2000, invalid.deleteLater)
        return False

    return True

#updates money variable
def update_money(items, index_list, i, total):
    cost = items[index_list[i]]
    if i == 1:
        food = True
    else:
        food = False
    return total - cost, food


#updates display for FUNDS ONLY
def update_display(total, btn):
    funds.setText(f"funds: ${total}")
    btn.setText("SOLD OUT")
    btn.setEnabled(False)

#combined function to run all the functions on click
def update(index_list, i, btn):
    global money, food, display_food

    if buy_item(items, index_list, i, shared_state.money):
        shared_state.money, is_food = update_money(items, index_list, i, shared_state.money)
        update_display(shared_state.money, btn)
        if is_food:
            shared_state.food +=1
            display_food.setText(f"food: {shared_state.food}")


#makes the buttons
def list_items(items):
    index_list = list(items.keys())

    for i in range(len(index_list)):
        key = index_list[i]
        cost = items[key]

        display_cost = abs(cost) if cost < 0 else cost

        btn = QPushButton(f"{key}: ${display_cost}")

        btn.clicked.connect(lambda checked=False, i=i, btn=btn: update(index_list, i, btn))

        row, col = divmod(i, 4)
        grid.addWidget(btn, row + 1, col)


list_items(items)

window.show()
sys.exit(app.exec())