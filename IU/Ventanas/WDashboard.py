from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QPushButton, QMenu, \
    QSizePolicy, QComboBox
from IU.estilosProject import *
from IU.Ventanas.Widgets.BarProgressCircle import WidgetCirculo
from IU.Ventanas.Widgets.targetaTarea import tareaTarget


class WidDashboard(QWidget):
    def __init__(self):
        super().__init__()

        right_layout = QVBoxLayout(self)
        right_layout.setContentsMargins(0, 0, 15, 0)
        right_layout.setSpacing(15)

        # Frame 2: Estatus + Cámara
        frame_status = QFrame()

        layoutSuperior = QHBoxLayout(frame_status)
        layoutSuperior.setContentsMargins(5, 5, 5, 5)
        layoutSuperior.setSpacing(10)

        frameDetect = QFrame(objectName = "frameInterno")
        layoutDetect = QVBoxLayout(frameDetect)
        layoutDetect.setContentsMargins(12, 15, 25, 10)

        estatusTxt = QLabel()
        estatusTxt.setText("Postura Correcta")
        estatusTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        estatusTxt.setStyleSheet(estado1)


        widgetTiempos = QWidget()
        layoutTiempos = QHBoxLayout(widgetTiempos)

        frameTiempo1=QFrame()
        frameTiempo1.setStyleSheet('''
        QFrame{
        background-color: rgba(255,255,255,40);
        border: 1px solid rgba(255,255,255,80);
        border-radius:20px;
         }
        ''')
        layoutFrame1 = QVBoxLayout(frameTiempo1)

        frameTiempo2 =QFrame()
        frameTiempo2.setStyleSheet('''
        QFrame{
        background-color: #8d0809;
        }
        ''')
        layoutFrame2 = QVBoxLayout(frameTiempo2)

        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)
        linea.setFrameShadow(QFrame.Shadow.Sunken)
        linea.setFixedHeight(1)
        linea.setStyleSheet("""
        QFrame{
            background-color: #b4b4b4;
            border-color: transparent;
        }
        """)

        linea2 = QFrame()
        linea2.setFrameShape(QFrame.Shape.HLine)
        linea2.setFrameShadow(QFrame.Shadow.Sunken)
        linea2.setFixedHeight(1)
        linea2.setStyleSheet("""
         QFrame{
             background-color: #b4b4b4;
             border-color: transparent;
         }
         """)

        postureGoodTxt1 = QLabel()
        postureGoodTxt1.setText("Buena Postura")
        postureGoodTxt1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        postureGoodTxt1.setStyleSheet(contador1)


        postureGoodTxt2 = QLabel()
        postureGoodTxt2.setText("5:20")
        postureGoodTxt2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        postureGoodTxt2.setStyleSheet(contador1)

        layoutFrame1.addWidget(postureGoodTxt1)
        layoutFrame1.addWidget(linea)
        layoutFrame1.addWidget(postureGoodTxt2)


        postureBadTxt1 = QLabel()
        postureBadTxt1.setText("Mala Postura")
        postureBadTxt1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        postureBadTxt1.setStyleSheet(contador2)

        postureBadTxt2 = QLabel()
        postureBadTxt2.setText("1:30")
        postureBadTxt2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        postureBadTxt2.setStyleSheet(contador2)

        layoutFrame2.addWidget(postureBadTxt1)
        layoutFrame2.addWidget(linea2)
        layoutFrame2.addWidget(postureBadTxt2)

        layoutTiempos.addWidget(frameTiempo1)
        layoutTiempos.addWidget(frameTiempo2)

        rachaTxt = QLabel()
        rachaTxt.setText("Racha:          2:05 min")
        rachaTxt.setAlignment(Qt.AlignmentFlag.AlignLeft)
        rachaTxt.setStyleSheet(racha)
        rachaTxt.setFixedWidth(300)

        timeSeccionTxt = QLabel()
        timeSeccionTxt.setText("Tiempo de sesión:    6:50")
        timeSeccionTxt.setAlignment(Qt.AlignmentFlag.AlignLeft.AlignVCenter)
        timeSeccionTxt.setStyleSheet(contador3)




        layoutDetect.addWidget(estatusTxt, alignment= Qt.AlignmentFlag.AlignTop)
        layoutDetect.addSpacing(4)
        layoutDetect.addWidget(widgetTiempos)
        layoutDetect.addSpacing(4)
        layoutDetect.addWidget(rachaTxt)
        layoutDetect.addStretch()
        layoutDetect.addWidget(timeSeccionTxt)
        layoutDetect.addStretch()



        frameVision = QFrame()

        layoutSuperior.addWidget(frameDetect, stretch=4)
        layoutSuperior.addWidget(frameVision, stretch=5)

        # Fila inferior: Frame 3 + Frame 4 lado a lado
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(10)

        frame_timer = QFrame()
        layoutTimer = QVBoxLayout(frame_timer)

        tareaTxt = QLabel("         Tareas")
        tareaTxt.setStyleSheet('''
        QLabel{
        border: transparent;
        font-size: 20px;
        font-weight: bold;

        }
        
        ''')
        tareaTxt.setAlignment(Qt.AlignmentFlag.AlignLeft)

        scrollTareas = QScrollArea()
        contenidoScroll = QWidget()
        contenidoLayout = QVBoxLayout(contenidoScroll)
        contenidoLayout.setAlignment(Qt.AlignmentFlag.AlignTop)


        targetas = tareaTarget()
        for i in range(4):
            targetas = tareaTarget()
            contenidoLayout.addWidget(targetas)



        scrollTareas.setWidget(contenidoScroll)
        scrollTareas.setWidgetResizable(True)


        botonTareaWidget = QWidget()
        layoutBotones = QHBoxLayout(botonTareaWidget)

        buttonAgregar = QPushButton("Agregar")
        buttonAgregar.setStyleSheet('''
        QPushButton{
        background-color: #00897b;
        font-size: 15px;
        font-weight: bold;
        }
        QPushButton:hover {
        background-color: #3a998f;
        }
        QPushButton:pressed {
        background-color: #00897b;
        }
        ''')
        buttonMarcar = QPushButton("Marcar todo")
        buttonMarcar.setStyleSheet('''
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
        layoutBotones.addWidget(buttonAgregar, stretch= 2)
        layoutBotones.addWidget(buttonMarcar, stretch= 3)

        layoutTimer.addWidget(tareaTxt)
        layoutTimer.addWidget(scrollTareas)
        layoutTimer.addWidget(botonTareaWidget)



        frame_prefs = QFrame()
        layoutPomodoro = QVBoxLayout(frame_prefs)

        progressTime = WidgetCirculo()

        widgetStart = QWidget()
        layoutStart = QHBoxLayout(widgetStart)

        estatatusModo = QLabel()
        estatatusModo.setText("Trabajando")
        estatatusModo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        estatatusModo.setStyleSheet(modo1)

        buttonStart = QPushButton()
        buttonStart.setIcon(QIcon("pictures/play.svg"))
        buttonStart.setIconSize(QSize(21, 21))
        buttonStart.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        layoutStart.addWidget(estatatusModo, stretch= 3)
        layoutStart.addWidget(buttonStart, stretch= 1)

        SelectModeBar = QWidget()
        layoutSelect = QHBoxLayout(SelectModeBar)


        buttonMode = QPushButton(self)
        buttonMode.setIcon(QIcon("pictures/menu.svg"))
        buttonMode.setIconSize(QSize(19, 19))
        buttonMode.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        buttonMode.setStyleSheet('''
                QPushButton{
                background-color: #9b9696;
                font-size: 15px;
                font-weight: bold;
                border-radius: 10px;
                }
                QPushButton:hover {
                background-color: #c2bbbb;
                }

                QPushButton:pressed {
                background-color: #9b9696;
                }
                ''')

        self.modoTxt = QLabel(self)
        self.modoTxt.setText("Modo")
        self.modoTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.modoTxt.setStyleSheet(modo1)


        selecMenu = QMenu(self)
        accionPomodoro = selecMenu.addAction("Pomodoro")
        accionEnfoque = selecMenu.addAction("Enfoque")
        accionPredeterminado = selecMenu.addAction("Predeterminado")

        accionPomodoro.triggered.connect(self.txtPomodoro)
        accionEnfoque.triggered.connect(self.txtEnfoque)
        accionPredeterminado.triggered.connect(self.txtPredeterminado)



        selecMenu.setStyleSheet("""
        QMenu {
            background-color: #2b2d31;
            color: white;
            border: 1px solid #444;
        }

        QMenu::item {
            padding: 8px 30px;
        }

        QMenu::item:selected {
            background-color: #5865F2;
        }
        """)
        buttonMode.setMenu(selecMenu)
        buttonMode.show()



        layoutSelect.addWidget(self.modoTxt, stretch= 4)
        layoutSelect.addWidget(buttonMode, stretch= 1)

        layoutPomodoro.addStretch()
        layoutPomodoro.addWidget(progressTime, stretch= 4)
        layoutPomodoro.addSpacing(15)
        layoutPomodoro.addWidget(widgetStart, stretch= 1)
        layoutPomodoro.addSpacing(10)
        layoutPomodoro.addWidget(SelectModeBar, stretch= 1)


        bottom_layout.addWidget(frame_timer, stretch=3)
        bottom_layout.addWidget(frame_prefs, stretch=2)

        right_layout.addWidget(frame_status, stretch=50)
        right_layout.addWidget(bottom_widget, stretch=50)

    def txtPomodoro(self):
        self.modoTxt.setText("Pomodoro Mode")
    def txtEnfoque(self):
        self.modoTxt.setText("Enfoque Mode")
    def txtPredeterminado(self):
        self.modoTxt.setText("Predeterminado Mode")


