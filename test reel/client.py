from network import Network


class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.x = int(input("Position X: "))
        self.y = int(input("Position Y: "))


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def main():
    run = True
    
    startPos = (50, 50)
    p = Player(startPos[0], startPos[1])
    p2 = Player(0, 0)

    prev_pos = (p.x, p.y)

    while run:
        current_pos = (p.x, p.y)

        p.move()
        current_pos = (p.x, p.y)
        if current_pos != prev_pos:
            p2Pos = read_pos(n.send(make_pos(current_pos)))
            p2.x = p2Pos[0]
            p2.y = p2Pos[1]
            prev_pos = current_pos
            print(f"Player 1 position: {p.x, p.y}")
            print(f"Player 2 position: {p2.x, p2.y}")

n = Network()
main()