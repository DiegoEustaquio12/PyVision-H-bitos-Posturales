from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout

class WidDashboard(QWidget):
    def __init__(self):
        super().__init__()

        right_layout = QVBoxLayout(self)
        right_layout.setContentsMargins(0, 0, 15, 0)
        right_layout.setSpacing(15)

        # Frame 2: Estatus + Cámara
        frame_status = QFrame()

        # Fila inferior: Frame 3 + Frame 4 lado a lado
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(10)

        frame_timer = QFrame()

        frame_prefs = QFrame()

        bottom_layout.addWidget(frame_timer, stretch=3)
        bottom_layout.addWidget(frame_prefs, stretch=2)

        right_layout.addWidget(frame_status, stretch=50)
        right_layout.addWidget(bottom_widget, stretch=50)

