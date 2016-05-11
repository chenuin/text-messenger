#!/usr/bin/env python

import socket, threading
from sys import stderr
from time import localtime, strftime, sleep

clients = {} # 紀錄client socket連線
chatwith = {} # 紀錄client訊息對象

friend = {} # 紀錄client friend list
unsend = []
unsend_msg = {}
unsend_file = {}

name = {'amy', 'john', 'tom'}
pwd = {'amy':'123', 'john':'456', 'tom':'789'}

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
    
def splitList(string):
    nameList = string.split(";")
    tmpList = {}
    for i in range(0, len(nameList), 1):
        #print(nameList[i])
        result = checkStatus(nameList[i])
        #print (result)
        if result in tmpList:
            tmpList[result] += ","
            tmpList[result] += nameList[i]
        else:
            tmpList[result] = nameList[i]
	
    if 'on' not in tmpList:
        tmpList['on'] = ""
    if 'off' not in tmpList:
        tmpList['off'] = ""
    strList = "::" + tmpList['on'] + ';' + tmpList['off']
    #print (strList)
    return strList

def checkStatus(name):
    if name in clients:
        return 'on'
    else:
        return 'off'

def rmName(string, target):
    name = string.split(";")
    strList = ""
    for i in range(0, len(name), 1):
        if name[i] != target:
            if len(strList) == 0:
                strList = name[i]
            else:
                strList += ";"
                strList += name[i]           
    return strList

def recvFile(sock, target):
    buf = ""
    while True:
        data = sock.recv(1024)
        #print (data)
        clients[target].send(data)
        if data == b'EOF':
            break
        #buf += data

