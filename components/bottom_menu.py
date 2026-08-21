from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Rectangle
from screen_manager import screen_manager
from components.fancy_button import FancyButton

class BottomMenu(BoxLayout):
    def __init__(self, manager, **kwargs):
        super(BottomMenu, self).__init__(**kwargs)
        self.manager = manager
        self.size_hint = (None,None)
        self.size = (dp(320),dp(110))
        self.canvas.before.clear()
        with self.canvas.before:
            self.rect = Rectangle(
                source = 'graphics/menu_background.png',
                pos=self.pos,
                size=self.size,
            )
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.spacing = dp(20)
        self.padding = dp(25)

        self.add_widget(FancyButton(background_normal="graphics/team_button.png", action = lambda y:self.change_screen("team")))
        self.add_widget(FancyButton(background_normal="graphics/skills_button.png", action = lambda y:self.change_screen("skills")))
        self.add_widget(FancyButton(background_normal="graphics/map_button.png", action = lambda y:self.change_screen("map")))
        
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def change_screen(self,screen_name):
        self.parent.clear_widgets()
        self.manager.current = screen_name