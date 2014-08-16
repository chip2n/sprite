import kivy
kivy.require('1.8.0')

import events
import palette

import itertools
from array import array
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.splitter import Splitter
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.core.image import Image
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, StringProperty
from kivy.graphics import Line, Color, Rectangle, InstructionGroup
from kivy.graphics.texture import Texture
import random

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
    texture = ObjectProperty()
    touch_type = 'move'
    current_color = [0,0,0,1]

    @property
    def scaled_size(self):
        w, h = self.canvas_size
        return (w * self.scale, h * self.scale)

    def __init__(self, **kwargs):
        super(CanvasWidget, self).__init__(**kwargs)
        self.size = (512, 512)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)


        self.img = Image.open('test.png')
        self.img = self.img =  self.img.transpose(Image.FLIP_TOP_BOTTOM)
        self.texture = Texture.create(size=(512,512))
        self.texture.mag_filter = 'nearest'
        size = 512*512*3
        buf = []
        for r,g,b,a in self.img.getdata():
            buf.extend([r,g,b,a])
        #buf = [int(x*255/size) for x in range(size)]
        #buf = self._flatten_list(self.pixels)
        self.arr = array('B', buf)
        self.texture.blit_buffer(self.arr, colorfmt='rgba', bufferfmt='ubyte')

        with self.canvas:
            self.test = InstructionGroup()
            #self.test.add(Color(1, 1, 0, mode='rgb'))
            self.test.add(Rectangle(texture=self.texture, pos=self.pos, size=self.size, group='heh'))

        #self.bind(texture=self.on_texture_update)
        self.bind(pos=self.on_texture_update)
        self.bind(size=self.on_texture_update)

    def on_texture_update(self, instance=None, value=None):
        print('on_texture_update')
        for inst in self.test.get_group('heh'):
            if hasattr(inst, 'pos'):
                inst.pos = self.pos
            if hasattr(inst, 'size'):
                inst.size = self.size
        pass

        #self.canvas.clear()
        #with self.canvas:
        #    Color(1, 1, 0, mode='rgb')
        #    #Rectangle(texture=self.texture, pos=self.pos, size=self.size)
        #    Rectangle(pos=self.pos, size=self.size)


    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'q':
            self.touch_type = 'move'
        elif keycode[1] == 'w':
            self.touch_type = 'draw'
        elif keycode[1] == 'e':
            r = random.random()
            g = random.random()
            b = random.random()
            print(self.parent.parent.ids.palette.add_color([r,g,b,1]))

    def on_touch_down(self, touch):
        if touch.button == 'scrolldown':
            print('Zoomin\' in')
            self.set_scale(self.scale * 1.2, touch.pos)
        elif touch.button == 'scrollup':
            print('Zoomin\' out')
            self.set_scale(self.scale / 1.2, touch.pos)
        else:
            if self.touch_type == 'draw':
                x,y = self.project(touch.pos)
                r,g,b,a = self.current_color
                self.update_pixel(int(x), int(y), r, g, b, a)
                self.refresh()
            touch.grab(self)
        return True

    def on_touch_move(self, touch):
        if touch.grab_current == self:
            if self.touch_type == 'move':
                x, y = self.pos
                dx, dy = touch.dpos
                self.pos = (x+dx, y+dy)
            elif self.touch_type == 'draw':
                x,y = self.project(touch.pos)
                px, py = self.project(touch.ppos)
                #self.update_pixel(int(x), int(y), 255, 0, 100, 100)
                r,g,b,a = self.current_color
                self.draw_line(px, py, x, y, r,g,b,a)
                
        return True

    def set_color(self, color):
        self.current_color = color

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            touch.ungrab(self)
        return True

    def update_pixel(self, x, y, r, g, b, a):
        w,h = self.canvas_size
        index = int((y * w * 4) + 4 * x)
        self.arr[index] = int(r*255)
        self.arr[index+1] = int(g*255)
        self.arr[index+2] = int(b*255)
        self.arr[index+3] = int(a*255)
        self.texture.blit_buffer(self.arr, colorfmt='rgba', bufferfmt='ubyte')
        print('PIXEL: %s,%s' % (int(x), int(y)))

    def refresh(self):
        self.canvas.ask_update()

    def draw_line(self, x0, y0, x1, y1, r,g,b,a):
        self.update_pixel(int(x0),int(y0),r,g,b,a)
        self.update_pixel(int(x1),int(y1),r,g,b,a)
        print('LINE: %s, %s -> %s, %s' % (x0,y0,x1,y1))
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        steep = abs(y1-y0) > abs(x1-x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        deltax = x1-x0
        deltay = abs(y1-y0)
        error = int(deltax / 2)
        ystep = 0
        y = y0
        if y0 < y1:
            ystep = 1
        else:
            ystep = -1

        for x in range(x0,x1):
            if steep:
                self.update_pixel(y, x, r,g,b,a)
            else:
                self.update_pixel(x, y, r,g,b,a)
            error -= deltay
            if error < 0:
                y = y + ystep
                error = error + deltax
        self.refresh()


    def redraw_canvas(self):
        arr = array('B', self.buf)
        self.texture.blit_buffer(arr, colorfmt='rgba', bufferfmt='ubyte')

    def is_moveable(self):
        w, h = self.size
        return w > Window.size[0] and h > Window.size[1]

    def set_scale(self, scale, pivot):
        delta_scale = self.scale - scale
        prev_w, prev_h = self.size
        c_w, c_h = self.canvas_size
        self.scale = scale
        w, h = (c_w * self.scale, c_h * self.scale)
        self.size = (w, h)
        dw = w - prev_w
        dh = h - prev_h
        px, py = pivot
        x, y = self.pos
        ratio_x =  abs(px - x) / w
        ratio_y =  abs(py - y) / h
        after_x = dw * ratio_x
        after_y = dh * ratio_y
        print('current', ratio_x, ratio_y)
        #self.center = (x - (ax-px)*scale, y - (ay-py)*scale)
        #if not self.is_moveable():
        #    self.center = Window.center
        #else:
        x,y = self.pos
        self.pos = (x - after_x, y - after_y)

    def project(self, point):
        px,py = point
        x, y = self.pos
        ratio = self.canvas_size[0]/self.size[0]
        return (ratio*(px-x), ratio*(py-y))

    def _flatten_list(self, lst):
        return list(itertools.chain.from_iterable(lst))


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
    lines = ObjectProperty((512,512))
    visibility_density = ObjectProperty(10)
    visible = ObjectProperty(True)
    
    def __init__(self, **kwargs):
        super(GridWidget, self).__init__(**kwargs)

        self.bind(pos=self.draw_grid)
        self.bind(size=self.draw_grid)
    
    def draw_grid(self, instance=None, value=None):
        if self.visible:
            self.canvas.clear()
            with self.canvas:
                for i in range(0,self.lines[0]):
                    x_density = self.width / self.lines[0]
                    if x_density > self.visibility_density:
                        x = x_density*i + self.pos[0]
                        if x > 0 and x < Window.size[0]:
                            Color(0, 0, 0, mode='rgb')
                            Line(points=[x, self.pos[1], x, self.height + self.pos[1]], width=1)

                for i in range(0,self.lines[1]):
                    y_density = self.height / self.lines[1]
                    if y_density > self.visibility_density:
                        y = y_density*i + self.pos[1]
                        if y > 0 and y < Window.size[1]:
                            Color(0, 0, 0, mode='rgb')
                            Line(points=[self.pos[0], y, self.pos[0] + self.width, y], width=1)



class SpriteApp(App):
    def build(self):
        #Window.clearcolor = (1, 1, 1, 1)
        self.root_widget = SpriteWidget()
        return self.root_widget

    def lol(self, color):
        self.root_widget.ids.canvas.set_color(color)

class TransparentStrip(Button):
    def __init__(self, **kwargs):
        super(TransparentStrip, self).__init__(**kwargs)
        self.background_normal = "transparent.png"
        self.background_down = "transparent.png"

class SpriteSplitter(BoxLayout):
    position = StringProperty('right')
    handle_size = NumericProperty(30)
    grabbed = False

    def __init__(self, **kwargs):
        super(SpriteSplitter, self).__init__(**kwargs)

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            touch.ungrab(self)
            x,y = self.pos
            if self.position == 'left':
                if x > -self.max_size/2:
                    self.pos = [0, y]
                else:
                    self.pos = [-self.width + self.min_size, y]
            elif self.position == 'bottom':
                if y > -self.max_size/2:
                    self.pos = [x, 0]
                else:
                    self.pos = [x, -self.height + self.min_size]

        return True

    def on_touch_down(self, touch):
        if self.position == 'left':
            x, y = touch.pos
            if self.collide_point(max(0, x - self.handle_size), y):
                touch.grab(self)
                super(SpriteSplitter, self).on_touch_down(touch)
                return True
        elif self.position == 'bottom':
            x, y = touch.pos
            if self.collide_point(x, max(0, y - self.handle_size)):
                touch.grab(self)
                super(SpriteSplitter, self).on_touch_down(touch)
                return True
        return super(SpriteSplitter, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current == self:
            x, y = self.pos
            dx, dy = touch.dpos
            if self.position == 'left':
                new_x = max(-self.width + self.min_size, min(0, x+dx))
                self.pos = (new_x, y)
            elif self.position == 'bottom':
                new_y = max(-self.height + self.min_size, min(0, y+dy))
                self.pos = (x, new_y)
        return True

    def grab(self):
        self.grabbed = True

if __name__ == '__main__':
    SpriteApp().run()
