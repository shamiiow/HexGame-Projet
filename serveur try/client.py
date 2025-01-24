import socket
import threading

# Paramètres du client
HOST = '127.0.0.1'  # Adresse locale (le serveur doit être sur la même machine)
PORT = 65432        # Le même port que celui du serveur
client_id = None    # ID du client, initialisé plus tard

# Envoyer des données (position) au serveur
def send_position(client_socket):
    while True:
        x = input("Entrez la position X du joueur : ")
        y = input("Entrez la position Y du joueur : ")
        message = f"{x},{y}"
        client_socket.sendall(message.encode())

# Recevoir des données du serveur (y compris l'ID initial)
def receive_data(client_socket):
    global client_id
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode()

            # Si on reçoit un message d'ID, on l'assigne au client
            if message.startswith("ID:"):
                client_id = message.split(":")[1]
                print(f"Votre identifiant est : {client_id}")
            else:
                print(f"Message reçu : {message}")
        except ConnectionResetError:
            break

# Démarrer le client
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Créer deux threads : un pour envoyer la position, un pour recevoir les données
    send_thread = threading.Thread(target=send_position, args=(client_socket,))
    receive_thread = threading.Thread(target=receive_data, args=(client_socket,))

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

if __name__ == "__main__":
    start_client()
