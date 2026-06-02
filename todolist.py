#use light mode!
import sys
import shared_state
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget,
    QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap, QKeyEvent


class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            event.accept()
            self.clicked.emit()
        

class TodoList(QWidget):
    icon_clicked = pyqtSignal()
    shop_clicked = pyqtSignal()
    action_triggered = pyqtSignal()
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("To-Do List")
        self.money = 0
        self.tasks = []

        w = 350
        h = 500 

        self.setup_ui()

        self.icon = ClickableLabel(self)
        icon_bu = QPixmap("assets/egg.png").scaled(int(w * 0.1), int(h * 0.1),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.icon.setPixmap(icon_bu)
        self.icon.move(5,0)

        self.shop = ClickableLabel(self)
        shop_bu = QPixmap("assets/shop.png").scaled(int(w * 0.1), int(h * 0.1),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.shop.setPixmap(shop_bu)
        self.shop.move(int(shop_bu.width()*1.1+6),0)

        self.home = ClickableLabel(self)
        home_bu = QPixmap("assets/home_button_icon.png").scaled(int(w * 0.1), int(h * 0.1),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.home.setPixmap(home_bu)
        self.home.move(int(shop_bu.width()*2.2+6),0)

        # Connect button to emission function
        self.icon.clicked.connect(self.open_icon)
        self.shop.clicked.connect(self.open_shop)
        self.home.clicked.connect(self.open_home)
     

    #detects when certain keys pressed
    def keyPressEvent(self, event: QKeyEvent):
            if event.key() == Qt.Key.Key_Return: #adds tasks using 'enter' key
                event.accept()
                self.add_task()
            elif event.key() == Qt.Key.Key_Backspace or event.key() == Qt.Key.Key_Delete: #deletes tasks using 'delete' or 'backspace' key
                event.accept()
                self.delete_task()
            else:
                super().keyPressEvent(event)
        
    #switches screens
    def open_icon(self):
        print("Icon clicked in MainWindow")
        self.icon_clicked.emit()
    def open_shop(self):
        print("Shop clicked in MainWindow")
        self.shop_clicked.emit()
    def open_home(self):
        print("Todo clicked in MainWindow")
        self.action_triggered.emit()


    def setup_ui(self):
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("To-Do")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        main_layout.addWidget(title)

        # Input row
        input_layout = QHBoxLayout()

        self.task_entry = QLineEdit()
        self.task_entry.setPlaceholderText("Enter a task...")
        self.task_entry.setStyleSheet("""
            padding: 6px;
            border: 2px solid #bdc3c7;
            border-radius: 6px;
        """)

        add_btn = QPushButton("+")
        add_btn.setStyleSheet("""
            background-color: #3498db;
            color: white;
            font-weight: bold;
            padding: 6px 10px;
            border-radius: 6px;
        """)
        
       

        add_btn.clicked.connect(self.add_task)

        input_layout.addWidget(self.task_entry)
        input_layout.addWidget(add_btn)

        main_layout.addLayout(input_layout)

        # Task list
        self.list_widget = QListWidget()
        self.list_widget.itemChanged.connect(self.task_state_change)
        self.list_widget.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                padding: 5px;
            }
                                       
            QListWidget::item {
                color: #3c3f41;
                background-color: #ffffff;
                /*padding: 8px;
                margin: 4px 0px;*/
            }

            /* Hover state for items */
            QListWidget::item:hover {
                color: #a3a3a3;
            }

            /* Selected state (Active/Focused) */
            QListWidget::item:selected {
                background-color: #d1d1d1;
                color: #3c3f41;
                /*border: 1px solid #bfbfbf;   optional border for selection*/ 
            }
                                 
                                       
            QListWidget::indicator {
                width: 16px;
                height: 16px;
                image: url(assets/unchecked_box.png);
            }
            /*
            QListWidget::indicator:hover {
                border-color: #3498db;
                background-color: #ecf0f1;
            }
            */
            QListWidget::indicator:checked {
                image: url(assets/checked_box.png);
            }
        """)
        main_layout.addWidget(self.list_widget)

        # Buttons
        btn_layout = QHBoxLayout()

        done_btn = QPushButton("Done")
        delete_btn = QPushButton("Delete")
        clear_btn = QPushButton("Clear")

        for btn, color in [
            (done_btn, "#2ecc71"),
            (delete_btn, "#e74c3c"),
            (clear_btn, "#7f8c8d")
        ]:
            btn.setStyleSheet(f"""
                background-color: {color};
                color: white;
                font-weight: bold;
                padding: 6px;
                border-radius: 6px;
            """)

        done_btn.clicked.connect(self.mark_done)
        delete_btn.clicked.connect(self.delete_task)
        clear_btn.clicked.connect(self.clear_all)

        btn_layout.addWidget(done_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(clear_btn)

        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    

    def task_state_change(self, item):
        font = item.font()
        
        if item.checkState() == Qt.CheckState.Checked:
            font.setStrikeOut(True)
            if item in self.tasks:
                shared_state.shared.money += 5
                self.tasks.remove(item)
                print(shared_state.shared.money)
        else:
            font.setStrikeOut(False)
        
        item.setFont(font)

    def add_task(self, info = ""):
        text = self.task_entry.text().strip()
        if info:
            text = info
        if not text:
            return

        item = QListWidgetItem(text)
        self.tasks.append(item)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(Qt.CheckState.Unchecked)
        self.list_widget.addItem(item)
        self.task_entry.clear()


    def get_selected_index(self):
        row = self.list_widget.currentRow()
        if row == -1:
            QMessageBox.information(self, "Select Task", "Pick a task first.")
            return None
        return row


    def mark_done(self):
        i = self.get_selected_index()
        if i is None:
            return
        item = self.list_widget.item(i)
        item.setCheckState(Qt.CheckState.Checked)


    def delete_task(self):
        i = self.get_selected_index()
        if i is None:
            return

        item = self.list_widget.item(i)
        if item.checkState() == Qt.CheckState.Checked:
            reply = QMessageBox.question(
                self,
                "Delete",
                "Delete this task?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                if item in self.tasks:
                    self.tasks.remove(item)
                self.list_widget.takeItem(i)
                del item
        else:
            reply = QMessageBox.question(
                self,
                "Delete",
                "Delete this task? You won't get any money.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                if item in self.tasks:
                    self.tasks.remove(item)
                self.list_widget.takeItem(i)
                del item

    def clear_all(self):
        reply = QMessageBox.question(
            self,
            "Clear",
            "Delete all tasks? You will not get money for the tasks you did not complete.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            completed = int(sum(1 for t in self.tasks if t["done"]))
            not_completed = len(self.tasks) - completed
            print(shared_state.shared.money)
            self.tasks.clear()
            self.refresh_list()


#fdksjfldsa