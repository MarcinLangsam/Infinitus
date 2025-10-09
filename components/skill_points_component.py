import UI_manager as UI
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.metrics import dp

class SkillPointWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(SkillPointWidget, self).__init__(**kwargs)
        self.canvas.before.clear()
        with self.canvas.before:
            self.rect = Rectangle(
                source = 'graphics/menu_background.png',
                pos=self.pos,
                size=self.size,
            )
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.padding = dp(20)

        self.add_widget(Image(source="graphics/main_fight_button.png"))
        self.add_widget(UI.stats["skill_points"])
        
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

skill_point_widget = SkillPointWidget(pos_hint={"center_x": 0.9, "y": 0}, size=(dp(270),dp(80)), size_hint=(None,None))