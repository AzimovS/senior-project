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
from PageClass.uploadVisualizationFilePage import uploadVisualizationFilePage
from PageClass.seeVisualsPage import seeVisualsPage

class WelcomePage(QDialog):
    def __init__(self):
        super(WelcomePage, self).__init__()
        loadUi("Pages/welcomePage.ui", self)
        # self.setGeometry(0, 0, 650, 900)
        self.aboutProjectButton.clicked.connect(self.gotoATPPage)  #go to About The Project page
        self.howItWorksButton.clicked.connect(self.gotoHIWPage)  #go to How It Works Page
        self.visualizationButton.clicked.connect(self.gotoUVFPage)  #go to Upload Visualization File Page

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
uploadVisualizationFile = uploadVisualizationFilePage(widget)
seeVisuals = seeVisualsPage(widget)

widget.addWidget(welcome)
widget.addWidget(about)
widget.addWidget(howItWorks)
widget.addWidget(uploadVisualizationFile)
widget.addWidget(seeVisuals)

widget.move(500, 250)
widget.setFixedHeight(650)
widget.setFixedWidth(900)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")