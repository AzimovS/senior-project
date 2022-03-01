from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap


class PositionForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(1450, 300, 400, 400)
        self.setWindowTitle('Ball Position')
        self.pixmap = QPixmap('positions.png')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.pixmap = self.pixmap.scaled(400, 400)
        # self.image.resize(500, 500)
        self.image.setPixmap(self.pixmap)