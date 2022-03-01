from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
import resnet_train
import plot_graph
from WelcomePageFile import WelcomePage
from uploadTrainingFilePageFile import uploadTrainingFilePage



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