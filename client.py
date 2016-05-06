#!/usr/bin/env python  
# -*- coding:utf8 -*-  
  
import sys  
#reload(sys)  
#sys.setdefaultencoding('utf-8')  
  
import socket  
  
class NetClient(object):  
    def tcpclient(self):  
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        clientSock.connect(('localhost', 9999))  
  
        msg = "this is send data from client"
        b_msg = msg.encode('UTF-8')
        sendDataLen = clientSock.send(b_msg)  
        recvData = clientSock.recv(1024)  
        print ("sendDataLen: {}".format(sendDataLen))
        print ("recvData: {}".format(recvData))
        
        recvData = clientSock.recv(1024)  
        print ("sendDataLen: {}".format(sendDataLen))
        print ("recvData: {}".format(recvData))
        
        input('press any button to quit...')
          
        clientSock.close()  
          
if __name__ == "__main__":  
    netClient = NetClient()  
    netClient.tcpclient()  
