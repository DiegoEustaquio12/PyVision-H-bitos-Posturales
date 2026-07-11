import time

class ContadorPostura:
    def __init__(self):
        self.tiempo_correcta = 0.0
        self.tiempo_incorrecta = 0.0
        self.racha_actual = 0.0
        self.racha_maxima = 0.0
        self._ultimo_tiemestamp = None

    def registrar_estado(self, estado_postura):
        ahora = time.time()

        if self._ultimo_tiemestamp is None:
            self._ultimo_tiemestamp = ahora
            return

        delta = ahora - self._ultimo_tiemestamp
        self._ultimo_tiemestamp = ahora

        if estado_postura == "CORRECTA":
            self.tiempo_correcta += delta
            self.racha_actual += delta
            if self.racha_actual > self.racha_maxima:
                self.racha_maxima = self.racha_actual

        elif estado_postura == "INCORRECTA":
            self.tiempo_incorrecta += delta

        elif estado_postura == "ALERTA":
            self.tiempo_incorrecta += delta
            self.racha_actual = 0.0

        elif estado_postura == "SIN_DETECCION":
            self.racha_actual = 0.0

    def obtener_resumen(self):
        return {
            "tiempo_correcta": self.tiempo_correcta,
            "tiempo_incorrecta": self.tiempo_incorrecta,
            "racha_actual": self.racha_actual,
            "racha_maxima": self.racha_maxima,
        }

    def reiniciar(self):
        self.tiempo_correcta = 0.0
        self.tiempo_incorrecta = 0.0
        self.racha_actual = 0.0
        self.racha_maxima = 0.0
        self._ultimo_tiemestamp = None