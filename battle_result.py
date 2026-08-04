import player, inventory_manager as im, fight, tooltip as tt, text_pop as tp, os
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.metrics import sp
from components.inventory_component import gold_gain_widget
from components.menu_components import event_dictionary

def save_game():
        tp.text_pop_save_game.text = "Zapisano Grę"
        save_path = os.path.join(os.path.expanduser("~"), "save_game.txt")
        f = open(save_path,"w")
        characters = ["player.main_player","player.companion1","player.companion2"]
        for x in range(0,len(player.team)):
           f.write(characters[x]+'.head = "'+str(player.team[x].head)+'"\n')
           f.write(characters[x]+'.name = "'+str(player.team[x].name)+'"\n')
           f.write(characters[x]+'.lv = '+str(player.team[x].lv)+'\n')
           f.write(characters[x]+'.MAX_HP = '+str(player.team[x].MAX_HP)+'\n')
           f.write(characters[x]+'.MAX_MP = '+str(player.team[x].MAX_MP)+'\n')
           f.write(characters[x]+'.MP_regen_base = '+str(player.team[x].MP_regen_base)+'\n')
           f.write(characters[x]+'.HP = '+str(player.team[x].HP)+'\n')
           f.write(characters[x]+'.MP = '+str(player.team[x].MP)+'\n')
           f.write(characters[x]+'.STR_base = '+str(player.team[x].STR_base)+'\n')
           f.write(characters[x]+'.DEX_base = '+str(player.team[x].DEX_base)+'\n')
           f.write(characters[x]+'.INT_base = '+str(player.team[x].INT_base)+'\n')
           f.write(characters[x]+'.weapon = '+str(player.team[x].weapon)+'\n')
           f.write(characters[x]+'.damage_base = '+str(player.team[x].STR_base+player.team[x].weapon)+'\n')
           f.write(characters[x]+'.defence_base = '+str(player.team[x].defence_base)+'\n')
           f.write(characters[x]+'.crit_chance_base = '+str(player.team[x].DEX*0.01)+'\n')
           f.write(characters[x]+'.dodge_chance_base = '+str(player.team[x].DEX*0.02)+'\n')
           f.write(characters[x]+'.crit_chance_bonus = '+str(player.team[x].crit_chance_bonus)+'\n')
           f.write(characters[x]+'.dodge_chance_bonus = '+str(player.team[x].dodge_chance_bonus)+'\n')
           f.write(characters[x]+'.EXP_boost = '+str(player.team[x].INT*0.01)+'\n')
           f.write(characters[x]+'.EXP = '+str(player.team[x].EXP)+'\n')
           f.write(characters[x]+'.EXP_To_Lv = '+str(player.team[x].EXP_To_Lv)+'\n')
           f.write(characters[x]+'.stat_points = '+str(player.team[x].stat_points)+'\n')
           f.write(characters[x]+'.skill_points = '+str(player.team[x].skill_points)+'\n')
           f.write(characters[x]+'.potions = '+str(player.team[x].potions)+'\n')
           f.write(characters[x]+'.potion_effect = "'+str(player.team[x].potion_effect)+'"\n')
           f.write(characters[x]+'.current_potions = '+str(player.team[x].current_potions)+'\n')
           f.write(characters[x]+'.potion_description = "'+str(player.team[x].potion_description)+'"\n')
           for y in player.team[x].skill:
               temp = str(player.team[x].skill[y][3]).replace("\n","\\n")
               temp2 = str(player.team[x].skill[y][0]).replace("\n","\\n")
               f.write(characters[x]+'.skill["'+y+'"] = ["'+temp2+'",'+str(player.team[x].skill[y][1])+',"'+str(player.team[x].skill[y][2])+'","'+temp+'","'+str(player.team[x].skill[y][4])+'","'+str(player.team[x].skill[y][5])+'","'+str(player.team[x].skill[y][6])+'","'+str(player.team[x].skill[y][7])+'","'+str(player.team[x].skill[y][8])+'"]\n')
           f.write(characters[x]+'.inventory["main_hand"][2] = "'+str(player.team[x].inventory["main_hand"][2])+'"\n')
           f.write(characters[x]+'.inventory["off_hand"][2] = "'+str(player.team[x].inventory["off_hand"][2])+'"\n')
           f.write(characters[x]+'.inventory["armor"][2] = "'+str(player.team[x].inventory["armor"][2])+'"\n')
           f.write(characters[x]+'.inventory["accessory"][2] = "'+str(player.team[x].inventory["accessory"][2])+'"\n')
           f.write(characters[x]+'.inventory["accessory2"][2] = "'+str(player.team[x].inventory["accessory2"][2])+'"\n')
           f.write(characters[x]+'.inventory["accessory3"][2] = "'+str(player.team[x].inventory["accessory3"][2])+'"\n')
           f.write(characters[x]+'.inventory["potion"][2] = "'+str(player.team[x].inventory["potion"][2])+'"\n')
        for x in range(0,48):
            f.write('player.main_player.inventory['+str(x)+'][2] = "'+(player.current_player.inventory[x][2])+'"\n')
        f.write("fight.stage1_progress="+str(fight.stage1_progress)+"\n")
        f.write("fight.stage2_progress="+str(fight.stage2_progress)+"\n")
        f.write("fight.current_fight="+str(fight.current_fight)+"\n")
        f.write("fight.current_stage="+str(fight.current_stage)+"\n")
        if len(player.team)>=2:
            f.write("player.team.append(player.companion1)\n")
        if len(player.team)>=3:
            f.write("player.team.append(player.companion2)\n")
        f.write("player.gold = "+str(player.gold))
        for key in event_dictionary.keys():
            f.write("\nevent_dictionary['"+str(key)+"'] = "+str(event_dictionary[key]))
        for key in player.main_player.story_items.keys():
            f.write("\nplayer.main_player.story_items['"+str(key)+"'][0] = "+str(player.main_player.story_items[key][0]))
        f.close()
        Clock.schedule_once(tp.clear_pop_up,2)

