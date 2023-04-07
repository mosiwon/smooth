import sys
import time
import socket
import cv2
import numpy as np
import imutils
import mediapipe as mp
import pygame
from mutagen.mp3 import MP3
from struct import Struct
from collections import deque, Counter
from datetime import datetime
from PyQt6.QtCore import QRegularExpression, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap, QImage, QColorDialog, QRegularExpressionValidator
from PyQt6.QtWidgets import QMainWindow, QIntValidator
from PyQt6 import uic
from hsemotion_onnx.facial_emotions import HSEmotionRecognizer



class Camera(QThread):
    update = pyqtSignal()

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.running = True

    def run(self):
        while self.running:
            self.update.emit()
            time.sleep(0.05)

    def stop(self):
        self.running = False


from_class = uic.loadUiType("/home/siwon/dev/smooth/layout/smooth.ui")[0]


class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Smart Moodlight Speaker")
        self.init_variables()
        self.init_emotion_recognition()
        self.init_music_player()
        self.init_connections()

    def init_variables(self):
        self.connect = False
        self.cam = False
        ip_range = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegex = QRegularExpression(
            "^" + ip_range + "\\." + ip_range + "\\." + ip_range + "\\." + ip_range + "$")
        self.ip_edt.setValidator(QRegularExpressionValidator(ipRegex, self))
        self.port_edt.setValidator(QIntValidator())
        self.port_edt.setText("80")
        self.pixmap = QPixmap()
        self.camera = Camera(self)
        self.camera.daemon = True
        self.image = None

    def init_emotion_recognition(self):
        self.emotion_mean = 'Neutral'
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

        self.emotion_edt.setText("보통")

    def init_music_player(self):
        while len(self.emotion_queue) < 300:
            self.emotion_queue.append('Neutral')

        self.pickerModeOn = False
        self.format = struct.Struct("BBB")
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

        self.musicison = False
        self.music_list = self.neutral_music_list
        self.music_index = 0
        self.music = self.music_list[self.music_index]
        self.stopped_position = 0
        self.current_position = 0
        self.emotion_music_list = self.neutral_music_list

        self.MusicSlider.setDisabled(True)

    def init_connections(self):
        self.connecting_btn.clicked.connect(self.toggle_connection)
        self.camera.update.connect(self.camUpdate)
        self.emotion_edt.textChanged.connect(self.emotion_edt_changed)
        self.btnColorPicker.clicked.connect(self.btnColorPicker_clicked)
        self.btnColorFalse.clicked.connect(self.btnColorModeFalse_clicked)
        self.btnMusic.clicked.connect(self.btnMusic_clicked)
        self.btnNextMusic.clicked.connect(self.btnNextMusic_clicked)
        self.btnPreviousMusic.clicked.connect(self.btnPreviousMusic_clicked)
        self.btnGoMusic.clicked.connect(self.btnGoMusic_clicked)
        self.btnBackMusic.clicked.connect(self.btnBackMusic_clicked)

    def getQImage(self, frame):
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QImage(frame.data, width, height,
                      bytesPerLine, QImage.Format_RGB888)
        return qImg.rgbSwapped()

    def toggle_connection(self):
        if not self.connect:
            self.connect_to_device()
        else:
            self.disconnect_from_device()

    def connect_to_device(self):
        ip = self.ip_edt.text()
        port = self.port_edt.text()
        self.sock = socket.socket()
        self.sock.connect((ip, int(port)))
        self.connect = True
        self.cam = True
        self.connecting_btn.setText("Disconnecting")
        self.cam_label.setText("Cam On")
        self.camStart()
        self.musicison = True
        self.btnMusic_clicked()

    def disconnect_from_device(self):
        self.connect = False
        self.cam = False
        self.connecting_btn.setText("Connecting")
        self.cam_label.setText("Cam Off")
        self.sock.close()
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
            image = self.process_image(image)
            self.update_emotion_ui()
            self.display_image(image)

    def process_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = imutils.resize(image, width=400)
        return self.emotion_detector(image)

    def display_image(self, image):
        h, w, c = image.shape
        qImg = QImage(image.data, w, h, w * c, QImage.Format.Format_RGB888)
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
        emotions_data = {
            'Anger': ('분노', 'rgb(255, 0, 0)', (255, 0, 0), 0),
            'Contempt': ('경멸', 'rgb(255, 255, 0)', (255, 255, 0), 1),
            'Disgust': ('혐오', 'rgb(0, 128, 0)', (0, 128, 0), 2),
            'Fear': ('공포', 'rgb(0, 0, 255)', (0, 0, 255), 3),
            'Happiness': ('행복', 'rgb(255, 192, 203)', (255, 192, 203), 4),
            'Neutral': ('보통', 'rgb(128, 128, 128)', (128, 128, 128), 5),
            'Sadness': ('슬픔', 'rgb(0, 255, 255)', (0, 255, 255), 6),
            'Surprise': ('놀람', 'rgb(128, 0, 128)', (128, 0, 128), 7)
        }
        if self.emotion_mean in emotions_data:
            emotion_text, color, rgb, music_index = emotions_data[self.emotion_mean]
            self.emotion_edt.setStyleSheet(f"color: {color};")
            self.colorUpdate(rgb[0], rgb[1], rgb[2], 1)
            self.musicUpdate(music_index)
            self.emotion_edt.setText(emotion_text)

    def btnColorPicker_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.pickerModeOn = True
            self.btnColorPicker.setStyleSheet(
                "background-color: {}".format(color.name()))
            r, g, b = color.getRgb()[:3]
            self.colorUpdate(r, g, b, 0)

    def colorUpdate(self, r, g, b, mode=1):
        self.emotion_r = r
        self.emotion_g = g
        self.emotion_b = b

        if mode == 1 and not self.pickerModeOn or mode == 0 and self.pickerModeOn:
            self.R_led_edt.setText(str(r))
            self.G_led_edt.setText(str(g))
            self.B_led_edt.setText(str(b))
            self.sendRGB(r, g, b)

    def sendRGB(self, r, g, b):
        data = self.format.pack(r, g, b)
        self.sock.send(data)

    def btnColorModeFalse_clicked(self):
        self.pickerModeOn = False

    def musicUpdate(self, emotion):
        emotion_music_lists = [
            self.angry_music_list, self.contempt_music_list,
            self.disgust_music_list, self.fear_music_list,
            self.happy_music_list, self.neutral_music_list,
            self.sad_music_list, self.surprise_music_list
        ]
        self.emotion_music_list = emotion_music_lists[emotion] if 0 <= emotion < len(
            emotion_music_lists) else self.neutral_music_list

    def emotion_edt_changed(self):
        self.music_list[self.music_index + 1:] = self.emotion_music_list
        pygame.mixer.music.fadeout(4000)  # Fade out for 2 seconds
        self.btnNextMusic_clicked()

    def update_MusicSlider(self):
        if pygame.mixer.music.get_busy():
            self.current_position += 1

        self.MusicSlider.setValue(self.current_position)

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

        pygame.mixer.music.play(start=start_position)
        pygame.mixer.music.set_volume(1)

        if self.music_timer is not None:
            self.music_timer.stop()

        self.music_timer = QTimer()
        self.music_timer.timeout.connect(self.update_MusicSlider)
        self.music_timer.start(1000)

        print('--------------------------')
        for i, m in enumerate(self.music_list):
            print(m + " (현재 재생중)" if i == self.music_index else m)

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
        self.music_index += 1
        self.music = self.music_list[self.music_index]
        self.current_position = 0
        self.play_music()

    def btnPreviousMusic_clicked(self):
        self.music_index -= 1
        self.music = self.music_list[self.music_index]
        self.current_position = 0
        self.play_music()

    def btnGoMusic_clicked(self):
        self.current_position += 15
        self.play_music(start_position=self.current_position)

    def btnBackMusic_clicked(self):
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
