import player, abilities_manager as am, UI_manager as UI, text_pop as tp, tooltip as tt
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader

class Switch_Character_Button(Button):
     pass
class Skills_Window(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.main_player_button = Button(pos=(140,15), size_hint=(0.065,0.13), background_normal="graphics/sprites/"+player.main_player.head+"_portrait.png", on_press = lambda y:self.change_character_menu(player.main_player))
        self.companion1_button = Button(pos=(280,15), size_hint=(0.065,0.13), background_normal="graphics/sprites/"+player.companion1.head+"_portrait.png", on_press = lambda y:self.change_character_menu(player.companion1))
        self.companion2_button = Button(pos=(410,15), size_hint=(0.065,0.13), background_normal="graphics/sprites/"+player.companion2.head+"_portrait.png", on_press = lambda y:self.change_character_menu(player.companion2))
        self.current_button = self.main_player_button
        self.tooltip = tt.Tooltip()
        self.accept_sound = SoundLoader.load("graphics/sounds/accpet.wav")

    def change_screen(self):
        self.accept_sound.play()
        self.change_character_menu(player.main_player)
        self.clear_widgets()
        self.manager.current = "menu"
    def change_window(self,window_name): #TYMCZASOWE OGARNĄĆ TO
        self.accept_sound.play()
        self.change_character_menu(player.main_player)
        self.clear_widgets()
        self.manager.current = window_name

    def setup_window(self):
        self.add_widget(Image(source="graphics/skills_background.png", size=(1540,950), pos=(0,0), size_hint=(None,None), allow_stretch=True))
        self.add_widget(Image(source="graphics/menu_background.png", size=(400,100), pos=(600,0), size_hint=(None,None), allow_stretch=True))
        self.add_widget(Button(pos=(660,10), size_hint=(0.05,0.09), background_normal="graphics/team_button.png", on_press = lambda y:self.change_window("team")))
        self.add_widget(Button(pos=(760,10), size_hint=(0.05,0.09), background_normal="graphics/skills_button.png", on_press = lambda y:self.change_window("skills")))
        self.add_widget(Button(pos=(860,10), size_hint=(0.05,0.09), background_normal="graphics/map_button.png", on_press = lambda y:self.change_window("map")))
        self.add_widget(Image(source="graphics/menu_background.png", size=(550,100), pos=(1010,15), size_hint=(None,None), allow_stretch=True)) #skill points widget
        self.add_widget(Image(source="graphics/main_fight_button.png", size=(60,60), pos=(1130,35), size_hint=(None,None), allow_stretch=True))


        self.main_player_button.background_normal ="graphics/sprites/"+player.main_player.head+"_portrait.png"
        self.companion1_button.background_normal ="graphics/sprites/"+player.companion1.head+"_portrait.png"
        self.companion2_button.background_normal ="graphics/sprites/"+player.companion2.head+"_portrait.png"


        UI.ui.skill_points_refresh(player.current_player)
        self.add_widget(UI.stats["skill_points"])
        self.add_widget(tp.text_pop)

        if len(player.team) >= 1:
            self.main_player_button.background_color = (0.4,0.4,0.4,1)
            self.add_widget(self.main_player_button)
        if len(player.team) >= 2:
            self.companion1_button.background_color = (0.4,0.4,0.4,1)
            self.add_widget(self.companion1_button)
        if len(player.team) >= 3:
            self.companion2_button.background_color = (0.4,0.4,0.4,1)
            self.add_widget(self.companion2_button)
            
        self.current_button.background_color = (1,1,1,1)
            
        self.add_widget(Button(pos=(1450,800), size=(50,50), size_hint=(None,None), background_normal="graphics/close_button.png", on_press = lambda y:self.change_screen()))
    
        for x in list(am.skills.skill_list.keys()):
            if am.skills.skill_list[x][6] == "none":
                pass
            else:
                self.add_widget(am.Skill_line(points=([am.skills.skill_list[x][4]+25,am.skills.skill_list[x][5]+25,am.skills.skill_list[am.skills.skill_list[x][6]][4]+25,am.skills.skill_list[am.skills.skill_list[x][6]][5]+25])))
    
        for x in am.skills.skill_list.keys():
            if am.skills.skill_list[x][0] in player.current_player.skill:
                am.skills_objects[x] = am.SkillSlot(pos=(am.skills.skill_list[x][4],am.skills.skill_list[x][5]), sprite=(am.skills.skill_list[x][7]))
                self.add_widget(am.skills_objects[x])
            else:
                am.skills_objects[x] = am.SkillSlot(pos=(am.skills.skill_list[x][4],am.skills.skill_list[x][5]), sprite=(am.skills.skill_list[x][3]))
                self.add_widget(am.skills_objects[x])

        
        self.add_widget(self.tooltip)
        

    def change_character_menu(self,character):
        self.clear_widgets()
        player.current_player = character
        if character == player.main_player:
            self.current_button = self.main_player_button
        if character == player.companion1:
            self.current_button = self.companion1_button
        if character == player.companion2:
            self.current_button = self.companion2_button
        UI.ui.skill_points_refresh(character)
        self.setup_window()
