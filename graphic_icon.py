import sys
from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            event.accept()
            self.clicked.emit()
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