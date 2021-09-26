import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
import os
import train_features
import create_imagenet
import resnet_train
import plot_graph

class WelcomePage(QDialog):
    def __init__(self):
        super(WelcomePage, self).__init__()
        loadUi("Pages/welcomePage.ui", self)
        self.aboutProjectButton.clicked.connect(self.gotoATPPage)  #go to About The Project page
        self.howItWorksButton.clicked.connect(self.gotoHIWPage)  #go to How It Works Page
        self.startTrainingButton.clicked.connect(self.gotoUTFPage)  #go to Upload Training File Page
        self.visualizationButton.clicked.connect(self.gotoUVFPage)  #go to Upload Visualization File Page
        self.predictionButton.clicked.connect(self.gotoPredictPage)  #go to prediction page

    #when about the project button is pressed
    def gotoATPPage(self):
        ATPPage = AboutProjectPage()
        widget.addWidget(ATPPage)
        widget.setCurrentIndex(widget.currentIndex()+1)

    #when how it works button pressed
    def gotoHIWPage(self):
        HIWPage = HowItWorksPage()
        widget.addWidget(HIWPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def gotoUTFPage(self):
        UTFPage = uploadTrainingFilePage()
        widget.addWidget(UTFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def gotoPredictPage(self):
        gotoPredictionPage = predictPage()
        widget.addWidget(gotoPredictionPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def gotoUVFPage(self):
        UVFPage = uploadVisualizationFilePage()
        widget.addWidget(UVFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AboutProjectPage(QDialog):
    def __init__(self):
        super(AboutProjectPage, self).__init__()
        loadUi("Pages/aboutTProjectPage.ui", self)
        self.howItWorksButton.clicked.connect(self.gotoHIWPage)
        self.FACButton.clicked.connect(self.goBack)

    def gotoHIWPage(self):
        HIWPage = HowItWorksPage()
        widget.addWidget(HIWPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class HowItWorksPage(QDialog):
    def __init__(self):
        super(HowItWorksPage, self).__init__()
        loadUi("Pages/howItWorksPage.ui", self)
        self.FACButton.clicked.connect(self.goBack)

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class uploadTrainingFilePage(QDialog):
    def __init__(self):
        super(uploadTrainingFilePage, self).__init__()
        loadUi("Pages/uploadTrainingFilePage.ui", self)
        self.FACButton.clicked.connect(self.goBack)
        self.browseButton.clicked.connect(self.browsefiles)
        self.byPictureButton.clicked.connect(self.gotoTrainingByPicturePage)
        self.byFeatureButton.clicked.connect(self.gotoTrainingByFeaturePage)

    def browsefiles(self):
        current_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory', current_dir)
        self.lineEdit.setText(fname)

    def goBack(self):
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
            gotoTBPPage = trainingByPicturePage(self.lineEdit.text())
            widget.addWidget(gotoTBPPage)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            gotoIFPPage = ImageFolderPreparePage(self.lineEdit.text())
            widget.addWidget(gotoIFPPage)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoTrainingByFeaturePage(self):
        gotoTBFPage = trainingByFeaturePage(self.lineEdit.text())
        widget.addWidget(gotoTBFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ImageFolderPreparePage(QDialog):
    def __init__(self, *args):
        super(ImageFolderPreparePage, self).__init__()
        self.data_path = args[-1]
        loadUi("Pages/dataPreparePage.ui", self)
        self.browseButton.clicked.connect(self.browsefiles)
        self.nextButton.clicked.connect(self.prepareData)
        self.FACButton.clicked.connect(self.goBack)

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def browsefiles(self):
        current_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory', current_dir)
        self.lineEdit.setText(fname)

    def prepareData(self):
        create_imagenet.create_imagenet_dataset(self.data_path)
        gotoTBPPage = trainingByPicturePage(self.data_path)
        widget.addWidget(gotoTBPPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class trainingByPicturePage(QDialog):
    def __init__(self, *args):
        super(trainingByPicturePage, self).__init__()
        loadUi("Pages/trainingByPicturePage.ui", self)

        self.data_path = args[-1]

        self.firstParameterText.hide()
        self.firstParameterEdit.hide()
        self.secondParameterText.hide()
        self.secondParameterEdit.hide()
        self.thirdParameterText.hide()
        self.thirdParameterEdit.hide()

        self.FACButton.clicked.connect(self.goBack)
        self.goBackButton.clicked.connect(self.gotoUTFPage)
        self.resnetButton.clicked.connect(self.resnetPrepare)
        self.trainButton.clicked.connect(self.trainResnet)
        #self.decisionTreeButton.clicked.connect(self.)
        #self.predictButton.clicked.connect(self.)

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoUTFPage(self):
        UTFPage = uploadTrainingFilePage()
        widget.addWidget(UTFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def addBorders(self, button):
        self.howItWorksText.hide()
        button.setStyleSheet("QPushButton {\n"
                                           "    border-radius: 15px;\n"
                                           "    background-color: qlineargradient(spread:pad, x1:0.384211, y1:0.023, x2:0.768,         y2:1, stop:0 rgba(29, 30, 73, 255), stop:1 rgba(39, 41, 100, 255));\n"
                                           "\n"
                                           "    font: 75 14pt \"Comic Sans MS\"; color: rgb(110, 164, 190);\n"
                                           "    border-color: white;\n"
                                           "    border: 3px solid;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           "    background-color: rgb(54, 57, 138);\n"
                                           "}\n"
                                           "QPushButton:pressed{\n"
                                           "    background-color: rgb(91, 96, 230);\n"
                                           "}")

    def removeBorders(self, button):
        button.setStyleSheet("QPushButton {\n"
                                            "    border-radius: 15px;\n"
                                            "    background-color: qlineargradient(spread:pad, x1:0.384211, y1:0.023, x2:0.768,         y2:1, stop:0 rgba(29, 30, 73, 255), stop:1 rgba(39, 41, 100, 255));\n"
                                            "\n"
                                            "    font: 75 13pt \"Comic Sans MS\"; color: rgb(110, 164, 190)\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "    background-color: rgb(54, 57, 138);\n"
                                            "}\n"
                                            "QPushButton:pressed{\n"
                                            "    background-color: rgb(91, 96, 230);\n"
                                            "}")

    def resnetPrepare(self):
        self.addBorders(self.resnetButton)
        self.removeBorders(self.somethingButton)

        self.firstParameterText.show()
        self.firstParameterEdit.show()
        self.secondParameterText.show()
        self.secondParameterEdit.show()
        self.thirdParameterText.show()
        self.thirdParameterEdit.show()

    def trainResnet(self):
        history, model = resnet_train.train(self.data_path, int(self.thirdParameterEdit.text()),
                                            float(self.firstParameterEdit.text()),
                                            float(self.secondParameterEdit.text()))

        print(history)
        train_loss = [x['train_loss'] for x in history]
        val_loss = [x['val_loss'] for x in history]
        val_acc = [x['val_acc'] for x in history]

        self.graph_loss = plot_graph.GraphWindow(self, train_loss=train_loss, val_loss=val_loss)
        self.graph_loss.show()

        self.graph_acc = plot_graph.GraphWindow(self, val_acc=val_acc)
        self.graph_acc.show()



class trainingByFeaturePage(QDialog):
    def __init__(self, *args):
        super(trainingByFeaturePage, self).__init__()
        self.data_path = args[-1]
        loadUi("Pages/trainingByFeaturePage.ui", self)

        self.firstParameterText.hide()
        self.firstParameterEdit.hide()
        self.secondParameterText.hide()
        self.secondParameterEdit.hide()
        self.accuracyText.hide()
        self.clf = ''


        self.FACButton.clicked.connect(self.goBack)
        self.goBackButton.clicked.connect(self.gotoUTFPage)
        self.extraTreeButton.clicked.connect(self.extraTreeTrainPrepare)
        self.kNeighborsButton.clicked.connect(self.kNeighborsPrepare)
        self.decisionTreeButton.clicked.connect(self.decisionTreePrepare)
        self.predictButton.clicked.connect(self.predict)

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoUTFPage(self):
        UTFPage = uploadTrainingFilePage()
        widget.addWidget(UTFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def addBorders(self, button):
        self.howItWorksText.hide()
        button.setStyleSheet("QPushButton {\n"
                                           "    border-radius: 15px;\n"
                                           "    background-color: qlineargradient(spread:pad, x1:0.384211, y1:0.023, x2:0.768,         y2:1, stop:0 rgba(29, 30, 73, 255), stop:1 rgba(39, 41, 100, 255));\n"
                                           "\n"
                                           "    font: 75 14pt \"Comic Sans MS\"; color: rgb(110, 164, 190);\n"
                                           "    border-color: white;\n"
                                           "    border: 3px solid;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           "    background-color: rgb(54, 57, 138);\n"
                                           "}\n"
                                           "QPushButton:pressed{\n"
                                           "    background-color: rgb(91, 96, 230);\n"
                                           "}")

    def removeBorders(self, button):
        button.setStyleSheet("QPushButton {\n"
                                            "    border-radius: 15px;\n"
                                            "    background-color: qlineargradient(spread:pad, x1:0.384211, y1:0.023, x2:0.768,         y2:1, stop:0 rgba(29, 30, 73, 255), stop:1 rgba(39, 41, 100, 255));\n"
                                            "\n"
                                            "    font: 75 13pt \"Comic Sans MS\"; color: rgb(110, 164, 190)\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "    background-color: rgb(54, 57, 138);\n"
                                            "}\n"
                                            "QPushButton:pressed{\n"
                                            "    background-color: rgb(91, 96, 230);\n"
                                            "}")

    def extraTreeTrainPrepare(self):
        self.clf = 'extra'
        self.addBorders(self.extraTreeButton)
        self.removeBorders(self.kNeighborsButton)
        self.removeBorders(self.decisionTreeButton)

        self.firstParameterText.setText("Random State: ")
        self.firstParameterText.show()

        self.firstParameterEdit.setText('0')
        self.firstParameterEdit.show()

        self.secondParameterText.setText("N Estimators: ")
        self.secondParameterText.show()

        self.secondParameterEdit.setText('100')
        self.secondParameterEdit.show()

    def kNeighborsPrepare(self):
        self.clf = 'kneigh'
        self.addBorders(self.kNeighborsButton)
        self.removeBorders(self.extraTreeButton)
        self.removeBorders(self.decisionTreeButton)

        self.firstParameterText.setText("N Neighbors: ")
        self.firstParameterText.show()

        self.firstParameterEdit.setText('3')
        self.firstParameterEdit.show()

        self.secondParameterText.hide()
        self.secondParameterEdit.hide()

    def decisionTreePrepare(self):
        self.clf = 'decision'
        self.addBorders(self.decisionTreeButton)
        self.removeBorders(self.extraTreeButton)
        self.removeBorders(self.kNeighborsButton)

        self.firstParameterText.setText("Random State: ")
        self.firstParameterText.show()

        self.firstParameterEdit.setText('42')
        self.firstParameterEdit.show()

        self.secondParameterText.hide()
        self.secondParameterEdit.hide()

    def predict(self):
        if self.clf == '':
            return
        data = train_features.load_data(self.data_path)
        acc = train_features.train_features_extratrees(data, clf=self.clf,
                                                        first=int(self.firstParameterEdit.text()),
                                                        second=int(self.secondParameterEdit.text()))
        self.accuracyText.setText("The accuracy is {}%".format(acc * 100))
        self.accuracyText.adjustSize()
        self.accuracyText.show()


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
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class uploadVisualizationFilePage(QDialog):
    def __init__(self):
        super(uploadVisualizationFilePage, self).__init__()
        loadUi("Pages/uploadVisualizationFilePage.ui", self)
        self.FACButton.clicked.connect(self.goBack)
        self.browseButton.clicked.connect(self.browsefiles)
        self.nextButton.clicked.connect(self.gotoSeeVisualsPage)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','C:\Desktop')
        self.lineEdit.setText(fname[0])

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoSeeVisualsPage(self):
        gotoSVPage = seeVisualsPage()
        widget.addWidget(gotoSVPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class seeVisualsPage(QDialog):
    def __init__(self):
        super(seeVisualsPage, self).__init__()
        loadUi("Pages/seeVisualsPage.ui", self)
        self.FACButton.clicked.connect(self.goBack)
        self.goBackButton.clicked.connect(self.gotoUVFPage)


    def gotoUVFPage(self):
        UVFPage = uploadVisualizationFilePage()
        widget.addWidget(UVFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#main
app = QApplication(sys.argv)
welcome = WelcomePage()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(650)
widget.setFixedWidth(900)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
