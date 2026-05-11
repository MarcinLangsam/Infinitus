import enemy, skill_record as sk, status_effect as se, tooltip as tt, random, text_pop as tp, inventory_manager as im, music_player as mp
from player import team, Character_Sprite, companion1, companion2, main_player
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.metrics import dp
from components.fight_components import PlayerStatusContainer, EnemyStatusContainer
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior

current_stage = 1
current_fight = 1

stage1_progress = 1
stage2_progress = 1

gold_gain = 0
is_random_fight = False

def update_stages_progression(current):
    global stage1_progress
    global stage2_progress
    if current == 1:
        stage1_progress += 1
    if current == 2:
        stage2_progress += 1

class HPBar(ProgressBar):
    pass
class MPBar(ProgressBar):
    pass
class EnemyHPBar(ProgressBar):
    pass
class Skill_List_Pop_Up(BoxLayout):
    list = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class AttackButton(ButtonBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_release=self.on_attack_release)
    def on_attack_release(self, *args):
        self.parent.action_attack()
class SkillButton(ButtonBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_release=self.on_skill_release)
    def on_skill_release(self, *args):
        self.parent.action_spells()
class DefendButton(ButtonBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_release=self.on_defend_release)
    def on_defend_release(self, *args):
        self.parent.action_defend()
class PotionButton(ButtonBehavior, BoxLayout):
    potion_description = StringProperty("Nie masz miskstur")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_release=self.on_potion_release)
    def on_potion_release(self, *args):
        self.parent.action_potion()

