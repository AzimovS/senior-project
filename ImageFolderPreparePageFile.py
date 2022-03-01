from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QFileDialog
import os
import create_imagenet
from WelcomePageFile import WelcomePage
from AboutProjectPageFile import AboutProjectPage
from HowItWorksPageFile import HowItWorksPage
from uploadTrainingFilePageFile import uploadTrainingFilePage


class ImageFolderPreparePage(QDialog):
    def __init__(self, *args):
        super(ImageFolderPreparePage, self).__init__()
        self.data_path = args[-1]
        loadUi("Pages/dataPreparePage.ui", self)
        self.browseButton.clicked.connect(self.browsefiles)
        self.nextButton.clicked.connect(self.prepareData)
        self.FACButton.clicked.connect(self.goBack)

    def goBack(self):
        from main import widget
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def browsefiles(self):
        current_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory', current_dir)
        self.lineEdit.setText(fname)

    def prepareData(self):
        new_data_path = create_imagenet.create_imagenet_dataset(self.data_path)
        from main import trainingByPicturePage, widget
        gotoTBPPage = trainingByPicturePage(new_data_path)
        widget.addWidget(gotoTBPPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)