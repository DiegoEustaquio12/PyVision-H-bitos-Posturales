from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QPushButton, QMenu, \
    QSizePolicy, QComboBox, QDialog
from IU.estilosProject import *
from IU.Ventanas.Widgets.BarProgressCircle import WidgetCirculo
from IU.Ventanas.Widgets.targetaTarea import tareaTarget
from IU.Ventanas.Widgets.dialogoTarea import dialogoNuevaTarea


class WidDashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.ciclosTerminados = 0

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

        frameRacha = QFrame()
        layoutRachaa = QHBoxLayout(frameRacha)

        rachaTxt = QLabel()
        rachaTxt.setText("Racha:          2:05 min")
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
        else:
            self.estatatusModo.setText("Descansando")

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
        self.contenidoLayout.addWidget(targeta)
        self.listaTareas.remove(targeta)
        targeta.deleteLater()
        print(targeta.trabajoLabel.text(), " ah sido elimidado")


