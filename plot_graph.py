# import sys
# import matplotlib
# matplotlib.use('Qt5Agg')
# import pandas as pd
# from PyQt5 import QtCore, QtGui, QtWidgets
#
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
# from matplotlib.figure import Figure
#
#
# class MplCanvas(FigureCanvasQTAgg):
#
#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#         super(MplCanvas, self).__init__(fig)
#
#
# class GraphWindow(QtWidgets.QMainWindow):
#     def __init__(self, parent=None, *args, **kwargs):
#         QtWidgets.QMainWindow.__init__(self)
#
#         sc = MplCanvas(self, width=5, height=4, dpi=100)
#         df = None
#         if 'train_loss' in kwargs:
#             df = pd.DataFrame({'Training loss': kwargs['train_loss'],
#                                'Validation loss': kwargs['val_loss']})
#         else:
#             df = pd.DataFrame({'Validation acc': kwargs['val_acc']})
#         df.plot(ax=sc.axes)
#
#         # sc.axes.plot(kwargs['train_loss'], label='Training loss')
#         # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
#         toolbar = NavigationToolbar(sc, self)
#
#         layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(toolbar)
#         layout.addWidget(sc)
#
#         # Create a placeholder widget to hold our toolbar and canvas.
#         widget = QtWidgets.QWidget()
#         widget.setLayout(layout)
#         self.setCentralWidget(widget)
