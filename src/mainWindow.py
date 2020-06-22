import sys
import datetime as dt 
import cv2 as cv
import numpy as np
import pathlib
import PyQt5.QtGui as qg 
import PyQt5.QtWidgets as qw 

import GrabCutSingle as gcs
import GrabCutBatch as gcb
import InteractiveSingle as ins 

CUR_DIR = pathlib.Path(__file__).parent.absolute()

class MainWindow(qw.QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # window setting
        self.setGeometry(450, 150, 400, 300)
        self.setWindowTitle('Background Vison Main Panel')

        # component setting
        self.singleButton = qw.QPushButton('Single File Mode')
        self.batchButton = qw.QPushButton('Batch Mode')
        self.interactiveSingleButton = qw.QPushButton('Interactive Single Mode')
        self.interactiveBatchButton = qw.QPushButton('Interactive Batch Mode')
        self.quitButton = qw.QPushButton('Quit')

        # layout setting
        self.mainWidget = qw.QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.layout = qw.QGridLayout(self.mainWidget)
        self.layout.addWidget(self.singleButton, 0, 0, 1, 1)
        self.layout.addWidget(self.batchButton, 0, 1, 1, 1)
        self.layout.addWidget(self.interactiveSingleButton, 1, 0, 1, 1)
        self.layout.addWidget(self.interactiveBatchButton, 1, 1, 1, 1)
        self.layout.addWidget(self.quitButton, 2, 1, 1, 1)

        # slot
        self.singleButton.clicked.connect(self.openSingleMode)
        self.batchButton.clicked.connect(self.openBatchMode)
        self.interactiveSingleButton.clicked.connect(self.openInteractiveSingMode)
        self.interactiveBatchButton.clicked.connect(self.openInteractiveBatchMode)
        self.quitButton.clicked.connect(self.close)

        self.show()

    def openSingleMode(self):
        self.gcSingle = gcs.SingleMode()

    def openBatchMode(self):
        self.gcBatch = gcb.BatchMode()

    def openInteractiveSingMode(self):
        self.gcInteractiveBatch = ins.InteractiveSingleMode()

    def openInteractiveBatchMode(self):
        pass





if __name__ == "__main__":
    app = qw.QApplication(sys.argv)
    path = f'{CUR_DIR}/../archive/eye.png'
    app.setWindowIcon(qg.QIcon(path))

    mw = MainWindow()
    sys.exit(app.exec_())


