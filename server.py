#!/usr/bin/env python

import socket, threading
from sys import stderr

def strDecode(string):
    bytes_str = string.decode('utf-8', "replace")
    return (bytes_str)

def strEncode(string):
    bytes_str = string.encode('UTF-8')
    return (bytes_str)

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

class ClientThread(threading.Thread):

    def __init__(self,ip,port,clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientsocket
        print ("[+] New thread started for "+ip+":"+str(port))

    def run(self):    
        print ("Connection from : "+ip+":"+str(port))

        # send to client
        msg = "Welcome to the server"
        msg = strEncode(msg)
        clientsock.send(msg)
        
        # Client reply
        inputName = self.csocket.recv(1024)
        print ("Client(%s:%s) sent : %s"%(self.ip, str(self.port), inputName))
        
        data = self.checkAccount()
        data = strEncode(data)
        clientsock.send(data)

        #data = "dummydata"
        while len(data):
            data = self.csocket.recv(2048)
            data = strDecode(data)
            print ("Client(%s:%s) sent : %s"%(self.ip, str(self.port), data))

        print ("Client at (%s:%s) disconnected..."%(self.ip, str(self.port)))
    def checkAccount(self):
        name = ['amy', 'john']
        clients = []
		
        inputName = self.csocket.recv(1024)
        inputName = strDecode(inputName)
        print ("Client(%s:%s) username : %s"%(self.ip, str(self.port), inputName))
        inputPWD = self.csocket.recv(1024)
        inputPWD = strDecode(inputPWD)
        print ("Client(%s:%s) password : %s"%(self.ip, str(self.port), inputPWD))
        
        if inputName in name:
            print(color.green+'user: %s Login Success'%(inputName)+color.end)
            return "Success"
        else:
            print(color.red+'user: %s Login Fail'%(inputName)+color.end)
            return "Fail"
		

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 9999

    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        tcpsock.bind((host,port))
    except Exception as msg:
        stderr.write("%s\n" % msg)
        tcpsock.close()
        exit()
    else:
        print ("Messemger Server Start")

    try:
        while True:
            print ("Listening for incoming connections...")
		
            tcpsock.listen(4)
            (clientsock, (ip, port)) = tcpsock.accept()

            #pass clientsock to the ClientThread thread object being created
            newthread = ClientThread(ip, port, clientsock)
            newthread.start()
    except KeyboardInterrupt as msg:
        stderr.write("%s\n" % msg)

    tcpsock.close()
