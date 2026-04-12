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

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
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
