
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.image import Image

class Map(Screen):
    def change_screen(self,screen):
        self.clear_widgets()
        self.manager.current = screen
    def setup_window(self):
        self.add_widget(Image(source="graphics/plain_background.png", size=(1540,950), pos=(0,0), size_hint=(None,None), allow_stretch=True)) 
        self.add_widget(Button(pos=(1450,800), size=(50,50), size_hint=(None,None), background_normal="graphics/close_button.png", on_press = lambda y:self.change_screen("menu")))
