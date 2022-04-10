from PIL import ImageDraw, ImageFont
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap, QKeySequence
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QAction
from PyQt5.uic import loadUi
from qtpy import QtCore

import create_imagenet
import train_features
from PageClass import GlobalVariables
from videoWidget import VideoWindow
import pandas as pd
import numpy as np
import os

class seeVisualsPage(QDialog):
    def __init__(self, widget, *args):
        super(seeVisualsPage, self).__init__()
        loadUi("Pages/seeVisualsPage.ui", self)
        self.widget = widget
        if len(args) > 0:
            self.data_path = args[-1]
            # self.data = train_features.load_data(self.data_path)
            self.list_of_valid_files = train_features.get_list_valid_files(self.data_path)
            # print(self.list_of_valid_files)
            self.cur_file = 0
            self.cur_frame = 0
            self.player_num = 0
            self.labels = {}
            self.set_frame()

        self.framePrev.clicked.connect(self.previous_frame)
        self.frameNext.clicked.connect(self.next_frame)
        self.actionNext.clicked.connect(self.button_next_action)
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
        if os.path.isfile(self.data.iloc[self.cur_frame, -1][:-3] + 'mp4'):
            self.video.openFile(self.data.iloc[self.cur_frame, -1][:-3] + 'mp4')
        else:
            self.video.openFile(self.data.iloc[self.cur_frame, -1][:-3] + 'avi')
        self.video.move(600, 300)
        self.video.resize(640, 480)
        self.video.show()

    def show_stats(self):
        if len(self.labels) > 0:
            total_actions = 0
            correct_actions = 0
            prev = None
            for k, v in self.labels.items():
                if prev != k[2]:
                    prev = k[2]
                    total_actions += 1
                    if v == 1:
                        correct_actions += 1
            resText = f"The total number of frames is {len(self.labels)}\n" + \
                        f"The total number of actions is {total_actions}\n" + \
                        f"The number of correct actions {correct_actions}\n" + \
                        f"The accuracy is {correct_actions / total_actions}"
        else:
            resText = f"Results will be shown here"
        self.resultsText.setText(resText)

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
        self.labels[(file_path, idx, self.data.iloc[idx, 1])] = is_correct

        iterated = self.frames[self.cur_frame + 1]
        prev_to_label = []
        prev_to_label.append(iterated)
        while self.data.iloc[idx, 1] == self.data.iloc[iterated, 1]:
            iterated -= 1
            if 0 > iterated:
                iterated = self.len_data - 1
                break
            prev_to_label.append(iterated)

        for frame in sorted(prev_to_label):
            self.labels[(file_path, frame, self.data.iloc[frame, 1])] = is_correct
        self.next_action(label=is_correct)
        print(self.labels)

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

    def load_file(self):
        data = np.load(self.list_of_valid_files[self.cur_file])
        dir_path_np = np.repeat(self.list_of_valid_files[self.cur_file], len(data)).reshape(-1, 1)
        data = np.concatenate((data, dir_path_np), axis=1)
        self.data = pd.DataFrame(data)
        self.frames = self.data.index
        self.len_data = len(self.data)

    def set_frame(self):
        self.load_file()

        idx = self.frames[self.cur_frame]
        x = self.data.iloc[idx, :]
        file_path = x.iloc[-1]
        img, original_wigth, original_height = create_imagenet.create_image_return(x, file_path)
        draw = ImageDraw.Draw(img)
        img_width, img_height = img.size
        img = self.draw_arrows(img, 580, 50, int(float(x.iloc[1])))

        print((file_path.split('/')[-1], idx, str(self.data.iloc[idx, 1])))
        if (file_path.split('/')[-1], idx, str(self.data.iloc[idx, 1])) in self.labels:
            if self.labels[(file_path.split('/')[-1], idx, self.data.iloc[idx, 1])] == 1:
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
        img.save('show_img.jpg')
        self.pixmap = QPixmap('show_img.jpg')
        # self.pixmap = self.pixmap.scaled(600, 337, QtCore.Qt.KeepAspectRatio)
        self.image.setPixmap(self.pixmap)
        text = "The filename: {}\nFrame number: {}\nCurrent Action: {}\n" \
               "Attacking Team: {}\nNumber of Detected Players #1: {}\n" \
               "Number of Detected Players #2: {}\n" \
               "".format(x.iloc[-1].split('/')[-1], x.iloc[0], x.iloc[1], x.iloc[2], x.iloc[7], x.iloc[30])
        self.mainText.setText(text)
        self.show_stats()

    def button_next_action(self):
        self.next_action()

    def next_action(self, label=-1):
        idx = self.frames[self.cur_frame]
        x = self.data.iloc[idx, :]
        file_path = x.iloc[-1].split('/')[-1]
        prev = idx
        while self.data.iloc[idx, 1] == self.data.iloc[prev, 1]:
            if label != -1:
                self.labels[(file_path, idx, self.data.iloc[idx, 1])] = label
            idx += 1
            if len(self.data) <= idx:
                idx = 0
                self.cur_file += 1
                if len(self.list_of_valid_files) == self.cur_file:
                    self.cur_file -= 1
                    idx = prev
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("This is the last file")
                    msg.setWindowTitle("Info")
                    retval = msg.exec_()
                break
        self.cur_frame = idx
        self.set_frame()

    def previous_acion(self, label=None):
        idx = self.frames[self.cur_frame]
        prev = idx
        while self.data.iloc[idx, 1] == self.data.iloc[prev, 1]:
            idx -= 1
            if 0 > idx:
                idx = 0
                self.cur_file -= 1
                if 0 > self.cur_file:
                    self.cur_file = 0
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("This is the first file")
                    msg.setWindowTitle("Info")
                    retval = msg.exec_()
                break
        self.cur_frame = idx
        self.set_frame()

    def next_frame(self):
        self.cur_frame += 1
        if self.len_data == self.cur_frame:
            self.cur_frame = 0
            self.cur_file += 1
            if len(self.list_of_valid_files) == self.cur_file:
                self.cur_file = 0
        self.set_frame()

    def previous_frame(self):
        self.cur_frame -= 1
        if self.cur_frame == -1:
            self.cur_frame = 0
            if len(self.list_of_valid_files) <= self.cur_file:
                self.cur_file = len(self.list_of_valid_files) - 1
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
        self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['uploadVisualizationFilePage'])

    def goBack(self):
        self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['WelcomePage'])

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