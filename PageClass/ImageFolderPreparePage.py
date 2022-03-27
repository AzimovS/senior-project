import os

from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.uic import loadUi

from PageClass import GlobalVariables
import create_imagenet
from PageClass.trainingByPicturePage import trainingByPicturePage


class ImageFolderPreparePage(QDialog):
    def __init__(self, widget, *args):
        super(ImageFolderPreparePage, self).__init__()
        if len(args) > 0:
            self.data_path = args[-1]
        self.widget = widget
        loadUi("Pages/dataPreparePage.ui", self)
        self.browseButton.clicked.connect(self.browsefiles)
        self.nextButton.clicked.connect(self.prepareData)
        self.FACButton.clicked.connect(self.goBack)

    def goBack(self):
        self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['WelcomePage'])

    def browsefiles(self):
        current_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory', current_dir)
        self.lineEdit.setText(fname)

    def prepareData(self):
        new_data_path = create_imagenet.create_imagenet_dataset(self.data_path)
        gotoTBPPage = trainingByPicturePage(self.widget, new_data_path)

        self.widget.insertWidget(GlobalVariables.PAGE_TO_INDEX['trainingByPicturePage'], gotoTBPPage)
        self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['trainingByPicturePage'])