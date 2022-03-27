from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog


class HowItWorksPage(QDialog):
    def __init__(self):
        super(HowItWorksPage, self).__init__()
        loadUi("Pages/howItWorksPage.ui", self)
        self.FACButton.clicked.connect(self.goBack)

    def goBack(self):
        from main import widget
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)
