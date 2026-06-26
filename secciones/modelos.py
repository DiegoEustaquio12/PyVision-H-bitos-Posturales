
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Objetivo:
    id_objetivo: int = None
    titulo: str = ""
    completado: bool = False
    pomodoros_estimados: int = 1
    pomodoros_realizados: int = 0

@dataclass
class SesionPomodoro:
    id_sesion: int = None
    id_objetivo: int = None
    tipo: str = "focus"  # "focus", "descanso_corto", "descanso_largo"
    duracion_segundos: int = 1500
    fecha_inicio: str = field(default_factory=lambda: datetime.now().isoformat())
    completada: bool = False

@dataclass
class EstadoPostura:
    id_registro: int = None
    fecha_hora: str = field(default_factory=lambda: datetime.now().isoformat())
    estado: str = "correcta"  # "correcta", "encorvado", "ausente", etc.
    confianza: float = 0.0    # Porcentaje de certeza del modelo de visión (0.0 a 1.0)