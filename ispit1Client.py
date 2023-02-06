import socket, threading

MAX = 65535


def hear(sl):
    while True:
        data, address = sl.recvfrom(MAX)
        print("Got message: " + data.decode())

        
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sl = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sl.bind(('localhost', 0))

command = input("Type register to register ")

if command == "register":
    username = input("username ")
    password = input("password ")
    status = input("status ")
    if status == "vraboten":
        rabotodavec = input("rabotodavec ")
    else:
        rabotodavec = "none"
    data = "register|" + username + "|" + password + "|" + status + "|" + rabotodavec
    s.sendto(data.encode(), ('127.0.0.1', 1061))
    
print("Logging in...\n")
username = input("username ")
password = input("password ")
data = "login|" + username + "|" + password + "|" + sl.getsockname()[0] + "|" + str(sl.getsockname()[1])
s.sendto(data.encode(), ('127.0.0.1', 1061))
data, address = s.recvfrom(MAX)
data = data.decode().split('|')
if data[0] != "ok":
    print("Neuspesno logiranje")
    quit()

threading.Thread(target = hear, args=(sl,)).start()

while True:
    toUser = input("To user: ")
    msg = input("Enter message: ")
    toSend = "message|" + toUser + "|" + msg + "|" + username
    s.sendto(toSend.encode(), ('127.0.0.1', 1061))
    data, address = s.recvfrom(MAX)
    data = data.decode()
    print(data)
    
