from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QFrame, QPushButton, QSizePolicy
from PySide6.QtGui import QIcon


class tareaTarget(QFrame):

    estadoCambiado = Signal(object, bool)
    solicitudEliminar = Signal(object)
    contador_id = 0

    def __init__(self, texto="No Asignada", id_tarea=None):
        super().__init__()

        if id_tarea is None:
            tareaTarget.contador_id += 1
            id_tarea = tareaTarget.contador_id
        self.id_tarea = id_tarea

        self.completada = False

        self.setStyleSheet('''
        QFrame{
        background-color: rgba(255,255,255,40);
        border: 1px solid rgba(255,255,255,80);
        border-radius: 14px;
        
         }
         
         QFrame::hover {
         background-color: rgba(255,255,255,60);
         }
        ''')


        self.setMaximumHeight(40)

        self.tareasLayout = QHBoxLayout(self)
        self.tareasLayout.setContentsMargins(15,3,10,3)

        self.trabajoLabel = QLabel(texto)
        self.trabajoLabel.setStyleSheet('''
        font-size:12px;
        border-color: transparent;
        font-weight:bold;
        background-color: transparent;
        
        ''')
        self.checkTrabajo = QCheckBox()


        self.iconNormal = QIcon("pictures/delete.svg")
        self.iconHover = QIcon("pictures/deleteRed.svg")


        self.deleteButton = QPushButton()
        self.deleteButton.setIcon(self.iconNormal)
        self.deleteButton.setIconSize(QSize(17, 17))
        self.deleteButton.setFixedWidth(28)
        self.deleteButton.setFixedHeight(28)
        self.deleteButton.enterEvent = lambda e: self.deleteButton.setIcon(self.iconHover)
        self.deleteButton.leaveEvent = lambda e: self.deleteButton.setIcon(self.iconNormal)

        self.deleteButton.setStyleSheet('''
        QPushButton {
        background-color: transparent;
        border: none;
        }
        QPushButton:hover {
        background-color: transparent;
        border: none;
        ''')



        self.tareasLayout.addWidget(self.trabajoLabel)
        self.tareasLayout.addStretch()
        self.tareasLayout.addWidget(self.checkTrabajo)
        self.tareasLayout.addWidget(self.deleteButton)

        self.checkTrabajo.stateChanged.connect(self._checkbox_cambiado)
        self.deleteButton.clicked.connect(self.eliminarTarea)

    def _checkbox_cambiado(self, state):
        self.completada = bool(state)
        self.estadoCambiado.emit(self, self.completada)
        self.actualizarEstilo()

    def actualizarEstilo(self):
        if self.completada:
            self.trabajoLabel.setStyleSheet('''
                    font-size:12px;
                    border-color: transparent;
                    font-weight:bold;
                    background-color: transparent;
                    color: rgba(255,255,255,120);
                    text-decoration: line-through;
                    ''')
            self.setStyleSheet('''
            QFrame{
            background-color: transparent;
            border: 1px solid rgba(255,255,255,120);
            border-color: green;
            border-radius: 14px;
            }
            ''')
        else:
            self.trabajoLabel.setStyleSheet('''
                    font-size:12px;
                    border-color: transparent;
                    font-weight:bold;
                    background-color: transparent;
                    ''')
            self.setStyleSheet('''
                    QFrame{
                    background-color: rgba(255,255,255,40);
                    border: 1px solid rgba(255,255,255,80);
                    border-radius: 14px;

                     }

                     QFrame::hover {
                     background-color: rgba(255,255,255,60);
                     border-radius: 14px;
                     }
                    ''')
    def eliminarTarea(self):
        self.solicitudEliminar.emit(self)



