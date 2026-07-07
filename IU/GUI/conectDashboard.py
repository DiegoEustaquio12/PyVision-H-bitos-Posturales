import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from visionWorker1 import VisionWorker
import visonAdapter
import time


class Ventana(QWidget):
    def __init__(self):
        super().__init__()

        visonAdapter.iniciar_vision()


        self.setWindowTitle("Prueba VisionWorker")
        self.resize(900, 700)

        # ==========================
        # Frame principal
        # ==========================
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame{
                background:#2b2d31;
                border-radius:12px;
            }
        """)

        layout_frame = QVBoxLayout(frame)

        # Label donde irá la cámara
        self.label_camara = QLabel()
        self.label_camara.setFixedSize(800, 500)
        self.label_camara.setAlignment(Qt.AlignCenter)
        self.label_camara.setStyleSheet("""
            background: transparent;
            border-radius:20px;
        """)

        # Pill del estado
        self.pill_estado = QLabel("Esperando...")
        self.pill_estado.setAlignment(Qt.AlignCenter)
        self.pill_estado.setFixedHeight(40)
        self.pill_estado.setStyleSheet("""
            background:#555;
            color:white;
            border-radius:20px;
            font-size:18px;
            font-weight:bold;
        """)

        layout_frame.addWidget(self.label_camara)
        layout_frame.addWidget(self.pill_estado)

        layout = QVBoxLayout(self)
        layout.addWidget(frame)

        # ==========================
        # Vision Worker
        # ==========================

        self.vision_worker = VisionWorker()
        self.vision_worker.frame_ready.connect(self._actualizar_camara)
        self.vision_worker.estado_actualizado.connect(self._actualizar_pill)
        self.vision_worker.start()

    # ==========================
    # Slots
    # ==========================
    def _actualizar_camara(self, qimg):
        self.label_camara.setPixmap(
            QPixmap.fromImage(qimg).scaled(
                self.label_camara.size(),
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
        self.pill_estado.setText(estado)
        self.pill_estado.setStyleSheet(f"""
            background:{color};
            color:white;
            border-radius:20px;
            font-size:18px;
            font-weight:bold;
        """)

    def closeEvent(self, event):
        self.vision_worker.stop()
        time.sleep(0.3)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana = Ventana()
    ventana.show()

    sys.exit(app.exec())