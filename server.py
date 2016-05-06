#!/usr/bin/env python

import socket, threading

class ClientThread(threading.Thread):

    def __init__(self,ip,port,clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientsocket
        print ("[+] New thread started for "+ip+":"+str(port))

    def run(self):    
        print ("Connection from : "+ip+":"+str(port))

        msg = "nWelcome to the servernn"
        b_msg = msg.encode('UTF-8')
        clientsock.send(b_msg)

        data = "dummydata"

        while len(data):
            data = self.csocket.recv(2048)
            print ("Client(%s:%s) sent : %s"%(self.ip, str(self.port), data))
            b_msg = "You sent me : ".encode('UTF-8')
            b_msg += data
            self.csocket.send(b_msg)

        print ("Client at "+self.ip+" disconnected...")

host = "0.0.0.0"
port = 9999

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcpsock.bind((host,port))

while True:
    tcpsock.listen(4)
    print ("nListening for incoming connections...")
    (clientsock, (ip, port)) = tcpsock.accept()

    #pass clientsock to the ClientThread thread object being created
    newthread = ClientThread(ip, port, clientsock)
    newthread.start()
