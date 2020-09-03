import requests
import json
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_MainWindow
from PyQt5.QtCore import *
import time

# global
host = 'http://'


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
        self.pushButton_2.clicked.connect(self.upDataDownloadInfoStart)

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

    def upDataDownloadInfoStart(self):
        self.pushButton_2.clicked.disconnect()
        self.pushButton_2.clicked.connect(self.upDataDownloadInfoStop)
        self.pushButton_2.setText('解绑')
        global host
        host += self.lineEdit_2.text()
        # 进度条信息更新
        self.t2 = thread_2()
        self.t2._signal.connect(self.drawDonloadProcessInfo)
        self.t2._signal_2.connect(self.drawDownloadWaitTable)
        self.t2._signal_3.connect(self.drawDownloaCpltTable)
        self.t2.start()
        # 等待列表更新

    def upDataDownloadInfoStop(self):
        self.t2.stop_flg = 1
        self.pushButton_2.clicked.disconnect()
        self.pushButton_2.clicked.connect(self.upDataDownloadInfoStart)
        self.lineEdit_2.setText('')
        self.pushButton_2.setText('绑定')
        global host
        host = 'http://'

    def drawDownloadWaitTable(self, data):
        self.tableWidget.horizontalHeader().setStretchLastSection(True)  # 拉倒最大
        self.tableWidget.horizontalHeader().resizeSection(0, 200)
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(i)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['序号', '下载参数'])
        if data[0] == 0:
            return 0
        data = data[1]
        for i in range(len(data)):
            row = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(row+1)
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i)))
            self.tableWidget.setItem(
                row, 1, QtWidgets.QTableWidgetItem(data[str(i)]['args']))

    def drawDownloaCpltTable(self, data):
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)  # 拉倒最大
        self.tableWidget_2.horizontalHeader().resizeSection(0, 200)
        for i in range(self.tableWidget_2.rowCount()):
            self.tableWidget_2.removeRow(i)
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setHorizontalHeaderLabels(['序号', '文件名', '下载参数'])
        if data[0] == 0:
            return 0
        data = data[1]
        for i in range(len(data)):
            row = self.tableWidget_2.rowCount()
            self.tableWidget_2.setRowCount(row+1)
            self.tableWidget_2.setItem(row, 0,QtWidgets.QTableWidgetItem(str(i)))
            self.tableWidget_2.setItem(
                row, 1, QtWidgets.QTableWidgetItem(data[str(i)]['title']))
            self.tableWidget_2.setItem(
                row, 2, QtWidgets.QTableWidgetItem(data[str(i)]['origin']))

    def drawDonloadProcessInfo(self, data):
        if data[0] == 0:
            self.lineEdit_2.setText('检查地址是否正确')
            return 0
        data = data[1]
        try:
            self.fileName0.setText(data['0']['title'])
            if data['0']['total_size'] == '0':
                self.progressBar0.setValue(0)
            else:
                self.progressBar0.setValue(
                    float(str(float(data['0']['size'])/float(data['0']['total_size']))[:5])*100)
        except:
            self.fileName0.setText('')
            self.progressBar0.setValue(0)
        try:
            self.fileName1.setText(data['1']['title'])
            if data['1']['total_size'] == '0':
                self.progressBar1.setValue(0)
            else:
                self.progressBar1.setValue(
                    float(str(float(data['1']['size'])/float(data['1']['total_size']))[:5])*100)
        except:
            self.fileName1.setText('')
            self.progressBar1.setValue(0)
        try:
            self.fileName2.setText(data['2']['title'])
            if data['2']['total_size'] == '0':
                self.progressBar2.setValue(0)
            else:
                self.progressBar2.setValue(
                    float(str(float(data['2']['size'])/float(data['2']['total_size']))[:5])*100)
        except:
            self.fileName2.setText('')
            self.progressBar2.setValue(0)


class thread_2(QtCore.QThread):
    _signal = pyqtSignal(list)
    _signal_2 = pyqtSignal(list)
    _signal_3 = pyqtSignal(list)

    def __init__(self, parent=None):
        super(thread_2, self).__init__(parent=parent)
        self.stop_flg = 0

    def getInfo(self, url):
        try:
            self.r = requests.get(url)
            return [1, json.loads(self.r.text)]
        except:
            return [0, 0]

    def getDownloadProcessInfo(self):
        return self.getInfo(url=host+':8002/download/info')

    def getDownloadWaitListInfo(self):
        return self.getInfo(url=host+':8002/download/waitInfo')

    def getDownloadCpltListInfo(self):
        return self.getInfo(url=host+':8002/download/cpltInfo')

    def getDownloadingInfo(self):
        global host
        self._signal.emit(self.getDownloadProcessInfo())
        self._signal_2.emit(self.getDownloadWaitListInfo())
        self._signal_3.emit(self.getDownloadCpltListInfo())

    def run(self):
        import time
        while (1):
            if self.stop_flg == 1:
                break
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
            self.data_1['downloader'] = 'you-get'
        else:
            self.data_1['downloader'] = 'aria2'
        self.data_1['args'] = self.data['args']
        self.data_1['key'] = 'fakenews!'
        global host
        self.r = requests.post(host+':8002/download', self.data_1)
        self._signal.emit()
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()  # 实例化
    mainWindow.show()
    sys.exit(app.exec_())
