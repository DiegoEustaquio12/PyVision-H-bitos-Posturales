from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel
from IU.estilosProject import *


class WidUsers(QWidget):
    def __init__(self):
        super().__init__()

        userlayout = QVBoxLayout(self)
        userlayout.setContentsMargins(0, 0, 15, 0)
        userlayout.setSpacing(15)

        frameUser = QFrame()
        layout = QVBoxLayout(frameUser)
        layout.setContentsMargins(0, 0, 0, 0)

        etiqueta = QLabel("Users")
        etiqueta.setAlignment(Qt.AlignmentFlag.AlignCenter)


        layout.addWidget(etiqueta)

        userlayout.addWidget(frameUser)