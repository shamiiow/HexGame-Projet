from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Line, Rectangle, Triangle
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from math import cos, sin, pi, sqrt
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from botIA import ask_bot1
import numpy as np
import random
import time

from kivy.clock import Clock
from network import Network


class GameScreen(Screen):
    def __init__(self, **kwargs):
        self.recap = []
        self.winner = 0
        self.widgets = []
        self.poss_pos = []
        self.hex_size = 25
        self.player = False
        self.turn_on = False
        self.longeur = 177013
        self.list_robot = ["dumb"]
        self.player1_name = "shamiiow"
        self.player2_name = "enwatibateau"
        self.type_robot = self.list_robot[0]
        self.couleur = ["white", "blue", "red"]
        self.text_color = (176 / 255, 97 / 255, 97 / 255)
        self.fpsServer = 1 / 60
        print(Window.size[0])

        # Creation du Grid

        super(GameScreen, self).__init__(**kwargs)

        self.GridGlobal = BoxLayout(orientation="vertical")

        # Creation des SousGrid

        self.header = GridLayout(
            rows=1, cols=3, size_hint_y=None, height=75, padding=[0, 20, 0, 0]
        )
        self.game_hex = Widget(size_hint_y=2)
        self.footer = GridLayout(
            rows=2,
            cols=2,
            size_hint_y=None,
            height=50 * (Window.size[0] / Window.size[1]),
        )

        # Creation des Widget

        self.player1_label = Label(
            text="Name player1",
            color=(176 / 255, 97 / 255, 97 / 255),
            font_size=30,
            bold=True,
        )  # Index 0
        self.turn_label = Label(
            text=self.player1_name + " commence !",
            color=(176 / 255, 97 / 255, 97 / 255),
            font_size=20,
            bold=True,
        )  # Index 1
        self.player2_label = Label(
            text="Name player2",
            color=(176 / 255, 97 / 255, 97 / 255),
            font_size=30,
            bold=True,
        )  # Index 2
        self.player1_last_play_label = Label(
            text="List of last play for player 1",
            color=(176 / 255, 97 / 255, 97 / 255),
            font_size=50,
        )  # Index 3
        self.player2_last_play_label = Label(
            text="List of last play for player 2",
            color=(176 / 255, 97 / 255, 97 / 255),
            font_size=50,
        )  # Index 4
        self.cancel_button = Button(
            text="Cancel last play",
            color=(0.9, 0.9, 0.9),
            font_size=40,
            background_color=(28 / 255, 65 / 255, 91 / 255),
            bold=True,
        )  # Index 5
        self.home_button = Button(
            text="Back home",
            color=(0.9, 0.9, 0.9),
            font_size=40,
            background_color=(28 / 255, 65 / 255, 91 / 255),
            bold=True,
        )  # Index 6

        # Association des commande

        self.home_button.bind(on_press=self.go_to_home)
        self.cancel_button.bind(on_press=self.cancel_last_play)
        Window.bind(on_resize=self.on_window_resize)

        # Ajout des Widget aux SousGrid

        self.header.add_widget(self.player1_label)
        self.header.add_widget(self.turn_label)
        self.header.add_widget(self.player2_label)

        # self.footer.add_widget(self.player1_last_play_label)
        # self.footer.add_widget(self.player2_last_play_label)
        self.footer.add_widget(self.cancel_button)
        self.footer.add_widget(self.home_button)

        # Ajout des SousGrid au GridGlobal

        self.GridGlobal.add_widget(self.header)
        self.GridGlobal.add_widget(self.game_hex)
        self.GridGlobal.add_widget(self.footer)

        self.add_widget(self.GridGlobal)

        self.widgets.extend(
            [
                self.player1_label,
                self.turn_label,
                self.player2_label,
                self.player1_last_play_label,
                self.player2_last_play_label,
                self.cancel_button,
                self.home_button,
            ]
        )

    def on_window_resize(self, window, width, height):
        if self.turn_on:
            self.update()

    def on_touch_down(self, touch):

        poss_mouse = self.is_in_who(touch.pos)
        if (
            (self.cancel_button.collide_point(*touch.pos))
            or (self.home_button.collide_point(*touch.pos))
            or (poss_mouse == None)
        ):
            self.update()
            return super(GameScreen, self).on_touch_down(touch)

        c = [poss_mouse[0] + 1, poss_mouse[1] + 1]

        if self.winner != 0 or self.grid_p[c[0]][c[1]] != 0:
            self.update()
            return
        self.base = c

        self.play(c)

    def play(self, c):
        if self.winner != 0 or self.grid_p[c[0]][c[1]] != 0:
            return
        self.grid_w = [[0 for _ in range(self.longeur)] for _ in range(self.longeur)]
        # self.grid_p[c[0]][c[1]] = 1 + int(self.player)
        self.recap.append(c)
        self.win()
        self.player = self.player ^ True

    def play_yummi(self):
        if self.winner != 0:
            self.update()
            return
        save_time = time.time()
        if self.type_robot == "dumb":
            self.poss_pos = []
            for i in range(1, self.longeur - 1):
                for j in range(1, self.longeur - 1):
                    if self.grid_p[i][j] == 0:
                        self.poss_pos.append((i, j))
            coord = random.choice(self.poss_pos)
        return coord

    def path(self, c, p):
        x, y = c[0], c[1]
        if self.grid_p[x][y] != p:
            return
        self.grid_w[x][y] = 1
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if [i, j] != [0, 0] and [i, j] != [-1, -1] and [i, j] != [1, 1]:
                    if (
                        self.grid_p[x + i][y + j] == p
                        and self.grid_w[x + i][y + j] == 0
                    ):
                        self.grid_w[x + i][y + j] = 1
                        self.path((x + i, y + j), p)
        if (1 in self.grid_w[self.longeur - 2] and p == 1) or (
            1 in [self.grid_w[i][self.longeur - 2] for i in range(self.longeur)]
            and p == 2
        ):
            self.winner = 1 + int(self.player)
            if self.winner == 1:
                self.turn_label.text = "Gagnant : " + str(self.player1_name)
            if self.winner == 2:
                self.turn_label.text = "Gagnant : " + str(self.player2_name)

    def win(self):
        self.grid_w = [[0 for _ in range(self.longeur)] for _ in range(self.longeur)]
        for i in range(1, self.longeur - 1):
            if self.winner == 0:
                self.path((1, i), 1)
        self.grid_w = [[0 for _ in range(self.longeur)] for _ in range(self.longeur)]
        for i in range(1, self.longeur - 1):
            if self.winner == 0:
                self.path((i, 1), 2)

    def is_in_who(self, moos_poss):
        for i in range(len(poss_hex)):
            for j in range(len(poss_hex[i])):
                distance = sqrt(
                    (moos_poss[0] - poss_hex[i][j][0]) ** 2
                    + (moos_poss[1] - poss_hex[i][j][1]) ** 2
                )
                if distance <= (self.hex_width) / 2:
                    return [i, j]

    def cancel_last_play(self, instance):
        if self.recap == []:
            return
        self.winner = 0
        self.grid_p[self.recap[-1][0]][self.recap[-1][1]] = 0
        self.recap.pop()
        self.player = self.player ^ True
        if self.player:
            self.turn_label.text = "Au tour de : " + str(self.player2_name)
        else:
            self.turn_label.text = "Au tour de : " + str(self.player1_name)
        self.update()

    def update(self):
        self.game_hex.canvas.before.clear()
        if self.winner == 1:
            self.turn_label.text = "Gagnant : " + str(self.player1_name)
        if self.winner == 2:
            self.turn_label.text = "Gagnant : " + str(self.player2_name)

        facteur = 2.5

        # resize les elements en fonction de la taill de la fenetre

        self.widgets[0].font_size = 30 * min(Window.size[0] / 800, Window.size[1] / 800)
        self.widgets[1].font_size = 20 * min(Window.size[0] / 800, Window.size[1] / 800)
        self.widgets[2].font_size = 30 * min(Window.size[0] / 800, Window.size[1] / 800)

        self.cancel_button.font_size = 40 * min(
            Window.size[0] / 800, Window.size[1] / 800
        )
        self.home_button.font_size = 40 * min(
            Window.size[0] / 800, Window.size[1] / 800
        )

        self.hex_size = min(
            (Window.size[0]) / (facteur * (self.coll + self.coll // 2)),
            ((Window.size[1]) / (facteur * self.coll)),
        )

        self.hex_width = cos(pi / 6) * 2 * self.hex_size
        self.hex_height = (cos(pi / 3) * self.hex_size + self.hex_size * 0.5) * 2

        if self.longeur % 2 != 0:
            self.center_x_grid = (
                Window.size[0] * 0.5
                - (self.coll + self.coll // 2 - 1) / 2 * self.hex_width
            )
            self.center_y_grid = Window.size[1] * 0.5 + (
                self.hex_height - cos(pi / 3) * self.hex_size
            ) * (self.coll // 2)
        if self.longeur % 2 == 0:
            self.center_x_grid = (
                Window.size[0] * 0.5
                - (0.75 + 1.5 * (self.coll / 2 - 1)) * self.hex_width
            )
            self.center_y_grid = (
                Window.size[1] * 0.5
                + ((cos(pi / 3) + 1) * self.hex_size * 0.5)
                + (self.hex_height - cos(pi / 3) * self.hex_size) * (self.coll / 2 - 1)
            )

        with self.game_hex.canvas.before:
            self.hex_grid = HexGrid(
                rows=self.coll,
                cols=self.coll,
                hex_size=self.hex_size,
                pos_x=self.center_x_grid,
                pos_y=self.center_y_grid,
                grid_p=self.grid_p,
                coll=self.coll,
            )

        self.header.height = min((Window.size[1]) / 12, 100000)
        self.footer.height = min((Window.size[1]) / 12, 100000)
        # self.affiche()

    def affiche(self):
        for i in range(1, self.longeur - 1):
            print(
                "  " * i
                + str(self.grid_p[i])
                + "   " * (self.longeur // 2)
                + str(self.grid_w[i])
                + "   " * (self.longeur // 2)
                + str(poss_hex[i - 1])
            )
        print(self.winner)

    def update_game_state(self, dt):
        try:
            print("------------------------Update-------------------------")
            send_data = str(self.base[0]) + "," + str(self.base[1]) + "," + str(self.id)
            print(send_data)
            self.data_recieve = self.network.send(send_data)
            self.data_recieve = self.format(self.data_recieve)
            print("Data recu :")
            for i in self.data_recieve:
                print(i)
            if type(self.data_recieve) == list:
                for i in range(1, self.longeur - 1):
                    for j in range(1, self.longeur - 1):
                        self.grid_p[i][j] = self.data_recieve[i - 1][j - 1]

            self.update()
            self.win()
            self.base = [-1, -1, self.id]

            print("------------------------Fin de l'update-------------------------")
        except Exception as e:
            print("Error : " + str(e))
            Clock.unschedule(self.gameUpdate)

    def format(self, texte):
        print(texte)
        print(type(texte))
        if "@" not in texte:
            return texte
        texte = texte.split("@")
        for i in range(1, len(texte)):
            print(texte[i])
            print(
                "---------------------------------------------------------------------"
            )
            if texte[i][-1] == "%":
                clean = texte[i][:-1]
        texte = clean
        texte = texte.split("\n")
        for i in range(len(texte)):
            texte[i] = (
                texte[i]
                .replace("[", "")
                .replace("]", "")
                .replace(",", "")
                .replace(" ", "")
            )
        new_grid = [
            [int(texte[i][j]) for j in range(len(texte[i]))] for i in range(len(texte))
        ]
        return new_grid

    def set_variables(
        self, player1_name, player2_name, p1_checkbox, p2_checkbox, longUeur
    ):
        global poss_hex

        self.network = Network()
        self.id = self.network.send("Connected")

        print(self.id)

        self.base = [-1, -1, self.id]
        self.gameUpdate = Clock.schedule_interval(
            self.update_game_state, self.fpsServer
        )
        self.turn_on = True
        self.longUeur = max(2, longUeur)
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.widgets[0].text = player1_name
        self.widgets[2].text = player2_name
        self.turn_label.text = self.player1_name + " commence !"
        self.p1_type = p1_checkbox
        self.p2_type = p2_checkbox
        self.longeur = self.longUeur + 2
        self.coll = self.longeur - 2
        self.height_total = self.hex_size * self.coll + (self.hex_size + 1) * (0.15)

        self.hex_size = min(
            (Window.size[0]) / (2 * (self.coll + self.coll // 2)),
            ((Window.size[1]) / (2 * self.coll)),
        )

        self.hex_width = cos(pi / 6) * 2 * self.hex_size
        self.hex_height = (cos(pi / 3) * self.hex_size + self.hex_size * 0.5) * 2
        self.grid_p = [[0 for _ in range(self.longeur)] for _ in range(self.longeur)]
        self.grid_w = [[0 for _ in range(self.longeur)] for _ in range(self.longeur)]
        poss_hex = [
            [0 for _ in range(self.longeur - 2)] for _ in range(self.longeur - 2)
        ]

        # definir le centre de la grille d'hexagone
        if self.longeur % 2 != 0:
            self.center_x_grid = (
                Window.size[0] * 0.5
                - (self.coll + self.coll // 2 - 1) / 2 * self.hex_width
            )
            self.center_y_grid = Window.size[1] * 0.5 + (
                self.hex_height - cos(pi / 3) * self.hex_size
            ) * (self.coll // 2)
        if self.longeur % 2 == 0:
            self.center_x_grid = (
                Window.size[0] * 0.5
                - (0.75 + 1.5 * (self.coll / 2 - 1)) * self.hex_width
            )
            self.center_y_grid = (
                Window.size[1] * 0.5
                + ((cos(pi / 3) + 1) * self.hex_size * 0.5)
                + (self.hex_height - cos(pi / 3) * self.hex_size) * (self.coll / 2 - 1)
            )

        if self.p2_type and self.p1_type:
            while self.winner == 0:
                self.play(self.play_yummi())

        elif self.p1_type:
            self.play(self.play_yummi())

        for i in range(self.longeur):
            for j in range(self.longeur):
                if (
                    (i == 0)
                    or (j == 0)
                    or (i == self.longeur - 1)
                    or (j == self.longeur - 1)
                ):
                    self.grid_p[i][j] = 9

        self.update()

    def go_to_home(self, instance):
        self.game_hex.canvas.before.clear()
        Clock.unschedule(self.gameUpdate)
        self.grid_p = [[0 for _ in range(self.longeur)] for _ in range(self.longeur)]
        self.recap == []
        self.player = False
        self.winner = 0
        self.manager.current = "home"


class Hexagon(Widget):
    def __init__(self, center_x, center_y, hex_size, row, col, grid_p, coll, **kwargs):
        super(Hexagon, self).__init__(**kwargs)
        self.row = row
        self.col = col
        self.grid_p = grid_p
        self.hex_size = hex_size
        self.center_x = center_x
        self.center_y = center_y
        self.hex_width = cos(pi / 6) * self.hex_size * 2
        self.coll = coll

        self.draw_hex()

    def draw_hex(self):
        with self.canvas:
            if self.grid_p[self.row + 1][self.col + 1] == 0:
                Color(0.8, 0.8, 0.8)
            if self.grid_p[self.row + 1][self.col + 1] == 1:
                Color(126 / 255, 215 / 255, 193 / 255)
                # Color(0,0,0.5)

            points = []
            for i in range(6):
                angle = pi / 2 + 2 * pi * i / 6
                points.extend(
                    [
                        self.center_x + self.hex_size * cos(angle),
                        self.center_y + self.hex_size * sin(angle),
                    ]
                )

            if self.grid_p[self.row + 1][self.col + 1] == 2:
                Color(220 / 255, 134 / 255, 134 / 255)
                # Color(0.5,0,0)

            Triangle(points=points[4:10])
            Triangle(points=points[-2:] + points[:5])
            Rectangle(pos=points[4:6], size=(self.hex_width, self.hex_size))

            Color(0.2, 0.2, 0.2)

            # Dessiner les contours du triangle

            Line(points=points + points[:2], width=(20) / (self.coll))


class HexGrid(Widget):
    def __init__(
        self, rows, cols, hex_size, pos_x=0, pos_y=0, grid_p=0, coll=0, **kwargs
    ):
        super(HexGrid, self).__init__(**kwargs)
        self.rows = rows
        self.cols = cols
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.grid_p = grid_p
        self.hex_size = hex_size
        self.hex_width = cos(pi / 6) * self.hex_size * 2
        self.height = (cos(pi / 3) * self.hex_size + self.hex_size * 0.5) * 2
        self.coll = coll

        self.draw_grid()

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                center_x = self.pos_x + (col + (row / 2)) * self.hex_width
                center_y = self.pos_y - row * (
                    self.height - cos(pi / 3) * self.hex_size
                )
                poss_hex[row][col] = (round(center_x), round(center_y))
        ratio = 1.25

        top_left = [
            (poss_hex[0][0][0] - self.hex_width * ratio),
            (poss_hex[0][0][1] + self.height * 0.5 * ratio),
        ]
        bot_right = [
            (poss_hex[-1][-1][0] + self.hex_width * ratio),
            (poss_hex[-1][-1][-1] - self.height * 0.5 * ratio),
        ]
        top_right = [
            (poss_hex[0][-1][0] + self.hex_width * 0.5 * ratio),
            (poss_hex[0][-1][1] + self.height * 0.5 * ratio),
        ]
        bot_left = [
            (poss_hex[-1][0][0] - self.hex_width * 0.5 * ratio),
            (poss_hex[-1][0][1] - self.height * 0.5 * ratio),
        ]
        middle = [Window.size[0] / 2, Window.size[1] / 2]

        Color(220 / 255, 134 / 255, 134 / 255)
        Triangle(points=top_left + bot_left + middle)
        Triangle(points=top_right + bot_right + middle)

        Color(126 / 255, 215 / 255, 193 / 255)
        Triangle(points=top_left + top_right + middle)
        Triangle(points=bot_left + bot_right + middle)

        for row in range(self.rows):
            for col in range(self.cols):
                center_x = self.pos_x + (col + (row / 2)) * self.hex_width
                center_y = self.pos_y - row * (
                    self.height - cos(pi / 3) * self.hex_size
                )
                Hexagon(
                    center_x, center_y, self.hex_size, row, col, self.grid_p, self.coll
                )


poss_hex = []
