from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from fight import current_stage, current_fight, stage1_progress, stage2_progress

class Map(Screen):
    def switch_stage(self,stage_number):
        current_stage = stage_number
        current_fight = self.get_stage_progress(stage_number)
        self.change_screen("menu")

    def get_stage_progress(self, stage_number):
        if stage_number == 1:
            return stage1_progress
        elif stage_number == 2:
            return stage2_progress
        else:
            return 0

    def change_screen(self,screen):
        self.clear_widgets()
        self.manager.current = screen
    def change_window(self,window_name): #TYMCZASOWE OGARNĄĆ TO
        self.clear_widgets()
        self.manager.current = window_name
    def setup_window(self):
        self.add_widget(Image(source="graphics/plain_background.png", size=(1540,950), pos=(0,0), size_hint=(None,None), allow_stretch=True)) 
        self.add_widget(Button(pos=(1450,800), size=(50,50), size_hint=(None,None), background_normal="graphics/close_button.png", on_press = lambda y:self.change_screen("menu")))

        self.add_widget(Image(source="graphics/menu_background.png", size=(400,100), pos=(600,0), size_hint=(None,None), allow_stretch=True))
        self.add_widget(Button(pos_hint={"center_x": 0.435, "center_y": 0.055}, size_hint=(0.05,0.09), background_normal="graphics/team_button.png", on_press = lambda y:self.change_window("team")))
        self.add_widget(Button(pos_hint={"center_x": 0.5, "center_y": 0.055}, size_hint=(0.05,0.09), background_normal="graphics/skills_button.png", on_press = lambda y:self.change_window("skills")))
        self.add_widget(Button(pos_hint={"center_x": 0.565, "center_y": 0.055}, size_hint=(0.05,0.09), background_normal="graphics/map_button.png", on_press = lambda y:self.change_window("map")))
        
        self.add_widget(Button(pos=(100,100), size=(100,100), on_press = lambda y:self.switch_stage(1)))
        self.add_widget(Button(pos=(100,300), size=(100,100), on_press = lambda y:self.switch_stage(2)))

