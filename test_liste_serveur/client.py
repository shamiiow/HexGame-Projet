from network import Network


def create_room():
    return "Menucreate%"

def join_room(id):
    return "Menujoin%"+id

def default():
    return "Menudefault%"

n = Network()
while True:
    try:
        message = input("----------Envoie d'un message------------\nNouveau serveur      : 1\nRejoindre un serveur : 2\nNe rien faire        : 3\nEnter a number : ")
        if message == "1":
            message = create_room()
        elif message[0] == "2":
            message = join_room(message[1:])
        elif message == "3":
            message = default()
        print("----------Info------------")
        print(f"Sending message: {message}")
        response = n.send(message)
        print(f"Server response: {response}")


    except Exception as e:
        print(f"[Client Side] : An error occurred: {e}")


