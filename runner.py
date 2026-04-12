import sys
from PyQt6.QtWidgets import QWidget, QStackedWidget, QApplication, QLabel
from PyQt6.QtCore import pyqtSignal, Qt

# Assuming these are your file names
from shop import ShopPage
from todolist import TodoList
from home import StatsWindow
from graphic_icon import MainWindow 
from engine import GameEngine

app = QApplication(sys.argv)
engine = GameEngine()

class run(QWidget):
    def __init__(self):
        super().__init__()
        
        # 1. Window Setup
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        w, h = 240, 280
        self.setFixedSize(w, h)

        # 2. Setup the Stack
        self.stack = QStackedWidget(self)
        self.stack.setGeometry(0, 0, w, h)

        # 3. Initialize Pages (CREATE THEM FIRST)
        self.icon = MainWindow() 
        self.home_page = StatsWindow()
        self.shop_page = ShopPage()
        self.email_page = TodoList()

        # 4. Add to Stack (AFTER CREATING THEM)
        self.stack.addWidget(self.icon)
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.shop_page)
        self.stack.addWidget(self.email_page)

        self.stack.setCurrentWidget(self.icon)

        # 5. Connect the Signal
        self.icon.action_triggered.connect(self.handle_child_action)
        self.icon.shop_clicked.connect(self.handle_child_action_shop)
        self.icon.todo_clicked.connect(self.handle_child_action_todo)

    def handle_child_action(self):
        print('Signal Received: Switching to Home Page')
        self.stack.setCurrentWidget(self.home_page)
    def handle_child_action_shop(self):
        print('Signal Received: Switching to Home Page')
        self.stack.setCurrentWidget(self.shop_page)
    def handle_child_action_todo(self):
        print('Signal Received: Switching to Home Page')
        self.stack.setCurrentWidget(self.email_page)

# --- START THE APP --- # Initialize App here
main_window = run()
main_window.show()
sys.exit(app.exec())