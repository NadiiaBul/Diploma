import cv2
import random
import logging
import os
import webbrowser
from logger_config import logger
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QMessageBox
from PyQt5.QtCore import QTimer, QDateTime
from detection import ObjectDetection


class Ui_videoView(object):

    def releaseCapture(self):
        if self.camera is not None:
            self.camera.release()
        else:
            print("in else")
            self.capture.release()

    def setPalleteForVideoView(self, videoView):
        #region Description
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(19, 48, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(19, 48, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(19, 48, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(19, 48, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)       
#endregion
        videoView.setPalette(palette)

    def setupUi(self, videoView):
        videoView.setObjectName("videoView")
        videoView.resize(1089, 980)

        self.setPalleteForVideoView(videoView)
        
        videoView.setStyleSheet("")
        self.font = QtGui.QFont("Candara")  # Задати шрифт
        self.font.setBold(True)
        self.font.setPointSize(8)
        self.height = 80
        self.width = 80
        self.detected_objects = []
        self.class_colors = {}
        self.startColor = (255, 255, 255)
        self.shouldTrack = False
        self.centralwidget = QtWidgets.QWidget(videoView)
        self.centralwidget.setMinimumSize(QtCore.QSize(1089, 0))
        self.centralwidget.setObjectName("centralwidget")
        
        self.scrollAreaObjects = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollAreaObjects.setGeometry(QtCore.QRect(10, 10, 221, 711))
        self.scrollAreaObjects.setMinimumSize(QtCore.QSize(221, 0))
        self.scrollAreaObjects.setWidgetResizable(True)
        self.scrollAreaObjects.setObjectName("scrollAreaObjects")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setEnabled(True)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 219, 719))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.menuWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.menuWidget.setObjectName("menuWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.menuWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.gridLayout.addWidget(self.menuWidget, 0, 0, 1, 1)
        self.scrollAreaObjects.setWidget(self.scrollAreaWidgetContents)
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(260, 10, 800, 460))
#region Palette
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
#endregion

        self.label.setPalette(palette)
        self.label.setAutoFillBackground(True)
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.mousePressEvent = self.getPos

        # Add scroll area for object list
        self.objectListArea = QtWidgets.QScrollArea(self.centralwidget)
        self.objectListArea.setGeometry(QtCore.QRect(260, 539, 800, 180))
        self.objectListArea.setWidgetResizable(True)
        self.objectListArea.setObjectName("objectListArea")

        self.objectListWidget = QtWidgets.QWidget()
        self.objectListWidget.setGeometry(QtCore.QRect(0, 0, 800, 180))
        self.objectListWidget.setObjectName("objectListWidget")
        self.objectListLayout = QtWidgets.QHBoxLayout(self.objectListWidget)
        self.objectListLayout.setObjectName("objectListLayout")
        self.objectListArea.setWidget(self.objectListWidget)

        #Pause/resume button
        self.pauseButton = QtWidgets.QPushButton(self.centralwidget)
        self.pauseButton.setGeometry(QtCore.QRect(640, 480, 48, 48))
        self.pauseButton.setStyleSheet("background-color: transparent;")
        self.pauseButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/pause-circle1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pauseButton.setIcon(icon1)
        self.pauseButton.setIconSize(QtCore.QSize(48, 48))
        self.pauseButton.setObjectName("pauseButton")
        self.pauseButton.clicked.connect(self.pauseVideo)

        #Відстеження об'єктів
        self.trackingButton = QtWidgets.QPushButton(self.centralwidget)
        self.trackingButton.setGeometry(QtCore.QRect(260, 800, 201, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.trackingButton.setFont(font)
        self.trackingButton.setStyleSheet("background-color: rgb(211, 225, 240); border-radius: 8;")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/Location.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.trackingButton.setIcon(icon2)
        self.trackingButton.setIconSize(QtCore.QSize(32, 32))
        self.trackingButton.setObjectName("trackingButton")
        self.trackingButton.clicked.connect(self.startTracking)

        self.labelTracking = QtWidgets.QLabel(self.centralwidget)
        self.labelTracking.setGeometry(QtCore.QRect(480, 800, 121, 41))
        self.labelTracking.setObjectName("labelTracking")
        self.comboBoxTracking = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxTracking.setGeometry(QtCore.QRect(610, 805, 132, 28))
        self.comboBoxTracking.setObjectName("comboBoxTracking")
        self.comboBoxTracking.addItems(["з моделлю", "без моделі"])
        self.comboBoxTracking.setStyleSheet("color: rgb(0, 0, 0);")
        self.comboBoxTracking.currentIndexChanged.connect(self.changeTrackingAlgorithm)

        #Трекер швидкості
        self.speedButton = QtWidgets.QPushButton(self.centralwidget)
        self.speedButton.setGeometry(QtCore.QRect(260, 740, 201, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.speedButton.setFont(font)
        self.speedButton.setStyleSheet("background-color: rgb(211, 225, 240); border-radius: 8;")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/Speedometer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.speedButton.setIcon(icon3)
        self.speedButton.setIconSize(QtCore.QSize(32, 32))
        self.speedButton.setObjectName("speedButton")
        self.showSpeed = False
        self.speedButton.clicked.connect(self.speed)

        self.labelLine = QtWidgets.QLabel(self.centralwidget)
        self.labelLine.setGeometry(QtCore.QRect(480, 740, 121, 41))
        self.labelLine.setObjectName("labelLine")
        self.comboBoxLine = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxLine.setGeometry(QtCore.QRect(610, 748, 132, 28))
        self.comboBoxLine.setObjectName("comboBoxLine")
        self.comboBoxLine.addItems(["по центру", "вгорі", "внизу"])
        self.comboBoxLine.setStyleSheet("color: rgb(0, 0, 0);")
        self.comboBoxLine.currentIndexChanged.connect(self.changeLinePosition)


        self.groupBoxInterface = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxInterface.setGeometry(QtCore.QRect(770, 740, 291, 221))
        self.groupBoxInterface.setStyleSheet("color: rgb(255, 255, 255);")
        self.groupBoxInterface.setObjectName("groupBoxInterface")

        self.fontSize = QtWidgets.QSpinBox(self.groupBoxInterface)
        self.fontSize.setGeometry(QtCore.QRect(220, 80, 48, 28))
        self.fontSize.setStyleSheet("color: rgb(0, 0, 0);")
        self.fontSize.setMinimum(1)
        self.fontSize.setMaximum(40)
        self.fontSize.setValue(8)
        self.fontSize.setObjectName("fontSize")

        #Налаштування розміру зображення
        self.spinBoxHeight = QtWidgets.QSpinBox(self.groupBoxInterface)
        self.spinBoxHeight.setGeometry(QtCore.QRect(220, 40, 48, 28))
        self.spinBoxHeight.setStyleSheet("color: rgb(0, 0, 0);")
        self.spinBoxHeight.setMinimum(10)
        self.spinBoxHeight.setMaximum(100)
        self.spinBoxHeight.setValue(80)
        self.spinBoxWidth = QtWidgets.QSpinBox(self.groupBoxInterface)
        self.spinBoxWidth.setGeometry(QtCore.QRect(90, 40, 48, 28))
        self.spinBoxWidth.setStyleSheet("color: rgb(0, 0, 0);")
        self.spinBoxWidth.setMinimum(10)
        self.spinBoxWidth.setMaximum(100)
        self.spinBoxWidth.setValue(80)
        self.spinBoxWidth.setObjectName("spinBoxWidth")
        self.spinBoxHeight.setObjectName("spinBoxHeight")
        self.width1 = QtWidgets.QLabel(self.groupBoxInterface)
        self.width1.setGeometry(QtCore.QRect(30, 40, 55, 28))
        self.width1.setObjectName("width1")
        self.height1 = QtWidgets.QLabel(self.groupBoxInterface)
        self.height1.setGeometry(QtCore.QRect(154, 40, 61, 28))
        self.height1.setObjectName("height1")

        #Налаштування шрифтів
        self.fontComboBox = QtWidgets.QFontComboBox(self.groupBoxInterface)
        self.fontComboBox.setGeometry(QtCore.QRect(30, 80, 181, 28))
        self.fontComboBox.setStyleSheet("color: rgb(0, 0, 0);")
        self.fontComboBox.setObjectName("fontComboBox")
        default_font = QtGui.QFont("Candara")
        self.fontComboBox.setCurrentFont(default_font)
         
        #Налаштування кольорів 
        self.colorLabel = QtWidgets.QLabel(self.groupBoxInterface)
        self.colorLabel.setObjectName("colorLabel")
        self.colorLabel.setGeometry(QtCore.QRect(30, 120, 91, 28))
        self.comboBoxColors = QtWidgets.QComboBox(self.groupBoxInterface)
        self.comboBoxColors.setGeometry(QtCore.QRect(123, 120, 144, 28))
        self.comboBoxColors.setCurrentText("")
        self.comboBoxColors.setObjectName("comboBoxColors")
        self.comboBoxColors.addItems(["Стандартний", "По класах", "Рандомний"])
        self.comboBoxColors.setStyleSheet("color: rgb(0, 0, 0);")

        #Налаштування параметрів інтерфейсу
        self.OKButton = QtWidgets.QPushButton(self.groupBoxInterface)
        self.OKButton.setGeometry(QtCore.QRect(29, 160, 241, 40))
        self.OKButton.setFont(font)
        self.OKButton.setStyleSheet("background-color: rgb(211, 225, 240); border-radius: 8;\n"
"color: rgb(0, 0, 0);")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("images/Settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.OKButton.setIcon(icon6)
        self.OKButton.setIconSize(QtCore.QSize(28, 28))
        self.OKButton.setObjectName("OKButton")
        self.OKButton.clicked.connect(self.applySettings)

        #Display infoLabel
        self.infoLabel = QtWidgets.QLabel(self.centralwidget)
        self.infoLabel.setGeometry(QtCore.QRect(260, 851, 481, 41))
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.infoLabel.setStyleSheet("background-color: rgb(255, 255, 255); border: 2px solid rgb(0, 0, 0);")
        self.infoLabel.setFont(font)
        self.infoLabel.setObjectName("infoLabel")

        self.parametersGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.parametersGroup.setGeometry(QtCore.QRect(260, 900, 481, 61))
        self.parametersGroup.setStyleSheet("color: rgb(255, 255, 255);")
        self.parametersGroup.setObjectName("parametersGroup")

        #Display frames
        self.checkBoxFrame = QtWidgets.QCheckBox(self.parametersGroup)
        self.checkBoxFrame.setEnabled(True)
        self.checkBoxFrame.setGeometry(QtCore.QRect(10, 30, 141, 20))
        self.checkBoxFrame.setObjectName("checkBoxFrame")
        self.checkBoxFrame.setChecked(True)
        self.checkBoxFrame.stateChanged.connect(self.toggleFrameDisplay)

        #Display colors
        self.checkBoxColors = QtWidgets.QCheckBox(self.parametersGroup)
        self.checkBoxColors.setGeometry(QtCore.QRect(260, 30, 181, 20))
        self.checkBoxColors.setObjectName("checkBoxColors")
        self.checkBoxColors.stateChanged.connect(self.toggleColorDisplay)

        self.time = QtWidgets.QLCDNumber(self.centralwidget)
        self.time.setGeometry(QtCore.QRect(10, 740, 221, 40))
        self.time.setObjectName("time")
        self.time.setSmallDecimalPoint(True)
        self.time.setDigitCount(8)

        #Сортування списку       
        self.comboBoxSort = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxSort.setGeometry(QtCore.QRect(360, 490, 132, 28))
        self.comboBoxSort.setObjectName("comboBoxSort")
        self.comboBoxSort.addItems(["спаданням %", "зростанням %"])
        self.comboBoxSort.setStyleSheet("color: rgb(0, 0, 0);")
        self.comboBoxSort.currentIndexChanged.connect(self.sortList)
        self.labelSort = QtWidgets.QLabel(self.centralwidget)
        self.labelSort.setGeometry(QtCore.QRect(260, 490, 101, 28))
        self.labelSort.setObjectName("labelSort")
        
        self.labelModel = QtWidgets.QLabel(self.centralwidget)
        self.labelModel.setGeometry(QtCore.QRect(840, 490, 61, 28))
        self.labelModel.setObjectName("labelModel")
        self.comboBoxModel = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxModel.setGeometry(QtCore.QRect(901, 490, 161, 28))
        self.comboBoxModel.setObjectName("comboBoxModel")
        self.comboBoxModel.addItems([" донавчена YOLOv8m", " стандартна YOLOv8m"])
        self.comboBoxModel.setStyleSheet("color: rgb(0, 0, 0);")
        self.comboBoxModel.currentIndexChanged.connect(self.changeTrackingAlgorithm)

        #Повернутися в головне меню
        self.backButton = QPushButton(self.centralwidget)
        self.backButton.setObjectName(u"backButton")
        self.backButton.setGeometry(QtCore.QRect(10, 920, 221, 40))
        self.backButton.setFont(font)
        self.backButton.setStyleSheet(u"background-color: rgb(211, 225, 240); border-radius: 8;")
        icon4 = QtGui.QIcon()
        icon4.addFile(u"images/back_button.png", QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backButton.setIcon(icon4)
        self.backButton.setIconSize(QtCore.QSize(32, 32))
        self.backButton.clicked.connect(self.openStartWindow)

        self.instructionButton = QPushButton(self.centralwidget)
        self.instructionButton.setObjectName("instructionButton")
        self.instructionButton.setGeometry(QtCore.QRect(10, 860, 221, 40))
        self.instructionButton.setFont(font)
        self.instructionButton.setStyleSheet("background-color: rgb(211, 225, 240); border-radius: 8;")
        icon7 = QtGui.QIcon()
        icon7.addFile("images/Instruction.png", QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.instructionButton.setIcon(icon7)
        self.instructionButton.setIconSize(QtCore.QSize(32, 32))
        self.instructionButton.clicked.connect(self.showInstruction)

        self.showLogsButton = QPushButton(self.centralwidget)
        self.showLogsButton.setObjectName("showLogsButton")
        self.showLogsButton.setGeometry(QtCore.QRect(10, 800, 221, 40))
        self.showLogsButton.setFont(font)
        self.showLogsButton.setStyleSheet("background-color: rgb(211, 225, 240); border-radius: 8;")
        icon5 = QtGui.QIcon()
        icon5.addFile("images/open_document.png", QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.showLogsButton.setIcon(icon5)
        self.showLogsButton.setIconSize(QtCore.QSize(32, 32))
        self.showLogsButton.setVisible(False)
        self.showLogsButton.clicked.connect(self.showLogs)

        self.defaultLeftPanel()

        videoView.setCentralWidget(self.centralwidget)

        self.retranslateUi(videoView)

        QtCore.QMetaObject.connectSlotsByName(videoView)

        # Створюємо таймер для оновлення годинника кожну секунду
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.displayWebcam)
        self.timer.start(30)  # Оновлення кадрів кожні 30 мс

        self.video_path = None
        self.capture = cv2.VideoCapture()
        self.camera = None
        self.detector = ObjectDetection()
        self.frame = None
        self.lcd_timer = QTimer()
        self.lcd_timer.timeout.connect(self.clock)
        self.lcd_timer.start() 

        self.activeClasses = []

        self.logger = logger

    def openStartWindow(self):
        self.close() 

    def showInstruction(self):
        # Зчитуємо вміст HTML-файлу
        webbrowser.open('instructions.html')
        
    def showLogs(self):
        log_file = 'example.log'
        if os.path.exists(log_file):
            os.startfile(log_file)  
        else:
            QtWidgets.QMessageBox.warning(None, "Увага", "Файл логів не знайдено!")
    
    def trackingAlgorithm(self, frame):
        current_index = self.comboBoxTracking.currentIndex()
        if current_index == 0:
            self.detector.track(frame)
        elif current_index == 1:
            self.detector.trackCSRT(frame)
    
    def changeTrackingAlgorithm(self):
        current_index = self.comboBoxTracking.currentIndex()
        if current_index == 1:
            self.detector.initTrackerCSRT(self.frame)
    
    def changeLinePosition(self):
        current_index = self.comboBoxLine.currentIndex()
        self.detector.setLinePts(current_index)

    def createClassElements(self, objects):
        names = self.detector.classNames()

        for object in objects:
            for box in object.boxes:
                print(f"CLASS: {names[int(box.cls.item())]}")
                className = names[int(box.cls.item())]
                if not className in self.activeClasses:
                    self.activeClasses.append(className)

                    widget = QtWidgets.QWidget(self.menuWidget)
                    widget.setObjectName(f"widget-{className}")
                    horizontalLayout = QtWidgets.QHBoxLayout(widget)
                    horizontalLayout.setContentsMargins(0, 0, 0, 0)
                    horizontalLayout.setObjectName(f"horizontalLayout-{className}")

                    mainObjectButton = QtWidgets.QPushButton(widget)
                    mainObjectButton.setAutoFillBackground(True)
                    mainObjectButton.setStyleSheet("")

                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap("images/Sort Right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    icon.addPixmap(QtGui.QPixmap("images/Sort Right1.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)

                    mainObjectButton.setIcon(icon)
                    mainObjectButton.setCheckable(True)
                    mainObjectButton.setFlat(True)
                    mainObjectButton.setObjectName(f"mainObjectButton-{className}")
                    mainObjectButton.setText(f"{className}")
                    mainObjectButton.setChecked(True)

                    horizontalLayout.addWidget(mainObjectButton)
                    self.verticalLayout_2.addWidget(widget)
                    objectsWidget = QtWidgets.QWidget(self.menuWidget)
                    objectsWidget.setObjectName(f"objects-{className}")
                    verticalLayout = QtWidgets.QVBoxLayout(objectsWidget)
                    verticalLayout.setObjectName(f"verticalLayout-{className}")
                    self.createChildElements(objects, objectsWidget, className, verticalLayout)
                    mainObjectButton.toggled['bool'].connect(objectsWidget.setVisible)
                    spacerItem = QtWidgets.QSpacerItem(20, 145, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                    self.verticalLayout_2.addItem(spacerItem)

    def createChildElements(self, objects, parent, parentName, verticalLayout):
        names = self.detector.classNames()
        for object in objects:
            for box in object.boxes:
                className = names[int(box.cls.item())]
                if className == parentName:
                    id = 0
                    if box.id == None:
                        continue
                    else:
                        id = box.id.item()
                    child = QtWidgets.QPushButton(parent)
                    child.setObjectName(f"child-id:{id}")
                    child.setText(f"{className}-id: {id}")
                    verticalLayout.addWidget(child)
                    self.verticalLayout_2.addWidget(parent)
    
    def clearElements(self):
        while self.verticalLayout_2.count():
            item = self.verticalLayout_2.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.activeClasses = []

    def createLeftPanelObjects(self, objects):
        
        self.createClassElements(objects)

    def defaultLeftPanel(self):
        self.widget = QtWidgets.QWidget(self.menuWidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.titleLabel = QtWidgets.QLabel(self.widget)
        self.titleLabel.setText("Спеціалізація")
        self.titleLabel.setFont(QtGui.QFont("Candara", 12, QtGui.QFont.Bold))
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setContentsMargins(0, 0, 0, 10)
        self.verticalLayout_2.addWidget(self.titleLabel)

        self.createSpoiler("Транспорт 🚗", "Модель донавчена для розпізнавання різних класів транспортних засобів, серед яких: \n🔸car;\n🔸bus;\n🔸bicycle;\n🔸truck.", "images/bus.png")
        self.createSpoiler("Люди 🧑", "Модель YOLO також донавчена для їх кращого розпізнавання класу 🔸person.", "images/person.png")
        self.createSpoiler("Дрони ⚡", "Клас 🔸drone був включений в датасет, щоб дозволити моделі виявляти дрони.", "images/drone.png")
        self.createSpoiler("Предмети 📚", "Нейронна модель донавчена для розпізнавання різних предметів побуту, зокрема: \n🔸book;\n🔸cup;\n🔸ruler;\n🔸phone.", "images/book.png")

        spacerItem = QtWidgets.QSpacerItem(20, 645, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.gridLayout.addWidget(self.menuWidget, 0, 0, 1, 1)
        self.scrollAreaObjects.setWidget(self.scrollAreaWidgetContents)        

    def createSpoiler(self, buttonText, labelText, imagePath):
        self.mainObjectButton = QtWidgets.QPushButton(self.widget)
        self.mainObjectButton.setAutoFillBackground(True)
        self.mainObjectButton.setStyleSheet("background-color: rgb(211, 225, 240); border-radius: 2;")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Sort Right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("images/Sort Right1.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.mainObjectButton.setIcon(icon)
        self.mainObjectButton.setCheckable(True)
        self.mainObjectButton.setFlat(True)
        self.mainObjectButton.setObjectName("mainObjectButton")
        self.mainObjectButton.setText(buttonText)
        self.mainObjectButton.setChecked(True)
        self.mainObjectButton.setFont(QtGui.QFont("Candara", 11))

        self.verticalLayout_2.addWidget(self.mainObjectButton)
        self.verticalLayout_2.addWidget(self.widget)
        self.objects = QtWidgets.QWidget(self.menuWidget)
        self.objects.setObjectName("objects")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.objects)
        self.verticalLayout.setObjectName("verticalLayout")
        self.object1 = QtWidgets.QLabel(self.objects)
        self.object1.setObjectName("object1")
        self.object1.setText(labelText)
        self.object1.setWordWrap(True)  
        self.object1.setMaximumWidth(160)  
        self.object1.setFont(QtGui.QFont("Calibri", 9))
        self.verticalLayout.addWidget(self.object1)

        self.imageLabel1 = QtWidgets.QLabel(self.objects)
        self.imageLabel1.setObjectName("imageLabel1")
        self.imageLabel1.setMaximumWidth(150)
        self.imageLabel1.setPixmap(QtGui.QPixmap(imagePath).scaledToWidth(150))
        self.imageLabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.imageLabel1)

        self.verticalLayout_2.addWidget(self.objects)
        self.mainObjectButton.toggled['bool'].connect(self.objects.setVisible)
    
    def startTracking(self):
        self.shouldTrack = not self.shouldTrack
        
        if not self.shouldTrack:
            self.logger.info("Stopped tracking!")
            self.detector.removeSelectedId()
            self.trackingButton.setStyleSheet("background-color: rgb(211, 225, 240); border-radius: 8;")
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap("images/Location.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.trackingButton.setIcon(icon2)
            self.trackingButton.setIconSize(QtCore.QSize(32, 32))
            self.trackingButton.setText("Відстеження об'єкту")
            self.clearElements()
            self.defaultLeftPanel()
        else:
            self.logger.info("Started tracking!")
            self.trackingButton.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 8;")
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap("images/Map_Marker.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.trackingButton.setIcon(icon2)
            self.trackingButton.setIconSize(QtCore.QSize(32, 32))
            self.trackingButton.setText("Зупинити відстеження")
            #self.pauseVideo()
            if self.detector.getTracks() == None:
                self.detector.track(self.frame)
            self.createLeftPanelObjects(self.detector.getTracks())

        self.setInfoLabelText(self.shouldTrack)

    def setInfoLabelText(self, shouldTrack = True):
        id = self.detector.getSelectedTrackedId()
        if id:
            self.infoLabel.setStyleSheet("color: rgb(1, 172, 38); background-color: rgb(255, 255, 255); border: 2px solid rgb(1, 172, 38);")
            self.infoLabel.setText(f"✅ Відстежуємо об'єкт з id {id}")
        elif shouldTrack:
            self.infoLabel.setStyleSheet("color: rgb(254,112,8); background-color: rgb(255, 255, 255); border: 2px solid rgb(254,112,8);")
            self.infoLabel.setText(f"🟠 Об'єкт для відстеження не обрано!")
        else:
            self.infoLabel.setStyleSheet("color: rgb(0,0,0); background-color: rgb(255, 255, 255); border: 2px solid rgb(0, 0, 0);")
            self.infoLabel.setText(f"❌ Відстеження вимкнено")
         
    def getPos(self, event):
        if self.shouldTrack:
            x = event.pos().x()
            y = event.pos().y()
            self.detector.getElementID(x, y)
            self.setInfoLabelText()

    def sortList(self):
        self.clearObjectList()
        self.showObjectList(False)   

    def getClassColor(self, className):
        if className not in self.class_colors:
            color = self.getRandomColor()
            self.class_colors[className] = color
        else:
            # Якщо для класу вже зберігався колір, поверніть його
            color = self.class_colors[className]
        return color

    def getRandomColor(self):
        # Генеруємо випадковий колір у форматі RGB
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        return (red, green, blue)
    
    def speed(self):
        self.showSpeed = not self.showSpeed
        if not self.showSpeed:
            self.logger.info("Stopped tracking speed!")
            self.speedButton.setStyleSheet("background-color: rgb(211, 225, 240); border-radius: 8;")
            icon3 = QtGui.QIcon()
            icon3.addPixmap(QtGui.QPixmap("images/Speedometer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.speedButton.setIcon(icon3)
            self.speedButton.setIconSize(QtCore.QSize(32, 32))
            self.speedButton.setText("Трекер швидкості")
        else:
            self.logger.info("Started tracking speed!")
            self.speedButton.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 8;")
            icon3 = QtGui.QIcon()
            icon3.addPixmap(QtGui.QPixmap("images/pause-circle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.speedButton.setIcon(icon3)
            self.speedButton.setIconSize(QtCore.QSize(32, 32))
            self.speedButton.setText("Вимкнути трекер")
    
    def applySettings(self):
        widthText = self.spinBoxWidth.text()
        heightText = self.spinBoxHeight.text()

        if not widthText or not heightText:
            QMessageBox.warning(self, "Попередження", "Будь ласка, введіть ширину і висоту.")
            return
        
        try:
            widthText = int(widthText)
            heightText = int(heightText)
        except ValueError:
            QMessageBox.warning(self, "Попередження", "Будь ласка, введіть цілі числа для ширини і висоти.")
            return
        
        if not (10 <= widthText <= 100) or not (10 <= heightText <= 100):
            QMessageBox.warning(self, "Попередження", "Ширина і висота має бути від 10 до 100.")
            return

        self.width = widthText
        self.heigth = heightText
        # Отримати обраний шрифт з fontComboBox
        self.font = self.fontComboBox.currentFont()

        self.font.setPointSize(int(self.fontSize.text()))
        self.clearObjectList()
        self.showObjectList(False)

    def toggleFrameDisplay(self, state):
        # Слот, який буде викликатися при зміні стану чекбоксу
        if state == QtCore.Qt.Checked:
            # Включення відображення рамок
            self.detector.show_frames = True
        else:
            # Вимкнення відображення рамок
            self.detector.show_frames = False

    def toggleColorDisplay(self, state):
        # Встановлюємо значення self.show_colors залежно від стану чекбокса
        self.detector.show_colors = state == QtCore.Qt.Unchecked

    def pauseVideo(self):
        if self.paused:
            self.timer.start()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("images/pause-circle1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pauseButton.setIcon(icon)
            self.pauseButton.setIconSize(QtCore.QSize(48, 48))
            self.showLogsButton.setVisible(False)
        else:
            self.timer.stop()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("images/play-circle1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pauseButton.setIcon(icon)
            self.pauseButton.setIconSize(QtCore.QSize(48, 48))
            self.showLogsButton.setVisible(True)
            self.clearObjectList()
            self.showObjectList()
        self.paused = not self.paused
        

    def showObjectList(self, detectNewObj=True):
        if detectNewObj:
            self.detected_objects, self.frame = self.detector.detect(self.frame, self.showSpeed, self.shouldTrack)

        sort_option = self.comboBoxSort.currentText()
        key_for_sorting = lambda obj: obj['confidence']

        # Перевірити, яке сортування вибрано
        if sort_option == "спаданням %":
            reverse_sorting = True
        else:
            reverse_sorting = False

        # Сортувати список об'єктів за відсотком впевненості
        sorted_objects = sorted(self.detected_objects, key=key_for_sorting, reverse=reverse_sorting)
        for obj in sorted_objects:
            object_container = QtWidgets.QWidget()
            container_layout = QtWidgets.QVBoxLayout()
            container_layout.setSpacing(0)
            
            # Додати зображення об'єкту
            object_image_label = QtWidgets.QLabel()
            resized_image = cv2.resize(obj['image'], (int(self.width), int(self.height)))  # Розмір зображення 
            h, w, ch = resized_image.shape
            bytesPerLine = ch * w
            qImg = QtGui.QImage(resized_image.tobytes(), w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            object_image_label.setPixmap(pixmap)
            container_layout.addWidget(object_image_label)

            # Словник емоджі для кожного класу
            emoji_dict = {
                'car': '🚘',
                'truck': '🚚',
                'bus': '🚌',
                'bicycle': '🚲',
                'drone': '🛸',
                'person': '🚶',
                'book': '📚',
                'cup': '☕',
                'ruler': '📏',
                'phone': '📱'
            }

            # Емоджі за замовчуванням
            default_emoji = '👁‍🗨'

            # Отримання емоджі відповідно до класу об'єкта, або емоджі за замовчуванням
            emoji = emoji_dict.get(obj['class_name'], default_emoji)
            

            # Додати назву класу та впевненість, емоджі додати для різних класів
            object_class_label = QtWidgets.QLabel(f"{emoji} "+obj['class_name'] + " " + str(round(obj['confidence'] * 100, 2)) + "%")

            option = self.comboBoxColors.currentText()
            if option == "Стандартний":
                object_class_label.setStyleSheet("color: rgb{};".format(self.startColor))
            elif option == "По класах":
                color = self.getClassColor(obj['class_name'])  # Повертає колір за назвою класу
                print(color)
                object_class_label.setStyleSheet("color: rgb{};".format(color))
            elif option == "Рандомний":
                random_color = self.getRandomColor()
                print(random_color)
                object_class_label.setStyleSheet("color: rgb{};".format(random_color))
            
            object_class_label.setFont(self.font)  # Встановити шрифт для тексту
            container_layout.addWidget(object_class_label)

            # Встановити макет контейнера та додати його до основного макету
            object_container.setLayout(container_layout)
            self.objectListLayout.addWidget(object_container)
            object_container.mousePressEvent = lambda event, obj=obj: self.showObjectInfo(obj)

    def showObjectInfo(self, obj):
        message = f"Назва об'єкту: {obj['class_name']}\nВпевненість: {round(obj['confidence'] * 100, 2)}%"
        QMessageBox.information(self, "Інформація про об'єкт", message)


    def clearObjectList(self):
        # Remove all widgets from the object list layout
        for i in reversed(range(self.objectListLayout.count())):
            widget = self.objectListLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def clock(self):
        self.DateTime = QDateTime.currentDateTime()
        self.time.display(self.DateTime.toString('hh:mm:ss'))
        if not self.paused:
            if self.shouldTrack:
                self.clearElements()
                if self.detector.getTracks() == None:
                    self.detector.track(self.frame)
                self.createLeftPanelObjects(self.detector.getTracks())
            self.clearObjectList()
            self.showObjectList()

    def captureVideoCadr(self, ret, frame):
        if ret:
            # Змінюємо розмір зображення на розмір QLabel
            frame = cv2.resize(frame, (self.label.width(), self.label.height()))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frame = frame
            if self.shouldTrack and not self.showSpeed:
                self.trackingAlgorithm(frame)
            _, frame = self.detector.detect(frame, self.showSpeed, self.shouldTrack)
            h, w, ch = frame.shape
            bytesPerLine = ch * w
            # Створюємо QImage з обробленого зображення
            image = QtGui.QImage(frame.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(image)
            self.label.setPixmap(pixmap)
        else:
            print("Помилка: Не вдалося отримати кадр")

    def displayWebcam(self):
        if self.video_path is not None:
            ret, frame = self.capture.read()
            self.captureVideoCadr(ret, frame)
        elif self.camera is not None and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:  # Додати умову перевірки наявності кадру
                self.captureVideoCadr(ret, frame)
            else:
                print("Помилка: Не вдалося отримати кадр з камери")
        else:
            print("Відео не обрано")

    def set_video_path(self, video_path):
        self.video_path = video_path
        self.capture.open(video_path)
        if not self.capture.isOpened():
            print("Помилка: Не вдалося відкрити відеофайл")
        else:
            print("Відеофайл успішно відкрито")
            

    def openCamera(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.displayWebcam)
        self.timer.start(30)  # Оновлення кадрів кожні 30 мс

        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            print("Помилка: Не вдалося відкрити камеру!")
        else:
            print("Камера успішно відкрита")


    def retranslateUi(self, videoView):
        _translate = QtCore.QCoreApplication.translate
        videoView.setWindowTitle(_translate("videoView", "Автоматизована система відстеження об'єктів"))
        self.trackingButton.setText(_translate("videoView", "Відстеження об\'єкту"))
        self.speedButton.setText(_translate("videoView", "Трекер швидкості"))
        self.groupBoxInterface.setTitle(_translate("videoView", "Налаштування інтерфейсу"))
        self.width1.setText(_translate("videoView", "Ширина:"))
        self.height1.setText(_translate("videoView", "Висота:"))
        self.colorLabel.setText(_translate("videoView", "Колір підписів:"))
        self.OKButton.setText(_translate("videoView", "Підтвердити"))
        self.comboBoxColors.setPlaceholderText(_translate("videoView", "Кольори"))
        self.infoLabel.setText(_translate("videoView", "❌ Відстеження вимкнено"))
        self.parametersGroup.setTitle(_translate("videoView", "Параметри відображення"))
        self.checkBoxFrame.setText(_translate("videoView", "Показувати рамки"))
        self.checkBoxColors.setText(_translate("videoView", "Чорно-біле відображення"))
        self.labelSort.setText(_translate("videoView", "Сортування за:"))
        self.labelModel.setText(_translate("videoView", "Модель:"))
        self.labelLine.setText(_translate("videoView", "Лінія вимірювання:"))
        self.labelTracking.setText(_translate("videoView", "Метод відстеження:"))
        self.backButton.setText(_translate("videoView", "Повернутися в меню"))
        self.showLogsButton.setText(_translate("videoView", "Відкрити логування"))
        self.instructionButton.setText(_translate("videoView", "Посібник користувача"))


class videoView(QtWidgets.QMainWindow, Ui_videoView):
    def __init__(self, parent=None):
        print("init")
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.paused = False

    def closeEvent(self, event):
        if self.video_path is not None:
            self.capture.release()
        elif self.camera is not None:
            self.camera.release()
        print("Close event called 1")
        super().closeEvent(event)
        event.accept()
