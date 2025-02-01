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

def threaded_client(conn, player):
    conn.send(str.encode((str(player))))
    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode()



            if not data:
                print("Disconnected")
                break
            
            reply = data + "\n"
            print("From : ", addr)
            print("Received: ", data)
            print("Sending : ", reply)
            print("--------------------")

            conn.sendall(str.encode(reply))
            for client in clients:
                if client != conn:
                    print(client)
                    client.send(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
clients = []
while True:
    conn, addr = s.accept()
    clients.append(conn)
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1