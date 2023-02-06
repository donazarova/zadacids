import socket, threading, struct
from xmlrpc.server import SimpleXMLRPCServer

class user():
    def __init__(self, username, password, selectedRole, info, address, port, loggedIn):
        self.username = username
        self.password = password
        self.selectedRole = selectedRole
        self.info = info
        self.address = address
        self.port = port
        self.loggedIn = loggedIn

class group():
    def __init__(self, name):
        self.name = name

users = {}
groups = {}

def register(username, password, selectedRole, info, address, port):
    if info not in groups:
        return "Grupata ne postoi "
    if username not in users[username]:
        users[username] = user(username, password, selectedRole, info, address, port, 0)
        return "Uspesno registriran"
    return "Korisnikot vekje postoi"
    
def login(username, password, address, port) -> bool:
    if username not in users[username] or users[username].password != password:
        return False
    users[username].address = address
    users[username].port = port
    users[username].loggedIn = 1
    return True

def logout(username, password):
    if username not in users[username] or users[username].password != password:
        return False
    users[username].loggedIn = 0
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
        groups[groupName] = group(groupName)
        
def getGroupUsers(fromUser, groupName):
    if fromUser not in users or users[fromUser].info != groupName:
        return "Nevalidna grupa"
    usersToReturn = []
    if groupName in groups:
        for user in users:
            if user.username == fromUser or user.loggedIn == 0:
                continue
            if user.info == groupName:
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
server.register_function(getGroupUsers)
server.serve_forever()