from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel, QFileDialog, QMessageBox
import os
from WelcomePageFile import WelcomePage



class uploadVisualizationFilePage(QDialog):
    def __init__(self):
        super(uploadVisualizationFilePage, self).__init__()
        loadUi("Pages/uploadVisualizationFilePage.ui", self)
        self.lineEdit.setText('/home/azimov/Desktop/senior-project/data')
        self.FACButton.clicked.connect(self.goBack)
        self.browseButton.clicked.connect(self.browsefiles)
        self.nextButton.clicked.connect(self.gotoSeeVisualsPage)

    def browsefiles(self):
        current_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory', current_dir)
        self.lineEdit.setText(fname)

    def goBack(self):
        from main import widget
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoSeeVisualsPage(self):
        from main import seeVisualsPage, widget
        gotoSVPage = seeVisualsPage(self.lineEdit.text())
        widget.addWidget(gotoSVPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)