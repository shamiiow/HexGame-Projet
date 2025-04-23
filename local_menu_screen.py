from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0 / 255, 45 / 255, 90 / 255, 1)
        with self.canvas.before:
            Color(0 / 255, 45 / 255, 90 / 255, 1)
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[15])
        self.bind(pos=self.update_bg_rect, size=self.update_bg_rect)

    def update_bg_rect(self, *args):
        self.bg_rect.pos = [self.pos[0]-8, self.pos[1]-3]
        self.bg_rect.size = [self.size[0]+16, self.size[1]+6]

class ColoredLabel(Label):
    def __init__(self, color = None, **kwargs):
        super(ColoredLabel, self).__init__(**kwargs)
        with self.canvas.before:
            Color(color[0], color[1], color[2])
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius = [(self.size[0]/4,self.size[1]/4)]*2)
            self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = (self.size[0] * 1, self.size[1] * 1)
        self.rect.pos = (self.x - (self.rect.size[0] - self.size[0]) / 2, self.y - (self.rect.size[1] - self.size[1]) / 2)  
        
class LocalMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(LocalMenuScreen, self).__init__(**kwargs)
        Window.clearcolor = "#F0DBAF"
        #Window.fullscreen = 'auto'                    # FORCE FULLSCREEN

        self.grille = 7
        self.p1_bot = False
        self.p2_bot = False

        self.root = AnchorLayout(anchor_x='left', anchor_y='top')

        with self.root.canvas.before:
            self.rects = []
            self.update_gradient()

        self.root.bind(size=self.update_rect, pos=self.update_rect)
        
        self.window = GridLayout(padding=[30,30,30,20], spacing=10, rows = 6, cols = 1)

        self.players_name = BoxLayout(orientation = 'horizontal', size_hint = (1,None), height = 130, spacing = 500, padding = [30, 80, 30, 0])
        
        self.players_bot = BoxLayout(orientation = 'horizontal', size_hint = (1,None), height = 60, padding = [30, 80, 30, 0])


        self.player1_bot_box = BoxLayout(orientation = 'horizontal', size_hint=(None, None), size=(130, 60))
        self.player2_bot_box = BoxLayout(orientation = 'horizontal', size_hint=(None, None), size=(130, 60))

        self.button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.8), padding=[150, 0, 150, 20], spacing=50)

        self.footer = GridLayout(rows = 1, cols = 1, padding = [200, 0, 200, 0], size_hint=(1, 0.8))



        self.title = Label(text='Local Mode', font_size=90, color=(0 / 255, 20 / 255, 40 / 255, 1))
        

        self.player1_entry = TextInput(text='', hint_text="Name player 1", multiline = False, size_hint_x = None, width = 220, background_color = (220/255,134/255,134/255), font_size = 30)
        self.player2_entry = TextInput(text='', hint_text="Name player 2", multiline = False, size_hint_x = None, width = 220, background_color = (126/255,215/255,193/255), font_size = 30, halign = 'right')
        
        


        self.texte = Label(text="Pick the grid size :", font_size=40, color=(0 / 255, 20 / 255, 40 / 255, 1))

        self.decrement_button = RoundedButton(text='-', font_size=60, size_hint=(0.3, 1))
        self.decrement_button.bind(on_press=self.decrement_grille)
        self.grille_label = ColoredLabel(text=str(self.grille), color=(0 / 255, 45 / 255, 90 / 255, 1), font_size=50, size_hint=(0.4, 1))
        self.increment_button = RoundedButton(text='+', font_size=60, size_hint=(0.3, 1))
        self.increment_button.bind(on_press=self.increment_grille)

        
        self.play_button = RoundedButton(text= "Play", font_size=40, background_color= (0/255, 45/255, 90/255))  
        self.play_button.bind(on_press=self.go_to_game)

        self.players_name.add_widget(self.player1_entry)
        self.players_name.add_widget(self.player2_entry)   

        self.player1_type_check = Button(text="X", size_hint = (None,1), width = 60, background_normal = '', background_color=(213/255,86/255,90/255), font_size=40)
        self.player1_type_check.bind(on_press=self.p1_checkbox)
        self.player1_type_label = Label(text="bot ?", color = (0,0,0), font_size=30)

        self.player2_type_label = Label(text="bot ?", color = (0,0,0), font_size=30)
        self.player2_type_check = Button(text="X", size_hint = (None,1), width = 60, background_normal = '', background_color=(213/255,86/255,90/255), font_size=40)
        self.player2_type_check.bind(on_press=self.p2_checkbox)

        self.player1_bot_box.add_widget(self.player1_type_check)
        self.player1_bot_box.add_widget(self.player1_type_label)

        self.player2_bot_box.add_widget(self.player2_type_label)
        self.player2_bot_box.add_widget(self.player2_type_check)

        self.players_bot.add_widget(self.player1_bot_box)
        self.players_bot.add_widget(self.player2_bot_box)

    
        self.button_layout.add_widget(self.decrement_button)
        self.button_layout.add_widget(self.grille_label)
        self.button_layout.add_widget(self.increment_button)


        self.footer.add_widget(self.play_button)

        self.window.add_widget(self.title)
        self.window.add_widget(self.players_name)
        self.window.add_widget(self.players_bot)   
        self.window.add_widget(self.texte)
        self.window.add_widget(self.button_layout)
        self.window.add_widget(self.footer)

        self.root.add_widget(self.window)
        self.add_widget(self.root)

        self.close_button = Button(text='Back', font_size=25, size_hint = (0.15, 0.13), background_normal = '', background_color=(0 / 255, 45 / 255, 90 / 255, 1))
        self.close_button.bind(on_press=self.go_to_menu)
        self.root.add_widget(self.close_button)


    def update_rect(self, *args):
        self.update_gradient()

        self.player1_entry.width = (Window.size[0] / 800 )*220
        self.player2_entry.width = (Window.size[0] / 800 )*220

        self.players_name.spacing = Window.size[0] - self.player1_entry.width*2 - 120
        self.players_bot.spacing = Window.size[0] - self.player1_bot_box.width*2 - 120

        self.button_layout.spacing = Window.size[0]/16
        self.button_layout.padding = [Window.size[0] / 6, 0, Window.size[0] / 6, 10]
        self.footer.padding = [Window.size[0] / 4, 0, Window.size[0] / 4, 0]

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
        
    def p1_checkbox(self, instance):
        if self.p1_bot == False:
            self.p1_bot = True
            self.player1_type_check.text = "√"
            self.player1_type_check.background_color = (118/255,232/255,150/255)
        else:
            self.p1_bot = False
            self.player1_type_check.text = "X"
            self.player1_type_check.background_color = (213/255,86/255,90/255)

    def p2_checkbox(self, instance):
        if self.p2_bot == False:
            self.p2_bot = True
            self.player2_type_check.text = "√"
            self.player2_type_check.background_color = (118/255,232/255,150/255)
        else:
            self.p2_bot = False
            self.player2_type_check.text = "X"
            self.player2_type_check.background_color = (213/255,86/255,90/255)

    def go_to_game(self, instance):
        self.manager.get_screen('game').set_variables(self.player1_entry.text, self.player2_entry.text, self.p1_bot, self.p2_bot, self.grille)
        self.manager.get_screen('game').update()

        self.manager.current = 'game'
    
    def go_to_menu(self, instance):
        print("Back to menu")
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'
    



