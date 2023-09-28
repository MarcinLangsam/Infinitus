import player, enemy, inventory_manager as im, abilities_manager as am, UI_manager as UI, text_pop as tp, random, fight, shop, team, battle_result, skills_window, character_creation, tooltip as tt
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
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
        self.bar = fight.current_fight
        self.text = "Postęp: "+str(int(fight.current_fight))+" / 2"
        self.tooltip = tt.Tooltip()
        self.add_widget(self.tooltip)
        self.add_widget(tt.Tooltip_Button("Sklep",pos=(500,500), size_hint=(0.1,0.133), background_normal="graphics/shop_button.png", on_press = lambda y:self.change_window("shop")))
        
    def start_main_fight(self):
        enemy.enemy_team.clear()
        fight.is_random_fight = False
        for x in range(0,len(enemy.story_fight[fight.current_stage][fight.current_fight])):
            enemy.enemy_team.append(enemy.story_fight[fight.current_stage][fight.current_fight][x])
        self.manager.current = "fight"
    def start_random_fight(self):
        enemy.enemy_team.clear()
        fight.is_random_fight = True
        roll_fight = random.randint(1,fight.current_fight)
        for x in range(0,len(enemy.story_fight[fight.current_stage][roll_fight])):
            enemy.enemy_team.append(enemy.story_fight[fight.current_stage][roll_fight][x])
        self.manager.current = "fight"
    def save_game(self):
        f = open("save_game.txt","w")
        characters = ["player.main_player","player.companion1","player.companion2"]
        for x in range(0,len(player.team)):
           f.write(characters[x]+'.name = "'+str(player.team[x].name)+'"\n')
           f.write(characters[x]+'.lv = '+str(player.team[x].lv)+'\n')
           f.write(characters[x]+'.MAX_HP = '+str(player.team[x].MAX_HP)+'\n')
           f.write(characters[x]+'.MAX_MP = '+str(player.team[x].MAX_MP)+'\n')
           f.write(characters[x]+'.HP = '+str(player.team[x].HP)+'\n')
           f.write(characters[x]+'.MP = '+str(player.team[x].MP)+'\n')
           f.write(characters[x]+'.STR = '+str(player.team[x].STR)+'\n')
           f.write(characters[x]+'.DEX = '+str(player.team[x].DEX)+'\n')
           f.write(characters[x]+'.INT = '+str(player.team[x].INT)+'\n')
           f.write(characters[x]+'.weapon = '+str(player.team[x].weapon)+'\n')
           f.write(characters[x]+'.damage = '+str(player.team[x].STR+player.team[x].weapon)+'\n')
           f.write(characters[x]+'.defence = '+str(player.team[x].defence)+'\n')
           f.write(characters[x]+'.crit_chance = '+str(player.team[x].DEX*0.01)+'\n')
           f.write(characters[x]+'.dodge_chance = '+str(player.team[x].DEX*0.02)+'\n')
           f.write(characters[x]+'.EXP_boost = '+str(player.team[x].INT*0.01)+'\n')
           f.write(characters[x]+'.EXP = '+str(player.team[x].EXP)+'\n')
           f.write(characters[x]+'.EXP_To_Lv = '+str(player.team[x].EXP_To_Lv)+'\n')
           f.write(characters[x]+'.stat_points = '+str(player.team[x].stat_points)+'\n')
           f.write(characters[x]+'.skill_points = '+str(player.team[x].skill_points)+'\n')
           for y in player.team[x].skill:
               temp = str(player.team[x].skill[y][3]).replace("\n","\\n")
               temp2 = str(player.team[x].skill[y][0]).replace("\n","\\n")
               f.write(characters[x]+'.skill["'+y+'"] = ["'+temp2+'",'+str(player.team[x].skill[y][1])+',"'+str(player.team[x].skill[y][2])+'","'+temp+'","'+str(player.team[x].skill[y][4])+'","'+str(player.team[x].skill[y][5])+'","'+str(player.team[x].skill[y][6])+'"]\n')
           f.write(characters[x]+'.inventory["main_hand"][2] = "'+str(player.team[x].inventory["main_hand"][2])+'"\n')
           f.write(characters[x]+'.inventory["off_hand"][2] = "'+str(player.team[x].inventory["off_hand"][2])+'"\n')
           f.write(characters[x]+'.inventory["armor"][2] = "'+str(player.team[x].inventory["armor"][2])+'"\n')
           f.write(characters[x]+'.inventory["accessory"][2] = "'+str(player.team[x].inventory["accessory"][2])+'"\n')
        for x in range(0,40):
            f.write('player.main_player.inventory['+str(x)+'][2] = "'+(player.current_player.inventory[x][2])+'"\n')
        f.write("fight.current_fight="+str(fight.current_fight)+"\n")
        f.write("fight.current_stage="+str(fight.current_stage))
        f.close()
        Clock.schedule_once(tp.clear_pop_up,2)

        
class Game_Over(Screen):
    pass
class End(Screen):
    pass
class Main_Menu(Screen):
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
    main_menu = ObjectProperty(None)
    tutorial = ObjectProperty(None)
    end = ObjectProperty(None)

screen_manager = WindowManger()
kv = Builder.load_file("mymain.kv")
Window.fullscreen = "auto"


class MyMainApp(App):
    def build(self):
        return kv
    
if __name__ == "__main__":
    MyMainApp().run()
