import UI_manager as UI, player, tooltip as tt, text_pop as tp
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.audio import SoundLoader

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
        self.add_widget(LabelsContainer(0,6))
        self.add_widget(ValuesContainer(7,13))
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
 

        self.container = (BoxLayout(orientation = "horizontal", size_hint_y=1))
        self.container.add_widget(BasicStatsContainer(size_hint_y=1, size_hint_x=0.9))
        
        #self.add_widget(BaicStatsTop(size_hint_y=0.25))
        self.add_widget(self.container)
        self.add_widget(DetailStatsContainer(size_hint_y=1))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def stats_update(self):
        UI.ui.stats_refresh(player.current_player)


stats_component = StatsComponent()


