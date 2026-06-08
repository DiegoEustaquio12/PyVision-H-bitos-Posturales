import os
import math
import urllib.request
from collections import deque

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# La API moderna de MediaPipe Tasks requiere el modelo físico (.task) en el equipo.
MODEL_PATH = "pose_landmarker_full.task"
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/1/pose_landmarker_full.task"

if not os.path.exists(MODEL_PATH):
    print("[INFO] Descargando modelo local de MediaPipe Pose...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

# Postura
# Tolerancias para vista frontal. Ajustar según la fisionomía del usuario objetivo.
MAX_INCLINACION_CABEZA  = 15.0  # Grados máximos permitidos de ladeo (oreja a oreja)
MAX_DESNIVEL_HOMBROS    = 10.0  # Grados máximos permitidos de desnivel (hombro a hombro)
MIN_RATIO_ENCORVAMIENTO = 0.42  # Relación mínima (altura cuello / ancho hombros)
MIN_RATIO_APERTURA      = 1.95  # Relación mínima (ancho hombros / ancho cabeza) para evitar colapso de pecho

# Compensación geométrica: Sube el punto base de los hombros un % respecto al ancho de la cabeza
OFFSET_SUPERIOR_HOMBRO  = 0.30  

# Suavizado de movimiento 
TAMANO_BUFFER = 5

# Paleta de colores 
COLOR_CORRECTO   = (40, 220, 100)  # Verde
COLOR_INCORRECTO = (50, 50, 240)   # Rojo
BLANCO           = (255, 255, 255)
AMARILLO         = (0, 230, 230)
OSCURO           = (20, 20, 20)

# Índices del esqueleto de MediaPipe
IDX_NARIZ = 0
IDX_OREJA_IZQ = 7; IDX_OREJA_DER = 8
IDX_HOMB_IZQ = 11; IDX_HOMB_DER = 12

# Colas de memoria para suavizar la vibración natural de los hombros
buffer_hombro_izq = deque(maxlen=TAMANO_BUFFER)
buffer_hombro_der = deque(maxlen=TAMANO_BUFFER)



def calcular_inclinacion(p1: tuple, p2: tuple) -> float:
    """Calcula los grados de desviación de una línea formada por p1 y p2 respecto al horizonte."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    if dx == 0: return 0.0
    return abs(math.degrees(math.atan(dy / dx)))

def calcular_distancia(p1: tuple, p2: tuple) -> float:
    """Retorna la distancia euclidiana en píxeles entre dos puntos bidimensionales."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def obtener_punto_medio(p1: tuple, p2: tuple) -> tuple:
    """Encuentra la coordenada central exacta entre dos puntos."""
    return (int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2))

def normalizar_a_pixeles(landmark, ancho: int, alto: int) -> tuple:
    """Convierte las coordenadas relativas de MediaPipe (0.0 a 1.0) a píxeles absolutos del frame."""
    return (int(landmark.x * ancho), int(landmark.y * alto))

def aplicar_suavizado(punto: tuple, buffer: deque) -> tuple:
    """Agrega un punto al buffer histórico y retorna la posición promedio para estabilizar visuales."""
    buffer.append(punto)
    promedio_x = int(sum(p[0] for p in buffer) / len(buffer))
    promedio_y = int(sum(p[1] for p in buffer) / len(buffer))
    return (promedio_x, promedio_y)




