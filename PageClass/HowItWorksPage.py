from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PageClass import GlobalVariables

class HowItWorksPage(QDialog):
    def __init__(self, widget):
        super(HowItWorksPage, self).__init__()
        loadUi("Pages/howItWorksPage.ui", self)
        self.widget = widget
        self.FACButton.clicked.connect(self.goBack)

    def goBack(self):
        self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['WelcomePage'])