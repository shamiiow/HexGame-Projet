import random
import socket
import string
import sys
from _thread import *

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
    if data[0] == "Disconnect":
        return reply_disconnect(data)
    if data[0] == "Menudefault":
        return reply_Menudefault()
    if data[0] == "Menucreate":
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

def reply_disconnect(conn):
    print(f"Player {saveID[conn]} disconnected"*50)
    
    #delete the room and gril relate to the player
    for room in list_of_rooms:
        if saveID[conn] in room:
            room.remove(saveID[conn])
            if len(room) == 0:
                list_of_rooms.remove(room)
                print(f"!Room {room[0][0]} is empty and has been removed")
                
    #delete the id from saveID
    for key in saveID.keys():
        if saveID[key] == conn[2]:
            del saveID[key]
            print(f"ID {conn[2]} deleted from saveID")
    
    

def reply_inGameDefault(data):
    if data[2] not in dico_grid:
        dico_grid[data[2]] = [[[0 for _ in range(7)] for _ in range(7)], data[3]]
    if data[4] == "-2;-2" :
        return f"InGameDefault%{dico_grid[data[2]][0]}"
    else:
        coord = data[4].split(";")
        x, y = int(coord[0]), int(coord[1])
        if dico_grid[data[2]][0][x][y] == 0:
            if is_it_your_turn(data):
                dico_grid[data[2]][0][x][y] = what_color_are_you(data)
    return f"InGameDefault%{dico_grid[data[2]][0]}"

def is_it_your_turn(data):
    for i in range(len(list_of_rooms)):
        if list_of_rooms[i][0][0] == data[2]:
            if dico_grid[data[2]][1] == data[3]:
                dico_grid[data[2]][1] = the_other_player(data)
                return True
            else:
                return False
    return False

def the_other_player(data):
    for i in range(len(list_of_rooms)):
        if list_of_rooms[i][0][0] == data[2]:
            if list_of_rooms[i][1] == data[3]:
                return list_of_rooms[i][2]
            else:
                return list_of_rooms[i][1]
    return None

def what_color_are_you(data): 
    for i in range(len(list_of_rooms)):
        if list_of_rooms[i][0][0] == data[2]:
            if list_of_rooms[i][1] == data[3]:
                return 1
            else :
                return 2  
    return 2 

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
        if len(list_of_rooms[i]) == 2 and list_of_rooms[i][0][0] not in dico_grid.keys():
            message += f"{list_of_rooms[i][0][0]}|"
    return message

def reply_create(data):
    name_room = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
    list_of_rooms.append([[name_room, 7], saveID[data[1]]])
    return f"Menucreate%{name_room}"

def reply_join(data):
    for i in range(len(list_of_rooms)):
        if len(list_of_rooms[i]) == 2:
            if list_of_rooms[i][0][0] == data[2]:
                list_of_rooms[i].append(saveID[data[1]])
                return f"Menujoin%{list_of_rooms[i][0][0]}"
            
def reply_Waitingdefault(data):
    for i in range(len(list_of_rooms)):
        if list_of_rooms[i][0][0] == data[2]:
            if len(list_of_rooms[i]) == 2:
                return f"Waitingdefault%{list_of_rooms[i]}"
            if len(list_of_rooms[i]) == 3:
                return f"GoToGame%{data[2]}"
    
def remove_player_from_rooms(conn):
    for room in list_of_rooms:
        if saveID[conn] in room:
            print(f"!Removing {saveID[conn]} from room {room[0][0]}")
            room.remove(saveID[conn])
            if len(room) == 1:
                list_of_rooms.remove(room)
                print(f"!Room {room[0][0]} is empty and has been removed")



def send_to_client(conn, message):
    try:
        conn.sendall(str.encode(message))
    except Exception as e:
        pass

def print_info(data, conn, reply):
    print("--------------------------Information Brute Trade------------------------------------")
    print(f"data: {data}")
    print(f"reply: {reply}")
    print("--------------------------Information Generales Serveur------------------------------")
    
    print("List of players :")
    for key, value in saveID.items():
        print(f"    -{str(str(key.getpeername()[0])+":"+str(key.getpeername()[1]))} : {value}")
    print("List of rooms :")
    for i in range(len(list_of_rooms), 0, -1):
        print(f"    -Room {i}: {list_of_rooms[i-1]}")
    print("List of grid :")
    for key, value in dico_grid.items():
        print(f"    -{key} : player turn {value[1]}")
        for i in range(len(value[0])):
            print(f"                            {value[0][i]}")

    print("--------------------------Fin Information Generales Serveur--------------------------")   

def threaded_client(conn, player):
    conn.send(str.encode(str(player)))
    while True:
        try:
            print("-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-Start the loop-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-")
            data = conn.recv(2048).decode()
            if not data:
                break
            
            reply = str(find_reply(data, conn))
            print_info(data, conn, reply)

            conn.sendall(str.encode(reply))

            print("-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-End the loop-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-")

        except Exception as e:
            print(f"[Server Side] : An error occurred: {e}")
            remove_player_from_rooms(conn)
            conn.close()
            del saveID[conn]
            clients.remove(conn)
            break
            

    #print("Lost connection")
    

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