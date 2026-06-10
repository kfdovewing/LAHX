from PyQt6.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QWidget
from PyQt6.QtCore import QDate
import sys

class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PyQt6 Calendar Example")
        self.setGeometry(100, 100, 400, 300)

        # Create main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create the Calendar Widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        
        # Connect date selection to a function
        self.calendar.selectionChanged.connect(self.date_changed)
        
        layout.addWidget(self.calendar)

        # Set an initial selected date programmatically
        self.calendar.setSelectedDate(QDate(2026, 6, 6))

    def date_changed(self):
        selected_date = self.calendar.selectedDate()
        print("Date selected:", selected_date.toString("MM-dd"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CalendarApp()
    ex.show()
    sys.exit(app.exec())
