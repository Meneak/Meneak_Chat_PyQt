from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import socket
import threading
import sys


class CHATCLIENT(QMainWindow):
    def __init__(self):
        super(CHATCLIENT, self).__init__()


        self.setFixedSize(600,600)
        self.move(400,100)
        self.setWindowTitle('BrettChat')
        self.buildUI()
        self.show()

    def buildUI(self):

        self.connectButton = QPushButton('Connect', self)
        self.connectButton.setGeometry(10,5,50,20)
        self.connectButton.clicked.connect(self.serverConnect)

        self.commWindow = QTextEdit(self)
        self.commWindow.setText('Welcome to BrettChat.')
        self.commWindow.setGeometry(10,30,580,440)
        self.commWindow.setFocusPolicy(Qt.NoFocus)

        self.inputFrame = QFrame(self)
        self.inputFrame.setGeometry(10,480,580,100)

        self.inputArea = QLineEdit(self.inputFrame)
        self.inputArea.setGeometry(0,0,470,100)
        self.inputArea.returnPressed.connect(self.send)


        self.sendButton = QPushButton('Send', self.inputFrame)
        self.sendButton.setGeometry(480,0,100,100)
        self.sendButton.clicked.connect(self.send)


    def echo_Data(self, sock):
        while True:
            try:
                self.msg = sock.recv(2048).decode('utf-8')
                self.commWindow.append(self.msg)
            except OSError as e:
                self.s.send(bytes('Error'))

    # Mouse Drag Movement
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    @pyqtSlot()



    def serverConnect(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host = 'MUZEETO-MAIN'
            self.port = 4005
            self.address = (self.host, self.port)
            self.s.connect(self.address)
            threading.Thread(target=self.echo_Data, args=(self.s,)).start()

        except:
            self.commWindow.append('Error: Unable to connect to Host. %s' % self.host)


    def send(self):
        try:
            self.message = self.inputArea.text()
            if self.message == '':
                self.commWindow.append('Please enter some text first.')
            else:
                self.s.send(bytes(self.message, 'utf-8'))
                self.inputArea.clear()

        except:
            self.commWindow.append('Error: You are not connected to a server. Please connect to send messages.')
            self.inputArea.clear()




if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = CHATCLIENT()
    sys.exit(app.exec_())