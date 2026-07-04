import cv2
import numpy as np
import time







_cap = cv2.VideoCapture(0)

def obtener_estado_postura():
    ret, frame = _cap.read()
    if not ret:
        return None

    estado = "CORRECTA"
    return {
        "frame": frame,
        "estado_postura": estado,
        "timestamp": time.time(),
    }

def liberar_camara():
    _cap.release()