from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.metrics import dp

class DynamicStageButton(Button):
    def __init__(self, x, y, s,  **kwargs):
        super(DynamicStageButton, self).__init__(**kwargs)
        self.background_normal = s
        self.border = (0,0,0,0)
        self.pos_hint = {"center_x": x, "center_y": y}
        self.size = (dp(120),dp(120))
        self.size_hint = (None, None)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


        