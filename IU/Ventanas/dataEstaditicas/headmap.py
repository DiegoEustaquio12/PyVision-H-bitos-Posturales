"""
Fase 2: Heatmap de actividad estilo GitHub, dibujado con QPainter puro.

Recibe una lista de ResumenSesion y no sabe nada de SQLite ni de cómo se
obtuvieron esos datos - solo pinta. Cuando Rodrigo conecte stats_adapter.py,
este widget no cambia: solo cambia quién le pasa la lista de sesiones.

Convención de la grilla:
    - Muestra el AÑO COMPLETO de forma estática (1 ene - 31 dic del año
      indicado). No se desplaza con el tiempo por ahora.
    - Columnas = semanas (izquierda = enero, derecha = diciembre)
    - Filas = días de la semana, Lunes arriba -> Domingo abajo
    - Intensidad de color = minutos totales de sesión ese día (5 niveles)
    - Días futuros (después de hoy) se pintan en gris neutro, distinto
      del gris de "día pasado sin actividad", para que la grilla se vea
      completa todo el año.
"""

import sys
from datetime import date, datetime, timedelta

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPaintEvent
from PySide6.QtWidgets import QApplication, QToolTip, QVBoxLayout, QWidget

DIAS_SEMANA_ES = ["L", "A", "M", "J", "V", "S", "D"]  # Lunes -> Domingo

MESES_ES = [
    "Ene", "Feb", "Mar", "Abr", "May", "Jun",
    "Jul", "Ago", "Sep", "Oct", "Nov", "Dic",
]

# Escala de verdes tipo GitHub. Índice 0 = día pasado sin actividad.
NIVELES_COLOR = [
    QColor("#d2d2d2"),  # sin actividad (pasado)
    QColor("#c8e6c0"),  # nivel 1
    QColor("#8fd18a"),  # nivel 2
    QColor("#4caf50"),  # nivel 3
    QColor("#2e7d32"),  # nivel 4 (máxima actividad)
]

# Días futuros: gris neutro, claramente distinto de "sin actividad" pasado
COLOR_DIA_FUTURO = QColor("#9e9e9e")
BORDE_DIA_FUTURO = QColor("#9e9e9e")


def _agrupar_minutos_por_dia(sesiones: list) -> dict[date, int]:
    """Suma minutos totales de sesión (buena + mala postura) agrupados por día."""
    totales: dict[date, int] = {}
    for s in sesiones:
        dia = s.fecha_inicio.date()
        minutos = s.minutos_buena_postura + s.minutos_mala_postura
        totales[dia] = totales.get(dia, 0) + minutos
    return totales


