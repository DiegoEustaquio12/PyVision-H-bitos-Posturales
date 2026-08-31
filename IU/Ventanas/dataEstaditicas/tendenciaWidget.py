"""
Fase 4: Línea de tendencia de % de buena postura en los últimos 14 días,
con QtCharts.

Decisión de diseño: los días SIN sesión registrada no se rellenan con
un valor inventado (ni 0%, ni el valor del día anterior). La línea se
corta en esos huecos, para no dar a entender que hay un dato donde no
lo hay. Los días con dato real se marcan con un punto sólido.

No sabe nada de SQLite - solo recibe una lista de ResumenSesion y pinta.
"""

import sys
from datetime import date, datetime, timedelta

from PySide6.QtCharts import QBarCategoryAxis, QChart, QChartView, QLineSeries, QScatterSeries, QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

MESES_ES = [
    "Ene", "Feb", "Mar", "Abr", "May", "Jun",
    "Jul", "Ago", "Sep", "Oct", "Nov", "Dic",
]

COLOR_LINEA = QColor("#4caf50")


def _porcentaje_por_dia(sesiones: list, dias: int = 14) -> list[tuple[date, int | None]]:
    """
    Devuelve una lista ordenada (más antiguo -> más reciente) de
    (fecha, porcentaje_buena_postura) para los últimos `dias` días,
    terminando hoy. porcentaje es None si ese día no tiene sesiones.
    """
    por_dia: dict[date, tuple[int, int]] = {}
    for s in sesiones:
        dia = s.fecha_inicio.date()
        buena, mala = por_dia.get(dia, (0, 0))
        por_dia[dia] = (buena + s.minutos_buena_postura, mala + s.minutos_mala_postura)

    hoy = datetime.now().date()
    resultado = []
    for offset in range(dias - 1, -1, -1):
        dia = hoy - timedelta(days=offset)
        if dia in por_dia:
            buena, mala = por_dia[dia]
            total = buena + mala
            pct = round((buena / total) * 100) if total > 0 else None
        else:
            pct = None
        resultado.append((dia, pct))
    return resultado


class TendenciaWidget(QWidget):
    def __init__(self, sesiones: list | None = None, dias: int = 14, parent=None):
        super().__init__(parent)
        self._dias = dias

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(4)

        self.titulo_label = QLabel("Tendencia de postura")
        #self.titulo_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #333;")
        layout.addWidget(self.titulo_label)

        self.chart = QChart()
        self.chart.legend().setVisible(False)
        self.chart.setBackgroundVisible(False)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setStyleSheet("background: transparent;")
        layout.addWidget(self.chart_view, stretch=1)

        self.set_sesiones(sesiones or [])

    def set_sesiones(self, sesiones: list) -> None:
        datos = _porcentaje_por_dia(sesiones, self._dias)
        self._actualizar_chart(datos)

    def _actualizar_chart(self, datos: list[tuple[date, int | None]]) -> None:
        self.chart.removeAllSeries()
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        valores_reales = [pct for _, pct in datos if pct is not None]
        if not valores_reales:
            self.titulo_label.setText("Tendencia de postura - sin datos")
            return

        promedio = round(sum(valores_reales) / len(valores_reales))
        fecha_inicio, _ = datos[0]
        fecha_fin, _ = datos[-1]
        rango_es = f"{fecha_inicio.day} {MESES_ES[fecha_inicio.month - 1]} - {fecha_fin.day} {MESES_ES[fecha_fin.month - 1]}"
        self.titulo_label.setText(f"Tendencia de postura ({rango_es}) · Promedio: {promedio}%")

        categorias = [str(d.day) for d, _ in datos]

        eje_x = QBarCategoryAxis()
        eje_x.append(categorias)
        eje_x.setLabelsFont(self._fuente_pequena())

        eje_y = QValueAxis()
        eje_y.setRange(0, 100)
        eje_y.setLabelFormat("%d%%")
        eje_y.setTickCount(6)
        eje_y.setLabelsFont(self._fuente_pequena())

        self.chart.addAxis(eje_x, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(eje_y, Qt.AlignmentFlag.AlignLeft)

        # --- Construir segmentos de línea, cortando en los huecos (días sin dato) ---
        pluma = QPen(COLOR_LINEA)
        pluma.setWidth(3)

        segmento_actual = QLineSeries()
        segmentos = []
        for i, (_, pct) in enumerate(datos):
            if pct is None:
                if segmento_actual.count() > 0:
                    segmentos.append(segmento_actual)
                    segmento_actual = QLineSeries()
                continue
            segmento_actual.append(i, pct)
        if segmento_actual.count() > 0:
            segmentos.append(segmento_actual)

        for seg in segmentos:
            seg.setPen(pluma)
            self.chart.addSeries(seg)
            seg.attachAxis(eje_x)
            seg.attachAxis(eje_y)

        # --- Puntos sólidos marcando días con dato real ---
        marcadores = QScatterSeries()
        marcadores.setMarkerSize(9)
        marcadores.setColor(COLOR_LINEA)
        marcadores.setBorderColor(QColor("#ffffff"))
        for i, (_, pct) in enumerate(datos):
            if pct is not None:
                marcadores.append(i, pct)

        self.chart.addSeries(marcadores)
        marcadores.attachAxis(eje_x)
        marcadores.attachAxis(eje_y)

    @staticmethod
    def _fuente_pequena():
        from PySide6.QtGui import QFont
        f = QFont()
        f.setPointSize(8)
        return f


def main():
    from Datapruba import generar_sesiones_prueba

    app = QApplication(sys.argv)
    hoy = datetime.now().date()
    dias_transcurridos = (hoy - date(hoy.year, 1, 1)).days + 1
    sesiones = generar_sesiones_prueba(dias_atras=dias_transcurridos)

    widget = TendenciaWidget(sesiones)
    widget.resize(650, 320)
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()