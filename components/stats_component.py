import UI_manager as UI, player, tooltip as tt, text_pop as tp
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.audio import SoundLoader

class StatsButton(Button):
    def __init__(self, stat, description, background_source, background_source_down, **kwargs):
        super(StatsButton, self).__init__(**kwargs)
        self.bind(on_release=self.on_toggle)
        self.stat = stat
        self.description = description
        self.background_normal = background_source
        self.background_down = background_source_down
        self.border = (0,0,0,0)
        #self.size = (dp(15),dp(15))
        #self.size_hint = (None, None)
        #self.height = self.width
        self.stat_up_sound = SoundLoader.load("graphics/sounds/stat_up.wav")

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        Clock.unschedule(self.display_tooltip)
        self.close_tooltip()
        if self.collide_point(*self.to_widget(*pos)):
            self.t = self.description
            self.p = (self.pos[0]+25,self.pos[1])
            Clock.schedule_once(self.display_tooltip, 0.5)
            print("TEST")

    def close_tooltip(self, *args):
        tt.clear_tooltip(self.tooltip)
    def display_tooltip(self, *args):
        tt.set_tooltip(self.tooltip, "TEST", self.p)
    
    def on_toggle(self, touch):
        print(self.pos)
        if isinstance(self.last_touch, MouseMotionEvent):
            self.increase_stat()
            self.stat_up_sound.play()

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
        else:
            tp.text_pop_stat_up.text = "Nie masz punktów statystyk"
            Clock.schedule_interval(tp.clear_pop_up,3)

class StatsUpButtonContainer(BoxLayout):
    def __init__(self, **kwargs):
        super(StatsUpButtonContainer, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = [-dp(35), -dp(20), dp(35), dp(80)]
        self.size_hint_y = 0.65
        self.size_hint_x = 0.1
        self.add_widget(StatsButton("HP", "Zwiększa zdrowię o 10","graphics/health_stat_up_button.png", "graphics/health_stat_up_button_press.png"))
        self.add_widget(StatsButton("STR", "Zwiększa obrażenia o 1\nWpływa na umiejętności wojownika", "graphics/strength_stat_up_button.png", "graphics/strength_stat_up_button_press.png"))
        self.add_widget(StatsButton("DEX", "Decyduje o kolejce w walce\nZwiększa szansę na unik i cios krytyczny\nWpływa na umięjętności łotra", "graphics/aglity_stat_up_button.png", "graphics/aglity_stat_up_button_press.png"))
        self.add_widget(StatsButton("INT", "Zwiększa bonus do doświadczenia\nWpływa na umiejętności maga", "graphics/inteligence_stat_up_button.png", "graphics/inteligence_stat_up_button_press.png"))

class LabelsContainer(BoxLayout):
    def __init__(self, start, end, **kwargs):
        super(LabelsContainer, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding=[70, 0, 0, dp(40)]
        for x in list(UI.stats.keys())[start:end]:
            self.add_widget(UI.stats[x])

class ValuesContainer(BoxLayout):
    def __init__(self, start, end, **kwargs):
        super(ValuesContainer, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding=[0, 0, 0, dp(40)]
        for x in list(UI.stats.keys())[start:end]:
            self.add_widget(UI.stats[x])

class BaicStatsTop(BoxLayout):
    def __init__(self, **kwargs):
        super(BaicStatsTop, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.add_widget(LabelsContainer(0,1))
        self.add_widget(ValuesContainer(7,8))
class BasicStatsContainer(BoxLayout):
    def __init__(self, **kwargs):
        super(BasicStatsContainer, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.add_widget(LabelsContainer(1,7))
        self.add_widget(ValuesContainer(8,14))
class DetailStatsContainer(BoxLayout):
    def __init__(self, **kwargs):
        super(DetailStatsContainer, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.add_widget(LabelsContainer(14,20))
        self.add_widget(ValuesContainer(20,26))
    
class EXPBar(ProgressBar):
    pass
class StatsComponent(BoxLayout):
    def __init__(self, **kwargs):
        super(StatsComponent, self).__init__(**kwargs)
        self.size_hint = (0.27,0.8)
        self.pos_hint={"center_x": 0.8, "center_y": 0.5}
        self.orientation = "vertical"
        self.padding = 10
        self.canvas.before.clear()
        with self.canvas.before:
            self.rect = Rectangle(
                source = 'graphics/stat_background.png',
                pos = self.pos,
                size = self.size,
            )
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.stats_up = StatsUpButtonContainer()

        self.container = (BoxLayout(orientation = "horizontal", size_hint_y=1))
        self.container.add_widget(BasicStatsContainer(size_hint_y=1, size_hint_x=0.9))
        self.container.add_widget(self.stats_up)

        self.add_widget(BaicStatsTop(size_hint_y=0.25))
        self.add_widget(self.container)
        self.add_widget(DetailStatsContainer(size_hint_y=1))

    def visible(self):
        self.stats_up.opacity = 1
        self.stats_up.disabled = False

    def hidden(self):
        self.stats_up.opacity = 0
        self.stats_up.disabled = True

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def stats_update(self):
        UI.ui.stats_refresh(player.current_player)


stats_component = StatsComponent()


