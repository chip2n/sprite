import events
from kivy.app import App
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout

class PaletteGrid(GridLayout):
    color_width = NumericProperty(10)
    def __init__(self, **kwargs):
        super(PaletteGrid, self).__init__(**kwargs)

    def add_color(self, color):
        palette_color = PaletteColor(color)
        self.add_widget(palette_color)
        self.on_color_added()

    def on_color_added(self):
        w = min(len(self.children) * self.color_width, self.cols * self.color_width)
        y = int((len(self.children) - 1) / self.cols) + 1
        h = min(y* self.color_width, self.rows * self.color_width)
        self.size = (w, h)

class Palette(AnchorLayout):

    def add_color(self, color):
        self.ids.palette_grid.add_color(color)

class PaletteColor(BoxLayout):
    color = ListProperty([0,0,0,1])

    def __init__(self, color, **kwargs):
        super(PaletteColor, self).__init__(**kwargs)
        self.color = color
        self.register_event_type('on_color_pick')

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch('on_color_pick', self.color)
            return True
        else:
            return super(PaletteColor, self).on_touch_down(touch)

    def on_color_pick(self, color):
        print('yay')
        App.get_running_app().lol(color)
