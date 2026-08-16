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
    QAbstractSpinBox, QScrollArea, QWidget
)
import sys
from PySide6.QtWidgets import QApplication
from IU.estilosProject import dialogSetTiempo
from IU.Ventanas.WDashboard import WidDashboard

class dialogSelectTask(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)



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


        self.contenidoDashboard = WidDashboard()



        self.scrollSeleccion.setWidget(self.contenidoScrollSeleccion)
        self.scrollSeleccion.setWidgetResizable(True)


        botonesWidget = QWidget()
        layoutbotones = QVBoxLayout(botonesWidget)
        self.buttonAceptar = QPushButton("Aceptar")
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












app = QApplication(sys.argv)
dialogo = dialogSelectTask()
dialogo.exec()
