from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from videoWidget import VideoWindow
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageQt import ImageQt
import os
import pandas as pd
import train_features
import create_imagenet
from WelcomePageFile import WelcomePage


class seeVisualsPage(QDialog):
    def __init__(self, *args):
        super(seeVisualsPage, self).__init__()
        loadUi("Pages/seeVisualsPage.ui", self)
        self.data_path = args[-1]
        self.data = train_features.load_data(self.data_path)
        self.len_data = len(self.data)
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

    def label_action(self):
        file_path = self.data.iloc[self.cur_frame, :].iloc[-1].split('/')[-1]
        label = None
        if self.sender().text() == "Correct":
            label = [1, file_path]
        else:
            label = [0, file_path]
        self.labels[self.cur_frame] = label
        print(label)
        iterated = self.cur_frame + 1
        while self.data.iloc[self.cur_frame, 1] == self.data.iloc[iterated, 1]:
            iterated += 1
            if self.len_data <= iterated:
                iterated = 0
                break
            self.labels[iterated - 1] = label
        iterated = self.cur_frame - 1
        while self.data.iloc[self.cur_frame, 1] == self.data.iloc[iterated, 1]:
            iterated -= 1
            if 0 > iterated:
                iterated = self.len_data - 1
                break
            self.labels[iterated + 1] = label
        print(self.labels)
        self.next_action()

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
        x = self.data.iloc[self.cur_frame, :]
        file_path = x.iloc[-1]
        img = create_imagenet.create_image_return(x, file_path)
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
            ball_y = int(float(x[4]) * img_height)
            draw.rectangle((ball_x - 10, ball_y - 10, ball_x + 10, ball_y + 10), outline=(255, 255, 255), width=2)
        if self.checkBoxPlayers.isChecked():
            j = 0
            for i in range(8, 52, 2):
                player_x = int(float(x[i]) * img_width)
                player_y = int(float(x[i + 1]) * img_height)
                print(j, x[i], x[i + 1], player_x, player_y)
                j += 1
                draw.rectangle((player_x - 10, player_y - 20, player_x + 10, player_y + 20), outline=(255, 255, 255), width=2)
        elif self.checkBoxOnePlayer.isChecked():
            player_x = int(float(x[8 + self.player_num]) * img_width)
            player_y = int(float(x[8 + self.player_num + 1]) * img_height)
            print(player_x, player_y)
            if player_x != 0 or player_y != 0:
                draw.rectangle((player_x - 10, player_y - 20, player_x + 10, player_y + 20), outline=(255, 255, 255),
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
        from uploadVisualizationFilePageFile import uploadVisualizationFilePage
        from main import widget
        UVFPage = uploadVisualizationFilePage()
        widget.addWidget(UVFPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def goBack(self):
        from main import widget
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)