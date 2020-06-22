import sys
import os
import math
import shutil
import platform
import datetime as dt 
import cv2 as cv
import numpy as np
import pathlib
import PyQt5.QtGui as qg 
import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc

CUR_DIR = pathlib.Path(__file__).parent.absolute()

class InteractiveSingleMode(qw.QMainWindow):

    def __init__(self):
        super().__init__()
        self.upperLeftX = 300
        self.upperLeftY = 40
        self.windowWidth = 870
        self.windowHeight = 500
        self.pictureWindowWidth = round(self.windowWidth*0.6)
        self.pictureWindowHeight = round(self.windowHeight*0.6)
        
        self.compressSchemeDefault = '25%'
        self.compressSchemeDict = {
            self.compressSchemeDefault: cv.IMREAD_REDUCED_COLOR_4,
            '100%': cv.IMREAD_COLOR,
            '50%': cv.IMREAD_REDUCED_COLOR_2,
            '12.5%': cv.IMREAD_REDUCED_COLOR_8}

        self.iteration = 6
        if platform.system == 'Windows': self.pathSep = '\\'
        else: self.pathSep = '/'

        self.initUI()

    def initUI(self):
        # window setting
        self.setGeometry(self.upperLeftX, self.upperLeftY, self.windowWidth, self.windowHeight)
        self.setWindowTitle('Interactive Single Mode')

        # components setting
        self.openButton = qw.QPushButton('Open')
        self.saveButton = qw.QPushButton('Save')
        self.quitButton = qw.QPushButton('Quit')
        self.compressLabel = qw.QLabel('Compress')

        self.compressComboBox = qw.QComboBox()
        self.compressComboBox.addItems(self.compressSchemeDict.keys())

        self.pictureOriginalSizeLabel = qw.QLabel('Original Size: 0MB')
        self.pictureCompressedSizeLabel = qw.QLabel('Reduced Size: 0MB')
        self.pictureSavedSizeLabel = qw.QLabel('Saved Size: 0MB')

        self.pictureLabel = qw.QLabel()
        self.processButton = qw.QPushButton('Process')
        self.configureButton = qw.QPushButton('Configure')
        self.cropButton = qw.QPushButton('Crop')
        self.iterationLabel = qw.QLabel('Iteration:')
        self.iterationText = qw.QLineEdit(str(self.iteration))
        self.logLabel = qw.QLabel('log')
        self.logText = qw.QTextBrowser()

        # layout setting
        self.mainWidget = qw.QWidget()
        self.setCentralWidget(self.mainWidget)
        self.layout = qw.QGridLayout(self.mainWidget)
        self.layout.addWidget(self.openButton, 0, 0, 1, 2)
        self.layout.addWidget(self.saveButton, 0, 2, 1, 2)
        self.layout.addWidget(self.quitButton, 0, 4, 1, 2)
        self.layout.addWidget(self.compressLabel, 1, 0, 1, 2)
        self.layout.addWidget(self.compressComboBox, 1, 2, 1, 4)
        self.layout.addWidget(self.pictureOriginalSizeLabel, 2, 0, 1, 2)
        self.layout.addWidget(self.pictureCompressedSizeLabel, 2, 2, 1, 2)
        self.layout.addWidget(self.pictureSavedSizeLabel, 2, 4, 1, 2)

        self.layout.setRowStretch(3, 1)
        self.layout.addWidget(self.pictureLabel, 3, 0, 1, 6)
        self.layout.addWidget(self.processButton, 4, 0, 1, 2)
        self.layout.addWidget(self.configureButton, 4, 2, 1, 2)
        self.layout.addWidget(self.cropButton, 4, 4, 1, 2)
        self.layout.addWidget(self.iterationLabel, 5, 0, 1, 3)
        self.layout.addWidget(self.iterationText, 5, 3, 1, 3)

        # self.layout.addWidget(self.logLabel, 0, 7, 1, 1)
        self.layout.addWidget(self.logText, 0, 7, 6, 6)

        # slot setting
        self.openButton.clicked.connect(self.openPicture)
        self.saveButton.clicked.connect(self.savePicture)
        self.quitButton.clicked.connect(self.close)
        self.processButton.clicked.connect(self.processPicture)
        self.compressComboBox.activated[str].connect(self.selectCompress)

        self.cropButton.clicked.connect(self.cropPicture)

        self.show()

    def getDiskSizeOfPicture(self, )

    def printf(self, tb, str):
        tb.append(str)
        cursor = tb.textCursor()
        tb.moveCursor(cursor.End)
        qw.QApplication.processEvents()

    def refreshShow(self, img):
        height, width, _ = img.shape
        bytesPerLine = 3 * width
        qImg = qg.QImage(img.data, width, height, bytesPerLine,
                           qg.QImage.Format_RGB888).rgbSwapped()
        self.pictureLabel.setPixmap(qg.QPixmap.fromImage(qImg))

    def resizeShownPicture(self):
        row, col, _ = self.imgShown.shape
        if row<=self.pictureWindowHeight and col<=self.pictureWindowWidth:
            return
        else:
            row_height = row/self.pictureWindowHeight
            col_width = col/self.pictureWindowWidth
            reduceRatio = max(row_height, col_width)
            rowNew = round( row/reduceRatio )
            colNew = round( col/reduceRatio )
            self.imgShown = cv.resize(self.imgShown, (colNew, rowNew), interpolation = cv.INTER_AREA)

    def refreshSize(self, img, label):
        self.imgReducedSizeByte = sys.getsizeof(self.imgReduced)
        self.imgReducedSizeMB = round( self.imgReducedSizeByte/1024/1024, 2)
        self.pictureCompressedSizeLabel.setText(f'Reduced Size: {self.imgReducedSizeMB}MB')
        self.show()

    def openPicture(self):
        self.openedFileName, _ = qw.QFileDialog.getOpenFileName(
            self, 'Open Image', f'{CUR_DIR}/../testData', '*.png *.jpg')
        if self.openedFileName == '':
            self.printf(self.logText, 'Open file action canceled')
            return

        if platform.system() == "Windows":
            # windows下需要进行文件分隔符转换
            self.openedFileName = self.openedFileName.replace('/','\\')

        self.printf(self.logText, f'Open file:\n{self.openedFileName}')

        self.imgUnchanged = cv.imread(self.openedFileName, cv.IMREAD_UNCHANGED)
        if self.imgUnchanged is None:
            self.printf(self.logText, f'Can not open file:\n{self.openedFileName}')
        self.imgReduced = cv.imread(self.openedFileName, 
            self.compressSchemeDict[self.compressSchemeDefault])
        
        self.imgShown = self.imgReduced
        self.resizeShownPicture()
        self.refreshShow(self.imgShown)

        # self.imgSizeByte = qc.QFileInfo(self.openedFileName).size()
        # self.imgSizeMB = round( self.imgSizeByte/1024/1024, 2)
        # self.pictureOriginalSizeLabel.setText(f'Original Size: {self.imgSizeMB}MB')

        self.imgSizeByte = sys.getsizeof(self.imgUnchanged)
        self.imgSizeMB = round( self.imgSizeByte/1024/1024, 2)
        self.pictureOriginalSizeLabel.setText(f'Original Size: {self.imgSizeMB}MB')

        self.imgReducedSizeByte = sys.getsizeof(self.imgReduced)
        self.imgReducedSizeMB = round( self.imgReducedSizeByte/1024/1024, 2)
        self.pictureCompressedSizeLabel.setText(f'Reduced Size: {self.imgReducedSizeMB}MB')

    def savePicture(self):
        self.openedFileDir = pathlib.Path(self.openedFileName).parent.absolute()
        self.openedFileDir = f'{self.openedFileDir}{self.pathSep}result'
        if os.path.exists(self.openedFileDir):
            shutil.rmtree(self.openedFileDir, ignore_errors=True)
        os.mkdir(self.openedFileDir)
        self.saveFileName = f'{self.openedFileDir}{self.pathSep}{self.openedFileName.split(self.pathSep)[-1]}'
        cv.imwrite(self.saveFileName, self.imgimgReducedCroped)
        self.printf(self.logText, f'Save croped picture as:')
        self.printf(self.logText, f'{self.saveFileName}')

        self.savedFileSizeByte = qc.QFileInfo(self.saveFileName).size()
        self.savedFileSizeMB = round( self.savedFileSizeByte/1024/1024, 2)
        self.pictureSavedSizeLabel.setText(f'Saved Size: {self.savedFileSizeMB}MB')

    def processPicture(self):
        self.printf(self.logText, "Select a ROI and then press SPACE or ENTER button!")
        self.printf(self.logText, "Cancel the selection process by pressing c button!")
        roi = cv.selectROI(windowName="Select ROI", img=self.imgReduced, showCrosshair=True, fromCenter=False)
        cv.destroyAllWindows()
        self.printf(self.logText, f'Region of Interest (x,y,w,h):{str(roi)}')

        startTime = dt.datetime.now()
        mask = np.zeros(self.imgReduced.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        cv.grabCut(self.imgReduced, mask, roi, bgdModel, fgdModel, self.iteration, cv.GC_INIT_WITH_RECT)

        mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
        row, col, channel = self.imgReduced.shape
        for i in range(row):
            for j in range(col):
                if mask2[i, j] == 0:
                    for k in range(channel):
                        self.imgReduced[i, j, k] = 255

        self.imgShown = self.imgReduced
        self.resizeShownPicture()
        self.refreshShow(self.imgShown)

        endTime = dt.datetime.now()
        spanMicroSeconds = round( (endTime-startTime).microseconds/1000000, 2)
        # self.printf(self.logText, f'Time: {spanSeconds}s or {spanMicroSeconds}s')
        self.printf(self.logText, f'Time: {spanMicroSeconds}s')

        self.imgimgReducedCroped = self.imgReduced[ roi[1]:roi[1]+roi[3], roi[0]:roi[2]+roi[0], :]

    def selectCompress(self, text):
        self.printf(self.logText, f'{text}: {self.compressSchemeDict[text]}')
        self.imgReduced = cv.imread(self.openedFileName, self.compressSchemeDict[text])
        self.imgShown = self.imgReduced
        self.resizeShownPicture()
        self.refreshShow(self.imgShown)
        self.refreshSize(self.imgReduced, self.pictureCompressedSizeLabel)

    def cropPicture(self):
        pass





if __name__ == "__main__":
    app = qw.QApplication(sys.argv)
    path = f'{CUR_DIR}/../archive/eye.png'
    app.setWindowIcon(qg.QIcon(path))

    ism = InteractiveSingleMode()
    sys.exit(app.exec_())
