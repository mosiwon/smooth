import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import uic
from PyQt6.QtCore import QRegularExpression
import socket
import time
from PyQt6.QtCore import *
import time
from struct import *
import datetime
import cv2
import imutils
from datetime import datetime
import numpy as np
import mediapipe as mp
from collections import deque
from hsemotion_onnx.facial_emotions import HSEmotionRecognizer
from collections import Counter
import pygame
from mutagen.mp3 import MP3


class Camera(QThread):
    update = pyqtSignal()

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.running = True

    def run(self):
        while self.running == True:
            self.update.emit()
            time.sleep(0.05)

    def stop(self):
        self.running = False

class ColorUpdateThread(QThread):
    def __init__(self, r, g, b, r_led_edt, g_led_edt, b_led_edt):
        self.r = r
        self.g = g
        self.b = b
        self.r_led_edt = r_led_edt
        self.g_led_edt = g_led_edt
        self.b_led_edt = b_led_edt
        super().__init__()

    def run(self):
        current_r, current_g, current_b = int(self.r_led_edt.text()), int(self.g_led_edt.text()), int(self.b_led_edt.text())
        for i in range(10):
            new_r = current_r + int((self.r - current_r) * (i + 1) / 10)
            new_g = current_g + int((self.g - current_g) * (i + 1) / 10)
            new_b = current_b + int((self.b - current_b) * (i + 1) / 10)
            self.r_led_edt.setText(str(new_r))
            self.g_led_edt.setText(str(new_g))
            self.b_led_edt.setText(str(new_b))
            time.sleep(0.1)
        self.r_led_edt.setText(str(self.r))
        self.g_led_edt.setText(str(self.g))
        self.b_led_edt.setText(str(self.b))

from_class = uic.loadUiType("/home/siwon/dev/smooth/layout/smooth.ui")[0]


class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Smart Moodlight Speaker")
######### esp 연결 관련 변수 #########
        self.connect = False
        self.cam = False

        # ip address
        ip_range = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegex = QRegularExpression("^" + ip_range + "\\." + ip_range + "\\." +
                                     ip_range + "\\." + ip_range + "$")

        self.ip_edt.setValidator(QRegularExpressionValidator(ipRegex, self))
        self.port_edt.setValidator(QIntValidator())
        self.port_edt.setText("80")

        self.pixmap = QPixmap()
        self.camera = Camera(self)
        self.camera.daemon = True

        self.image = None

        self.connecting_btn.clicked.connect(self.connecting)
        self.camera.update.connect(self.camUpdate)
######### esp 연결 관련 변수 #########
######### 색상 관련 변수 #########        
        self.R_led_edt.setText("0")
        self.G_led_edt.setText("0")
        self.B_led_edt.setText("0")
        self.color_update_thread = None
######### 색상 관련 변수 #########
######### 감정 인식 관련 변수 #########
        self.emotion_mean = 'Neutral'
        # Emotion Recognition
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(
            thickness=1, circle_radius=1)
        self.model_name = 'enet_b0_8_best_vgaf'
        self.fer = HSEmotionRecognizer(model_name=self.model_name)
        self.recent_scores = deque(maxlen=15)
        self.emotion_mean = None
        self.emotion_queue = deque(maxlen=500)

        # emotion_edt가 바뀔때
        self.emotion_edt.setText("보통")
        self.emotion_edt.textChanged.connect(self.emotion_edt_changed)
