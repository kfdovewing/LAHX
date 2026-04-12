import sys
from PyQt6.QtWidgets import QWidget, QStackedWidget, QApplication, QLabel
from PyQt6.QtCore import pyqtSignal, Qt

# Assuming these are your file names
from shop import ShopPage
from todolist import TodoList
from home import StatsWindow
from graphic_icon import MainWindow 
from engine import GameEngine
from starter_menu import start
import shared_state


app = QApplication(sys.argv)


# buddy = ""
# money = 0
# food = 0
# hunger = 0
# happiness = 100

# def cat():
#     global buddy
#     buddy = "assets/buddies/cat.png"

# def frog():
#     global buddy
#     buddy = "assets/buddies/froggy.png"

# def hat():
#     global buddy
#     buddy = "assets/buddies/hat_guy.png"

# def party():
#     global buddy
#     buddy = "assets/buddies/party_guy.png"



class run(QWidget):
    def __init__(self):
        super().__init__()
        
        # 1. Window Setup
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        w, h = 240, 280
        # self.resize(w, h)

        # 2. Setup the Stack
        self.stack = QStackedWidget(self)
        self.resize(400,400)
        self.stack.resize(400,400)
        # self.stack.setGeometry(0, 0, 400, 400)

        # 3. Initialize Pages (CREATE THEM FIRST)
        self.vars = shared_state.shared()
        self.start_page = start()
        self.icon = MainWindow() 
        self.home_page = StatsWindow()
        self.shop_page = ShopPage()
        self.email_page = TodoList()

        # 4. Add to Stack (AFTER CREATING THEM)
        self.stack.addWidget(self.start_page)
        self.stack.addWidget(self.icon)
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.shop_page)
        self.stack.addWidget(self.email_page)
        self.stack.addWidget(self.vars)

        self.stack.setCurrentWidget(self.start_page)

        # 5. Connect the Signal
        self.start_page.select.connect(self.handle_child_start)

        self.icon.action_triggered.connect(self.handle_child_action)
        self.icon.shop_clicked.connect(self.handle_child_action_shop)
        self.icon.todo_clicked.connect(self.handle_child_action_todo)

        self.home_page.action_triggered.connect(self.handle_child_start)
        self.home_page.shop_clicked.connect(self.handle_child_action_shop)
        self.home_page.todo_clicked.connect(self.handle_child_action_todo)

        self.email_page.action_triggered.connect(self.handle_child_action)
        self.email_page.shop_clicked.connect(self.handle_child_action_shop)
        self.email_page.icon_clicked.connect(self.handle_child_start)

    def handle_child_start(self):
        print('Signal Received: Updating and Switching')
        # This triggers the code above!
        self.icon.update_pet_display() 
        self.screen = app.primaryScreen().availableGeometry()
        self.setGeometry(self.screen.right()-240,0,240, 280)
        self.stack.setCurrentWidget(self.icon)

    def handle_child_action(self):
        print('Signal Received: Switching to Home Page')
        self.home_page.update_pet_display() 
        self.screen = app.primaryScreen().availableGeometry()
        self.showMaximized()
        self.stack.resize(self.screen.width(),self.screen.height())
        self.stack.setCurrentWidget(self.home_page)

    def handle_child_action_shop(self):
        print('Signal Received: Switching to Shop Page')
        self.screen = app.primaryScreen().availableGeometry()
        self.showMaximized()
        self.stack.resize(self.screen.width(),self.screen.height())
        self.stack.setCurrentWidget(self.shop_page)

    def handle_child_action_todo(self):
        print('Signal Received: Switching to todo Page')
        self.setGeometry(self.screen.right()-350,0,350, 500)
        self.stack.resize(350,500)
        self.stack.setCurrentWidget(self.email_page)
    def handle_child_action_shop(self):
        print('Signal Received: Updating Shop and Switching')
        
        # Refresh the numbers before the user sees the page
        self.shop_page.refresh_ui() 
        
        self.resize(400, 500) # Shop is usually bigger than the icon
        self.stack.setCurrentWidget(self.shop_page)

# --- START THE APP --- # Initialize App here
main_window = run()
main_window.show()
sys.exit(app.exec())