from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
import fight
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from player import main_player

class StageButton(Button):
    def __init__(self, stage, **kwargs):
        super().__init__(**kwargs)
        self.stage = stage
        self.key = "teleport"+str(stage)
        if main_player.story_items[self.key][0] == 0:
            self.background_normal = "graphics/stage"+str(stage)+"_background_locked.png"
        else:
            self.background_normal = "graphics/stage"+str(stage)+"_background.png"
        self.background_down = "graphics/stage"+str(stage)+"_background_locked.png"

class StagesBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spacing = 25
        self.size_hint=(1,0.5)
        self.padding = 30

class Map(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.stages_box = StagesBox(pos_hint={"x": 0, "center_y": 0.5})

    def switch_stage(self,stage_number):
        fight.current_stage = stage_number
        fight.current_fight = self.get_stage_progress(stage_number)
        self.stages_box.clear_widgets()
        self.clear_widgets()
        self.change_screen("menu")

    def get_stage_progress(self, stage_number):
        if stage_number == 1:
            return fight.stage1_progress
        elif stage_number == 2:
            return fight.stage2_progress
        elif stage_number == 3:
            return fight.stage3_progress
        else:
            return 0

    def change_screen(self,screen):
        self.stages_box.clear_widgets()
        self.clear_widgets()
        self.manager.current = screen
    def setup_window(self):
        self.add_widget(Image(source="graphics/plain_background.png", size_hint=(1,1), allow_stretch=True, fit_mode="fill"))
        self.add_widget(Button(pos_hint={"center_x": 0.95, "center_y": 0.95}, size=(50,50), size_hint=(None,None), background_normal="graphics/close_button.png", background_down="graphics/close_button_press.png", on_release = lambda y:self.change_screen("menu")))
        self.add_widget(Label(text="Kliknij na wybraną mapę aby się tam przenieść", pos_hint={"center_x": 0.5,"center_y": 0.05}, font_size=18))     

        self.add_widget(self.stages_box)
        self.stages_box.add_widget(StageButton(1, on_release = lambda y:self.switch_stage(1)))
        self.stages_box.add_widget(StageButton(2, on_release = lambda y:self.switch_stage(2)))
        self.stages_box.add_widget(StageButton(3, on_release = lambda y:self.switch_stage(3)))
        