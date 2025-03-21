from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.widget import Widget

class CustomCheckbox(CheckBox):
    def __init__(self, **kwargs):
        super(CustomCheckbox, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (48, 48)  # This sets the size of the CheckBox
        self.bind(active=self.on_checkbox_active)

    # Customize the canvas
    def on_size(self, *args):
        self.canvas.clear()
        with self.canvas:
            self.draw_checkbox()

    def draw_checkbox(self):
        from kivy.graphics import Rectangle
        # Draw a bigger checkbox
        Rectangle(pos=self.pos, size=self.size)

    def on_checkbox_active(self, checkbox, value):
        if value:
            print('Checkbox checked')
        else:
            print('Checkbox unchecked')


class CheckboxApp(App):
    def build(self):
        layout = BoxLayout(orientation='horizontal', spacing=10, padding=50)
        
        # Create a custom large CheckBox
        checkbox = CustomCheckbox()
        
        label = Label(text="Select option", size_hint=(None, None), size=(200, 48))

        layout.add_widget(checkbox)
        layout.add_widget(label)
        
        return layout

if __name__ == "__main__":
    CheckboxApp().run()
