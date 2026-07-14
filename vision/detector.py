import os
import math
import time
import urllib.request
from collections import deque

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Modelo
MODEL_PATH = "pose_landmarker_full.task"
MODEL_URL  = (
    "https://storage.googleapis.com/mediapipe-models/pose_landmarker/"
    "pose_landmarker_full/float16/1/pose_landmarker_full.task"
)

if not os.path.exists(MODEL_PATH):
    print("Descargando modelo local de MediaPipe Pose...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)


# Perfil activo del usuario  opciones: "adulto" y "nino"
PERFIL_ACTIVO = "adulto"

# Umbrales dinámicos por perfil
PERFILES_USUARIO = {
    "adulto": {
        "max_inclinacion_cabeza"  : 15.0,
        "max_desnivel_hombros"    : 12.0,
        "max_inclinacion_tronco"  :  8.0,
        "min_ratio_altura_tronco" :  1.00,
        "min_ratio_encorvamiento" :  0.42,
        "min_ratio_apertura"      :  1.95,
    },
    "nino": {
        "max_inclinacion_cabeza"  : 18.0,
        "max_desnivel_hombros"    : 14.0,
        "max_inclinacion_tronco"  : 12.0,
        "min_ratio_altura_tronco" :  0.85,
        "min_ratio_encorvamiento" :  0.38,
        "min_ratio_apertura"      :  1.75,
    },
}

umbrales = PERFILES_USUARIO[PERFIL_ACTIVO]


PUNTOS_TRONCO_LATERAL   = 40  # Primario — rotación del tronco
PUNTOS_TRONCO_COLAPSO   = 15  # Auxiliar — sensible al zoom
PUNTOS_CABEZA           = 20  # Secundario — ladeo de cabeza
PUNTOS_ENCORVAMIENTO    = 20  # Secundario — cuello/hombros
PUNTOS_APERTURA         = 15  # Secundario — apertura de pecho
PUNTOS_HOMBROS_BASE     = 10  
UMBRAL_PUNTOS_MALA_POSTURA = 20

#alerta tras 5 segundos continuos de mala postura
SEGUNDOS_PARA_ACTIVAR_ALERTA = 5.0

TAMANO_BUFFER_HOMBROS = 8
TAMANO_BUFFER_TRONCO  = 5

# colores rgb
COLOR_CORRECTO   = (40, 220, 100)
COLOR_INCORRECTO = (50, 50, 240)
COLOR_ALERTA     = (0, 165, 255)
BLANCO           = (255, 255, 255)
AMARILLO         = (0, 230, 230)
OSCURO           = (20, 20, 20)
GRIS_CLARO       = (200, 200, 200)

OFFSET_SUPERIOR_HOMBRO = 0.30

# Índices de landmarks de MediaPipe Pose
IDX_NARIZ      = 0
IDX_OREJA_IZQ  = 7;  IDX_OREJA_DER  = 8
IDX_HOMB_IZQ   = 11; IDX_HOMB_DER   = 12
IDX_CADERA_IZQ = 23; IDX_CADERA_DER = 24

buffer_hombro_izq = deque(maxlen=TAMANO_BUFFER_HOMBROS)
buffer_hombro_der = deque(maxlen=TAMANO_BUFFER_HOMBROS)
buffer_cadera_izq = deque(maxlen=TAMANO_BUFFER_TRONCO)
buffer_cadera_der = deque(maxlen=TAMANO_BUFFER_TRONCO)


#Creación de variable global para almacenar los datos del dashboard
_datos_dashboard = {
    "estado_postura": "SIN_DETECCION",
    "tiempo_postura": 0.0,
    "timestamp": time.time()
}

# Función para obtener el estado de la postura y el tiempo acumulado
def obtener_estado_postura():
    """
    Función expuesta para que el backend la consuma de manera asíncrona.
    Retorna el estado y el tiempo acumulado de la postura actual.
    """
    global _datos_dashboard
    _datos_dashboard["timestamp"] = time.time()
    return _datos_dashboard


#funciones de calcular
def calcular_inclinacion(p1: tuple, p2: tuple) -> float:
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    if dx == 0:
        return 0.0
    return abs(math.degrees(math.atan(dy / dx)))


def calcular_inclinacion_vertical(p_inferior: tuple, p_superior: tuple) -> float:
    dx = p_superior[0] - p_inferior[0]
    dy = p_inferior[1] - p_superior[1]
    if dy == 0:
        return 0.0
    return abs(math.degrees(math.atan(dx / dy)))


def calcular_distancia(p1: tuple, p2: tuple) -> float:
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def obtener_punto_medio(p1: tuple, p2: tuple) -> tuple:
    return (int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2))


