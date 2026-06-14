from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel


class WidObjetivos(QWidget):
    def __init__(self):
        super().__init__()

        objetivoslayout = QVBoxLayout(self)
        objetivoslayout.setContentsMargins(0, 0, 15, 0)
        objetivoslayout.setSpacing(15)

        frameObjetivos = QFrame()
        layout = QVBoxLayout(frameObjetivos)
        layout.setContentsMargins(0, 0, 0, 0)

        etiqueta = QLabel("Objetivos")
        etiqueta.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(etiqueta)

        objetivoslayout.addWidget(frameObjetivos)