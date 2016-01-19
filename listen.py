#coding:utf-8
import threading
import socket
import re
import os
import urllib
import urllib.request as urllib2
encoding = 'utf-8'
BUFSIZE = 1024

# a read thread, read data from remote
class Reader(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
        self.index_url="http://mirrors.aliyun.com/pypi/simple/"
        self.dir_url="http://mirrors.aliyun.com/pypi/packages/source/"
        self.pkgname=""
        self.pkgdir=[]
        self.storepath="/home/alvin/pypi"
        
    def run(self):
        while True:
             f=open("listen.log","a+")
             data = self.client.recv(BUFSIZE)
             if(data):
                string = bytes.decode(data, encoding)
                f.writelines(string)
                self.pkgname=re.findall("GET /(.*?)/",string)
                self.pkgname="".join(self.pkgname)
                f.writelines("*******the pkgname: "+self.pkgname+"*******")
                self.getpkgdir()
                pkgdir=self.pkgdir
                for pkg in pkgdir:
                	  self.download(self.dir_url+pkg)

             else:
                break
        peername=self.client.getpeername()
        f.writelines("close:"+str(peername))
        f.writelines("\n=============================================\n")
        f.close()

    def getpkgdir(self):

    	  pkg_url=self.index_url+self.pkgname
    	  request=urllib2.Request(pkg_url)
    	  response=urllib2.urlopen(request)
    	  data=response.read().decode("utf-8")
    	  self.pkgdir=re.findall('<a href=".*?source/(.*?)" rel="internal">',data)

    def download(self,url):
        os.system("wget -P %s %s"%(self.storepath,url))
    
    def readline(self):
        rec = self.inputs.readline()
        if rec:
            string = bytes.decode(rec, encoding)
            if len(string)>2:
                string = string[0:-2]
            else:
                string = ' '
        else:
            string = False
        return string

# a listen thread, listen remote connect
# when a remote machine request to connect, it will create a read thread to handle
class Listener(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        self.sock.listen(0)
    def run(self):
        print("listener started")
        while True:
            client, cltadd = self.sock.accept()
            Reader(client).start()
            cltadd = cltadd
            print("accept a connect")
            client.send("Not Found!Retry after some while")
lst  = Listener(9000)   # create a listen thread
lst.start() # then start