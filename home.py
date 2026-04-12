import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QApplication
from PyQt6.QtCore import QTimer, pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
import shared_state

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            event.accept()
            self.clicked.emit()

app = QApplication(sys.argv)

class StatsWindow(QWidget):
    shop_clicked = pyqtSignal()
    todo_clicked = pyqtSignal()
    action_triggered = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Stats")
        layout = QVBoxLayout()
        screen_dim = app.primaryScreen().availableGeometry()

        # self.resize(screen_dim.width(), screen_dim.height())
        w = screen_dim.width()
        h = screen_dim.height()
        bg = QLabel(self)
        room = QPixmap("assets/room.png").scaled(screen_dim.width(),screen_dim.height(),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        bg.setPixmap(room)
        bg.move(0,35)

        self.char_label = QLabel(self)
        pet = QPixmap(shared_state.shared.buddy)
        self.char_label.setPixmap(pet)
        self.char_label.move(int(screen_dim.width()/2.3),int(screen_dim.height()/2.3))


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

        # Connect button to emission function
        self.icon.clicked.connect(self.open_icon)
        self.shop.clicked.connect(self.open_shop)
        self.email.clicked.connect(self.open_todo)
        
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
    window = MainWindow()
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