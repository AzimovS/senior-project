from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.uic import loadUi
import os

from PageClass import GlobalVariables
from PageClass.seeVisualsPage import seeVisualsPage


class uploadVisualizationFilePage(QDialog):
    def __init__(self, widget):
        super(uploadVisualizationFilePage, self).__init__()
        loadUi("Pages/uploadVisualizationFilePage.ui", self)
        self.widget = widget
        self.lineEdit.setText('/home/azimov/Desktop/senior-project/check_new_data')
        self.FACButton.clicked.connect(self.goBack)
        self.browseButton.clicked.connect(self.browsefiles)
        self.nextButton.clicked.connect(self.gotoSeeVisualsPage)

    def browsefiles(self):
        current_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory', current_dir)
        self.lineEdit.setText(fname)

    def goBack(self):
        self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['WelcomePage'])

    def gotoSeeVisualsPage(self):
        gotoSVPage = seeVisualsPage(self.widget, self.lineEdit.text())
        self.widget.insertWidget(GlobalVariables.PAGE_TO_INDEX['seeVisualsPage'], gotoSVPage)
        self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['seeVisualsPage'])