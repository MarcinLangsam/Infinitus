import player, enemy, inventory_manager as im, abilities_manager as am, UI_manager as UI, random
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.uix.label import Label
import time
current_stage = 1
current_fight = 2
gold_gain = 0

class Shop(Screen):
    def change_screen(self):
        self.manager.current = "menu"
    def enter_setup(self):
        self.clear_widgets()
        self.shop_window() 
    def shop_window(self):
        for x in range(0,80):
            im.inventory[x] = im.ItemSlot(pos=(player.main_player.inventory[x][0],player.main_player.inventory[x][1]), sprite=(player.main_player.inventory[x][2]))
            self.add_widget(im.inventory[x])

        self.add_widget(Button(pos=(1450,800), size=(50,50), size_hint=(None,None), on_press = lambda y:self.change_screen()))
        self.add_widget(im.gold_on_screen)
        im.update_gold()
        im.check_whitch_screen(self.manager.current)


class Skills_Window(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def change_screen(self):
        self.manager.current = "menu"
    def enter_setup(self):
        self.clear_widgets()
        self.skills_window()
    def skills_window(self):
        self.add_widget(UI.stats["skill_points"])

        self.add_widget(Button(text=player.team[0].name, size_hint=(0.05,0.05), pos=(600,800), on_press = lambda y:self.change_character_menu(player.team[0])))
        self.add_widget(Button(text=player.team[1].name, size_hint=(0.05,0.05), pos=(700,800), on_press = lambda y:self.change_character_menu(player.team[1])))
        self.add_widget(Button(text=player.team[2].name, size_hint=(0.05,0.05), pos=(800,800), on_press = lambda y:self.change_character_menu(player.team[2])))

        self.add_widget(Button(pos=(1450,800), size=(50,50), size_hint=(None,None), on_press = lambda y:self.change_screen()))
    
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

    def change_character_menu(self,character):
        self.clear_widgets()
        player.current_player = character
        self.add_widget(UI.stats["skill_points"])
        UI.ui.skill_points_refresh(character)
        self.add_widget(Button(text=player.team[0].name, size_hint=(0.05,0.05), pos=(600,800), on_press = lambda y:self.change_character_menu(player.team[0])))
        self.add_widget(Button(text=player.team[1].name, size_hint=(0.05,0.05), pos=(700,800), on_press = lambda y:self.change_character_menu(player.team[1])))
        self.add_widget(Button(text=player.team[2].name, size_hint=(0.05,0.05), pos=(800,800), on_press = lambda y:self.change_character_menu(player.team[2])))

        self.add_widget(Button(pos=(1450,800), size=(50,50), size_hint=(None,None), on_press = lambda y:self.change_screen()))
        
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
        
        
class Team(Screen):    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.current_sprite = player.Main_Player_Sprite(pos=(768-50,432-50), size_hint=(0.1,0.1))
        
    def change_screen(self):
        self.manager.current = "menu"
    def enter_setup(self):
        self.clear_widgets()
        self.team_window() 
    def team_window(self):
            im.inventory["main_hand"] = im.ItemSlot(pos=(player.main_player.inventory["main_hand"][0],player.main_player.inventory["main_hand"][1]), sprite=(player.main_player.inventory["main_hand"][2]))
            im.inventory["off_hand"] = im.ItemSlot(pos=(player.main_player.inventory["off_hand"][0],player.main_player.inventory["off_hand"][1]), sprite=(player.main_player.inventory["off_hand"][2]))
            im.inventory["armor"] = im.ItemSlot(pos=(player.main_player.inventory["armor"][0],player.main_player.inventory["armor"][1]), sprite=(player.main_player.inventory["armor"][2]))
            im.inventory["accessory"] = im.ItemSlot(pos=(player.main_player.inventory["accessory"][0],player.main_player.inventory["accessory"][1]), sprite=(player.main_player.inventory["accessory"][2]))
            self.add_widget(im.inventory["main_hand"])
            self.add_widget(im.inventory["off_hand"])
            self.add_widget(im.inventory["armor"])
            self.add_widget(im.inventory["accessory"])
            for x in range(0,40):
                im.inventory[x] = im.ItemSlot(pos=(player.main_player.inventory[x][0],player.main_player.inventory[x][1]), sprite=(player.main_player.inventory[x][2]))
                self.add_widget(im.inventory[x])

            self.add_widget(Button(pos=(1450,800), size=(50,50), size_hint=(None,None), on_press = lambda y:self.change_screen()))
            
            if len(player.team) >= 1:
                self.add_widget(Button(text=player.team[0].name, size_hint=(0.05,0.05), pos=(600,800), on_press = lambda y:self.change_character_menu(player.main_player)))
            if len(player.team) >= 2:
                self.add_widget(Button(text=player.team[1].name, size_hint=(0.05,0.05), pos=(700,800), on_press = lambda y:self.change_character_menu(player.companion1)))
            if len(player.team) >= 3 :
                self.add_widget(Button(text=player.team[2].name, size_hint=(0.05,0.05), pos=(800,800), on_press = lambda y:self.change_character_menu(player.companion2)))
      
            for x in list(UI.stats.keys())[0:-1]:
                self.add_widget(UI.stats[x])

            self.add_widget(am.Stat_STR_Button(pos=(1380,635)))
            self.add_widget(am.Stat_DEX_Button(pos=(1380,595)))
            self.add_widget(am.Stat_INT_Button(pos=(1380,550)))
            UI.ui.stats_refresh(player.current_player)
            im.check_whitch_screen(self.manager.current)
            
            self.current_sprite.set_sprite("hero_sprite.png")
            self.add_widget(self.current_sprite)

    def change_character_menu(self,character):
        self.clear_widgets()
        self.add_widget(Button(pos=(1450,800), size=(50,50), size_hint=(None,None), on_press = lambda y:self.change_screen()))
        if len(player.team) >= 1:
            self.add_widget(Button(text=player.team[0].name, size_hint=(0.05,0.05), pos=(600,800), on_press = lambda y:self.change_character_menu(player.main_player)))
        if len(player.team) >= 2:
            self.add_widget(Button(text=player.team[1].name, size_hint=(0.05,0.05), pos=(700,800), on_press = lambda y:self.change_character_menu(player.companion1)))
        if len(player.team) >= 3 :
            self.add_widget(Button(text=player.team[2].name, size_hint=(0.05,0.05), pos=(800,800), on_press = lambda y:self.change_character_menu(player.companion2)))
        for x in list(UI.stats.keys())[0:-1]:
                self.add_widget(UI.stats[x])
        UI.ui.stats_refresh(character)
        player.current_player = character
        for x in range(0,40):
            character.inventory[x][2] = im.inventory[x].sprite
        im.inventory["main_hand"] = im.ItemSlot(pos=(player.current_player.inventory["main_hand"][0],player.current_player.inventory["main_hand"][1]), sprite=(player.current_player.inventory["main_hand"][2]))
        im.inventory["off_hand"] = im.ItemSlot(pos=(player.current_player.inventory["off_hand"][0],player.current_player.inventory["off_hand"][1]), sprite=(player.current_player.inventory["off_hand"][2]))
        im.inventory["armor"] = im.ItemSlot(pos=(player.current_player.inventory["armor"][0],player.current_player.inventory["armor"][1]), sprite=(player.current_player.inventory["armor"][2]))
        im.inventory["accessory"] = im.ItemSlot(pos=(player.current_player.inventory["accessory"][0],player.current_player.inventory["accessory"][1]), sprite=(player.current_player.inventory["accessory"][2]))
        self.add_widget(im.inventory["main_hand"])
        self.add_widget(im.inventory["off_hand"])
        self.add_widget(im.inventory["armor"])
        self.add_widget(im.inventory["accessory"])
        for x in range(0,40):
            im.inventory[x] = im.ItemSlot(pos=(character.inventory[x][0],character.inventory[x][1]), sprite=(character.inventory[x][2]))
            self.add_widget(im.inventory[x])
        
        if character == player.main_player:
            self.current_sprite = player.Main_Player_Sprite(pos=(768-50,432-50), size_hint=(0.1,0.1))
            self.current_sprite.set_sprite("hero_sprite.png")
        if character == player.companion1:
            self.current_sprite = player.Companion1_Sprite(pos=(768-50,432-50), size_hint=(0.1,0.1))
            self.current_sprite.set_sprite("hero_move.png")
        if character == player.companion2:
            self.current_sprite = player.Companion2_Sprite(pos=(768-50,432-50), size_hint=(0.1,0.1))
            self.current_sprite.set_sprite("hero_sprite.png")    
        self.add_widget(self.current_sprite)

        self.add_widget(am.Stat_STR_Button(pos=(1380,635)))
        self.add_widget(am.Stat_DEX_Button(pos=(1380,595)))
        self.add_widget(am.Stat_INT_Button(pos=(1380,550)))
        
class Skill_List_Pop_Up(Widget):
    pass
class Fight(Screen):
    hp_bar_player = ObjectProperty(None)
    mp_bar_player = ObjectProperty(None)
    hp_bar_companion_one = ObjectProperty(None)
    mp_bar_companion_one = ObjectProperty(None)
    hp_bar_companion_two = ObjectProperty(None)
    mp_bar_companion_two = ObjectProperty(None) 
    hp_bar_enemy_one = ObjectProperty(None)
    hp_bar_enemy_two = ObjectProperty(None)
    hp_bar_enemy_three = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = player.team[0]
        self.enemy = enemy.enemy_team[0]
        self.player_sprites = list()
        self.enemy_sprites = list()
        self.sprite = enemy.Enemy1_Sprite()
        self.anim_queue = []
        self.turn_order = list()
        self.target_option = {}
        self.turn_number = 0
        self.action = ""
        self.resign_button = Button(text="wróć", size_hint=(0.06,0.06), pos=(900,0), on_press = lambda y:self.resign_action())
        self.enemy_team_alive = list()
        self.battle_end = False
        self.kolejka = Label(pos=(0,0))
        self.moja = Label(pos=(0,100))

    def clear_after_battle(self):
        for x in range(0,len(player.team)):
            self.remove_widget(self.player_sprites[x])
        for x in range(0,len(enemy.enemy_team)):
            self.remove_widget(self.enemy_sprites[x])
        self.remove_widget(self.kolejka)
        self.remove_widget(self.moja)
    def prepare_battle_visuals(self):
        self.player_sprites.clear()
        self.enemy_sprites.clear()
        self.player_sprites.append(player.Main_Player_Sprite())
        self.player_sprites.append(player.Companion1_Sprite())
        self.player_sprites.append(player.Companion2_Sprite())
        self.enemy_sprites.append(enemy.Enemy1_Sprite())
        self.enemy_sprites.append(enemy.Enemy2_Sprite())
        self.enemy_sprites.append(enemy.Enemy3_Sprite())
        self.skill_list_pop_up = Skill_List_Pop_Up()
        self.add_widget(self.kolejka)

        for x in range(0,len(player.team)):
            self.add_widget(self.player_sprites[x])
        for x in range(0,len(enemy.enemy_team)):
            self.add_widget(self.enemy_sprites[x])
            
    def chose_sprite(self,e):
        for x in range(0,len(player.team)):
            if e == player.team[x]:                                           
                sprite = self.player_sprites[x]
        for y in range(0,len(enemy.enemy_team)):
            if e == enemy.enemy_team[y]:
                sprite = self.enemy_sprites[y]
        return sprite
    def chose_enemy_index(self,e):
        for x in range(0,len(player.team)):
            if e == player.team[x]:                                           
                index = x
        for y in range(0,len(enemy.enemy_team)):
            if e == enemy.enemy_team[y]:
                index = y
        return index
        
    def chose_target(self):
        for x in self.target_option:
            self.add_widget(self.target_option[x][0])
    def start_fight_setup(self):
        enemy.player_team_alive = player.team
        for x in range(0,len(enemy.enemy_team)):
            self.enemy_team_alive.append(enemy.enemy_team[x])
        self.battle_end = False
        self.prepare_battle_visuals()
        self.update_status()
        self.create_turn_order()
        self.create_target_option()
        self.take_action(self.turn_order[self.turn_number]) 

    def battle_over(self):
        for x in player.team:
            x.HP = x.MAX_HP
            x.MP = x.MAX_MP
        for x in enemy.enemy_team:
            x.HP = x.MAX_HP
        self.clear_after_battle()
        self.battle_end = True

    def disable_control(self):
        self.ids.attack.disabled = True
        self.ids.spells.disabled = True
    def restore_control(self):
        self.ids.attack.disabled = False
        self.ids.spells.disabled = False
    
    def sort_by(self,e):
        return e.DEX
    def create_turn_order(self):
        self.turn_order.clear()
        for x in range(0,len(player.team)):
            self.turn_order.append(player.team[x])
        for x in range(0,len(enemy.enemy_team)):
            self.turn_order.append(enemy.enemy_team[x])
        self.turn_order.sort(key=self.sort_by)
        self.turn_number = len(self.turn_order)-1

        for x in self.turn_order:
            self.kolejka.text += str(x)
        
    def create_target_option(self):
        if len(enemy.enemy_team) == 1:
            self.target_option[0] = [Button(text=enemy.enemy_team[0].name,size_hint=(0.06,0.06), pos=(570+0*100,60), on_press = lambda y:self.attack(0)),self.chose_sprite(enemy.enemy_team[0]).pos]
        if len(enemy.enemy_team) == 2:
            self.target_option[0] = [Button(text=enemy.enemy_team[0].name,size_hint=(0.06,0.06), pos=(570+0*100,60), on_press = lambda y:self.attack(0)),self.chose_sprite(enemy.enemy_team[0]).pos]
            self.target_option[1] = [Button(text=enemy.enemy_team[1].name,size_hint=(0.06,0.06), pos=(570+1*100,60), on_press = lambda y:self.attack(1)),self.chose_sprite(enemy.enemy_team[1]).pos]
        if len(enemy.enemy_team) == 3:
            self.target_option[0] = [Button(text=enemy.enemy_team[0].name,size_hint=(0.06,0.06), pos=(570+0*100,60), on_press = lambda y:self.attack(0)),self.chose_sprite(enemy.enemy_team[0]).pos]
            self.target_option[1] = [Button(text=enemy.enemy_team[1].name,size_hint=(0.06,0.06), pos=(570+1*100,60), on_press = lambda y:self.attack(1)),self.chose_sprite(enemy.enemy_team[1]).pos]
            self.target_option[2] = [Button(text=enemy.enemy_team[2].name,size_hint=(0.06,0.06), pos=(570+2*100,60), on_press = lambda y:self.attack(2)),self.chose_sprite(enemy.enemy_team[2]).pos]
    def animation(self,dt):
        self.sprite.time += dt
        if (self.sprite.time > self.sprite.rate):
                self.sprite.time -= self.sprite.rate
                self.sprite.sprite = "atlas://"+self.sprite.source+"/frame" + str(self.sprite.frame)
                self.sprite.frame = self.sprite.frame + 1
                if (self.sprite.frame > self.sprite.frame_sum):
                    self.sprite.frame = 1
                    self.run_animation()
                    return False
    def create_movement_animation(self, widget,x_pos, y_pos):
        self.anim_queue.append((widget, Animation(x=x_pos, y=y_pos)))
    def animation_complete(self):
        self.update_status()
        self.check_for_death()
        Clock.schedule_interval(self.animation,0.3)
    def run_animation(self):
        if len(self.anim_queue)>0:
            w, a = self.anim_queue.pop(0)
            a.bind(on_start=lambda x,y: self.disable_control(),
                on_complete=lambda x,y: self.animation_complete())
            a.start(w)
        else:
            self.restore_control()
            self.next_turn()

    def get_loot_and_exp(self):
        global gold_gain
        exp = 0
        g = 0
        for x in range(0,len(enemy.enemy_team)):
            exp += enemy.enemy_team[x].exp_gain
            g += enemy.enemy_team[x].gold_gain
            enemy.enemy_team[x].drop_mashine()
        player.main_player.EXP += exp*player.main_player.EXP_boost
        player.companion1.EXP += exp*player.companion1.EXP_boost
        player.companion2.EXP += exp*player.companion2.EXP_boost
        gold_gain = g
        player.gold += g
    def check_for_victory_or_defeat(self):
        global current_fight
        global current_stage
        if len(self.enemy_team_alive) <= 0:
            self.battle_over()
            current_fight=current_fight+1
            self.get_loot_and_exp()
            self.manager.current = "battle_result"
        if len(enemy.player_team_alive) <= 0:
            self.battle_over()
            self.manager.current = "game_over" 
    
    def find_current_turn(self):
        return self.turn_order[self.turn_number-1]
    def check_for_death(self):
        if self.player.HP <= 0:
            if self.player in self.turn_order:
                self.turn_order.remove(self.player)
                self.remove_widget(self.chose_sprite(self.player))
                enemy.player_team_alive.remove(self.player)
                self.turn_number -= 1
        if self.enemy.HP <= 0:
            if self.enemy in self.turn_order:
                self.turn_order.remove(self.enemy)
                self.remove_widget(self.chose_sprite(self.enemy))
                self.target_option[self.chose_enemy_index(self.enemy)][0] = Button(pos=(10000,10000), size=(1,1)) 
                self.enemy_team_alive.remove(self.enemy)
                self.turn_number -= 1
        self.kolejka.text = ""
        for x in self.turn_order:
            self.kolejka.text += str(x)

    def update_status(self):
        if len(player.team) == 1:
            self.hp_bar_player.text = (("HP: ") + str(player.team[0].HP) + ("/") + str(player.team[0].MAX_HP))
            self.mp_bar_player.text = (("MP: ") + str(player.team[0].MP) + ("/") + str(player.team[0].MAX_MP))
        if len(player.team) == 2:
            self.hp_bar_player.text = (("HP: ") + str(player.team[0].HP) + ("/") + str(player.team[0].MAX_HP))
            self.mp_bar_player.text = (("MP: ") + str(player.team[0].MP) + ("/") + str(player.team[0].MAX_MP))
            self.hp_bar_companion_one.text = (("HP: ") + str(player.team[1].HP) + ("/") + str(player.team[1].MAX_HP))
            self.mp_bar_companion_one.text = (("MP: ") + str(player.team[1].MP) + ("/") + str(player.team[1].MAX_MP))
        if len(player.team) == 3:
            self.hp_bar_player.text = (("HP: ") + str(player.team[0].HP) + ("/") + str(player.team[0].MAX_HP))
            self.mp_bar_player.text = (("MP: ") + str(player.team[0].MP) + ("/") + str(player.team[0].MAX_MP))
            self.hp_bar_companion_one.text = (("HP: ") + str(player.team[1].HP) + ("/") + str(player.team[1].MAX_HP))
            self.mp_bar_companion_one.text = (("MP: ") + str(player.team[1].MP) + ("/") + str(player.team[1].MAX_MP))
            self.hp_bar_companion_two.text = (("HP: ") + str(player.team[2].HP) + ("/") + str(player.team[2].MAX_HP))
            self.mp_bar_companion_two.text = (("MP: ") + str(player.team[2].MP) + ("/") + str(player.team[2].MAX_MP))
        
        if len(enemy.enemy_team) == 1:
            self.hp_bar_enemy_one.text = (("HP: ") + str(enemy.enemy_team[0].HP))
        if len(enemy.enemy_team) == 2:
            self.hp_bar_enemy_one.text = (("HP: ") + str(enemy.enemy_team[0].HP))
            self.hp_bar_enemy_two.text = (("HP: ") + str(enemy.enemy_team[1].HP))
        if len(enemy.enemy_team) == 3:
            self.hp_bar_enemy_one.text = (("HP: ") + str(enemy.enemy_team[0].HP))
            self.hp_bar_enemy_two.text = (("HP: ") + str(enemy.enemy_team[1].HP))
            self.hp_bar_enemy_three.text = (("HP: ") + str(enemy.enemy_team[2].HP))
    
    def attack(self,target):
        self.enemy = enemy.enemy_team[target]
        exec(self.action)
        self.create_movement_animation(self.sprite, self.target_option[target][1][0]-100, self.target_option[target][1][1])
        self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
        for x in self.target_option:
            self.remove_widget(self.target_option[x][0])
        self.remove_widget(self.skill_list_pop_up)
        self.remove_widget(self.resign_button)
        self.run_animation()

    def action_attack(self):
        self.disable_control()
        self.action = "self.enemy.HP -= self.player.damage"
        self.add_widget(self.resign_button)
        self.chose_target()

    def resign_action(self):
        self.skill_list_pop_up.ids.list.clear_widgets()
        self.remove_widget(self.skill_list_pop_up)
        for x in self.target_option:
            self.remove_widget(self.target_option[x][0])
        self.remove_widget(self.resign_button)
        self.restore_control()

    def chosen_skill(self,target):
        self.action = target
        self.chose_target()
    def action_spells(self):
        self.disable_control()
        self.add_widget(self.resign_button)
        self.skill_list_pop_up.ids.list.clear_widgets()
        for x in self.player.skill:
            self.skill_list_pop_up.ids.list.add_widget(Button(text=x, size=(100,100), size_hint=(None,None), on_press= lambda y:self.chosen_skill(self.player.skill[x][0])))
        self.add_widget(self.skill_list_pop_up)

    def take_action(self,e):
        self.sprite = self.chose_sprite(e)
        if e in player.team:
            self.player = e 
        else:
            self.enemy = e
            self.disable_control()
            self.player = e.check_what_to_do()[0]
            exec(e.AI[e.check_what_to_do()[1][0]][1])
            self.create_movement_animation(self.sprite, self.chose_sprite(self.player).pos[0]+100,self.chose_sprite(self.player).pos[1])
            self.create_movement_animation(self.sprite, self.sprite.pos[0],self.sprite.pos[1])
            self.run_animation()
    
    def next_turn(self):
        self.check_for_victory_or_defeat()
        if self.battle_end == False:
            self.turn_number -= 1
            if self.turn_number < 0:
                self.turn_number = len(self.turn_order)-1
            self.moja.text = str(self.turn_order[self.turn_number])
            self.take_action(self.turn_order[self.turn_number])
        else:
            return False

class Menu(Screen):
    area_progress = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.progress_bar_start)

    def enter_setup(self):
        Clock.schedule_once(self.progress_bar_start)

    def start_main_fight(self):
        global current_stage
        global current_fight
        enemy.enemy_team.clear()
        for x in range(0,len(enemy.story_fight[current_stage][current_fight])):
            enemy.enemy_team.append(enemy.story_fight[current_stage][current_fight][x])
        self.manager.current = "fight"
    def start_random_fight(self):
        enemy.enemy_team.clear()
        roll_fight = random.randint(1,current_fight)
        for x in range(0,len(enemy.story_fight[current_stage][roll_fight])):
            enemy.enemy_team.append(enemy.story_fight[current_stage][current_fight][x])
        self.manager.current = "fight"

    def progress_bar_start(self, instance): 
        self.ids.area_progress.value = 0
        self.ids.area_progress.max = 10
        self.start_fill_animation()
  
    def next(self, dt):
        if self.ids.area_progress.value >= current_fight:
            return False
        else:
            self.ids.area_progress.value += 1
            self.ids.area_progress_text.text = str(int(self.ids.area_progress.value))+" / 10"

    def start_fill_animation(self):
        Clock.schedule_interval(self.next, 1/25)

