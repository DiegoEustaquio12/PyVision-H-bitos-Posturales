from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QMessageBox,
    QAbstractSpinBox, QScrollArea, QWidget, QCheckBox
)
import sys
from PySide6.QtWidgets import QApplication
from IU.estilosProject import dialogSetTiempo

class dialogSelectTask(QDialog):

    def __init__(self, tareas_pendientes: list[tuple[int, str]],  parent=None):
        super().__init__(parent)

        self.checkboxs = {}
        self.sinAsignaciones = False #Bandera para distinguir el caso


        self.setFixedSize(600, 500)
        self.setStyleSheet(dialogSetTiempo)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)

        tittle = QLabel("Seleccion de Asignaciones")
        tittle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scrollSeleccion = QScrollArea()
        self.contenidoScrollSeleccion = QWidget()
        self.contenidoLayout = QVBoxLayout(self.contenidoScrollSeleccion)
        self.scrollSeleccion.setStyleSheet('''
                QScrollArea {
            border: none;
            background: transparent;
        }

        QScrollArea > QWidget > QWidget {
            background: #1f1f1f;
            border-radius: 15px;
        }
                ''')




        for id_tarea, texto in tareas_pendientes:
            check = QCheckBox(texto)
            self.checkboxs[id_tarea] = check
            self.contenidoLayout.addWidget(check)



        self.scrollSeleccion.setWidget(self.contenidoScrollSeleccion)
        self.scrollSeleccion.setWidgetResizable(True)


        botonesWidget = QWidget()
        layoutbotones = QVBoxLayout(botonesWidget)
        self.buttonAceptar = QPushButton("Aceptar")
        self.buttonAceptar.clicked.connect(self.on_aceptar)
        self.buttonAceptar.setStyleSheet('''
                QPushButton{
                background-color: #23614a;
                font-size: 15px;
                font-weight: bold;
                }
                QPushButton:hover {
                background-color: #3a8066;
                }
                QPushButton:pressed {
                background-color: #3d9e7a;
                }
                ''')
        self.buttonNinguna = QPushButton("Continuar sin Asignaciones")
        self.buttonNinguna.clicked.connect(self.on_sinAsignacion)
        self.buttonNinguna.setStyleSheet('''
                QPushButton{
                background-color: #9b9696;
                font-size: 15px;
                font-weight: bold;
                }
                QPushButton:hover {
                background-color: #c2bbbb;
                }

                QPushButton:pressed {
                background-color: #9b9696;
                }
                ''')
        layoutbotones.addWidget(self.buttonAceptar, stretch=2)
        layoutbotones.addWidget(self.buttonNinguna, stretch=2)

        layout.addWidget(tittle)
        layout.addWidget(self.scrollSeleccion)
        layout.addWidget(botonesWidget)

    def tareas_seleccionadas(self) -> list[int]:
        return [id_tarea for id_tarea, check in self.checkboxs.items() if check.isChecked()]

    def on_aceptar(self):
        if not self.tareas_seleccionadas():
            return
        self.accept()

    def on_sinAsignacion(self):
        self.sinAsignaciones = True
        self.accept()











#app = QApplication(sys.argv)
#dialogo = dialogSelectTask()
#dialogo.exec()
