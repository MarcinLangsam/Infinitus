import player, inventory_manager as im, UI_manager as UI, abilities_manager as am, text_pop as tp, tooltip as tt
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image

class EXPBar(ProgressBar):
    pass
class Switch_Character_Button(Button):
    pass
class Team(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.main_player_sprite = player.Character_Sprite(player.main_player,pos=(768-90,432-65))
        self.companion1_sprite = player.Character_Sprite(player.companion1,pos=(768-90,432-65))
        self.companion2_sprite = player.Character_Sprite(player.companion2, pos=(768-90,432-65))
        self.current_sprite = self.main_player_sprite
        self.main_player_button = Switch_Character_Button(text=player.team[0].name, pos=(550,800), on_press = lambda y:self.change_character_menu(player.main_player))
        self.companion1_button = Switch_Character_Button(text=player.team[1].name, pos=(730,800), on_press = lambda y:self.change_character_menu(player.companion1))
        self.companion2_button = Switch_Character_Button(text=player.team[2].name,  pos=(910,800), on_press = lambda y:self.change_character_menu(player.companion2))
        self.current_button = self.main_player_button
        self.exp_bar = EXPBar()
        self.tooltip = tt.Tooltip()

    def change_screen(self):
        self.clear_widgets()
        self.manager.current = "menu"
    def setup_window(self):
            self.add_widget(Image(source="graphics/team_background.png", size=(1540,950), pos=(0,0), size_hint=(None,None), allow_stretch=True))
            self.add_widget(Image(source="graphics/stat_background.png", size=(300,2000), pos=(1130,-550), size_hint=(None,None), allow_stretch=True))

            im.inventory["main_hand"] = im.ItemSlot(pos=(player.current_player.inventory["main_hand"][0],player.current_player.inventory["main_hand"][1]), sprite=(player.current_player.inventory["main_hand"][2]))
            im.inventory["off_hand"] = im.ItemSlot(pos=(player.current_player.inventory["off_hand"][0],player.current_player.inventory["off_hand"][1]), sprite=(player.current_player.inventory["off_hand"][2]))
            im.inventory["armor"] = im.ItemSlot(pos=(player.current_player.inventory["armor"][0],player.current_player.inventory["armor"][1]), sprite=(player.current_player.inventory["armor"][2]))
            im.inventory["accessory"] = im.ItemSlot(pos=(player.current_player.inventory["accessory"][0],player.current_player.inventory["accessory"][1]), sprite=(player.current_player.inventory["accessory"][2]))
            self.add_widget(im.inventory["main_hand"])
            self.add_widget(im.inventory["off_hand"])
            self.add_widget(im.inventory["armor"])
            self.add_widget(im.inventory["accessory"])
            for x in range(0,40):
                im.inventory[x] = im.ItemSlot(pos=(player.current_player.inventory[x][0],player.current_player.inventory[x][1]), sprite=(player.current_player.inventory[x][2]))
                self.add_widget(im.inventory[x])

            self.add_widget(Button(pos=(1450,800), size=(50,50), size_hint=(None,None), background_normal="graphics/close_button.png", on_press = lambda y:self.change_screen()))
            
            if len(player.team) >= 1:
                self.main_player_button.background_color = (1,1,1,1)
                self.add_widget(self.main_player_button)
            if len(player.team) >= 2:
                self.companion1_button.background_color = (1,1,1,1)
                self.add_widget(self.companion1_button)
            if len(player.team) >= 3:
                self.companion2_button.background_color = (1,1,1,1)
                self.add_widget(self.companion2_button)
            
            self.current_button.background_color = (0,1,0,1)

            self.exp_bar.value = player.current_player.EXP
            self.exp_bar.max = player.current_player.EXP_To_Lv
            self.exp_bar.pos_hint = {'x':0.745,'y':0.45}
            self.exp_bar.size_hint_x = 0.18
            self.add_widget(self.exp_bar)
            for x in list(UI.stats.keys())[0:-1]:
                UI.stats[x].bind(size=UI.stats[x].setter("text_size"))
                self.add_widget(UI.stats[x])
            self.add_widget(am.Stat_Button("HP",pos=(1380,725)))
            self.add_widget(am.Stat_Button("MP",pos=(1380,680)))
            self.add_widget(am.Stat_Button("STR",pos=(1380,635)))
            self.add_widget(am.Stat_Button("DEX",pos=(1380,595)))
            self.add_widget(am.Stat_Button("INT",pos=(1380,550)))
            
            UI.ui.stats_refresh(player.current_player)
            im.check_whitch_screen(self.manager.current)
            
            self.add_widget(self.current_sprite)
            self.add_widget(tp.text_pop)
            self.add_widget(Label(text="EKWIPUNEK", pos=(-490,415), font_size=40))
            
            

            self.add_widget(Label(text="Broń",font_size=18,pos=(-145,-15)))
            self.add_widget(Label(text="Druga ręka",font_size=18,pos=(120,-15)))
            self.add_widget(Label(text="Pancerz",font_size=18,pos=(-15,140)))
            self.add_widget(Label(text="Akcesoria",font_size=18,pos=(-15,-160)))
            self.add_widget(self.tooltip)
            self.refresh_items()
            
    def change_character_menu(self,character):
        self.clear_widgets()
        UI.ui.stats_refresh(character)
        player.current_player = character
        for x in range(0,40):
            character.inventory[x][2] = im.inventory[x].sprite
        
        if character == player.main_player:
            self.current_sprite = self.main_player_sprite
            self.current_button = self.main_player_button
        if character == player.companion1:
            self.current_sprite = self.companion1_sprite
            self.current_button = self.companion1_button
        if character == player.companion2:
            self.current_sprite = self.companion2_sprite
            self.current_button = self.companion2_button
        
        self.setup_window()
    
    def refresh_items(self):
        self.remove_widget(self.current_sprite)
        self.current_sprite.set_sprite()
        self.current_sprite.set_sprite_weapon()
        self.add_widget(self.current_sprite)
        self.remove_widget(self.tooltip)
        self.add_widget(self.tooltip)
 