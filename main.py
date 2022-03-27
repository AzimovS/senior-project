import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel, QFileDialog, QMessageBox, QAction
from PyQt5.QtGui import QPixmap, QImage, QKeySequence
from PyQt5.QtGui import QPainter, QColor
from videoWidget import VideoWindow


from PageClass.AboutProjectPage import AboutProjectPage
from PageClass.HowItWorksPage import HowItWorksPage
from PageClass import GlobalVariables
from PageClass.trainingByFeaturePage import trainingByFeaturePage
from PageClass.uploadTrainingFilePage import uploadTrainingFilePage
from PageClass.ImageFolderPreparePage import ImageFolderPreparePage
from PageClass.trainingByPicturePage import trainingByPicturePage
from PageClass.visualizeFeaturePage import visualizeFeaturePage

from PIL import Image, ImageDraw, ImageFont
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
        # self.setGeometry(0, 0, 650, 900)
        self.aboutProjectButton.clicked.connect(self.gotoATPPage)  #go to About The Project page
        self.howItWorksButton.clicked.connect(self.gotoHIWPage)  #go to How It Works Page
        self.startTrainingButton.clicked.connect(self.gotoUTFPage)  #go to Upload Training File Page
        self.visualizationButton.clicked.connect(self.gotoUVFPage)  #go to Upload Visualization File Page
        self.predictionButton.clicked.connect(self.gotoPredictPage)  #go to prediction page

    #when about the project button is pressed
    def gotoATPPage(self):
        widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['AboutProjectPageFile'])

    #when how it works button pressed
    def gotoHIWPage(self):
        widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['AboutProjectPageFile'])

    def gotoUTFPage(self):
        widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['uploadTrainingFilePage'])

    def gotoPredictPage(self):
        gotoPredictionPage = predictPage()
        widget.addWidget(gotoPredictionPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoUVFPage(self):
        UVFPage = uploadVisualizationFilePage()
        widget.addWidget(UVFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


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
        self.lineEdit.setText('/home/azimov/Desktop/senior-project/check_new_data')
        self.FACButton.clicked.connect(self.goBack)
        self.browseButton.clicked.connect(self.browsefiles)
        self.nextButton.clicked.connect(self.gotoSeeVisualsPage)

    def browsefiles(self):
        current_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory', current_dir)
        self.lineEdit.setText(fname)

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoSeeVisualsPage(self):
        gotoSVPage = seeVisualsPage(self.lineEdit.text())
        widget.addWidget(gotoSVPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class seeVisualsPage(QDialog):
    def __init__(self, *args):
        super(seeVisualsPage, self).__init__()
        loadUi("Pages/seeVisualsPage.ui", self)
        self.data_path = args[-1]
        self.data = train_features.load_data(self.data_path)
        self.len_data = len(self.data)
        self.frames = self.data.index

        self.cur_frame = 0
        self.player_num = 0
        self.labels = {}

        self.set_frame()
        self.framePrev.clicked.connect(self.previous_frame)
        self.frameNext.clicked.connect(self.next_frame)
        self.actionNext.clicked.connect(self.next_action)
        self.actionPrev.clicked.connect(self.previous_acion)
        self.FACButton.clicked.connect(self.goBack)
        self.goBackButton.clicked.connect(self.gotoUVFPage)
        self.playVideoButton.clicked.connect(self.show_video)
        self.checkBoxBall.clicked.connect(self.set_frame)
        self.checkBoxPlayers.clicked.connect(self.set_frame)
        self.checkBoxOnePlayer.clicked.connect(self.set_frame)
        self.playerPrevious.clicked.connect(self.previous_player)
        self.playerNext.clicked.connect(self.next_player)
        self.correctButton.clicked.connect(self.label_action)
        self.incorrectButton.clicked.connect(self.label_action)
        self.generateButton.clicked.connect(self.generate_file)

        self.nextAction = QAction("Next Action", self)
        self.nextAction.setShortcut(QKeySequence(QtCore.Qt.Key_Up))
        self.nextAction.setStatusTip('Up')
        self.nextAction.triggered.connect(self.next_action)

    def show_video(self):
        self.video = VideoWindow(self)
        self.video.openFile(self.data.iloc[self.cur_frame, -1][:-3] + 'mp4')
        self.video.move(600, 300)
        self.video.resize(640, 480)
        self.video.show()

    def generate_file(self):
        if len(self.labels) > 0:
            df = pd.DataFrame.from_dict(self.labels, orient='index')
            df.to_csv('labels.csv')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("The file was saved in the following path: " + os.getcwd() + '/labels.csv')
            msg.setWindowTitle("Info")
            retval = msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("There is no labels. Please click on correct/incorrect.")
            msg.setWindowTitle("Info")
            retval = msg.exec_()

    def set_label(self, is_correct):
        idx = self.frames[self.cur_frame]
        x = self.data.iloc[idx, :]
        file_path = x.iloc[-1].split('/')[-1]
        self.labels[self.frames[self.cur_frame]] = is_correct
        iterated = self.cur_frame + 1
        while self.data.iloc[self.frames[self.cur_frame], 1] == self.data.iloc[self.frames[iterated], 1]:
            iterated += 1
            if self.len_data <= iterated:
                iterated = 0
                break
            self.labels[iterated - 1] = is_correct
        iterated = self.cur_frame - 1
        while self.data.iloc[self.frames[self.cur_frame], 1] == self.data.iloc[self.frames[iterated], 1]:
            iterated -= 1
            if 0 > iterated:
                iterated = self.len_data - 1
                break
            self.labels[iterated + 1] = is_correct
        print(self.labels)
        self.next_action()

    def label_action(self):
        if self.sender().text() == "Correct":
            self.set_label(1)
        else:
            self.set_label(0)

    def positions(self, dr, color, draw, ball_x, ball_y):
        if 1 <= dr <= 4:
            draw.line((ball_x + 15, ball_y + 15, ball_x + 55, ball_y + 40), fill=color, width=3)
        if 5 <= dr <= 8:
            draw.line((ball_x + 15, ball_y + 15, ball_x + 55, ball_y + 25), fill=color, width=3)
        if 9 <= dr <= 12:
            draw.line((ball_x + 15, ball_y + 15, ball_x + 55, ball_y + 8), fill=color, width=3)
        if 13 <= dr <= 16:
            draw.line((ball_x + 15, ball_y + 15, ball_x + 55, ball_y - 15), fill=color, width=3)
        if 17 <= dr <= 20:
            draw.line((ball_x + 15, ball_y + 15, ball_x + 15, ball_y - 25), fill=color, width=3)
        if 21 <= dr <= 24:
            draw.line((ball_x + 15, ball_y + 15, ball_x - 25, ball_y - 15), fill=color, width=3)
        if 25 <= dr <= 28:
            draw.line((ball_x + 15, ball_y + 15, ball_x - 25, ball_y + 8), fill=color, width=3)
        if 29 <= dr <= 32:
            draw.line((ball_x + 15, ball_y + 15, ball_x - 25, ball_y + 25), fill=color, width=3)
        if 33 <= dr <= 36:
            draw.line((ball_x + 15, ball_y + 15, ball_x - 25, ball_y + 40), fill=color, width=3)
        if 37 <= dr <= 40:
            draw.line((ball_x + 15, ball_y + 15, ball_x + 15, ball_y + 55), fill=color, width=3)

    def draw_arrows(self, frame, ball_x, ball_y, true, pred=None):
        draw = ImageDraw.Draw(frame)
        start_x = int(ball_x)
        start_y = int(ball_y)
        self.positions(true, (255, 0, 0), draw, start_x, start_y)
        if pred:
            self.positions(pred, (0, 0, 255), draw, start_x, start_y)
        return frame

    def set_frame(self):
        idx = self.frames[self.cur_frame]
        x = self.data.iloc[idx, :]
        file_path = x.iloc[-1]
        img, original_wigth, original_height = create_imagenet.create_image_return(x, file_path)
        draw = ImageDraw.Draw(img)
        img_width, img_height = img.size
        img = self.draw_arrows(img, 580, 50, int(float(x.iloc[1])))

        if self.cur_frame in self.labels:
            if self.labels[self.cur_frame] == 1:
                text = "correct"
                color = (0, 255, 0)
            else:
                text = "incorrect"
                color = (255, 0, 0)
            font = ImageFont.truetype('DejaVuSans.ttf', 30)
            draw.text((0, 0), text, fill=color, font=font)

        if self.checkBoxBall.isChecked():
            ball_x = int(float(x[3]) * img_width)
            ball_y = int(float(x[4])  * img_height)
            draw.rectangle((ball_x - 5, ball_y - 5, ball_x + 5, ball_y + 5), outline=(255, 255, 255), width=2)
        if self.checkBoxPlayers.isChecked():
            j = 0
            for i in range(8, 52, 2):
                player_x = int(float(x[i]) / original_wigth * img_width)
                player_y = int(float(x[i + 1]) / original_height * img_height)
                if (player_x == 0 and player_y == 0):
                    continue
                j += 1
                draw.text((player_x, player_y - 10), f"{j}th {x[i]} {x[i + 1]} {player_x} {player_y}", fill=(255, 0, 0), font=ImageFont.truetype('DejaVuSans.ttf', 15))
                draw.rectangle((player_x - 20, player_y - 40, player_x, player_y), outline=(255, 255, 255), width=2)
        elif self.checkBoxOnePlayer.isChecked():
            player_x = int(float(x[8 + self.player_num]) / original_wigth * img_width)
            player_y = int(float(x[8 + self.player_num + 1]) / original_height * img_height)
            if player_x != 0 or player_y != 0:
                draw.rectangle((player_x - 20, player_y - 40, player_x, player_y), outline=(255, 255, 255),
                           width=2)
        img = ImageQt(img)
        self.pixmap = QPixmap.fromImage(img)
        # self.pixmap = self.pixmap.scaled(600, 337, QtCore.Qt.KeepAspectRatio)
        self.image.setPixmap(self.pixmap)
        text = "The filename: {}\nFrame number: {}\nCurrent Action: {}\n" \
               "Attacking Team: {}\nNumber of Detected Players #1: {}\n" \
               "Number of Detected Players #2: {}\n" \
               "".format(x.iloc[-1].split('/')[-1], x.iloc[0], x.iloc[1], x.iloc[2], x.iloc[5], x.iloc[6])
        self.mainText.setText(text)

    def next_action(self):
        prev = self.cur_frame
        while self.data.iloc[self.cur_frame, 1] == self.data.iloc[prev, 1]:
            self.cur_frame += 1
            if self.len_data <= self.cur_frame:
                self.cur_frame = 0
                break
        self.set_frame()

    def previous_acion(self):
        prev = self.cur_frame
        while self.data.iloc[self.cur_frame, 1] == self.data.iloc[prev, 1]:
            self.cur_frame -= 1
            if 0 > self.cur_frame:
                self.cur_frame = self.len_data - 1
        self.set_frame()

    def next_frame(self):
        self.cur_frame += 1
        if self.len_data == self.cur_frame:
            self.cur_frame = 0
        self.set_frame()

    def previous_frame(self):
        self.cur_frame -= 1
        if self.cur_frame == -1:
            self.cur_frame = self.len_data - 1
        self.set_frame()

    def next_player(self):
        self.player_num += 1
        if self.player_num == 22:
            self.player_num = 0
        self.set_frame()

    def previous_player(self):
        self.player_num -= 1
        if self.player_num == -1:
            self.player_num = 21
        self.set_frame()

    def gotoUVFPage(self):
        UVFPage = uploadVisualizationFilePage()
        widget.addWidget(UVFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goBack(self):
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_I:
            self.next_action()
        if event.key() == QtCore.Qt.Key_K:
            self.previous_acion()
        if event.key() == QtCore.Qt.Key_L:
            self.next_frame()
        if event.key() == QtCore.Qt.Key_J:
            self.previous_frame()
        if event.key() == QtCore.Qt.Key_X:
            self.set_label(0)
        if event.key() == QtCore.Qt.Key_C:
            self.set_label(1)
        if event.key() == QtCore.Qt.Key_V:
            self.show_video()


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

welcome = WelcomePage()
about = AboutProjectPage(widget)
howItWorks = HowItWorksPage(widget)
uploadTrainingFile = uploadTrainingFilePage(widget)
trainingByFeature = trainingByFeaturePage(widget)
imageFolder = ImageFolderPreparePage(widget)
trainingByPicture = trainingByPicturePage(widget)
visualizeFeature = visualizeFeaturePage(widget)

widget.addWidget(welcome)
widget.addWidget(about)
widget.addWidget(howItWorks)
widget.addWidget(uploadTrainingFile)
widget.addWidget(trainingByFeature)
widget.addWidget(imageFolder)
widget.addWidget(trainingByPicture)
widget.addWidget(visualizeFeature)

widget.move(500, 250)
widget.setFixedHeight(650)
widget.setFixedWidth(900)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")