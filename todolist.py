#use light mode!
import sys
import shared_state
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget,
    QListWidgetItem, QMessageBox, QCheckBox, QSizePolicy, QScrollArea, QStackedWidget
)
from PyQt6.QtCore import pyqtSignal, Qt, QRect, QSize
from PyQt6.QtGui import QPixmap, QKeyEvent, QFontMetrics



class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            event.accept()
            self.clicked.emit()
        


class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        # Keep layout direction standard (Left to Right) so text behaves normally
        self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.setStyleSheet("""
             QListWidget {
                 font-size: 15px;
                 padding: 5px;
             }
                                       
             QListWidget::item {
                 color: #3c3f41;
                 background-color: #ffffff;
                 padding: 8px;
                 /*margin: 4px 0px;*/
                 border-bottom: 1px solid #eee;
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
                                       
             QCheckBox::indicator {
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
             QCheckBox::indicator:checked {
                 image: url(assets/checked_box.png);
             }
         """)
        


    def get_handle_rect(self, item):
        """Calculates the handle rectangle on the right side using standard LTR coordinate space."""
        item_rect = self.visualItemRect(item)
        if item_rect.isEmpty():
            return QRect()
        
        icon_width =  24+5  # Icon size + padding
        
        # Calculate X position sitting right against the inner right margin
        #  "-5" is to get the handle box off the edge of the task wall
        handle_x = item_rect.x() + item_rect.width() - icon_width -5
        
        return QRect(handle_x, item_rect.y(), icon_width, item_rect.height())


    def mousePressEvent(self, event):
        item = self.itemAt(event.position().toPoint())
        if item:

            handle_rect = self.get_handle_rect(item)
            
            # Check if click coordinates fall inside the right handle box
            if not handle_rect.contains(event.position().toPoint()):
                item.setData(Qt.ItemDataRole.UserRole, False)   # Clicked the text
                
                if item.isSelected():
                    event.accept()
                    self.clearSelection()
                    return
            
            else:
                item.setData(Qt.ItemDataRole.UserRole, True)  # Clicked the Handle


        if not item:
            # Clicked on empty background space -> drop all selections
            self.clearSelection()
        
                
        super().mousePressEvent(event)


    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item and item.data(Qt.ItemDataRole.UserRole) is True:
            super().startDrag(supportedActions)

    


