import cv2
import sys
import pathlib
import PyQt5.QtCore as qc 
import PyQt5.QtWidgets as qw 
import PyQt5.QtGui as qg 

CUR_DIR = pathlib.Path(__file__).parent.absolute()

class GrabcutApp(qw.QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Background Vision'
        self.appIconPath = f'{CUR_DIR}/assets/eye.png'
        
        self.initUI()

    def initUI(self):
        mainWidget = qw.QWidget()
        self.setCentralWidget(mainWidget)

        picLabel = qw.QLabel()
        print(qc.QFile.exists(f'{CUR_DIR}/assets/hat.jpg'))
        pic = qg.QPixmap(f'{CUR_DIR}/assets/hat.jpg')
        picLabel.setPixmap(pic)

        grid = qw.QGridLayout()
        grid.addWidget(picLabel, 1, 1)
        mainWidget.setLayout(grid)

        self.statusBar()
        openFile = qw.QAction(qg.QIcon(f'{CUR_DIR}/assets/open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+o')
        openFile.setStatusTip('Open new file')
        openFile.triggered.connect(self.showDialog)
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu('File')
        fileMenu.addAction(openFile)
        self.setWindowTitle(self.title)
        self.setGeometry(300, 300, 450, 300)
        self.show()

    def showDialog(self):
        home_dir = str(pathlib.Path.home())
        fname = qw.QFileDialog.getOpenFileName(self, 'Open file', home_dir)

        if fname[0]:
            print(fname[0])
            img = qg.QPixmap(fname[0])
            self.imgLabel.setPixmap(img)
            

def main():
    app = qw.QApplication(sys.argv)
    window = GrabcutApp()
    app.setWindowIcon(qg.QIcon(window.appIconPath))
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()