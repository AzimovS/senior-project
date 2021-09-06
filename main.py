import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap

class WelcomePage(QDialog):
    def __init__(self):
        super(WelcomePage, self).__init__()
        loadUi("Pages/welcomePage.ui", self)
        self.aboutProjectButton.clicked.connect(self.gotoATPPage)
        self.howItWorksButton.clicked.connect(self.gotoHIWPage)
        self.startAnalysisButton.clicked.connect(self.gotoSAPage)

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

    #whem start analysis button is pressed
    def gotoSAPage(self):
        SAPage = StartAnalysisPage()
        widget.addWidget(SAPage)
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
        self.startAnalysisButton.clicked.connect(self.gotoSAPage)

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoSAPage(self):
        SAPage = StartAnalysisPage()
        widget.addWidget(SAPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class StartAnalysisPage(QDialog):
    def __init__(self):
        super(StartAnalysisPage, self).__init__()
        loadUi("Pages/startAnalysisPage.ui", self)
        self.FACButton.clicked.connect(self.goBack)
        self.browseButton.clicked.connect(self.browsefiles)
        self.byPictureButton.clicked.connect(self.gotoByPicturePage)
        self.seeVisualsButton.clicked.connect(self.gotoSVPage)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','C:\Desktop')
        self.lineEdit.setText(fname[0])

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoByPicturePage(self):
        gotoBPPage = ByPicturePage()
        widget.addWidget(gotoBPPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoSVPage(self):
        gotoSVPage = SeeVisualsPage()
        widget.addWidget(gotoSVPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ByPicturePage(QDialog):
    def __init__(self):
        super(ByPicturePage, self).__init__()
        loadUi("Pages/byPicturePage.ui", self)
        self.FACButton.clicked.connect(self.goBack)
        self.goBackButton.clicked.connect(self.gotoSAPage)
        self.browseButton.clicked.connect(self.browsefiles)

    def gotoSAPage(self):
        SAPage = StartAnalysisPage()
        widget.addWidget(SAPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','C:\Desktop')
        self.lineEdit.setText(fname[0])

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class SeeVisualsPage(QDialog):
    def __init__(self):
        super(SeeVisualsPage, self).__init__()
        loadUi("Pages/seeVisualsPage.ui", self)
        self.FACButton.clicked.connect(self.goBack)
        self.goBackButton.clicked.connect(self.gotoSAPage)


    def gotoSAPage(self):
        SAPage = StartAnalysisPage()
        widget.addWidget(SAPage)
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
