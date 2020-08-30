import sys
sys.path.append('/home/zy/Rpi3BAndSamb')
import requests
import json

from PyQt5 import QtCore, QtGui, QtWidgets
from src.QtUi.ui import Ui_MainWindow
from PyQt5.QtCore import *


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setUpFunction()

    def setUpFunction(self):
        self.pushButton.clicked.connect(self.submit)
        self.upDataDownloadInfo()

    def setBtn(self):
        self.pushButton.setEnabled(True)

    def submit(self):
        self.pushButton.setEnabled(False)
        data = {}
        data['downloader'] = self.comboBox.currentIndex()
        data['args'] = self.lineEdit.text()
        t = thread_1(data=data)
        t._signal.connect(self.setBtn)
        t.start()

    def upDataDownloadInfo(self):
        t = thread_2()
        t._signal.connect(self.drawDonloadInfo)
        t.start()

    def drawDonloadInfo(self,data):
        total = len(data)
        try:
            self.fileName0.setText(data['0']['title'])
            if data['0']['total_size'] == '0':
                self.progressBar0.setValue(0)
            else:
                self.progressBar0.setValue(float(str(int(data['0']['size'])/int(data['0']['total_size']))[:5])*100)
            self.fileName1.setText(data['1']['title'])
            if data['1']['total_size'] == '0':
                self.progressBar1.setValue(0)
            else:
                self.progressBar1.setValue(float(str(int(data['1']['size'])/int(data['1']['total_size']))[:5])*100)
            self.fileName2.setText(data['2']['title'])
            if data['2']['total_size'] == '0':
                self.progressBar2.setValue(0)
            else:
                self.progressBar2.setValue(float(str(int(data['2']['size'])/int(data['2']['total_size']))[:5])*100)
        except:
            self.fileName0.setText('')
            self.fileName1.setText('')
            self.fileName2.setText('')
            self.progressBar0.setValue(0)
            self.progressBar1.setValue(0)
            self.progressBar2.setValue(0)
            
class thread_2(QtCore.QThread):
    _signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(thread_2, self).__init__(parent=parent)

    def getDownloadInfo(self, url):
        r = requests.get(url)
        return json.loads(r.text)
    def getDownloadingInfo(self):
        url = 'http://127.0.0.1:8002/download/info'
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
        data_1 = {}
        if self.data['downloader'] == 0:
            data_1['downloader']= 'you-get'
        else:
            data_1['downloader'] = 'aria2'
        data_1['args'] = self.data['args']
        data_1['key'] = 'fakenews!'
        r = requests.post('http://127.0.0.1:8002/download',data_1)
        self._signal.emit()
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()  # 实例化
    mainWindow.show()
    sys.exit(app.exec_())
