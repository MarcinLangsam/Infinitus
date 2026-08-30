import os
import player, enemy, abilities_manager as am, random, fight, shop, team, battle_result, skills_window, character_creation, map, add_new_character, music_player as mp
import components.hover_behavior
from components.hover_behavior import HoverButton
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('kivy', 'exit_on_escape', '0')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar
from kivy.metrics import dp
from resource_path import get_resource_path
from components.bottom_menu import BottomMenu
from components.menu_components import DynamicStageButton, Settings_Menu, event_companion1, event_companion2, event_dictionary
from kivy.uix.button import Button
from kivy.uix.image import Image
from music_player import music_player
from kivy.uix.label import Label
from kivy.animation import Animation

class StageProgressBar(ProgressBar):
    pass
class Menu(Screen):
    bar = ObjectProperty(None)
    stage_background = StringProperty("graphics/stage1_background.png")
    current_shop = ObjectProperty([0.12,0.48])
    current_random_fight = ObjectProperty([0.29,0.6])
    current_main_fight = ObjectProperty([0.82,0.66])
                        #shop -> random fight -> main fight
    button_placment = [[[0.115,0.48],[0.29,0.6],[0.82,0.66]],[[0.1,0.7],[0.08,0.22],[0.9,0.62]],[[0.695,0.7],[0.47,0.75],[0.3,0.75]]]
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.setting_menu = Settings_Menu(self.manager, pos_hint={"center_x": 0.87, "center_y": 0.25}, size_hint=(0.175, 0.25))
        self.settings_button = Button(pos_hint={"center_x": 0.9, "center_y": 0.055}, size_hint=(0.04,0.07), background_normal="graphics/setting_button.png", background_down="graphics/setting_button_press.png", on_release = lambda y:self.toggle_visibility())
        music_player.music_component.opacity = 0
        music_player.music_component.disabled = True
        self.save_game_label = Label(text="ZAPISANO GRE", font_size=dp(35), outline_width = 1, opacity = 0, pos_hint={"center_x": 0.5, "center_y": 0.75})
        self.anim = (
            Animation(opacity=1, duration=0.4) +
            Animation(duration=2.0) +
            Animation(opacity=0, duration=0.5)
        )
        self.fight_flag_for_save = False

    def show_message(self):
        if self.fight_flag_for_save == True:
            self.save_game_label.opacity = 0
            self.anim.start(self.save_game_label)
            self.fight_flag_for_save = False
        else:
            pass


    def toggle_visibility(self):
        self.setting_menu.is_visible = not self.setting_menu.is_visible
        
        if self.setting_menu.is_visible:
            self.setting_menu.opacity = 1
            self.setting_menu.disabled = False
            music_player.music_component.opacity = 1
            music_player.music_component.disabled = False
        else:
            self.setting_menu.opacity = 0
            self.setting_menu.disabled = True
            music_player.music_component.opacity = 0
            music_player.music_component.disabled = True


    def change_window(self,window_name):
        self.clear_widgets()
        self.manager.current = window_name

    def get_stage_background(self):
        if fight.current_stage == 1:
            return "graphics/stage1_background.png"
        elif fight.current_stage == 2:
            return "graphics/stage2_background.png"
        elif fight.current_stage == 3:
            return "graphics/stage3_background.png"
        else:
            return "graphics/stage1_background.png"
        
    def event_add_character(self):
        self.change_window("add_new_character")

    def add_events(self):
        if event_dictionary["companion1"] == 0 and fight.current_stage == event_companion1.which_stage and fight.current_fight >= event_companion1.which_fight:
            self.add_widget(event_companion1)
        if event_dictionary["companion2"] == 0 and fight.current_stage == event_companion2.which_stage and fight.current_fight >= event_companion2.which_fight:
            self.add_widget(event_companion2)

    def setup_window(self):
        self.stage_background = self.get_stage_background()
        self.current_shop = self.button_placment[fight.current_stage-1][0]
        self.current_random_fight = self.button_placment[fight.current_stage-1][1]
        self.current_main_fight = self.button_placment[fight.current_stage-1][2]
        mp.music_player.change_music("graphics/music/stage1.wav")
        self.bar = fight.current_fight

        self.add_widget(Image(source=self.stage_background, size_hint=(1,1), allow_stretch=True, fit_mode="fill"))
        self.add_widget(StageProgressBar(max=10,value=self.bar))
        self.add_widget(BottomMenu(self.manager, pos_hint={"center_x": 0.5, "y": 0}))
        #self.add_widget(Settings_Menu(self.manager, pos_hint={"center_x": 0.87, "center_y": 0.25}, size_hint=(0.175, 0.25)))
        self.add_widget(self.setting_menu)
        self.add_widget(self.settings_button)
        #self.add_widget(Button(pos_hint={"center_x": 0.9, "center_y": 0.055}, size=(dp(60),dp(60)), size_hint=(None,None), background_normal="graphics/setting_button.png", background_down="graphics/setting_button_press.png", on_release = lambda y:self.change_window("settings_menu")))
        self.add_widget(DynamicStageButton(self.current_shop[0],self.current_shop[1],"graphics/shop_button.png", "graphics/shop_button_press.png", on_release = lambda y:self.change_window("shop")))
        self.add_widget(DynamicStageButton(self.current_random_fight[0],self.current_random_fight[1],"graphics/random_fight_button.png", "graphics/random_fight_button_press.png", on_release = lambda y:self.start_random_fight()))
        self.add_widget(DynamicStageButton(self.current_main_fight[0],self.current_main_fight[1],"graphics/main_fight_button.png", "graphics/main_fight_button_press.png", on_release = lambda y:self.start_main_fight()))
        self.add_widget(music_player.music_component)
        self.save_game_label.opacity = 0
        self.add_widget(self.save_game_label)
        self.add_events()
        
    def start_main_fight(self):
        self.fight_flag_for_save = True
        enemy.enemy_team.clear()
        enemy.player_team_alive = player.team
        fight.is_random_fight = False
        for x in range(0,len(enemy.story_fight[fight.current_stage][fight.current_fight][0])):
            enemy.enemy_team.append(enemy.story_fight[fight.current_stage][fight.current_fight][0][x])
        self.clear_widgets()
        self.manager.current = "fight"

    def start_random_fight(self):
        self.fight_flag_for_save = True
        enemy.enemy_team.clear()
        enemy.player_team_alive = player.team
        fight.is_random_fight = True

        roll_fight = random.randint(1,fight.current_fight)
        while enemy.story_fight[fight.current_stage][roll_fight][1] != "normal":
            roll_fight = random.randint(1,fight.current_fight)

        for x in range(0,len(enemy.story_fight[fight.current_stage][roll_fight][0])):
            enemy.enemy_team.append(enemy.story_fight[fight.current_stage][roll_fight][0][x])
        self.clear_widgets()
        self.manager.current = "fight"


