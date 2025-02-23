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
        print(grid[i])
    print()


def nice_data(data):
    if data == 'Connected':
        return '-1'


    data = data.split(",")
    data2 = list(data)
    data = [int(i) for i in data[:-1]]
    data.append(int(data2[-1]))

    return data

def threaded_client(conn, player):
    global player_turn, player_1, player_2, currentPlayer
    conn.send(str.encode((str(player))))
    reply = ""
    while True:
        try:
        
            data = conn.recv(2048).decode()

            if not data:
                print("Disconnected")
                break
            
            print("-*-*-*-*-*-*-*-*-*-Message from user-*-*-*-*-*-*-*-*-*-")
            print('Contenu :\n' + str(data))
            print('----------Fin du message recu----------')
            
            id = None

            data = nice_data(data)
            
            if data != '-1' and currentPlayer == 2 and type(data) == list:
                id = data[2]
                print("----------Gestion de la partie----------")
                #print(id, player_1, player_2, player_turn, data)
                print('id : ' + str(id)+ ' type : ' + str(type(id))+'\nplayer_1 : ' + str(player_1)+ ' type : ' + str(type(player_1))+'\nplayer_2 : ' + str(player_2)+ ' type : ' + str(type(player_2))+'\nplayer_turn : ' + str(player_turn)+ ' type : ' + str(type(player_turn))+'\ndata : ' + str(data)+ ' type : ' + str(type(data)))
                #print(type(id), type(player_1), type(player_2), type(player_turn), data[:2])
                #print(id == player_1 == player_turn)
                if id == player_1 == player_turn:
                    grid_global[data[0]-1][data[1]-1] = 1
                    player_turn = player_2
                    print(f"Le joueur {player_1} a joué en {data[0], data[1]} au tour du joueur {player_2}")
                if id == player_2 == player_turn:
                    grid_global[data[0]-1][data[1]-1] = 2
                    player_turn = player_1
                    print(f"Le joueur {player_2} a joué en {data[0], data[1]} au tour du joueur {player_1}")
                print("\nGrid :")
                display(grid_global)
                print("----------Fin de la gestion de la partie----------")
                reply = str(grid_global).replace("],", "],\n").replace("[[", " [").replace("]]", "]")
                reply = '@'+reply

            if data == '-1':
                if not(player_1) :
                    reply = '69'
                    player_1 = 69
                elif not(player_2):
                    reply = '420'
                    player_2 = 420



            

            print("Message envoye :\n" + str(reply))
            print("----------Fin du message envoye----------") 
            print("-*-*-*-*-*-*-*-*-*-Fin-*-*-*-*-*-*-*-*-*-")   



            #conn.sendall(str.encode(reply))
            for client in clients:
                #print(client)
                client.send(str.encode(reply))
        except Exception as e:
            print('Error : ' + str(e))
            break

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