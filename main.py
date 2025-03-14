from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from menu_screen import MenuScreen
from local_menu_screen import LocalMenuScreen
from server_screen import ServerScreen
from waiting_screen import WaitingScreen
from game_screen import GameScreen


class MyApp(App):
    def build(self):
        self.title = 'Hex Game'
        sm = ScreenManager(transition=SlideTransition(direction='left'))
        
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(LocalMenuScreen(name='local_menu'))
        sm.add_widget(ServerScreen(name='server'))
        sm.add_widget(WaitingScreen(name='waiting'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
     MyApp().run()