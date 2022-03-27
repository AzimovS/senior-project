from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PageClass import GlobalVariables


class AboutProjectPage(QDialog):
    def __init__(self, widget):
        super(AboutProjectPage, self).__init__()
        loadUi("Pages/aboutTProjectPage.ui", self)
        self.widget = widget
        self.howItWorksButton.clicked.connect(self.gotoHIWPage)
        self.FACButton.clicked.connect(self.goBack)

    def gotoHIWPage(self):
        self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['HowItWorksPage'])

    def goBack(self):
        self.widget.setCurrentIndex(0)