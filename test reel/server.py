import socket
from _thread import *
import sys

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(0)
print("Waiting for a connection, Server Started")

def display(grid):
    for i in range(7):
        for j in range(7):
            print(grid[i][j], end = " ")
        print()
    print()

def nice_data(data):
    if data == 'Connected' :
        return '-1'
    data = data.split(",")
    data2 = list(data)
    data = [int(i) for i in data[:-1]]

    if data2[-1] == "True":
        data.append(True)
    else:
        data.append(False)
    return data

def threaded_client(conn, player):
    global player_turn, player_1, player_2
    conn.send(str.encode((str(player))))
    reply = ""
    while True:
        
        data = conn.recv(2048).decode()

        if not data:
            print("Disconnected")
            break
        
        reply = data + "\n"
        print("From : ", addr)
        print("Received: ", data)
        

        data = nice_data(data)
        
        if data != '-1':
            id = data[2]
            print("---------------------")
            print(id, player_1, player_2, player_turn, data[:2])
            print(type(id), type(player_1), type(player_2), type(player_turn), data[:2])
            print(id == player_1 == player_turn)
            if id == player_1 == player_turn:
                grid_global[data[0]-1][data[1]-1] = 1
                player_turn = player_2
            if id == player_2 == player_turn:
                grid_global[data[0]-1][data[1]-1] = 2
                player_turn = player_1
            display(grid_global)

        if data == '-1':
            if not(player_1) :
                reply = '69'
                player_1 = 69
            elif not(player_2):
                reply = '420'
                player_2 = 420

        print("Sending : ", reply)
        print("--------------------")    

        conn.sendall(str.encode(reply))
        '''for client in clients:
            if client != conn:
                #print(client)
                client.send(str.encode(reply))'''
        

    print("Lost connection")
    conn.close()

currentPlayer = 0
clients = []
grid_global = [[0 for _ in range(9)] for _ in range(9)]
player_1 = False
player_2 = False



while True:
    conn, addr = s.accept()
    clients.append(conn)
    print("Connected to:", addr)
    player_turn = 69
        

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1