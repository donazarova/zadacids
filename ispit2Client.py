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

if command == "Y":
    username = input("username ")
    password = input("password ")
    ime = input("ime ")
    prezime = input("prezime ")
    telefon = input("telefon ")
    email = input("email ")
    godini = input("godini ")
    iskustvo = input("praktikant/junior/senior ")
    sektor = input("sektor ")
    response = proxy.register(username, password, ime, prezime, telefon, email, godini, iskustvo, sektor)
    print(response)

print("Logging in...\n")
username = input("username ")
password = input("password ")
najaven = proxy.login(username, password, sl.getsockname()[0], sl.getsockname()[1])
if not najaven:
    print("login fail")
    exit()

while True:
    command = input("userMessage/groupMessage/createGroup/joinGroup/leaveGroup/addUserToGroup ")
    if command == "userMessage":
        toUser = input("user ")
        address = proxy.getUserAddress(toUser)
        port = proxy.getUserPort(toUser)
        if address == None or port == None:
            print("User not logged in, can't get info")
            continue
        msg = input("message ")
        msgToSend = username + " : " + msg
        sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sendSocket.connect((address, port))
        sendData(sendSocket, msgToSend)
    elif command == "groupMessage":
        toGroup = input("group ")
        msg = input("message ")
        msgToSend = username + " in " + toGroup + " : " + msg
        usersToSend = proxy.getGroupUsers(username, toGroup)
        for user in usersToSend:
            address = user.address
            port = user.port
            if address == None or port == None:
                print("User not logged in, can't get info")
                continue
            sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sendSocket.connect((address, port))
            sendData(sendSocket, msgToSend)
    elif command == "createGroup":
        groupName = input("groupname ")
        print(proxy.createGroup(groupName))
    elif command == "joinGroup":
        groupName = input("groupname ")
        print(proxy.joinGroup(username, groupName))
    elif command == "leaveGroup":
        groupName = input("groupname ")
        print(proxy.leaveGroup(username, groupName))
    elif command == "addUserToGroup":
        groupName = input("groupname ")
        userToAdd = input("userToAdd ")
        print(proxy.addUserToGroup(username, groupName, userToAdd))
    else:
        print("invalid command")