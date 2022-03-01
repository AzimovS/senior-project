from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel, QFileDialog, QMessageBox

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
        from main import AboutProjectPage, widget
        ATPPage = AboutProjectPage()
        widget.addWidget(ATPPage)
        widget.setCurrentIndex(widget.currentIndex()+1)

    #when how it works button pressed
    def gotoHIWPage(self):
        from main import HowItWorksPage, widget
        HIWPage = HowItWorksPage()
        widget.addWidget(HIWPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def gotoUTFPage(self):
        from main import uploadTrainingFilePage, widget
        UTFPage = uploadTrainingFilePage()
        widget.addWidget(UTFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def gotoPredictPage(self):
        from main import predictPage, widget
        gotoPredictionPage = predictPage()
        widget.addWidget(gotoPredictionPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def gotoUVFPage(self):
        from uploadVisualizationFilePageFile import uploadVisualizationFilePage
        from main import widget
        UVFPage = uploadVisualizationFilePage()
        widget.addWidget(UVFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)