def normalizar_a_pixeles(landmark, ancho: int, alto: int) -> tuple:
    return (int(landmark.x * ancho), int(landmark.y * alto))


def aplicar_suavizado(punto: tuple, buffer: deque) -> tuple:
    buffer.append(punto)
    promedio_x = int(sum(p[0] for p in buffer) / len(buffer))
    promedio_y = int(sum(p[1] for p in buffer) / len(buffer))
    return (promedio_x, promedio_y)

#evaluacion de postura
def evaluar_postura(
    inclinacion_tronco: float,
    ratio_altura_tronco: float,
    tilt_cabeza: float,
    ratio_encorvamiento: float,
    ratio_apertura: float,
    tilt_hombros: float,
) -> tuple:
    u = umbrales
    puntos_acumulados = 0

    # Indicadores primarios para el tronco
    if inclinacion_tronco > u["max_inclinacion_tronco"]:
        puntos_acumulados += PUNTOS_TRONCO_LATERAL

    if ratio_altura_tronco > 0.1 and ratio_altura_tronco < u["min_ratio_altura_tronco"]:
        puntos_acumulados += PUNTOS_TRONCO_COLAPSO

    # Indicadores secundarios
    if tilt_cabeza > u["max_inclinacion_cabeza"]:
        puntos_acumulados += PUNTOS_CABEZA

    if ratio_encorvamiento > 0 and ratio_encorvamiento < u["min_ratio_encorvamiento"]:
        puntos_acumulados += PUNTOS_ENCORVAMIENTO

    if ratio_apertura > 0 and ratio_apertura < u["min_ratio_apertura"]:
        puntos_acumulados += PUNTOS_APERTURA

    if tilt_hombros > u["max_desnivel_hombros"]:
        hay_corroboracion = (
            tilt_cabeza > u["max_inclinacion_cabeza"] * 0.5 or
            ratio_encorvamiento > 0 and ratio_encorvamiento < u["min_ratio_encorvamiento"] * 1.1
        )
        if hay_corroboracion:
            puntos_acumulados += PUNTOS_HOMBROS_BASE

    es_mala_postura_frame = puntos_acumulados >= UMBRAL_PUNTOS_MALA_POSTURA
    puntuacion_total      = min(100, puntos_acumulados)

    return es_mala_postura_frame, puntuacion_total

class GestorAlertaPostura:
    """Temporiza alertas: solo se activa tras N segundos continuos de mala postura."""

    def __init__(self, segundos_umbral: float = SEGUNDOS_PARA_ACTIVAR_ALERTA):
        self.segundos_umbral = segundos_umbral
        self.timestamp_inicio_mala_postura = None
        self.duracion_mala_postura_actual  = 0.0
        self.alerta_sostenida_activa       = False

    def actualizar(self, es_mala_postura_frame: bool) -> bool:
        ahora = time.monotonic()

        if es_mala_postura_frame:
            if self.timestamp_inicio_mala_postura is None:
                self.timestamp_inicio_mala_postura = ahora
            self.duracion_mala_postura_actual = ahora - self.timestamp_inicio_mala_postura

            if self.duracion_mala_postura_actual >= self.segundos_umbral:
                self.alerta_sostenida_activa = True
        else:
            self.timestamp_inicio_mala_postura = None
            self.duracion_mala_postura_actual  = 0.0
            self.alerta_sostenida_activa       = False

        return self.alerta_sostenida_activa

def dibujar_esqueleto_postura(
    frame,
    nariz, oreja_izq, oreja_der,
    hombro_izq, hombro_der, centro_hombros,
    cadera_izq, cadera_der, centro_caderas,
    color_estado,
):
    # lineas
    cv2.line(frame, cadera_izq, cadera_der, color_estado, 2, cv2.LINE_AA)
    cv2.line(frame, hombro_izq, hombro_der, color_estado, 3, cv2.LINE_AA)
    cv2.line(frame, oreja_izq,  oreja_der,  color_estado, 2, cv2.LINE_AA)
    cv2.line(frame, centro_caderas, centro_hombros, color_estado, 4, cv2.LINE_AA)
    cv2.line(frame, centro_hombros, nariz,          color_estado, 4, cv2.LINE_AA)

    for punto in [oreja_izq, oreja_der, hombro_izq, hombro_der,
                  cadera_izq, cadera_der, nariz, centro_hombros, centro_caderas]:
        cv2.circle(frame, punto, 7, color_estado, -1)
        cv2.circle(frame, punto, 9, BLANCO, 2)


