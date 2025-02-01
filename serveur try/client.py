import pygame
from network import Network

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def redrawWindow(win, player, player2):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    startPos = read_pos(n.getPos())
    p = Player(startPos[0], startPos[1], 100, 100, (0, 255, 0))
    p2 = Player(0, 0, 100, 100, (255, 0, 0))
    clock = pygame.time.Clock()

    prev_pos = (p.x, p.y)

    while run:
        clock.tick(60)
        current_pos = (p.x, p.y)
        
        if current_pos != prev_pos:
            p2Pos = read_pos(n.send(make_pos(current_pos)))
            p2.x = p2Pos[0]
            p2.y = p2Pos[1]
            p2.update()
            prev_pos = current_pos

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        current_pos = (p.x, p.y)
        if current_pos != prev_pos:
            p2Pos = read_pos(n.send(make_pos(current_pos)))
            p2.x = p2Pos[0]
            p2.y = p2Pos[1]
            p2.update()
            prev_pos = current_pos
            print(f"Player 1 position: {p.x, p.y}")
            print(f"Player 2 position: {p2.x, p2.y}")

        redrawWindow(win, p, p2)

main()