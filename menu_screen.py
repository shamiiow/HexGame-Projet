import os

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

# changer le bind des boutons quand les fenêtres seront créées


class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0 / 255, 45 / 255, 90 / 255, 1)
        with self.canvas.before:
            Color(0 / 255, 45 / 255, 90 / 255, 1)
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[30])
        self.bind(pos=self.update_bg_rect, size=self.update_bg_rect)

    def update_bg_rect(self, *args):
        self.bg_rect.pos = [self.pos[0] - 13, self.pos[1] - 6]
        self.bg_rect.size = [self.size[0] + 26, self.size[1] + 12]


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        Window.clearcolor = "#F0DBAF"
        # Window.fullscreen = 'auto'                    # FORCE FULLSCREEN

        self.root = AnchorLayout()

        # Ajout de l'arrière-plan
        with self.root.canvas.before:
            self.rects = []
            self.update_gradient()
        self.root.bind(size=self.update_rects, pos=self.update_rects)
        # Layout principal pour le contenu
        self.content_layout = BoxLayout(
            orientation="vertical", padding=[30, 70, 30, 30], spacing=10
        )

        # Nom du jeu
        self.game_title = Label(
            text="Hexgame",
            font_size=130,
            color=(0 / 255, 20 / 255, 40 / 255, 1),
            size_hint=(1, 0.2),
        )
        self.content_layout.add_widget(self.game_title)

        # Espacement entre le titre et les boutons
        self.spacer = Widget(size_hint=(1, 0.1))
        self.content_layout.add_widget(self.spacer)

        # Boutons
        self.button_layout = BoxLayout(
            orientation="vertical",
            size_hint=(1, 0.6),
            padding=[100, 0, 100, 0],
            spacing=20,
        )

        self.local_button = RoundedButton(text="Local", font_size=60, size_hint=(1, 1))
        self.local_button.bind(on_press=self.go_to_local)

        self.online_button = RoundedButton(
            text="Online", font_size=60, size_hint=(1, 1)
        )
        self.online_button.bind(on_press=self.go_to_online)

        self.button_layout.add_widget(self.local_button)
        self.button_layout.add_widget(self.online_button)

        # Centrer les boutons en bas de la fenêtre (2/3 hauteur)
        self.content_layout.add_widget(
            Widget(size_hint=(1, 0.2))
        )  # Ajouter un autre espace au-dessus des boutons
        self.content_layout.add_widget(self.button_layout)

        # Ajouter le layout principal au root layout
        self.root.add_widget(self.content_layout)

        # Ajouter le root layout à la fenêtre
        self.add_widget(self.root)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_rects(self, instance, value):
        self.update_gradient()

    def update_gradient(self, *args):
        self.root.canvas.before.clear()
        with self.root.canvas.before:
            # Définir les couleurs de départ et de fin du dégradé
            color_start = Color(240 / 255, 219 / 255, 175 / 255, 1)
            color_end = Color(225 / 255, 156 / 255, 144 / 255, 1)

            # Dessiner le dégradé
            self.rects = []
            for i in range(100):
                color = Color(
                    color_start.r + (color_end.r - color_start.r) * i / 100,
                    color_start.g + (color_end.g - color_start.g) * i / 100,
                    color_start.b + (color_end.b - color_start.b) * i / 100,
                    1,
                )
                rect = Rectangle(
                    pos=(0, i * self.height / 100), size=(self.width, self.height / 100)
                )
                self.rects.append(rect)

    def go_to_online(self, instance):
        self.manager.get_screen("server").setup_network()
        self.manager.transition.direction = "left"
        self.manager.current = "server"

    def go_to_local(self, instance):
        self.manager.transition.direction = "left"
        self.manager.current = "local_menu"
