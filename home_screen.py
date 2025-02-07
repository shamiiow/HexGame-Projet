from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from math import cos, sin, pi, sqrt
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from random import choice


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        Window.clearcolor = "#F0DBAF"
        #Window.fullscreen = 'auto'                    # FORCE FULLSCREEN

        self.window = GridLayout()
        self.window.rows = 5
        self.window.cols = 1

        self.header = GridLayout()
        self.header.rows = 1
        self.header.cols = 3

        self.title_layout = GridLayout()
        self.title_layout.rows = 1
        self.title_layout.cols = 1

        self.players_name = GridLayout()
        self.players_name.rows = 1
        self.players_name.cols = 2

        self.players_bot = GridLayout()
        self.players_bot.rows = 1
        self.players_bot.cols = 4

        self.hex_grid_size = GridLayout()
        self.hex_grid_size.rows = 1
        self.hex_grid_size.cols = 3

        self.footer = GridLayout()
        self.footer.rows = 1
        self.footer.cols = 2

        with self.window.canvas.before:
            Color(240/255, 219/255, 175/255)
            self.rect = Rectangle(pos=self.window.pos, size=(self.window.size[0] + 20, self.window.size[1]))
        self.window.bind(pos=self.update_rect, size=self.update_rect)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        with self.title_layout.canvas.before:
            Color(28/255, 65/255, 91/255)
            self.rect = Rectangle(pos=self.title_layout.pos, size=self.title_layout.size)
        self.title_layout.bind(pos=self.update_rect, size=self.update_rect)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        
        

        self.window.padding = 0
        
        
        
        self.exit_button = Button(text="X", background_color= (28/255, 65/255, 91/255), padding = 15)
        self.exit_button.bind(on_press=self.close_window)
        self.titre = Label(text="Hex Game", font_size = 65)
        

        self.player1_entry = TextInput(text='enwatibateau', hint_text="Name player 1", multiline = False,size_hint=(0.2, 0.2))
        
        self.player1_type_check = CheckBox()
        self.player1_type_label = Label(text="bot ?")

        self.player2_entry = TextInput(text='shamiiow', hint_text="Name player 2", multiline = False, size_hint=(0.75, 1.5))
        
        self.player2_type_check = CheckBox()
        self.player2_type_label = Label(text="bot ?")
        

        self.len_grid = TextInput(text="7", hint_text = "len grid",)

        self.play_button = Button(text= "Play", font_size=40)  
        self.play_button.bind(on_press=self.go_to_game)



        
        self.title_layout.add_widget(self.titre)

        self.header.add_widget(self.exit_button)
        self.header.add_widget(self.title_layout)
        self.header.add_widget(Label(text=" "))

        self.players_name.add_widget(self.player1_entry)
        self.players_name.add_widget(self.player2_entry)   

        self.players_bot.add_widget(self.player1_type_check)
        self.players_bot.add_widget(self.player2_type_check)

        self.hex_grid_size.add_widget(Label(text="Faudra mettre les boutons ici bg"))

        self.footer.add_widget(self.play_button)

        self.window.add_widget(self.header)
        self.window.add_widget(self.players_name)
        self.window.add_widget(self.players_bot)
        self.window.add_widget(self.hex_grid_size)
        self.window.add_widget(self.footer)

        self.add_widget(self.window)

    def update_rect(self, instance, value):
        value = 20
        self.rect.pos = (instance.pos[0] - value, instance.pos[1] - value)
        self.rect.size = (instance.size[0] + value*2, instance.size[1] + value*2)

    def go_to_game(self, instance):
        self.manager.get_screen('game').set_variables(self.player1_entry.text, self.player2_entry.text, self.p1_checkbox(), self.p2_checkbox(), int(self.len_grid.text))
        self.manager.get_screen('game').update()

        self.manager.current = 'game'

    def close_window(self, instance):
        App.get_running_app().stop() 
        Window.close()    

    def p1_checkbox(self):
        return self.player1_type_check.active

    def p2_checkbox(self):
        return self.player2_type_check.active
            