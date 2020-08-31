import requests
import json
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_MainWindow
from PyQt5.QtCore import *
import time

host = 'http://127.0.0.1'
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setUpFunction()

    def setUpFunction(self):
        self.fileName0.setText('')
        self.fileName1.setText('')
        self.fileName2.setText('')
        self.progressBar0.setValue(0)
        self.progressBar1.setValue(0)
        self.progressBar2.setValue(0)
        self.pushButton.clicked.connect(self.submit)
        self.upDataDownloadInfo()

    def setBtn(self):
        self.pushButton.setEnabled(True)

    def submit(self):
        self.pushButton.setEnabled(False)
        self.data = {}
        self.data['downloader'] = self.comboBox.currentIndex()
        self.data['args'] = self.lineEdit.text()
        self.t1 = thread_1(data=self.data)
        self.t1._signal.connect(self.setBtn)
        self.t1.start()

    def upDataDownloadInfo(self):
        self.t2 = thread_2()
        self.t2._signal.connect(self.drawDonloadInfo)
        self.t2.start()

    def drawDonloadInfo(self,data):
        total = len(data)
        try:
            self.fileName0.setText(data['0']['title'])
            if data['0']['total_size'] == '0':
                self.progressBar0.setValue(0)
            else:
                self.progressBar0.setValue(float(str(float(data['0']['size'])/float(data['0']['total_size']))[:5])*100)
            self.fileName1.setText(data['1']['title'])
            if data['1']['total_size'] == '0':
                self.progressBar1.setValue(0)
            else:
                self.progressBar1.setValue(float(str(float(data['1']['size'])/float(data['1']['total_size']))[:5])*100)
            self.fileName2.setText(data['2']['title'])
            if data['2']['total_size'] == '0':
                self.progressBar2.setValue(0)
            else:
                self.progressBar2.setValue(float(str(float(data['2']['size'])/float(data['2']['total_size']))[:5])*100)
        except:
            pass            
class thread_2(QtCore.QThread):
    _signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(thread_2, self).__init__(parent=parent)

    def getDownloadInfo(self, url):
        self.r = requests.get(url)
        return json.loads(self.r.text)
    def getDownloadingInfo(self):
        global host
        url = host+':8002/download/info'
        self._signal.emit(self.getDownloadInfo(url))
    def run(self):
        import time
        while 1:
            self.getDownloadingInfo()
            time.sleep(0.5)

class thread_1(QtCore.QThread):
    _signal = pyqtSignal()

    def __init__(self, parent=None, data=None):
        super(thread_1, self).__init__(parent=parent)
        self.data = data
    def run(self):
        self.data_1 = {}
        if self.data['downloader'] == 0:
            self.data_1['downloader']= 'you-get'
        else:
            self.data_1['downloader'] = 'aria2'
        self.data_1['args'] = self.data['args']
        self.data_1['key'] = 'fakenews!'
        global host
        self.r = requests.post(host+':8002/download',self.data_1)
        self._signal.emit()
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()  # 实例化
    mainWindow.show()
    sys.exit(app.exec_())
