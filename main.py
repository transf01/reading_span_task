from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class KeyLabel(Label):
    def __init__(self, **kwargs):
        super(KeyLabel, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.text = keycode[1]
        Clock.schedule_once(self.callback, 5)

    def callback(self, dt):
        self.text = 'timer'

class TestApp(App):
    def build(self):
        label = KeyLabel(text='[color=ff3333]Hello[/color][color=3333ff]World[/color]', markup = True)
        return label

TestApp().run()