def text_pop_up(t,pos_x,pos_y):
    text_pop = Label(pos=(pos_x,pos_y), text=t, font_size=25, outline_width=1)
    return text_pop

class EXPBar(ProgressBar):
    pass
class Battle_Result(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.exp_bar_player = EXPBar(pos_hint={"center_x": 0.55, "center_y": 0.7}, size_hint_x = 0.16, max=100)
        self.exp_bar_companion_one = EXPBar(pos_hint={"center_x": 0.55, "center_y": 0.5}, size_hint_x = 0.16, max=100) 
        self.exp_bar_companion_two = EXPBar(pos_hint={"center_x": 0.55, "center_y": 0.3}, size_hint_x = 0.16, max=100)
        self.ok1 = False
        self.ok2 = False
        self.ok3 = False
        self.tooltip = tt.Tooltip()
    def change_screen(self):
        self.check_for_lv_up()
        self.clear_widgets()
        self.manager.current = "menu"
    def setup_window(self):
        self.add_widget(Image(source="graphics/team_background.png", size_hint=(1,1), allow_stretch=True, fit_mode="fill"))
        self.add_widget(Button(pos_hint={"center_x": 0.95, "center_y": 0.95}, size=(50,50), size_hint=(None,None), background_normal="graphics/close_button.png", on_press = lambda y:self.change_screen()))
        Clock.schedule_once(self.progress_bar_start)

        if len(player.team) >= 1:
            self.add_widget(Image(source="graphics/sprites/"+player.main_player.head+"_portrait.png", pos_hint={"center_x": 0.42, "center_y": 0.7}))
            self.add_widget(self.exp_bar_player)
        if len(player.team) >= 2:
            self.add_widget(Image(source="graphics/sprites/"+player.companion1.head+"_portrait.png", pos_hint={"center_x": 0.42, "center_y": 0.5}))
            self.add_widget(self.exp_bar_companion_one)
        if len(player.team) >= 3:
            self.add_widget(Image(source="graphics/sprites/"+player.companion2.head+"_portrait.png", pos_hint={"center_x": 0.42, "center_y": 0.3}))
            self.add_widget(self.exp_bar_companion_two)
        self.add_widget(gold_gain_widget)
        self.add_widget(Label(text="EKWIPUNEK", font_size=(sp(50)), pos_hint={"center_x": 0.235, "center_y": 0.9}, outline_width = 1))
        self.add_widget(Label(text="ŁUPY", font_size=(sp(50)), pos_hint={"center_x": 0.75, "center_y": 0.9}, outline_width = 1))
        im.check_whitch_screen(self.manager.current)

        if fight.current_stage == 1 and fight.current_fight == 2:
            self.add_widget(Label(text="ZDOBYTE PRZEDMIOTY FABULARNE", pos_hint={"center_x": 0.76,"center_y": 0.225}, font_size=27, outline_width=1))
            self.add_widget(im.StorySlot(pos_hint={"center_x": 0.7,"center_y": 0.17}, sprite="graphics/teleport1.png", tooltip_text=player.main_player.story_items["teleport1"][3]+"\n\nPrzedmioty fabularne autamtycznie przenoszą się do ekwipunku."))
            self.add_widget(im.StorySlot(pos_hint={"center_x": 0.762,"center_y": 0.17}, sprite="graphics/teleport2.png", tooltip_text=player.main_player.story_items["teleport2"][3]+"\n\nPrzedmioty fabularne autamtycznie przenoszą się do ekwipunku."))
        if fight.current_stage == 2 and fight.current_fight == 10:
            self.add_widget(Label(text="ZDOBYTE PRZEDMIOTY FABULARNE", pos_hint={"center_x": 0.76,"center_y": 0.225}, font_size=27, outline_width=1))
            self.add_widget(im.StorySlot(pos_hint={"center_x": 0.7,"center_y": 0.17}, sprite="graphics/teleport3.png", tooltip_text=player.main_player.story_items["teleport3"][3]+"\n\nPrzedmioty fabularne autamtycznie przenoszą się do ekwipunku."))
                            
        
        for x in range(0,96):
            im.inventory[x] = im.ItemSlot(pos_hint={"x": player.main_player.inventory[x][0], "y": player.main_player.inventory[x][1]}, sprite=(player.main_player.inventory[x][2]))
            
            self.add_widget(im.inventory[x])
        gold_gain_widget.update_gold_gain(fight.gold_gain)
        self.add_widget(self.tooltip)
            
    def progress_bar_start(self, instance): 
        self.ok1 = False
        self.ok2 = False
        self.ok3 = False
        self.exp_bar_player.value = 0
        self.exp_bar_companion_one.value = 0
        self.exp_bar_companion_two.value = 0
        self.exp_bar_player.max = player.main_player.EXP_To_Lv
        self.exp_bar_companion_one.max = player.companion1.EXP_To_Lv
        self.exp_bar_companion_two.max = player.companion2.EXP_To_Lv
        self.start_fill_animation()
    
    def check_for_lv_up(self):
        if player.main_player.EXP >= player.main_player.EXP_To_Lv:
            player.level_up(player.main_player)
        if player.companion1.EXP >= player.companion1.EXP_To_Lv:
            player.level_up(player.companion1)
        if player.companion2.EXP >= player.companion2.EXP_To_Lv:
            player.level_up(player.companion2)
  
    def next(self, dt):
        if self.ok1 == True and self.ok2 == True and self.ok3 == True:

            return False
        
        if self.exp_bar_player.value >= player.main_player.EXP or self.exp_bar_player.value == self.exp_bar_player.max:
            if self.exp_bar_player.value == self.exp_bar_player.max and self.ok1 == False:
                self.ok1 = True
        else:
            self.exp_bar_player.value += 1
            
        if self.exp_bar_companion_one.value >= player.companion1.EXP or self.exp_bar_companion_one.value == self.exp_bar_companion_one.max:
            if self.exp_bar_companion_one.value == self.exp_bar_companion_one.max and self.ok2 == False:
                self.ok2 = True
            pass    
        else:
            self.exp_bar_companion_one.value += 1
            
        if self.exp_bar_companion_two.value >= player.companion2.EXP or self.exp_bar_companion_two.value == self.exp_bar_companion_two.max:
            if self.exp_bar_companion_two.value == self.exp_bar_companion_two.max and self.ok3 == False:
                self.ok3 = True
            pass
        else:
            self.exp_bar_companion_two.value += 1
            
    def start_fill_animation(self):
        Clock.schedule_interval(self.next, 1/100)

    def save_game(self):
        tp.text_pop_save_game.text = "Zapisano Grę"
        save_path = os.path.join(os.path.expanduser("~"), "save_game.txt")
        f = open(save_path,"w")
        characters = ["player.main_player","player.companion1","player.companion2"]
        for x in range(0,len(player.team)):
           f.write(characters[x]+'.head = "'+str(player.team[x].head)+'"\n')
           f.write(characters[x]+'.name = "'+str(player.team[x].name)+'"\n')
           f.write(characters[x]+'.lv = '+str(player.team[x].lv)+'\n')
           f.write(characters[x]+'.MAX_HP = '+str(player.team[x].MAX_HP)+'\n')
           f.write(characters[x]+'.MAX_MP = '+str(player.team[x].MAX_MP)+'\n')
           f.write(characters[x]+'.MP_regen_base = '+str(player.team[x].MP_regen_base)+'\n')
           f.write(characters[x]+'.HP = '+str(player.team[x].HP)+'\n')
           f.write(characters[x]+'.MP = '+str(player.team[x].MP)+'\n')
           f.write(characters[x]+'.STR_base = '+str(player.team[x].STR_base)+'\n')
           f.write(characters[x]+'.DEX_base = '+str(player.team[x].DEX_base)+'\n')
           f.write(characters[x]+'.INT_base = '+str(player.team[x].INT_base)+'\n')
           f.write(characters[x]+'.weapon = '+str(player.team[x].weapon)+'\n')
           f.write(characters[x]+'.damage_base = '+str(player.team[x].STR_base+player.team[x].weapon)+'\n')
           f.write(characters[x]+'.defence_base = '+str(player.team[x].defence_base)+'\n')
           f.write(characters[x]+'.crit_chance_base = '+str(player.team[x].DEX*0.01)+'\n')
           f.write(characters[x]+'.dodge_chance_base = '+str(player.team[x].DEX*0.02)+'\n')
           f.write(characters[x]+'.crit_chance_bonus = '+str(player.team[x].crit_chance_bonus)+'\n')
           f.write(characters[x]+'.dodge_chance_bonus = '+str(player.team[x].dodge_chance_bonus)+'\n')
           f.write(characters[x]+'.EXP_boost = '+str(player.team[x].INT*0.01)+'\n')
           f.write(characters[x]+'.EXP = '+str(player.team[x].EXP)+'\n')
           f.write(characters[x]+'.EXP_To_Lv = '+str(player.team[x].EXP_To_Lv)+'\n')
           f.write(characters[x]+'.stat_points = '+str(player.team[x].stat_points)+'\n')
           f.write(characters[x]+'.skill_points = '+str(player.team[x].skill_points)+'\n')
           f.write(characters[x]+'.potions = '+str(player.team[x].potions)+'\n')
           f.write(characters[x]+'.potion_effect = "'+str(player.team[x].potion_effect)+'"\n')
           f.write(characters[x]+'.current_potions = '+str(player.team[x].current_potions)+'\n')
           f.write(characters[x]+'.potion_description = "'+str(player.team[x].potion_description)+'"\n')
           for y in player.team[x].skill:
               temp = str(player.team[x].skill[y][3]).replace("\n","\\n")
               temp2 = str(player.team[x].skill[y][0]).replace("\n","\\n")
               f.write(characters[x]+'.skill["'+y+'"] = ["'+temp2+'",'+str(player.team[x].skill[y][1])+',"'+str(player.team[x].skill[y][2])+'","'+temp+'","'+str(player.team[x].skill[y][4])+'","'+str(player.team[x].skill[y][5])+'","'+str(player.team[x].skill[y][6])+'","'+str(player.team[x].skill[y][7])+'","'+str(player.team[x].skill[y][8])+'"]\n')
           f.write(characters[x]+'.inventory["main_hand"][2] = "'+str(player.team[x].inventory["main_hand"][2])+'"\n')
           f.write(characters[x]+'.inventory["off_hand"][2] = "'+str(player.team[x].inventory["off_hand"][2])+'"\n')
           f.write(characters[x]+'.inventory["armor"][2] = "'+str(player.team[x].inventory["armor"][2])+'"\n')
           f.write(characters[x]+'.inventory["accessory"][2] = "'+str(player.team[x].inventory["accessory"][2])+'"\n')
           f.write(characters[x]+'.inventory["accessory2"][2] = "'+str(player.team[x].inventory["accessory2"][2])+'"\n')
           f.write(characters[x]+'.inventory["accessory3"][2] = "'+str(player.team[x].inventory["accessory3"][2])+'"\n')
           f.write(characters[x]+'.inventory["potion"][2] = "'+str(player.team[x].inventory["potion"][2])+'"\n')
        for x in range(0,48):
            f.write('player.main_player.inventory['+str(x)+'][2] = "'+(player.current_player.inventory[x][2])+'"\n')
        f.write("fight.stage1_progress="+str(fight.stage1_progress)+"\n")
        f.write("fight.stage2_progress="+str(fight.stage2_progress)+"\n")
        f.write("fight.current_fight="+str(fight.current_fight)+"\n")
        f.write("fight.current_stage="+str(fight.current_stage)+"\n")
        if len(player.team)>=2:
            f.write("player.team.append(player.companion1)\n")
        if len(player.team)>=3:
            f.write("player.team.append(player.companion2)\n")
        f.write("player.gold = "+str(player.gold))
        f.close()
        Clock.schedule_once(tp.clear_pop_up,2)

        