import sys
import shared_state
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
)
import subprocess
from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            event.accept()
            self.clicked.emit()



app = QApplication(sys.argv)


class MainWindow(QWidget):
    action_triggered = pyqtSignal()
    shop_clicked = pyqtSignal()
    todo_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        print(shared_state.shared.buddy)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        w, h = 240, 280
        screen_dim = app.primaryScreen().availableGeometry()
        # self.setFixedSize(w, h)

        # 1. Background sky
        bg = QLabel(self)
        sky = QPixmap("assets/sky.png").scaled(int(w * 0.7), int(h * 0.7), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        bg.setPixmap(sky)
        bg.move(int(w / 2 - sky.width() / 2), int(h / 2 - sky.height() / 2))

        # 2. Character
        self.char_label = QLabel(self)
        pet = QPixmap(shared_state.shared.buddy).scaled(int(w/5), int(h/5), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.char_label.setPixmap(pet)
        self.char_label.move(int(w/4), int(h/3))

        # 3. Egg Shell (FIXED: Added Mouse Transparency)
        egg = QLabel(self)
        shell = QPixmap("assets/bigegg.png").scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        egg.setPixmap(shell)
        # This makes the egg image "invisible" to the mouse so buttons underneath work
        egg.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # 4. Navigation Buttons
        self.home = ClickableLabel(self)
        home_bu = QPixmap("assets/home_button_icon.png").scaled(int(w * 0.15), int(h * 0.15),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.home.setPixmap(home_bu)
        self.home.move(int(w/4),int(h-(h/4.8)))

        self.shop = ClickableLabel(self)
        shop_bu = QPixmap("assets/shop.png").scaled(int(w * 0.15), int(h * 0.15),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.shop.setPixmap(shop_bu)
        self.shop.move(int(w-w/2.5),int(h-(h/4.8)))

        self.email = ClickableLabel(self)
        email_bu = QPixmap("assets/email.png").scaled(int(w * 0.15), int(h * 0.15),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.email.setPixmap(email_bu)
        self.email.move(int(w/2 - email_bu.width()/2),int(h-(h/4.8)))

        # Connect button to emission function
        self.home.clicked.connect(self.open_home)
        self.shop.clicked.connect(self.open_shop)
        self.email.clicked.connect(self.open_todo)
    
    def update_pet_display(self):
        new_pixmap = QPixmap(shared_state.shared.buddy)
        self.char_label.setPixmap(new_pixmap)

    def open_home(self):
        print("Home clicked in MainWindow")
        self.action_triggered.emit()
    def open_shop(self):
        print("Shop clicked in MainWindow")
        self.shop_clicked.emit()
    def open_todo(self):
        print("Todo clicked in MainWindow")
        self.todo_clicked.emit()

# --- PROTECTED EXECUTION BLOCK ---
if __name__ == "__main__":
    # This only runs if you play THIS file directly. 
    # It won't run when you import it into run.py.
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
