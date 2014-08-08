import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.splitter import Splitter
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import ObjectProperty

class SpriteWidget(Widget):
    pass
    #def __init__(self):
    #    pass
        #for key, val in self.ids.items():
        #    print("hej")

        #self.ids.splitter1.strip_cls = TransparentStrip

class SpriteApp(App):
    def build(self):
        #Window.clearcolor = (1, 1, 1, 1)
        return SpriteWidget()

class TransparentStrip(Button):
    def __init__(self, **kwargs):
        super(TransparentStrip, self).__init__(**kwargs)
        self.background_normal = ""
    pass

class SpriteSplitter(Splitter):
    strip_cls = ObjectProperty(TransparentStrip)

if __name__ == '__main__':
    SpriteApp().run()