class ServerThread(threading.Thread):

    def __init__(self,ip,port,clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientsocket
        print ("[+] New thread started for "+ip+":"+str(port))

    def run(self):    
        print ("Connection from : "+ip+":"+str(port))

        # send to client
        msg = "Welcome to the Message program"
        msg = strEncode(msg)
        self.csocket.send(msg)
        
        # Client reply
        inputName = self.csocket.recv(1024)
        print ("Client(%s:%s) sent : %s"%(self.ip, str(self.port), inputName))
        
        # check login
        log = self.checkAccount()
        # send message "Success" or "Fail" to client
        b_log = strEncode(log)
        self.csocket.send(b_log)
        
        if log == "Success":
            while True:
                command = self.csocket.recv(2048)
                data = strDecode(command)
                print(self.name +' send command: '+data)
                
                if self.name in chatwith:
                    index = chatwith[self.name]
                    if data == 'y' or data == 'yes':  # [4] reply yes
                        msg1 = strEncode("[5] Start transmiting file \"{}\"...".format(unsend_file[index]))
                        clients[chatwith[self.name]].send(msg1)
                        msg2 = strEncode("[6] Start receiving file \"{}\" from {}".format(unsend_file[index], chatwith[self.name]))
                        self.csocket.send(msg2)
                        print('')
                    elif data == 'start':
                        print ('[FILE] start upload')
                        recvFile(self.csocket, chatwith[self.name])
                        print ('[FILe] complete')
                        del chatwith[index]
                        del chatwith[self.name]
                        del unsend_file[self.name]
                    elif data == 'n' or data == 'no': # [4] reply no
                        print ('Refused')
                        msg1 = strEncode("[END] Reply for " + chatwith[self.name])
                        self.csocket.send(msg1)
                        msg2 = strEncode("[END] Denied from " + self.name)
                        clients[chatwith[self.name]].send(msg2)
                        #print (chatwith[index])
                        #print (chatwith[self.name])
                        del chatwith[index]
                        del chatwith[self.name]
                        del unsend_file[index]
                    elif data == "quit":
                        del chatwith[index]
                        del chatwith[self.name]
                        if index in unsend_file:
                            del unsend_file[index]
                        elif self.name in unsend_file:
                            del unsend_file[self.name]
                        print ('[FILE] quit')
                    else:
                        data = strEncode('Error command')
                        self.csocket.send(data)
                else:
                    if data[:6] == 'friend':
                        self.friendList(data)
                    elif data[:8] == 'sendfile':
                        self.fileSend(data)
                    elif data[:4] == 'send':
                        self.msgSend(data)
                    elif data == 'check msg':
                        self.msgUnsend()
                    elif data[:4] == 'exit':
                        data = strEncode(color.blue+'Good bye'+color.end)
                        self.csocket.send(data)
                        break
                    else:
                        data = strEncode('Error command')
                        self.csocket.send(data)
                
            del clients[self.name]
            print (color.red+"[OFF] %s Logout"% (self.name)+color.end)
        else:
            if self.name in clients:
                del clients[self.name]
                
        print ("Client at (%s:%s) disconnected..."%(self.ip, str(self.port)))

    def checkAccount(self):
        inputName = self.csocket.recv(1024)
        inputName = self.name = strDecode(inputName)
        print ("Client(%s:%s) username : %s"%(self.ip, str(self.port), inputName))
        inputPWD = self.csocket.recv(1024)
        inputPWD = strDecode(inputPWD)
        print ("Client(%s:%s) password : %s"%(self.ip, str(self.port), inputPWD))
        
        if (inputName in name) and (pwd[inputName] == inputPWD) and (inputName not in clients):
            print(color.green+'[ON] %s Login Success'%(inputName)+color.end)
            clients[self.name] = self.csocket
            return "Success"
        else:
            print(color.red+'[ERR] %s Login Fail'%(inputName)+color.end)
            return "Fail"

    def friendList(self, data):
        if data[7:11] == "list":    # friend list
            if self.name in friend:
                data = splitList(friend[self.name])
                #print (friend[self.name])
                data = strEncode(data)
            else:
                data = strEncode("none")
        elif data[7:10] == "add":   # friend add
            if self.name in friend:
                friend[self.name] += ";"
                friend[self.name] += data[11:]
            else:
                friend[self.name] = data[11:]

            tmp = data[11:]+" added into the friend list"
            data = strEncode(tmp)
        elif data[7:9] == "rm":     # friend rm
            if self.name in friend:
                strTmp = rmName(friend[self.name], data[10:])
                friend[self.name] = strTmp
                tmp = data[10:]+" removed from the friend list"
                if len(friend[self.name]) == 0:
                    del friend[self.name]
            else:
                tmp = "You friend list is empty"
            data = strEncode(tmp)
        else:
            data = strEncode('Error command')
        self.csocket.send(data)

    def msgSend(self, data):
        command, target, msg = data.split()
        timer = strftime("%Y-%m-%d %H:%M:%S", localtime())
        if (target in name) and (target in clients):       # online message
            msg1 = "[{} from {}] ".format(timer, self.name) + color.cyan + msg + color.end
            data = strEncode(msg1)
            clients[target].send(data)
            
            msg2 = "[{} to {}] ".format(timer, target) + color.purple + msg + color.end
            data = strEncode(msg2)
        elif (target in name) and (target not in clients): # offline message
            msg = "[{} from {}] ".format(timer, self.name) + color.yellow + msg + color.end
            if target in unsend:
                unsend_msg[target] += '\n'
                unsend_msg[target] += msg
            else:
                unsend.append(target)
                unsend_msg[target] = msg
            data = strEncode("Leave message to {}".format(target))
        else:
            data = strEncode(target+" is not exist")
        self.csocket.send(data)

    def msgUnsend(self):
        if self.name in unsend:
            data = strEncode(unsend_msg[self.name])			
            delIndex = unsend.index(self.name)
            del unsend[delIndex]
            del unsend_msg[self.name]
        else:
            data = strEncode("No message")
        self.csocket.send(data)
    
    def fileSend(self, data):
        command, target, fileName = data.split()
        if (target in chatwith) or (self.name in chatwith):
            data = strEncode(target+" is busy. Try again later!")
        else:
            if (target in name) and (target in clients):
                data = strEncode("[3] file \"{}\" from {}, accept it or not? (y/n)".format(fileName, self.name))
                clients[target].send(data)
                chatwith[target] = self.name
                chatwith[self.name] = target
                unsend_file[self.name] = fileName
            
                data = strEncode("[2] waiting for reply...")
            else:
                data = strEncode(target+" is offline, or not exist")
        self.csocket.send(data)    

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

            #pass clientsock to the ServerThread thread object being created
            newthread = ServerThread(ip, port, clientsock)
            newthread.start()
    except KeyboardInterrupt as msg:
        stderr.write("%s\n" % msg)

    tcpsock.close()