class CreateTaskWiget(QWidget):
    def __init__(self, current_page, text, own):
        super().__init__()        
        self.current_page = current_page
        task_layout = QHBoxLayout(self)
        task_layout.setSpacing(5)
        task_layout.setContentsMargins(5, 0, 0, 0)


        # 1. Create a QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 0px;
                background: transparent;
                margin: 2px;
            }
            QScrollArea > QWidget > QWidget {
                border: none;
                background: transparent;
            }
            /* Completely hide the horizontal scrollbar track, buttons, and handles */
            QScrollBar:horizontal {
                height: 0px;
                background: transparent;
            }
            QScrollBar::handle:horizontal, 
            QScrollBar::add-line:horizontal, 
            QScrollBar::sub-line:horizontal {
                background: none;
                width: 0px;
            }
        """)
        
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    
        self.task_text = text
        self.text_label = QLabel(f" {self.task_text} ")
        self.text_font = self.text_label.font()
        self.text_font.setPointSize(15)
        self.text_label.setFont(self.text_font)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        if own:
            self.text_label.setStyleSheet("color: #3B5DF7;")


        scroll_area.setWidget(self.text_label)


        self.time_label = QLabel("11:00 PM")
        self.time_label.setStyleSheet("""
            color: #000000;
            font-size: 14px;
            border: 0px;
            padding: 0px;
        """)

        self.task_checkbox = QCheckBox()
        self.task_checkbox.setStyleSheet("""
            color: #000000;
            border: 0px;
            padding: 0px;
        """)
        self.task_checkbox.stateChanged.connect(
            lambda state: self.current_page.task_state_change(self, self.text_label, state)
        )

        icon_label = QLabel()
        icon_label.setPixmap(QPixmap("assets/grab_handle.png").scaled(24, 24))
        icon_label.setScaledContents(True)
        icon_label.setFixedSize(20, 20)
        
        
        task_layout.addWidget(self.task_checkbox, alignment=Qt.AlignmentFlag.AlignVCenter)
        task_layout.addWidget(scroll_area, alignment=Qt.AlignmentFlag.AlignVCenter)
        task_layout.addStretch() # Pushes the icon all the way to the right side
        task_layout.addWidget(self.time_label, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        task_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)




class CreatePage(QWidget):
    def __init__(self, page_name, parent):
        super().__init__(parent)
        self.stack = parent

        self.tasks = []
        self.not_earnable_tasks = []
        

        w = 350
        h = 500 

        
        #change value based on page user last on

        self.setup_ui(page_name)

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



    def setup_ui(self, page_name):
        main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        #travel buttons layout on left of header
        travel_btn_layout = QHBoxLayout()
        travel_btn_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        travel_btn_layout.setSpacing(4)

        buttons = []

        icon_btn = QPixmap("assets/egg.png")
        self.icon = ClickableLabel(self)
        self.icon.setPixmap(icon_btn)
        buttons.append(self.icon)
        
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
            btn.setFixedSize(35,35)
            btn.setStyleSheet("border: none; background: transparent;")

            travel_btn_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignLeft)
        

        #middle of header layout for text and more
        middle_header_items = QHBoxLayout()
        middle_header_items.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel(f"To-Do: {page_name}")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")

        middle_header_items.addWidget(self.title)


        #layout for variables on right side of header
        vars_header_items = QHBoxLayout()
        vars_header_items.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.wallet = QLabel(f"Money: ${shared_state.shared.money}")
        self.wallet.setStyleSheet("font-size: 13px; color: #050505;")        

        vars_header_items.addWidget(self.wallet, alignment=Qt.AlignmentFlag.AlignBaseline)


        #adding the sublayouts to the header
        header_layout.addLayout(travel_btn_layout, stretch=1)
        header_layout.addLayout(middle_header_items, stretch=1)
        header_layout.addLayout(vars_header_items, stretch=1)
        
        main_layout.addLayout(header_layout)

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
        self.list_widget = CustomListWidget()
        main_layout.addWidget(self.list_widget)

        # Buttons
        btn_layout = QHBoxLayout()

        back_arrow = QPushButton("<")
        forward_arrow = QPushButton(">")
        clear_btn = QPushButton("Clear")

        for btn, color in [
            (back_arrow, "#707070"),
            (forward_arrow, "#707070"),
            (clear_btn, "#4a85bd")
        ]:
            btn.setStyleSheet(f"""
                background-color: {color};
                color: white;
                font-weight: bold;
                padding: 6px;
                border-radius: 6px;
            """)

        clear_btn.clicked.connect(self.clear_all)
        back_arrow.clicked.connect(lambda: self.stack.page_back())
        forward_arrow.clicked.connect(lambda: self.stack.page_forward())

        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch(1)
        btn_layout.addWidget(back_arrow)
        btn_layout.addWidget(forward_arrow)

        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)




    def task_state_change(self, item, text, state):
        font = text.font()
        
        if state == 2: #item checked
            font.setStrikeOut(True)

            if item not in self.not_earnable_tasks:
                shared_state.shared.money += 5
                self.not_earnable_tasks.append(item)
                self.update_wallet()
                print(shared_state.shared.money)

        elif state == 0: #item unchecked
            font.setStrikeOut(False)
        
        text.setFont(font)


    def add_task(self, info = ""):
        text = self.task_entry.text().strip()

        item = QListWidgetItem() #placeholder list item
        item.setSizeHint(QSize(200, 45))

        if info:
            text = info
            custom_task = CreateTaskWiget(self, text, False)


        else:
            custom_task = CreateTaskWiget(self, text, True)
            self.task_entry.clear()

        if not text:
            return
        
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, custom_task)
            


    def get_selected_index(self):
        row = self.list_widget.currentRow()
        if row == -1:
            QMessageBox.information(self, "Select Task", "Pick a task first.")
            return None
        return row


    def delete_task(self):
        i = self.get_selected_index()
        if i is None:
            return

        item = self.list_widget.item(i)
        if item.checkState() == Qt.CheckState.Checked or (item.checkState() == Qt.CheckState.Unchecked and (item not in self.tasks)):
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

        elif item.checkState() == Qt.CheckState.Unchecked:
            reply = QMessageBox.question(
                self,
                "Delete",
                "Delete this task? You won't get any money.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.tasks.remove(item)
                self.list_widget.takeItem(i)
                del item


    def clear_all(self):
        reply = QMessageBox.question(
            self,
            "Clear",
            "Delete all tasks?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.tasks.clear()
            self.list_widget.clear()

    
    def update_wallet(self):
        self.wallet.setText(f"Money: ${shared_state.shared.money}")


class TodoList(QStackedWidget):
    icon_clicked = pyqtSignal()
    shop_clicked = pyqtSignal()
    action_triggered = pyqtSignal()
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("To-Do List")
        self.setGeometry(100, 100, 400, 350)

        self.list_pages = []
        self.school_page = CreatePage("School", parent=self)
        self.list_pages.append(self.school_page)
        self.own_page = CreatePage("Own", parent=self)
        self.list_pages.append(self.own_page)

        for page in self.list_pages:
            self.addWidget(page)

        self.page_num = 0
        self.setCurrentIndex(self.page_num)

    
    def page_back(self):
        if self.page_num > 0:
            self.page_num -= 1
            self.change_page(self.page_num)
        
        else:
            print("no previous page")
    
    def page_forward(self):
        if self.page_num < (len(self.list_pages)-1):
            self.page_num += 1
            self.change_page(self.page_num)
        
        else:
            print("no more pages")
   
    def change_page(self, page_num):
        self.setCurrentIndex(page_num)
        page = self.currentWidget()
        page.update_wallet()

    
    def receive_task(self, info):
        self.school_page.add_task(info)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoList()
    window.show()
    sys.exit(app.exec())