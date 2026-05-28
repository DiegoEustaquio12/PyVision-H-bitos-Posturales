import cv2
import mediapipe as mp 
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions
import time

result_list = []

#Funcion callback para procesar resultados
def res_callback(result, output_image, timestamp_ms):
    result_list.append(result)
    
#Especificar la configuracion
#Especificar la configuracion
options = vision.PoseLandmarkerOptions(
    base_options = BaseOptions(model_asset_path="pose_landmarker_full.task"),
    running_mode = vision.RunningMode.LIVE_STREAM,
    result_callback = res_callback
)
landmarker = vision.PoseLandmarker.create_from_options(options)

#leer el video
#1 webcam EMEET
#0 webcam Predeterminada
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame,1)
    
    h,w, _ = frame.shape
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frameRGB = mp.Image(image_format=mp.ImageFormat.SRGB, data = frameRGB)
    
    #obtener los resultados
    landmarker.detect_async(frameRGB, time.time_ns() // 1_000_000)
    
    if result_list:
        for lm in result_list[0].pose_landmarks:
            for each_lm in lm:
                if each_lm.visibility > 0.9:
                    x = int(each_lm.x * w)
                    y = int(each_lm.y * h)
                    cv2.circle(frame, (x, y), 4, (0, 0, 255), -1)
                    #linea (img, puntoInicio, PuntoFinal, color, grosor)
           
        cv2.line(frame, (int(lm[12].x * w), int(lm[12].y * h) ), (int(lm[11].x * w), int(lm[11].y * h)), (255, 0, 0), 2)  
        cv2.line(frame, (int(lm[10].x * w), int(lm[10].y * h) ), (int(lm[9].x * w), int(lm[9].y * h)), (255, 0, 0), 2)  
        cv2.line(frame, (int(lm[12].x * w), int(lm[12].y * h) ), (int(lm[0].x * w), int(lm[0].y * h)), (255, 0, 0), 2)  
        cv2.line(frame, (int(lm[0].x * w), int(lm[0].y * h) ), (int(lm[11].x * w), int(lm[11].y * h)), (255, 0, 0), 2)  
        cv2.line(frame, (int(lm[8].x * w), int(lm[8].y * h) ), (int(lm[7].x * w), int(lm[7].y * h)), (255, 0, 0), 2)  
         #rectangulo (img, puntoInicio, PuntoFinal, color, grosor)
        
        result_list.clear()
    cv2.imshow("video", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release
cv2.destroyAllWindows()