class Game_Complete(Screen):
    pass   
class Game_Over(Screen):
    pass
class End(Screen):
    pass
class Main_Menu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        mp.music_player.play_music()

    def load_game(self):
        player.main_player.hard_reset_player()
        player.companion1.hard_reset_player()
        player.companion2.hard_reset_player()
        player.team.clear()
        player.team.append(player.main_player)
        try:
            save_path = os.path.join(os.path.expanduser("~"), "save_game.txt")
            f = open(save_path)
        except Exception as e:
            print(f"Błąd podczas odczytu pliku")
            return None
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
        Do obsługi gry jest wymagana tylko myszka, masz dostęp do jednego slotu zapisu swojego progresu. 
        Z ekranu zaprezentowanego poniżej możesz podjąć kolejną walkę i zarządzać swoją drużyną. 
        Aby sprawdzić pomoc do reszty mechanik kliknij na jeden z rozdziałów wyżej.
        """
        self.ids.help_image.source = "graphics/help_start.png"
    def creation(self):
        self.ids.help_text.text = """
        Podczas twożenia postaci możesz wybrać jej imię, twarz oraz klasę. 
        Klasy maja unikatowe bonusy do statystyk ale determinują tylko startową broń i umiejętność.
        Każda klasa może nauczyzć sie wszystkich umiejętności i nosić dowolny ekwipunek. 
        Wraz z progresem walk możesz zdobyć do 3 członków drużyny.
        """
        self.ids.help_image.source = "graphics/help_creation.png"
    def inventory(self):
        self.ids.help_text.text = """
        W ekranie ekwipunku możesz wyposażać swoją drużynę w zdobyte przedmioty, wystarczy przeciągnąć myszką na odpowiedni slot, 
        najedź na przedmiot myszką, aby sprawdzić jego właściwości.
        Tutaj możesz też sprawdzić statystyki swoich bohaterów oraz rozdawać punkty statystyk po awansie.
        Przeciagaj przedmioty na ikone śmietnika aby je zniszczć.
        """
        self.ids.help_image.source = "graphics/help_inventory.png"
    def shop(self):
        self.ids.help_text.text = """
        W ekranie sklepu możesz kupować oraz sprzedawać przedmioty. 
        Przeciągaj przedmioty ze sklepu do ekwipunku, aby coś kupić oraz vice versa, aby coś sprzedać. 
        O wartości sprzedaży bądź kupna dowiesz się najeżdżając na przedmiot myszką.
        """
        self.ids.help_image.source = "graphics/help_shop.png"
    def progress(self):
        self.ids.help_text.text = """
        W tym ekranie możesz uczyć swoich bohaterów nowych umiejętności, wystarczy na nie kliknąć, najedź na nie myszą, aby zobaczyć opis umiejętności. 
        Drzewko zaczyna się od dołu, nie można wybrać umiejętności bez posiadania poprzednich z drzewka.
        Walcząc zdobywasz punkty doświadczenia, a awansując zyskujesz 1 punkt umiejętności oraz 5 punktów statystyk.
        Ikony na szaro to umiejętności nie wyuczone natomiast w żółtej ramcte to te już znane.
        Każda klasa może się nauczyć każdej umiejetności i każda kosztuje 1 punkt.
        """
        self.ids.help_image.source = "graphics/help_progress.png"
    def fight(self):
        self.ids.help_text.text = """
        Walka odbywa się turowo, kolejka tur jest zależna od statystyki zręczności. 
        Po każdej walce zdobywasz złoto oraz doświadczenie jest również procentowa szansa na zdobycie łupów w postaci przedmiotów, 
        aby je zachować przeciągnij je do swojego ekwipunku.
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
