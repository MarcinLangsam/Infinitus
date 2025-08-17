from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty, StringProperty

class WindowManger(ScreenManager):
    menu = ObjectProperty(None) 
    team = ObjectProperty(None)
    shop = ObjectProperty(None)
    skills = ObjectProperty(None)
    fight = ObjectProperty(None)
    game_over = ObjectProperty(None)
    battle_result = ObjectProperty(None)
    character_creation = ObjectProperty(None)
    add_new_charater = ObjectProperty(None)
    map = ObjectProperty(None)
    main_menu = ObjectProperty(None)
    tutorial = ObjectProperty(None)
    end = ObjectProperty(None)
    settings_menu = ObjectProperty(None)

    def change_screen(self):
        self.current = "team"

screen_manager = WindowManger()