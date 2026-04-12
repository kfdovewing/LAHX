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



app = QApplication(sys.argv)

class start(QWidget):
    select = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)

        def open_file():
            self.select.emit()

        w = 400
        h = 400

        centerx = int(w/2)
        centery = int(h/2)
        # self.resize(w,h)
        bg = QLabel(self)
        egg_bg = QPixmap("assets/eggselectionbg.png").scaled(w,h,Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        bg.setPixmap(egg_bg)


        cat_egg = QPixmap("assets/buddy_eggs/categg.png")
        frog_egg = QPixmap("assets/buddy_eggs/frogegg.png")
        hat_egg = QPixmap("assets/buddy_eggs/hategg.png")
        party_egg = QPixmap("assets/buddy_eggs/sharkegg.png")

        self.egg1 = ClickableLabel(self)
        self.egg1.setPixmap(cat_egg)
        self.egg1.clicked.connect(lambda: shared_state.shared.cat())
        self.egg1.clicked.connect(open_file)

        self.egg2 = ClickableLabel(self)
        self.egg2.setPixmap(frog_egg)
        self.egg2.move(int(w-frog_egg.width()),0)
        self.egg2.clicked.connect(lambda: shared_state.shared.frog())
        self.egg2.clicked.connect(open_file)

        self.egg3 = ClickableLabel(self)
        self.egg3.setPixmap(hat_egg)
        self.egg3.move(0,centery)
        self.egg3.clicked.connect(lambda: shared_state.shared.hat())
        self.egg3.clicked.connect(open_file)

        self.egg4 = ClickableLabel(self)
        self.egg4.setPixmap(party_egg)
        self.egg4.move(int(w-party_egg.width()),centery)
        self.egg4.clicked.connect(lambda: shared_state.shared.party())
        self.egg4.clicked.connect(open_file)

        
        

if __name__ == "__main__":
    # This only runs if you play THIS file directly. 
    # It won't run when you import it into run.py.
    app = QApplication(sys.argv)
    window = start()
    window.show()
    sys.exit(app.exec())