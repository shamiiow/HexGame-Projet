import socket
from _thread import *
import sys
import random
import string

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

def find_reply(data, conn):
    data = data.split("%")
    data.insert(1, conn)
    if data[0] == "Menudefault":
        return reply_default()
    if data[0] == "Menucreate":
        return reply_create(data)
    if data[0] == "Menujoin":
        return reply_join(data)
    return data

def reply_default():
    message = 'Menudefault%'
    for i in range(len(list_of_rooms)):
        if len(list_of_rooms[i]) == 2:
            message += f"{list_of_rooms[i][0]}|"
    print(f"Message to send: {message}")
    return message

def  reply_create(data):
    name_room = ''.join(random.choices(string.ascii_lowercase + string.digits, k=50))
    print(f"Room created: {name_room}")
    list_of_rooms.append([name_room, data[1]])
    return f"Menucreate%{name_room}"

def reply_join(data):
    for i in range(len(list_of_rooms)):
        if len(list_of_rooms[i]) == 2:
            if list_of_rooms[i][0] == data[2]:
                list_of_rooms[i].append(data[1])
                return f"Menujoin%{list_of_rooms[i][0]}"
    
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


def threaded_client(conn, player):
    conn.send(str.encode(str(player)))
    while True:
        try:
            data = conn.recv(2048).decode()
            if not data:
                break
            
            reply = str(find_reply(data, conn))
            print(f"Received from client {conn}: {data}")
            print(f"Sending to client: {reply}")

            conn.sendall(str.encode(reply))

            print("-------------------")
            print(f"List of rooms: ")
            for room in list_of_rooms:
                print(room)
            print("-------------------")

        except Exception as e:
            print(f"[Server Side] : An error occurred: {e}")
            break

    print("Lost connection")
    remove_player_from_rooms(conn)
    conn.close()
    clients.remove(conn)

list_of_rooms = []
clients = []
currentPlayer = 0
while True:
    conn, addr = s.accept()
    print(f"Connected to: {addr}")
    clients.append(conn)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1