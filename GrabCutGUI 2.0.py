import sys
import cv2 as cv
import numpy as np
import pathlib
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGridLayout,
                             QLabel, QPushButton)

CUR_DIR = pathlib.Path(__file__).parent.absolute()

class win(QDialog):
    def __init__(self):

        # 初始化一个img的ndarray, 用于存储图像
        self.img = np.ndarray(())

        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 300)
        self.btnOpen = QPushButton('Open', self)
        self.btnSave = QPushButton('Save', self)
        self.btnProcess = QPushButton('Process', self)
        self.btnQuit = QPushButton('Quit', self)
        self.label = QLabel()

        # 布局设定
        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 1, 3, 4)
        layout.addWidget(self.btnOpen, 4, 1, 1, 1)
        layout.addWidget(self.btnSave, 4, 2, 1, 1)
        layout.addWidget(self.btnProcess, 4, 3, 1, 1)
        layout.addWidget(self.btnQuit, 4, 4, 1, 1)

        # 信号与槽连接, PyQt5与Qt5相同, 信号可绑定普通成员函数
        self.btnOpen.clicked.connect(self.openSlot)
        self.btnSave.clicked.connect(self.saveSlot)
        self.btnProcess.clicked.connect(self.processSlot)
        self.btnQuit.clicked.connect(self.close)
        self.setWindowTitle('Background Vision')

    def openSlot(self):
        # 调用打开文件diglog
        fileName, tmp = QFileDialog.getOpenFileName(
            self, 'Open Image', './__data', '*.png *.jpg *.bmp')

        if fileName is '':
            return

        # 采用opencv函数读取数据
        self.img = cv.imread(fileName, -1)
        self.imgReal = self.img
        self.img = cv.resize(self.img, (360, 270))

        if self.img.size == 1:
            return

        self.refreshShow()

    def saveSlot(self):
        # 调用存储文件dialog
        fileName, tmp = QFileDialog.getSaveFileName(
            self, 'Save Image', './__data', '*.png *.jpg *.bmp', '*.png')

        if fileName is '':
            return
        if self.img.size == 1:
            return

        # 调用opencv写入图像
        cv.imwrite(fileName, self.img)

    def processSlot(self):
        if self.img.size == 1:
            return

        mask = np.zeros(self.imgReal.shape[:2], np.uint8)

        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        rect = (1, 1, self.imgReal.shape[1], self.imgReal.shape[0])
        cv.grabCut(self.imgReal, mask, rect, bgdModel, fgdModel, 10, cv.GC_INIT_WITH_RECT)
        print('Process Complete')

        mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
        self.imgReal = self.imgReal * mask2[:, :, np.newaxis]
        self.img = cv.resize(self.imgReal, (360, 270))

        # 显示图片
        # plt.subplot(121), plt.imshow(img)
        # plt.title("grabcut"), plt.xticks([]), plt.yticks([])
        # plt.subplot(122), plt.imshow(cv2.cvtColor(cv2.imread('varese.jpg'), cv2.COLOR_BGR2RGB))
        # plt.title("original"), plt.xticks([]), plt.yticks([])
        # plt.show()

        self.refreshShow()

    def refreshShow(self):
        # 提取图像的尺寸和通道, 用于将opencv下的image转换成Qimage
        height, width, channel = self.img.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()

        # 将Qimage显示出来
        self.label.setPixmap(QPixmap.fromImage(self.qImg))


if __name__ == '__main__':
    a = QApplication(sys.argv)
    path = f'{CUR_DIR}/assets/eye.png'
    a.setWindowIcon(QIcon(path))
    w = win()
    w.show()
    sys.exit(a.exec_())