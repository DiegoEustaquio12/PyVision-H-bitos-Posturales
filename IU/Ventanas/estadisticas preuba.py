import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


def _placeholder_frame(texto: str, color_fondo: str, alto_minimo: int = 0) -> QFrame:
    """
    Crea un frame de relleno para previsualizar proporciones del layout.
    Se reemplaza en fases siguientes por el widget real (heatmap custom
    o QChartView).
    """
    frame = QFrame()
    frame.setStyleSheet(
        f"""
        QFrame {{
            background-color: {color_fondo};
            border-radius: 12px;
        }}
        """
    )
    if alto_minimo:
        frame.setMinimumHeight(alto_minimo)

    layout = QVBoxLayout(frame)
    label = QLabel(texto)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("color: #555; font-size: 14px; font-weight: 500; border: none;")
    layout.addWidget(label)

    return frame


class EstadisticasWindow(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Estadísticas - PyVision")
        self.setMinimumSize(900, 650)
        self._construir_ui()

    def _construir_ui(self) -> None:
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(24, 24, 24, 24)
        layout_principal.setSpacing(20)

        # --- Título ---
        titulo = QLabel("Estadísticas")
        titulo.setStyleSheet("font-size: 22px; font-weight: 700;")
        layout_principal.addWidget(titulo)

        # --- Heatmap (ancho completo) ---
        self.heatmap_placeholder = _placeholder_frame(
            "Heatmap estilo GitHub\n(Fase 2 - QPainter custom)",
            color_fondo="#e8f0e3",
            alto_minimo=180,
        )
        layout_principal.addWidget(self.heatmap_placeholder)

        # --- Fila inferior: Dona | Línea 14 días ---
        fila_inferior = QHBoxLayout()
        fila_inferior.setSpacing(20)

        self.dona_placeholder = _placeholder_frame(
            "Dona: buena vs. mala postura\n(Fase 3 - QtCharts)",
            color_fondo="#e3e9f0",
        )
        self.linea_placeholder = _placeholder_frame(
            "Línea de tendencia (14 días)\n(Fase 4 - QtCharts)",
            color_fondo="#f0e9e3",
        )

        # Proporción 35 / 65 vía stretch factors
        fila_inferior.addWidget(self.dona_placeholder, 35)
        fila_inferior.addWidget(self.linea_placeholder, 65)

        layout_principal.addLayout(fila_inferior, stretch=1)

        self.setLayout(layout_principal)


def main():
    app = QApplication(sys.argv)
    ventana = EstadisticasWindow()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()