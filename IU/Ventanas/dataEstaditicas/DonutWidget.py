"""
Fase 3: Dona de buena vs. mala postura, con QtCharts.

Muestra el desglose de un día (por defecto, el día más reciente con
datos disponibles) como una dona con dos segmentos: buena postura y
mala postura, con el porcentaje de buena postura al centro.

No sabe nada de SQLite - solo recibe una lista de ResumenSesion y pinta.
"""

import sys
from datetime import date, datetime

from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

MESES_ES = [
    "Ene", "Feb", "Mar", "Abr", "May", "Jun",
    "Jul", "Ago", "Sep", "Oct", "Nov", "Dic",
]

COLOR_BUENA = QColor("#4caf50")
COLOR_MALA = QColor("#ef5350")


def _obtener_resumen_dia(sesiones: list, fecha: date | None = None) -> tuple[date | None, int, int]:
    """
    Agrupa minutos de buena/mala postura por día y devuelve el resumen
    para `fecha`. Si no se especifica fecha (o no tiene datos), usa hoy
    si tiene datos, y si no, el día más reciente con datos disponibles.

    Devuelve (fecha_usada, minutos_buena, minutos_mala). fecha_usada es
    None si no hay ninguna sesión en absoluto.
    """
    por_dia: dict[date, tuple[int, int]] = {}
    for s in sesiones:
        dia = s.fecha_inicio.date()
        buena, mala = por_dia.get(dia, (0, 0))
        por_dia[dia] = (buena + s.minutos_buena_postura, mala + s.minutos_mala_postura)

    if not por_dia:
        return None, 0, 0

    if fecha and fecha in por_dia:
        buena, mala = por_dia[fecha]
        return fecha, buena, mala

    hoy = datetime.now().date()
    if hoy in por_dia:
        buena, mala = por_dia[hoy]
        return hoy, buena, mala

    dia_mas_reciente = max(por_dia.keys())
    buena, mala = por_dia[dia_mas_reciente]
    return dia_mas_reciente, buena, mala


class DonutPostura(QWidget):
    def __init__(self, sesiones: list | None = None, fecha: date | None = None, parent=None):
        super().__init__(parent)
        self._fecha_solicitada = fecha

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(16, 16, 16, 16)
        layout_principal.setSpacing(4)

        self.titulo_label = QLabel("Postura")
        #self.titulo_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #333;")
        layout_principal.addWidget(self.titulo_label)

        # --- Chart + overlay centrado, superpuestos con QStackedLayout ---
        contenedor_chart = QWidget()
        stack = QStackedLayout(contenedor_chart)
        stack.setStackingMode(QStackedLayout.StackingMode.StackAll)

        self.chart = QChart()
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.chart.legend().setLabelColor(QColor("white"))
        self.chart.setBackgroundVisible(False)
        self.chart.setMargins(self.chart.margins().__class__(0, 45, 0, 0))
        self.chart.layout().setContentsMargins(0, 0, 0, 0)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setStyleSheet("background: transparent;")

        overlay = QWidget()
        overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        overlay_layout = QVBoxLayout(overlay)
        overlay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overlay_layout.setSpacing(0)

        self.pct_label = QLabel("--%")
        self.pct_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pct_label.setStyleSheet("font-size: 26px; font-weight: 700; color: white; background: transparent;")

        self.pct_sub_label = QLabel("Buena Postura")
        self.pct_sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.pct_sub_label.setStyleSheet("font-size: 11px; color: #d4d4d4; background: transparent;")
        self.pct_sub_label.setStyleSheet('''
        QLabel {
        color: white;
        }
        ''')

        overlay_layout.addWidget(self.pct_label)
        overlay_layout.addWidget(self.pct_sub_label)

        stack.addWidget(self.chart_view)
        stack.addWidget(overlay)

        layout_principal.addWidget(contenedor_chart, stretch=1)

        self.set_sesiones(sesiones or [])

    def set_sesiones(self, sesiones: list, fecha: date | None = None) -> None:
        if fecha is not None:
            self._fecha_solicitada = fecha

        dia_usado, minutos_buena, minutos_mala = _obtener_resumen_dia(sesiones, self._fecha_solicitada)
        self._actualizar_chart(dia_usado, minutos_buena, minutos_mala)

    def _actualizar_chart(self, dia: date | None, minutos_buena: int, minutos_mala: int) -> None:
        self.chart.removeAllSeries()

        total = minutos_buena + minutos_mala

        if dia is None or total == 0:
            self.titulo_label.setText("Postura - sin datos")
            self.pct_label.setText("--%")
            self.pct_sub_label.setText("sin sesiones")
            return

        fecha_es = f"{dia.day} {MESES_ES[dia.month - 1]} {dia.year}"
        self.titulo_label.setText(f"Postura - {fecha_es}")

        serie = QPieSeries()
        serie.setHoleSize(0.8)
        serie.setPieSize(9)

        slice_buena = serie.append("Buena postura", minutos_buena)
        slice_mala = serie.append("Mala postura", minutos_mala)

        slice_buena.setBrush(COLOR_BUENA)
        slice_mala.setBrush(COLOR_MALA)
        slice_buena.setPen(Qt.PenStyle.NoPen)
        slice_mala.setPen(Qt.PenStyle.NoPen)

        slice_buena.setLabelVisible(False)
        slice_mala.setLabelVisible(False)

        self.chart.addSeries(serie)

        porcentaje_buena = round((minutos_buena / total) * 100)
        self.pct_label.setText(f"{porcentaje_buena}%")
        self.pct_sub_label.setText("buena postura")


def main():
    from Datapruba import generar_sesiones_prueba

    app = QApplication(sys.argv)
    hoy = datetime.now().date()
    dias_transcurridos = (hoy - date(hoy.year, 1, 1)).days + 1
    sesiones = generar_sesiones_prueba(dias_atras=dias_transcurridos)

    donut = DonutPostura(sesiones)
    donut.resize(320, 320)
    donut.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()