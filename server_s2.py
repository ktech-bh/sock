from threading import Thread
from socket import *
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from _datetime import datetime

class ServerSocket(QObject):
    update_signal = pyqtSignal(tuple, bool)
    recv_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.bListen = False
        self.clients = []
        self.ip = []
        self.threads = []

        self.update_signal.connect(self.parent.update_client)
        self.recv_signal.connect(self.parent.update_msg)

    def __del__(self):
        self.close()

    def open(self, ip, port):
        self.server = socket(AF_INET, SOCK_STREAM)

        try:
            self.server.bind((ip, port))
        except Exception as err:
            print(f'Error [1] : {err}')
        else:
            self.bListen = True
            self.threading = Thread(target=self.listen, args=(self.server,))
            self.threading.start()
            print("Server open")

        return True

    def close(self):

        self.bListen = False
        if hasattr(self, 'server'):
            self.server.close()
            print("Server close")

    def listen(self, server):

        while self.bListen:
            server.listen(5)
            try:
                client, addr = server.accept()
            except Exception as err:
                print(f'Error [2] : {err}')
                break
            else:
                self.clients.append(client)
                self.ip.append(addr)
                self.update_signal.emit(addr, True)
                threading = Thread(target=self.receive, args=(addr, client))
                self.threads.append(threading)
                threading.start()

        self.remove_all_clients()
        self.server.close()

    def receive(self, addr, client):

        while True:
            try:
                recv = client.recv(1024)
            except Exception as err:
                print(f'Error [3] : {err}')
                break
            else:
                msg = str(recv, encoding='utf-8')
                msg = f'[{addr[0]}] : {msg}'

                if msg:
                    self.send(msg)
                    self.recv_signal.emit(msg)
                    # print("msg", addr)

        self.remove_client(addr, client)

    def send(self, msg):
        try:
            for i in self.clients:
                i.send(msg.encode())
        except Exception as err:
            print(f'Err [4] : {err}')

    def remove_client(self, addr, client):
        f = -1
        for i, j in enumerate(self.clients):
            if j == client:
                f = i
                break
        client.close()
        self.ip.remove(addr)
        self.clients.remove(client)

        del (self.threads[f])

        self.update_signal.emit(addr, False)

    def remove_all_clients(self):
        for i in self.clients:
            i.close()

        for addr in self.ip:
            self.update_signal.emit(addr, False)

        self.ip.clear()
        self.clients.clear()
        self.threads.clear()




