from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import GlobalVariables
from HowItWorksPageFile import HowItWorksPage


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