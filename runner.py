import sys
import json
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
engine = GameEngine()

#change

class run(QWidget):
    def __init__(self):
        super().__init__()
        
        # 1. Window Setup
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        w, h = 240, 280
        # self.resize(w, h)

        # 2. Setup the Stack
        self.stack = QStackedWidget(self)
        self.resize(400,400)
        self.stack.resize(400,400)
        # self.stack.setGeometry(0, 0, 400, 400)

        # 3. Initialize Pages (CREATE THEM FIRST)
        self.vars = shared_state.shared() #creates the variables so they don't reload
        self.start_page = start() #choose egg start screen
        self.icon = MainWindow() #gadget in small form on screen
        self.home_page = StatsWindow()
        self.shop_page = ShopPage()
        self.list_page = TodoList() 

        # 4. Add to Stack (AFTER CREATING THEM)
        self.stack.addWidget(self.start_page)
        self.stack.addWidget(self.icon)
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.shop_page)
        self.stack.addWidget(self.list_page)
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

        self.list_page.action_triggered.connect(self.handle_child_action)
        self.list_page.shop_clicked.connect(self.handle_child_action_shop)
        self.list_page.icon_clicked.connect(self.handle_child_start)

        self.shop_page.action_triggered.connect(self.handle_child_action) # Home Icon -> Home Page
        self.shop_page.icon_clicked.connect(self.handle_child_start)     # Egg Icon -> Small Icon
        self.shop_page.todo_clicked.connect(self.handle_child_action_todo)

        self.read_assignments()



    def read_assignments(self):
        try:
            # Open and read the file
            with open('saved_assignments.json', 'r') as f:
                info = json.load(f)
                
            print(" Successfully read the array from file!")
            
            self.list_page.add_task(info)
                
            return info

        except FileNotFoundError:
            print("❌ Error: 'saved_array.json' does not exist yet.")
            print("Please send data from your extension first to create the file.")
            return None




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
        print('Signal Received: Updating Shop and Switching')
        
        # 1. Ensure we are in "Normal" mode (not Maximized)
        self.setWindowState(Qt.WindowState.WindowNoState)
        
        # 2. Update the Shop UI numbers
        self.shop_page.refresh_ui() 
        
        # 3. Define the dimensions
        new_w = 400
        new_h = 500
        
        # 4. Get the usable screen area
        screen_geo = QApplication.primaryScreen().availableGeometry()
        
        # 5. Calculate X: Right edge of screen minus the width of our window
        new_x = screen_geo.right() - new_w
        new_y = 0  # Top of the screen
        
        # 6. Apply everything at once
        self.setGeometry(new_x, new_y, new_w, new_h)
        self.stack.resize(new_w, new_h)
        
        # 7. Finally, swap the page
        self.stack.setCurrentWidget(self.shop_page)

    def handle_child_action_todo(self):
        print('Signal Received: Switching to todo Page')
        # Force out of maximized mode if coming from Home
        self.setWindowState(Qt.WindowState.WindowNoState)
        
        w, h = 350, 500
        screen_geo = QApplication.primaryScreen().availableGeometry()
        
        # Calculate right-aligned X position
        new_x = screen_geo.right() - w
        
        self.setGeometry(new_x, 0, w, h)
        self.stack.resize(w, h)
        self.stack.setCurrentWidget(self.list_page)


# --- START THE APP --- # Initialize App here
main_window = run()
main_window.show()
sys.exit(app.exec())
