import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel, QFileDialog, QMessageBox
import os
# from WelcomePageFile import WelcomePage


class uploadTrainingFilePage(QDialog):
    def __init__(self):
        super(uploadTrainingFilePage, self).__init__()
        loadUi("Pages/uploadTrainingFilePage.ui", self)
        self.lineEdit.setText('/home/azimov/Desktop/senior-project/data')
        self.FACButton.clicked.connect(self.goBack)
        self.browseButton.clicked.connect(self.browsefiles)
        self.byPictureButton.clicked.connect(self.gotoTrainingByPicturePage)
        self.byFeatureButton.clicked.connect(self.gotoTrainingByFeaturePage)

    def browsefiles(self):
        current_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory', current_dir)
        self.lineEdit.setText(fname)

    def goBack(self):
        from main import widget
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoTrainingByPicturePage(self):
        need_to_create = False
        for file in os.listdir(self.lineEdit.text()):
            if file.endswith(".npy"):
                need_to_create = True
                break

        if not need_to_create:
            from main import trainingByPicturePage, widget
            gotoTBPPage = trainingByPicturePage(self.lineEdit.text())
            widget.addWidget(gotoTBPPage)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            from main import ImageFolderPreparePage, widget
            gotoIFPPage = ImageFolderPreparePage(self.lineEdit.text())
            widget.addWidget(gotoIFPPage)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoTrainingByFeaturePage(self):
        from main import trainingByFeaturePage, widget
        gotoTBFPage = trainingByFeaturePage(self.lineEdit.text())
        widget.addWidget(gotoTBFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)