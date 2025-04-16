from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.image import Image

class Map(Screen):
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
        self.add_widget(Button(pos=(660,10), size_hint=(0.05,0.09), background_normal="graphics/team_button.png", on_press = lambda y:self.change_window("team")))
        self.add_widget(Button(pos=(760,10), size_hint=(0.05,0.09), background_normal="graphics/skills_button.png", on_press = lambda y:self.change_window("skills")))
        self.add_widget(Button(pos=(860,10), size_hint=(0.05,0.09), background_normal="graphics/map_button.png", on_press = lambda y:self.change_window("map")))
        