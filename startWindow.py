import atexit
from PyQt5 import QtCore, QtGui, QtWidgets
from videoView1 import videoView  
from logger_config import queue_listener

class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MyMainWindow()
        self.ui.setupUi(self)
        self.video_view = None

    def closeEvent(self, event):
        print("Close event called")
        super().closeEvent(event)

class Ui_MyMainWindow(object):
    def setupUi(self, MyMainWindow):
        MyMainWindow.setObjectName("MyMainWindow")
        MyMainWindow.resize(800, 454)
        MyMainWindow.setToolTipDuration(-1)
        MyMainWindow.setStyleSheet("background-color: rgb(19, 48, 79);")
        MyMainWindow.setIconSize(QtCore.QSize(100, 100))
        self.centralwidget = QtWidgets.QWidget(MyMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 40, 521, 41))
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.fromCameraButton = QtWidgets.QPushButton(self.centralwidget)
        self.fromCameraButton.setGeometry(QtCore.QRect(150, 250, 231, 71))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(180)
        sizePolicy.setVerticalStretch(180)
        sizePolicy.setHeightForWidth(self.fromCameraButton.sizePolicy().hasHeightForWidth())
        self.fromCameraButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(14)
        self.fromCameraButton.setFont(font)
        self.fromCameraButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.fromCameraButton.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.fromCameraButton.setToolTipDuration(5)
        self.fromCameraButton.setStyleSheet("background-color: rgb(211, 225, 240);\n"
                                             "border-radius: 16;")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/camera.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fromCameraButton.setIcon(icon)
        self.fromCameraButton.setIconSize(QtCore.QSize(48, 48))
        self.fromCameraButton.setObjectName("fromCameraButton")
        self.fromFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.fromFileButton.setGeometry(QtCore.QRect(420, 250, 231, 71))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(180)
        sizePolicy.setVerticalStretch(180)
        sizePolicy.setHeightForWidth(self.fromFileButton.sizePolicy().hasHeightForWidth())
        self.fromFileButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(14)
        self.fromFileButton.setFont(font)
        self.fromFileButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.fromFileButton.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.fromFileButton.setToolTipDuration(5)
        self.fromFileButton.setStyleSheet("background-color: rgb(211, 225, 240);\n"
                                           "border-radius: 16;")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/file-text.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fromFileButton.setIcon(icon1)
        self.fromFileButton.setIconSize(QtCore.QSize(48, 48))
        self.fromFileButton.setObjectName("images/fromFileButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 210, 461, 20))
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(140, 90, 541, 61))
        font = QtGui.QFont()
        font.setFamily("Rubik Glitch")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        MyMainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MyMainWindow)
        QtCore.QMetaObject.connectSlotsByName(MyMainWindow)

        # Підключення сигналів кнопок до відповідних методів
        self.fromCameraButton.clicked.connect(lambda: self.openVideoView(self.fromCameraButton))
        self.fromFileButton.clicked.connect(self.openFileDialog)

    def retranslateUi(self, MyMainWindow):
        _translate = QtCore.QCoreApplication.translate
        MyMainWindow.setWindowTitle(_translate("MyMainWindow", "Вхід в програму"))
        self.label.setText(_translate("MyMainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:400;\">Вітаємо в програмі</span></p></body></html>"))
        self.fromCameraButton.setText(_translate("MyMainWindow", "  з камери"))
        self.fromFileButton.setText(_translate("MyMainWindow", " з файлу"))
        self.label_2.setText(_translate("MyMainWindow", "Оберіть джерело для перегляду відеоданих:"))
        self.label_3.setText(_translate("MyMainWindow", "<html><head/><body><p align=\"center\">ВІДСТЕЖЕННЯ ОБ\'ЄКТІВ</p></body></html>"))

    def openFileDialog(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Вибрати відео', "", 'Video Files (*.mp4 *.avi *.mkv)')
        if filePath:
            self.openVideoView(self.fromFileButton, filePath)

    def openVideoView(self, button, filePath=None):
        self.ui = videoView()
        if button == self.fromCameraButton:
            self.ui.openCamera()  # Відкриття вебкамери
        else:
            if filePath:
                self.ui.set_video_path(filePath)  # Встановлення шляху до відеофайлу

        self.ui.show()

# Function to stop the queue listener at program exit
@atexit.register
def cleanup():
    queue_listener.stop()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MyMainWindow = MyMainWindow()
    MyMainWindow.show()
    sys.exit(app.exec_())