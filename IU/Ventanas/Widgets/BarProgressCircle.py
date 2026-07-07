from PySide6.QtCore import Qt, QRectF, QTimer
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout
import sys


class WidgetCirculo(QWidget):
    def __init__(self):
        super().__init__()
        self.bar_width = 14
        self.textColor = QColor("#FFFFFF")
        self.setMinimumSize(200, 200)



        self.total_seconds = 60
        self.remaining_seconds = 60 * 1000

        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.updateCirculo)
        self.timer.start()

    def updateCirculo(self):
        self.remaining_seconds -= self.timer.interval()

        if self.remaining_seconds <= 0:
            self.remaining_seconds = 0
            self.timer.stop()

        self.update()

    def get_fraction(self):
        total_ms = self.total_seconds * 1000
        return self.remaining_seconds / total_ms

    def get_time_text(self):
        totalSeconsRemaining = round(self.remaining_seconds / 1000)
        minutesRemaining = totalSeconsRemaining // 60
        secondsRemaining = totalSeconsRemaining % 60
        return f"{minutesRemaining}:{secondsRemaining:02d}"

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        lado = min(self.width(), self.height()) - self.bar_width

        x = (self.width() - lado) / 2
        y = (self.height() - lado) / 2

        rect = QRectF(x, y, lado, lado)

        # Progreso
        fraction = self.get_fraction()
        angulo = int(fraction * 360 * 16)

        colorBackground = self.get_background_color(fraction)
        # Fondo
        pen_bg = QPen(colorBackground)
        pen_bg.setWidth(self.bar_width)
        pen_bg.setCapStyle(Qt.RoundCap)
        painter.setPen(pen_bg)
        painter.drawArc(rect, 0, 360 * 16)



        colorActual = self.get_progress_color(fraction)

        pen_progress = QPen(colorActual)
        pen_progress.setWidth(self.bar_width)
        pen_progress.setCapStyle(Qt.RoundCap)
        painter.setPen(pen_progress)
        painter.drawArc(rect, 90 * 16, -angulo)  # negativo para sentido horario

        # Texto
        painter.setPen(self.textColor)
        painter.setFont(QFont("Segoe UI", int(lado * 0.18), QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, self.get_time_text())

    def get_progress_color(self, fraction):
        # fraction: 1.0 (inicio, verde) -> 0.0 (final, rojo)
        hue = int(fraction * 120)  # 120=verde, 60=amarillo, 0=rojo
        color = QColor()
        color.setHsv(hue, 255, 150)  # value=200 para que no sea demasiado brillante
        return color
    def get_background_color(self, fraction):
        # fraction: 1.0 (inicio, verde) -> 0.0 (final, rojo)
        hue1 = int(fraction * 120)  # 120=verde, 60=amarillo, 0=rojo
        color2 = QColor()
        color2.setHsv(hue1, 255, 50)  # value=200 para que no sea demasiado brillante
        return color2

