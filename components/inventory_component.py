import UI_manager as UI
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label

class GoldWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(GoldWidget, self).__init__(**kwargs)
        self.canvas.before.clear()
        with self.canvas.before:
            self.rect = Rectangle(
                source = 'graphics/menu_background.png',
                pos=self.pos,
                size=self.size,
            )
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.size = (dp(325),dp(100))
        self.pos = (dp(200), dp(110))
        self.size_hint = (None, None)
        self.spacing = dp(110)
        self.padding = dp(20)

        self.add_widget(Image(source="graphics/shop_button.png"))
        self.add_widget(UI.stats["gold"])
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class GoldGainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(GoldGainWidget, self).__init__(**kwargs)
        self.canvas.before.clear()
        with self.canvas.before:
            self.rect = Rectangle(
                source = 'graphics/menu_background.png',
                pos=self.pos,
                size=self.size,
            )
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.size = (dp(325),dp(100))
        self.pos = (dp(200), dp(110))
        self.size_hint = (None, None)
        self.spacing = dp(120)
        self.gold_gain = 0
        self.gold_gain_label = Label(text=str(self.gold_gain), font_size=40)
        self.padding = dp(20)

        self.add_widget(Image(source="graphics/shop_button.png"))
        self.add_widget(self.gold_gain_label)
    
    def update_gold_gain(self, gold_gain):
        self.gold_gain_label.text = "+"+"{0:g}".format(gold_gain)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class Trash(Image):
    def __init__(self, **kwargs):
        super(Trash, self).__init__(**kwargs)
        self.source = "graphics/trash.png"
        self.size_hint = (0.031,0.055)
        self.pos_hint = {"x": 0.105, "y": 0.72}
        
gold_widget = GoldWidget(size=(dp(325),dp(100)), pos_hint={"x": 0.138, "y": 0.16}, size_hint=(None,None))
gold_gain_widget = GoldGainWidget(size=(dp(325),dp(100)), pos_hint={"x": 0.138, "y": 0.16}, size_hint=(None,None))