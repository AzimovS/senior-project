import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtGui import QPainter, QColor

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
import os
import pandas as pd
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
        new_data_path = create_imagenet.create_imagenet_dataset(self.data_path)
        gotoTBPPage = trainingByPicturePage(new_data_path)
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
        self.visualizeButton.hide()


        self.FACButton.clicked.connect(self.goBack)
        self.goBackButton.clicked.connect(self.gotoUTFPage)
        self.extraTreeButton.clicked.connect(self.extraTreeTrainPrepare)
        self.kNeighborsButton.clicked.connect(self.kNeighborsPrepare)
        self.decisionTreeButton.clicked.connect(self.decisionTreePrepare)
        self.predictButton.clicked.connect(self.train)
        self.visualizeButton.clicked.connect(self.visualize)

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

    def train(self):
        if self.clf == '':
            return
        data = train_features.load_data(self.data_path)
        acc, self.clf, self.test_data = train_features.train_features(data, clf=self.clf,
                                                        first=int(self.firstParameterEdit.text()),
                                                        second=int(self.secondParameterEdit.text()))
        self.accuracyText.setText("The accuracy for validation set is {}%".format(acc * 100))
        self.accuracyText.adjustSize()
        self.accuracyText.show()
        self.visualizeButton.show()

    def visualize(self):
        visualizePage = visualizeFeaturePage(self.clf, self.test_data)
        widget.addWidget(visualizePage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class visualizeFeaturePage(QDialog):
    def __init__(self, *args):
        super(visualizeFeaturePage, self).__init__()
        loadUi("Pages/visualizeFeaturePage.ui", self)
        self.clf = args[-2]
        self.test_data = args[-1]
        self.len_data = len(self.test_data[0])
        print(self.len_data)
        self.cur_frame = 0
        self.set_prediction()

        self.position_form = PositionForm()
        self.position_form.show()

        self.FACButton.clicked.connect(self.goBack)
        self.nextButton.clicked.connect(self.next_frame)
        self.previousButton.clicked.connect(self.previous_frame)

    def positions(self, dr, color, draw, ball_x, ball_y):
        if 1 <= dr <= 4:
            draw.line((ball_x + 15, ball_y + 15, ball_x + 55, ball_y + 55), fill=color, width=3)
        if 5 <= dr <= 8:
            draw.line((ball_x + 15, ball_y + 15, ball_x + 55, ball_y + 30), fill=color, width=3)
        if 9 <= dr <= 12:
            draw.line((ball_x + 15, ball_y + 15, ball_x + 55, ball_y - 15), fill=color, width=3)
        if 13 <= dr <= 16:
            draw.line((ball_x + 15, ball_y + 15, ball_x + 55, ball_y - 30), fill=color, width=3)
        if 17 <= dr <= 20:
            draw.line((ball_x + 15, ball_y + 15, ball_x + 15, ball_y - 30), fill=color, width=3)
        if 21 <= dr <= 24:
            draw.line((ball_x + 15, ball_y + 15, ball_x - 25, ball_y - 25), fill=color, width=3)
        if 25 <= dr <= 28:
            draw.line((ball_x + 15, ball_y + 15, ball_x - 25, ball_y - 15), fill=color, width=3)
        if 29 <= dr <= 32:
            draw.line((ball_x + 15, ball_y + 15, ball_x - 25, ball_y + 15), fill=color, width=3)
        if 33 <= dr <= 36:
            draw.line((ball_x + 15, ball_y + 15, ball_x - 25, ball_y + 30), fill=color, width=3)
        if 37 <= dr <= 40:
            draw.line((ball_x + 15, ball_y + 15, ball_x, ball_y + 55), fill=color, width=3)

    def draw_arrows(self, frame, ball_x, ball_y, true, pred):
        draw = ImageDraw.Draw(frame)
        start_x = int(ball_x)
        start_y = int(ball_y)
        self.positions(pred, (0, 0, 255), draw, start_x, start_y)
        self.positions(true, (255, 0, 0), draw, start_x, start_y)
        return frame

    def set_prediction(self):
        x, y = self.test_data
        x = x.iloc[self.cur_frame, :]
        file_path = x.iloc[-1]
        img = create_imagenet.create_image_return(x, file_path)
        frame_num = int(float(x.iloc[0]))
        ball_x = float(x[3]) * 640
        ball_y = float(x[4]) * 360
        x = x[1:-1]
        x = pd.DataFrame(x).T

        self.trueText.setText("True action: " + str(int(float(y[self.cur_frame]))))
        self.predictionText.setText("Predicted action: " + str(int(float(self.clf.predict(x)[0]))))
        img = self.draw_arrows(img, ball_x, ball_y, int(float(y[self.cur_frame])),
                               int(float(self.clf.predict(x)[0])))
        img = ImageQt(img)
        self.pixmap = QPixmap.fromImage(img)
        # self.pixmap = self.pixmap.scaled(600, 337, QtCore.Qt.KeepAspectRatio)
        self.image.setPixmap(self.pixmap)


    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def next_frame(self):
        self.cur_frame += 1
        if self.len_data == self.cur_frame:
            self.cur_frame = 0
        self.set_prediction()

    def previous_frame(self):
        self.cur_frame -= 1
        if self.cur_frame == -1:
            self.cur_frame = self.len_data - 1
        self.set_prediction()


class PositionForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Ball Position')
        self.pixmap = QPixmap('positions.png')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.pixmap = self.pixmap.scaled(400, 400)
        # self.image.resize(500, 500)
        self.image.setPixmap(self.pixmap)

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
