import sys 
# import pathlib
# from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QGridLayout, QApplication

import GrabCutSingle as gcs
import GrabCutBatch as gcb
import InteractiveSingle as ins 

# CUR_DIR = pathlib.Path(__file__).parent.absolute()

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # window setting
        self.setGeometry(450, 150, 400, 300)
        self.setWindowTitle('Background Vison Main Panel')

        # component setting
        self.singleButton = QPushButton('Single File Mode')
        self.batchButton = QPushButton('Batch Mode')
        self.interactiveSingleButton = QPushButton('Interactive Single Mode')
        self.interactiveBatchButton = QPushButton('Interactive Batch Mode')
        self.quitButton = QPushButton('Quit')

        # layout setting
        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.layout = QGridLayout(self.mainWidget)
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
    app = QApplication(sys.argv)
    # path = f'{CUR_DIR}/../archive/eye.png'
    # app.setWindowIcon(QIcon(path))

    mw = MainWindow()
    sys.exit(app.exec_())


