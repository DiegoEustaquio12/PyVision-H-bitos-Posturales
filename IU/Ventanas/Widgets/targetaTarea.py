from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QFrame


class tareaTarget(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet('''
        QFrame{
        background-color: rgba(255,255,255,40);
        border: 1px solid rgba(255,255,255,80);
        border-radius:10px;
         }
        ''')


        self.setMaximumHeight(35)
        self.tareasLayout = QHBoxLayout(self)

        self.trabajoLabel = QLabel("Trabajo")
        self.trabajoLabel.setStyleSheet('''
        font-size:12px;
        border-color: transparent;
        font-weight:bold;
        background-color: transparent;
        
        ''')
        self.checkTrabajo = QCheckBox()
        self.checkTrabajo.setStyleSheet('''
        
        QCheckBox {
                color: white;
            }
         QCheckBox::indicator {
                width: 30px;
                height: 15px;
            }
        ''')

        self.tareasLayout.addWidget(self.trabajoLabel)
        self.tareasLayout.addWidget(self.checkTrabajo, alignment= Qt.AlignmentFlag.AlignRight)



