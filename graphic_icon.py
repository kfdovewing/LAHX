import sys
import shared_state
from pathlib import Path
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
screen_dim = app.primaryScreen().availableGeometry()

w = 240
h = 280
window = QWidget()
window.resize(w,h)
window.move(screen_dim.right()-w,screen_dim.top())
bg = QLabel(window)
sky = QPixmap("assets/sky.png").scaled(int(w*0.7),int(h*0.7),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
bg.setPixmap(sky)
bg.move(int(w/2-sky.width()/2),int(h/2-sky.height()/2))

char = QLabel(window)
buddy = QPixmap(shared_state.buddy).scaled(int(w*0.45),int(h*0.45),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
char.setPixmap(buddy)

centerx = int(w/2)
centery = int(h/2)
char.move(int(centerx-buddy.width()/2),int(centery-buddy.height()/2))

egg = QLabel(window)
shell = QPixmap("assets/bigegg.png").scaled(w,h,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
egg.setPixmap(shell)


home = ClickableLabel(window)
home_bu = QPixmap("assets/home_button_icon.png").scaled(int(w*0.15),int(h*0.15),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
home.setPixmap(home_bu)
home.move(int(w/4),int(h-(h/4.8)))

email = ClickableLabel(window)
email_bu = QPixmap("assets/email.png").scaled(int(w*0.15),int(h*0.15),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
email.setPixmap(email_bu)
email.move(int(w/2 - email_bu.width()/2),int(h-(h/4.8)))

shop = ClickableLabel(window)
shop_bu = QPixmap("assets/shop.png").scaled(int(w*0.15),int(h*0.15),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
shop.setPixmap(shop_bu)
shop.move(int(w-w/2.5),int(h-(h/4.8)))

def open_file():
    subprocess.Popen([sys.executable, "todolist.py"])

home.clicked.connect(lambda: print("home"))
email.clicked.connect(lambda: print("email"))
shop.clicked.connect(lambda: print("shop"))
# Transparent window
window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
email.clicked.connect(open_file)
# # Transparent window
# window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

# # Remove title bar
# window.setWindowFlags(
#     Qt.WindowType.FramelessWindowHint|
#     Qt.WindowType.WindowStaysOnTopHint
# )
window.show()

sys.exit(app.exec())
        else:
            event.ignore()

class MainWindow(QWidget):
    action_triggered = pyqtSignal()
    shop_clicked = pyqtSignal()
    todo_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        w, h = 240, 280
        self.setFixedSize(w, h)

        # 1. Background sky
        bg = QLabel(self)
        sky = QPixmap("assets/sky.png").scaled(int(w * 0.7), int(h * 0.7), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        bg.setPixmap(sky)
        bg.move(int(w / 2 - sky.width() / 2), int(h / 2 - sky.height() / 2))

        # 2. Character
        char = QLabel(self)
        party = QPixmap("assets/party_guy.png").scaled(int(w * 0.5), int(h * 0.5), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        char.setPixmap(party)
        centerx = int(w / 2 - party.width() / 2)
        char.move(centerx, int(h / 2 - party.height() / 2.5))

        # 3. Egg Shell (FIXED: Added Mouse Transparency)
        egg = QLabel(self)
        shell = QPixmap("assets/egg2.png").scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        egg.setPixmap(shell)
        # This makes the egg image "invisible" to the mouse so buttons underneath work
        egg.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # 4. Navigation Buttons
        self.home = ClickableLabel(self)
        home_bu = QPixmap("assets/home_button_icon.png").scaled(int(w * 0.1), int(h * 0.1))
        self.home.setPixmap(home_bu)
        self.home.move(centerx, int(h - (h / 6)))

        self.shop = ClickableLabel(self)
        shop_bu = QPixmap("assets/shop.png").scaled(int(w * 0.1), int(h * 0.1))
        self.shop.setPixmap(shop_bu)
        self.shop.move(int(w/2+shop_bu.width()*1.5),int(h-(h/6)))

        self.email = ClickableLabel(self)
        email_bu = QPixmap("assets/email.png").scaled(int(w * 0.1), int(h * 0.1))
        self.email.setPixmap(email_bu)
        self.email.move(int(w/2 - email_bu.width()/2.5),int(h-(h/6)))

        # Connect button to emission function
        self.home.clicked.connect(self.open_home)
        self.shop.clicked.connect(self.open_shop)
        self.email.clicked.connect(self.open_todo)

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
