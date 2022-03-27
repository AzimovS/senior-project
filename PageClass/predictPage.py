from PyQt5.QtGui import QPixmap, QKeySequence
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QAction
from PyQt5.uic import loadUi

from PageClass import GlobalVariables


class predictPage(QDialog):
    def __init__(self, widget):
        super(predictPage, self).__init__()
        self.widget = widget
        loadUi("Pages/predictPage.ui", self)
        self.FACButton.clicked.connect(self.goBack)
        self.browseButton.clicked.connect(self.browsefiles)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','C:\Desktop')
        self.lineEdit.setText(fname[0])

    def goBack(self):
        self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['WelcomePage'])
