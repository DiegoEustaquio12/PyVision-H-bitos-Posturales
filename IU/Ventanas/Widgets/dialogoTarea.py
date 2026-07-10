from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
import sys
from PySide6.QtWidgets import QApplication

class dialogoNuevaTarea(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nueva tarea")
        self.setFixedSize(300, 120)

        self.texto_resultado = None

        layout = QVBoxLayout(self)

        label1 = QLabel("Nombre de la tarea:")
        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(label1)

        self.inputTexto = QLineEdit()
        layout.addWidget(self.inputTexto)

        botonAceptar = QPushButton("Aceptar")
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
            print(self.texto_resultado)


        print("Nueva tarea: ", texto)

#app = QApplication(sys.argv)
#dialogo = dialogoNuevaTarea()
#dialogo.exec()