def dibujar_hud_metricas(
    frame, fuente,
    perfil_activo,
    tilt_cabeza, tilt_hombros,
    inclinacion_tronco, ratio_altura_tronco,
    ratio_encorvamiento, ratio_apertura,
    puntuacion_postura,
    duracion_mala_postura,
    estado_texto, color_estado,
    alerta_activa,
):
    capa_sombra = frame.copy()
    cv2.rectangle(capa_sombra, (15, 15), (430, 235), OSCURO, -1)
    cv2.addWeighted(capa_sombra, 0.72, frame, 0.28, 0, frame)

    cv2.putText(frame, f"MODULO VISION: ANALISIS FRONTAL  [{perfil_activo.upper()}]",
                (25, 40), fuente, 0.50, AMARILLO, 2)

    # Métricas primarias
    cv2.putText(frame, f"[TRONCO] Inclinacion  : {inclinacion_tronco:.1f} deg",
                (25, 63), fuente, 0.46, BLANCO, 1)
    cv2.putText(frame, f"[TRONCO] Altura/Ancho : {ratio_altura_tronco:.2f}",
                (25, 81), fuente, 0.46, BLANCO, 1)

    # Métricas secundarias
    cv2.putText(frame, f"[CABEZA] Ladeo        : {tilt_cabeza:.1f} deg",
                (25, 100), fuente, 0.43, GRIS_CLARO, 1)
    cv2.putText(frame, f"[HOMBRO] Desnivel     : {tilt_hombros:.1f} deg",
                (25, 117), fuente, 0.43, GRIS_CLARO, 1)
    cv2.putText(frame, f"[PECHO]  Rectitud     : {ratio_encorvamiento:.2f}",
                (25, 134), fuente, 0.43, GRIS_CLARO, 1)
    cv2.putText(frame, f"[PECHO]  Apertura     : {ratio_apertura:.2f}",
                (25, 151), fuente, 0.43, GRIS_CLARO, 1)

    # Puntuación
    color_punt = COLOR_CORRECTO if puntuacion_postura < UMBRAL_PUNTOS_MALA_POSTURA else COLOR_INCORRECTO
    cv2.putText(frame, f"Puntuacion postura    : {int(puntuacion_postura)} pts  (umbral {UMBRAL_PUNTOS_MALA_POSTURA})",
                (25, 171), fuente, 0.46, color_punt, 1)

    # tiempo de postura
    tiempo_restante = max(0.0, SEGUNDOS_PARA_ACTIVAR_ALERTA - duracion_mala_postura)
    if duracion_mala_postura > 0:
        barra = int((duracion_mala_postura / SEGUNDOS_PARA_ACTIVAR_ALERTA) * 20)
        cv2.putText(frame, f"Alerta en             : {tiempo_restante:.1f}s  [{('|' * barra).ljust(20, '-')}]",
                    (25, 189), fuente, 0.43, COLOR_ALERTA, 1)
    else:
        cv2.putText(frame, "Alerta en             : --   [--------------------]",
                    (25, 189), fuente, 0.43, GRIS_CLARO, 1)

    # Estado principal
    cv2.putText(frame, estado_texto, (25, 218), fuente, 0.65, color_estado, 2)


# seleccion de camara
def listar_y_seleccionar_camara(max_indice: int = 10) -> int:
  
    camaras_disponibles = []

    print("Buscando camaras disponibles...")
    for indice in range(max_indice):
        cap_test = cv2.VideoCapture(indice, cv2.CAP_ANY)
        if cap_test.isOpened():
            # leer resolucion para mostrar info util
            ancho = int(cap_test.get(cv2.CAP_PROP_FRAME_WIDTH))
            alto  = int(cap_test.get(cv2.CAP_PROP_FRAME_HEIGHT))
            camaras_disponibles.append((indice, ancho, alto))
            cap_test.release()

    if not camaras_disponibles:
        print("ERROR: No se encontro ninguna camara conectada.")
        print("Usando camara 0 por defecto.")
        return 0

    if len(camaras_disponibles) == 1:
        idx = camaras_disponibles[0][0]
        print(f"Se encontro 1 camara disponible (indice {idx}). Seleccionada automaticamente.")
        return idx

    # multiples camaras — mostrar lista y pedir seleccion
    print(f"\nSe encontraron {len(camaras_disponibles)} camaras disponibles:\n")
    for i, (idx, ancho, alto) in enumerate(camaras_disponibles):
        print(f"  [{i}] Camara {idx}  ({ancho}x{alto})")

    print()
    while True:
        entrada = input(f"Selecciona una camara (0-{len(camaras_disponibles) - 1}): ").strip()
        if entrada.isdigit():
            seleccion = int(entrada)
            if 0 <= seleccion < len(camaras_disponibles):
                indice_seleccionado = camaras_disponibles[seleccion][0]
                print(f"Camara {indice_seleccionado} seleccionada.")
                return indice_seleccionado
        print("Opcion no valida. Intenta de nuevo.")


