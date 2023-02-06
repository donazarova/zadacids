import socket, threading, struct
from xmlrpc.server import SimpleXMLRPCServer

class user():
    def __init__(self, username, password, ime, prezime, telefon, email, godini, iskustvo, sektor):
        self.username = username
        self.password = password
        self.ime = ime
        self.prezime = prezime
        self.telefon = telefon
        self.email = email
        self.godini = godini
        self.iskustvo = iskustvo
        self.sektor = sektor
        self.address = ""
        self.port = -1
        self.loggedIn = 0

class group():
    def __init__(self):
        self.users = set()

users = {}
groups = { "senior" : group() }

def register(username, password, ime, prezime, telefon, email, godini, iskustvo, sektor):
    if username in users:
        return "Korisnikot vekje postoi"
    else:
        if sektor not in groups:
            groups[sektor] = group()
        users[username] = user(username, password, ime, prezime, telefon, email, godini, iskustvo, sektor)
        # odma se dodava vo grupa za sektorot
        groups[sektor].users.add(username)
        # odma se dodava vo grupa za seniori ako e senior
        if iskustvo == "senior":
            groups["senior"].users.add(username)
        return "Uspesno registriran"
    
def login(username, password, address, port) -> bool:
    if username not in users[username] or users[username].password != password:
        return False
    users[username].address = address
    users[username].port = port
    users[username].loggedIn = 1
    return True
    
def getUserAddress(searchedUser):
    if searchedUser not in users or users[searchedUser].loggedIn == 0:
        return None
    return users[searchedUser].address
    
def getUserPort(searchedUser):
    if searchedUser not in users or users[searchedUser].loggedIn == 0:
        return None
    return users[searchedUser].port
    
def createGroup(groupName):
    if groupName not in groups:
        groups[groupName] = group()
    return "Success"
        
def joinGroup(username, groupName):
    if groupName not in groups:
        return "Group doesn't exist"
    success = True
    for user in groups[groupName].users:
        if user.iskustvo != users[username].iskustvo:
            success = False
    if success == True:
        groups[groupName].users.add(username)
        return "Success"
    else:
        return "Iskustvoto ne e tocno"
        
def leaveGroup(username, groupName):
    if groupName not in groups:
        return "Group doesn't exist"
    if username in groups[groupName].users:
        groups[groupName].users.remove(username)
    return "Success"
        
def addUserToGroup(username, groupName, userToAdd):
    if groupName not in groups:
        return "Group doesn't exist"
    if username in groups[groupName].users:
        if users[userToAdd].iskustvo == users[username].iskustvo:
            groups[groupName].users.add(userToAdd)
            return "Success"
        else:
            return "Razlicno iskustvo"
    return "Ne si vo grupata za da go dodadesh"

# ovaa funkcija ke vrakja user info za da mozhe da se povrzeme so nivnata adresa i porta
def getGroupUsers(fromUser, groupName):
    if fromUser not in groups[groupName].users:
        return "Ne pripagjas vo ovaa grupa"
    usersToReturn = []
    for username in groups[groupName].users:
        user = users[username]
        if user.username == fromUser or user.loggedIn == 0:
            continue
        usersToReturn.append(user)
    return usersToReturn

server = SimpleXMLRPCServer(('127.0.0.1', 7001))
server.register_introspection_functions()
server.register_multicall_functions()
server.register_function(register)
server.register_function(login)
server.register_function(getUserAddress)
server.register_function(getUserPort)
server.register_function(createGroup)
server.register_function(joinGroup)
server.register_function(leaveGroup)
server.register_function(addUserToGroup)
server.register_function(getGroupUsers)
server.serve_forever()