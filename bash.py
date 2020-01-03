#copyright © Pavel Fedorov. Do not use without a reference (citation).
#!/usr/bin/env python
# coding: utf-8

import base64
import paramiko
import yaml



class Server:
    def __init__(self, ip, port, user, psw):
        self.ip = ip
        self.port = port
        self.user = user
        self.psw = psw
        self.commands = []
        self.online = False
    def print(self):      
        if self.online:
            print("server " + self.ip + " online")
            for item in self.commands:
                print(item)
        else:
            print("server " + self.ip + " OFFLINE")
class EmailInfo:
    def __init__(self, smtpServer, user, psw, recipient):
        self.smtpServer = smtpServer
        self.recipient = recipient
        self.user = user
        self.psw = psw

def ReadConfig():
    servers=[]
    emailInfo = None
    with open("bash.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        email = cfg['email']
        recipient = email['recipient']
        smtpServer = email['smtpServer']
        user = email['user']
        psw = email['psw']
        emailInfo = EmailInfo(smtpServer, user, psw, recipient) 
            
        cf_servers = cfg['servers']
        for section in cf_servers:
            ip = section
            cf_server = cf_servers[section]
            port = cf_server['port']
            user = cf_server['user']
            psw = cf_server['psw']
            server = Server(ip, port, user, psw)
            servers.append(server)
    return servers, emailInfo


# In[84]:



def CheckServer(server):
    try:
        with paramiko.SSHClient() as client:
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server.ip, username=server.user, port = server.port, password=server.psw)
            server.online = True
            stdin, stdout, stderr = client.exec_command("free | grep Mem | awk '{print $4/$2 * 100.0}'")
            server.commands.append("free RAM % " + stdout.readlines()[0].strip())
            stdin, stdout, stderr = client.exec_command("systemctl is-active nginx")
            server.commands.append("nginx " + stdout.readlines()[0].strip())
            client.close()
    except:
        pass
    server.print()



servers, emailInfo = ReadConfig()
for server in servers:
    CheckServer(server)





from threading import Timer
def hello():
    print("hello, world")

t = Timer(30.0, hello)
t.start()  # after 30 seconds, "hello, world" will be printed




