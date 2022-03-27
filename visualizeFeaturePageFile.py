from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
import pandas as pd
import create_imagenet
# from WelcomePageFile import WelcomePage



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

        from main import PositionForm
        self.position_form = PositionForm()
        self.position_form.show()

        self.FACButton.clicked.connect(self.goBack)
        self.nextButton.clicked.connect(self.next_frame)
        self.previousButton.clicked.connect(self.previous_frame)

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
        img = self.draw_arrows(img, 580, 50, int(float(y[self.cur_frame])),
                               int(float(self.clf.predict(x)[0])))
        img = ImageQt(img)
        self.pixmap = QPixmap.fromImage(img)
        # self.pixmap = self.pixmap.scaled(600, 337, QtCore.Qt.KeepAspectRatio)
        self.image.setPixmap(self.pixmap)


    def goBack(self):
        from main import widget
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