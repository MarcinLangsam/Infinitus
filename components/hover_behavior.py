from kivy.properties import BooleanProperty, ObjectProperty
from kivy.core.window import Window
from kivy.uix.button import Button

class HoverBehavior(object):
    hovered = BooleanProperty(False)
    border_point = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self):
        pass
    def on_leave(self):
        pass

class HoverButton(HoverBehavior, Button):
    pass

class TargetButton(HoverBehavior, Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.normal_source = "graphics/target_normal.png"
        self.hover_source = "graphics/target_hover.png"
        self.down_source = "graphics/target_down.png"

        self.background_normal = self.normal_source
        self.background_down = self.down_source
        
        self.size_hint = (0.1,0.15)
        self.allow_stretch = True
        self.keep_ratio = True
        self.opacity = 0.9
        
    def on_enter(self, *args):
        self.background_normal = self.hover_source

    def on_leave(self, *args):
        self.background_normal = self.normal_source