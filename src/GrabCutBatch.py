import sys
import os
import datetime as dt 
import shutil
import platform
import cv2 as cv
import numpy as np
import pathlib
import PyQt5.QtGui as qg
import PyQt5.QtWidgets as qw

CUR_DIR = pathlib.Path(__file__).parent.absolute()

class BatchMode(qw.QMainWindow):

    def __init__(self):
        super().__init__()
        self.pictureFormat = ['jpg', 'png', 'jpeg']
        self.iterTimes = 10
        self.resultDir = 'results'
        self.initUI()

    def initUI(self):
        # window setting
        self.move(300, 100)
        self.setWindowTitle('Background Vision Batch Mode')

        # component setting
        self.chooseDir = qw.QPushButton('Choose Directory', self)
        self.startButton = qw.QPushButton('Start Processing', self)
        self.iterLabel = qw.QLabel('Iteration: ', self)
        self.iterInput = qw.QLineEdit(self)
        self.selectedFilesLabel = qw.QLabel('Selected Files:')
        self.selectedFilesText = qw.QTextBrowser()
        self.processedFilesLabel = qw.QLabel('Completed Files:')
        self.processedFilesText = qw.QTextBrowser()
        self.logLabel = qw.QLabel('log:')
        self.logText = qw.QTextBrowser()

        # layout setting
        self.mainWidget = qw.QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.layout = qw.QGridLayout(self.mainWidget)
        self.layout.addWidget(self.chooseDir, 0, 0, 1, 1)
        self.layout.addWidget(self.startButton, 0, 1, 1, 1)
        self.layout.addWidget(self.iterLabel, 1, 0, 1, 1)
        self.layout.addWidget(self.iterInput, 1, 1, 1, 1)
        self.layout.addWidget(self.selectedFilesLabel, 2, 0, 1, 1)
        self.layout.addWidget(self.selectedFilesText, 3, 0, 4, 1)
        self.layout.addWidget(self.processedFilesLabel, 2, 1, 1, 1)
        self.layout.addWidget(self.processedFilesText, 3, 1, 4, 1)
        self.layout.addWidget(self.logLabel, 7, 0, 1, 1)
        self.layout.addWidget(self.logText, 8, 0, 1, 4)

        # slot
        self.chooseDir.clicked.connect(self.openDirDialog)
        self.startButton.clicked.connect(self.startProcessing)
        self.iterInput.returnPressed.connect(self.inputIteration)

        self.show()

    def inputIteration(self):
        self.iterTimes = int(self.iterInput.text())
        self.printf(self.logText, f'Current iteration = {self.iterTimes}')

    def clearOutput(self):
        self.selectedFilesText.clear()
        self.processedFilesText.clear()
        self.logText.clear()


    def openDirDialog(self):
        self.clearOutput()
        self.printf(self.logText, f'Current iteration = {self.iterTimes}')
        self.dirPath = qw.QFileDialog.getExistingDirectory(
            self, "choose directory", f'{CUR_DIR}')

        if not os.path.exists(self.dirPath): return

        if platform.system() == "Windows":
            # windows下需要进行文件分隔符转换
            self.dirPath = self.dirPath.replace('/','\\')
            self.resultDirFull = f'{self.dirPath}\\{self.resultDir}\\'
            if os.path.exists(self.resultDirFull):
                shutil.rmtree(self.resultDirFull, ignore_errors=True)
            os.mkdir(self.resultDirFull)
            self.printf( self.logText, f'Processed pictures will be stored in:\n{self.resultDirFull}' )
        else:
            self.resultDirFull = f'{self.dirPath}/{self.resultDir}/'
            if os.path.exists(self.resultDirFull):
                shutil.rmtree(self.resultDirFull, ignore_errors=True)
            os.mkdir(self.resultDirFull)
            self.printf( self.logText, f'Processed pictures will be stored in:\n{self.resultDirFull}')

        self.filesUnderDir = os.listdir(self.dirPath)
        
        self.picturesList = []
        self.picturesFullPathList = []
        for fileName in self.filesUnderDir:
            fileName = fileName.lower()
            if fileName.split('.')[-1] in self.pictureFormat:
                self.selectedFilesText.append(fileName)
                self.picturesList.append(fileName)

                if platform.system() == 'Windows': fileName = self.dirPath + "\\" + fileName
                else: fileName = self.dirPath + "/" + fileName 
                self.picturesFullPathList.append(fileName)

    def printf(self, tb, str):
        tb.append(str)   #在指定的区域显示提示信息
        cursor = tb.textCursor()
        tb.moveCursor(cursor.End)  #光标移到最后，这样就会自动显示出来
        qw.QApplication.processEvents()  #一定加上这个功能，不然有卡顿

    def startProcessing(self):
        for i in range(len(self.picturesList)):
            startTime = dt.datetime.now()
            self.grabcut(self.picturesFullPathList[i])
            endTime = dt.datetime.now()
            spanTime = endTime - startTime
            minutes = spanTime.seconds // 60
            seconds = spanTime.seconds % 60
            self.printf( self.processedFilesText,f'{self.picturesList[i]}  Time: {minutes} min, {seconds} sec.')
        self.printf( self.logText, '\nAll pictures are processed.')

    def grabcutTest(self, picName):
        if platform.system() == 'Windows':
            picNameShort = picName.split('\\')[-1]
        else:
            picNameShort = picName.split('/')[-1]
        resultPath = f'{self.resultDirFull}{picNameShort}'
        # cv.imwrite(resultPath, self.imgReal)
        self.printf( self.logText, f'{picName} is saved at {resultPath}.' )

    def grabcut(self, picName):
        self.imgReal = cv.imread(picName, -1)
        if self.imgReal.size == 1:
            self.printf( self.logText, f'\n{picName}\ndoes not exits.')
            return
        else:
            self.printf( self.logText, f'\n{picName}\nloaded.')

        mask = np.zeros(self.imgReal.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        rect = (1, 1, self.imgReal.shape[1], self.imgReal.shape[0])

        cv.grabCut(self.imgReal, mask, rect, bgdModel, fgdModel, self.iterTimes, cv.GC_INIT_WITH_RECT)
        self.printf( self.logText, f'\n{picName}\nis processed after {self.iterTimes} iterations.')

        mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
        row, col, channel = self.imgReal.shape
        for i in range(row):
            for j in range(col):
                if mask2[i, j] == 0:
                    for k in range(channel):
                        self.imgReal[i, j, k] = 255

        if platform.system() == 'Windows':
            picNameShort = picName.split('\\')[-1]
        else:
            picNameShort = picName.split('/')[-1]
        resultPath = f'{self.resultDirFull}{picNameShort}'
        cv.imwrite(resultPath, self.imgReal)
        self.printf( self.logText, f'\n{picName}\nis saved at\n{resultPath}.' )
        



if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    path = f'{CUR_DIR}/archive/eye.png'
    app.setWindowIcon(qg.QIcon(path))
    bw = BatchMode()
    sys.exit(app.exec_())