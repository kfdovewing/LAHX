import sys
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

app = QApplication(sys.argv)

w = 350
h = 400

centerw = w/2
centerh = h/2

label = QLabel()

pixmap = QPixmap("egg2.png")
label.setPixmap(pixmap)
# Remove title bar
# label.setWindowFlags(Qt.WindowType.FramelessWindowHint|Qt.WindowType.WindowStaysOnTopHint)

label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
label.setStyleSheet("background: transparent;")

label.show()


sys.exit(app.exec())
