import os

from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.uic import loadUi
from PageClass import GlobalVariables
from PageClass.ImageFolderPreparePage import ImageFolderPreparePage
from PageClass.trainingByFeaturePage import trainingByFeaturePage
from PageClass.trainingByPicturePage import trainingByPicturePage


class uploadTrainingFilePage(QDialog):
    def __init__(self, widget):
        super(uploadTrainingFilePage, self).__init__()
        loadUi("Pages/uploadTrainingFilePage.ui", self)
        self.widget = widget
        self.FACButton.clicked.connect(self.goBack)
        self.browseButton.clicked.connect(self.browsefiles)
        self.byPictureButton.clicked.connect(self.gotoTrainingByPicturePage)
        self.byFeatureButton.clicked.connect(self.gotoTrainingByFeaturePage)

    def browsefiles(self):
        current_dir = os.path.normpath(os.getcwd())
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory', current_dir)
        self.lineEdit.setText(fname)

    def goBack(self):
        self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['WelcomePage'])

    def gotoTrainingByPicturePage(self):
        need_to_create = False
        for file in os.listdir(self.lineEdit.text()):
            if file.endswith(".npy"):
                need_to_create = True
                break

        if not need_to_create:
            gotoTBPPage = trainingByPicturePage(self.widget, self.lineEdit.text())
            self.widget.insertWidget(GlobalVariables.PAGE_TO_INDEX['trainingByPicturePage'], gotoTBPPage)
            self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['trainingByPicturePage'])
        else:
            gotoIFPPage = ImageFolderPreparePage(self.widget, self.lineEdit.text())
            self.widget.insertWidget(GlobalVariables.PAGE_TO_INDEX['ImageFolderPreparePage'], gotoIFPPage)
            self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['ImageFolderPreparePage'])

    def gotoTrainingByFeaturePage(self):
        gotoTBFPage = trainingByFeaturePage(self.widget, self.lineEdit.text())
        self.widget.insertWidget(GlobalVariables.PAGE_TO_INDEX['trainingByFeaturePage'], gotoTBFPage)
        self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['trainingByFeaturePage'])