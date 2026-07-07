from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage
import cv2
import visonAdapter

class VisionWorker(QThread):
    frame_ready = Signal(QImage)
    estado_actualizado = Signal(str)

    def __init__(self):
        super().__init__()
        self._running = True

    def run(self):
        while self._running:
            datos = visonAdapter.obtener_estado_postura()
            print(f"datos: {datos}")
            if datos is None:
                continue

            frame_rgb = cv2.cvtColor(datos["frame"], cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            qimg = QImage(frame_rgb.data, w, h, ch * w, QImage.Format_RGB888)

            self.frame_ready.emit(qimg.copy())  # .copy() evita corrupción de memoria
            self.estado_actualizado.emit(datos["estado_postura"])

            self.msleep(30)

    def stop(self):
        self._running = False
        self.wait()
        visonAdapter.liberar_camara()