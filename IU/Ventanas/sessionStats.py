
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ResumenSesion:
    fecha_inicio: datetime
    fecha_fin: datetime
    duracion_segundos: int
    minutos_buena_postura: int
    minutos_mala_postura: int
    tareas_completadas: list[int] = field(default_factory=list)

    @property
    def cantidad_tareas_completadas(self) -> int:
        return len(self.tareas_completadas)