import socket, threading

class rabotodavec():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.address = ""
        self.port = -1
        self.vraboteni = set()
        
class klient():
    def __init__(self, username, password, rabotodavec):
        self.username = username
        self.password = password
        self.address = ""
        self.port = -1
        self.rabotodavec = rabotodavec

rabotodavci = {}
klienti = {}
MAX = 65535

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('localhost', 1061))

maxl = int(input("Vnesi Max dolzina na poraki "))

while True:
    data, _address = s.recvfrom(MAX)
    data = data.decode().split('|')
    command = data[0]
    if command == "register":
        username = data[1]
        if username in rabotodavci or username in klienti:
            s.sendto("error, korisnikot vekje postoi ".encode(), _address)
        password = data[2]
        status = data[3]
        employer = data[4]
        if status == "rabotodavec":
            rabotodavci[username] = rabotodavec(username, password)
            s.sendto("ok ".encode(), _address)
        else:
            if employer == "none":
                klienti[username] = klient(username, password, employer) # employer e "none" za nevraboteni
                s.sendto("ok ".encode(), _address)
            else:
                if employer not in rabotodavci:
                    s.sendto("error, rabotodavecot ne postoi ".encode(), _address)
                else:
                    rabotodavci[employer].vraboteni.add(username)
                    klienti[username] = klient(username, password, employer)

    elif command == "login":
        username = data[1]
        password = data[2]
        address = data[3]
        port = int(data[4])

        if username in klienti:
            if klienti[username].password == password:
                klienti[username].address = address
                klienti[username].port = port
                s.sendto("ok".encode(), _address)
            else:
                s.sendto("error".encode(), _address)

        elif username in rabotodavci:
            if rabotodavci[username].password == password:
                rabotodavci[username].address = address
                rabotodavci[username].port = port
                s.sendto("ok".encode(), _address)
            else:
                s.sendto("error".encode(), _address)

        else:
            s.sendto("error".encode(), _address)
    elif command == "message":
        toUserName = data[1]
        msg = data[2]
        fromUserName = data[3]
        msgLength = len(msg.encode())
        msgToSend = "Message from " + fromUserName + ":" + msg

        if msgLength > 64:
            s.sendto("Message too long...".encode(), _address)

        if toUserName not in klienti or toUserName not in rabotodavci:
            s.sendto("error, user doesn't exist ".encode(), _address)
        
        if toUserName in klienti:
            toUser = klienti[toUserName]
        elif toUserName in rabotodavci:
            toUser = rabotodavci[toUserName]
            
        if fromUserName in klienti:
            fromUser = klienti[toUserName]
        elif fromUserName in rabotodavci:
            fromUser = rabotodavci[toUserName]

        # megju klienti
        if toUserName in klienti and fromUserName in klienti:
            if klienti[fromUserName].rabotodavec == "none" or klienti[toUserName].rabotodavec == "none":
                s.sendto("Nemozhe prakjanje megju nevraboten i vraboten...".encode(), _address)
            
        # megju vraboten i employer
        if (toUserName in klienti and fromUserName in rabotodavci) or (toUserName in rabotodavci and fromUserName in klienti):
            if toUserName in klienti:
                if (klienti[toUserName].rabotodavec == "none"):
                    if msgLength > maxl:
                        s.sendto(("Pregolema poraka..., treba da e pod "+str(maxl)).encode(), _address)
                    else:
                        s.sendto("ok".encode(), _address)
                        s.sendto(msgToSend.encode(), (toUser.address, toUser.port))
                elif (klienti[toUserName].rabotodavec != fromUserName) or (toUserName in rabotodavci[fromUserName].vraboteni):
                    s.sendto("Nesoodveten vraboten...".encode(), _address)
                elif msgLength > 16:
                    s.sendto("Pregolema poraka, pomala od 16B treba da e megju vraboten i rabotodavec...".encode(), _address)
                else:
                    s.sendto("ok".encode(), _address)
                    s.sendto(msgToSend.encode(), (toUser.address, toUser.port))
                    
            elif toUserName in rabotodavci:
                if (klienti[fromUserName].rabotodavec == "none"):
                    if msgLength > maxl:
                        s.sendto(("Pregolema poraka..., treba da e pod "+str(maxl)).encode(), _address)
                    else:
                        s.sendto("ok".encode(), _address)
                        s.sendto(msgToSend.encode(), (toUser.address, toUser.port))
                elif (klienti[fromUserName].rabotodavec != toUserName) or (fromUserName in rabotodavci[toUserName].vraboteni):
                    s.sendto("Nesoodveten employer...".encode(), _address)
                elif msgLength > 16:
                    s.sendto("Pregolema poraka, pomala od 16B treba da e megju vraboten i rabotodavec...".encode(), _address)
                else:
                    s.sendto("ok".encode(), _address)
                    s.sendto(msgToSend.encode(), (toUser.address, toUser.port))

        if (toUserName in klienti and fromUserName in rabotodavci) or (toUserName in rabotodavci and fromUserName in klienti):
            s.sendto("Nemozhe prakjanje od vraboten na nevraboten i obratno...".encode(), _address)

    else:
        s.sendto("error".encode(), _address)


