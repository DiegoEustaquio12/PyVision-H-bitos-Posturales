from PySide6.QtCore import Qt, QRectF, QTimer
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout
import sys


class WidgetCirculo(QWidget):
    def __init__(self):
        super().__init__()
        self.bar_width = 14
        self.bg_color = QColor("#203d2f")
        self.progressColor = QColor("#056d38")
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

        # Fondo
        pen_bg = QPen(self.bg_color)
        pen_bg.setWidth(self.bar_width)
        pen_bg.setCapStyle(Qt.RoundCap)
        painter.setPen(pen_bg)
        painter.drawArc(rect, 0, 360 * 16)

        # Progreso
        fraction = self.get_fraction()
        angulo = int(fraction * 360 * 16)

        pen_progress = QPen(self.progressColor)
        pen_progress.setWidth(self.bar_width)
        pen_progress.setCapStyle(Qt.RoundCap)
        painter.setPen(pen_progress)
        painter.drawArc(rect, 90 * 16, -angulo)  # negativo para sentido horario

        # Texto
        painter.setPen(self.textColor)
        painter.setFont(QFont("Segoe UI", int(lado * 0.18), QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, self.get_time_text())

