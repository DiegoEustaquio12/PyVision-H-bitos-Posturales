from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QAction, QIcon, QPixmap, QColor
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QPushButton, QMenu, \
    QSizePolicy, QComboBox, QDialog, QGraphicsDropShadowEffect
from IU.estilosProject import *
from IU.Ventanas.Widgets.BarProgressCircle import WidgetCirculo
from IU.Ventanas.Widgets.targetaTarea import tareaTarget
from IU.Ventanas.Widgets.dialogoTarea import dialogoNuevaTarea
from IU.Ventanas.Widgets.dialogNewSetTime import dialogNewTime
from IU.Ventanas.Widgets.structureTime import ContadorPostura
from PySide6.QtSvgWidgets import QSvgWidget
from IU.Ventanas.Widgets.dialogManegerTask import dialogSelectTask

from IU.GUI.visionWorker1 import VisionWorker
from IU.GUI import visonAdapter
import time

import os
from PySide6.QtMultimedia import QSoundEffect
from enum import Enum, auto


from dataclasses import dataclass, field
from datetime import datetime



class EstadoApp(Enum):
    INACTIVO = auto()
    LIBRE = auto()
    EN_SESION = auto()


class WidDashboard(QWidget):
    def __init__(self):
        super().__init__()

        self._estado_app = EstadoApp.INACTIVO
        self._sesion_pendientes = set()


        self.ciclosTerminados = 0

        self._sonido_alerta = QSoundEffect(self)
        base_path = os.path.dirname(os.path.abspath(__file__))
        ruta_wav = os.path.normpath(os.path.join(base_path, "..", "sounds", "errorSound.wav"))
        self._sonido_alerta.setSource(QUrl.fromLocalFile(ruta_wav))
        self._sonido_alerta.setLoopCount(-2)
        self._sonido_alerta.setVolume(1)

        self._estado_anterior = None

        self._sonido_ausencia = QSoundEffect(self)
        base_path_deteccion = os.path.dirname(os.path.abspath(__file__))
        ruta_wav_2 = os.path.normpath(os.path.join(base_path_deteccion, "..", "sounds", "sindeteccion1.wav"))
        self._sonido_ausencia.setSource(QUrl.fromLocalFile(ruta_wav_2))
        self._sonido_ausencia.setLoopCount(-2)
        self._sonido_ausencia.setVolume(1)

        self._estado_anterior_ausencia = None


        right_layout = QVBoxLayout(self)
        right_layout.setContentsMargins(0, 0, 15, 0)
        right_layout.setSpacing(15)

        # Frame 2: Estatus + Cámara
        frame_status = QFrame()

        layoutSuperior = QHBoxLayout(frame_status)
        layoutSuperior.setContentsMargins(9, 15, 20, 15)
        #layoutSuperior.setSpacing(10)

        frameDetect = QFrame(objectName = "frameInterno")
        layoutDetect = QVBoxLayout(frameDetect)
        layoutDetect.setContentsMargins(12, 15, 18, 10)



        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)  # Qué tan difuminada
        shadow.setOffset(0, 6)  # x, y
        shadow.setColor(QColor(0, 0, 0, 120))
        frameDetect.setGraphicsEffect(shadow)
        frameDetect.graphicsEffect()

        self.estatusTxt = QLabel()
        self.estatusTxt.setText("Esperando...")
        self.estatusTxt.setFixedHeight(50)
        self.estatusTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.estatusTxt.setStyleSheet("""
            background:#555;
            color:white;
            border-radius:20px;
            font-size:25px;
            font-weight:bold;
            """
            )


        widgetTiempos = QWidget()
        layoutTiempos = QHBoxLayout(widgetTiempos)
        widgetTiempos.setMinimumHeight(90)

        frameTiempo1=QFrame()
        frameTiempo1.setStyleSheet('''
        QFrame{
        background-color: #172928;
        border: 1px solid #1e5649;
        border-radius:20px;
         }
        ''')
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(30)  # Qué tan difuminada
        shadow2.setOffset(0, 6)  # x, y
        shadow2.setColor(QColor(0, 50, 0, 120))

        frameTiempo1.setGraphicsEffect(shadow2)
        frameTiempo1.graphicsEffect()

        layoutFrame1 = QVBoxLayout(frameTiempo1)

        frameTiempo2 =QFrame()
        frameTiempo2.setStyleSheet('''
        QFrame{
        background-color: #292021;
        border: 1px solid #61332e;
        border-radius:20px;
        }
        ''')

        shadow3 = QGraphicsDropShadowEffect()
        shadow3.setBlurRadius(30)  # Qué tan difuminada
        shadow3.setOffset(0, 6)  # x, y
        shadow3.setColor(QColor(50, 0, 0, 120))

        frameTiempo2.setGraphicsEffect(shadow3)
        frameTiempo2.graphicsEffect()

        layoutFrame2 = QVBoxLayout(frameTiempo2)

        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)
        linea.setFrameShadow(QFrame.Shadow.Sunken)
        linea.setFixedHeight(1)
        linea.setStyleSheet("""
        QFrame{
            background-color: #1e5649;
            border-color: transparent;
        }
        """)

        linea2 = QFrame()
        linea2.setFrameShape(QFrame.Shape.HLine)
        linea2.setFrameShadow(QFrame.Shadow.Sunken)
        linea2.setFixedHeight(1)
        linea2.setStyleSheet("""
         QFrame{
             background-color: #61332e;
             border-color: transparent;
         }
         """)

        linea3 = QFrame()
        linea3.setFrameShape(QFrame.Shape.VLine)
        linea3.setFrameShadow(QFrame.Shadow.Sunken)
        linea3.setFixedWidth(1)
        linea3.setStyleSheet("""
                 QFrame{
                     background-color: #dd9a3a;
                     border-color: transparent;
                 }
                 """)
        linea4 = QFrame()
        linea4.setFrameShape(QFrame.Shape.VLine)
        linea4.setFrameShadow(QFrame.Shadow.Sunken)
        linea4.setFixedWidth(1)
        linea4.setStyleSheet("""
                         QFrame{
                             background-color: #fdd502;
                             border-color: transparent;
                         }
                         """)
        widgetTiempo1 = QWidget()
        layoutIconString1 = QHBoxLayout(widgetTiempo1)
        layoutIconString1.setContentsMargins(5, 0, 0, 5)
        layoutIconString1.setSpacing(6)



        icon1 = QSvgWidget("pictures/posturaBuena.svg")
        icon1.setFixedSize(22,22)

        postureGoodTxt1 = QLabel()
        postureGoodTxt1.setText("Buena Postura")
        postureGoodTxt1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        postureGoodTxt1.setStyleSheet(labelGood)

        layoutIconString1.addWidget(icon1)
        layoutIconString1.addWidget(postureGoodTxt1)


        self.postureGoodTxt2 = QLabel()
        self.postureGoodTxt2.setText("0:00")
        self.postureGoodTxt2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.postureGoodTxt2.setStyleSheet(contador1)


        layoutFrame1.addWidget(widgetTiempo1)
        layoutFrame1.addWidget(linea)
        layoutFrame1.addWidget(self.postureGoodTxt2)


        widgetTiempo2 = QWidget()
        layoutIconString2 = QHBoxLayout(widgetTiempo2)
        layoutIconString2.setContentsMargins(5, 0, 0, 5)
        layoutIconString2.setSpacing(6)


        icon2 = QSvgWidget("pictures/posturaMala.svg")
        icon2.setFixedSize(22,22)

        postureBadTxt1 = QLabel()
        postureBadTxt1.setText("Mala Postura")
        postureBadTxt1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        postureBadTxt1.setStyleSheet(labelBad)

        layoutIconString2.addWidget(icon2)
        layoutIconString2.addWidget(postureBadTxt1)

        self.postureBadTxt2 = QLabel()
        self.postureBadTxt2.setText("0:00")
        self.postureBadTxt2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.postureBadTxt2.setStyleSheet(contador2)

        layoutFrame2.addWidget(widgetTiempo2)
        layoutFrame2.addWidget(linea2)
        layoutFrame2.addWidget(self.postureBadTxt2)

        layoutTiempos.addWidget(frameTiempo1)
        layoutTiempos.addWidget(frameTiempo2)

        frameRacha = QFrame()
        layoutRachaa = QHBoxLayout(frameRacha)

        frameRacha.setStyleSheet('''
                QFrame{
                background-color: #black;
                border: None;
                border-radius:16px;
                }
                ''')
        shadowR = QGraphicsDropShadowEffect()
        shadowR.setBlurRadius(30)  # Qué tan difuminada
        shadowR.setOffset(0, 6)  # x, y
        shadowR.setColor(QColor(0, 0, 0, 120))
        frameRacha.setGraphicsEffect(shadowR)
        frameRacha.graphicsEffect()

        icon3 = QSvgWidget("pictures/rachaIcon.svg")
        icon3.setFixedSize(22, 22)

        rachaTxt = QLabel()
        rachaTxt.setText("Racha")
        rachaTxt.setStyleSheet(labelRacha)
        rachaTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #rachaTxt.setFixedWidth(300)


        self.rachaTxt2 = QLabel()
        self.rachaTxt2.setText("0:00")
        self.rachaTxt2.setStyleSheet(contador1)
        self.rachaTxt2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layoutRachaa.addSpacing(10)
        layoutRachaa.addWidget(icon3)

        layoutRachaa.addWidget(rachaTxt, stretch=1)
        layoutRachaa.addWidget(linea3)
        layoutRachaa.addStretch()
        layoutRachaa.addWidget(self.rachaTxt2, stretch=3)

        frameRecord = QFrame()
        layoutRecord = QHBoxLayout(frameRecord)

        frameRecord.setStyleSheet('''
                        QFrame{
                        background-color: #black;
                        border: None;
                        border-radius:16px;
                        }
                        ''')
        shadowRec = QGraphicsDropShadowEffect()
        shadowRec.setBlurRadius(30)  # Qué tan difuminada
        shadowRec.setOffset(0, 6)  # x, y
        shadowRec.setColor(QColor(0, 0, 0, 120))
        frameRecord.setGraphicsEffect(shadowRec)
        frameRecord.graphicsEffect()

        icon4 = QSvgWidget("pictures/trophy.svg")
        icon4.setFixedSize(22, 22)

        recordTxt = QLabel()
        recordTxt.setText("Tiempo mas alto")
        recordTxt.setStyleSheet(labelRecord)
        recordTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # rachaTxt.setFixedWidth(300)

        self.recordTxt2 = QLabel()
        self.recordTxt2.setText("0:00")
        self.recordTxt2.setStyleSheet(contador1)
        self.recordTxt2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.botonPrueba = QPushButton("Iniciar Seccion")
        self.botonPrueba.clicked.connect(self.on_start_clicked)
        self.setStyleSheet(botonSecion)



        layoutRecord.addSpacing(10)
        layoutRecord.addWidget(icon4)
        layoutRecord.addSpacing(14)
        layoutRecord.addWidget(recordTxt, stretch=1)
        layoutRecord.addSpacing(10)
        layoutRecord.addWidget(linea4)
        layoutRecord.addSpacing(20)
        layoutRecord.addWidget(self.recordTxt2, stretch=3)
        layoutRecord.addSpacing(20)




        layoutDetect.addWidget(self.estatusTxt, alignment= Qt.AlignmentFlag.AlignTop)
        layoutDetect.addSpacing(4)
        layoutDetect.addWidget(widgetTiempos)
        layoutDetect.addSpacing(4)
        layoutDetect.addWidget(frameRacha)
        layoutDetect.addSpacing(9)
        layoutDetect.addWidget(frameRecord)

        layoutDetect.addSpacing(10)
        layoutDetect.addWidget(self.botonPrueba)
        #layoutDetect.addWidget(timeSeccionTxt)
        #layoutDetect.addWidget(self.visionButton, alignment= Qt.AlignmentFlag.AlignLeft)



        frameVision = QFrame()
        frameVision.setStyleSheet("""
        QFrame{
        border-color: transparent;
        border-radius: 120px;
        }
        """)
        visionLayout = QVBoxLayout(frameVision)
        visionLayout.setContentsMargins(0, 0, 0, 0)

        shadowS = QGraphicsDropShadowEffect()
        shadowS.setBlurRadius(35)  # Qué tan difuminada
        shadowS.setOffset(0, 8)  # x, y
        shadowS.setColor(QColor(0,0, 0, 140))

        frameVision.setGraphicsEffect(shadowS)
        frameVision.graphicsEffect()



        #visonAdapter.iniciar_vision()

        self.labelCamara = QLabel()
        self.labelCamara.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelCamara.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.labelCamara.setMinimumSize(1, 1)  # evita que colapse a 0
        self.labelCamara.setPixmap(QPixmap("pictures/placeholder.png").scaled(440, 440,
                                                                    Qt.AspectRatioMode.KeepAspectRatio,
                                                                    Qt.TransformationMode.SmoothTransformation))
        self.labelCamara.setStyleSheet("""
                    background: black;
                    border-radius:20px;
                """)

        visionLayout.addWidget(self.labelCamara)

        self.vision_worker = None
        self.contador_postura = ContadorPostura()

        #self.activar_vision()




        layoutSuperior.addWidget(frameDetect, stretch=5)
        layoutSuperior.addSpacing(15)
        layoutSuperior.addWidget(frameVision, stretch=6)

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

        self.scrollTareas = QScrollArea()
        self.contenidoScroll = QWidget()
        self.contenidoLayout = QVBoxLayout(self.contenidoScroll)

        self.contenidoLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scrollTareas.setStyleSheet('''
        QScrollArea {
    border: none;
    background: transparent;
}

QScrollArea > QWidget > QWidget {
    background: #1f1f1f;
    border-radius: 15px;
}

    QScrollBar:vertical {
        width: 0px;
    }

    QScrollBar:horizontal {
        height: 0px;
    }
        ''')

        self.listaTareas = []



        self.targetas1 = tareaTarget(texto="tarea 1")
        self.targetas2 = tareaTarget(texto="tarea 2")
        self.targetas3 = tareaTarget(texto="tarea 3")

        self.listaTareas.append(self.targetas1)
        self.listaTareas.append(self.targetas2)
        self.listaTareas.append(self.targetas3)



        self.contenidoLayout.addWidget(self.targetas1)
        self.contenidoLayout.addWidget(self.targetas2)
        self.contenidoLayout.addWidget(self.targetas3)

        self.targetas1.estadoCambiado.connect(self.cambioCheckout)
        self.targetas1.solicitudEliminar.connect(self.eleminarFrameTarea)
        self.targetas2.estadoCambiado.connect(self.cambioCheckout)
        self.targetas2.solicitudEliminar.connect(self.eleminarFrameTarea)
        self.targetas3.estadoCambiado.connect(self.cambioCheckout)
        self.targetas3.solicitudEliminar.connect(self.eleminarFrameTarea)





        self.scrollTareas.setWidget(self.contenidoScroll)
        self.scrollTareas.setWidgetResizable(True)



        botonTareaWidget = QWidget()
        layoutBotones = QHBoxLayout(botonTareaWidget)
        layoutBotones.addSpacing(22)
        layoutBotones.setContentsMargins(15, 5, 19, 5)

        self.buttonAgregar = QPushButton("Agregar")
        self.buttonAgregar.setStyleSheet(botonAgregar)
        self.buttonMarcar = QPushButton("Eliminar Completadas")
        self.buttonMarcar.setStyleSheet(botonCompletar)
        layoutBotones.addWidget(self.buttonAgregar, stretch= 2)
        layoutBotones.addWidget(self.buttonMarcar, stretch= 3)

        self.buttonAgregar.clicked.connect(self.accionAgregarTarea)
        self.buttonMarcar.clicked.connect(self.accioneLimpiarCompletas)

        layoutTimer.addWidget(tareaTxt)
        layoutTimer.addWidget(self.scrollTareas)
        layoutTimer.addWidget(botonTareaWidget)



        frame_prefs = QFrame()
        layoutPomodoro = QVBoxLayout(frame_prefs)

        self.progressTime = WidgetCirculo()
        self.progressTime.finished.connect(self.pomodoroTerminado)
        self.progressTime.cambioFase.connect(self.al_cambiar_fase)

        widgetStart = QWidget()
        layoutStart = QHBoxLayout(widgetStart)

        self.estatatusModo = QLabel()
        self.estatatusModo.setText("Trabajando")
        self.estatatusModo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.estatatusModo.setStyleSheet(modo1)

        shadowL2 = QGraphicsDropShadowEffect()
        shadowL2.setBlurRadius(30)  # Qué tan difuminada
        shadowL2.setOffset(0, 6)  # x, y
        shadowL2.setColor(QColor(0, 0, 0, 120))
        self.estatatusModo.setGraphicsEffect(shadowL2)
        self.estatatusModo.graphicsEffect()

        self.timerPausado = True
        self.modoTrabajo= True

        self.buttonStart = QPushButton()
        self.buttonStart.setIcon(QIcon("pictures/play.svg"))
        self.buttonStart.setIconSize(QSize(21, 21))
        self.buttonStart.setStyleSheet(botonSecion)
        #self.buttonStart.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.buttonStart.clicked.connect(self.accionBotonPomodoro)

        self.buttonRefresh = QPushButton()
        self.buttonRefresh.setIcon(QIcon("pictures/refresh.svg"))
        self.buttonRefresh.setIconSize(QSize(21, 21))
        self.buttonRefresh.setStyleSheet(botonSecion)
        #self.buttonRefresh.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.buttonRefresh.clicked.connect(self.accionBotonRefresh)
        self.buttonRefresh.setEnabled(False)



        layoutStart.addWidget(self.estatatusModo, stretch= 3)
        layoutStart.addWidget(self.buttonStart, stretch= 1)
        layoutStart.addWidget(self.buttonRefresh, stretch= 1)

        SelectModeBar = QWidget()
        layoutSelect = QHBoxLayout(SelectModeBar)


        self.buttonMode = QPushButton(self)
        self.buttonMode.setIcon(QIcon("pictures/menu.svg"))
        self.buttonMode.setIconSize(QSize(19, 19))
        self.buttonMode.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.buttonMode.setStyleSheet('''
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


        shadowL1 = QGraphicsDropShadowEffect()
        shadowL1.setBlurRadius(30)  # Qué tan difuminada
        shadowL1.setOffset(0, 6)  # x, y
        shadowL1.setColor(QColor(0, 0, 0, 120))
        self.modoTxt.setGraphicsEffect(shadowL1)
        self.modoTxt.graphicsEffect()


        self.selecMenu = QMenu(self)
        self.accionPomodoro = self.selecMenu.addAction("Recomendación 1")
        self.accionEnfoque = self.selecMenu.addAction("Recomendación 2")

        self.separador = self.selecMenu.addSeparator()
        self.accionAgregar = self.selecMenu.addAction("Agregar")

        self.listaSets = []
        self.listaSets.append(self.accionPomodoro)
        self.listaSets.append(self.accionEnfoque)
        self.listaSets.append(self.accionAgregar)

        self.accionPomodoro.triggered.connect(lambda :self.selectorTiempo("Recomendacion 1", 50, 25))
        self.accionEnfoque.triggered.connect(lambda : self.selectorTiempo("Recomendacion 2", 40, 20))
        self.accionAgregar.triggered.connect(self.agregarSetTiempos)



        self.selecMenu.setStyleSheet("""
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
        self.buttonMode.setMenu(self.selecMenu)
        self.buttonMode.show()

        self.ShowTimeWork = QFrame(self)




        layoutSelect.addWidget(self.modoTxt, stretch= 4)
        layoutSelect.addWidget(self.buttonMode, stretch= 1)

        layoutPomodoro.addStretch()
        layoutPomodoro.addWidget(self.progressTime)
        layoutPomodoro.addStretch()
        layoutPomodoro.addWidget(widgetStart)

        layoutPomodoro.addWidget(SelectModeBar)


        bottom_layout.addWidget(frame_timer, stretch=3)
        bottom_layout.addWidget(frame_prefs, stretch=2)

        right_layout.addWidget(frame_status, stretch=50)
        right_layout.addWidget(bottom_widget, stretch=50)

        self._cambiar_estado(EstadoApp.INACTIVO)


    def txtPomodoro(self):
        self.progressTime.set_tiempos(30,15)
        self.modoTxt.setText("Pomodoro Mode")
        self.buttonStart.setIcon(QIcon("pictures/play.svg"))
        self.buttonStart.setIconSize(QSize(21, 21))
        self.buttonRefresh.setEnabled(True)

    def txtEnfoque(self):
        self.progressTime.set_tiempos(20, 15)
        self.modoTxt.setText("Enfoque Mode")
        self.buttonStart.setIcon(QIcon("pictures/play.svg"))
        self.buttonStart.setIconSize(QSize(21, 21))
        self.buttonRefresh.setEnabled(True)

    def txtPredeterminado(self):
        self.progressTime.set_tiempos(15, 10)
        self.modoTxt.setText("Predeterminado Mode")
        self.buttonStart.setIcon(QIcon("pictures/play.svg"))
        self.buttonStart.setIconSize(QSize(21, 21))
        self.buttonRefresh.setEnabled(True)

    def selectorTiempo(self, etiqueta : str,  minTrabajo : int, minDescanso : int):
        self.progressTime.set_tiempos(minTrabajo, minDescanso)
        self.modoTxt.setText(etiqueta)
        self.buttonStart.setIcon(QIcon("pictures/play.svg"))
        self.buttonStart.setIconSize(QSize(21, 21))
        self.buttonRefresh.setEnabled(True)

    def accionBotonPomodoro(self):
        if self.progressTime.runningTime():
            self.progressTime.pausar()
            self.buttonRefresh.setEnabled(True)
            self.buttonStart.setIcon(QIcon("pictures/play.svg"))
            self.buttonStart.setIconSize(QSize(21, 21))

            self.timerPausado = True

            self.actualizar_estado_vision()


        else:
            self.progressTime.iniciar()
            self.buttonRefresh.setEnabled(False)
            self.buttonStart.setIcon(QIcon("pictures/stop.svg"))
            self.buttonStart.setIconSize(QSize(21, 21))


            self.timerPausado = False
            self.actualizar_estado_vision()

    def accionBotonRefresh(self):
        self.progressTime.reiniciar()

    def pomodoroTerminado(self):

        self.ciclosTerminados += 1

    def al_cambiar_fase(self, working):
        if working:
            self.estatatusModo.setText("Trabajando")
            self.modoTrabajo = True

        else:
            self.estatatusModo.setText("Descansando")
            self.modoTrabajo = False

        self.actualizar_estado_vision()

    def agregarSetTiempos(self):
        dialogoNuevoTiempos = dialogNewTime(self)
        if dialogoNuevoTiempos.exec():

            nombreset = dialogoNuevoTiempos.nombreSet
            segTrabajo = dialogoNuevoTiempos.setTrabajo
            segDescanso = dialogoNuevoTiempos.setDescanso



            newSet = QAction(nombreset, self)
            self.selecMenu.insertAction(self.separador, newSet)

            newSet.triggered.connect(lambda: self.selectorTiempo(dialogoNuevoTiempos.nombreSet, segTrabajo, segDescanso))

            self.listaSets.append(newSet)
            for i in self.listaSets:
                print(i)

    def _cambiar_estado(self, nuevo_estado: EstadoApp):
        self._estado_app = nuevo_estado
        print(f"Estado cambiado a: {nuevo_estado}")

        if nuevo_estado == EstadoApp.EN_SESION:
            self._sesion_fecha_inicio = datetime.now()

        self.buttonStart.setEnabled(nuevo_estado != EstadoApp.INACTIVO)
        self.buttonRefresh.setEnabled(nuevo_estado != EstadoApp.INACTIVO)
        self.botonPrueba.setEnabled(nuevo_estado != EstadoApp.EN_SESION)

    def cambioCheckout(self, targeta, completado):
        print(f"Tarea : {targeta.trabajoLabel.text()}, Completada : {completado}")

        if completado and targeta.id_tarea in self._sesion_pendientes:
            self._sesion_pendientes.discard(targeta.id_tarea)
            if not self._sesion_pendientes and self._estado_app == EstadoApp.EN_SESION:
                self._on_sesion_completado()




    def accionAgregarTarea(self):
        dialogNewTarea = dialogoNuevaTarea(self)

        if dialogNewTarea.exec():
            targetas = tareaTarget(texto= dialogNewTarea.texto_resultado)
            self.contenidoLayout.addWidget(targetas)
            targetas.estadoCambiado.connect(self.cambioCheckout)
            self.listaTareas.append(targetas)
            targetas.solicitudEliminar.connect(self.eleminarFrameTarea)

    def eleminarFrameTarea(self, targeta):
        self.contenidoLayout.removeWidget(targeta)
        self.listaTareas.remove(targeta)

        if targeta.id_tarea in self._sesion_pendientes:
            self._sesion_pendientes.discard(targeta.id_tarea)
            if not self._sesion_pendientes and self._estado_app == EstadoApp.EN_SESION:
                self._on_sesion_completado()

        targeta.deleteLater()
        print(targeta.trabajoLabel.text(), " ah sido elimidado")

    def accioneLimpiarCompletas(self):

        tareas_a_eliminar = [t for t in self.listaTareas if t.completada]


        if tareas_a_eliminar:
            for tarjeta in tareas_a_eliminar:
                self.eleminarFrameTarea(tarjeta)

        else:
            print("Sin Tareas terminadas")

    def _actualizar_camara(self, qimg):
        self.labelCamara.setPixmap(
            QPixmap.fromImage(qimg).scaled(
                self.labelCamara.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

    def _actualizar_pill(self, estado):
        colores = {
            "CORRECTA": "#4CAF50",
            "INCORRECTA": "#E53935",
            "ALERTA": "#FF6F00",
            "SIN_DETECCION": "#9E9E9E",
        }
        color = colores.get(estado, "#9E9E9E")
        self.estatusTxt.setText(estado)
        self.estatusTxt.setStyleSheet(f"""
            background:{color};
            color:white;
            border-radius:20px;
            font-size:25px;
            font-weight:bold;
        """)
        #self.procesar_estado(estado)




    def activar_vision(self):
        if self.vision_worker is not None:
            return

        visonAdapter.iniciar_vision()
        self.vision_worker = VisionWorker()
        self.vision_worker.frame_ready.connect(self._actualizar_camara)
        self.vision_worker.estado_actualizado.connect(self.procesar_estado)
        self.vision_worker.start()
        self.buttonMode.setEnabled(False)

    def desactivar_camara(self):
        if self.vision_worker is None:
            return
        self.vision_worker.stop()
        self.vision_worker = None
        self.contador_postura._ultimo_tiemestamp =None
        self.buttonMode.setEnabled(True)

        self.mostrar_placeholder_camera()

    def procesar_estado(self, estado):
        #actualizare el pill
        self._actualizar_pill(estado)


        #alimentar el contador
        self.contador_postura.registrar_estado(estado)

        #tomar resumen y actualizar labels
        resumen = self.contador_postura.obtener_resumen()
        self.actualizarLabelsContador(resumen)

        if estado == "ALERTA" and self._estado_anterior != "ALERTA":
            self._sonido_alerta.play()

        elif estado != "ALERTA" and self._estado_anterior == "ALERTA":
            self._sonido_alerta.stop()



        if estado == "SIN_DETECCION" and self._estado_anterior != "SIN_DETECCION":
            self._sonido_ausencia.play()
        elif estado != "SIN_DETECCION" and self._estado_anterior == "SIN_DETECCION":
            self._sonido_ausencia.stop()


        self._estado_anterior = estado



    def actualizarLabelsContador(self, resumen):
        self.postureGoodTxt2.setText(self.formaterTime(resumen["tiempo_correcta"]))
        self.postureBadTxt2.setText(self.formaterTime(resumen["tiempo_incorrecta"]))
        self.rachaTxt2.setText(self.formaterTime(resumen["racha_actual"]))
        self.recordTxt2.setText(self.formaterTime(resumen["racha_maxima"]))



    def formaterTime(self, time):

        minutesRemaining = int(time//60)
        secondsRemaining = int(time % 60)
        return f"{minutesRemaining}:{secondsRemaining:02d}"

    def toggle_button_camara(self, checked): #boton prendido/apagado MODULO VISION
        if checked:
            self.activar_vision()
        else:
            self.desactivar_camara()



    def mostrar_placeholder_camera(self):
        self.labelCamara.setPixmap(QPixmap("pictures/placeholder.png").scaled(440, 440,
                                                                              Qt.AspectRatioMode.KeepAspectRatio,
                                                                              Qt.TransformationMode.SmoothTransformation))
        self.estatusTxt.setText("Esperando...")
        self.estatusTxt.setStyleSheet("""
                    background:#555;
                    color:white;
                    border-radius:20px;
                    font-size:25px;
                    font-weight:bold;
                    """)
        self._sonido_ausencia.stop()
        self._sonido_alerta.stop()

    def actualizar_estado_vision(self):
        debePrender = (self.modoTrabajo == True) and not self.timerPausado

        if debePrender and self.vision_worker is None:
            self.activar_vision()
            print("Vision Activa")
        elif not debePrender and self.vision_worker is not None:
            self.desactivar_camara()
            print("Vision Desactivada")

    def obtener_tareas_pendientes(self) -> list[tuple[int, str]]:
        return [(t.id_tarea, t.trabajoLabel.text()) for t in self.listaTareas if not t.completada]


    def iniciar_sesion(self, ids_seleccionados: list[int]):
        self._sesion_pendientes = set(ids_seleccionados)

        for tarjeta in self.listaTareas:
            if tarjeta.id_tarea in self._sesion_pendientes:
                tarjeta.marcar_en_sesion(True)

    def _on_sesion_completado(self):
        print("sesion completa, terminar monitoreo")
        self.desactivar_camara()
        self.accionBotonRefresh()


        for tarjeta in self.listaTareas:
            tarjeta.marcar_en_sesion(False)

        self._sesion_pendientes.clear()
        self._cambiar_estado(EstadoApp.INACTIVO)


    def on_start_clicked(self):
        pendientes = self.obtener_tareas_pendientes()
        dialogo = dialogSelectTask(pendientes, parent=self)
        if dialogo.exec_() != QDialog.Accepted:
            print("seccion cancelada")
            return

        if dialogo.sinAsignaciones:
            ids_seleccionados = []
            print("continuar sin asignaciones")
        else:
            ids_seleccionados = dialogo.tareas_seleccionadas()
            print(f"inicio de seccion{ids_seleccionados}")

        if self._estado_app == EstadoApp.INACTIVO:
            #self.activar_vision()
            print("se prende vision")
            if ids_seleccionados:
                self.iniciar_sesion(ids_seleccionados)
                self._cambiar_estado(EstadoApp.EN_SESION)
            else:
                self._cambiar_estado(EstadoApp.LIBRE)

        elif self._estado_app == EstadoApp.LIBRE:
            if ids_seleccionados:
                self.iniciar_sesion(ids_seleccionados)
                self._cambiar_estado(EstadoApp.EN_SESION)
                #por si elige "sin asignaciones" estando ya libre no hay cambio

        self.iniciar_sesion(ids_seleccionados)









