import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtGui import QPainter, QColor
from videoWidget import VideoWindow
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageQt import ImageQt
import os
import pandas as pd
import train_features
import create_imagenet
import resnet_train
import plot_graph
from WelcomePageFile import WelcomePage
from AboutProjectPageFile import AboutProjectPage
from HowItWorksPageFile import HowItWorksPage
from uploadTrainingFilePageFile import uploadTrainingFilePage
from ImageFolderPreparePageFile import ImageFolderPreparePage
from trainingByPicturePageFile import trainingByPicturePage
from trainingByFeaturePageFile import trainingByFeaturePage
from visualizeFeaturePageFile import visualizeFeaturePage
from PositionFormFile import PositionForm
from predictPageFile import predictPage
from seeVisualsPageFile import seeVisualsPage


#main
app = QApplication(sys.argv)
welcome = WelcomePage()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.move(500, 250)
widget.setFixedHeight(650)
widget.setFixedWidth(900)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
