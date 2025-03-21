from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.anchorlayout import AnchorLayout

from kivy.clock import Clock
from network import Network

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

class ServerScreen(Screen):
    def __init__(self, **kwargs):
        super(ServerScreen, self).__init__(**kwargs)
        Window.clearcolor = (240 / 255, 219 / 255, 175 / 255, 1)
        self.fpsServer = 8/4
        self.stat = "Menudefault%"
        self.message = self.stat
        self.nomServ = ""
        

        self.root = AnchorLayout(anchor_x='left', anchor_y='top')

        with self.root.canvas.before:
            self.rects = []
            self.update_gradient()
        self.root.bind(size=self.update_rects, pos=self.update_rects)

        self.content_layout = BoxLayout(orientation='vertical', padding=[30, 30, 30, 30], spacing=10)

        self.title = Label(text='Server', font_size=130, color=(0/255, 20/255, 40/255, 1), size_hint=(1, 0.2))
        self.content_layout.add_widget(self.title)

        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, 300))
        self.server_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.server_layout.bind(minimum_height=self.server_layout.setter('height'))

        self.game_host = []
        self.varParceQuePythonEstNul = 0
        

        scroll_view.add_widget(self.server_layout)
        self.content_layout.add_widget(scroll_view)

        self.input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=100)
        self.text_input = TextInput(hint_text='Enter player name', size_hint=(0.7, 1))
        self.create_button = RoundedButton(text='Créer', size_hint=(0.3, 1))
        self.create_button.bind(on_press=self.go_to_waiting)
        self.input_layout.add_widget(self.text_input)
        self.input_layout.add_widget(self.create_button)

        self.content_layout.add_widget(self.input_layout)

        self.root.add_widget(self.content_layout)
        self.add_widget(self.root)

        self.close_button = Button(text='Back', font_size=25, size_hint = (0.15, 0.13), background_normal = '', background_color=(0 / 255, 45 / 255, 90 / 255, 1))
        self.close_button.bind(on_press=self.print_server)
        self.root.add_widget(self.close_button)
    
    def update_line_rect(self, rect):
        def _update_rect(instance, value):
            rect.pos = instance.pos
            rect.size = instance.size
        return _update_rect

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_game_state(self, dt):
        print('-----------------------------------------')
        print(f"id: {self.id}")
        print(f"Data send: {self.message}")
        self.data = self.network.send(self.message).split("%")
        print(f"Data received: {self.data}")
        if self.data[0] == "Menudefault":
            self.game_host = self.data[1].split("|")
            self.game_host.pop()
            self.game_host.reverse()
            print(self.game_host)
            self.server_layout.clear_widgets()
            self.print_server()
        
        if self.data[0] == "Menujoin":
            self.nomServ = self.data[1]
            self.print_server()
            self.go_to_waiting(self)
            
        
        

        self.message = self.stat

    def update_rects(self,instance, value):
        if self.varParceQuePythonEstNul == 0: self.varParceQuePythonEstNul = 1

        elif self.varParceQuePythonEstNul == 1:
            self.varParceQuePythonEstNul = 2
            print('setup_server')
            self.network = Network()
            self.id = self.network.send("AskAttribId")
            self.gameUpdate = Clock.schedule_interval(self.update_game_state, self.fpsServer)
            
        elif self.varParceQuePythonEstNul == 2: self.varParceQuePythonEstNul = 3
            
        self.update_gradient()
    
    def update_gradient(self, *args):
        
        self.root.canvas.before.clear()
        with self.root.canvas.before:
            # Définir les couleurs de départ et de fin du dégradé
            color_start = Color(240/255, 219/255, 175/255, 1)  
            color_end = Color(225/255, 156/255, 144/255,1)   

            # Dessiner le dégradé
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
    
    def go_to_waiting(self, instance):
        self.message = self.network.send("Menucreate%").split("%")[1]
        self.manager.get_screen('waiting').set_variables(self.id, self.message)
        self.network.disconnect()
        Clock.unschedule(self.gameUpdate)
        self.manager.transition.direction = 'left'
        self.manager.current = 'waiting'

    def go_to_menu(self, instance):
        
        
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

    def go_to_x(self, instance, x):
        self.message = "Menujoin%" + x

    def print_server(self):
        print(self.game_host)
        for host in self.game_host:
            line_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=[10, 0, 20, 0])
            with line_layout.canvas.before:
                Color(0.7, 0.7, 0.7, 1)  # Couleur de fond gris clair
                rect = Rectangle(size=line_layout.size, pos=line_layout.pos)
            line_layout.bind(size=self.update_line_rect(rect), pos=self.update_line_rect(rect))
            
            label = Label(text=host, size_hint=(None, 1), width=200)
            join_button = RoundedButton(text='Join', size_hint=(None, None), width=100, height=40)  # Taille réduite du bouton "Join"
            join_button.bind(on_press= lambda instance, numServ = host: self.go_to_x(instance, numServ))
            button_container = BoxLayout(orientation='vertical', size_hint=(None, 1), width=100)
            button_container.add_widget(Widget())
            button_container.add_widget(join_button)
            button_container.add_widget(Widget())
            
            line_layout.add_widget(label)
            line_layout.add_widget(Widget())  # Espacement
            line_layout.add_widget(button_container)
            self.server_layout.add_widget(line_layout)