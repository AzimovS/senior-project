from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.uic import loadUi

import plot_graph
import resnet_train
from PageClass import GlobalVariables


class trainingByPicturePage(QDialog):
    def __init__(self, widget, *args):
        super(trainingByPicturePage, self).__init__()
        loadUi("Pages/trainingByPicturePage.ui", self)

        if len(args) > 0:
            self.data_path = args[-1]

        self.widget = widget
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
        self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['WelcomePage'])

    def gotoUTFPage(self):
        self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['uploadTrainingFilePage'])

    def addBorders(self, button):
        self.howItWorksText.hide()
        button.setStyleSheet("QPushButton {\n"
                                           "    border-radius: 20px;\n"
                                           "    background-color: rgb(224, 224, 224);\n"
                                           "\n"
                                           "    font: 70 14pt \"Century Gothic\"; color: black;\n"
                                           "    border-color: black;\n"
                                           "    border: 3px solid;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           "    background - color: rgb(73, 96, 96);\n"
                                           "}\n"
                                           "QPushButton:pressed{\n"
                                           "    background-color: black;\n"
                                           "}")


    def removeBorders(self, button):
        button.setStyleSheet("QPushButton {\n"
                                           "    border-radius: 20px;\n"
                                           "    background-color: rgb(224, 224, 224);\n"
                                           "\n"
                                           "    font: 70 14pt \"Century Gothic\"; color: black;\n"
                                           "    border-color: white;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           "    background - color: rgb(73, 96, 96);\n"
                                           "}\n"
                                           "QPushButton:pressed{\n"
                                           "    background-color: black;\n"
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
        self.graph_loss.move(1450, 0)
        self.graph_loss.show()

        self.graph_acc = plot_graph.GraphWindow(self, val_acc=val_acc)
        self.graph_acc.move(1450, 500)
        self.graph_acc.show()