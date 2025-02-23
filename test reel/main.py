from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from home_screen import HomeScreen
from game_screen import GameScreen

class MyApp(App):
    def build(self):
        self.title = 'Hex Game'
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
     MyApp().run()