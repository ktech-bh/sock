import sys
import time

from PyQt5.QtWidgets import *
from PyQt5 import uic
import socket
from datetime import datetime
import server_s2
import os
from threading import Thread


form_class = uic.loadUiType("Server_ping.ui")[0]

# ####
# p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# p.bind(("", 0))
# p.listen(1)
# port = p.getsockname()[1]
# p.close()
# #####




class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.threads = []
        self.setupUi(self)

        self.pushButton_open.clicked.connect(self.pushbutton_open_func)
        self.pushButton_close.clicked.connect(self.pushbutton_close_func)
        self.pushButton_send.clicked.connect(self.pushbutton_send_func)
        self.pushButton_clear.clicked.connect(self.pushbutton_clear_func)

        self.progressBar.setValue(0)

        self.lineEdit_ip.setText(socket.gethostbyname(socket.gethostname()))
        # self.lineEdit_port.setText(str(port))
        self.lineEdit_port.setText(str(8888))
        self.s2 = server_s2.ServerSocket(self)
        self.pushButton_ping.clicked.connect(self.pushbutton_ping_func)

        self.tableWidget_iplist.setColumnWidth(0, 120)
        self.tableWidget_iplist.setColumnWidth(1, 40)
        self.tableWidget_iplist.setColumnWidth(2, 140)

    def pushbutton_ping_func(self):
        for i in self.tableWidget_iplist.selectedIndexes():
            chk_ip = self.tableWidget_iplist.item(i.row(), 0).text()
            ping = os.popen(f'ping -n 4 {chk_ip}').read()
            ping_msg = f' - - - - {chk_ip} ping test start - - - - -' \
                       f'{ping}' \
                       f' - - - - {chk_ip} ping test   end - - - - '

            self.list_chat.addItem(QListWidgetItem(ping_msg))

            parsing_start = ping.index("(") + 1
            parsing_end = ping.index("%")

            loss_per = ping[parsing_start:parsing_end]

            # progressbar_loss_per = 100 - int(loss_per)

            # self.progressBar.setValue(progressbar_loss_per)



    def isNumber(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def pushbutton_open_func(self):

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        ip = self.lineEdit_ip.text()
        port = self.lineEdit_port.text()

        ip_chk = ip.replace(".", "")
        port_chk = port.replace(".", "")

        # print("ip 입력 양식", self.isNumber(ip_chk))
        # print("port 입력 양식", self.isNumber(port_chk))

        if not self.isNumber(ip_chk):
            QMessageBox.information(self, '오류', 'IP 주소 확인')

        if not self.isNumber(port_chk):
            QMessageBox.information(self, '오류', 'Port 확인')

        if self.s2.open(ip, int(port)):
            open_msg = f'{current_time}│ Server Open'
            self.list_chat.addItem(QListWidgetItem(open_msg))
            # print("서버 오픈")

    def pushbutton_close_func(self):
        self.s2.close()
        self.chat_list.clear()

        # print("close")

    def update_client(self, addr, isConnect=False):

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        row = self.tableWidget_iplist.rowCount()

        if isConnect:
            self.tableWidget_iplist.setRowCount(row + 1)
            self.tableWidget_iplist.setItem(row, 0, QTableWidgetItem(addr[0]))
            self.tableWidget_iplist.setItem(row, 1, QTableWidgetItem(str(addr[1])))
            join_msg = f'{current_time}│ -- IP:{addr[0]}  Port:{str(addr[1])} 접속 --'
            print(join_msg)

            self.list_chat.addItem(QListWidgetItem(join_msg))

            threading = Thread(target=self.ping_test)
            self.threads.append(threading)
            threading.start()

        else:
            out_msg = f'{current_time}│ -- IP:{addr[0]}  Port:{str(addr[1])} 종료 -- '
            for i in range(row):
                ip = self.tableWidget_iplist.item(i, 0).text()
                port = self.tableWidget_iplist.item(i, 1).text()
                if addr[0] == ip and str(addr[1]) == port:
                    self.tableWidget_iplist.removeRow(i)
                    self.list_chat.addItem(QListWidgetItem(out_msg))
                    break

    def ping_test(self):
        row = self.tableWidget_iplist.rowCount()
        # self.progressBar.setValue(100)
        while True:
            if row >= 1:
                self.progressBar.setValue(100)
                try:
                    for i in range(row):
                        ip_addr = self.tableWidget_iplist.item(i, 0)
                        ip_addr = ip_addr.text()

                        response = os.popen(f'ping -n 3 {ip_addr}').read()
                        parsing_start = response.index("(") + 1
                        parsing_end = response.index(")")
                        ping_loss_per = response[parsing_start:parsing_end]
                        ping_avg = response.index("평균")
                        ping_avg = response[ping_avg:].replace("= ", "").strip()

                        ping_result = f'{ping_avg} ({ping_loss_per})'

                        self.tableWidget_iplist.setItem(i, 2, QTableWidgetItem(str(ping_result)))
                        QTableWidget.QApplication.processEvents()

                except :
                    row = self.tableWidget_iplist.rowCount()
                    if row == 0:
                        self.progressBar.setValue(0)

                    break















        ############################################

    def update_msg(self, msg):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        fin_msg = f'{current_time}│{msg}'

        self.list_chat.addItem(QListWidgetItem(fin_msg))
        self.list_chat.setCurrentRow(self.list_chat.count() - 1)

    def pushbutton_send_func(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        message = self.lineEdit_input.text()
        message = f'[Server] : {message}'
        if len(message) == 0:
            return

        self.update_msg(message)
        self.s2.send(message)
        self.lineEdit_input.clear()

    def pushbutton_clear_func(self):
        self.list_chat.clear()

    def closeEvent(self, err):
        self.s2.close()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()