class Fight(Screen):
    battle_background = StringProperty("graphics/battle_background.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_turn = team[0]
        self.current_target = 0
        self.player_sprites = []
        self.enemy_sprites = []
        self.sprite = enemy.Enemy_Sprite(enemy.enemy_team[0].enemy_sprite,enemy.enemy_team[0].source,pos_hint={"center_x": 0.61, "center_y": 0.58})
        self.target_sprite = enemy.Enemy_Sprite(enemy.enemy_team[0].enemy_sprite,enemy.enemy_team[0].source,pos_hint={"center_x": 0.61, "center_y": 0.58})
        self.anim_queue = []
        self.turn_order = list()
        self.target_option = {}
        self.target = 0
        self.turn_number = 0
        self.action = ""
        self.action_status = ""
        self.resign_button = Button(size_hint=(None,None), size=(dp(85),dp(75)), pos_hint={"x": 0.21, "y": 0.25}, on_press = lambda y:self.resign_action(), background_normal="graphics/back_button.png", border=(0,0,0,0))
        self.enemy_team = list()
        self.battle_end = False
        self.if_attack = True
        self.animation_type = ""
        self.text_pop = Label(font_size = 33, outline_width = 1)
        self.final_damage = 0
        self.final_damage_all = list()
        self.MP_cost = 0
        self.distance = 0
        self.target_type = 0
        self.skill_list_pop_up = Skill_List_Pop_Up()
        self.crit_roll = 0
        self.dodge_roll = 0
        self.tooltip = tt.Tooltip()
        self.if_critical_or_miss = False
        self.if_all_targets = False
        self.effect = ""
        self.skill_sound_effect = SoundLoader.load("graphics/sounds/hit.wav")
        self.error_sound = SoundLoader.load("graphics/sounds/error.wav")
        self.pos_hint_copy = {}


    def get_battle_background(self):
        if current_stage == 1:
            return "graphics/battle_background.png"
        elif current_stage == 2:
            return "graphics/battle_background2.png"
        else:
            return "graphics/battle_background.png"

    def send_tooltip():
        return Fight.tooltip

    def clear_after_battle(self):
        if len(team) >=1:
            self.player1_container.hide_border()
        if len(team) >=2:
            self.player2_container.hide_border()
        if len(team) >=3:
            self.player3_container.hide_border()
        if len(enemy.enemy_team) >=1:
            self.enemy1_container.hide_border()
        if len(enemy.enemy_team) >=2:
            self.enemy2_container.hide_border()
        if len(enemy.enemy_team) >=3:
            self.enemy3_container.hide_border()
        for x in range(0,len(team)):
            self.player_sprites[x][1].status_icons.clear_all_icons()
            for y in range(0,1):
                self.remove_widget(self.player_sprites[x][y])
        for x in range(0,len(enemy.enemy_team)):
            for y in range(0,2):
                self.remove_widget(self.enemy_sprites[x][y])
        self.remove_widget(self.tooltip)
        self.remove_widget(tp.text_pop_fight)
        self.remove_widget(self.text_pop)
        self.final_damage = 0
        
        
    def prepare_battle_visuals(self):
        self.battle_background = self.get_battle_background()
        self.player_sprites.clear()
        self.enemy_sprites.clear()
        if len(team) >=1:
            self.player1_container = PlayerStatusContainer(team[0], self.tooltip, pos_hint={"x": 0.02, "y": 0.005})
            self.player_sprites.append([Character_Sprite(main_player,im.items.item_list[main_player.inventory["main_hand"][2]][0],main_player.head, pos_hint={"center_x": 0.39, "center_y": 0.58}),
                                        self.player1_container
                                        ])
        if len(team) >=2:
            self.player2_container = PlayerStatusContainer(team[1], self.tooltip, pos_hint={"x": 0.23, "y": 0.005})
            self.player_sprites.append([Character_Sprite(companion1,im.items.item_list[companion1.inventory["main_hand"][2]][0], companion1.head, pos_hint={"center_x": 0.25, "center_y": 0.73}),
                                        self.player2_container
                                        ])
        if len(team) >=3:
            self.player3_container = PlayerStatusContainer(team[2], self.tooltip, pos_hint={"x": 0.44, "y": 0.005})
            self.player_sprites.append([Character_Sprite(companion2,im.items.item_list[companion2.inventory["main_hand"][2]][0],companion2.head, pos_hint={"center_x": 0.29, "center_y": 0.45}),
                                        self.player3_container
                                        ])
        if len(enemy.enemy_team) >=1:
            self.enemy1_container = EnemyStatusContainer(enemy.enemy_team[0], self.tooltip, pos_hint={"x": 0.55, "y": 0.81})
            self.enemy_sprites.append([enemy.Enemy_Sprite(enemy.enemy_team[0].enemy_sprite,enemy.enemy_team[0].source, pos_hint={"center_x": 0.61, "center_y": 0.58}),
                                       self.enemy1_container
                                       ])
        if len(enemy.enemy_team) >=2:
            self.enemy2_container = EnemyStatusContainer(enemy.enemy_team[1], self.tooltip, pos_hint={"x": 0.68, "y": 0.81})
            self.enemy_sprites.append([enemy.Enemy_Sprite(enemy.enemy_team[1].enemy_sprite,enemy.enemy_team[1].source, pos_hint={"center_x": 0.76, "center_y": 0.73}),
                                       self.enemy2_container
                                       ])
        if len(enemy.enemy_team) >=3:
            self.enemy3_container = EnemyStatusContainer(enemy.enemy_team[2], self.tooltip, pos_hint={"x": 0.8, "y": 0.81})
            self.enemy_sprites.append([enemy.Enemy_Sprite(enemy.enemy_team[2].enemy_sprite,enemy.enemy_team[2].source, pos_hint={"center_x": 0.71, "center_y": 0.45}),
                                       self.enemy3_container
                                       ])
        for x in range(0,len(team)):
            for y in range(0,2):
                self.add_widget(self.player_sprites[x][y])
        for x in range(0,len(enemy.enemy_team)):
            for y in range(0,2):
                self.add_widget(self.enemy_sprites[x][y])
        self.add_widget(tp.text_pop_fight)
        self.add_widget(self.text_pop)
        self.add_widget(self.tooltip)
        

    def chose_sprite(self,e):
        for x in range(0,len(team)):
            if e == team[x]:                                           
                sprite = self.player_sprites[x][0]
        for y in range(0,len(enemy.enemy_team)):
            if e == enemy.enemy_team[y]:
                sprite = self.enemy_sprites[y][0]
        return sprite
    def chose_enemy_index(self,e):
        for x in range(0,len(team)):
            if e == team[x]:                                           
                index = x
        for y in range(0,len(enemy.enemy_team)):
            if e == enemy.enemy_team[y]:
                index = y
        return index
    def get_turn_index(self,e):
        for x in range(0,len(self.turn_order)):
            if e == self.turn_order[x]:
                return x
        
    def chose_target(self,target):
        if target == "on_enemy":
            for x in range(0,len(enemy.enemy_team)):
                self.add_widget(self.target_option[x][0])
        elif target == "on_self":
            self.add_widget(self.target_option[self.chose_enemy_index(self.current_turn)+3][0])
        elif target == "on_all_enemy":
            self.add_widget(self.target_option[6][0])
        elif target == "on_all_character":
            self.add_widget(self.target_option[7][0])
        else:
            for x in range(3,3+len(team)):
                self.add_widget(self.target_option[x][0])
    
    def start_fight_setup(self):
        music_number = random.randint(1,4)
        mp.music_player.change_music("graphics/music/battle"+str(music_number)+".wav")

        enemy.enemy_team_alive.clear()
        enemy.player_team_alive = team.copy()
        for x in range(0,len(enemy.enemy_team)):
            enemy.enemy_team_alive.append(enemy.enemy_team[x])
        self.battle_end = False
        self.prepare_battle_visuals()
        self.create_turn_order()
        self.create_target_option()
        for x in team:
            self.aplly_stats_modifier(x)
        for x in enemy.enemy_team:
            self.aplly_stats_modifier(x)
        #self.take_action(self.turn_order[self.turn_number])

        Clock.schedule_once(lambda dt: self.take_action(self.turn_order[self.turn_number]), 0)

    def battle_over(self):
        for x in team:
            if len(x.status) != 0:
                for y in x.status:
                    self.remove_widget(y[1])
                    self.remove_widget(y[2])
                    #exec(y[0][7])
                    self.reset_stats_modifier(x)
                x.status.clear()
            x.HP = x.MAX_HP
            x.MP = x.MAX_MP
            x.current_potions = x.potions
        for x in enemy.enemy_team:
            if len(x.status) != 0:
                for y in x.status:
                    self.remove_widget(y[1])
                    self.remove_widget(y[2])
                    #exec(y[0][7])
                    self.reset_stats_modifier(x)
                x.status.clear()
            x.HP = x.MAX_HP
        self.clear_after_battle()
        self.battle_end = True

    def disable_control(self):
        self.ids.attack.disabled = True
        self.ids.spells.disabled = True
        self.ids.defend.disabled = True
        self.ids.potion.disabled = True
    def restore_control(self):
        self.ids.attack.disabled = False
        self.ids.spells.disabled = False
        self.ids.defend.disabled = False
        self.ids.potion.disabled = False

    def sort_by(self,e):
        return e.DEX
    def create_turn_order(self):
        self.turn_order.clear()
        for x in range(0,len(team)):
            self.turn_order.append(team[x])
        for x in range(0,len(enemy.enemy_team)):
            self.turn_order.append(enemy.enemy_team[x])
        self.turn_order.sort(key=self.sort_by)
        self.turn_number = len(self.turn_order)-1
      
    def create_target_option(self):
        if len(enemy.enemy_team) >= 1:
            enemy_name1 = enemy.enemy_team[0].name.replace(" ","\n")
            self.target_option[0] = [Button(text=enemy_name1,font_size = 18, size_hint=(0.08,0.07), pos_hint={"x": 0.30, "y": 0.25}, on_press = lambda y:self.attack(0), background_normal="graphics/target_button.png"),self.chose_sprite(enemy.enemy_team[0]).pos]
        if len(enemy.enemy_team) >= 2:
            enemy_name2 = enemy.enemy_team[1].name.replace(" ","\n")
            self.target_option[1] = [Button(text=enemy_name2,font_size = 18, size_hint=(0.08,0.07), pos_hint={"x": 0.38, "y": 0.25}, on_press = lambda y:self.attack(1), background_normal="graphics/target_button.png"),self.chose_sprite(enemy.enemy_team[1]).pos]
        if len(enemy.enemy_team) >= 3:
            enemy_name3 = enemy.enemy_team[2].name.replace(" ","\n")
            self.target_option[2] = [Button(text=enemy_name3,font_size = 18, size_hint=(0.08,0.07), pos_hint={"x": 0.46, "y": 0.25}, on_press = lambda y:self.attack(2), background_normal="graphics/target_button.png"),self.chose_sprite(enemy.enemy_team[2]).pos]
        
        if len(team) >= 1:
            self.target_option[3] = [Button(text=team[0].name,font_size = 18, size_hint=(0.08,0.07), pos_hint={"x": 0.30, "y": 0.25}, on_press = lambda y:self.attack(0), background_normal="graphics/target_button.png"),self.chose_sprite(team[0]).pos]
        if len(team) >= 2:
            self.target_option[4] = [Button(text=team[1].name,font_size = 18, size_hint=(0.08,0.07), pos_hint={"x": 0.38, "y": 0.25}, on_press = lambda y:self.attack(1), background_normal="graphics/target_button.png"),self.chose_sprite(team[1]).pos]
        if len(team) >= 3:
            self.target_option[5] = [Button(text=team[2].name,font_size = 18, size_hint=(0.08,0.07), pos_hint={"x": 0.46, "y": 0.25}, on_press = lambda y:self.attack(2), background_normal="graphics/target_button.png"),self.chose_sprite(team[2]).pos]

        self.target_option[6] = [Button(text="Wszyscy wrogowie",font_size = 18, size_hint=(0.1,0.07), pos_hint={"x": 0.30, "y": 0.25}, on_press = lambda y:self.attack(3), background_normal="graphics/target_button.png"),self.chose_sprite(team[self.chose_enemy_index(self.current_turn)]).pos]
        self.target_option[7] = [Button(text="Wszyscy sojusznicy",font_size = 18, size_hint=(0.1,0.07), pos_hint={"x": 0.30, "y": 0.25}, on_press = lambda y:self.attack(4), background_normal="graphics/target_button.png"),self.chose_sprite(team[self.chose_enemy_index(self.current_turn)]).pos]


    def set_sound_effect(self,sound_source):
        self.skill_sound_effect.unload()
        self.skill_sound_effect = SoundLoader.load(sound_source)
    def clear_pop_up(self,dt):
        self.text_pop.text = ""
        return False
    def sprite_animation(self,dt):
        self.sprite.time += dt
        if(self.target_sprite!=self.sprite and self.if_all_targets == True):
            for x in enemy.enemy_team:
                self.chose_sprite(x).time += dt
        elif(self.target_sprite!=self.sprite):
            self.target_sprite.time += dt
        
        if self.skill_sound_effect and self.sprite.frame==30:
            self.skill_sound_effect.play()
        if (self.sprite.time > self.sprite.rate):
                self.sprite.time -= self.sprite.rate
                self.sprite.head = "atlas://graphics/animations/"+self.sprite.head_source+"/"+self.sprite.anim + self.animation_type + str(self.sprite.frame)
                self.sprite.sprite = "atlas://graphics/animations/"+self.sprite.source+"/"+self.sprite.anim + self.animation_type + str(self.sprite.frame)
                self.sprite.weapon = "atlas://graphics/animations/"+self.sprite.weapon_source+"/"+self.sprite.weapon_source + self.animation_type + str(self.sprite.frame)
                if(self.target_sprite==self.sprite):
                    self.sprite.effect = "atlas://graphics/effects/"+self.sprite.effect_source+"/effect" + str(self.sprite.frame)
                self.sprite.frame = self.sprite.frame + 1

                            

                if(self.if_all_targets == True and self.distance not in ["status","heal"]):
                    if self.current_target in team:
                        for x in team:
                            self.chose_sprite(x).time -= self.chose_sprite(x).rate
                            self.chose_sprite(x).head = "atlas://graphics/animations/"+self.chose_sprite(x).head_source+"/"+self.chose_sprite(x).anim + "_hit" + str(self.chose_sprite(x).frame)
                            self.chose_sprite(x).sprite = "atlas://graphics/animations/"+self.chose_sprite(x).source+"/"+self.chose_sprite(x).anim + "_hit" + str(self.chose_sprite(x).frame)
                            self.chose_sprite(x).weapon = "atlas://graphics/animations/"+self.chose_sprite(x).weapon_source+"/"+self.chose_sprite(x).weapon_source + "_hit" + str(self.chose_sprite(x).frame)
                            self.chose_sprite(x).effect = "atlas://graphics/effects/"+self.chose_sprite(x).effect_source+"/effect" + str(self.target_sprite.frame)
                            self.chose_sprite(x).frame = self.chose_sprite(x).frame + 1
                
                    else:
                        for x in enemy.enemy_team:
                            self.chose_sprite(x).time -= self.chose_sprite(x).rate
                            self.chose_sprite(x).head = "atlas://graphics/animations/"+self.chose_sprite(x).head_source+"/"+self.chose_sprite(x).anim + "_hit" + str(self.chose_sprite(x).frame)
                            self.chose_sprite(x).sprite = "atlas://graphics/animations/"+self.chose_sprite(x).source+"/"+self.chose_sprite(x).anim + "_hit" + str(self.chose_sprite(x).frame)
                            self.chose_sprite(x).weapon = "atlas://graphics/animations/"+self.chose_sprite(x).weapon_source+"/"+self.chose_sprite(x).weapon_source + "_hit" + str(self.chose_sprite(x).frame)
                            self.chose_sprite(x).effect = "atlas://graphics/effects/"+self.chose_sprite(x).effect_source+"/effect" + str(self.target_sprite.frame)
                            self.chose_sprite(x).frame = self.chose_sprite(x).frame + 1
                
                elif(self.target_sprite!=self.sprite and self.distance in ["status","heal"]):
                    self.target_sprite.effect = "atlas://graphics/effects/"+self.target_sprite.effect_source+"/effect" + str(self.target_sprite.frame)
                    self.target_sprite.frame = self.target_sprite.frame + 1
                elif(self.target_sprite!=self.sprite and self.distance not in ["status","heal"]):
                    self.target_sprite.time -= self.target_sprite.rate
                    self.target_sprite.head = "atlas://graphics/animations/"+self.target_sprite.head_source+"/"+self.target_sprite.anim + "_hit" + str(self.target_sprite.frame)
                    self.target_sprite.sprite = "atlas://graphics/animations/"+self.target_sprite.source+"/"+self.target_sprite.anim + "_hit" + str(self.target_sprite.frame)
                    self.target_sprite.weapon = "atlas://graphics/animations/"+self.target_sprite.weapon_source+"/"+self.target_sprite.weapon_source + "_hit" + str(self.target_sprite.frame)
                    self.target_sprite.effect = "atlas://graphics/effects/"+self.target_sprite.effect_source+"/effect" + str(self.target_sprite.frame)
                    self.target_sprite.frame = self.target_sprite.frame + 1
            
                if (self.sprite.frame > self.sprite.frame_sum):
                    self.sprite.frame = 1
                    
                    if self.if_all_targets == True:
                        if self.current_target in team:
                            for x in team:
                                self.chose_sprite(x).frame = 1
                        else:
                            for x in enemy.enemy_team:
                                self.chose_sprite(x).frame = 1
                    else:
                        self.target_sprite.frame = 1

                    if self.if_all_targets == True:
                        if self.current_target in team:
                            self.text_pop.pos = (self.chose_sprite(team[0]).pos[0]-635,self.chose_sprite(team[0]).pos[1]-245)
                        else:
                            self.text_pop.pos = (self.chose_sprite(enemy.enemy_team[0]).pos[0]-635,self.chose_sprite(enemy.enemy_team[0]).pos[1]-245)   
                        if len(self.final_damage_all)==2:
                            self.text_pop.text += str(self.final_damage_all[1]) + "\n\n"
                            self.text_pop.text += str(self.final_damage_all[0]) + "\n\n"
                        if len(self.final_damage_all)==3:
                            self.text_pop.text += str(self.final_damage_all[1]) + "\n\n"
                            self.text_pop.text += str(self.final_damage_all[0]) + "\n\n"
                            self.text_pop.text += str(self.final_damage_all[2]) + "\n\n"
                        #for x in self.final_damage_all:
                            #self.text_pop.text += str(x) + "\n\n"
                    else:
                        if self.current_turn == self.current_target:
                            self.text_pop.pos = (Window.width*self.pos_hint_copy['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.pos_hint_copy['center_y']-(Window.height/2))
                        else:
                            self.text_pop.pos = (Window.width*self.chose_sprite(self.current_target).pos_hint['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.chose_sprite(self.current_target).pos_hint['center_y']-(Window.height/2))      
                        self.text_pop.text = str(self.final_damage)
                    
                    Clock.schedule_interval(self.clear_pop_up,1)
                    if self.if_all_targets == True:
                        if self.current_target in team:
                            for x in team:
                                self.update_status()
                                self.check_for_death_entity(x)
                        else:
                            for x in enemy.enemy_team:
                                self.update_status()
                                self.check_for_death_entity(x)
                    else:
                        self.update_status()
                        self.check_for_death()
                    self.run_animation()
                    return False
    def create_movement_animation(self, widget, x_pos, y_pos):
        if widget == self.text_pop:
            if self.if_critical_or_miss == True:
                self.anim_queue.append((widget, Animation(x=x_pos, y=y_pos, duration=0.4, font_size=44, t="out_circ")))
            if self.if_critical_or_miss == False:
                self.anim_queue.append((widget, Animation(x=x_pos, y=y_pos, duration=0.4, font_size=38, t="out_circ")))
            self.if_critical_or_miss = False
        else:
            self.anim_queue.append((widget, Animation(x=x_pos, y=y_pos, duration=0.5, t="in_out_quad")))
    def create_death_animation(self, widget,x_pos, y_pos):
        self.anim_queue.append((widget, Animation(x=x_pos, y=y_pos, duration=0.2, t="in_out_elastic")))

    def animation_complete(self):
        if self.if_attack == True:
            Clock.schedule_interval(self.sprite_animation,0.02)
            self.if_attack = False
        else:
            self.run_animation()

    def run_animation(self):
        if self.sprite.pos_hint != {}:
            self.pos_hint_copy = self.sprite.pos_hint.copy()
        self.sprite.pos_hint = {}
        if len(self.anim_queue)>0:
            w, a = self.anim_queue.pop(0)
            a.bind(on_start=lambda x,y: self.disable_control(),
                on_complete=lambda x,y: self.animation_complete())
            a.start(w)
        else:
            self.sprite.pos_hint = self.pos_hint_copy
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
        for x in team:
            x.EXP += exp+(exp*x.EXP_boost)
        gold_gain = g
        import player
        player.gold += g
    def check_for_victory_or_defeat(self):
        global current_fight
        global current_stage
        if len(enemy.enemy_team_alive) <= 0:
            self.battle_over()
            self.get_loot_and_exp()

            if enemy.story_fight[current_stage][current_fight][1] == "character":
                if current_fight < 10 and is_random_fight == False:
                    update_stages_progression(current_stage)
                    current_fight=current_fight+1
                self.manager.current = "add_new_character"
            else:
                if current_fight < 10 and is_random_fight == False:      
                    current_fight=current_fight+1
                self.manager.current = "battle_result"
        if len(enemy.player_team_alive) <= 0:
            self.battle_over()
            self.manager.current = "game_over"

    def check_for_death(self):
        if self.current_target.HP <= 0:
            if self.current_target in self.turn_order:
                self.turn_order[self.get_turn_index(self.current_target)] = "dead"
                self.anim_queue.append((self.chose_sprite(self.current_target), Animation(opacity=0, duration=0.7)))
                if self.current_target in team:
                    enemy.player_team_alive.remove(self.current_target)
                else:
                    if self.current_target.on_death == True:
                        self.on_death_effect_status_enemy_team(self.current_target.on_death_status)
                    self.target_option[self.chose_enemy_index(self.current_target)][0] = Button(pos=(10000,10000), size=(1,1)) 
                    enemy.enemy_team_alive.remove(self.current_target)
                    
        
        #if self.current_turn.HP <= 0:
        #    if self.current_turn in self.turn_order:
        #        self.turn_order[self.get_turn_index(self.current_turn)] = "dead"
        #        self.remove_widget(self.chose_sprite(self.current_turn))
        #        if self.current_turn in team:
        #            enemy.player_team_alive.remove(self.current_turn)
        #        else:
        #            self.target_option[self.chose_enemy_index(self.current_turn)][0] = Button(pos=(10000,10000), size=(1,1)) 
        #            enemy.enemy_team_alive.remove(self.current_turn)
    def check_for_death_entity(self,e):
        if e.HP <= 0:
            if e in self.turn_order:
                self.turn_order[self.get_turn_index(e)] = "dead"
                self.remove_widget(self.chose_sprite(e))
                if e in team:
                    enemy.player_team_alive.remove(e)
                else:
                    if e.on_death == True:
                        self.on_death_effect_status_enemy_team(e.on_death_status)
                    self.target_option[self.chose_enemy_index(e)][0] = Button(pos=(10000,10000), size=(1,1)) 
                    enemy.enemy_team_alive.remove(e)
    
    def on_death_effect_status_enemy_team(self, status):
        for e in enemy.enemy_team_alive:
            self.start_status_by_target(status, e)
    def on_death_effect_status_player_team(self, status):
        for character in enemy.player_team_alive:
            self.start_status_by_target(status, character)
        

    def check_for_status(self):
        if len(self.current_turn.status) != 0:

            for x in range(0,len(self.current_turn.status)):
                if self.current_turn.status[x][0][4] != "one_time":
                    exec(self.current_turn.status[x][0][1])

            for x in self.current_turn.status:
                x[0][2] -= 1
                
            temp = []
            for x in self.current_turn.status:
                if x[0][2] > 0:
                    temp.append(x)
                else:
                    exec(x[0][5])
                    self.aplly_stats_modifier(self.current_turn)
            self.current_turn.status = temp

            
                
            if self.current_turn in enemy.player_team_alive:
                self.player_sprites[self.chose_enemy_index(self.current_turn)][1].status_icons.draw_all_icons(self.current_turn.status)
            else:
                self.enemy_sprites[self.chose_enemy_index(self.current_turn)][1].status_icons.draw_all_icons(self.current_turn.status)
    def check_for_status_target(self):
        if len(self.current_target.status) != 0:
            #for x in self.current_target.status:
            #    x[0][2] -= 1
                
            #temp = []
            #for x in self.current_target.status:
            #    if x[0][2] > 0:
            #        temp.append(x)
            #    else:
            #        exec(x[0][5])
            #        self.aplly_stats_modifier(self.current_target)
            #self.current_target.status = temp

            #for x in range(0,len(self.current_target.status)):
            #    if self.current_target.status[x][0][4] != "one_time":
            #        exec(self.current_target.status[x][0][1])
                
            if self.current_target in enemy.player_team_alive:
                self.player_sprites[self.chose_enemy_index(self.current_target)][1].status_icons.draw_all_icons(self.current_target.status)
            else:
                self.enemy_sprites[self.chose_enemy_index(self.current_target)][1].status_icons.draw_all_icons(self.current_target.status)

    def reset_stats_modifier(self,target):
        target.STR_modifier = 1
        target.DEX_modifier = 1
        target.INT_modifier = 1
        target.damage_modifier = 1
        target.defence_modifier = 1
        target.crit_chance_modifier = 0
        target.dodge_chance_modifier = 0

        target.damage = target.STR_base + target.weapon
        target.crit_chance = 0.1*target.DEX_base + target.crit_chance_bonus
        target.dodge_chance = 0.02*target.DEX_base + target.dodge_chance_bonus
        target.damage_bonus = 0
        target.damage_special_effect = ""
        target.MP_regen_modifier = 0
        self.aplly_stats_modifier(target)

    def aplly_stats_modifier(self,target):
        target.STR = target.STR_base * target.STR_modifier
        target.DEX = target.DEX_base * target.DEX_modifier
        target.INT = target.INT_base * target.INT_modifier
        target.damage = (target.STR+target.weapon) * target.damage_modifier
        target.defence = target.defence_base * target.defence_modifier
        target.crit_chance = target.crit_chance_base + target.crit_chance_bonus + target.crit_chance_modifier
        target.dodge_chance = target.dodge_chance_base + target.dodge_chance_bonus + target.dodge_chance_modifier
        if target.crit_chance < 0:
            target.crit_chance = 0
        if target.dodge_chance < 0:
            target.dodge_chance = 0

    def start_status_by_target(self,new_status,target):
            ok_to_add = True
            for x in range(0,len(target.status)):
                if new_status == target.status[x][0][0]:
                    target.status[x][0][2] = se.status_effects.status_list[new_status][2]
                    ok_to_add = False
            if ok_to_add == True:
                target.status.append([se.status_effects.status_list[new_status].copy(),se.Status_Icon(se.status_effects.status_list[new_status][3],se.status_effects.status_list[new_status][6]),Label(font_size = 22)])
                if len(target.status) != 0:
                    if target.status[-1][0][4] == "one_time":
                        exec(target.status[-1][0][1])
                        self.aplly_stats_modifier(target)
                    if target in enemy.player_team_alive:
                        self.player_sprites[self.chose_enemy_index(target)][1].status_icons.draw_all_icons(target.status)
                    else:
                        self.enemy_sprites[self.chose_enemy_index(target)][1].status_icons.draw_all_icons(target.status)
        

    def start_status(self,new_status):
            ok_to_add = True
            for x in range(0,len(self.current_target.status)):
                if new_status == self.current_target.status[x][0][0]:
                    self.current_target.status[x][0][2] = se.status_effects.status_list[new_status][2]
                    ok_to_add = False
            if ok_to_add == True:
                self.current_target.status.append([se.status_effects.status_list[new_status].copy(),se.Status_Icon(se.status_effects.status_list[new_status][3],se.status_effects.status_list[new_status][6]),Label(font_size = 22)])
                if len(self.current_target.status) != 0:
                    if self.current_target.status[-1][0][4] == "one_time":
                        exec(self.current_target.status[-1][0][1])
                        self.aplly_stats_modifier(self.current_target)
                    if self.current_turn in enemy.player_team_alive:
                        self.player_sprites[self.chose_enemy_index(self.current_turn)][1].status_icons.draw_all_icons(self.current_turn.status)
                    else:
                        self.enemy_sprites[self.chose_enemy_index(self.current_turn)][1].status_icons.draw_all_icons(self.current_turn.status)
        
    def update_status(self):
        for x in range(0,len(self.player_sprites)):
            self.player_sprites[x][1].update_bars()
        for y in range(0,len(self.enemy_sprites)):
            self.enemy_sprites[y][1].update_bars()
            
    def calculate_damage(self,target):
        self.dodge_roll = random.randint(0,100)
        self.crit_roll = random.randint(0,100)
        self.action = "self.current_target.HP -= self.final_damage"
        ### roll for critical hit
        if self.crit_roll < self.current_turn.crit_chance and self.distance != "heal" and self.distance != "status":
                self.final_damage = self.final_damage+(self.final_damage*0.5)
                self.final_damage = int(self.final_damage)
                self.action = "self.current_target.HP -= self.final_damage\nself.final_damage = str(self.final_damage)+'!'"
                self.if_critical_or_miss = True
        ### substract defence of the target(can't deal less than 5 points of damage)
        if ((self.final_damage - self.current_target.defence) * self.current_target.damage_reduction) < 5  and self.distance != "heal" and self.distance != "status":    
            self.final_damage = 5
        elif self.distance != "heal" and self.distance != "status":
            self.final_damage = (self.final_damage - self.current_target.defence) * self.current_target.damage_reduction
            self.final_damage = int(self.final_damage)
        ### roll for dodeging the attack
        if self.dodge_roll < self.current_target.dodge_chance  and self.distance != "heal" and self.distance != "status":
                self.action = "self.final_damage = 'PUDŁO!'"
                self.if_critical_or_miss = True
                
        exec(self.action)
        if self.current_turn.damage_special_effect != "":
            exec(self.current_turn.damage_special_effect)
        if self.action_status != "":
            self.start_status(self.action_status)
            self.check_for_status_target()
            if self.final_damage == 0:
                self.final_damage = self.action_status.upper()
            else:
                self.final_damage = str(self.final_damage) + " | " + self.action_status.upper()
        
        

        self.check_for_exceed_HP_MP()
        #if self.current_turn in team:
        #print("TERAZ DZIALA: "+str(self.current_turn))
        #self.current_turn.printBattleStats()
        #print("JEGO CEL"+str(self.current_target))
        #self.current_target.printBattleStats()
        #print("\n\n")
        if(self.if_all_targets == False):
            self.action_status = ""

    def add_animation(self,target):
        if self.distance == "melee":
            self.animation_type = "_attack"
            if self.current_turn in team:
                self.create_movement_animation(self.sprite, self.target_option[target][1][0]-dp(180), self.target_option[target][1][1])
            else: 
                self.create_movement_animation(self.sprite, self.chose_sprite(self.current_target).pos[0]+dp(180),self.chose_sprite(self.current_target).pos[1])
            
            if self.if_all_targets and self.current_target in team:
                self.create_movement_animation(self.text_pop, Window.width*self.chose_sprite(team[0]).pos_hint['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.chose_sprite(team[0]).pos_hint['center_y']-(Window.height/2)+(Window.height*0.1))
            elif self.if_all_targets and self.current_target in enemy.enemy_team:
                self.create_movement_animation(self.text_pop, Window.width*self.chose_sprite(enemy.enemy_team[0]).pos_hint['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.chose_sprite(enemy.enemy_team[0]).pos_hint['center_y']-(Window.height/2)+(Window.height*0.1))
            else:
                print(self.chose_sprite(self.current_target).pos_hint['center_x'])
                self.create_movement_animation(self.text_pop, Window.width*self.chose_sprite(self.current_target).pos_hint['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.chose_sprite(self.current_target).pos_hint['center_y']-(Window.height/2)+(Window.height*0.1))
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])

        elif self.distance == "ranged":
            self.animation_type = "_magic"
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
            if self.if_all_targets and self.current_target in team:
                self.create_movement_animation(self.text_pop, Window.width*self.chose_sprite(team[0]).pos_hint['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.chose_sprite(team[0]).pos_hint['center_y']-(Window.height/2)+(Window.height*0.1))
            elif self.if_all_targets and self.current_target in enemy.enemy_team:
                self.create_movement_animation(self.text_pop, Window.width*self.chose_sprite(enemy.enemy_team[0]).pos_hint['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.chose_sprite(enemy.enemy_team[0]).pos_hint['center_y']-(Window.height/2)+(Window.height*0.1))
            else:
                self.create_movement_animation(self.text_pop, Window.width*self.chose_sprite(self.current_target).pos_hint['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.chose_sprite(self.current_target).pos_hint['center_y']-(Window.height/2)+(Window.height*0.1))
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
        
        elif self.distance == "heal":
            self.animation_type = "_magic"
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
            if self.if_all_targets and self.current_target in team:
                self.create_movement_animation(self.text_pop, Window.width*self.chose_sprite(team[0]).pos_hint['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.chose_sprite(team[0]).pos_hint['center_y']-(Window.height/2)+(Window.height*0.1))
            elif self.if_all_targets and self.current_target in enemy.enemy_team:
                self.create_movement_animation(self.text_pop, Window.width*self.chose_sprite(enemy.enemy_team[0]).pos_hint['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.chose_sprite(enemy.enemy_team[0]).pos_hint['center_y']-(Window.height/2)+(Window.height*0.1))
            else:
                self.create_movement_animation(self.text_pop, Window.width*self.chose_sprite(self.current_target).pos_hint['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.chose_sprite(self.current_target).pos_hint['center_y']-(Window.height/2)+(Window.height*0.1))
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
        
        elif self.distance == "status":
            self.animation_type = "_magic"
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
            if self.if_all_targets and self.current_target in team:
                self.create_movement_animation(self.text_pop, Window.width*self.chose_sprite(team[0]).pos_hint['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.chose_sprite(team[0]).pos_hint['center_y']-(Window.height/2)+(Window.height*0.1))
            elif self.if_all_targets and self.current_target in enemy.enemy_team:
                self.create_movement_animation(self.text_pop, Window.width*self.chose_sprite(enemy.enemy_team[0]).pos_hint['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.chose_sprite(enemy.enemy_team[0]).pos_hint['center_y']-(Window.height/2)+(Window.height*0.1))
            else:
                self.create_movement_animation(self.text_pop, Window.width*self.chose_sprite(self.current_target).pos_hint['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.chose_sprite(self.current_target).pos_hint['center_y']-(Window.height/2)+(Window.height*0.1))
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
        
        else:
            self.animation_type = "_attack"
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
            if self.if_all_targets and self.current_target in team:
                self.create_movement_animation(self.text_pop, Window.width*self.chose_sprite(team[0]).pos_hint['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.chose_sprite(team[0]).pos_hint['center_y']-(Window.height/2)+(Window.height*0.1))
            elif self.if_all_targets and self.current_target in enemy.enemy_team:
                self.create_movement_animation(self.text_pop, Window.width*self.chose_sprite(enemy.enemy_team[0]).pos_hint['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.chose_sprite(enemy.enemy_team[0]).pos_hint['center_y']-(Window.height/2)+(Window.height*0.1))
            else:
                self.create_movement_animation(self.text_pop, Window.width*self.chose_sprite(self.current_target).pos_hint['center_x']-(Window.width/2)+(Window.width*0.05), Window.height*self.chose_sprite(self.current_target).pos_hint['center_y']-(Window.height/2)+(Window.height*0.1))
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])

    def check_for_exceed_HP_MP(self):
        if self.current_target in team and self.current_target.MP > self.current_target.MAX_MP:
            self.current_target.MP = self.current_target.MAX_MP
        if self.current_target.HP > self.current_target.MAX_HP:
            self.current_target.HP = self.current_target.MAX_HP

        if self.current_turn in team and self.current_turn.MP > self.current_turn.MAX_MP:
            self.current_turn.MP = self.current_turn.MAX_MP
        if self.current_turn.HP > self.current_turn.MAX_HP:
            self.current_turn.HP = self.current_turn.MAX_HP

    def attack(self,target):
        if target == 3: #all enemys
            final_damage_base = self.final_damage
            self.if_all_targets = True

            for x in self.skill_list_pop_up.children:
                x.disabled = False
            for x in self.target_option:
                self.remove_widget(self.target_option[x][0])
                self.remove_widget(self.skill_list_pop_up)
                self.remove_widget(self.resign_button)
            
            self.add_animation(target)
            for x in range(0,len(enemy.enemy_team)):
                self.target = x
                self.current_target = enemy.enemy_team[self.target]
                self.target_sprite = self.chose_sprite(self.current_target)
                self.target_sprite.effect_source = self.effect
                if self.distance == "status":
                    self.final_damage = final_damage_base
                self.calculate_damage(target)
                self.final_damage_all.append(self.final_damage)
            self.add_animation(target)
            self.run_animation()
            self.action_status = ""

        elif target == 4: #all allies
            final_damage_base = self.final_damage
            self.if_all_targets = True

            for x in self.skill_list_pop_up.children:
                x.disabled = False
            for x in self.target_option:
                self.remove_widget(self.target_option[x][0])
                self.remove_widget(self.skill_list_pop_up)
                self.remove_widget(self.resign_button)

            for x in range(0,len(team)):
                self.target = x
                self.current_target = team[self.target]
                self.target_sprite = self.chose_sprite(self.current_target)
                self.target_sprite.effect_source = self.effect
                if self.distance == "status":
                    self.final_damage = final_damage_base
                self.calculate_damage(target)
                self.final_damage_all.append(self.final_damage)
            
            self.add_animation(target)
            self.run_animation()
            self.action_status = ""
        else:
            self.target = target

            ### activate skills and decide targets 
            for x in self.skill_list_pop_up.children:
                x.disabled = False
            if self.target_type == "on_enemy":
                self.current_target = enemy.enemy_team[self.target]
                self.target_sprite = self.chose_sprite(self.current_target)
                self.target_sprite.effect_source = self.effect
            else:
                self.current_target = team[self.target]
                self.target_sprite = self.chose_sprite(self.current_target)
                self.target_sprite.effect_source = self.effect

            self.add_animation(target)
            self.calculate_damage(target)
            for x in self.target_option:
                self.remove_widget(self.target_option[x][0])
            self.remove_widget(self.skill_list_pop_up)
            self.remove_widget(self.resign_button)
            self.run_animation()
        if self.current_turn in team:
            self.current_turn.MP -= self.MP_cost

    def action_attack(self):
        self.disable_control()
        self.final_damage = self.current_turn.damage+self.current_turn.damage_bonus
        self.MP_cost = 0
        self.distance = "melee"
        self.target_type = "on_enemy"
        self.action_status = ""
        self.action = "self.final_damage = self.current_turn.damage+self.current_turn.damage_bonus"
        self.effect = "no_effect"
        self.set_sound_effect("graphics/sounds/hit.wav")
        self.add_widget(self.resign_button)
        self.chose_target("on_enemy")

    def action_potion(self):
        if self.current_turn.current_potions == 0:
            tp.text_pop_fight.text = "Nie masz żadnych misktur!"
            self.error_sound.play()
            Clock.schedule_interval(tp.clear_pop_up,2)
        else:
            self.disable_control()
            self.MP_cost = 0
            self.current_turn.current_potions -= 1
            self.distance = "heal"
            self.target_type = "on_self"
            self.action = self.current_turn.potion_effect
            self.action_status = "" #!!!! jesli chce aby byl status to trza kolejnosc zmenic
            self.effect = "leczenie_effect"
            self.set_sound_effect("graphics/sounds/potion.wav")
            self.final_damage = 0
            exec(self.current_turn.potion_effect)
            self.add_widget(self.resign_button)
            self.chose_target("on_self")

    def action_defend(self):
        self.disable_control()
        self.MP_cost = 0
        self.distance = "status"
        self.target_type = "on_self"
        self.action = "self.final_damage = 0\nself.action_status = 'obrona'"
        self.action_status = "obrona"
        self.effect = "obrona_buff_effect"
        self.set_sound_effect("graphics/sounds/positive_effect_1.wav")
        self.final_damage = 0
        self.add_widget(self.resign_button)
        self.chose_target("on_self")

    def resign_action(self):
        self.action_status = ""
        for x in self.skill_list_pop_up.children:
            x.disabled = False
        self.skill_list_pop_up.list.clear_widgets()
        self.remove_widget(self.skill_list_pop_up)
        for x in self.target_option:
            self.remove_widget(self.target_option[x][0])
        self.remove_widget(self.resign_button)
        self.restore_control()

    def chosen_skill(self,skill,MP,distance,target,effect_source,sound):
        if self.current_turn.MP < MP:
            self.resign_action()
            tp.text_pop_fight.text = "Nie masz wystarczająco many!"
            self.error_sound.play()
            Clock.schedule_interval(tp.clear_pop_up,2)
        else:
            for x in self.skill_list_pop_up.children:
                x.disabled = True
            exec(skill)
            self.MP_cost = MP
            self.distance = distance
            self.target_type = target
            self.effect = effect_source
            self.set_sound_effect(sound)
            self.chose_target(target)
    def action_spells(self):
        self.disable_control()
        self.add_widget(self.resign_button)
        self.skill_list_pop_up.list.clear_widgets()
        for x in self.current_turn.skill:
            if self.current_turn.skill[x][4] != "passive":
                self.skill_list_pop_up.list.add_widget(sk.Skill_Record(self.current_turn.skill[x][2], text=x+"  MP:"+str(self.current_turn.skill[x][1]),halign = "left", valign="middle" ,font_size = 20, color=(0,0,0,1), on_press = (lambda y, x=x:self.chosen_skill(self.current_turn.skill[x][0],self.current_turn.skill[x][1],self.current_turn.skill[x][5],self.current_turn.skill[x][6],self.current_turn.skill[x][7],self.current_turn.skill[x][8]))))
        self.add_widget(self.skill_list_pop_up)
        
    
    def enemy_action(self,e):
            enemy.current = e    
            temp = e.set_actions()
            
            exec(temp[1])
            self.distance = temp[3]
            if temp[2] != "atak":
                tp.text_pop_fight.text = self.current_turn.name+" używa: "+temp[2]
            Clock.schedule_interval(tp.clear_pop_up,2)

            final_damage_base = self.final_damage

            if temp[4] == "on_all_character":
                self.if_all_targets = True
                for x in range(0,len(team)):
                    self.final_damage = final_damage_base
                    self.current_target = team[x]
                    self.target_sprite = self.chose_sprite(self.current_target)
                    self.target_sprite.effect_source = temp[5]
                    self.set_sound_effect(temp[6])
                    self.calculate_damage(x)
                    self.final_damage_all.append(self.final_damage)
                self.add_animation(0)

            elif temp[4] == "on_all_enemy":
                self.if_all_targets = True
                for x in range(0,len(enemy.enemy_team)):
                    self.final_damage = final_damage_base
                    self.current_target = enemy.enemy_team[x]
                    self.target_sprite = self.chose_sprite(self.current_target)
                    self.target_sprite.effect_source = temp[5]
                    self.set_sound_effect(temp[6])
                    self.calculate_damage(x)
                    self.final_damage_all.append(self.final_damage)
                self.add_animation(3)
                
            else:
                self.current_target = temp[0]
                self.target_sprite = self.chose_sprite(self.current_target)
                self.target_sprite.effect_source = temp[5]
                self.add_animation(temp[0])
                self.set_sound_effect(temp[6])
                self.calculate_damage(temp[0])
            self.run_animation()

    def status_menagment(self):
        stun_ok = False
        for x in self.current_turn.status:
            if x[0][4] == "dmg_ot" or x[0][4] == "stun_dmg_ot":
                self.update_status()
                self.check_for_death()
                self.check_for_victory_or_defeat()
            if x[0][4] == "stun" or x[0][4] == "stun_dmg_ot":
                    stun_ok = True
        if self.current_turn.HP <= 0 or stun_ok == True:
                self.next_turn()
        elif self.current_turn in enemy.enemy_team_alive:
                self.enemy_action(self.current_turn) 
           
    def take_action(self,e):
        self.if_attack = True
        self.if_all_targets = False
        self.final_damage_all.clear()
        self.sprite = self.chose_sprite(e)
        self.current_turn = e 
        self.check_for_status()

        for x in range(0, len(self.player_sprites)):
            self.player_sprites[x][1].hide_border()
        for x in range(0, len(self.enemy_sprites)):   
            self.enemy_sprites[x][1].hide_border()
        
        ### if player turn regain mp and update potion destription ###
        if self.current_turn in enemy.player_team_alive:            
            self.player_sprites[self.chose_enemy_index(self.current_turn)][1].show_border()
            self.current_turn.MP += self.current_turn.MP_regen_base + self.current_turn.MP_regen_modifier
            self.ids.potion.potion_description = self.current_turn.potion_description + "\n("+str(self.current_turn.current_potions)+")"
            if self.current_turn.MP > self.current_turn.MAX_MP:
                self.current_turn.MP = self.current_turn.MAX_MP
            self.update_status()
        else:
            self.enemy_sprites[self.chose_enemy_index(self.current_turn)][1].show_border()
    

        self.status_menagment()
                            
    def next_turn(self):
        self.check_for_victory_or_defeat()
        if self.battle_end == False:
            self.final_damage = 0
            self.action_status = ""
            self.turn_number -= 1
            if self.turn_number < 0:
                self.turn_number = len(self.turn_order)-1
            if self.turn_order[self.turn_number] != "dead":
                self.take_action(self.turn_order[self.turn_number])
            else:
                self.next_turn()
        else:
            return False
