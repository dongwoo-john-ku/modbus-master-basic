from PyQt5 import uic
from PyQt5.QtWidgets import *
import time, datetime, threading, sys, os
from datetime import datetime
from pymodbus.client.sync import ModbusTcpClient

form_class = uic.loadUiType("main.ui")[0]
class myWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.connectClicked)
        self.pushButton_2.clicked.connect(self.dirPushButtonClicked)
        self.dirInfo = './csv'
        self.label_5.setText(self.dirInfo)

        self.ipAddress = self.lineEdit.text()
        self.interval = self.lineEdit_4.text()
        self.startAddress = self.lineEdit_2.text()
        self.length = self.lineEdit_3.text()
        self.mbFunction = self.comboBox.currentText()

        global stop
        stop = False
        self.btnClicked = False

    def dirPushButtonClicked(self):
        dirInfo = QFileDialog.getExistingDirectory(self)
        self.label_5.setText(dirInfo)
        self.dirInfo = dirInfo

    def connectClicked(self):
        global stop
        if self.btnClicked :
            self.btnClicked = False
            stop = True
            self.pushButton.setText('start')
            self.label_3.setText('paused')
        else:
            self.ipAddress = self.lineEdit.text()
            self.interval = self.lineEdit_4.text()
            self.startAddress = self.lineEdit_2.text()
            self.length = self.lineEdit_3.text()
            self.mbFunction = self.comboBox.currentText()

            self.pushButton.setText('pause')
            self.label_3.setText('started')
            stop = False
            self.btnClicked = True
            t = MyThread(self.dirInfo, self.ipAddress, self.interval, self.startAddress, self.length, self.mbFunction)
            try:
                t.daemon = True   # Daemon True is necessary
                t.start()
            except:
                self.label_3.setText('Threading Exception!!!')
            else:
                print("Threading Started")

    def updateDisconnect(self):
        self.pushButton.setText('접속')

class MyThread(threading.Thread):
    def __init__(self, dirInfo, ipAddress, interval, startAddress, length, mbFunction):
        threading.Thread.__init__(self)
        self.daemon = True
        self.lengthBuffer = 0
        self.dataBuffer = ''
        self.dirInfo = dirInfo

        self.ipAddress = ipAddress
        self.interval = int(interval)
        self.startAddress = int(startAddress)
        self.length = int(length)

        print(self.startAddress , self.length)
        if mbFunction =='Read Input Registers':
            self.mbFunction = 0
        else:
            self.mbFunction = 1

    def run(self):
        c = ModbusTcpClient(self.ipAddress, 502)

        while True:
            # break condition is required
            now = datetime.now()
            curDate = str(now.year) +'-' + str(now.month) +'-' + str(now.day)
            # curDate = '2019-12-11'

            if curDate != self.dataBuffer :
                self.dataBuffer = curDate

            try:
                if not (os.path.isdir(self.dirInfo)):
                    os.makedirs(os.path.join(self.dirInfo))
            except OSError :
                print("Failed to create directory!!!!!")

            curDateFileName = self.dirInfo + '/' + curDate + '.csv'

            try:
                if self.mbFunction == 0:
                    readDataList = c.read_input_registers(self.startAddress, self.length).registers
                else:
                    readDataList = c.read_holding_registers(self.startAddress, self.length).registers
            except:
                print("failed to connect the Modbus/Tcp slave")
            else:
                print(readDataList)
                readDataListconverted = convert(now.time(), readDataList)
                with open(curDateFileName, "a") as f:
                    f.write(readDataListconverted)

            time.sleep(self.interval/1000)

            if stop == True:
                print("Break!")
                break

def convert(curTime, list):
    # Converting integer list to string list
    s = [str(i) for i in list]
    # Join list items using join()
    res = ", ".join(s)
    res = str(curTime) + ', ' + res
    res += '\n'
    return res

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = myWindow()
    myWindow.show()
    sys.exit(app.exec_())
