from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QPushButton
from IU.estilosProject import *

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

        tareaTxt = QLabel("Tareas")
        tareaTxt.setAlignment(Qt.AlignmentFlag.AlignLeft)

        scrollTareas = QScrollArea()
        contenidoScroll = QWidget()
        contenidoLayout = QVBoxLayout(contenidoScroll)
        for i in range(30):
            contenidoLayout.addWidget(QLabel(f"tarea {i+1} "))
        scrollTareas.setWidget(contenidoScroll)
        scrollTareas.setWidgetResizable(True)


        botonTareaWidget = QWidget()
        layoutBotones = QHBoxLayout(botonTareaWidget)

        buttonAgregar = QPushButton("Agregar")
        buttonMarcar = QPushButton("Marcar todo")
        layoutBotones.addWidget(buttonAgregar, stretch= 2)
        layoutBotones.addWidget(buttonMarcar, stretch= 3)

        layoutTimer.addWidget(tareaTxt)
        layoutTimer.addWidget(scrollTareas)
        layoutTimer.addWidget(botonTareaWidget)



        frame_prefs = QFrame()

        bottom_layout.addWidget(frame_timer, stretch=3)
        bottom_layout.addWidget(frame_prefs, stretch=2)

        right_layout.addWidget(frame_status, stretch=50)
        right_layout.addWidget(bottom_widget, stretch=50)

