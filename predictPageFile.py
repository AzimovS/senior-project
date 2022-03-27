from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel, QFileDialog, QMessageBox
# from WelcomePageFile import WelcomePage


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
        from main import widget
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)