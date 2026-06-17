import sys
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QVBoxLayout, QHBoxLayout,QMainWindow
from PyQt6.QtCore import QTimer, pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
import shared_state

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            event.accept()
            self.clicked.emit()


class ShopPage(QWidget):
    action_triggered = pyqtSignal()
    icon_clicked = pyqtSignal()
    todo_clicked = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("color: #000000")
        # ---------------- BACKGROUND ----------------
        
        bg = QLabel(self)
        bg_pix = QPixmap("shopbg.jpg")
        # bg_pix = QPixmap("shopbg.jpg").scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        # self.resize(bg_pix.width(), bg_pix.height())
        bg.setPixmap(bg_pix)
        # bg.setGeometry(0,0, self.width(), self.height())
        bg.lower()
        bg.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        

        #sets item layout
        # self.setFixedSize(bg_pix.size())
        grid = QVBoxLayout()
        self.setLayout(grid)

        w=self.width()
        h=self.height()

        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        # self.back_btn = QPushButton(self)
        # self.back_btn.setText("Back")
        # self.back_btn.clicked.connect(self.back_requested.emit)
        # grid.addWidget(self.back_btn, 0, 2)
        
        # sky = QLabel(self)
        # sky_pix = QPixmap("assets/sky_long.png")
        # sky.setPixmap(sky_pix)
        # sky.resize(400,700)
        # sky.lower()
        # sky.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)


        
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addSpacing(20)


        self.icon = ClickableLabel(self)
        icon_bu = QPixmap("assets/egg.png").scaled(int(w * 0.1), int(h * 0.1),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.icon.setPixmap(icon_bu)
        hbox.addWidget(self.icon)


        self.home = ClickableLabel(self)
        home_bu = QPixmap("assets/home_button_icon.png").scaled(int(w * 0.1), int(h * 0.1),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.home.setPixmap(home_bu)
        hbox.addWidget(self.home)

        self.email = ClickableLabel(self)
        email_bu = QPixmap("assets/email.png").scaled(int(w * 0.1), int(h * 0.1),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.email.setPixmap(email_bu)
        hbox.addWidget(self.email)

        
        # Connect button to emission function
        self.home.clicked.connect(self.open_home)
        self.icon.clicked.connect(self.open_icon)
        self.email.clicked.connect(self.open_todo)

   


        # ---------------- UI LABELS ----------------
        self.funds = QLabel(f"funds: ${shared_state.shared.money}")
        self.display_food = QLabel(f"food: {shared_state.shared.food}")

        grid.addWidget(self.funds)
        grid.addWidget(self.display_food)

        # ---------------- ITEMS ----------------
        self.items = {
            "free gift": 0,
            "food": 15,
            "clown nose": 35,
            "party hat": 50
        }

        for i, key in enumerate(self.items):

            btn = QPushButton(f"{key}: ${self.items[key]}")
            btn.setStyleSheet("background-color: #8490a3; color: #000000")
            btn.clicked.connect(lambda _, k=key, b=btn: self.buy(k, b))
            grid.addWidget(btn)
        grid.setContentsMargins(20,20,20,20) 

        # ... (your icon setups) ...

        
        # CRITICAL: Bring them to the very front
        self.icon.raise_()
        self.home.raise_()
        self.email.raise_()
        grid.addLayout(hbox)
        # container = QWidget()
        # container.setLayout(grid)
        # self.setCentralWidget(container)

    def open_home(self):
        print("Home clicked in MainWindow")
        self.action_triggered.emit()
    def open_icon(self):
        print("Shop clicked in MainWindow")
        self.icon_clicked.emit()
    def open_todo(self):
        print("Todo clicked in MainWindow")
        self.todo_clicked.emit()
    # ---------------- BUY LOGIC ----------------
    def show_warning(self, text):
        self.invalid = QLabel(text, self)
        self.invalid.setStyleSheet("""
            background-color: rgba(255, 0, 0, 200); 
            color: white; padding: 5px; border-radius: 5px;
        """)
        self.invalid.adjustSize()
        self.invalid.move(70, 120) 
        self.invalid.raise_()
        self.invalid.show()
        QTimer.singleShot(2000, self.invalid.deleteLater)
    def buy(self, item, btn):
        cost = self.items[item]

        if shared_state.shared.money < cost:
            self.show_warning("Not enough money")
            return

        shared_state.shared.money -= cost

        if item == "food":
            shared_state.shared.food += 1
            self.display_food.setText(f"food: {shared_state.shared.food}")

        self.funds.setText(f"funds: ${shared_state.shared.money}")
        btn.setText("SOLD OUT")
        btn.setEnabled(False)
    def refresh_ui(self):
        # Update the labels with the CURRENT values from shared_state
        self.funds.setText(f"funds: ${shared_state.shared.money}")
        self.display_food.setText(f"food: {shared_state.shared.food}")
        print(f"Shop UI Refreshed: Money is {shared_state.shared.money}")
    
    



    # --- PROTECTED EXECUTION BLOCK ---
if __name__ == "__main__":
    # This only runs if you play THIS file directly. 
    # It won't run when you import it into run.py.
    app = QApplication(sys.argv)
    window = ShopPage()
    window.show()
    sys.exit(app.exec())

