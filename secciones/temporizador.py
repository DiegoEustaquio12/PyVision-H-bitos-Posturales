import sys
from PySide6.QtCore import QObject, QTimer, Signal, QCoreApplication

# 1. Importamos nuestros modelos y el gestor de la base de datos
from modelos import SesionPomodoro
from historial import HistorialBD

class ContadorBackend(QObject):
    tiempo_actualizado = Signal(int)
    seccion_terminada = Signal()
    seccion_cancelada = Signal() 

    def __init__(self):
        super().__init__()
        self.tiempo_restante = 0
        self.duracion_inicial = 0  # NUEVO: Para recordar de cuánto fue la sesión
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)

    def iniciar_seccion(self, segundos: int):
        self.duracion_inicial = segundos # Guardamos la meta original
        self.tiempo_restante = segundos
        self.tiempo_actualizado.emit(self.tiempo_restante)
        self.timer.start(1000)
        print(f"\n[Backend] Sección iniciada: {segundos} segundos.")

    def pausar(self):
        if self.timer.isActive():
            self.timer.stop()
            print("\n[Backend] Temporizador pausado.")

    def reanudar(self):
        if self.tiempo_restante > 0 and not self.timer.isActive():
            self.timer.start(1000)
            print("\n[Backend] Temporizador reanudado.")

    def detener(self):
        if self.timer.isActive():
            self.timer.stop()
        self.tiempo_restante = 0
        self.duracion_inicial = 0
        self.tiempo_actualizado.emit(self.tiempo_restante)
        self.seccion_cancelada.emit()
        print("\n[Backend] Temporizador detenido y reseteado.")

    def _tick(self):
        self.tiempo_restante -= 1
        self.tiempo_actualizado.emit(self.tiempo_restante)
        
        if self.tiempo_restante <= 0:
            self.timer.stop()
            self.seccion_terminada.emit()


# --- Bloque Controlador / Pruebas en Terminal ---

def mostrar_tiempo(segundos):
    mins, secs = divmod(segundos, 60)
    sys.stdout.write(f"\rTiempo restante: {mins:02d}:{secs:02d} ")
    sys.stdout.flush()

def guardar_sesion_en_bd():
    """Esta función se ejecuta automáticamente cuando el temporizador termina."""
    print("\n¡Sección completada! Guardando en la base de datos...")
    
    # 1. Creamos el objeto de la sesión usando la duración que guardamos
    nueva_sesion = SesionPomodoro(
        tipo="focus", 
        duracion_segundos=backend.duracion_inicial,
        completada=True
    )
    
    # 2. Lo guardamos en la base de datos real
    id_guardado = db.registrar_sesion(nueva_sesion)
    print(f"[OK] Sesión registrada exitosamente con el ID: {id_guardado}")
    
    # Mostramos todas las sesiones registradas para comprobar
    print("\n--- Historial de Sesiones en BD ---")
    for sesion in db.leer_sesiones():
        print(f"ID: {sesion.id_sesion} | Tipo: {sesion.tipo} | Duración: {sesion.duracion_segundos}s | Completada: {sesion.completada}")
    
    QCoreApplication.quit()

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    
    # Inicializamos la base de datos real (productividad.db)
    db = HistorialBD("productividad.db")
    
    # Inicializamos el temporizador
    backend = ContadorBackend()
    
    # Conectamos las señales
    backend.tiempo_actualizado.connect(mostrar_tiempo)
    
    # Conectamos el final del temporizador con la funcion de guardado
    backend.seccion_terminada.connect(guardar_sesion_en_bd)

    print("--- Prueba de Integración: Temporizador + Base de Datos ---")
    
    # Iniciamos una sesión muy corta (3 segundos) para probar el guardado rápido
    backend.iniciar_seccion(3)

    sys.exit(app.exec())