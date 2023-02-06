import socket, threading

MAX = 65535

def hear(sl):
    while True:
        data, address = sl.recvfrom(MAX)
        print("Got message: " + data.decode())

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sl = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sl.bind(('localhost', 0))

command = input("register/login ")
najaven = False
currentUser = ""

if command == "register":
    username = input("username ")
    password = input("password ")
    selectedRole = input("vraboten/korisnik ")
    data = "register|" + username + "|" + password + "|" + selectedRole + "|" + sl.getsockname()[0] + "|" + str(sl.getsockname()[1])
    s.sendto(data.encode(), ('127.0.0.1', 1061))
    data, address = s.recvfrom(MAX)
    if data.decode() == "ok":
        najaven = True
        currentUser = username

elif command == "login":
    username = input("username ")
    password = input("password ")
    data = "login|" + username + "|" + password + "|" + sl.getsockname()[0] + "|" + str(sl.getsockname()[1])
    s.sendto(data.encode(), ('127.0.0.1', 1061))
    data, address = s.recvfrom(MAX)
    data = data.decode().split('|')
    if data[0] == "ok":
        najaven = True
        currentUser = username

if not najaven:
    print("login fail")
    exit()

threading.Thread(target = hear, args=(sl,)).start()

while True:
    user = input("To user: ")
    msg = input("Enter message: ")
    toSend = "message|" + user + "|" + msg + "|" + currentUser
    s.sendto(toSend.encode(), ('127.0.0.1', 1061))



