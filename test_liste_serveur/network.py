import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "176.169.236.42"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            print("Connected to server")
            return self.client.recv(2048).decode()
        except Exception as e:
            print(f"Connection error: {e}")
        
    def disconnect(self):
        self.client.close()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            response = self.client.recv(2048).decode()
            return response
        except socket.error as e:
            print(f"[Network Side] : Send/receive error: {e}")
            return ""