from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.uic import loadUi

import train_features
from PageClass import GlobalVariables
from PageClass.visualizeFeaturePage import visualizeFeaturePage

class trainingByFeaturePage(QDialog):
    def __init__(self, widget, *args):
        super(trainingByFeaturePage, self).__init__()
        if (len(args) > 0):
            self.data_path = args[-1]
        self.widget = widget
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
        visualizePage = visualizeFeaturePage(self.widget, self.clf, self.test_data)
        self.widget.insertWidget(GlobalVariables.PAGE_TO_INDEX['visualizeFeaturePage'], visualizePage)
        self.widget.setCurrentIndex(GlobalVariables.PAGE_TO_INDEX['visualizeFeaturePage'])
