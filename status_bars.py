import sys
import shared_state
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QProgressBar, QGridLayout
from PyQt6.QtCore import QTimer

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("tester")
window.setGeometry(100, 100, 400, 300)

grid = QGridLayout()
window.setLayout(grid)

hunger_bar = QProgressBar()
hunger_bar.setGeometry(50, 80, 200, 30)
hunger_bar.setValue(shared_state.hunger)
hunger_label = QLabel("Hunger")

happy_bar = QProgressBar()
happy_bar.setGeometry(50, 80, 200, 30)
happy_bar.setValue(shared_state.happiness)
happy_label = QLabel("Happiness")

grid.addWidget(hunger_label, 0,0)
grid.addWidget(happy_label, 1, 0)
grid.addWidget(hunger_bar, 0, 1)
grid.addWidget(happy_bar, 1, 1)

grid.setHorizontalSpacing(20)
grid.setVerticalSpacing(10)
timer = QTimer()
def increase_hunger():
    shared_state.hunger+=1
    hunger_bar.setValue(shared_state.hunger)



timer.timeout.connect(increase_hunger)
timer.start(1000)


def decrease_happiness():
    shared_state.happiness-=1
    happy_bar.setValue(shared_state.happiness)

timer2 = QTimer()

timer2.timeout.connect(decrease_happiness)
timer2.start(5000)

window.show()
sys.exit(app.exec())
