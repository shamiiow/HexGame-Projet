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



#changer le bind des boutons quand les fenêtres seront créées



class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0/255, 45/255, 90/255, 1)
        with self.canvas.before:
            Color(0/255, 45/255, 90/255, 1)
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[30])
        self.bind(pos=self.update_bg_rect, size=self.update_bg_rect)

    def update_bg_rect(self, *args):
        self.bg_rect.pos = [self.pos[0]-13, self.pos[1]-6]
        self.bg_rect.size = [self.size[0]+26, self.size[1]+11]

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        Window.clearcolor = "#F0DBAF"
        #Window.fullscreen = 'auto'                    # FORCE FULLSCREEN

        self.root = AnchorLayout()

        # Ajout de l'arrière-plan
        with self.root.canvas.before:
            Color(240 / 255, 219 / 255, 175 / 255, 1)  # Couleur de fond
            self.rect = Rectangle(size=self.root.size, pos=self.root.pos)
        self.root.bind(size=self.update_rect, pos=self.update_rect)
        # Layout principal pour le contenu
        self.content_layout = BoxLayout(orientation='vertical', padding=[30,70,30,30], spacing=10)
        
        # Nom du jeu
        self.game_title = Label(text='Hexgame', font_size=130, color = (176/255,97/255,97/255), size_hint=(1, 0.2))
        self.content_layout.add_widget(self.game_title)
        
        # Espacement entre le titre et les boutons
        self.spacer = Widget(size_hint=(1, 0.1))
        self.content_layout.add_widget(self.spacer)
        
        # Boutons
        self.button_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.6), padding=[100, 0, 100, 0], spacing=20)

        self.local_button = RoundedButton(text='Local', font_size = 60, size_hint=(1, 1))
        self.local_button.bind(on_press=self.go_to_local)
        
        self.online_button = RoundedButton(text='En ligne', font_size = 60, size_hint=(1, 1))
        self.online_button.bind(on_press=self.go_to_online)

        self.button_layout.add_widget(self.local_button)
        self.button_layout.add_widget(self.online_button)

        # Centrer les boutons en bas de la fenêtre (2/3 hauteur)
        self.content_layout.add_widget(Widget(size_hint=(1, 0.2)))  # Ajouter un autre espace au-dessus des boutons
        self.content_layout.add_widget(self.button_layout)
        
        # Ajouter le layout principal au root layout
        self.root.add_widget(self.content_layout)

        # Ajouter le root layout à la fenêtre 
        self.add_widget(self.root)
    
    def update_rect(self,instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def go_to_online(self, instance):
        self.manager.current = 'waiting'

    def go_to_local(self, instance):
        self.manager.current = 'home'

