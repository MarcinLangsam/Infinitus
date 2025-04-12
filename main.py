import player, enemy, inventory_manager as im, abilities_manager as am, UI_manager as UI, text_pop as tp, random, fight, shop, team, battle_result, skills_window, character_creation, tooltip as tt, map, settings_menu, add_new_character, music_player as mp
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button

class StageProgressBar(ProgressBar):
    pass
class Menu(Screen):
    bar = ObjectProperty(None)
    text = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.setup_window()

    def change_window(self,window_name):
        self.manager.current = window_name

    def setup_window(self):
        mp.music_player.change_music("graphics/music/stage1.wav")
        self.bar = fight.current_fight
        self.text = "Postęp: "+str(int(fight.current_fight))+" / 10"
        self.add_widget(Image(source="graphics/menu_background.png", size=(400,100), pos=(600,0), size_hint=(None,None), allow_stretch=True))
        self.add_widget(Button(pos=(110,350), size_hint=(0.1,0.18), background_normal="graphics/shop_button.png", on_press = lambda y:self.change_window("shop")))
        self.add_widget(Button(pos=(380,510), size_hint=(0.1,0.18), background_normal="graphics/random_fight_button.png", on_press = lambda y:self.start_random_fight()))
        self.add_widget(Button(pos=(1175,540), size_hint=(0.1,0.18), background_normal="graphics/main_fight_button.png", on_press = lambda y:self.start_main_fight()))
        self.add_widget(Button(pos=(660,10), size_hint=(0.05,0.09), background_normal="graphics/team_button.png", on_press = lambda y:self.change_window("team")))
        self.add_widget(Button(pos=(760,10), size_hint=(0.05,0.09), background_normal="graphics/skills_button.png", on_press = lambda y:self.change_window("skills")))
        self.add_widget(Button(pos=(860,10), size_hint=(0.05,0.09), background_normal="graphics/map_button.png", on_press = lambda y:self.change_window("map")))
        self.add_widget(Button(pos=(1350,10), size_hint=(0.05,0.09), background_normal="graphics/setting_button.png", on_press = lambda y:self.change_window("settings_menu")))
        

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

    def exit(self):
        quit()
    def load_game(self):
        f = open("save_game.txt")
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
        Witaj w 'NIESKOŃCZONYM LOCHU', twoim celem jest odkrycie głęboko ukrytej tajemnicy tego miejsca. Ulepszaj swoich bohaterów, zdobywaj coraz lepsze 
        wyposarzenie aby pokonywać trudniejsze wyzwania. Do obsługi gry jest wymagana tylko myszka, masz dostęp tylko do jednego slotu zapisu swojego progressu. 
        Z tego ekranu możesz podjąć kolneją walkę i zarządzać swoją drużyną. Aby sprawdzić pomoc do reszty mechanik po prostu kliknij na jeden z rodziałów wyrzej. 
        """
        self.ids.help_image.source = "graphics/help_start.png"
    def inventory_shop(self):
        self.ids.help_text.text = """
        W ekranie ekwipunku możesz wyposarzać swoją drużynę w zdobyte przemioty, wystarczy przeciągnąć myszką na odpowiedni slot,najedź na przedmiot
        myszką aby sprawdzić jego właściwości, tutaj możesz też sprawdzić statystyki swoich bohaterów. W ekranie sklepu możesz kupiwać oraz sprzedawać
        przedmioty przeciagaj przemioty ze sklepu do ekwipunku aby coś kupić oraz vice versa aby coś sprzedać. O wartośći sprzedarzy bądź kupna dopwiesz
        się najeżdżając na przedmiot myszką.
        """
        self.ids.help_image.source = "graphics/help_inventory.png"
    def progress(self):
        self.ids.help_text.text = """
        W tym ekranie możesz uczyć swoich bohaterów nowych umiejętności, wystraczy na nie kliknąć, najedź na nie myszą aby zobaczyć opis umiejętności. 
        Rozwijanie zaczyna się od dołu, nie można wybrać umiejętności bez posiadania poprzednich z drzewka.
        W ekranie ekwipunku możesz również zwiększać statystyki bohaterów. 
        Walcząć zdobywasz punkty doświadczenia a awansując zyskujesz 1 punkt umijętności oraz 5 punktów statystyk.
        """
        self.ids.help_image.source = "graphics/help_progress.png"
    def fight(self):
        self.ids.help_text.text = """
        Walka odbywa się turowo, kolejka tur jest zależna od statytyki zręczności. Po każdej walce zdobywasz złoto oraz doświadczenie jest również 
        procentowa szansa na zdobycie łupów w postaci przedmiotów, aby je zachować przeciągnij je do swojego ekwipunku.   
        """
        self.ids.help_image.source = "graphics/help_fight.png"
    
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

screen_manager = WindowManger()
kv = Builder.load_file("mymain.kv")
Window.fullscreen = "auto"


class MyMainApp(App):
    def build(self):
        return kv
    
if __name__ == "__main__":
    MyMainApp().run()
