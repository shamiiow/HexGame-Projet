import socket
from _thread import *
import sys
import random
import string

server = ""
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
saveID = {}


try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

def generate_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

def find_reply(data, conn):
    data = data.split("%")
    data.insert(1, conn)
    if data[0] == "Menudefault":
        return reply_Menudefault()
    if data[0] == "Menucreate":
        print("caca"*100)
        return reply_create(data)
    if data[0] == "Menujoin":
        return reply_join(data)
    if data[0] == "Waitingdefault":
        return reply_Waitingdefault(data)
    if data[0] == "AskAttribId":
        return reply_askAttribId(conn)
    if data[0] == "iKnowMyId":
        return reply_iKnowMyId(data)
    if data[0] == "InGameDefault":
        return reply_inGameDefault(data)
    return data

def reply_inGameDefault(data):
    if data[2] not in dico_grid:
        print(f"Creating grid for {data[2]}")
        dico_grid[data[2]] = [[0 for _ in range(7)] for _ in range(6)]
    if data[3] == "-1;-1" :
        return f"InGameDefault%{dico_grid[data[2]]}"
         
    return f"InGameDefault%{dico_grid[data[2]]}"
            

def reply_iKnowMyId(data):
    saveID[data[1]] = data[2]
    return reply_Menudefault()

def reply_askAttribId(conn):
    id = generate_id()
    saveID[conn] = id
    return id

def reply_Menudefault():
    message = 'Menudefault%'
    for i in range(len(list_of_rooms)):
        if len(list_of_rooms[i]) == 2:
            message += f"{list_of_rooms[i][0]}|"
    print(f"Message to send: {message}")
    return message

def reply_create(data):
    name_room = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
    print(f"Room created: {name_room}")
    list_of_rooms.append([name_room, saveID[data[1]]])
    print("caca"*100)
    return f"Menucreate%{name_room}"

def reply_join(data):
    for i in range(len(list_of_rooms)):
        if len(list_of_rooms[i]) == 2:
            if list_of_rooms[i][0] == data[2]:
                list_of_rooms[i].append(saveID[data[1]])
                return f"Menujoin%{list_of_rooms[i][0]}"
            
def reply_Waitingdefault(data):
    print(f"Data: {data}")
    for i in range(len(list_of_rooms)):
        if list_of_rooms[i][0] == data[2]:
            if len(list_of_rooms[i]) == 2:
                return f"Waitingdefault%{list_of_rooms[i]}"
            if len(list_of_rooms[i]) == 3:
                return f"GoToGame%{data[2]}"
    
def remove_player_from_rooms(conn):
    for room in list_of_rooms:
        if conn in room:
            room.remove(conn)
            print(f"Removed {conn} from room {room[0]}")

def send_to_client(conn, message):
    try:
        conn.sendall(str.encode(message))
    except Exception as e:
        print(f"Send to client error: {e}")

def print_info(data, conn, reply):
    print("-------------Trade info-------------")
    print(f"data: {data}")
    print(f"reply: {reply}")
    print("-------------Information-------------")
    
    print("List of players :")
    for key, value in saveID.items():
        print(f"{key}: {value}")
    print("List of rooms :")
    for i in range(len(list_of_rooms)):
        print(f"Room {i}: {list_of_rooms[i]}")
    print("List of grid :")
    for key, value in dico_grid.items():
        print(f"{key}: {value}")
    print("---------------Fin------------------")   

def threaded_client(conn, player):
    conn.send(str.encode(str(player)))
    while True:
        #try:
            data = conn.recv(2048).decode()
            if not data:
                break
            
            reply = str(find_reply(data, conn))
            print_info(data, conn, reply)

            conn.sendall(str.encode(reply))

            #print("-------------------")
            #print(f"List of rooms: ")
            for room in list_of_rooms:
                pass#print(room)
            #print("-------------------")

        #except Exception as e:
            #print(f"[Server Side] : An error occurred: {e}")
            #break

    print("Lost connection")
    remove_player_from_rooms(conn)
    conn.close()
    del saveID[conn]
    clients.remove(conn)

dico_grid = {}
list_of_rooms = []
clients = []
currentPlayer = 0
while True:
    conn, addr = s.accept()
    print(f"Connected to: {addr}")
    clients.append(conn)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1