from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import QTimer, pyqtSignal
import shared_state

class StatsWindow(QWidget):
    action_triggered = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Stats")

        layout = QVBoxLayout()

        self.hunger_bar = QProgressBar()
        self.happy_bar = QProgressBar()

        layout.addWidget(QLabel("Hunger"))
        layout.addWidget(self.hunger_bar)
        layout.addWidget(QLabel("Happiness"))
        layout.addWidget(self.happy_bar)

        self.setLayout(layout)

        # update timer for THIS window only
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(200)

    def update_ui(self):
        self.hunger_bar.setValue(shared_state.hunger)
        self.happy_bar.setValue(shared_state.happiness)