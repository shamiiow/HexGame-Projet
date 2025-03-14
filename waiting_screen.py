import os
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.anchorlayout import AnchorLayout

class ColoredLabel(Label):
    def __init__(self, color=None, **kwargs):
        super(ColoredLabel, self).__init__(**kwargs)
        with self.canvas.before:
            Color(color[0], color[1], color[2])
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[(self.size[0]/2, self.size[1]/2)]*4)
            self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = (self.size[0] * 1, self.size[1] * 1)
        self.rect.pos = (self.x - (self.rect.size[0] - self.size[0]) / 2, self.y - (self.rect.size[1] - self.size[1]) / 2)

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0 / 255, 45 / 255, 90 / 255, 1)
        with self.canvas.before:
            Color(0 / 255, 45 / 255, 90 / 255, 1)
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[30])
        self.bind(pos=self.update_bg_rect, size=self.update_bg_rect)

    def update_bg_rect(self, *args):
        self.bg_rect.pos = [self.pos[0]-13, self.pos[1]-6]
        self.bg_rect.size = [self.size[0]+26, self.size[1]+12]

class CloseButton(Button):
    def __init__(self, **kwargs):
        super(CloseButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (100 / 255, 45 / 255, 90 / 255, 1)
        with self.canvas.before:
            Color(0 / 255, 45 / 255, 90 / 255, 1)
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[30])
        self.bind(pos=self.update_bg_rect, size=self.update_bg_rect)

    def update_bg_rect(self, *args):
        self.bg_rect.pos = [self.pos[0]-13, self.pos[1]-6]
        self.bg_rect.size = [self.size[0]+26, self.size[1]+12]
        print(self.bg_rect.pos, self.bg_rect.size)

def close_app(instance):
    App.get_running_app().stop()

class WaitingScreen(Screen):
    def __init__(self, **kwargs):
        super(WaitingScreen, self).__init__(**kwargs)
        Window.clearcolor = (240 / 255, 219 / 255, 175 / 255, 1)

        self.grille = 7

        self.root = AnchorLayout(anchor_x='left', anchor_y='top')

        with self.root.canvas.before:
            self.rects = []
            self.update_gradient()

        self.root.bind(size=self.update_rect, pos=self.update_rect)

        self.content_layout = BoxLayout(orientation='vertical', padding=[30, 70, 30, 30], spacing=10)
        self.title = Label(text='Waiting Screen ...', font_size=90, color=(0 / 255, 20 / 255, 40 / 255, 1))
        self.content_layout.add_widget(self.title)

        self.spacer = Widget(size_hint=(1, 0.5))
        self.content_layout.add_widget(self.spacer)

        self.texte = Label(text="Pick the grid size :", font_size=40, color=(0 / 255, 20 / 255, 40 / 255, 1))
        self.content_layout.add_widget(self.texte)

        self.button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1), padding=[150, 0, 150, 20], spacing=20)
        self.decrement_button = RoundedButton(text='-', font_size=60, size_hint=(0.3, 1))
        self.decrement_button.bind(on_press=self.decrement_grille)
        self.grille_label = ColoredLabel(text=str(self.grille), color=(0 / 255, 45 / 255, 90 / 255, 1), font_size=60, size_hint=(0.4, 1))
        self.increment_button = RoundedButton(text='+', font_size=60, size_hint=(0.3, 1))
        self.increment_button.bind(on_release=self.increment_grille)

        self.button_layout.add_widget(self.decrement_button)
        self.button_layout.add_widget(self.grille_label)
        self.button_layout.add_widget(self.increment_button)
        self.content_layout.add_widget(self.button_layout)

        self.root.add_widget(self.content_layout)
        self.add_widget(self.root)

        # Ajout du bouton "X" arrondi
        self.close_button = CloseButton(text='Back', size_hint = (None, None), size = (70, 30), pos_hint = (None, None), pos=(10,60))
        self.close_button.bind(on_press=close_app)
        self.root.add_widget(self.close_button)

    def update_rect(self, *args):
        self.update_gradient()

    def update_gradient(self, *args):
        self.root.canvas.before.clear()
        with self.root.canvas.before:
            color_start = Color(240 / 255, 219 / 255, 175 / 255, 1)
            color_end = Color(225 / 255, 156 / 255, 144 / 255, 1)
            self.rects = []
            for i in range(100):
                color = Color(
                    color_start.r + (color_end.r - color_start.r) * i / 100,
                    color_start.g + (color_end.g - color_start.g) * i / 100,
                    color_start.b + (color_end.b - color_start.b) * i / 100,
                    1
                )
                rect = Rectangle(pos=(0, i * self.height / 100), size=(self.width, self.height / 100))
                self.rects.append(rect)

    def increment_grille(self, instance):
        self.grille = min(self.grille + 1, 17)
        self.grille_label.text = str(self.grille)

    def decrement_grille(self, instance):
        self.grille = max(self.grille - 1, 2)
        self.grille_label.text = str(self.grille)
