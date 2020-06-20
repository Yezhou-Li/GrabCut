import sys
import datetime as dt 
import cv2 as cv
import numpy as np
import pathlib
import PyQt5.QtGui as qg 
import PyQt5.QtWidgets as qw 
import GrabCutSingle as gcs
import GrabCutBatch as gcb

CUR_DIR = pathlib.Path(__file__).parent.absolute()

class MainWindow(qw.QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # window setting
        self.setGeometry(300, 300, 360, 270)
        self.setWindowTitle('Background Vison Main Panel')

        # component setting
        self.singleButton = qw.QPushButton('Single File Mode', self)
        self.batchButton = qw.QPushButton('Batch Mode', self)

        # layout setting
        self.mainWidget = qw.QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.layout = qw.QGridLayout(self.mainWidget)
        self.layout.addWidget(self.singleButton, 0, 0, 1, 1)
        self.layout.addWidget(self.batchButton, 0, 1, 1, 1)

        # slot
        self.singleButton.clicked.connect(self.openSingleMode)
        self.batchButton.clicked.connect(self.openBatchMode)

        self.show()

    def openSingleMode(self):
        self.gcSingle = gcs.SingleMode()
        self.gcSingle.show()

    def openBatchMode(self):
        self.gcBatch = gcb.BatchMode()





if __name__ == "__main__":
    app = qw.QApplication(sys.argv)
    path = f'{CUR_DIR}/archive/eye.png'
    app.setWindowIcon(qg.QIcon(path))

    mw = MainWindow()
    sys.exit(app.exec_())


