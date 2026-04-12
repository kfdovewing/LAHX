import sys
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QProgressBar, QApplication, QPushButton
from PyQt6.QtCore import QTimer, pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
import shared_state

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            event.accept()
            self.clicked.emit()



class StatsWindow(QWidget):
    shop_clicked = pyqtSignal()
    todo_clicked = pyqtSignal()
    action_triggered = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Stats")
        layout = QHBoxLayout()
        screen_dim = QApplication.primaryScreen().availableGeometry()
        # Create a small "HUD" area for the stats
        self.stats_panel = QWidget(self)
        self.stats_panel.setGeometry(10, 0, 400, 100) # Position it in the top-left
        
        panel_layout = QHBoxLayout(self.stats_panel)
        
        # Now add your buttons/bars to panel_layout instead of the window layout
        
        
        # Remove self.setLayout(layout) - we are using the panel instead

        # self.resize(screen_dim.width(), screen_dim.height())
        w = screen_dim.width()
        h = screen_dim.height()
        bg = QLabel(self)
        room = QPixmap("assets/room.png").scaled(w, h, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        bg.setPixmap(room)
        bg.setGeometry(0, 0, w, h)
        bg.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents) # Let clicks pass through
        bg.lower() # Send to back

        self.char_label = QLabel(self)
        pet = QPixmap(shared_state.shared.buddy)
        self.char_label.setPixmap(pet)
        self.char_label.move(int(screen_dim.width()/2.3),int(screen_dim.height()/2.3))
        self.char_label.raise_()


        self.icon = ClickableLabel(self)
        icon_bu = QPixmap("assets/egg.png").scaled(int(w * 0.1), int(h * 0.1),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.icon.setPixmap(icon_bu)
        self.icon.move(int(w/6),int(h-(h/5.2)))

        self.shop = ClickableLabel(self)
        shop_bu = QPixmap("assets/shop.png").scaled(int(w * 0.1), int(h * 0.1),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.shop.setPixmap(shop_bu)
        self.shop.move(int(w-w/4.5),int(h-(h/5.2)))

        self.email = ClickableLabel(self)
        email_bu = QPixmap("assets/email.png").scaled(int(w * 0.1), int(h * 0.1),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.email.setPixmap(email_bu)
        self.email.move(int(w/2 - email_bu.width()/2),int(h-(h/5.2)))

        self.icon.raise_()
        self.shop.raise_()
        self.email.raise_()

        # Connect button to emission function
        self.icon.clicked.connect(self.open_icon)
        self.shop.clicked.connect(self.open_shop)
        self.email.clicked.connect(self.open_todo)
        # --- FEED BUTTON ---
        self.feed_btn = QPushButton("Feed", self)
        self.feed_btn.clicked.connect(self.handle_feeding) # Connect to class method
        layout.addWidget(self.feed_btn) # ADDED TO LAYOUT

        self.food_label = QLabel(f"Food: {shared_state.shared.food}")
        layout.addWidget(self.food_label)

        # --- BARS ---
        self.hunger_bar = QProgressBar()
        self.hunger_bar.setFixedSize(150, 20)


        panel_layout.addWidget(self.feed_btn)
        panel_layout.addWidget(self.food_label)
        panel_layout.addWidget(QLabel("Hunger"))
        panel_layout.addWidget(self.hunger_bar)

        

        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(200)
        self.food_label.setText(f"Food: {shared_state.shared.food}")

    # Move logic OUT of __init__
    def handle_feeding(self):
        if shared_state.shared.food > 0:
            shared_state.shared.food -= 1
            # Increase hunger bar (assuming 100 is full)
            shared_state.shared.hunger = max(0, shared_state.shared.hunger - 30)
            self.food_label.setText(f"Food: {shared_state.shared.food}")
            print(f"Fed! Remaining food: {shared_state.shared.food}")
        else:
            self.show_warning("Not enough food!")

    def show_warning(self, text):
        self.invalid = QLabel(text, self)
        self.invalid.setStyleSheet("""
            background-color: rgba(255, 0, 0, 200); 
            color: white; padding: 5px; border-radius: 5px;
        """)
        self.invalid.adjustSize()
        self.invalid.move(70, 120) 
        self.invalid.show()
        QTimer.singleShot(2000, self.invalid.deleteLater)

    def update_ui(self):
        self.hunger_bar.setValue(shared_state.shared.hunger)
        self.food_label.setText(f"Food: {shared_state.shared.food}")
        
    def open_icon(self):
        print("Icon clicked in MainWindow")
        self.action_triggered.emit()
    def open_shop(self):
        print("Shop clicked in MainWindow")
        self.shop_clicked.emit()
    def open_todo(self):
        print("Todo clicked in MainWindow")
        self.todo_clicked.emit()


    def update_pet_display(self):
        new_pixmap = QPixmap(shared_state.shared.buddy).scaled(280, 280, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.char_label.setPixmap(new_pixmap)


if __name__ == "__main__":
    # This only runs if you play THIS file directly. 
    # It won't run when you import it into run.py.
    app = QApplication(sys.argv)
    window = StatsWindow()
    window.show()
    sys.exit(app.exec())
    #     self.hunger_bar = QProgressBar()
    #     self.hunger_bar.setStyleSheet("QProgressBar"
    #                       "{"
    #                       "background-color : rgba(0, 0, 0, 0);"
    #                       "border : 1px"
    #                       "}")
    #     self.happy_bar = QProgressBar()

    #     layout.addWidget(QLabel("Hunger"))
    #     layout.addWidget(self.hunger_bar)
    #     layout.addWidget(QLabel("Happiness"))
    #     layout.addWidget(self.happy_bar)

    #     self.setLayout(layout)
        

    #     # update timer for THIS window only
    #     self.timer = QTimer()
    #     self.timer.timeout.connect(self.update_ui)
    #     self.timer.start(200)

    # def update_ui(self):
    #     self.hunger_bar.setValue(shared_state.shared.hunger)
    #     self.happy_bar.setValue(shared_state.shared.happiness)