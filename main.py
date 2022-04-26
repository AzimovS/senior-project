import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel, QFileDialog, QMessageBox, QAction
from PyQt5.QtGui import QPixmap, QImage, QKeySequence
from PyQt5.QtGui import QPainter, QColor
from videoWidget import VideoWindow


from PageClass.AboutProjectPage import AboutProjectPage
from PageClass.HowItWorksPage import HowItWorksPage
from PageClass import GlobalVariables
from PageClass.trainingByFeaturePage import trainingByFeaturePage
from PageClass.uploadTrainingFilePage import uploadTrainingFilePage
from PageClass.ImageFolderPreparePage import ImageFolderPreparePage
from PageClass.trainingByPicturePage import trainingByPicturePage
from PageClass.visualizeFeaturePage import visualizeFeaturePage
from PageClass.uploadVisualizationFilePage import uploadVisualizationFilePage
from PageClass.seeVisualsPage import seeVisualsPage
from PageClass.predictPage import predictPage

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageQt import ImageQt
import os
import pandas as pd
import train_features
import create_imagenet
import resnet_train
import plot_graph

class WelcomePage(QDialog):
    def __init__(self):
        super(WelcomePage, self).__init__()
        loadUi("Pages/welcomePage.ui", self)
        # self.setGeometry(0, 0, 650, 900)
        self.aboutProjectButton.clicked.connect(self.gotoATPPage)  #go to About The Project page
        self.howItWorksButton.clicked.connect(self.gotoHIWPage)  #go to How It Works Page
        self.startTrainingButton.clicked.connect(self.gotoUTFPage)  #go to Upload Training File Page
        self.visualizationButton.clicked.connect(self.gotoUVFPage)  #go to Upload Visualization File Page
        self.predictionButton.clicked.connect(self.gotoPredictPage)  #go to prediction page

    #when about the project button is pressed
    def gotoATPPage(self):
        widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['AboutProjectPageFile'])

    #when how it works button pressed
    def gotoHIWPage(self):
        widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['HowItWorksPage'])

    def gotoUTFPage(self):
        widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['uploadTrainingFilePage'])

    def gotoPredictPage(self):
        widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['predictPage'])

    def gotoUVFPage(self):
        widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['uploadVisualizationFilePage'])





app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

welcome = WelcomePage()
about = AboutProjectPage(widget)
howItWorks = HowItWorksPage(widget)
uploadTrainingFile = uploadTrainingFilePage(widget)
trainingByFeature = trainingByFeaturePage(widget)
imageFolder = ImageFolderPreparePage(widget)
trainingByPicture = trainingByPicturePage(widget)
visualizeFeature = visualizeFeaturePage(widget)
uploadVisualizationFile = uploadVisualizationFilePage(widget)
seeVisuals = seeVisualsPage(widget)
predictP = predictPage(widget)

widget.addWidget(welcome)
widget.addWidget(about)
widget.addWidget(howItWorks)
widget.addWidget(uploadTrainingFile)
widget.addWidget(uploadVisualizationFile)
widget.addWidget(predictP)
widget.addWidget(seeVisuals)
widget.addWidget(trainingByFeature)
widget.addWidget(imageFolder)
widget.addWidget(trainingByPicture)
widget.addWidget(visualizeFeature)

widget.move(500, 250)
widget.setFixedHeight(650)
widget.setFixedWidth(900)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")