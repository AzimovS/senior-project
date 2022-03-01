from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
import train_features
from WelcomePageFile import WelcomePage
from uploadTrainingFilePageFile import uploadTrainingFilePage



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
        from main import widget
        gotoMainPage = WelcomePage()
        widget.addWidget(gotoMainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoUTFPage(self):
        from main import widget
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
        from main import visualizeFeaturePage, widget
        visualizePage = visualizeFeaturePage(self.clf, self.test_data)
        widget.addWidget(visualizePage)
        widget.setCurrentIndex(widget.currentIndex() + 1)