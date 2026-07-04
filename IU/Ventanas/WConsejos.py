from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel


class WidConsejos(QWidget):
    def __init__(self):
        super().__init__()

        consejoslayout = QVBoxLayout(self)
        consejoslayout.setContentsMargins(0, 0, 15, 0)
        consejoslayout.setSpacing(15)

        frameConsejos = QFrame()
        layout = QVBoxLayout(frameConsejos)
        layout.setContentsMargins(0, 0, 0, 0)

        etiqueta = QLabel("Consejos")
        etiqueta.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(etiqueta)

        consejoslayout.addWidget(frameConsejos)