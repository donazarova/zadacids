import socket, threading

class user():
    def __init__(self, username, password, role, address, port):
        self.username = username
        self.password = password
        self.role = role
        self.address = address
        self.port = port

users = {}

MAX = 65535

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('localhost', 1061))

while True:
    data, _address = s.recvfrom(MAX)
    data = data.decode().split('|')
    command = data[0]
    if command == "register":
        username = data[1]
        password = data[2]
        role = data[3]
        address = data[4]
        port = data[5]
        if username not in users:
            users[username] = user(username, password, role, address, int(port))
            s.sendto("ok".encode(), _address)

    elif command == "login":
        username = data[1]
        password = data[2]
        address = data[3]
        port = data[4]
        if username in users:
            if users[username].password == password:
                users[username].address = address
                users[username].port = int(port)
                s.sendto("ok".encode(), _address)

    elif command == "message":
        toUserName = data[1]
        msg = data[2]
        fromUserName = data[3]
        msgLength = len(msg.encode())

        if msgLength > 48:
            s.sendto("Message too long...".encode(), _address)

        if toUserName in users:
            toUser = users[toUserName]
            fromUser = users[fromUserName]
            if fromUser.role == "korisnik" and toUser.role == "vraboten" and msgLength > 24:
                s.sendto("Message too long by "+str(48-msgLength)+" bytes".encode(), _address)
            if fromUser.role == "korisnik" and toUser.role == "korisnik" and msgLength > 16:
                s.sendto("Message too long by "+str(48-msgLength)+" bytes".encode(), _address)
            if fromUser.role == "vraboten" and toUser.role == "vraboten" and msgLength > 26:
                s.sendto("Message too long by "+str(48-msgLength)+" bytes".encode(), _address)
            else:
                msgToSend = "Message from " + fromUserName + ":" + msg
                s.sendto(msgToSend.encode(), (toUser.address, toUser.port))

            
