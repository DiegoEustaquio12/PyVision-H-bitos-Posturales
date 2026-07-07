
import vision.visionCopy as visionModule

def iniciar_vision():
    visionModule.iniciar_vision()

def obtener_estado_postura():
    datos = visionModule.obtener_datos_dashboard()
    if datos["frame"] is None:
        return None
    return {

        "frame": datos["frame"],
        "estado_postura": datos["estado_postura"],
        "timestamp": datos["tiempo_postura"]
    }

def liberar_camara():
    visionModule.detener_vision()