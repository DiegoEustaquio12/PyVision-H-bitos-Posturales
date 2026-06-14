from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel
from IU.estilosProject import *


class WidEstadisticas(QWidget):
    def __init__(self):
        super().__init__()

        Estadisticaslayout = QVBoxLayout(self)
        Estadisticaslayout.setContentsMargins(0, 0, 15, 0)
        Estadisticaslayout.setSpacing(15)

        frameEstadisticas = QFrame()
        layout = QVBoxLayout(frameEstadisticas)
        layout.setContentsMargins(0, 0, 0, 0)

        etiqueta = QLabel("Estadisticas")
        etiqueta.setAlignment(Qt.AlignmentFlag.AlignCenter)


        layout.addWidget(etiqueta)

        Estadisticaslayout.addWidget(frameEstadisticas)