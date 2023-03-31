import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import uic
from PyQt6.QtCore import QRegularExpression
import socket
from PyQt6.QtCore import *
import time
from struct import *
from formatter import *
import datetime
import cv2, imutils
from datetime import datetime


# 카메라 쓰레드
class Camera(QThread):
    update = pyqtSignal()
    def __init__(self, sec=0,parent=None):
        super().__init__()
        self.main = parent
        self.running = True
    def run(self):
        while self.running == True:
            self.update.emit()
            time.sleep(0.05)
    def stop(self):
        self.running = False
    


from_class = uic.loadUiType("smooth.ui")[0]

class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Smart Moodlight Speaker")

        self.connect = False
        self.cam = False

        # ip address
        range = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegex = QRegularExpression("^" + range + "\\." + range + "\\." + \
                                        range + "\\." + range + "$")

        self.ip_edt.setValidator(QRegularExpressionValidator(ipRegex, self))
        self.port_edt.setValidator(QIntValidator())
        self.port_edt.setText("80")

        self.pixmap = QPixmap()
        self.camera = Camera(self)
        self.camera.daemon = True

        self.image = None

        self.connecting_btn.clicked.connect(self.connecting)
        self.camera.update.connect(self.camUpdate)
        




    def getQImage(self, frame):
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
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

        # 연결X
        else:
            self.connect = False
            self.cam = False
            self.connecting_btn.setText("Connecting")
            self.cam_label.setText("Cam Off")
            # self.sock.close()

            self.camStop()


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

            h, w, c = image.shape
            qImg = QImage(image.data, w, h, w*c, QImage.Format.Format_RGB888)

            self.pixmap = self.pixmap.fromImage(qImg)
            self.pixmap = self.pixmap.scaled(self.label.width(),self.label.height())

            self.label.setPixmap(self.pixmap)








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