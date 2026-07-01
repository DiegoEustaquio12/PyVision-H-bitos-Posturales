from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QPushButton, QCheckBox
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
        layoutDetect.setContentsMargins(30, 20, 25, 12)

        estatusTxt = QLabel()
        estatusTxt.setText("Postura Correcta")
        estatusTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        estatusTxt.setStyleSheet(estado1)


        postureGoodTxt = QLabel()
        postureGoodTxt.setText("Tiempo con buena postura:       5:20")
        postureGoodTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        postureGoodTxt.setStyleSheet(contador1)
        postureGoodTxt.setAlignment(Qt.AlignmentFlag.AlignLeft)

        postureBadTxt = QLabel()
        postureBadTxt.setText("Tiempo con mala postura:         1:30")
        postureBadTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        postureBadTxt.setStyleSheet(contador2)
        postureBadTxt.setAlignment(Qt.AlignmentFlag.AlignLeft)

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
        layoutDetect.addSpacing(30)
        layoutDetect.addWidget(postureGoodTxt)
        layoutDetect.addSpacing(4)
        layoutDetect.addWidget(postureBadTxt)
        layoutDetect.addSpacing(10)
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

        tareaTxt = QLabel("            Tareas")
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
        for i in range(8):
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

        layoutProgression = QHBoxLayout()



        progressTime = WidgetCirculo()

        estatatusModo = QLabel()
        estatatusModo.setText("Trabajando")
        estatatusModo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        estatatusModo.setStyleSheet(modo1)

        modoTxt = QLabel()
        modoTxt.setText("Pomodoro modo")
        modoTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        modoTxt.setStyleSheet(modo1)

        txt = QLabel()
        txt.setText("texto relleno")
        txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        txt.setStyleSheet(modo1)



        layoutPomodoro.addSpacing(10)
        layoutPomodoro.addWidget(progressTime, stretch= 4)
        layoutPomodoro.addWidget(estatatusModo, stretch= 1)
        layoutPomodoro.addWidget(modoTxt, stretch= 1)


        bottom_layout.addWidget(frame_timer, stretch=3)
        bottom_layout.addWidget(frame_prefs, stretch=2)

        right_layout.addWidget(frame_status, stretch=50)
        right_layout.addWidget(bottom_widget, stretch=50)

