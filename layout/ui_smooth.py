# Form implementation generated from reading ui file '/home/siwon/dev/smooth/layout/smooth.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(950, 578)
        self.groupBox = QtWidgets.QGroupBox(parent=Dialog)
        self.groupBox.setGeometry(QtCore.QRect(710, 20, 231, 151))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.ip_edt = QtWidgets.QLineEdit(parent=self.groupBox)
        self.ip_edt.setGeometry(QtCore.QRect(10, 30, 211, 21))
        self.ip_edt.setObjectName("ip_edt")
        self.port_edt = QtWidgets.QLineEdit(parent=self.groupBox)
        self.port_edt.setGeometry(QtCore.QRect(10, 80, 71, 21))
        self.port_edt.setReadOnly(True)
        self.port_edt.setObjectName("port_edt")
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 60, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 60, 60, 16))
        self.label_4.setObjectName("label_4")
        self.connecting_btn = QtWidgets.QPushButton(parent=self.groupBox)
        self.connecting_btn.setGeometry(QtCore.QRect(60, 110, 113, 32))
        self.connecting_btn.setObjectName("connecting_btn")
        self.label_9 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(0, 0, 231, 31))
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.groupBox_2 = QtWidgets.QGroupBox(parent=Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(710, 170, 231, 401))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 231, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.groupBox_3 = QtWidgets.QGroupBox(parent=self.groupBox_2)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 240, 211, 151))
        self.groupBox_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.groupBox_3.setObjectName("groupBox_3")
        self.MusicSlider = QtWidgets.QSlider(parent=self.groupBox_3)
        self.MusicSlider.setGeometry(QtCore.QRect(10, 120, 191, 16))
        self.MusicSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.MusicSlider.setObjectName("MusicSlider")
        self.btnMusic = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.btnMusic.setGeometry(QtCore.QRect(80, 80, 51, 31))
        self.btnMusic.setObjectName("btnMusic")
        self.btnBackMusic = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.btnBackMusic.setGeometry(QtCore.QRect(40, 80, 31, 31))
        self.btnBackMusic.setObjectName("btnBackMusic")
        self.btnPreviousMusic = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.btnPreviousMusic.setGeometry(QtCore.QRect(0, 80, 31, 31))
        self.btnPreviousMusic.setObjectName("btnPreviousMusic")
        self.btnGoMusic = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.btnGoMusic.setGeometry(QtCore.QRect(140, 80, 31, 31))
        self.btnGoMusic.setObjectName("btnGoMusic")
        self.btnNextMusic = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.btnNextMusic.setGeometry(QtCore.QRect(180, 80, 31, 31))
        self.btnNextMusic.setObjectName("btnNextMusic")
        self.music_edt = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.music_edt.setEnabled(False)
        self.music_edt.setGeometry(QtCore.QRect(10, 40, 191, 31))
        self.music_edt.setReadOnly(True)
        self.music_edt.setObjectName("music_edt")
        self.groupBox_4 = QtWidgets.QGroupBox(parent=self.groupBox_2)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 30, 211, 201))
        self.groupBox_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.groupBox_4.setObjectName("groupBox_4")
        self.emotion_edt = QtWidgets.QLineEdit(parent=self.groupBox_4)
        self.emotion_edt.setGeometry(QtCore.QRect(40, 30, 131, 31))
        self.emotion_edt.setReadOnly(True)
        self.emotion_edt.setObjectName("emotion_edt")
        self.B_led_edt = QtWidgets.QLineEdit(parent=self.groupBox_4)
        self.B_led_edt.setGeometry(QtCore.QRect(150, 90, 41, 21))
        self.B_led_edt.setReadOnly(True)
        self.B_led_edt.setObjectName("B_led_edt")
        self.label_6 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_6.setGeometry(QtCore.QRect(80, 90, 16, 16))
        self.label_6.setObjectName("label_6")
        self.G_led_edt = QtWidgets.QLineEdit(parent=self.groupBox_4)
        self.G_led_edt.setGeometry(QtCore.QRect(90, 90, 41, 21))
        self.G_led_edt.setReadOnly(True)
        self.G_led_edt.setObjectName("G_led_edt")
        self.R_led_edt = QtWidgets.QLineEdit(parent=self.groupBox_4)
        self.R_led_edt.setGeometry(QtCore.QRect(30, 90, 41, 21))
        self.R_led_edt.setText("")
        self.R_led_edt.setReadOnly(True)
        self.R_led_edt.setObjectName("R_led_edt")
        self.label_5 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_5.setGeometry(QtCore.QRect(20, 90, 16, 16))
        self.label_5.setObjectName("label_5")
        self.label_7 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_7.setGeometry(QtCore.QRect(140, 90, 16, 16))
        self.label_7.setObjectName("label_7")
        self.btnColorFalse = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.btnColorFalse.setGeometry(QtCore.QRect(30, 160, 151, 31))
        self.btnColorFalse.setObjectName("btnColorFalse")
        self.label_8 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_8.setGeometry(QtCore.QRect(80, 60, 51, 31))
        self.label_8.setObjectName("label_8")
        self.btnColorPicker = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.btnColorPicker.setGeometry(QtCore.QRect(40, 120, 131, 31))
        self.btnColorPicker.setObjectName("btnColorPicker")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(10, 30, 691, 541))
        self.label.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.label.setText("")
        self.label.setObjectName("label")
        self.cam_label = QtWidgets.QLabel(parent=Dialog)
        self.cam_label.setGeometry(QtCore.QRect(10, 10, 101, 16))
        self.cam_label.setObjectName("cam_label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_3.setText(_translate("Dialog", "IP"))
        self.label_4.setText(_translate("Dialog", "Port"))
        self.connecting_btn.setText(_translate("Dialog", "Connecting"))
        self.label_9.setText(_translate("Dialog", "< Connect >"))
        self.label_2.setText(_translate("Dialog", "< Current Status >"))
        self.groupBox_3.setTitle(_translate("Dialog", "< Music >"))
        self.btnMusic.setText(_translate("Dialog", "Stop"))
        self.btnBackMusic.setText(_translate("Dialog", "<"))
        self.btnPreviousMusic.setText(_translate("Dialog", "<<"))
        self.btnGoMusic.setText(_translate("Dialog", ">"))
        self.btnNextMusic.setText(_translate("Dialog", ">>"))
        self.groupBox_4.setTitle(_translate("Dialog", "< Mood Light >"))
        self.label_6.setText(_translate("Dialog", "G"))
        self.label_5.setText(_translate("Dialog", "R"))
        self.label_7.setText(_translate("Dialog", "B"))
        self.btnColorFalse.setText(_translate("Dialog", "Emotion color set"))
        self.label_8.setText(_translate("Dialog", "< LED >"))
        self.btnColorPicker.setText(_translate("Dialog", "Color Set"))
        self.cam_label.setText(_translate("Dialog", "Cam Off"))
