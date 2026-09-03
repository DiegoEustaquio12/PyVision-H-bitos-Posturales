from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel, QHBoxLayout

from IU.Ventanas.sessionStats import ResumenSesion
from IU.estilosProject import *
from datetime import date, datetime

from IU.Ventanas.dataEstaditicas.Datapruba import generar_sesiones_prueba
from IU.Ventanas.dataEstaditicas.headmap import HeatmapActividad
from IU.Ventanas.dataEstaditicas.DonutWidget import DonutPostura
from IU.Ventanas.dataEstaditicas.tendenciaWidget import TendenciaWidget
from PySide6.QtCore import QTimer



class WidEstadisticas(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setStyleSheet(estadisticas)
        self._construir_ui()


    def _construir_ui(self) -> None:

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(24, 24, 24, 24)
        layout_principal.setSpacing(20)

        # --- Título ---
        titulo = QLabel("Estadísticas", objectName = "Titulo")


        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(titulo, stretch=6)

        # --- Heatmap (ancho completo) ---
        hoy = datetime.now().date()
        dias_transcurridos = (hoy - date(hoy.year, 1, 1)).days + 1
        sesiones_prueba = generar_sesiones_prueba(dias_atras=dias_transcurridos)
        self.heatmap = HeatmapActividad(sesiones_prueba, anio=hoy.year)


        layout_principal.addWidget(self.heatmap, stretch= 40)

        # --- Fila inferior: Dona | Línea 14 días ---
        fila_inferior = QHBoxLayout()
        fila_inferior.setSpacing(20)

        self.dona_placeholder = DonutPostura(sesiones_prueba)
        self.setObjectName("Widgets")
        self._contador_postura = None
        self._timer_dona = QTimer(self)
        self._timer_dona.setInterval(1000)  # se actualiza cada segundo
        self._timer_dona.timeout.connect(self._actualizar_dona_en_vivo)
        self._timer_dona.start()

        self.linea_placeholder = TendenciaWidget(sesiones_prueba)

        # Proporción 35 / 65 vía stretch factors
        fila_inferior.addWidget(self.dona_placeholder, 35)
        fila_inferior.addWidget(self.linea_placeholder, 65)

        layout_principal.addLayout(fila_inferior, stretch=55)

        self.setLayout(layout_principal)

    def set_contador_postura(self, contador):
        self._contador_postura = contador

    def _actualizar_dona_en_vivo(self):
        if self._contador_postura is None:
            return
        r = self._contador_postura.obtener_resumen()
        ahora = datetime.now()
        resumen = ResumenSesion(
            fecha_inicio=ahora,
            fecha_fin=ahora,
            duracion_segundos=0,
            minutos_buena_postura=r["tiempo_correcta"],  # ojo: van en SEGUNDOS, no minutos
            minutos_mala_postura=r["tiempo_incorrecta"],  # el nombre del campo no importa, es solo proporción
        )
        self.dona_placeholder.set_sesiones([resumen])