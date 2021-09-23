import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
import os

class WelcomePage(QDialog):
    def __init__(self):
        super(WelcomePage, self).__init__()
        loadUi("Pages/welcomePage.ui", self)
        self.aboutProjectButton.clicked.connect(self.gotoATPPage)  #go to About The Project page
        self.howItWorksButton.clicked.connect(self.gotoHIWPage)  #go to How It Works Page
        self.startTrainingButton.clicked.connect(self.gotoUTFPage)  #go to Upload Training File Page
        self.visualizationButton.clicked.connect(self.gotoUVFPage)  #go to Upload Visualization File Page
        self.predictionButton.clicked.connect(self.gotoPredictPage)  #go to prediction page

    #when about the project button is pressed
    def gotoATPPage(self):
        ATPPage = AboutProjectPage()
        widget.addWidget(ATPPage)
        widget.setCurrentIndex(widget.currentIndex()+1)

    #when how it works button pressed
    def gotoHIWPage(self):
        HIWPage = HowItWorksPage()
        widget.addWidget(HIWPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def gotoUTFPage(self):
        UTFPage = uploadTrainingFilePage()
        widget.addWidget(UTFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def gotoPredictPage(self):
        gotoPredictionPage = predictPage()
        widget.addWidget(gotoPredictionPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def gotoUVFPage(self):
        UVFPage = uploadVisualizationFilePage()
        widget.addWidget(UVFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AboutProjectPage(QDialog):
    def __init__(self):
        super(AboutProjectPage, self).__init__()
        loadUi("Pages/aboutTProjectPage.ui", self)
        self.howItWorksButton.clicked.connect(self.gotoHIWPage)
        self.FACButton.clicked.connect(self.goBack)

    def gotoHIWPage(self):
        HIWPage = HowItWorksPage()
        widget.addWidget(HIWPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class HowItWorksPage(QDialog):
    def __init__(self):
        super(HowItWorksPage, self).__init__()
        loadUi("Pages/howItWorksPage.ui", self)
        self.FACButton.clicked.connect(self.goBack)


    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class uploadTrainingFilePage(QDialog):
    def __init__(self):
        super(uploadTrainingFilePage, self).__init__()
        loadUi("Pages/uploadTrainingFilePage.ui", self)
        self.FACButton.clicked.connect(self.goBack)
        self.browseButton.clicked.connect(self.browsefiles)
        self.byPictureButton.clicked.connect(self.gotoTrainingByPicturePage)
        self.byFeatureButton.clicked.connect(self.gotoTrainingByFeaturePage)

    def browsefiles(self):
        current_dir = os.getcwd()
        fname = QFileDialog.getOpenFileName(self, 'Open file', current_dir)
        self.lineEdit.setText(fname[0])

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoTrainingByPicturePage(self):
        gotoTBPPage = trainingByPicturePage()
        widget.addWidget(gotoTBPPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoTrainingByFeaturePage(self):
        gotoTBFPage = trainingByFeaturePage()
        widget.addWidget(gotoTBFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class trainingByPicturePage(QDialog):
    def __init__(self):
        super(trainingByPicturePage, self).__init__()
        loadUi("Pages/trainingByPicturePage.ui", self)
        self.FACButton.clicked.connect(self.goBack)
        self.goBackButton.clicked.connect(self.gotoUTFPage)
        #self.extraTreeButton.clicked.connect(self.)
        #self.kNeighborsButton.clicked.connect(self.)
        #self.decisionTreeButton.clicked.connect(self.)
        #self.predictButton.clicked.connect(self.)

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoUTFPage(self):
        UTFPage = uploadTrainingFilePage()
        widget.addWidget(UTFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class trainingByFeaturePage(QDialog):
    def __init__(self):
        super(trainingByFeaturePage, self).__init__()
        loadUi("Pages/trainingByFeaturePage.ui", self)
        self.FACButton.clicked.connect(self.goBack)
        self.goBackButton.clicked.connect(self.gotoUTFPage)
        #self.extraTreeButton.clicked.connect(self.)
        #self.kNeighborsButton.clicked.connect(self.)
        #self.decisionTreeButton.clicked.connect(self.)
        #self.predictButton.clicked.connect(self.)

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoUTFPage(self):
        UTFPage = uploadTrainingFilePage()
        widget.addWidget(UTFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class predictPage(QDialog):
    def __init__(self):
        super(predictPage, self).__init__()
        loadUi("Pages/predictPage.ui", self)
        self.FACButton.clicked.connect(self.goBack)
        self.browseButton.clicked.connect(self.browsefiles)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','C:\Desktop')
        self.lineEdit.setText(fname[0])

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class uploadVisualizationFilePage(QDialog):
    def __init__(self):
        super(uploadVisualizationFilePage, self).__init__()
        loadUi("Pages/uploadVisualizationFilePage.ui", self)
        self.FACButton.clicked.connect(self.goBack)
        self.browseButton.clicked.connect(self.browsefiles)
        self.nextButton.clicked.connect(self.gotoSeeVisualsPage)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','C:\Desktop')
        self.lineEdit.setText(fname[0])

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoSeeVisualsPage(self):
        gotoSVPage = seeVisualsPage()
        widget.addWidget(gotoSVPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class seeVisualsPage(QDialog):
    def __init__(self):
        super(seeVisualsPage, self).__init__()
        loadUi("Pages/seeVisualsPage.ui", self)
        self.FACButton.clicked.connect(self.goBack)
        self.goBackButton.clicked.connect(self.gotoUVFPage)


    def gotoUVFPage(self):
        UVFPage = uploadVisualizationFilePage()
        widget.addWidget(UVFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#main
app = QApplication(sys.argv)
welcome = WelcomePage()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(650)
widget.setFixedWidth(900)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
