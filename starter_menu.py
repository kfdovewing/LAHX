import sys
import subprocess
import shared_state
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
)


class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

def open_file():
    subprocess.Popen([sys.executable, "graphic_icon.py"])


w = 400
h = 400

centerx = int(w/2)
centery = int(h/2)
app = QApplication(sys.argv)
window = QWidget()
window.resize(w,h)

cat_egg = QPixmap("assets/buddy_eggs/categg.png")
frog_egg = QPixmap("assets/buddy_eggs/frogegg.png")
hat_egg = QPixmap("assets/buddy_eggs/hategg.png")
party_egg = QPixmap("assets/buddy_eggs/sharkegg.png")

egg1 = ClickableLabel(window)
egg1.setPixmap(cat_egg)
egg1.clicked.connect(lambda: shared_state.cat())
egg1.clicked.connect(open_file)

egg2 = ClickableLabel(window)
egg2.setPixmap(frog_egg)
egg2.move(int(w-frog_egg.width()),0)
egg2.clicked.connect(lambda: shared_state.frog())
egg2.clicked.connect(open_file)

egg3 = ClickableLabel(window)
egg3.setPixmap(hat_egg)
egg3.move(0,centery)
egg3.clicked.connect(lambda: shared_state.hat())
egg3.clicked.connect(open_file)

egg4 = ClickableLabel(window)
egg4.setPixmap(party_egg)
egg4.move(int(w-party_egg.width()),centery)
egg4.clicked.connect(lambda: shared_state.party())
egg4.clicked.connect(open_file)



window.show()

sys.exit(app.exec())