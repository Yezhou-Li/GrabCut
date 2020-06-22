import sys
from PyQt5.QtWidgets import QApplication
import mainWindow as mw 

app = QApplication(sys.argv)
mw = mw.MainWindow()
sys.exit(app.exec_())