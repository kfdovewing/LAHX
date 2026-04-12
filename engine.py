from PyQt6.QtCore import QTimer
import shared_state

class GameEngine:
    def __init__(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(2000)  # every 2 seconds

    def tick(self):
        shared_state.hunger = max(0, shared_state.hunger + 1)
        shared_state.happiness = max(0, shared_state.happiness - 1)

        print("tick", shared_state.hunger, shared_state.happiness)  # debug