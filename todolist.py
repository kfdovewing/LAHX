#use light mode!
import sys
import shared_state
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget,
    QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt


class TodoList(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List")
        self.setFixedSize(350, 500)

        self.tasks = []

        self.setup_ui()

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
        self.list_widget.setStyleSheet("""
            background: white;
            border: none;
            font-size: 14px;
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

    def refresh_list(self):
        self.list_widget.clear()

        for task in self.tasks:
            text = task["task"]

            # no checkbox anymore → use visual prefix + strikethrough effect
            if task["done"]:
                text = "✔ " + text
                item = QListWidgetItem(text)
                font = item.font()
                font.setStrikeOut(True)
                item.setFont(font)
                item.setForeground(Qt.GlobalColor.darkGray)
            else:
                text = "○ " + text
                item = QListWidgetItem(text)

            self.list_widget.addItem(item)

    def add_task(self):
        text = self.task_entry.text().strip()
        if not text:
            return

        self.tasks.append({"task": text, "done": False})
        self.task_entry.clear()
        self.refresh_list()

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
        self.tasks[i]["done"] = True
        self.refresh_list()
        shared_state.money += 2

    def delete_task(self):
        i = self.get_selected_index()
        if i is None:
            return

        if self.tasks[i]["done"]:
            self.tasks.pop(i)
            self.refresh_list()
        else:
            reply = QMessageBox.question(
                self,
                "Delete",
                "Delete this task? You won't get any money.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.tasks.pop(i)
                self.refresh_list()

    def clear_all(self):
        reply = QMessageBox.question(
            self,
            "Clear",
            "Delete all tasks? You'll only get money for the tasks you completed",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            completed = int(sum(1 for t in self.tasks if t["done"]))
            not_completed = len(self.tasks) - completed
            shared_state.money += completed
            print(shared_state.money)
            self.tasks.clear()
            self.refresh_list()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoList()
    window.show()
    sys.exit(app.exec())