class Game_Over(Screen):
    pass
class Battle_Result(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.exp_bar_player = ProgressBar(pos=(1250,200), size_hint_x = 0.15, max=100)
        self.exp_bar_companion_one = ProgressBar(pos=(1250,-100), size_hint_x = 0.15, max=100) 
        self.exp_bar_companion_two = ProgressBar(pos=(1250,-400), size_hint_x = 0.15, max=100)
        self.exp_bar_player_text = Label(pos=(500,220))
        self.exp_bar_companion_one_text = Label(pos=(500,-80))
        self.exp_bar_companion_two_text = Label(pos=(500,-380))
        self.gold = Label(pos=(300,-420))
        self.gold_gain = Label(pos=(300,-400))
    def change_screen(self):
        self.clear_widgets()
        self.manager.current = "menu"
    def enter_setup(self):
        self.add_widget(Button(pos=(1450,800), size=(50,50), size_hint=(None,None), on_press = lambda y:self.change_screen()))
        Clock.schedule_once(self.progress_bar_start)
        self.add_widget(player.Main_Player_Sprite(pos=(1300,660)))
        self.add_widget(player.Companion1_Sprite(pos=(1300,360)))
        self.add_widget(player.Companion2_Sprite(pos=(1300,60)))
        self.add_widget(self.exp_bar_player)
        self.add_widget(self.exp_bar_companion_one)
        self.add_widget(self.exp_bar_companion_two)
        self.add_widget(self.exp_bar_player_text)
        self.add_widget(self.exp_bar_companion_one_text)
        self.add_widget(self.exp_bar_companion_two_text)
        self.add_widget(self.gold)
        self.add_widget(self.gold_gain)
        im.check_whitch_screen(self.manager.current)
        
        for x in range(0,80):
            im.inventory[x] = im.ItemSlot(pos=(player.main_player.inventory[x][0],player.main_player.inventory[x][1]), sprite=(player.main_player.inventory[x][2]))
            self.add_widget(im.inventory[x])
        self.gold_gain.text = "+"+str(gold_gain)
        self.gold.text = str(player.gold)
            
    def progress_bar_start(self, instance): 
        self.exp_bar_player.value = 0
        self.exp_bar_companion_one.value = 0
        self.exp_bar_companion_two.value = 0
        self.exp_bar_player.max = player.main_player.EXP_To_Lv
        self.exp_bar_companion_one.max = player.companion1.EXP_To_Lv
        self.exp_bar_companion_two.max = player.companion2.EXP_To_Lv
        self.start_fill_animation()
  
    def next(self, dt):
        if self.exp_bar_player.value >= player.main_player.EXP and self.exp_bar_companion_one.value >= player.companion1.EXP and self.exp_bar_companion_two.value >= player.companion2.EXP:
            return False
        
        if self.exp_bar_player.value >= player.main_player.EXP:
            pass
        else:
            self.exp_bar_player.value += 1
            self.exp_bar_player_text.text = f'{int(self.exp_bar_player.value)}'
        
        if self.exp_bar_companion_one.value >= player.companion1.EXP:
            pass    
        else:
            self.exp_bar_companion_one.value += 1
            self.exp_bar_companion_one_text.text = f'{int(self.exp_bar_companion_one.value)}'
        
        if self.exp_bar_companion_two.value >= player.companion2.EXP:
            pass
        else:
            self.exp_bar_companion_two.value += 1
            self.exp_bar_companion_two_text.text = f'{int(self.exp_bar_companion_two.value)}'
      
    def start_fill_animation(self):
        Clock.schedule_interval(self.next, 1/25)
        
class WindowManger(ScreenManager):
    menu = ObjectProperty(None)
    team = ObjectProperty(None)
    shop = ObjectProperty(None)
    skills = ObjectProperty(None)
    fight = ObjectProperty(None)
    game_over = ObjectProperty(None)
    battle_result = ObjectProperty(None)

screen_manager = WindowManger()

kv = Builder.load_file("mymain.kv")
Window.fullscreen = "auto"

class MyMainApp(App):
    def build(self):
        return kv
    
if __name__ == "__main__":
    MyMainApp().run()
