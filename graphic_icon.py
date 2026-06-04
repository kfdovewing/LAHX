import sys
import shared_state
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QGridLayout,
    QVBoxLayout, 
    QHBoxLayout,
    QSizePolicy
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
        #self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        w, h = 240, 280
        # screen_dim = app.primaryScreen().availableGeometry()
        self.resize(w, h)

        layout = QGridLayout(self)

        # 1. Background sky
        bg_image = QPixmap("assets/sky.png")
        self.bg = QLabel(self)
        self.bg.setPixmap(bg_image)
        self.bg.setScaledContents(True)
        self.bg.setFixedSize(150, 140)

        # 2. Character
        pet = QPixmap(shared_state.shared.buddy)
        self.buddy = QLabel(self)
        self.buddy.setPixmap(pet)
        self.buddy.setScaledContents(True)

        # 3. Egg Shell (FIXED: Added Mouse Transparency)
        shell = QPixmap("assets/bigegg.png")
        self.egg = QLabel(self)
        self.egg.setPixmap(shell)
        # This makes the egg image "invisible" to the mouse so buttons underneath work
        self.egg.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.egg.setScaledContents(True)
        self.egg.resize(w,h)

        

        overlay_widget = QWidget()
        # overlay_widget.setStyleSheet("background-color: lightblue; border: 1px solid blue;")
        overlay_btns_layout = QHBoxLayout()
        overlay_btns_layout.setContentsMargins(52, 2, 52, 10) #decreases margins pushing the buttons/elements closer together 

        buttons = []

        task_image = QPixmap("assets/email.png")
        self.task_btn = ClickableLabel(self)
        self.task_btn.setPixmap(task_image)
        buttons.append(self.task_btn)
        
        shop_btn = QPixmap("assets/shop.png")
        self.shop = ClickableLabel(self)
        self.shop.setPixmap(shop_btn)
        buttons.append(self.shop)

        home_btn = QPixmap("assets/home_button_icon.png")
        self.home = ClickableLabel(self)
        self.home.setPixmap(home_btn)
        buttons.append(self.home)

        for btn in buttons:
            btn.setScaledContents(True)
            btn.setFixedSize(32,32)
            btn.setStyleSheet("border: none; background: transparent;")

            overlay_btns_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignTop)

        pos_cut_for_btns = 5 #the divide value/cut for the position of the buttons veritcally
        overlay_widget.setLayout(overlay_btns_layout)
        overlay_widget.setFixedHeight(int(h/pos_cut_for_btns))

        layout.addWidget(self.bg, 0, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.buddy, 0, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.egg, 0, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(overlay_widget, 0, 0, Qt.AlignmentFlag.AlignBottom)


        # 4. Navigation Buttons
        # self.home = ClickableLabel(self)
        # home_bu = QPixmap("assets/home_button_icon.png").scaled(int(w * 0.15), int(h * 0.15),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        # self.home.setPixmap(home_bu)
        # self.home.move(int(w/4),int(h-(h/4.8)))

        # self.shop = ClickableLabel(self)
        # shop_bu = QPixmap("assets/shop.png").scaled(int(w * 0.15), int(h * 0.15),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        # self.shop.setPixmap(shop_bu)
        # self.shop.move(int(w-w/2.5),int(h-(h/4.8)))

        # self.email = ClickableLabel(self)
        # email_bu = QPixmap("assets/email.png").scaled(int(w * 0.15), int(h * 0.15),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        # self.email.setPixmap(email_bu)
        # self.email.move(int(w/2 - email_bu.width()/2),int(h-(h/4.8)))

        # Connect button to emission function
        self.home.clicked.connect(self.open_home)
        self.shop.clicked.connect(self.open_shop)
        self.task_btn.clicked.connect(self.open_todo)
    
    def update_pet_display(self):
        new_pixmap = QPixmap(shared_state.shared.buddy)
        self.buddy.setPixmap(new_pixmap)


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
