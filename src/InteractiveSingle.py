import sys
import os
import math
import shutil
import platform
import datetime as dt 
import cv2 as cv
import numpy as np
import pathlib

from PyQt5.QtGui import QGuiApplication, QImage, QPixmap
# from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QTextBrowser, QWidget, QFileDialog, QGridLayout, QApplication, QComboBox
from PyQt5.QtCore import QFileInfo

CUR_DIR = pathlib.Path(__file__).parent.absolute()

class InteractiveSingleMode(QMainWindow):

    def __init__(self):
        super().__init__()
        self.updateFlag = 1
        self.upperLeftX = 300
        self.upperLeftY = 40
        self.windowWidth = 870
        self.windowHeight = 600
        self.pictureWindowWidth = round(self.windowWidth*0.6)
        self.pictureWindowHeight = round(self.windowHeight*0.5)
        
        self.picWHTextWidth = self.windowWidth*0.082
        self.compressSchemeCurrent = '50%'
        self.compressSchemeDict = {
            '50%': cv.IMREAD_REDUCED_COLOR_2,
            '25%': cv.IMREAD_REDUCED_COLOR_4,
            '100%': cv.IMREAD_COLOR,
            '12.5%': cv.IMREAD_REDUCED_COLOR_8}

        self.iteration = 3
        if platform.system == 'Windows': self.pathSep = '\\'
        else: self.pathSep = '/'

        self.initUI()

    def initUI(self):
        # window setting
        self.setGeometry(self.upperLeftX, self.upperLeftY, self.windowWidth, self.windowHeight)
        self.setWindowTitle('Interactive Single Mode')
        QGuiApplication.processEvents()

        # components setting
        self.openButton = QPushButton('Open')
        self.saveButton = QPushButton('Save')
        self.quitButton = QPushButton('Quit')
        self.compressLabel = QLabel('Compress')
        self.compressComboBox = QComboBox()
        self.compressComboBox.addItems(self.compressSchemeDict.keys())

        self.pictureOriginalLabel = QLabel('Original')
        self.pictureOriginalWidthLabel = QLabel('W')
        self.pictureOriginalWidthText = QLineEdit()
        self.pictureOriginalWidthText.setMaximumWidth(self.picWHTextWidth)
        self.pictureOriginalWidthText.setReadOnly(True)
        self.pictureOriginalHeightLabel = QLabel('H')
        self.pictureOriginalHeightText = QLineEdit()
        self.pictureOriginalHeightText.setMaximumWidth(self.picWHTextWidth)
        self.pictureOriginalHeightText.setReadOnly(True)
        self.pictureCompressedLabel = QLabel('Compressed')
        self.pictureCompressedWidthLabel = QLabel('W')
        self.pictureCompressedWidthText = QLineEdit()
        self.pictureCompressedWidthText.setMaximumWidth(self.picWHTextWidth)
        self.pictureCompressedWidthText.setReadOnly(True)
        self.pictureCompressedHeightLabel = QLabel('H')
        self.pictureCompressedHeightText = QLineEdit()
        self.pictureCompressedHeightText.setMaximumWidth(self.picWHTextWidth)
        self.pictureCompressedHeightText.setReadOnly(True)
        self.pictureSavedLabel = QLabel('Saved')
        self.pictureSavedWidthLabel = QLabel('W')
        self.pictureSavedWidthText = QLineEdit()
        self.pictureSavedWidthText.setMaximumWidth(self.picWHTextWidth)
        self.pictureSavedWidthText.setReadOnly(True)
        self.pictureSavedHeightLabel = QLabel('H')
        self.pictureSavedHeightText = QLineEdit()
        self.pictureSavedHeightText.setMaximumWidth(self.picWHTextWidth)
        self.pictureSavedHeightText.setReadOnly(True)

        self.pictureLabel = QLabel()
        self.processButton = QPushButton('Process')
        self.configureButton = QPushButton('Configure')
        self.cropButton = QPushButton('Crop')
        self.iterationLabel = QLabel('Iteration:')
        self.iterationText = QLineEdit(str(self.iteration))
        self.logLabel = QLabel('log')
        self.logText = QTextBrowser()

        # layout setting
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.layout = QGridLayout(self.mainWidget)
        self.layout.addWidget(self.openButton, 0, 0, 1, 2)
        self.layout.addWidget(self.saveButton, 0, 2, 1, 2)
        self.layout.addWidget(self.quitButton, 0, 4, 1, 2)
        self.layout.addWidget(self.compressLabel, 1, 0, 1, 2)
        self.layout.addWidget(self.compressComboBox, 1, 2, 1, 4)

        self.layout.addWidget(self.pictureOriginalLabel, 2, 0, 1, 1)
        self.layout.addWidget(self.pictureOriginalWidthLabel, 2, 1, 1, 1)
        self.layout.addWidget(self.pictureOriginalWidthText, 2, 2, 1, 1)
        self.layout.addWidget(self.pictureOriginalHeightLabel, 2, 3, 1, 1)
        self.layout.addWidget(self.pictureOriginalHeightText, 2, 4, 1, 1)
        self.layout.addWidget(self.pictureCompressedLabel, 3, 0, 1, 1)
        self.layout.addWidget(self.pictureCompressedWidthLabel, 3, 1, 1, 1)
        self.layout.addWidget(self.pictureCompressedWidthText, 3, 2, 1, 1)
        self.layout.addWidget(self.pictureCompressedHeightLabel, 3, 3, 1, 1)
        self.layout.addWidget(self.pictureCompressedHeightText, 3, 4, 1, 1)
        self.layout.addWidget(self.pictureSavedLabel, 4, 0, 1, 1)
        self.layout.addWidget(self.pictureSavedWidthLabel, 4, 1, 1, 1)
        self.layout.addWidget(self.pictureSavedWidthText, 4, 2, 1, 1)
        self.layout.addWidget(self.pictureSavedHeightLabel, 4, 3, 1, 1)
        self.layout.addWidget(self.pictureSavedHeightText, 4, 4, 1, 1)

        self.layout.setRowStretch(5, 1)
        self.layout.addWidget(self.pictureLabel, 5, 0, 1, 6)
        self.layout.addWidget(self.processButton, 6, 0, 1, 6)
        # self.layout.addWidget(self.configureButton, 6, 2, 1, 2)
        # self.layout.addWidget(self.cropButton, 6, 4, 1, 2)
        self.layout.addWidget(self.iterationLabel, 7, 0, 1, 3)
        self.layout.addWidget(self.iterationText, 7, 3, 1, 3)

        # self.layout.addWidget(self.logLabel, 0, 7, 1, 1)
        self.layout.addWidget(self.logText, 0, 7, 9, 7)

        # slot setting
        self.openButton.clicked.connect(self.openPicture)
        self.saveButton.clicked.connect(self.savePicture)
        self.quitButton.clicked.connect(self.close)
        self.processButton.clicked.connect(self.processPicture)
        self.compressComboBox.activated[str].connect(self.selectCompress)
        self.iterationText.returnPressed.connect(self.inputIteration)

        self.cropButton.clicked.connect(self.cropPicture)

        self.show()

    def printf(self, tb, str):
        tb.append(str)
        cursor = tb.textCursor()
        tb.moveCursor(cursor.End)
        QApplication.processEvents()

    def refreshShow(self, img):
        height, width, _ = img.shape
        bytesPerLine = 3 * width
        qImg = QImage(img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()
        self.pictureLabel.setPixmap(QPixmap.fromImage(qImg))

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
        try:
            self.openedFileName, _ = QFileDialog.getOpenFileName(
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
                self.compressSchemeDict[self.compressSchemeCurrent])
            
            self.imgShown = self.imgReduced
            self.resizeShownPicture()
            self.refreshShow(self.imgShown)

            # self.imgSizeByte = qc.QFileInfo(self.openedFileName).size()
            # self.imgSizeMB = round( self.imgSizeByte/1024/1024, 2)
            # self.pictureOriginalSizeLabel.setText(f'Original Size: {self.imgSizeMB}MB')
            # self.imgSizeByte = sys.getsizeof(self.imgUnchanged)
            # self.imgSizeMB = round( self.imgSizeByte/1024/1024, 2)
            # self.pictureOriginalSizeLabel.setText(f'Original Size: {self.imgSizeMB}MB')

            self.pictureOriginalWidthText.setText(f'{self.imgUnchanged.shape[1]}')
            self.pictureOriginalHeightText.setText(f'{self.imgUnchanged.shape[0]}')
            self.pictureCompressedWidthText.setText(f'{self.imgReduced.shape[1]}')
            self.pictureCompressedHeightText.setText(f'{self.imgReduced.shape[0]}')
            self.pictureSavedWidthText.clear()
            self.pictureSavedHeightText.clear()
        except:
            self.printf(self.logText, f'Error')
            self.setGeometry(self.upperLeftX, self.upperLeftY, self.windowWidth+self.updateFlag, self.windowHeight)
            self.updateFlag *= -1
            return
        

    def savePicture(self):
        try:
            self.openedFileDir = pathlib.Path(self.openedFileName).parent.absolute()
            self.openedFileDir = f'{self.openedFileDir}{self.pathSep}result'
            if os.path.exists(self.openedFileDir):
                shutil.rmtree(self.openedFileDir, ignore_errors=True)
            os.mkdir(self.openedFileDir)
            self.saveFileName = f'{self.openedFileDir}{self.pathSep}{self.openedFileName.split(self.pathSep)[-1]}'
            cv.imwrite(self.saveFileName, self.imgimgReducedCroped)
            self.printf(self.logText, f'Save croped picture as:')
            self.printf(self.logText, f'{self.saveFileName}')

            self.savedFileSizeByte = QFileInfo(self.saveFileName).size()
            self.savedFileSizeMB = round( self.savedFileSizeByte/1024/1024, 2)
            self.pictureSavedWidthText.setText(f'{self.imgimgReducedCroped.shape[1]}')
            self.pictureSavedHeightText.setText(f'{self.imgimgReducedCroped.shape[0]}')
        except:
            return

    def processPicture(self):
        try:
            # if not self.imgReduce is None:
            #     self.printf(self.logText, "Select a ROI and then press SPACE or ENTER button!")
            #     self.printf(self.logText, "Cancel the selection process by pressing c button!")
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
            self.printf(self.logText, f'Iteration: {self.iteration}')

            self.imgimgReducedCroped = self.imgReduced[ roi[1]:roi[1]+roi[3], roi[0]:roi[2]+roi[0], :]
        except:
            self.printf(self.logText, f'Error')
            self.setGeometry(self.upperLeftX, self.upperLeftY, self.windowWidth+self.updateFlag, self.windowHeight)
            self.updateFlag *= -1
            return

    def selectCompress(self, text):
        try:
            # self.printf(self.logText, f'{text}: {self.compressSchemeDict[text]}')
            self.compressSchemeCurrent = text
            self.imgReduced = cv.imread(self.openedFileName, self.compressSchemeDict[text])
            self.imgShown = self.imgReduced
            self.resizeShownPicture()
            self.refreshShow(self.imgShown)
            self.pictureCompressedWidthText.clear()
            self.pictureCompressedWidthText.setText(f'{self.imgReduced.shape[1]}')
            self.pictureCompressedHeightText.clear()
            self.pictureCompressedHeightText.setText(f'{self.imgReduced.shape[0]}')
            self.setGeometry(self.upperLeftX, self.upperLeftY, self.windowWidth+self.updateFlag, self.windowHeight)
            self.updateFlag *= -1
        except:
            return

    def cropPicture(self):
        pass

    def inputIteration(self):
        self.iteration = int(self.iterationText.text())
        self.printf(self.logText, f'Current iteration = {self.iteration}')




if __name__ == "__main__":
    app = QApplication(sys.argv)
    # path = f'{CUR_DIR}/../archive/eye.png'
    # app.setWindowIcon(qg.QIcon(path))

    ism = InteractiveSingleMode()
    sys.exit(app.exec_())
