
import sqlite3
from modelos import Objetivo, SesionPomodoro, EstadoPostura

class HistorialBD:
    def __init__(self, db_name="productividad.db"):
        self.db_name = db_name
        self.inicializar_tablas()

    def _conectar(self):
        """Crea una conexión lista para usar con soporte para llaves foráneas."""
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def inicializar_tablas(self):
        """Crea las tablas necesarias si no existen en el archivo .db."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # 1. Tabla de Objetivos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS objetivos (
                    id_objetivo INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    completado INTEGER DEFAULT 0,
                    pomodoros_estimados INTEGER DEFAULT 1,
                    pomodoros_realizados INTEGER DEFAULT 0
                )
            """)
            
            # 2. Tabla de Sesiones (Relacionada con Objetivos)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sesiones (
                    id_sesion INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_objetivo INTEGER,
                    tipo TEXT NOT NULL,
                    duracion_segundos INTEGER NOT NULL,
                    fecha_inicio TEXT NOT NULL,
                    completada INTEGER DEFAULT 0,
                    FOREIGN KEY (id_objetivo) REFERENCES objetivos(id_objetivo) ON DELETE SET NULL
                )
            """)
            
            # 3. Tabla de Historial de Postura
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historial_postura (
                    id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_hora TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    confianza REAL DEFAULT 0.0
                )
            """)
            conn.commit()

    # ==========================================
    # CRUD: OBJETIVOS
    # ==========================================
    def crear_objetivo(self, objetivo: Objetivo) -> int:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO objetivos (titulo, completado, pomodoros_estimados, pomodoros_realizados)
                VALUES (?, ?, ?, ?)
            """, (objetivo.titulo, int(objetivo.completado), objetivo.pomodoros_estimados, objetivo.pomodoros_realizados))
            conn.commit()
            return cursor.lastrowid

    def leer_objetivos(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM objetivos")
            filas = cursor.fetchall()
            return [Objetivo(id_objetivo=f[0], titulo=f[1], completado=bool(f[2]), pomodoros_estimados=f[3], pomodoros_realizados=f[4]) for f in filas]

    def actualizar_objetivo(self, objetivo: Objetivo):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE objetivos 
                SET titulo = ?, completado = ?, pomodoros_estimados = ?, pomodoros_realizados = ?
                WHERE id_objetivo = ?
            """, (objetivo.titulo, int(objetivo.completado), objetivo.pomodoros_estimados, objetivo.pomodoros_realizados, objetivo.id_objetivo))
            conn.commit()

    def eliminar_objetivo(self, id_objetivo: int):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM objetivos WHERE id_objetivo = ?", (id_objetivo,))
            conn.commit()

    # ==========================================
    # CRUD: SESIONES
    # ==========================================
    def registrar_sesion(self, sesion: SesionPomodoro) -> int:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sesiones (id_objetivo, tipo, duracion_segundos, fecha_inicio, completada)
                VALUES (?, ?, ?, ?, ?)
            """, (sesion.id_objetivo, sesion.tipo, sesion.duracion_segundos, sesion.fecha_inicio, int(sesion.completada)))
            conn.commit()
            return cursor.lastrowid

    def leer_sesiones(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sesiones")
            filas = cursor.fetchall()
            return [SesionPomodoro(id_sesion=f[0], id_objetivo=f[1], tipo=f[2], duracion_segundos=f[3], fecha_inicio=f[4], completada=bool(f[5])) for f in filas]

    # ==========================================
    # ALMACENAMIENTO: HISTORIAL DE POSTURA
    # ==========================================
    def registrar_postura(self, postura: EstadoPostura) -> int:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO historial_postura (fecha_hora, estado, confianza)
                VALUES (?, ?, ?)
            """, (postura.fecha_hora, postura.estado, postura.confianza))
            conn.commit()
            return cursor.lastrowid

    def obtener_historial_postura(self, limite=100):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM historial_postura ORDER BY fecha_hora DESC LIMIT ?", (limite,))
            filas = cursor.fetchall()
            return [EstadoPostura(id_registro=f[0], fecha_hora=f[1], estado=f[2], confianza=f[3]) for f in filas]


# --- Bloque de Prueba para verificar el funcionamiento ---
if __name__ == "__main__":
    print("--- Probando Base de Datos SQLite ---")
    db = HistorialBD("prueba_productividad.db")

    # 1. Prueba de creación (C de CRUD)
    nuevo_obj = Objetivo(titulo="Estudiar Análisis de Algoritmos", pomodoros_estimados=3)
    id_generado = db.crear_objetivo(nuevo_obj)
    print(f"[OK] Objetivo creado con ID: {id_generado}")

    # 2. Prueba de lectura (L de CRUD)
    lista_objetivos = db.leer_objetivos()
    print(f"[OK] Objetivos actuales en BD: {lista_objetivos}")

    # 3. Prueba de actualización (U de CRUD)
    if lista_objetivos:
        objetivo_a_modificar = lista_objetivos[0]
        objetivo_a_modificar.completado = True
        objetivo_a_modificar.pomodoros_realizados = 1
        db.actualizar_objetivo(objetivo_a_modificar)
        print(f"[OK] Objetivo ID {objetivo_a_modificar.id_objetivo} actualizado.")

    # 4. Prueba registro de postura
    registro_postura = EstadoPostura(estado="encorvado", confianza=0.88)
    id_postura = db.registrar_postura(registro_postura)
    print(f"[OK] Registro de postura insertado, ID: {id_postura}")
    
    print(f"Historial reciente de postura: {db.obtener_historial_postura(5)}")