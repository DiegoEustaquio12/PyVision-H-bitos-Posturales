from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel
from IU.estilosProject import *


class WidConfiguracion(QWidget):
    def __init__(self):
        super().__init__()

        configuracionLayout = QVBoxLayout(self)
        configuracionLayout.setContentsMargins(0, 0, 15, 0)
        configuracionLayout.setSpacing(15)

        frameConfiguracion = QFrame()
        layout = QVBoxLayout(frameConfiguracion)
        layout.setContentsMargins(0, 0, 0, 0)

        etiqueta = QLabel("Configuracion")
        etiqueta.setAlignment(Qt.AlignmentFlag.AlignCenter)


        layout.addWidget(etiqueta)

        configuracionLayout.addWidget(frameConfiguracion)