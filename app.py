import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.splitter import Splitter
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty
from kivy.graphics import Line, Color

from PIL import Image

class SpriteWidget(Widget):
    pass
    #def __init__(self):
    #    pass
        #for key, val in self.ids.items():
        #    print("hej")

        #self.ids.splitter1.strip_cls = TransparentStrip

class CanvasWidget(FloatLayout):
    canvas_size = ObjectProperty((512, 512))
    scale = NumericProperty(1)
    touch_type = 'move'

    @property
    def scaled_size(self):
        w, h = self.canvas_size
        return (w * self.scale, h * self.scale)

    def __init__(self, **kwargs):
        super(CanvasWidget, self).__init__(**kwargs)
        self.size = (512, 512)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.img = Image.new('RGB', (255,255), "black")
        self.pixels = self.img.load()
        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):
                pixels[i,j] = (i, j, 100)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'q':
            self.touch_type = 'move'
        elif keycode[1] == 'w':
            self.touch_type = 'draw'

    def on_touch_down(self, touch):
        print(self.scaled_size)
        if touch.button == 'scrolldown':
            print('Zoomin\' in')
            self.set_scale(self.scale + 0.2)
        elif touch.button == 'scrollup':
            print('Zoomin\' out')
            self.set_scale(self.scale - 0.2)

        if self.collide_point(*touch.pos):
            touch.grab(self)
        return True

    def set_scale(self, scale):
        delta_scale = self.scale - scale
        w, h = self.canvas_size
        self.scale = scale
        self.size = [w * self.scale, h * self.scale]

    def zoom(self, amount):
        w, h = self.canvas_size
        self.canvas_size = [w+amount, h+amount]
        x, y = self.pos
        self.pos = [x-amount/2, y-amount/2]
    
    def on_touch_move(self, touch):
        if touch.grab_current == self:
            if self.touch_type == 'move':
                x, y = self.pos
                dx, dy = touch.dpos
                self.pos = (x+dx, y+dy)
            elif self.touch_type == 'draw':
                print('Drawing on pixels %s' % str(self.project(touch.pos)))
                
        return True

    def project(self, point):
        px,py = point
        x, y = self.pos
        return (px-x, py-y)

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            touch.ungrab(self)
        return True

    def resize(self):
        print('Resize %s' % self.size)

    def redraw_region(region=None):
        # This will redraw a region of the canvas by iterating over
        # a box of pixels in the pixel map and then drawing a
        # rectangle for each of them. Every time something is drawn
        # the rectangle dimensions containing the shape will be sent
        # through a callback to this function
        pass

class GridWidget(Widget):
    lines = ObjectProperty((10,10))
    visible = ObjectProperty(False)
    def __init__(self, **kwargs):
        super(GridWidget, self).__init__(**kwargs)

        self.draw_grid()
    
    def draw_grid(self, instance=None, value=None):
        if self.visible:
            self.canvas.clear()
            with self.canvas:
                Color(1, 0, 0, mode='rgb')

                for i in range(0,self.lines[0]):
                    x_density = self.width / self.lines[0]
                    x = x_density*i + self.pos[0]
                    Line(points=[x, self.pos[1], x, self.height + self.pos[1]], width=1)

            self.bind(pos=self.draw_grid)
            self.bind(size=self.draw_grid)

class SpriteApp(App):
    def build(self):
        #Window.clearcolor = (1, 1, 1, 1)
        return SpriteWidget()

class TransparentStrip(Button):
    def __init__(self, **kwargs):
        super(TransparentStrip, self).__init__(**kwargs)
        self.background_normal = "transparent.png"
        self.background_down = "transparent.png"
    pass

class SpriteSplitter(BoxLayout):
    strip_cls = ObjectProperty(TransparentStrip)
    grabbed = False

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            touch.ungrab(self)
            x,y = self.pos
            if x > -100:
                self.pos = [0, y]
            else:
                self.pos = [-self.width + 20 + self.min_size, y]
        return True

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True
        return False

    def on_touch_move(self, touch):
        if touch.grab_current == self:
            x, y = self.pos
            dx, _ = touch.dpos
            new_x = max(-self.width + 20 + self.min_size, min(self.max_size/2-self.width/2, x+dx))
            self.pos = (new_x, y)
        return True

    def grab(self):
        self.grabbed = True

if __name__ == '__main__':
    SpriteApp().run()
