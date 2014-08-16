from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class BrushPanel(BoxLayout):
    def __init__(self, **kwargs):
        super(BrushPanel, self).__init__(**kwargs)
    pass

class BrushSelector(Button):
    showing_dropdown = False

    def on_press(self):
        print('yey')
        if not self.showing_dropdown:
            self.show_dropdown()
        else:
            self.hide_dropdown()
    
    def show_dropdown(self):
        self.parent.ids.drop_down.open(self)
        self.parent.ids.drop_down.opacity = 1.0
        self.showing_dropdown = True

    def hide_dropdown(self):
        self.parent.ids.drop_down.dismiss()
        self.parent.ids.drop_down.opacity = 0.0
        self.showing_dropdown = False

    def on_touch_down(self, touch):
        if self.showing_dropdown:
            print('oh my')
            self.hide_dropdown()
        return super(BrushSelector, self).on_touch_down(touch)

