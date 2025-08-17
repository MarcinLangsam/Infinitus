import os
import player, enemy, abilities_manager as am, random, fight, shop, team, battle_result, skills_window, character_creation, map, settings_menu, add_new_character, music_player as mp
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.metrics import dp
from resource_path import get_resource_path
from components.bottom_menu import BottomMenu
from components.menu_components import DynamicStageButton

class StageProgressBar(ProgressBar):
    pass
class Menu(Screen):
    bar = ObjectProperty(None)
    stage_background = StringProperty("graphics/stage1_background.png")
    current_shop = ObjectProperty([0.12,0.4])
    current_random_fight = ObjectProperty([0.29,0.6])
    current_main_fight = ObjectProperty([0.82,0.66])
                        #shop -> random fight -> main fight
    button_placment = [[[0.12,0.4],[0.29,0.6],[0.82,0.66]],[[0.1,0.7],[0.08,0.22],[0.9,0.62]]]
    

    def __init__(self, **kw):
        super().__init__(**kw)
        self.setup_window()

    def change_window(self,window_name):
        self.manager.current = window_name

    def get_stage_background(self):
        if fight.current_stage == 1:
            return "graphics/stage1_background.png"
        elif fight.current_stage == 2:
            return "graphics/stage2_background.png"
        else:
            return "graphics/stage1_background.png"

    def setup_window(self):
        self.stage_background = self.get_stage_background()
        self.current_shop = self.button_placment[fight.current_stage-1][0]
        self.current_random_fight = self.button_placment[fight.current_stage-1][1]
        self.current_main_fight = self.button_placment[fight.current_stage-1][2]
        mp.music_player.change_music("graphics/music/stage1.wav")
        self.bar = fight.current_fight
        
        self.add_widget(BottomMenu(self.manager, pos_hint={"center_x": 0.5, "y": 0}))
        self.add_widget(Button(pos_hint={"center_x": 0.9, "center_y": 0.055}, size=(dp(60),dp(60)), size_hint=(None,None), border=(0,0,0,0),  background_normal="graphics/setting_button.png", on_press = lambda y:self.change_window("settings_menu")))
        self.add_widget(DynamicStageButton(self.current_shop[0],self.current_shop[1],"graphics/shop_button.png", on_press = lambda y:self.change_window("shop")))
        self.add_widget(DynamicStageButton(self.current_random_fight[0],self.current_random_fight[1],"graphics/random_fight_button.png", on_press = lambda y:self.start_random_fight()))
        self.add_widget(DynamicStageButton(self.current_main_fight[0],self.current_main_fight[1],"graphics/main_fight_button.png", on_press = lambda y:self.start_main_fight()))
    
    def start_main_fight(self):
        enemy.enemy_team.clear()
        fight.is_random_fight = False
        for x in range(0,len(enemy.story_fight[fight.current_stage][fight.current_fight][0])):
            enemy.enemy_team.append(enemy.story_fight[fight.current_stage][fight.current_fight][0][x])
        self.manager.current = "fight"

    def start_random_fight(self):
        enemy.enemy_team.clear()
        fight.is_random_fight = True

        roll_fight = random.randint(1,fight.current_fight)
        while enemy.story_fight[fight.current_stage][roll_fight][1] != "normal":
            roll_fight = random.randint(1,fight.current_fight)

        for x in range(0,len(enemy.story_fight[fight.current_stage][roll_fight][0])):
            enemy.enemy_team.append(enemy.story_fight[fight.current_stage][roll_fight][0][x])
        self.manager.current = "fight"
        
class Game_Over(Screen):
    pass
class End(Screen):
    pass
class Main_Menu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        mp.music_player.play_music()

    def load_game(self):
        save_path = os.path.join(os.path.expanduser("~"), "save_game.txt")
        if not os.path.exists(save_path):
            save_path = "save_game.txt"
        f = open(save_path)
        while True: 
            line = f.readline()
            if not line:
                break
            exec(line.strip())
        f.close()
        self.manager.current = "menu"

class Tutorial(Screen):
    def start(self):
        self.ids.help_text.text = """
        Witaj w 'NIESKOŃCZONYM LOCHU', twoim celem jest odkrycie głęboko ukrytej tajemnicy tego miejsca. 
        Ulepszaj swoich bohaterów, zdobywaj coraz lepsze wyposażenie, aby pokonywać trudniejsze wyzwania. 
        Do obsługi gry jest wymagana tylko myszka, masz dostęp tylko do jednego slotu zapisu swojego progresu. 
        Z tego ekranu możesz podjąć kolejną walkę i zarządzać swoją drużyną. 
        Aby sprawdzić pomoc do reszty mechanik po prostu kliknij na jeden z rozdziałów wyżej.
        """
        self.ids.help_image.source = "graphics/help_start.png"
    def inventory_shop(self):
        self.ids.help_text.text = """
        W ekranie ekwipunku możesz wyposażać swoją drużynę w zdobyte przedmioty, wystarczy przeciągnąć myszką na odpowiedni slot, najedź na przedmiot myszką, aby sprawdzić jego właściwości.
        Tutaj możesz też sprawdzić statystyki swoich bohaterów. 
        W ekranie sklepu możesz kupować oraz sprzedawać przedmioty. 
        Przeciągaj przedmioty ze sklepu do ekwipunku, aby coś kupić oraz vice versa, aby coś sprzedać. 
        O wartości sprzedaży bądź kupna dowiesz się najeżdżając na przedmiot myszką.
        """
        self.ids.help_image.source = "graphics/help_inventory.png"
    def progress(self):
        self.ids.help_text.text = """
        W tym ekranie możesz uczyć swoich bohaterów nowych umiejętności, wystarczy na nie kliknąć, najedź na nie myszą, aby zobaczyć opis umiejętności. 
        Rozwijanie zaczyna się od dołu, nie można wybrać umiejętności bez posiadania poprzednich z drzewka.
        W ekranie ekwipunku możesz również zwiększać statystyki bohaterów. 
        Walcząc zdobywasz punkty doświadczenia, a awansując zyskujesz 1 punkt umiejętności oraz 5 punktów statystyk.
        """
        self.ids.help_image.source = "graphics/help_progress.png"
    def fight(self):
        self.ids.help_text.text = """
        Walka odbywa się turowo, kolejka tur jest zależna od statystyki zręczności. 
        Po każdej walce zdobywasz złoto oraz doświadczenie jest również  procentowa szansa na zdobycie łupów w postaci przedmiotów, aby je zachować przeciągnij je do swojego ekwipunku.
        """
        self.ids.help_image.source = "graphics/help_fight.png"


kivy_file = get_resource_path("mymain.kv")
kv = Builder.load_file(kivy_file)
Window.fullscreen = "auto"


class MyMainApp(App):
    def exit_app(self):
        self.stop()

    def build(self):
        return kv
    
if __name__ == "__main__":
    MyMainApp().run()
