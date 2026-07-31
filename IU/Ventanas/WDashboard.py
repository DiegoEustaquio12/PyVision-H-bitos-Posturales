from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QPushButton, QMenu, \
    QSizePolicy, QComboBox, QDialog
from IU.estilosProject import *
from IU.Ventanas.Widgets.BarProgressCircle import WidgetCirculo
from IU.Ventanas.Widgets.targetaTarea import tareaTarget
from IU.Ventanas.Widgets.dialogoTarea import dialogoNuevaTarea
from IU.Ventanas.Widgets.structureTime import ContadorPostura

from IU.GUI.visionWorker1 import VisionWorker
from IU.GUI import visonAdapter
import time

import os
from PySide6.QtMultimedia import QSoundEffect



class WidDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.ciclosTerminados = 0

        self._sonido_alerta = QSoundEffect()
        base_path = os.path.dirname(os.path.abspath(__file__))
        ruta_wav = os.path.normpath(os.path.join(base_path, "..", "sounds", "errorSound.wav"))
        self._sonido_alerta.setSource(QUrl.fromLocalFile(ruta_wav))
        self._sonido_alerta.setLoopCount(-2)
        self._sonido_alerta.setVolume(1)

        self._estado_anterior = None

        self._sonido_ausencia = QSoundEffect()
        base_path_deteccion = os.path.dirname(os.path.abspath(__file__))
        ruta_wav_2 = os.path.normpath(os.path.join(base_path_deteccion, "..", "sounds", "sinDeteccion2.wav"))
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
        layoutSuperior.setContentsMargins(5, 5, 5, 5)
        layoutSuperior.setSpacing(10)

        frameDetect = QFrame(objectName = "frameInterno")
        layoutDetect = QVBoxLayout(frameDetect)
        layoutDetect.setContentsMargins(12, 15, 25, 10)

        self.estatusTxt = QLabel()
        self.estatusTxt.setText("Esperando...")
        self.estatusTxt.setFixedHeight(45)
        self.estatusTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.estatusTxt.setStyleSheet("""
            background:#555;
            color:white;
            border-radius:15px;
            font-size:20px;
            font-weight:bold;
            """
            )


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
        border: 1px solid rgba(255,255,255,80);
        border-radius:20px;
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

        linea3 = QFrame()
        linea3.setFrameShape(QFrame.Shape.VLine)
        linea3.setFrameShadow(QFrame.Shadow.Sunken)
        linea3.setFixedWidth(1)
        linea3.setStyleSheet("""
                 QFrame{
                     background-color: #b4b4b4;
                     border-color: transparent;
                 }
                 """)

        postureGoodTxt1 = QLabel()
        postureGoodTxt1.setText("Buena Postura")
        postureGoodTxt1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        postureGoodTxt1.setStyleSheet(contador1)


        self.postureGoodTxt2 = QLabel()
        self.postureGoodTxt2.setText("0:00")
        self.postureGoodTxt2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.postureGoodTxt2.setStyleSheet(contador1)


        layoutFrame1.addWidget(postureGoodTxt1)
        layoutFrame1.addWidget(linea)
        layoutFrame1.addWidget(self.postureGoodTxt2)


        postureBadTxt1 = QLabel()
        postureBadTxt1.setText("Mala Postura")
        postureBadTxt1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        postureBadTxt1.setStyleSheet(contador2)

        self.postureBadTxt2 = QLabel()
        self.postureBadTxt2.setText("0:00")
        self.postureBadTxt2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.postureBadTxt2.setStyleSheet(contador2)

        layoutFrame2.addWidget(postureBadTxt1)
        layoutFrame2.addWidget(linea2)
        layoutFrame2.addWidget(self.postureBadTxt2)

        layoutTiempos.addWidget(frameTiempo1)
        layoutTiempos.addWidget(frameTiempo2)

        frameRacha = QFrame()
        layoutRachaa = QHBoxLayout(frameRacha)

        frameRacha.setStyleSheet('''
                QFrame{
                background-color: #black;
                border: 1px solid rgba(255,255,255,80);
                border-radius:20px;
                }
                ''')

        rachaTxt = QLabel()
        rachaTxt.setText("Racha")
        rachaTxt.setStyleSheet(contador1)
        rachaTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #rachaTxt.setFixedWidth(300)


        self.rachaTxt2 = QLabel()
        self.rachaTxt2.setText("0:00")
        self.rachaTxt2.setStyleSheet(contador1)
        self.rachaTxt2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layoutRachaa.addWidget(rachaTxt)
        layoutRachaa.addWidget(linea3)
        layoutRachaa.addWidget(self.rachaTxt2)


        timeSeccionTxt = QLabel()
        timeSeccionTxt.setText("Primera fase")
        timeSeccionTxt.setAlignment(Qt.AlignmentFlag.AlignLeft.AlignVCenter)
        timeSeccionTxt.setStyleSheet(contador3)

        self.visionButton = QPushButton()
        self.visionButton.setText("Vision")
        self.visionButton.setIcon(QIcon("pictures/play.svg"))
        self.visionButton.setCheckable(True)
        self.visionButton.toggled.connect(self.toggle_button_camara)







        layoutDetect.addWidget(self.estatusTxt, alignment= Qt.AlignmentFlag.AlignTop)
        layoutDetect.addSpacing(4)
        layoutDetect.addWidget(widgetTiempos)
        layoutDetect.addSpacing(4)
        layoutDetect.addWidget(frameRacha)
        layoutDetect.addStretch()
        layoutDetect.addWidget(timeSeccionTxt)
        layoutDetect.addWidget(self.visionButton, alignment= Qt.AlignmentFlag.AlignLeft)



        frameVision = QFrame()
        frameVision.setStyleSheet("""
        QFrame{
        border-color: transparent;
        }
        """)
        visionLayout = QVBoxLayout(frameVision)

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

        self.buttonAgregar = QPushButton("Agregar")
        self.buttonAgregar.setStyleSheet('''
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
        self.buttonMarcar = QPushButton("Eliminar Completadas")
        self.buttonMarcar.setStyleSheet('''
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

        self.buttonStart = QPushButton()
        self.buttonStart.setIcon(QIcon("pictures/play.svg"))
        self.buttonStart.setIconSize(QSize(21, 21))
        #self.buttonStart.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.buttonStart.clicked.connect(self.accionBotonPomodoro)

        self.buttonRefresh = QPushButton()
        self.buttonRefresh.setIcon(QIcon("pictures/refresh.svg"))
        self.buttonRefresh.setIconSize(QSize(21, 21))
        self.buttonRefresh.setStyleSheet('''
        QPushButton::disabled {
        background-color: black;
        }
        
        ''')
        #self.buttonRefresh.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.buttonRefresh.clicked.connect(self.accionBotonRefresh)
        self.buttonRefresh.setEnabled(False)



        layoutStart.addWidget(self.estatatusModo, stretch= 3)
        layoutStart.addWidget(self.buttonStart, stretch= 1)
        layoutStart.addWidget(self.buttonRefresh, stretch= 1)

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
        layoutPomodoro.addWidget(self.progressTime, stretch= 4)
        layoutPomodoro.addStretch()
        layoutPomodoro.addWidget(widgetStart, stretch= 1)

        layoutPomodoro.addWidget(SelectModeBar, stretch= 1)


        bottom_layout.addWidget(frame_timer, stretch=3)
        bottom_layout.addWidget(frame_prefs, stretch=2)

        right_layout.addWidget(frame_status, stretch=50)
        right_layout.addWidget(bottom_widget, stretch=50)


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

    def accionBotonPomodoro(self):
        if self.progressTime.runningTime():
            self.progressTime.pausar()
            self.buttonRefresh.setEnabled(True)
            self.buttonStart.setIcon(QIcon("pictures/play.svg"))
            self.buttonStart.setIconSize(QSize(21, 21))
        else:
            self.progressTime.iniciar()
            self.buttonRefresh.setEnabled(False)
            self.buttonStart.setIcon(QIcon("pictures/stop.svg"))
            self.buttonStart.setIconSize(QSize(21, 21))

    def accionBotonRefresh(self):
        self.progressTime.reiniciar()

    def pomodoroTerminado(self):

        self.ciclosTerminados += 1

    def al_cambiar_fase(self, working):
        if working:
            self.estatatusModo.setText("Trabajando")
            #self.activar_vision()
        else:
            self.estatatusModo.setText("Descansando")
            #self.desactivar_camara()

    def cambioCheckout(self, targeta, completado):
        print(f"Tarea : {targeta.trabajoLabel.text()}, Completada : {completado}")

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
        targeta.deleteLater()
        print(targeta.trabajoLabel.text(), " ah sido elimidado")

    def accioneLimpiarCompletas(self):

        tareas_a_eliminar = [t for t in self.listaTareas if t.completada]

        if tareas_a_eliminar:
            for tarjeta in tareas_a_eliminar:
                self.contenidoLayout.removeWidget(tarjeta)
                self.listaTareas.remove(tarjeta)
                tarjeta.deleteLater()
            for tarjeta in tareas_a_eliminar:
                print(tarjeta)

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
            font-size:18px;
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

    def desactivar_camara(self):
        if self.vision_worker is None:
            return
        self.vision_worker.stop()
        self.vision_worker = None
        self.contador_postura._ultimo_tiemestamp =None

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



    def formaterTime(self, time):

        minutesRemaining = int(time//60)
        secondsRemaining = int(time % 60)
        return f"{minutesRemaining}:{secondsRemaining:02d}"

    def toggle_button_camara(self, checked): #boton prendido/apagado MODULO VISION
        if checked:
            self.activar_vision()
        else:
            self.desactivar_camara()

    def closeEvent(self, event):
        self.desactivar_camara()
        event.accept()


    def mostrar_placeholder_camera(self):
        self.labelCamara.setPixmap(QPixmap("pictures/placeholder.png").scaled(440, 440,
                                                                              Qt.AspectRatioMode.KeepAspectRatio,
                                                                              Qt.TransformationMode.SmoothTransformation))
        self.estatusTxt.setText("Esperando...")
        self.estatusTxt.setStyleSheet("""
                    background:#555;
                    color:white;
                    border-radius:20px;
                    font-size:18px;
                    font-weight:bold;
                    """)
        self._sonido_ausencia.stop()
        self._sonido_alerta.stop()



