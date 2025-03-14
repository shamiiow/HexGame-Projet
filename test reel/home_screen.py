from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        Window.clearcolor = "#F0DBAF"
        # Window.fullscreen = 'auto'                    # FORCE FULLSCREEN

        self.window = GridLayout()
        self.window.rows = 5
        self.window.cols = 1

        self.header = GridLayout(padding=[10, 10, 10, 50])
        self.header.rows = 1
        self.header.cols = 3

        self.title_layout = GridLayout()
        self.title_layout.rows = 1
        self.title_layout.cols = 1

        self.players_name = GridLayout(
            padding=10, size_hint_y=None, height=0.09 * Window.size[1]
        )
        self.players_name.rows = 1
        self.players_name.cols = 2

        self.players_bot = GridLayout(
            padding=10, size_hint_y=None, height=0.09 * Window.size[1]
        )
        self.players_bot.rows = 1
        self.players_bot.cols = 4

        self.player1_bot_box = BoxLayout(
            orientation="horizontal", size_hint_x=None, width=0.1 * Window.size[0]
        )
        self.player2_bot_box = BoxLayout(
            orientation="horizontal", size_hint_x=None, width=0.1 * Window.size[0]
        )

        self.hex_grid_size = GridLayout(spacing=25)
        self.hex_grid_size.rows = 1
        self.hex_grid_size.cols = 3

        self.footer = GridLayout()
        self.footer.rows = 1
        self.footer.cols = 2

        self.float_layout = FloatLayout(size_hint=(1, 1))

        with self.window.canvas.before:
            Color(240 / 255, 219 / 255, 175 / 255)
            self.rect = Rectangle(
                pos=self.window.pos,
                size=(self.window.size[0] + 20, self.window.size[1]),
            )
        self.window.bind(pos=self.update_rect, size=self.update_rect)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # , size_hint_x = None, width = 10

        # self.exit_button = Button(text="X", background_color= (0/255, 45/255, 90/255), size_hint = (None,None), width = Window.size[0]/25, height =  Window.size[1]/25, pos_hint={'x': 0, 'y': 1-(self.height/Window.size[1])})
        self.exit_button = Button(
            text="X",
            background_color=(0 / 255, 45 / 255, 90 / 255),
            pos_hint={"x": 0, "y": 1 - (50 / self.float_layout.size[0])},
            size_hint=(None, None),
            size=(50, 50),
        )
        self.exit_button.bind(on_press=self.close_window)

        self.title = ColoredLabel(text="Hex Game", color=[0 / 255, 20 / 255, 40 / 255])

        self.player1_entry = TextInput(
            text="Joueur 1",
            hint_text="Name player 1",
            multiline=False,
            size_hint_x=None,
            width=150,
            background_color=(220 / 255, 134 / 255, 134 / 255),
        )

        self.player2_entry = TextInput(
            text="Joueur 2",
            hint_text="Name player 2",
            multiline=False,
            size_hint_x=None,
            width=150,
            background_color=(126 / 255, 215 / 255, 193 / 255),
        )

        self.player1_type_check = CheckBox(
            size_hint=(None, None), size=(40, 40), color=(0, 0, 1, 1)
        )
        self.player1_type_label = Label(text="bot ?", color=(0, 0, 0))

        self.player2_type_label = Label(text="bot ?", color=(0, 0, 0))
        self.player2_type_check = CheckBox(
            size_hint=(None, None), size=(40, 40), color=(0, 0, 1, 1)
        )

        self.grid_size_minus = Button(
            text="-",
            background_color=(56 / 255, 62 / 255, 153 / 255),
            background_normal="",
        )
        self.grid_size = ColoredLabel(
            text="Hex Game", color=[56 / 255, 62 / 255, 153 / 255]
        )
        self.grid_size_plus = Button(
            text="+",
            background_color=(56 / 255, 62 / 255, 153 / 255),
            background_normal="",
        )

        self.len_grid = TextInput(text="7", hint_text="len grid")

        self.play_button = Button(
            text="Play", font_size=40, background_color=(0 / 255, 45 / 255, 90 / 255)
        )
        self.play_button.bind(on_press=self.go_to_game)

        self.float_layout.add_widget(self.exit_button)

        self.header.add_widget(self.float_layout)
        self.header.add_widget(self.title)
        self.header.add_widget(Label(text=""))

        self.players_name.add_widget(self.player1_entry)
        self.players_name.add_widget(self.player2_entry)

        self.player1_bot_box.add_widget(self.player1_type_check)
        self.player1_bot_box.add_widget(self.player1_type_label)

        self.player2_bot_box.add_widget(self.player2_type_label)
        self.player2_bot_box.add_widget(self.player2_type_check)

        self.players_bot.add_widget(self.player1_bot_box)
        self.players_bot.add_widget(self.player2_bot_box)

        self.hex_grid_size.add_widget(self.grid_size_minus)
        self.hex_grid_size.add_widget(self.grid_size)
        self.hex_grid_size.add_widget(self.grid_size_plus)

        self.footer.add_widget(self.play_button)

        self.window.add_widget(self.header)
        self.window.add_widget(self.players_name)
        self.window.add_widget(self.players_bot)
        self.window.add_widget(self.hex_grid_size)
        self.window.add_widget(self.footer)

        self.add_widget(self.window)

    def update_rect(self, instance, value):
        value = 20
        self.players_name.spacing = (
            Window.size[0]
            - self.player2_entry.width
            - self.player1_entry.width
            - 2 * self.players_name.padding[0]
        )
        self.players_bot.spacing = (
            Window.size[0]
            - self.player1_bot_box.width
            - self.player2_bot_box.width
            - 2 * self.players_bot.padding[0]
        )
        self.footer.padding = [Window.size[0] * 0.3, 0] * 2
        self.hex_grid_size.padding = [
            Window.size[0] * 0.32,
            Window.size[1] * 0.12,
            Window.size[0] * 0.32,
            Window.size[1] * 0.04,
        ]
        self.rect.pos = (instance.pos[0] - value, instance.pos[1] - value)
        self.rect.size = (instance.size[0] + value * 2, instance.size[1] + value * 2)

    def go_to_game(self, instance):
        self.manager.get_screen("game").set_variables(
            self.player1_entry.text,
            self.player2_entry.text,
            self.p1_checkbox(),
            self.p2_checkbox(),
            int(self.len_grid.text),
        )
        self.manager.get_screen("game").update()

        self.manager.current = "game"

    def close_window(self, instance):
        App.get_running_app().stop()
        Window.close()

    def p1_checkbox(self):
        return self.player1_type_check.active

    def p2_checkbox(self):
        return self.player2_type_check.active


class ColoredLabel(Label):
    def __init__(self, color=None, **kwargs):
        super(ColoredLabel, self).__init__(**kwargs)
        with self.canvas.before:
            Color(color[0], color[1], color[2])
            self.rect = RoundedRectangle(
                size=self.size,
                pos=self.pos,
                radius=[(self.size[0] / 2, self.size[1] / 2)] * 4,
            )
            self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = (self.size[0] * 1, self.size[1] * 1)
        self.rect.pos = (
            self.x - (self.rect.size[0] - self.size[0]) / 2,
            self.y - (self.rect.size[1] - self.size[1]) / 2,
        )


class RoundButton(Button):
    def __init__(self, **kwargs):
        super(RoundButton, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 0, 0, 1)  # Couleur rouge
            self.circle = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self.update_shape, size=self.update_shape)

    def update_shape(self, *args):
        self.circle.pos = self.pos
        self.circle.size = self.size
