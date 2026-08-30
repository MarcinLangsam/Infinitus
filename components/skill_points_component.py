import UI_manager as UI, text_pop as tp, player
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader

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

class Stat_Up_Container(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas.before.clear()
        with self.canvas.before:
            self.rect = Rectangle(
                source = 'graphics/stat_background.png',
                pos = self.pos,
                size = self.size,
            )
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.orientation = "vertical"
        self.padding = 15
        self.spacing = 5
        self.add_widget(health_widget)
        self.add_widget(strength_widget)
        self.add_widget(aglity_widget)
        self.add_widget(inteligencec_widget)
        self.add_widget(stata_points_widget)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class Stat_Up_Widget(BoxLayout):
    def __init__(self, stat, description, background_source, background_source_down, **kwargs):
        super().__init__(**kwargs)
        self.stat = stat
        self.description = description
        self.background_source = background_source
        self.background_source_down = background_source_down
        self.error_sound = SoundLoader.load("graphics/sounds/error.wav")
        self.stat_up_sound = SoundLoader.load("graphics/sounds/stat_up.wav")
        self.orientation = "horizontal"
        self.spacing = 5

        self.add_widget(Image(source = self.background_source, size_hint_x=0.4))
        self.add_widget(UI.stats[stat+"_stat_up"])
        self.add_widget(Button(background_normal = "graphics/stat_up_button.png", background_down = "graphics/stat_up_button_press.png", border = (0,0,0,0), on_release= lambda y:self.increase_stat(), size_hint=(0.2, 0.5)))


    def increase_stat(self):
        if player.current_player.stat_points > 0:
            if self.stat == "HP":
                player.current_player.MAX_HP += 10
                player.current_player.HP +=10
            elif self.stat == "STR":
                player.current_player.STR_base +=1
            elif self.stat == "DEX":
                player.current_player.DEX_base +=1
            elif self.stat == "INT":
                player.current_player.INT_base +=1   
            player.current_player.stat_points -=1
            UI.ui.stats_refresh(player.current_player)
            self.stat_up_sound.play()
        else:
            tp.text_pop_stat_up.text = "Nie masz punktów statystyk"
            self.error_sound.play()
            Clock.schedule_interval(tp.clear_pop_up,3)

class Stat_Points_Widget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.spacing = 5

        self.add_widget(UI.stats["stat_points_label"])
        self.add_widget(UI.stats["stat_points"])

            
skill_point_widget = SkillPointWidget(pos_hint={"x": 0.83, "y": 0}, size_hint=(0.17, 0.09))
health_widget = Stat_Up_Widget("HP", "TEST", "graphics/health_stat_up_button.png", "")
strength_widget = Stat_Up_Widget("STR", "TEST", "graphics/strength_stat_up_button.png", "")
aglity_widget = Stat_Up_Widget("DEX", "TEST", "graphics/agility_stat_up_button.png", "")
inteligencec_widget = Stat_Up_Widget("INT", "TEST", "graphics/inteligence_stat_up_button.png", "")
stata_points_widget = Stat_Points_Widget()