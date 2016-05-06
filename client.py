#!/usr/bin/env python  
# -*- coding:utf8 -*-  
  
import sys  
#reload(sys)  
#sys.setdefaultencoding('utf-8')  
  
import socket
import getpass

class color:
    end =  "\033[0m"
    black = "\033[30m"
    red =   "\033[31m"
    green = "\033[32m"
    yellow ="\033[33m"
    blue =  "\033[34m"
    purple ="\033[35m"
    cyan =  "\033[36m"
    grey =  "\033[37m"

def strDecode(string):
    bytes_str = string.decode('utf-8', "replace")
    return (bytes_str)

def strEncode(string):
    bytes_str = string.encode('UTF-8')
    return (bytes_str)

def printStatus(string):
    strON, strOFF = string.split(";")

    onList = strON.split(",")
    offList = strOFF.split(",")
    for i in range(0, len(onList), 1):
        if onList[i] == "":
            break;
        print(" {0:10} : online".format(onList[i]))
    for i in range(0, len(offList), 1):
        if offList[i] == "":
            break;
        print(" {0:10} : offline".format(offList[i]))

class NetClient(object):  
    def tcpclient(self):  
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = clientSock
        clientSock.connect(('localhost', 9999))  

        # send to server
        msg = strEncode("Data send from client")
        sendDataLen = clientSock.send(msg)
        #print ("sendDataLen: {}".format(sendDataLen))
        
        # Server reply(welcome)
        recvData = clientSock.recv(1024)
        print ("%s"%(recvData))
        
        # login
        if self.login():
            print(color.green+'Login Success'+color.end)
            while True:
                command = input("> ")
                
                self.socket.send(strEncode(command))
                recvData = self.socket.recv(1024)

                if command == 'friend list':
                    printStatus(strDecode(recvData))
                elif command == 'quit':
                    print(strDecode(recvData))
                    break
                else:
                    print(strDecode(recvData))
        else:
            print(color.red+'Login Fail'+color.end)

        clientSock.close()

    def login(self):
        user = input('login: ')
        sendDataLen = self.socket.send(strEncode(user))
        pwd = getpass.getpass('password: ')
        sendDataLen = self.socket.send(strEncode(pwd))
        
        # Server reply login result
        recvData = self.socket.recv(1024)
        recvData = strDecode(recvData)
        if recvData == "Success":
            return 1
        else:
            return 0
          
if __name__ == "__main__":  
    netClient = NetClient()  
    netClient.tcpclient()  