def main():
    # Configuración de rendimiento: Modo IMAGE procesa lo más rápido posible sin encolar frames
    opciones_vision = vision.PoseLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=vision.RunningMode.IMAGE,
        min_pose_detection_confidence=0.5,
        min_pose_presence_confidence=0.5,
        output_segmentation_masks=False
    )

    cap = cv2.VideoCapture(0)
    
    # Calidad y los fps
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_FPS, 30) 

    print("[INFO] Módulo de Visión Postural inicializado. Presiona 'q' en la ventana para salir.")

    with vision.PoseLandmarker.create_from_options(opciones_vision) as landmarker:
        while True:
            exito, frame = cap.read()
            if not exito:
                break

            # Modo espejo camara
            frame = cv2.flip(frame, 1)
            alto_frame, ancho_frame = frame.shape[:2]
            
            # MediaPipe requiere formato RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
            
            
            resultados = landmarker.detect(mp_img)

            # Valores por defecto si no hay detección
            estado_texto = "Buscando cuerpo..."
            color_estado = BLANCO
            tilt_cabeza = tilt_hombros = ratio_encorvamiento = ratio_apertura = 0.0

            if resultados.pose_landmarks:
                landmarks = resultados.pose_landmarks[0]

                # Extracción de coordenadas clave
                nariz = normalizar_a_pixeles(landmarks[IDX_NARIZ], ancho_frame, alto_frame)
                oreja_izq = normalizar_a_pixeles(landmarks[IDX_OREJA_IZQ], ancho_frame, alto_frame)
                oreja_der = normalizar_a_pixeles(landmarks[IDX_OREJA_DER], ancho_frame, alto_frame)
                
                hombro_izq_crudo = list(normalizar_a_pixeles(landmarks[IDX_HOMB_IZQ], ancho_frame, alto_frame))
                hombro_der_crudo = list(normalizar_a_pixeles(landmarks[IDX_HOMB_DER], ancho_frame, alto_frame))
                
                # Distancia hombros
                ancho_cabeza = calcular_distancia(oreja_izq, oreja_der)
                offset_y = int(ancho_cabeza * OFFSET_SUPERIOR_HOMBRO)
                hombro_izq_crudo[1] -= offset_y
                hombro_der_crudo[1] -= offset_y

                # Suavizado de puntos de los hombros
                hombro_izq = aplicar_suavizado(tuple(hombro_izq_crudo), buffer_hombro_izq)
                hombro_der = aplicar_suavizado(tuple(hombro_der_crudo), buffer_hombro_der)
                centro_hombros = obtener_punto_medio(hombro_izq, hombro_der)

                # Cálculos inclinacion de lado a lado 
                tilt_cabeza = calcular_inclinacion(oreja_izq, oreja_der)
                tilt_hombros = calcular_inclinacion(hombro_izq, hombro_der) 
                
                ancho_hombros = calcular_distancia(hombro_izq, hombro_der)
                altura_cuello = centro_hombros[1] - nariz[1] # Distancia vertical pura
                
                
                if ancho_hombros > 10 and ancho_cabeza > 10:
                    ratio_encorvamiento = altura_cuello / ancho_hombros
                    ratio_apertura = ancho_hombros / ancho_cabeza
                
                # la decisión de postura
                es_mala_postura = (
                    tilt_cabeza > MAX_INCLINACION_CABEZA or 
                    tilt_hombros > MAX_DESNIVEL_HOMBROS or 
                    ratio_encorvamiento < MIN_RATIO_ENCORVAMIENTO or
                    ratio_apertura < MIN_RATIO_APERTURA
                )
                
                if es_mala_postura:
                    estado_texto = "INCORRECTA (Abre el pecho)" if ratio_apertura < MIN_RATIO_APERTURA else "INCORRECTA"
                    color_estado = COLOR_INCORRECTO
                else:
                    estado_texto = "CORRECTA"
                    color_estado = COLOR_CORRECTO

                # lineas 
                cv2.line(frame, hombro_izq, hombro_der, color_estado, 3, cv2.LINE_AA)
                cv2.line(frame, oreja_izq, oreja_der, color_estado, 2, cv2.LINE_AA)
                cv2.line(frame, nariz, centro_hombros, color_estado, 4, cv2.LINE_AA)

                for punto in [oreja_izq, oreja_der, hombro_izq, hombro_der, nariz, centro_hombros]:
                    cv2.circle(frame, punto, 7, color_estado, -1)
                    cv2.circle(frame, punto, 9, BLANCO, 2)

           
            capa_sombra = frame.copy()
            cv2.rectangle(capa_sombra, (15, 15), (380, 170), OSCURO, -1)
            cv2.addWeighted(capa_sombra, 0.7, frame, 0.3, 0, frame)

            # Textos de monitoreo
            fuente = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, "MODULO VISION: ANALISIS FRONTAL", (25, 40), fuente, 0.55, AMARILLO, 2)
            cv2.putText(frame, f"Ladeo Cabeza : {tilt_cabeza:.1f} deg", (25, 65), fuente, 0.5, BLANCO, 1)
            cv2.putText(frame, f"Desnivel Homb: {tilt_hombros:.1f} deg", (25, 85), fuente, 0.5, BLANCO, 1)
            cv2.putText(frame, f"Nivel Rectitud: {ratio_encorvamiento:.2f} (Min {MIN_RATIO_ENCORVAMIENTO})", (25, 105), fuente, 0.5, BLANCO, 1)
            cv2.putText(frame, f"Apertura Pecho: {ratio_apertura:.2f} (Min {MIN_RATIO_APERTURA})", (25, 125), fuente, 0.5, BLANCO, 1)
            cv2.putText(frame, estado_texto, (25, 155), fuente, 0.6, color_estado, 2)

            cv2.imshow("PyVision - Módulo de Control Postural", frame)
            
            # salir con la q
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()