######### 감정 인식 관련 변수 #########
######### 음악 재생 관련 변수 #########
        # whlie문으로 emotion_queue에 Neutral을 300번 넣어주기
        while len(self.emotion_queue) < 300:
            self.emotion_queue.append('Neutral')

        self.btnColorPicker.clicked.connect(self.btnColorPicker_clicked)
        self.btnColorFalse.clicked.connect(self.btnColorModeFalse_clicked)
        self.pickerModeOn = False

        # 음악(각 감정(8개) 별로 4개) (mp3))불러오기(각 리스트별로 만듬)
        self.angry_music_list = []
        self.contempt_music_list = []
        self.disgust_music_list = []
        self.fear_music_list = []
        self.happy_music_list = []
        self.neutral_music_list = []
        self.sad_music_list = []
        self.surprise_music_list = []

        for i in range(1, 5):
            self.angry_music_list.append(
                (f"/home/siwon/dev/smooth/data/music/0/{i}.mp3"))
            self.contempt_music_list.append(
                (f"/home/siwon/dev/smooth/data/music/1/{i}.mp3"))
            self.disgust_music_list.append(
                (f"/home/siwon/dev/smooth/data/music/2/{i}.mp3"))
            self.fear_music_list.append(
                (f"/home/siwon/dev/smooth/data/music/3/{i}.mp3"))
            self.happy_music_list.append(
                (f"/home/siwon/dev/smooth/data/music/4/{i}.mp3"))
            self.neutral_music_list.append(
                (f"/home/siwon/dev/smooth/data/music/5/{i}.mp3"))
            self.sad_music_list.append(
                (f"/home/siwon/dev/smooth/data/music/6/{i}.mp3"))
            self.surprise_music_list.append(
                (f"/home/siwon/dev/smooth/data/music/7/{i}.mp3"))

        self.music_timer = None

        self.btnMusic.clicked.connect(self.btnMusic_clicked)
        self.musicison = False
        self.music_list = self.neutral_music_list
        self.music_index = 0
        self.music = self.music_list[self.music_index]
        self.stopped_position = 0
        self.current_position = 0
        self.emotion_music_list = self.neutral_music_list
        # 슬라이더 못 움직이게 하기
        self.MusicSlider.setDisabled(True)
        self.btnNextMusic.clicked.connect(self.btnNextMusic_clicked)
        self.btnPreviousMusic.clicked.connect(self.btnPreviousMusic_clicked)
        self.btnGoMusic.clicked.connect(self.btnGoMusic_clicked)
        self.btnBackMusic.clicked.connect(self.btnBackMusic_clicked)