def main():
    global _datos_dashboard
    with open(MODEL_PATH, "rb") as f:
        model_data = f.read()

    opciones_vision = vision.PoseLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_buffer=model_data),
        running_mode=vision.RunningMode.IMAGE,
        min_pose_detection_confidence=0.5,
        min_pose_presence_confidence=0.5,
        output_segmentation_masks=False,
    )

    # seleccionar camara antes de iniciar la captura
    indice_camara = listar_y_seleccionar_camara()
    cap = cv2.VideoCapture(indice_camara, cv2.CAP_ANY)

    # calidad y los fps
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        cap.set(cv2.CAP_PROP_FPS, 30)

    print(f"Módulo de Visión de postura inicializado. Perfil activo: {PERFIL_ACTIVO.upper()}")
    print("Presiona 'q' en la ventana para salir.")

    gestor_alerta = GestorAlertaPostura(segundos_umbral=SEGUNDOS_PARA_ACTIVAR_ALERTA)
    
    # Variable persistente para controlar el inicio de la buena postura
    ts_inicio_buena_postura = None

    with vision.PoseLandmarker.create_from_options(opciones_vision) as landmarker:
        while True:
            exito, frame = cap.read()
            if not exito:
                break

            # Modo espejo camara
            frame = cv2.flip(frame, 1)
            alto_frame, ancho_frame = frame.shape[:2]

            # MediaPipe formato RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_img    = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

            resultados = landmarker.detect(mp_img)

            # Valores por defecto si no hay nada
            estado_texto        = "Buscando cuerpo..."
            color_estado        = BLANCO
            tilt_cabeza         = 0.0
            tilt_hombros        = 0.0
            inclinacion_tronco  = 0.0
            ratio_altura_tronco = 0.0
            ratio_encorvamiento = 0.0
            ratio_apertura      = 0.0
            puntuacion_postura  = 0.0
            alerta_activa       = False

            if resultados.pose_landmarks:
                landmarks = resultados.pose_landmarks[0]

                #coordenadas clave
                nariz      = normalizar_a_pixeles(landmarks[IDX_NARIZ],      ancho_frame, alto_frame)
                oreja_izq  = normalizar_a_pixeles(landmarks[IDX_OREJA_IZQ],  ancho_frame, alto_frame)
                oreja_der  = normalizar_a_pixeles(landmarks[IDX_OREJA_DER],  ancho_frame, alto_frame)

                hombro_izq_crudo = list(normalizar_a_pixeles(landmarks[IDX_HOMB_IZQ],   ancho_frame, alto_frame))
                hombro_der_crudo = list(normalizar_a_pixeles(landmarks[IDX_HOMB_DER],   ancho_frame, alto_frame))
                cadera_izq_cruda =      normalizar_a_pixeles(landmarks[IDX_CADERA_IZQ], ancho_frame, alto_frame)
                cadera_der_cruda =      normalizar_a_pixeles(landmarks[IDX_CADERA_DER], ancho_frame, alto_frame)

                ancho_cabeza = calcular_distancia(oreja_izq, oreja_der)
                offset_y     = int(ancho_cabeza * OFFSET_SUPERIOR_HOMBRO)
                hombro_izq_crudo[1] -= offset_y
                hombro_der_crudo[1] -= offset_y

                hombro_izq = aplicar_suavizado(tuple(hombro_izq_crudo), buffer_hombro_izq)
                hombro_der = aplicar_suavizado(tuple(hombro_der_crudo), buffer_hombro_der)
                cadera_izq = aplicar_suavizado(cadera_izq_cruda,        buffer_cadera_izq)
                cadera_der = aplicar_suavizado(cadera_der_cruda,        buffer_cadera_der)

                centro_hombros = obtener_punto_medio(hombro_izq, hombro_der)
                centro_caderas = obtener_punto_medio(cadera_izq, cadera_der)

                # Cálculos inclinacion de lado a lado
                tilt_cabeza  = calcular_inclinacion(oreja_izq, oreja_der)
                tilt_hombros = calcular_inclinacion(hombro_izq, hombro_der)

                ancho_hombros = calcular_distancia(hombro_izq, hombro_der)
                altura_cuello = centro_hombros[1] - nariz[1]

                inclinacion_tronco = calcular_inclinacion_vertical(centro_caderas, centro_hombros)
                altura_tronco      = calcular_distancia(centro_caderas, centro_hombros)

                if ancho_hombros > 10 and ancho_cabeza > 10:
                    ratio_encorvamiento = altura_cuello / ancho_hombros
                    ratio_apertura      = ancho_hombros / ancho_cabeza
                    if altura_tronco > 10:
                        ratio_altura_tronco = altura_tronco / ancho_hombros
                es_mala_postura_frame, puntuacion_postura = evaluar_postura(
                    inclinacion_tronco  = inclinacion_tronco,
                    ratio_altura_tronco = ratio_altura_tronco,
                    tilt_cabeza         = tilt_cabeza,
                    ratio_encorvamiento = ratio_encorvamiento,
                    ratio_apertura      = ratio_apertura,
                    tilt_hombros        = tilt_hombros,
                )

                alerta_activa = gestor_alerta.actualizar(es_mala_postura_frame)

                if alerta_activa:
                    estado_texto = "ALERTA: Corrige tu postura"
                    color_estado = COLOR_ALERTA
                elif es_mala_postura_frame:
                    estado_texto = "INCORRECTA (ajustando...)"
                    color_estado = COLOR_INCORRECTO
                else:
                    estado_texto = "CORRECTA"
                    color_estado = COLOR_CORRECTO

                # lineas
                dibujar_esqueleto_postura(
                    frame,
                    nariz, oreja_izq, oreja_der,
                    hombro_izq, hombro_der, centro_hombros,
                    cadera_izq, cadera_der, centro_caderas,
                    color_estado,
                )

            # Diccionarioz
            if not resultados.pose_landmarks:
                estado_postura_dashboard = "SIN_DETECCION"
                tiempo_postura_dashboard = 0.0
                ts_inicio_buena_postura = None
            else:
                if alerta_activa:
                    estado_postura_dashboard = "ALERTA"
                    tiempo_postura_dashboard = round(gestor_alerta.duracion_mala_postura_actual, 2)
                    ts_inicio_buena_postura = None
                elif es_mala_postura_frame:
                    estado_postura_dashboard = "INCORRECTA"
                    tiempo_postura_dashboard = round(gestor_alerta.duracion_mala_postura_actual, 2)
                    ts_inicio_buena_postura = None
                else:
                    estado_postura_dashboard = "CORRECTA"
                    if ts_inicio_buena_postura is None:
                        ts_inicio_buena_postura = time.monotonic()
                    tiempo_postura_dashboard = round(time.monotonic() - ts_inicio_buena_postura, 2)

            # >> NOTA INTERNA DE BACKEND <<
            # En esta sección del flujo ya tienes disponibles:
            # - `estado_postura_dashboard` (String)
            # - `tiempo_postura_dashboard` (Float en segundos)
            # Puedes enviarlas por WebSockets, un cliente MQTT, o una cola de tareas.
            # ========================================================

            # =====================================================================
            # >>> AQUÍ SE ESCRIBEN LOS DATOS EN TIEMPO REAL EN LA VARIABLE GLOBAL <<<
            # =====================================================================
            _datos_dashboard["estado_postura"] = estado_postura_dashboard
            _datos_dashboard["tiempo_postura"] = tiempo_postura_dashboard

            # Textos
            fuente = cv2.FONT_HERSHEY_SIMPLEX
            dibujar_hud_metricas(
                frame, fuente,
                perfil_activo       = PERFIL_ACTIVO,
                tilt_cabeza         = tilt_cabeza,
                tilt_hombros        = tilt_hombros,
                inclinacion_tronco  = inclinacion_tronco,
                ratio_altura_tronco = ratio_altura_tronco,
                ratio_encorvamiento = ratio_encorvamiento,
                ratio_apertura      = ratio_apertura,
                puntuacion_postura  = puntuacion_postura,
                duracion_mala_postura = gestor_alerta.duracion_mala_postura_actual,
                estado_texto        = estado_texto,
                color_estado        = color_estado,
                alerta_activa       = alerta_activa,
            )

            cv2.imshow("PyVision - detector de postura", frame)

            # salir con la q
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()