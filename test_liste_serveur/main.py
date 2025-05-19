from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from game_screen_local import GameScreenLocal
from game_screen_online import GameScreenOnline
from local_menu_screen import LocalMenuScreen
from menu_screen import MenuScreen
from server_screen import ServerScreen
from waiting_screen import WaitingScreen


class MyApp(App):
    def build(self):
        self.title = 'Hex Game'
        sm = ScreenManager(transition=SlideTransition(direction='left'))
        
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(LocalMenuScreen(name='local_menu'))
        sm.add_widget(ServerScreen(name='server'))
        sm.add_widget(WaitingScreen(name='waiting'))
        sm.add_widget(GameScreenOnline(name='game_online'))
        sm.add_widget(GameScreenLocal(name='game_local'))
        return sm

if __name__ == '__main__':
     MyApp().run()