class HeatmapActividad(QWidget):
    def __init__(self, sesiones: list | None = None, anio: int | None = None, parent=None):
        """
        anio: año completo a mostrar (estático, 1 ene - 31 dic). Por
        defecto el año actual. Más adelante, cuando se vuelva dinámico,
        aquí se podría agregar navegación entre años.
        """
        super().__init__(parent)
        self._anio = anio or datetime.now().year
        self._minutos_por_dia: dict[date, int] = {}
        self._celdas_rect: dict[QRect, tuple[date, int, bool]] = {}  # rect -> (fecha, minutos, es_futuro)

        self.setMouseTracking(True)
        self.setMinimumHeight(180)
        self.set_sesiones(sesiones or [])

    def set_sesiones(self, sesiones: list) -> None:
        self._minutos_por_dia = _agrupar_minutos_por_dia(sesiones)
        self.update()

    # ------------------------------------------------------------------
    # Cálculo de niveles de color
    # ------------------------------------------------------------------
    def _nivel_para_minutos(self, minutos: int, maximo: int) -> int:
        if minutos <= 0 or maximo <= 0:
            return 0
        proporcion = minutos / maximo
        if proporcion <= 0.25:
            return 1
        elif proporcion <= 0.50:
            return 2
        elif proporcion <= 0.75:
            return 3
        return 4

    # ------------------------------------------------------------------
    # Pintado
    # ------------------------------------------------------------------
    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self._celdas_rect.clear()

        hoy = datetime.now().date()
        inicio_anio = date(self._anio, 1, 1)
        fin_anio = date(self._anio, 12, 31)

        # Alinear la grilla a semanas completas (Lunes -> Domingo)
        inicio_grilla = inicio_anio - timedelta(days=inicio_anio.weekday())
        fin_grilla = fin_anio + timedelta(days=(6 - fin_anio.weekday()))

        num_dias_grilla = (fin_grilla - inicio_grilla).days + 1
        num_semanas = num_dias_grilla // 7  # exacto, ya está alineado a semanas completas

        maximo_minutos = max(self._minutos_por_dia.values(), default=0)

        margen_izq = 26   # espacio para etiquetas de día L-D
        margen_arriba = 34  # espacio para año + meses

        lado_celda = 25
        espacio_celda = 3
        paso = lado_celda + espacio_celda

        ancho_disponible = self.width() - margen_izq
        alto_disponible = self.height() - margen_arriba

        ancho_necesario = num_semanas * paso
        if ancho_necesario > ancho_disponible and num_semanas > 0:
            paso = max(8, ancho_disponible // num_semanas)
            lado_celda = max(5, paso - espacio_celda)

        # --- Etiqueta de año (esquina superior izquierda) ---
        painter.setPen(QColor("#d4d4d4"))
        fuente_anio = painter.font()
        fuente_anio.setPointSize(10)
        fuente_anio.setBold(True)
        painter.setFont(fuente_anio)
        painter.drawText(
            QRect(0, 0, margen_izq + 60, 16),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            str(self._anio),
        )

        # --- Etiquetas de mes ---
        fuente = painter.font()
        fuente.setBold(False)
        fuente.setPointSize(8)
        painter.setFont(fuente)
        painter.setPen(QColor("white"))

        mes_anterior = None
        for semana in range(num_semanas):
            dia_lunes_semana = inicio_grilla + timedelta(weeks=semana)
            # Solo cuenta el mes si ese lunes cae dentro del año que mostramos
            if inicio_anio <= dia_lunes_semana <= fin_anio:
                mes_actual = MESES_ES[dia_lunes_semana.month - 1]
            else:
                mes_actual = None

            if mes_actual and mes_actual != mes_anterior:
                x = margen_izq + semana * paso
                painter.drawText(
                    QRect(x, 18, paso * 4, 16),
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                    mes_actual,
                )
                mes_anterior = mes_actual

        # --- Etiquetas de días de la semana (columna izquierda), las 7 ---
        for fila, etiqueta in enumerate(DIAS_SEMANA_ES):
            y = margen_arriba + fila * paso
            painter.drawText(
                QRect(0, y, margen_izq - 6, lado_celda),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                etiqueta,
            )

        # --- Cuadros de días: TODO el año, incluyendo futuro en gris ---
        for offset in range(num_dias_grilla):
            dia_actual = inicio_grilla + timedelta(days=offset)

            # Días de relleno fuera del año (para completar la semana) -> no se dibujan
            if dia_actual < inicio_anio or dia_actual > fin_anio:
                continue

            semana = offset // 7
            dia_semana = offset % 7  # 0=Lunes

            x = margen_izq + semana * paso
            y = margen_arriba + dia_semana * paso
            rect = QRect(x, y, lado_celda, lado_celda)

            es_futuro = dia_actual > hoy

            if es_futuro:
                painter.setPen(BORDE_DIA_FUTURO)
                painter.setBrush(COLOR_DIA_FUTURO)
                minutos = 0
            else:
                minutos = self._minutos_por_dia.get(dia_actual, 0)
                nivel = self._nivel_para_minutos(minutos, maximo_minutos)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(NIVELES_COLOR[nivel])

            painter.drawRoundedRect(rect, 3, 3)
            self._celdas_rect[rect] = (dia_actual, minutos, es_futuro)

        painter.end()

    # ------------------------------------------------------------------
    # Tooltip al pasar el mouse
    # ------------------------------------------------------------------
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = event.position().toPoint()
        for rect, (dia, minutos, es_futuro) in self._celdas_rect.items():
            if rect.contains(pos):
                fecha_es = f"{dia.day} {MESES_ES[dia.month - 1]} {dia.year}"
                if es_futuro:
                    texto = f"{fecha_es}: aún no llega"
                elif minutos:
                    texto = f"{fecha_es}: {minutos} min"
                else:
                    texto = f"{fecha_es}: sin sesiones"
                QToolTip.showText(event.globalPosition().toPoint(), texto, self)
                return
        QToolTip.hideText()

    def leaveEvent(self, event) -> None:
        QToolTip.hideText()


def main():
    from Datapruba import generar_sesiones_prueba

    app = QApplication(sys.argv)
    contenedor = QWidget()
    contenedor.setWindowTitle("Prueba - Heatmap de actividad")
    contenedor.resize(950, 240)

    layout = QVBoxLayout(contenedor)

    hoy = datetime.now().date()
    dias_transcurridos = (hoy - date(hoy.year, 1, 1)).days + 1
    sesiones = generar_sesiones_prueba(dias_atras=dias_transcurridos)

    heatmap = HeatmapActividad(sesiones, anio=hoy.year)
    layout.addWidget(heatmap)

    contenedor.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()