from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QApplication
)
import sys
from IU.estilosProject import dialogo


class dialogoNuevaTarea(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)



        self.setFixedSize(400, 220)

        self.texto_resultado = None

        self.setStyleSheet(dialogo)



        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)

        titulo = QLabel("Nueva tarea")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)

        layout.addWidget(titulo)

        lblNombre = QLabel("Nombre de la tarea")

        self.inputTexto = QLineEdit()
        self.inputTexto.setPlaceholderText(
            "Tarea / Asignacion / Pendiente"
        )

        layout.addWidget(lblNombre)
        layout.addWidget(self.inputTexto)

        layout.addStretch()

        botonAceptar = QPushButton("Aceptar")
        botonAceptar.setCursor(Qt.PointingHandCursor)
        botonAceptar.clicked.connect(self._on_aceptar)

        layout.addWidget(botonAceptar)

    def _on_aceptar(self):
        texto = self.inputTexto.text().strip()

        if texto:
            self.texto_resultado = texto
            self.accept()
        else:
            self.texto_resultado = None
            self.reject()

        print("Nueva tarea:", texto)

#app = QApplication(sys.argv)
#dialogo = dialogoNuevaTarea()
#dialogo.exec()
