import sys
import PyQt5.QtWidgets as qw 
import mainWindow as mw 

app = qw.QApplication(sys.argv)
mw = mw.MainWindow()
sys.exit(app.exec_())