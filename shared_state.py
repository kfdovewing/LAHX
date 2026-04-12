import sys
import subprocess
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
)#add your very global variables here
# chars = {"cat" : "assets/buddies/cat.png", "froggy" : "assets/buddies/froggy.png", "hat_guy" : "assets/buddies/hat_guy.png", "party_guy" : "assets/buddies/party_guy.png"}
class shared(QWidget):
    buddy = ""
    money = 0
    food = 0
    hunger = 0
    happiness = 100

    def cat():
        shared.buddy = "assets/buddies/cat1.png"

    def frog():
        shared.buddy = "assets/buddies/frog1.png"

    def hat():
        shared.buddy = "assets/buddies/hat_guy.png"

    def party():
        shared.buddy = "assets/buddies/party1.png"