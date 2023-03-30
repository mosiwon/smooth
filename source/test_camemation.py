import sys
import time
import cv2
import numpy as np
import mediapipe as mp
from collections import deque

from hsemotion_onnx.facial_emotions import HSEmotionRecognizer

def process_video(videofile=0):
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    
    face_mesh=mp_face_mesh.FaceMesh(max_num_faces=1,refine_landmarks=True,min_detection_confidence=0.5,min_tracking_confidence=0.5)

    model_name='enet_b0_8_best_vgaf'

    fer=HSEmotionRecognizer(model_name=model_name)
    
    emotion_queue=deque(maxlen=50000)

    maxlen=15 #51
    recent_scores=deque(maxlen=maxlen)

    cap = cv2.VideoCapture(videofile)
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        total_start = time.time()
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        start = time.time()
        results = face_mesh.process(image_rgb)
        elapsed = (time.time() - start)
        #print('Face mesh elapsed:',elapsed)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if results.multi_face_landmarks:
            height,width,_=image.shape
            for face_landmarks in results.multi_face_landmarks:
                if False:
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACE_CONNECTIONS,
                        landmark_drawing_spec=drawing_spec,
                        connection_drawing_spec=drawing_spec)
                x1 = y1 = 1
                x2 = y2 = 0
                for id, lm in enumerate(face_landmarks.landmark):
                    cx, cy = lm.x, lm.y
                    if cx<x1:
                        x1=cx
                    if cy<y1:
                        y1=cy
                    if cx>x2:
                        x2=cx
                    if cy>y2:
                        y2=cy
                if x1<0:
                    x1=0
                if y1<0:
                    y1=0
                x1,x2=int(x1*width),int(x2*width)
                y1,y2=int(y1*height),int(y2*height)
                face_img=image_rgb[y1:y2,x1:x2,:]
                if np.prod(face_img.shape)==0:
                    #print('Empty face ', x1,x2,y1,y2)
                    continue
                
                start = time.time()
                emotion,scores=fer.predict_emotions(face_img,logits=True)
                elapsed = (time.time() - start)
                recent_scores.append(scores)

                ## queue에 저장된 emotion들의 평균을 계산
                # 먼저 emotion_queue에 emotion 저장
                emotion_queue.append(emotion)
                # emotion_queue에 저장된 emotion중에서 가장 많이 나온 emotion을 emotion_mean으로 설정
                emotion_mean = max(set(emotion_queue), key=emotion_queue.count)
                print(emotion_mean)
                
                scores=np.mean(recent_scores,axis=0)
                emotion=np.argmax(scores)
                #rint(scores,fer.idx_to_class[emotion], 'Emotion elapsed:',elapsed)
                
                cv2.rectangle(image, (x1,y1), (x2,y2), (255, 0, 0), 2)
                fontScale=1
                min_y=y1
                if min_y<0:
                    min_y=10
                cv2.putText(image, fer.idx_to_class[emotion], (x1, min_y), cv2.FONT_HERSHEY_PLAIN , fontScale=fontScale, color=(0,255,0), thickness=1)
        else:
            print('No face detected')      
        elapsed = (time.time() - total_start)
        #print('Total frame processing elapsed:',elapsed)
        cv2.imshow('Facial emotions', image)
        if cv2.waitKey(5) & 0xFF == 27:
          break

    face_mesh.close()
    cap.release()

if __name__ == '__main__':
    if len(sys.argv)==2:
        process_video(sys.argv[1])
    else:
        process_video()