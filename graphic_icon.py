import sys
import shared_state
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QPoint, QEvent
from PyQt6.QtWidgets import (
    QApplication, QLabel, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QSizePolicy, QPushButton, QSpacerItem
)
import subprocess


class ClickableLabel(QLabel):
        
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            event.accept()
            self.clicked.emit()





class MainWindow(QWidget):
    action_triggered = pyqtSignal()
    shop_clicked = pyqtSignal()
    todo_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setStyleSheet("background-color: lightblue; border: 1px solid blue;")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        w, h = 404, 408
        # screen_dim = app.primaryScreen().availableGeometry()
        self.setFixedSize(w, h)
        

        layout = QGridLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
        # 1. Background sky
        bg_image = QPixmap("assets/LunchBox.png")
        # print(bg_image.size())
        self.bg = QLabel(self)
        self.bg.setPixmap(bg_image)
        # self.bg.setFixedSize(int(bg_image.width()*0.8),int(bg_image.height()*0.8))
        # self.bg.setScaledContents(True)


        # 2. Character
        pet = QPixmap(shared_state.shared.buddy)
        self.buddy = QLabel(self)
        self.buddy.setPixmap(pet)
        # self.buddy.setScaledContents(True)


        self.lunch_box_container = QWidget()
        self.box_layout = QVBoxLayout(self.lunch_box_container)
        self.box_layout.setContentsMargins(0, 0, 0, 0)
        
        self.top_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Ignored)
        self.box_layout.addSpacerItem(self.top_spacer)

        self.open_cover = QPixmap("assets/LunchBox_Open_Cover.png")
        self.closed_cover = QPixmap("assets/LunchBox_Cover.png")

        self.box_cover = QPushButton()
        self.box_cover.setCheckable(True)
        self.box_cover.setStyleSheet("border: none; background: transparent;")
        
        self.box_layout.addWidget(self.box_cover)

        self.bottom_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Ignored)
        self.box_layout.addSpacerItem(self.bottom_spacer)

        self.toggle_cover()
        self.box_cover.clicked.connect(self.toggle_cover)


        overlay_widget = QWidget()
        # overlay_widget.setStyleSheet("background-color: lightblue; border: 1px solid blue;")
        overlay_btns_layout = QHBoxLayout(overlay_widget)
        overlay_btns_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        overlay_btns_layout.setContentsMargins(10, 2, 10, 20) #decreases margins pushing the buttons/elements closer together 
        overlay_btns_layout.setSpacing(3)
        
        buttons = []

        
        self.task_btn = ClickableLabel(self)
        task_image = QPixmap("assets/email.png")
        # task_image = QPixmap("assets/email.png").scaled(self.task_btn.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.task_btn.setPixmap(task_image)
        buttons.append(self.task_btn)
        
        
        self.shop = ClickableLabel(self)
        shop_btn = QPixmap("assets/shop.png")
        # shop_btn = QPixmap("assets/shop.png").scaled(self.shop.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.shop.setPixmap(shop_btn)
        buttons.append(self.shop)

        
        self.home = ClickableLabel(self)
        home_btn = QPixmap("assets/home_button_icon.png")
        # home_btn = QPixmap("assets/home_button_icon.png").scaled(self.home.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.home.setPixmap(home_btn)
        buttons.append(self.home)
        
        for btn in buttons:
            # btn.setMinimumSize(QSize(32,32))
            # btn.setMaximumSize(QSize(128,128))
            btn.setFixedSize(QSize(32,32))
            btn.setScaledContents(True)
            btn.setStyleSheet("border: none; background: transparent;")
            overlay_btns_layout.addWidget(btn)
            # btn.setScaledContents(True)



        layout.addWidget(self.bg, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.buddy, 0, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(overlay_widget, 0, 0)
        layout.addWidget(self.lunch_box_container, 0, 0, Qt.AlignmentFlag.AlignCenter)
        


        # Connect button to emission function
        self.home.clicked.connect(self.open_home)
        self.shop.clicked.connect(self.open_shop)
        self.task_btn.clicked.connect(self.open_todo)

    
    def update_pet_display(self):
        new_pixmap = QPixmap(shared_state.shared.buddy)
        self.buddy.setPixmap(new_pixmap)

    
    def toggle_cover(self):
        current_pixmap = self.open_cover if self.box_cover.isChecked() else self.closed_cover
        # Apply the image as an Icon
        self.box_cover.setIcon(QIcon(current_pixmap))
        self.box_cover.setIconSize(current_pixmap.size())
        self.box_cover.setFixedSize(current_pixmap.size())
        # self.box_cover.setIconSize(QSize(int(current_pixmap.width()*0.8),int(current_pixmap.height()*0.8)))
        # self.box_cover.setFixedSize(int(current_pixmap.width()*0.8),int(current_pixmap.height()*0.8))

        if self.box_cover.isChecked():
            self.top_spacer.changeSize(0, 500, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
            self.bottom_spacer.changeSize(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Ignored)
        else:
            self.top_spacer.changeSize(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Ignored)
            self.bottom_spacer.changeSize(0, 38, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)


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
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
