#!/usr/bin/env python  
# -*- coding:utf8 -*-  
  
import sys  
#reload(sys)  
#sys.setdefaultencoding('utf-8')  
  
import socket
import getpass

def strDecode(string):
    bytes_str = string.decode('utf-8', "replace")
    return (bytes_str)

def strEncode(string):
    bytes_str = string.encode('UTF-8')
    return (bytes_str)

class NetClient(object):  
    def tcpclient(self):  
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = clientSock
        clientSock.connect(('localhost', 9999))  

        # send to server
        msg = strEncode("this is send data from client")
        sendDataLen = clientSock.send(msg)
        print ("sendDataLen: {}".format(sendDataLen))
        
        # welcome
        recvData = clientSock.recv(1024)
        print ("recvData: {}".format(recvData))
        
        #recvData = clientSock.recv(1024)  
        #print ("sendDataLen: {}".format(sendDataLen))
        #print ("recvData: {}".format(recvData))
        
        # login
        self.login()
        clientSock.close()
    def login(self):
        user = input('login: ')
        sendDataLen = self.socket.send(strEncode(user))
        pwd = getpass.getpass('password: ')
        sendDataLen = self.socket.send(strEncode(pwd))
        
        #recvData = clientSock.recv(1024)  
        sendDataLen = self.socket.send(b'')
          
if __name__ == "__main__":  
    netClient = NetClient()  
    netClient.tcpclient()  
