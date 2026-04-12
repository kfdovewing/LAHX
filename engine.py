from PyQt6.QtCore import QTimer
import shared_state

class GameEngine:
    def __init__(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(2000*60)  # every 2 seconds

    def tick(self):
        shared_state.shared.hunger = max(0, shared_state.shared.hunger + 1)

        print("tick", shared_state.shared.hunger) # debug