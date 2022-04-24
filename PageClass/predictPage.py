from PyQt5.QtGui import QPixmap, QKeySequence
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QAction
from PyQt5.uic import loadUi
from PageClass import GlobalVariables
import os
from torch import load, device
from torchvision import transforms
from PIL import Image

device = device('cpu')

class predictPage(QDialog):
    def __init__(self, widget):
        super(predictPage, self).__init__()
        self.widget = widget
        loadUi("Pages/predictPage.ui", self)
        self.FACButton.clicked.connect(self.goBack)
        self.browseButton.clicked.connect(self.browsefiles)
        self.resnetButton.clicked.connect(self.predictResnet)
        self.densenetButton.clicked.connect(self.predictDensenet)

    def browsefiles(self):
        selected_file_path = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())[0]
        self.lineEdit.setText(selected_file_path)
        pixmap = QPixmap(selected_file_path)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setScaledContents(True)

    def goBack(self):
        self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['WelcomePage'])

    def predictResnet(self):
        self.predict_label('./40actionsresnet_8.40%.pth')

    def predictDensenet(self):
        self.predict_label('./40actionsdensenet121_6.84%.pth')

    def transform_image(self, image):
        my_transforms = transforms.Compose([transforms.Resize(256),
                                            transforms.ToTensor()])
        return my_transforms(image).unsqueeze(0)

    def predict_label(self, model_path):
        img_path = self.lineEdit.text()
        if not img_path:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("You did not upload the image")
            msg.setWindowTitle("Info")
            retval = msg.exec_()
            return
        model = load(model_path, map_location=device)
        model.eval()
        img = Image.open(img_path)
        img = img.resize((256, 256))
        img = self.transform_image(img)
        outputs = model.forward(img)
        _, y_hat = outputs.max(1)
        predicted_idx = y_hat.item()
        self.predictedActionText.setText(f"Predicted Action: {predicted_idx}") # if all classes is exist

