"""
Generador de datos de prueba para la ventana de Estadísticas.

Simula sesiones (ResumenSesion) a lo largo de ~18-20 días, con variabilidad
realista: días sin sesión, días con 1-3 sesiones, y proporción buena/mala
postura que varía (algunos días mejores que otros) para que el heatmap,
la dona y la línea de 14 días tengan datos interesantes que mostrar.

Cuando Rodrigo tenga el stats_adapter.py conectado a SQLite de verdad,
esta función se reemplaza por la consulta real - la forma de los datos
(lista de ResumenSesion) se mantiene igual.
"""

import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class ResumenSesion:
    fecha_inicio: datetime
    fecha_fin: datetime
    duracion_segundos: int
    minutos_buena_postura: int
    minutos_mala_postura: int
    tareas_completadas: list[int] = field(default_factory=list)


def generar_sesiones_prueba(dias_atras: int = 20, semilla: int = 42) -> list[ResumenSesion]:
    """
    Genera sesiones falsas distribuidas en los últimos `dias_atras` días.

    - Algunos días no tienen ninguna sesión (simula días sin usar la app).
    - Otros días tienen 1 a 3 sesiones.
    - La proporción de buena/mala postura varía por "racha": hay tramos
      de días buenos y tramos de días malos, no es puramente random,
      para que la línea de tendencia se vea con una forma real.
    """
    random.seed(semilla)
    sesiones: list[ResumenSesion] = []
    hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Genera una "calidad base" por día usando un paseo aleatorio suave,
    # así los días consecutivos tienden a parecerse (más realista que
    # puro random por día).
    calidad_base = 0.6
    calidades_por_dia = []
    for _ in range(dias_atras):
        calidad_base += random.uniform(-0.12, 0.12)
        calidad_base = max(0.25, min(0.9, calidad_base))
        calidades_por_dia.append(calidad_base)

    for i in range(dias_atras):
        dia = hoy - timedelta(days=(dias_atras - 1 - i))
        calidad_dia = calidades_por_dia[i]

        # ~20% de probabilidad de que no haya ninguna sesión ese día
        if random.random() < 0.20:
            continue

        num_sesiones = random.choices([1, 2, 3], weights=[0.55, 0.30, 0.15])[0]

        hora_actual = 8 + random.randint(0, 2)  # empieza entre 8-10am
        for _ in range(num_sesiones):
            duracion_min = random.choice([25, 25, 25, 50])  # pomodoro clásico o doble
            inicio = dia.replace(hour=min(int(hora_actual), 21))
            fin = inicio + timedelta(minutes=duracion_min)

            # Ruido por sesión sobre la calidad base del día
            calidad_sesion = max(0.1, min(0.95, calidad_dia + random.uniform(-0.1, 0.1)))
            minutos_buena = round(duracion_min * calidad_sesion)
            minutos_mala = duracion_min - minutos_buena

            tareas = random.sample(range(1, 30), k=random.randint(0, 2))

            sesiones.append(
                ResumenSesion(
                    fecha_inicio=inicio,
                    fecha_fin=fin,
                    duracion_segundos=duracion_min * 60,
                    minutos_buena_postura=minutos_buena,
                    minutos_mala_postura=minutos_mala,
                    tareas_completadas=tareas,
                )
            )
            hora_actual += duracion_min / 60 + random.uniform(0.5, 2.0)

    return sesiones


if __name__ == "__main__":
    # Prueba rápida por consola
    datos = generar_sesiones_prueba()
    print(f"Total de sesiones generadas: {len(datos)}")
    for s in datos[:5]:
        print(s)