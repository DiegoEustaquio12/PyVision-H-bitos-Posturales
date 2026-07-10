from PySide6.QtCore import Qt, QRectF, QTimer, Signal, QUrl
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout
import sys
from PySide6.QtMultimedia import QSoundEffect


class WidgetCirculo(QWidget):
    finished = Signal()
    cambioFase = Signal(bool)
    def __init__(self):
        super().__init__()
        self.bar_width = 14
        self.textColor = QColor("#FFFFFF")
        self.setMinimumSize(200, 200)

        self.workSeconds = 10 * 60
        self.restSeconds = 5* 60
        self.working = True

        self.total_seconds = self.workSeconds
        self.remaining_seconds = self.total_seconds * 1000

        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.updateCirculo)
        #self.timer.start()


        self.sonidos_alerta =QSoundEffect()
        self.sonidos_alerta.setSource(QUrl.fromLocalFile("sounds/alarmaPomodoro.wav"))
        self.sonidos_alerta.setVolume(0.5)

        self.yaSonoAlerta = False

    def updateCirculo(self):
        self.remaining_seconds -= self.timer.interval()

        if self.remaining_seconds == 3600:
            self.sonidos_alerta.play()

        if self.remaining_seconds <= 0:
            #self.remaining_seconds = 0
            self.finished.emit()
            self.alternarFase()
            #self.reiniciar()
            self.timer.start()

        self.update()

    def set_tiempos(self, work_seconds, rest_seconds):
        """Se llama desde el QMenu al elegir una opción (Pomodoro/Enfoque/Predeterminado)."""
        self.workSeconds = work_seconds
        self.restSeconds = rest_seconds
        self.working = True
        self.total_seconds = self.workSeconds
        self.remaining_seconds = self.total_seconds * 1000
        self.timer.stop()
        self.cambioFase.emit(self.working)
        self.update()

    def alternarFase(self):
        self.working = not self.working
        self.total_seconds = self.workSeconds if self.working else self.restSeconds
        self.remaining_seconds = self.total_seconds * 1000
        self.cambioFase.emit(self.working)


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

        hue1 = int(fraction * 120)
        color2 = QColor()
        color2.setHsv(hue1, 255, 50)
        return color2

    def iniciar(self):
        if self.remaining_seconds <= 0:
            self.reiniciar()
        self.timer.start()

    def pausar(self):
        self.timer.stop()

    def reiniciar(self):
        self.timer.stop()
        self.remaining_seconds = self.total_seconds * 1000
        self.update()

    def runningTime(self):
        return self.timer.isActive()

