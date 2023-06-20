import player, abilities_manager as am, UI_manager as UI, text_pop as tp, tooltip as tt
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

class Switch_Character_Button(Button):
     pass
class Skills_Window(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.main_player_button = Switch_Character_Button(text=player.team[0].name, pos=(500,800), on_press = lambda y:self.change_character_menu(player.main_player))
        self.companion1_button = Switch_Character_Button(text=player.team[1].name, pos=(680,800), on_press = lambda y:self.change_character_menu(player.companion1))
        self.companion2_button = Switch_Character_Button(text=player.team[2].name,  pos=(860,800), on_press = lambda y:self.change_character_menu(player.companion2))
        self.current_button = self.main_player_button


    def change_screen(self):
        self.clear_widgets()
        self.manager.current = "menu"
    def setup_window(self):
        self.add_widget(Image(source="graphics/skills_background.png", size=(1540,950), pos=(0,0), size_hint=(None,None), allow_stretch=True))
        UI.ui.skill_points_refresh(player.current_player)
        self.add_widget(UI.stats["skill_points"])
        self.add_widget(tp.text_pop)

        if len(player.team) >= 1:
                self.main_player_button.background_color = (1,1,1,1)
                self.add_widget(self.main_player_button)
        if len(player.team) >= 2:
                self.companion1_button.background_color = (1,1,1,1)
                self.add_widget(self.companion1_button)
        if len(player.team) >= 3 :
                self.companion2_button.background_color = (1,1,1,1)
                self.add_widget(self.companion2_button)

        self.current_button.background_color = (0,1,0,1)
            
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

        self.add_widget(tt.tooltip)
        

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
