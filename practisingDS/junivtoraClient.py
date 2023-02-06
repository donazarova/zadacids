import socket, threading, struct
import xmlrpc.client as client

def recv_all(sock, length):
	data = ''
	while len(data) < length:
		more = sock.recv(length - len(data)).decode()
		if not more:
			raise EOFError('socket closed %d bytes into a %d-byte message' % (len(data), length))
		data += more
	return data.encode()

def receiveData(s) -> str:
    length = struct.unpack("!i", recv_all(s, 4))[0]
    return recv_all(s, length).decode()

def sendData(s, messageToSend):
    length = len(messageToSend)
    msg = struct.pack("!i", length) + messageToSend.encode()
    s.sendall(msg)

def sendMessage():
    userOrGroup = input("user/group ")
    if userOrGroup == "user":
        toUser = input("user ")
        address = proxy.getUserAddress(toUser)
        port = proxy.getUserPort(toUser)
        msg = input("message ")
        msgToSend = username + "|" + msg
        sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sendSocket.connect((address, port))
        sendData(sendSocket, msgToSend)
    elif userOrGroup == "group":
        toGroup = input("group ")
        msg = input("message ")
        msgToSend = username + " in " + toGroup + "|" + msg
        usersToSend = proxy.getGroupUsers(username, toGroup)
        for user in usersToSend:
            address = user.address
            port = user.port
            sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sendSocket.connect((address, port))
            sendData(sendSocket, msgToSend)

proxy = client.ServerProxy('http://127.0.0.1:7001', allow_none=True)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sl.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sl.bind(('localhost', 1061))

def hear(s):
    s.listen(5)
    while True:
        sc, sockname = s.accept()
        msg = receiveData(sc)
        print("Got message: " + msg)

command = input("type Y to register ")
najaven = False
currentUser = ""

if command == "Y":
    username = input("username ")
    password = input("password ")
    selectedRole = input("vospituvac/gotvac/administrator")
    info = ""
    if selectedRole == "vospituvac":
        info = input("grupa ")
    elif selectedRole == "gotvac":
        info = input("specijalizacija ")
    if info == "administracija":
        info = input("ne smee administracija, vnesi odnovo ")
    if selectedRole == "administrator":
        info = "administracija"
    response = proxy.register(username, password, selectedRole, info, sl.getsockname()[0], sl.getsockname()[1])
    print(response)

print("Logging in...\n")
username = input("username ")
password = input("password ")
najaven = proxy.login(username, password, sl.getsockname()[0], sl.getsockname()[1])
if not najaven:
    print("login fail")
    exit()

threading.Thread(target = hear, args=(sl,)).start()

if selectedRole == "administrator":
    while True:
        command = input("send/creategroup ")
        if command == "send":
            sendMessage()
        elif command == "creategroup":
            groupName = input("group name ")
            proxy.create(groupName)
elif selectedRole == "vospituvac" or selectedRole == "gotvac":
    while True:
        sendMessage()
    

