from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton, QStackedWidget)
from PySide6.QtGui import (QPixmap, QIcon)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
import sys
from estilosProject import *
from IU.Ventanas.WEstadisticas import WidEstadisticas
from IU.Ventanas.WDashboard import WidDashboard
from IU.Ventanas.WObjetivos import WidObjetivos
from IU.Ventanas.WConsejos import WidConsejos
from IU.Ventanas.WUsers import WidUsers
from IU.Ventanas.WConfig import WidConfiguracion


class PyVisionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyVision")
        self.setMinimumSize(1100, 680)
        self.setStyleSheet(estilo1)

        # Widget central
        central = QWidget(objectName = "main")
        self.setCentralWidget(central)

        # Layout raíz: horizontal (sidebar | contenido)
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(5, 0, 0, 15)
        root_layout.setSpacing(10)

        # --- Frame 1: Sidebar ---
        self.sidebar = QFrame(objectName = "Sidebar")
        self.sidebar.setMaximumWidth(210)
        self.sidebar.setMinimumWidth(210)


        self.sidebarLayout = QVBoxLayout()
        #self.sidebarLayout.setContentsMargins(0,0,0,0)


        self.logo = QLabel()
        self.logo.setStyleSheet(imagenes)
        self.logo.setPixmap(QPixmap("pictures/logo.png").scaled(150, 150,
                                                                Qt.AspectRatioMode.KeepAspectRatio,
                                                                Qt.TransformationMode.SmoothTransformation))
        self.logo.setFixedHeight(60)

        #self.logo.setScaledContents(True)
        buttonToggle = QPushButton()
        buttonDash = QPushButton("    Dashboard")
        buttonEstadisticas = QPushButton("    Estadísticas")
        buttonObjetivos = QPushButton("    Objetivos")
        buttonConsejos = QPushButton("    Consejos")
        buttonUsuarios = QPushButton("    Usuarios")
        buttonConfiguracion = QPushButton("    Configuración")

        self.sidebarLayout.addWidget(self.logo, alignment= Qt.AlignmentFlag.AlignHCenter |
                                                           Qt.AlignmentFlag.AlignTop)


        botonesLayout = [buttonToggle, buttonDash,buttonEstadisticas, buttonObjetivos, buttonConsejos
                         , buttonUsuarios, buttonConfiguracion]

        buttonToggle.setIcon(QIcon("pictures/column.svg"))
        buttonDash.setIcon(QIcon("pictures/dash.svg"))
        buttonEstadisticas.setIcon(QIcon("pictures/statistics.svg"))
        buttonObjetivos.setIcon(QIcon("pictures/goals.svg"))
        buttonConsejos.setIcon(QIcon("pictures/health.svg"))
        buttonUsuarios.setIcon(QIcon("pictures/users.svg"))
        buttonConfiguracion.setIcon(QIcon("pictures/settings.svg"))

        for i in botonesLayout:
            i.setStyleSheet(buttonSide)
            i.setIconSize(QSize(24, 24))
        buttonToggle.clicked.connect(self.moveToggle)

        self.sidebarLayout.addWidget(buttonToggle, alignment= Qt.AlignmentFlag.AlignRight)
        self.sidebarLayout.addSpacing(10)
        self.sidebarLayout.addWidget(buttonDash)
        self.sidebarLayout.addSpacing(60)
        self.sidebarLayout.addWidget(buttonEstadisticas)
        self.sidebarLayout.addSpacing(10)
        self.sidebarLayout.addWidget(buttonObjetivos)
        self.sidebarLayout.addSpacing(10)
        self.sidebarLayout.addWidget(buttonConsejos)
        self.sidebarLayout.addStretch()
        self.sidebarLayout.addWidget(buttonUsuarios)
        self.sidebarLayout.addWidget(buttonConfiguracion)



        self.sidebar.setLayout(self.sidebarLayout)


        # --- Contenido derecho: vertical (frame2 arriba | frames 3+4 abajo) ---

        self.pilaFrames = QStackedWidget(ObjectName = "pila")


        self.ventanaDashboard = WidDashboard()
        self.ventanaEstadisticas = WidEstadisticas()
        self.ventanaObjetivos = WidObjetivos()
        self.ventanaConsejos = WidConsejos()
        self.ventanaUsuarios = WidUsers()
        self.ventanaConfiguracion = WidConfiguracion()

        self.pilaFrames.addWidget(self.ventanaDashboard)
        self.pilaFrames.addWidget(self.ventanaEstadisticas)
        self.pilaFrames.addWidget(self.ventanaObjetivos)
        self.pilaFrames.addWidget(self.ventanaConsejos)
        self.pilaFrames.addWidget(self.ventanaUsuarios)
        self.pilaFrames.addWidget(self.ventanaConfiguracion)



        root_layout.addWidget(self.sidebar)
        root_layout.addWidget(self.pilaFrames)

        buttonDash.clicked.connect(lambda: self.cambiarVentana(0))
        buttonEstadisticas.clicked.connect(lambda: self.cambiarVentana(1))
        buttonObjetivos.clicked.connect(lambda: self.cambiarVentana(2))
        buttonConsejos.clicked.connect(lambda: self.cambiarVentana(3))
        buttonUsuarios.clicked.connect(lambda: self.cambiarVentana(4))
        buttonConfiguracion.clicked.connect(lambda: self.cambiarVentana(5))


    def moveToggle(self):
        expandido = self.sidebar.width() > 60

        ancho_inicio = 210 if expandido else 60
        ancho_fin = 60 if expandido else 210
        if ancho_inicio > 60 :
            self.logo.setPixmap(QPixmap("pictures/logo.png").scaled(100, 100,
                                                                    Qt.AspectRatioMode.KeepAspectRatio,
                                                                    Qt.TransformationMode.SmoothTransformation))
        else:
            self.logo.setPixmap(QPixmap("pictures/logo.png").scaled(150, 150,
                                                                    Qt.AspectRatioMode.KeepAspectRatio,
                                                                    Qt.TransformationMode.SmoothTransformation))


        self.anim_min = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.anim_min.setDuration(250)
        self.anim_min.setStartValue(ancho_inicio)
        self.anim_min.setEndValue(ancho_fin)
        self.anim_min.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self.anim_max = QPropertyAnimation(self.sidebar, b"maximumWidth")
        self.anim_max.setDuration(250)
        self.anim_max.setStartValue(ancho_inicio)
        self.anim_max.setEndValue(ancho_fin)
        self.anim_max.setEasingCurve(QEasingCurve.Type.InOutCubic)


        self.anim_min.start()
        self.anim_max.start()


    def cambiarVentana(self, indice):
        self.pilaFrames.setCurrentIndex(indice)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PyVisionWindow()
    window.show()
    sys.exit(app.exec())