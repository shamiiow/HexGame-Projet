import socket
import threading

# Paramètres du serveur
HOST = ''  # Adresse locale
PORT = 65432        # Port d'écoute

# Liste des connexions clients
clients = {}
client_id_counter = 1  # Compteur pour générer des identifiants uniques

# Diffuser les messages à tous les clients sauf à l'envoyeur
def broadcast(message, client_socket):
    for c in clients.values():
        if c != client_socket:
            c.sendall(message)

# Gérer chaque connexion client
def handle_client(client_socket, client_id):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            # Prendre la position reçue et la renvoyer aux autres clients avec l'ID du joueur
            print(f"Reçu du client {client_id} : {data.decode()}")
            broadcast(f"Joueur {client_id} : {data.decode()}".encode(), client_socket)
        except ConnectionResetError:
            break

    # Si le client se déconnecte, fermer la connexion
    print(f"Client {client_id} déconnecté")
    del clients[client_id]
    client_socket.close()

# Démarrer le serveur
def start_server():
    global client_id_counter
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Serveur en écoute sur {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connexion de {client_address}")
        
        # Assigner un identifiant unique au client
        client_id = client_id_counter
        clients[client_id] = client_socket
        client_id_counter += 1

        # Envoyer l'ID au client
        client_socket.sendall(f"ID:{client_id}".encode())

        # Créer un thread pour gérer chaque client séparément
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
        client_thread.start()

if __name__ == "__main__":
    start_server()