######### 음악 재생 관련 변수 #########

    def getQImage(self, frame):
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QImage(frame.data, width, height,
                      bytesPerLine, QImage.Format_RGB888)
        return qImg.rgbSwapped()

    def connecting(self):
        # 연결O
        if self.connect == False:
            # ip, port 연결
            # ip = self.ip_edt.text()
            # port = self.port_edt.text()
            # self.sock = socket.socket()
            # self.sock.connect((ip, int(port)))
            self.connect = True
            self.cam = True
            self.connecting_btn.setText("Disconnecting")
            self.cam_label.setText("Cam On")
            self.camStart()
            self.musicison = True
            self.btnMusic_clicked()
        # 연결X
        else:
            self.connect = False
            self.cam = False
            self.connecting_btn.setText("Connecting")
            self.cam_label.setText("Cam Off")
            # self.sock.close()
            self.camStop()
            self.musicison = False
            self.btnMusic_clicked()

    def camStart(self):
        self.cam_thread = Camera()
        self.cam_thread.update.connect(self.camUpdate)
        self.cam_thread.start()
        self.cap = cv2.VideoCapture(0)

    def camStop(self):
        self.cam_thread.stop()
        self.cam_thread.wait()

    def camUpdate(self):
        retval, image = self.cap.read()
        if retval:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = imutils.resize(image, width=400)
            image = self.emotion_detector(image)
            self.update_emotion_ui()

            h, w, c = image.shape
            qImg = QImage(image.data, w, h, w*c, QImage.Format.Format_RGB888)

            self.pixmap = self.pixmap.fromImage(qImg)
            self.pixmap = self.pixmap.scaled(
                self.label.width(), self.label.height())

            self.label.setPixmap(self.pixmap)

    def emotion_detector(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        results = self.face_mesh.process(image_rgb)
        height, width, _ = image.shape
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                x1 = y1 = 1
                x2 = y2 = 0
                for id, lm in enumerate(face_landmarks.landmark):
                    cx, cy = lm.x, lm.y
                    if cx < x1:
                        x1 = cx
                    if cy < y1:
                        y1 = cy
                    if cx > x2:
                        x2 = cx
                    if cy > y2:
                        y2 = cy
                x1, x2 = int(x1 * width), int(x2 * width)
                y1, y2 = int(y1 * height), int(y2 * height)
                face_img = image_rgb[y1:y2, x1:x2, :]
                if np.prod(face_img.shape) == 0:
                    continue
                emotion, scores = self.fer.predict_emotions(
                    face_img, logits=True)

                self.recent_scores.append(scores)
                scores = np.mean(self.recent_scores, axis=0)
                emotion = np.argmax(scores)
                # emotion을 문자열로 변환
                emotion_str = self.fer.idx_to_class[emotion]
                # emotion_queue에 문자열 emotion 추가
                self.emotion_queue.append(emotion_str)
                self.emotion_mean = max(
                    set(self.emotion_queue), key=self.emotion_queue.count)

                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                min_y = y1 if y1 >= 0 else 10
                cv2.putText(image, self.fer.idx_to_class[emotion], (
                    x1, min_y), cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(0, 255, 0), thickness=1)

        return image

    def update_emotion_ui(self):
        # emotion_edt 에 emotion_mean 출력
        # self.emotion_edt.setText(self.emotion_mean)

        # emotion_mean에 따라 R,G,B 변경
        if self.emotion_mean == 'Anger':
            self.emotion_edt.setStyleSheet("color: rgb(255, 0, 0);")
            self.colorUpdate(255, 0, 0, 1)
            self.musicUpdate(0)
            self.emotion_edt.setText("분노")

        elif self.emotion_mean == 'Contempt':
            self.emotion_edt.setStyleSheet("color: rgb(255, 255, 0);")
            self.colorUpdate(255, 255, 0, 1)
            self.musicUpdate(1)
            self.emotion_edt.setText("경멸")

        elif self.emotion_mean == 'Disgust':
            self.emotion_edt.setStyleSheet("color: rgb(0, 128, 0);")
            self.colorUpdate(0, 128, 0, 1)
            self.musicUpdate(2)
            self.emotion_edt.setText("혐오")

        elif self.emotion_mean == 'Fear':
            self.emotion_edt.setStyleSheet("color: rgb(0, 0, 255);")
            self.colorUpdate(0, 0, 255, 1)
            self.musicUpdate(3)
            self.emotion_edt.setText("공포")

        elif self.emotion_mean == 'Happiness':
            self.emotion_edt.setStyleSheet("color: rgb(255, 192, 203);")
            self.colorUpdate(255, 192, 203, 1)
            self.musicUpdate(4)
            self.emotion_edt.setText("행복")

        elif self.emotion_mean == 'Neutral':
            self.emotion_edt.setStyleSheet("color: rgb(128, 128, 128);")
            self.colorUpdate(128, 128, 128, 1)
            self.musicUpdate(5)
            self.emotion_edt.setText("보통")

        elif self.emotion_mean == 'Sadness':
            self.emotion_edt.setStyleSheet("color: rgb(0, 255, 255);")
            self.colorUpdate(0, 255, 255, 1)
            self.musicUpdate(6)
            self.emotion_edt.setText("슬픔")

        elif self.emotion_mean == 'Surprise':
            self.emotion_edt.setStyleSheet("color: rgb(128, 0, 128);")
            self.colorUpdate(128, 0, 128, 1)
            self.musicUpdate(7)
            self.emotion_edt.setText("놀람")

    def btnColorPicker_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.pickerModeOn = True
            self.btnColorPicker.setStyleSheet(
                "background-color: {}".format(color.name()))
            r, g, b = color.getRgb()[:3]
            self.colorUpdate(r, g, b, 0)

    def colorUpdate(self, r, g, b, mode=1):
        if mode == 1:
            if self.pickerModeOn:
                pass
            else:
                pass
        elif mode == 0:
            if self.pickerModeOn:
                self.color_update_thread = ColorUpdateThread(r, g, b, self.R_led_edt, self.G_led_edt, self.B_led_edt)
                self.color_update_thread.start()
            else:
                pass

    def btnColorModeFalse_clicked(self):
        self.pickerModeOn = False

    def musicUpdate(self, emotion):
        if emotion == 0:  # 분노
            self.emotion_music_list = self.angry_music_list
        elif emotion == 1:  # 경멸
            self.emotion_music_list = self.contempt_music_list
        elif emotion == 2:  # 혐오
            self.emotion_music_list = self.disgust_music_list
        elif emotion == 3:  # 공포
            self.emotion_music_list = self.fear_music_list
        elif emotion == 4:  # 행복
            self.emotion_music_list = self.happy_music_list
        elif emotion == 5:  # 보통
            self.emotion_music_list = self.neutral_music_list
        elif emotion == 6:  # 슬픔
            self.emotion_music_list = self.sad_music_list
        elif emotion == 7:  # 놀람
            self.emotion_music_list = self.surprise_music_list
        else:  # 예외처리
            self.emotion_music_list = self.neutral_music_list

    def emotion_edt_changed(self):
        # self.music_list에서 현재 음악 인덱스+1부터 전부 삭제
        for i in range(self.music_index+1, len(self.music_list)):
            self.music_list.pop()
        # self.emotion_music_list를 self.music_list에 추가
        for i in range(len(self.emotion_music_list)):
            self.music_list.append(self.emotion_music_list[i])
        # 다음곡 재생
        
        pygame.mixer.music.fadeout(4000)  # Fade out for 2 seconds
        
        r, g, b = self.get_emotion_color()
        self.color_update_thread = ColorUpdateThread(r, g, b, self.R_led_edt, self.G_led_edt, self.B_led_edt)
        self.color_update_thread.start()
        
        self.btnNextMusic_clicked()


    def update_MusicSlider(self):
        # If the music is playing, update the current position
        if pygame.mixer.music.get_busy():
            self.current_position += 1
        # Update the slider's value
        self.MusicSlider.setValue(self.current_position)
        # print("Current position: {} seconds".format(self.current_position))

        # If the music has stopped playing, stop the timer and play the next music
        if not pygame.mixer.music.get_busy():
            self.music_timer.stop()
            self.music = self.next_music
            self.play_music(self.music)

    def play_music(self, music=None, start_position=0):
        if music is None:
            music = self.music

        pygame.mixer.init()
        audio = MP3(music)
        length = int(audio.info.length)
        self.MusicSlider.setMaximum(length)
        self.music_edt.setText(music)
        pygame.mixer.music.load(music)

        # 서서히 페이드인하는 코드 추가
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play(start=start_position)

        for i in range(20):
            pygame.mixer.music.set_volume(i / 20)
            time.sleep(0.05)
        pygame.mixer.music.set_volume(1)

        if self.music_timer is not None:
            self.music_timer.stop()

        self.music_timer = QTimer()
        self.music_timer.timeout.connect(self.update_MusicSlider)
        self.music_timer.start(1000)
        print('--------------------------')
        for i in range(len(self.music_list)):
            if i == self.music_index:
                print(self.music_list[i] + " (현재 재생중)")
            else:
                print(self.music_list[i])


    def btnMusic_clicked(self):
        self.musicison = not self.musicison
        if self.musicison:
            pygame.mixer.music.pause()
            self.stopped_position = self.current_position
            self.music_timer.stop()
            self.btnMusic.setText("Play")
        else:
            self.current_position = self.stopped_position
            self.play_music(start_position=self.stopped_position)
            self.btnMusic.setText("Stop")
            self.music_timer.start(1000)

    def btnNextMusic_clicked(self):
        # 인덱스를 이용한 다음곡 재생
        self.music_index += 1
        self.music = self.music_list[self.music_index]
        self.current_position = 0
        self.play_music()

    def btnPreviousMusic_clicked(self):
        # 인덱스를 이용한 이전곡 재생
        self.music_index -= 1
        self.music = self.music_list[self.music_index]
        self.current_position = 0
        self.play_music()

    def btnGoMusic_clicked(self):
        # 5초 앞으로 이동
        self.current_position += 15
        self.play_music(start_position=self.current_position)

    def btnBackMusic_clicked(self):
        # 5초 뒤로 이동
        self.current_position -= 15
        if self.current_position < 0:
            self.current_position = 0
        self.play_music(start_position=self.current_position)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec())

    '''
    분노: 주황 (RGB(255, 165, 0))
    경멸: 노랑 (RGB(255, 255, 0))
    혐오: 초록 (RGB(0, 128, 0))
    공포: 파랑 (RGB(0, 0, 255))
    행복: 핑크 (RGB(255, 192, 203))
    중립: 회색 (RGB(128, 128, 128))
    슬픔: 청록색 (RGB(0, 255, 255))
    놀람: 보라 (RGB(128, 0, 128))`
    '''
