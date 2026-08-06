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
    QAbstractSpinBox
)
import sys
from PySide6.QtWidgets import QApplication



class dialogNewTime(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.nombreSet = None
        self.setTrabajo = None
        self.setDescanso = None

        self.setWindowTitle(" ")
        self.setFixedSize(400, 535)

        self.setStyleSheet("""
        QDialog{
            background:#202124;
        }

        QLabel#title{
            color:white;
            font-size:24px;
            font-weight:700;
        }

        QLabel#subtitle{
            color:#B8B8B8;
            font-size:18px;
            font-weight:700;
        }

        QLabel{
            color:white;
            font-size:15px;
            font-weight:600;
        }

        QLineEdit{
            background:#2B2D31;
            border:2px solid #3A3D42;
            border-radius:12px;
            padding:10px;
            color:white;
            font-size:15px;
        }

        QLineEdit:focus{
            border:2px solid #4F8EF7;
        }

        QSpinBox{
            background:#2B2D31;
            border:2px solid #3A3D42;
            border-radius:12px;

            color:white;
            font-size:26px;
            font-weight:bold;

            min-width:120px;
            min-height:45px;
        }

        QSpinBox:focus{
            border:2px solid #4F8EF7;
        }

        QSpinBox::up-button,
        QSpinBox::down-button{
            width:25px;
            height:30px;
            }
        


        QPushButton{
            background:#4F8EF7;
            color:white;
            border:none;
            border-radius:12px;
            padding:12px;
            font-size:15px;
            font-weight:bold;
        }

        QPushButton:hover{
            background:#6AA5FF;
        }

        QPushButton:pressed{
            background:#2F6FE5;
        }
        """)

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(25, 20, 25, 20)
        mainLayout.setSpacing(20)

        # ------------------------
        # Título
        # ------------------------

        lblTitle = QLabel("Nuevo temporizador")
        lblTitle.setObjectName("title")
        lblTitle.setAlignment(Qt.AlignCenter)

        mainLayout.addWidget(lblTitle)

        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)
        linea.setFrameShadow(QFrame.Shadow.Sunken)
        linea.setFixedHeight(2)
        linea.setStyleSheet("""
                QFrame{
                    background-color: #2F6FE5;
                    border-color: #2F6FE5;
                }
                """)
        mainLayout.addWidget(linea)

        # ------------------------
        # Nombre
        # ------------------------

        lblNombre = QLabel(objectName = "subtitle")
        lblNombre.setText("Nombre del temporizador")

        self.txtNombre = QLineEdit()
        self.txtNombre.setPlaceholderText("Asignación")

        mainLayout.addWidget(lblNombre)
        mainLayout.addWidget(self.txtNombre)

        # ------------------------
        # Trabajo
        # ------------------------

        lblTrabajo = QLabel(objectName = "subtitle")
        lblTrabajo.setText("Tiempo de trabajo")

        gridTrabajo = QGridLayout()

        self.spMinTrabajo = QSpinBox()
        self.spMinTrabajo.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spMinTrabajo.setRange(0, 999)
        self.spMinTrabajo.setValue(25)

        self.spSegTrabajo = QSpinBox()
        self.spSegTrabajo.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spSegTrabajo.setRange(0, 59)

        gridTrabajo.addWidget(self.spMinTrabajo, 0, 0)
        gridTrabajo.addWidget(self.spSegTrabajo, 0, 1)

        lblMin = QLabel()
        lblMin.setText("Minutos")
        lblMin.setAlignment(Qt.AlignmentFlag.AlignRight)

        lblSeg = QLabel("Segundos")
        lblSeg.setAlignment(Qt.AlignmentFlag.AlignRight)

        gridTrabajo.addWidget(lblMin, 1, 0)
        gridTrabajo.addWidget(lblSeg, 1, 1)

        mainLayout.addWidget(lblTrabajo)
        mainLayout.addLayout(gridTrabajo)

        # ------------------------
        # Descanso
        # ------------------------

        lblDescanso = QLabel(objectName = "subtitle")
        lblDescanso.setText("Tiempo de descanso")
        gridDescanso = QGridLayout()

        self.spMinDescanso = QSpinBox()
        self.spMinDescanso.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spMinDescanso.setRange(0, 999)
        self.spMinDescanso.setValue(5)

        self.spSegDescanso = QSpinBox()
        self.spSegDescanso.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spSegDescanso.setRange(0, 59)

        gridDescanso.addWidget(self.spMinDescanso, 0, 0)
        gridDescanso.addWidget(self.spSegDescanso, 0, 1)

        lblMin2 = QLabel("Minutos")
        lblMin2.setAlignment(Qt.AlignmentFlag.AlignRight)

        lblSeg2 = QLabel("Segundos")
        lblSeg2.setAlignment(Qt.AlignmentFlag.AlignRight)

        gridDescanso.addWidget(lblMin2, 1, 0)
        gridDescanso.addWidget(lblSeg2, 1, 1)

        mainLayout.addWidget(lblDescanso)
        mainLayout.addLayout(gridDescanso)

        mainLayout.addStretch()

        # ------------------------
        # Botón
        # ------------------------

        self.btnAgregar = QPushButton("Agregar")
        self.btnAgregar.setCursor(Qt.PointingHandCursor)

        self.btnAgregar.clicked.connect(self.accept)

        mainLayout.addWidget(self.btnAgregar)

    @property
    def nombreTemporizador(self) -> str:
        return self.txtNombre.text().strip()

    @property
    def minTrabajo(self) -> int:
        return self.spMinTrabajo.value()

    @property
    def segTrabajo(self) -> int:
        return self.spSegTrabajo.value()

    @property
    def minDescanso(self) -> int:
        return self.spMinDescanso.value()

    @property
    def segDescanso(self) -> int:
        return self.spSegDescanso.value()

    def accept(self):

        nombre = self.txtNombre.text().strip()

        # Validar nombre
        if not nombre:
            QMessageBox.warning(
                self,
                "Nombre requerido",
                "Ingresa un nombre para el temporizador."
            )
            self.txtNombre.setFocus()
            return

        # Validar tiempo de trabajo
        if (self.spMinTrabajo.value() == 0 and
                self.spSegTrabajo.value() == 0):
            QMessageBox.warning(
                self,
                "Tiempo inválido",
                "El tiempo de trabajo no puede ser 00:00."
            )
            self.spMinTrabajo.setFocus()
            return

        # Validar tiempo de descanso
        if (self.spMinDescanso.value() == 0 and
                self.spSegDescanso.value() == 0):
            QMessageBox.warning(
                self,
                "Tiempo inválido",
                "El tiempo de descanso no puede ser 00:00."
            )
            self.spMinDescanso.setFocus()
            return

        #all correct
        super().accept()
        print(f"Nombre: {nombre}")
        print(f"Tiempos de Trabajo: {self.spMinTrabajo.value()} : {self.spSegTrabajo.value()}")
        print(f"Tiempos de Descanso: {self.spMinDescanso.value()} : {self.spSegDescanso.value()}")

        self.setTrabajo = (self.spMinTrabajo.value() * 60) + self.spSegTrabajo.value()
        self.setDescanso = (self.spMinDescanso.value() * 60) + self.spSegDescanso.value()
        self.nombreSet = nombre

        print(f"Tiempo de trabajo: {self.setTrabajo}, Tiempo de descanso: {self.setDescanso}, Nombre: {self.nombreSet}")



#app = QApplication(sys.argv)
#dialogo = dialogNewTime()
#dialogo.exec()
