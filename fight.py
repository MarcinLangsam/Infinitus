import player, enemy, skill_record as sk, status_effect as se, tooltip as tt,random, text_pop as tp, inventory_manager as im
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

current_stage = 1
current_fight = 2
gold_gain = 0
is_random_fight = False

def text_pop_up(t,pos_x,pos_y):
    text_pop = Label(pos=(pos_x,pos_y), text=t, font_size=24)
    return text_pop

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
        #self.list.bind(minimum_height=self.list.setter('height'))

class Fight(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_turn = 0
        self.current_target = 0
        self.player_sprites = []
        self.enemy_sprites = []
        self.sprite = enemy.Enemy_Sprite(enemy.enemy_team[0].enemy_sprite,enemy.enemy_team[0].source,pos=(950,500))
        self.target_sprite = enemy.Enemy_Sprite(enemy.enemy_team[0].enemy_sprite,enemy.enemy_team[0].source,pos=(950,500))
        self.anim_queue = []
        self.turn_order = list()
        self.target_option = {}
        self.target = 0
        self.turn_number = 0
        self.action = ""
        self.action_status = ""
        self.resign_button = Button(size_hint=(0.09,0.113), pos=(900,0), on_press = lambda y:self.resign_action(), background_normal="graphics/back_button.png")
        self.enemy_team = list()
        self.battle_end = False
        self.if_attack = True
        self.animation_type = ""
        self.text_pop = Label(font_size = 30)
        self.final_damage = 0
        self.MP_cost = 0
        self.distance = 0
        self.target_type = 0
        self.skill_list_pop_up = Skill_List_Pop_Up()
        self.crit_roll = 0
        self.dodge_roll = 0
        self.pointer = Image(pos=(0,0), source="graphics/pointer.png")
        self.tooltip = tt.Tooltip()

    def send_tooltip():
        return Fight.tooltip

    def clear_after_battle(self):
        for x in range(0,len(player.team)):
            for y in range(0,6):
                self.remove_widget(self.player_sprites[x][y])
        for x in range(0,len(enemy.enemy_team)):
            for y in range(0,4):
                self.remove_widget(self.enemy_sprites[x][y])
        self.remove_widget(self.tooltip)
        self.remove_widget(self.pointer)
        self.remove_widget(tp.text_pop)
        self.remove_widget(self.text_pop)
        
        
    def prepare_battle_visuals(self):
        self.player_sprites.clear()
        self.enemy_sprites.clear()
        print(player.team[0].name)
        if len(player.team) >=1:
            self.player_sprites.append([player.Character_Sprite(player.main_player,im.items.item_list[player.main_player.inventory["main_hand"][2]][0],player.main_player.head,pos=(310,380)),
                                        Image(pos=(55,35), size_hint=(0.075,0.14), source = "graphics/sprites/"+player.main_player.head+"_portrait.png"),
                                        Image(pos=(15,4), size_hint=(0.1274,0.05), source = "graphics/name_holder.png"),
                                        HPBar(pos=(-9,52), max=player.team[0].MAX_HP, value=player.team[0].HP, size_hint=(0.078,0.1)),
                                        MPBar(pos=(139,52), max=player.team[0].MAX_MP, value=player.team[0].MP, size_hint=(0.078,0.1)),
                                        Label(text=str(player.team[0].HP), pos=(-729,-330), font_size=23),
                                        Label(text=str(player.team[0].MP), pos=(-581,-330), font_size=23),
                                        Label(text=str(player.team[0].MAX_HP), pos=(-729,-350), font_size=19),
                                        Label(text=str(player.team[0].MAX_MP), pos=(-581,-350), font_size=19),
                                        Label(text=player.team[0].name, pos=(-710,-406), font_size=17)
                                        ])
        if len(player.team) >=2:
            self.player_sprites.append([player.Character_Sprite(player.companion1,im.items.item_list[player.companion1.inventory["main_hand"][2]][0],player.companion1.head,pos=(105,490)),
                                        Image(pos=(265,35), size_hint=(0.075,0.14), source = "graphics/sprites/"+player.companion1.head+"_portrait.png"), #skok o 210 w prawo
                                        Image(pos=(225,4), size_hint=(0.1274,0.05), source = "graphics/name_holder.png"),
                                        HPBar(pos=(201,52), max=player.team[1].MAX_HP, value=player.team[1].HP, size_hint=(0.078,0.1)),
                                        MPBar(pos=(349,52), max=player.team[1].MAX_MP, value=player.team[1].MP, size_hint=(0.078,0.1)),
                                        Label(text=str(player.team[1].HP), pos=(-519,-330), font_size=23),
                                        Label(text=str(player.team[1].MP), pos=(-371,-330), font_size=23),
                                        Label(text=str(player.team[1].MAX_HP), pos=(-519,-350), font_size=19),
                                        Label(text=str(player.team[1].MAX_MP), pos=(-371,-350), font_size=19),
                                        Label(text=player.team[1].name, pos=(-490,-406), font_size=17) #skok o 220
                                        ])
        if len(player.team) >=3:
            self.player_sprites.append([player.Character_Sprite(player.companion2,im.items.item_list[player.companion2.inventory["main_hand"][2]][0],player.companion2.head,pos=(160,200)),
                                        Image(pos=(475,35), size_hint=(0.075,0.14), source = "graphics/sprites/"+player.companion2.head+"_portrait.png"),
                                        Image(pos=(435,4), size_hint=(0.1274,0.05), source = "graphics/name_holder.png"),
                                        HPBar(pos=(411,52), max=player.team[2].MAX_HP, value=player.team[2].HP, size_hint=(0.078,0.1)),
                                        MPBar(pos=(559,52), max=player.team[2].MAX_MP, value=player.team[2].MP, size_hint=(0.078,0.1)),
                                        Label(text=str(player.team[2].HP), pos=(-309,-330), font_size=23),
                                        Label(text=str(player.team[2].MP), pos=(-161,-330), font_size=23),
                                        Label(text=str(player.team[2].MAX_HP), pos=(-309,-350), font_size=19),
                                        Label(text=str(player.team[2].MAX_MP), pos=(-161,-350), font_size=19),
                                        Label(text=player.team[2].name, pos=(-280,-406), font_size=17) #skok o 220
                                        ])
        if len(enemy.enemy_team) >=1:
            self.enemy_sprites.append([enemy.Enemy_Sprite(enemy.enemy_team[0].enemy_sprite,enemy.enemy_team[0].source,pos=(800,380)),
                                       Image(pos=(875,735), size_hint=(0.075,0.14), source = "graphics/sprites/"+enemy.enemy_team[0].source+"_portrait.png"),
                                       Image(pos=(835,707), size_hint=(0.0958,0.05), source = "graphics/name_holder.png"),
                                       EnemyHPBar(pos=(811,752), max=enemy.enemy_team[0].MAX_HP, value=enemy.enemy_team[0].HP, size_hint=(0.078,0.1)),
                                       Label(text=str(enemy.enemy_team[0].HP),pos=(91,380), font_size=23),
                                       Label(text=enemy.enemy_team[0].name,pos=(140,297), font_size=17)
                                       ])
        if len(enemy.enemy_team) >=2:
            self.enemy_sprites.append([enemy.Enemy_Sprite(enemy.enemy_team[1].enemy_sprite,enemy.enemy_team[1].source,pos=(800,380)),
                                       Image(pos=(1075,735), size_hint=(0.075,0.14), source = "graphics/sprites/"+enemy.enemy_team[1].source+"_portrait.png"),
                                       Image(pos=(1035,707), size_hint=(0.0958,0.05), source = "graphics/name_holder.png"),
                                       EnemyHPBar(pos=(1011,752), max=enemy.enemy_team[1].MAX_HP, value=enemy.enemy_team[1].HP, size_hint=(0.078,0.1)),
                                       Label(text=str(enemy.enemy_team[1].HP),pos=(1091,380), font_size=23),
                                       Label(text=enemy.enemy_team[1].name,pos=(1140,297), font_size=17)
                                       ])
        if len(enemy.enemy_team) >=3:
            self.enemy_sprites.append([enemy.Enemy_Sprite(enemy.enemy_team[2].enemy_sprite,enemy.enemy_team[2].source,pos=(800,380)),
                                       Image(pos=(12875,735), size_hint=(0.075,0.14), source = "graphics/sprites/"+enemy.enemy_team[2].source+"_portrait.png"),
                                       Image(pos=(12835,707), size_hint=(0.0958,0.05), source = "graphics/name_holder.png"),
                                       EnemyHPBar(pos=(12811,752), max=enemy.enemy_team[2].MAX_HP, value=enemy.enemy_team[2].HP, size_hint=(0.078,0.1)),
                                       Label(text=str(enemy.enemy_team[2].HP),pos=(1291,380), font_size=23),
                                       Label(text=enemy.enemy_team[2].name,pos=(1340,297), font_size=17)
                                       ])
        for x in range(0,len(player.team)):
            for y in range(0,10):
                self.add_widget(self.player_sprites[x][y])
        for x in range(0,len(enemy.enemy_team)):
            for y in range(0,6):
                self.add_widget(self.enemy_sprites[x][y])
        self.add_widget(self.pointer)
        self.add_widget(tp.text_pop)
        self.add_widget(self.text_pop)
        self.add_widget(self.tooltip)
        

    def chose_sprite(self,e):
        for x in range(0,len(player.team)):
            if e == player.team[x]:                                           
                sprite = self.player_sprites[x][0]
        for y in range(0,len(enemy.enemy_team)):
            if e == enemy.enemy_team[y]:
                sprite = self.enemy_sprites[y][0]
        return sprite
    def chose_enemy_index(self,e):
        for x in range(0,len(player.team)):
            if e == player.team[x]:                                           
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
        else:
            for x in range(3,3+len(player.team)):
                self.add_widget(self.target_option[x][0])
    
    def start_fight_setup(self):
        enemy.enemy_team_alive.clear()
        enemy.player_team_alive = player.team.copy()
        for x in range(0,len(enemy.enemy_team)):
            enemy.enemy_team_alive.append(enemy.enemy_team[x])
        self.battle_end = False
        self.prepare_battle_visuals()
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
      
    def create_target_option(self):
        if len(enemy.enemy_team) >= 1:
            self.target_option[0] = [Button(text=enemy.enemy_team[0].name,font_size = 18,size_hint=(0.08,0.08), pos=(570+0*130,100), on_press = lambda y:self.attack(0), background_normal="graphics/target_button.png"),self.chose_sprite(enemy.enemy_team[0]).pos]
        if len(enemy.enemy_team) >= 2:
            self.target_option[1] = [Button(text=enemy.enemy_team[1].name,font_size = 18,size_hint=(0.08,0.08), pos=(570+1*130,100), on_press = lambda y:self.attack(1), background_normal="graphics/target_button.png"),self.chose_sprite(enemy.enemy_team[1]).pos]
        if len(enemy.enemy_team) >= 3:
            self.target_option[2] = [Button(text=enemy.enemy_team[2].name,font_size = 18,size_hint=(0.08,0.08), pos=(570+2*130,100), on_press = lambda y:self.attack(2), background_normal="graphics/target_button.png"),self.chose_sprite(enemy.enemy_team[2]).pos]
        
        if len(player.team) >= 1:
            self.target_option[3] = [Button(text=player.team[0].name,font_size = 18,size_hint=(0.08,0.08), pos=(570+0*130,100), on_press = lambda y:self.attack(0), background_normal="graphics/target_button.png"),self.chose_sprite(player.team[0]).pos]
        if len(player.team) >= 2:
            self.target_option[4] = [Button(text=player.team[1].name,font_size = 18,size_hint=(0.08,0.08), pos=(570+1*130,100), on_press = lambda y:self.attack(1), background_normal="graphics/target_button.png"),self.chose_sprite(player.team[1]).pos]
        if len(player.team) >= 3:
            self.target_option[5] = [Button(text=player.team[2].name,font_size = 18,size_hint=(0.08,0.08), pos=(570+2*130,100), on_press = lambda y:self.attack(2), background_normal="graphics/target_button.png"),self.chose_sprite(player.team[2]).pos]
    
    def clear_pop_up(self,dt):
        self.text_pop.text = ""
        return False
    def sprite_animation(self,dt):
        self.sprite.time += dt
        if(self.target_sprite!=self.sprite):
            self.target_sprite.time += dt

        if (self.sprite.time > self.sprite.rate):
                self.sprite.time -= self.sprite.rate
                self.sprite.head = "atlas://graphics/animations/"+self.sprite.head_source+"/"+self.sprite.anim + self.animation_type + str(self.sprite.frame)
                self.sprite.sprite = "atlas://graphics/animations/"+self.sprite.source+"/"+self.sprite.anim + self.animation_type + str(self.sprite.frame)
                self.sprite.weapon = "atlas://graphics/animations/"+self.sprite.weapon_source+"/"+self.sprite.weapon_source + self.animation_type + str(self.sprite.frame)
                self.sprite.frame = self.sprite.frame + 1

                if(self.target_sprite!=self.sprite):
                    self.target_sprite.time -= self.target_sprite.rate
                    self.target_sprite.head = "atlas://graphics/animations/"+self.target_sprite.head_source+"/"+self.target_sprite.anim + "_hit" + str(self.target_sprite.frame)
                    self.target_sprite.sprite = "atlas://graphics/animations/"+self.target_sprite.source+"/"+self.target_sprite.anim + "_hit" + str(self.target_sprite.frame)
                    self.target_sprite.weapon = "atlas://graphics/animations/"+self.target_sprite.weapon_source+"/"+self.target_sprite.weapon_source + "_hit" + str(self.target_sprite.frame)
                    self.target_sprite.frame = self.target_sprite.frame + 1

                

                if (self.sprite.frame > self.sprite.frame_sum):
                    self.sprite.frame = 1
                    self.target_sprite.frame = 1
                    self.text_pop.pos = (self.chose_sprite(self.current_target).pos[0]-635,self.chose_sprite(self.current_target).pos[1]-245)   
                    self.text_pop.text = str(self.final_damage)
                    Clock.schedule_interval(self.clear_pop_up,1)
                    self.update_status()
                    self.check_for_death()
                    self.run_animation()
                    return False
    def create_movement_animation(self, widget,x_pos, y_pos):
        if widget == self.text_pop:
            self.anim_queue.append((widget, Animation(x=x_pos, y=y_pos, duration=0.4, font_size=35, t="out_circ")))
        else:
            self.anim_queue.append((widget, Animation(x=x_pos, y=y_pos, duration=0.5, t="in_out_quad")))
    def animation_complete(self):
        if self.if_attack == True:
            Clock.schedule_interval(self.sprite_animation,0.02)
            self.if_attack = False
        else:
            self.run_animation()

    def run_animation(self):
        self.pointer.pos = (9999,9999)
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
        for x in player.team:
            x.EXP += exp+(exp*x.EXP_boost)
        gold_gain = g
        player.gold += g
    def check_for_victory_or_defeat(self):
        global current_fight
        global current_stage
        if len(enemy.enemy_team_alive) <= 0:
            self.battle_over()
            self.get_loot_and_exp()
            if current_fight < 3 and is_random_fight == False:
                current_fight=current_fight+1
            if current_fight == 3:
                self.manager.current = "end"
            else:
                self.manager.current = "battle_result"
        if len(enemy.player_team_alive) <= 0:
            self.battle_over()
            self.manager.current = "game_over" 
    
    def check_for_death(self):
        if self.current_target.HP <= 0:
            if self.current_target in self.turn_order:
                self.turn_order[self.get_turn_index(self.current_target)] = "dead"
                self.remove_widget(self.chose_sprite(self.current_target))
                if self.current_target in player.team:
                    enemy.player_team_alive.remove(self.current_target)
                else:
                    self.target_option[self.chose_enemy_index(self.current_target)][0] = Button(pos=(10000,10000), size=(1,1)) 
                    enemy.enemy_team_alive.remove(self.current_target)
        
        if self.current_turn.HP <= 0:
            if self.current_turn in self.turn_order:
                self.turn_order[self.get_turn_index(self.current_turn)] = "dead"
                self.remove_widget(self.chose_sprite(self.current_turn))
                if self.current_turn in player.team:
                    enemy.player_team_alive.remove(self.current_turn)
                else:
                    self.target_option[self.chose_enemy_index(self.current_turn)][0] = Button(pos=(10000,10000), size=(1,1)) 
                    enemy.enemy_team_alive.remove(self.current_turn)
                
    def check_for_status(self):
        if len(self.current_turn.status) != 0:
            for x in self.current_turn.status:
                x[0][2] -= 1
                self.remove_widget(x[1])
                self.remove_widget(x[2])

            temp = []
            for x in self.current_turn.status:
                if x[0][2] > 0:
                    temp.append(x)
                else:
                    exec(x[0][5])
            self.current_turn.status = temp

            for x in range(0,len(self.current_turn.status)):
                if self.current_turn in enemy.player_team_alive:
                    self.current_turn.status[x][1].pos = (self.player_sprites[self.chose_enemy_index(self.current_turn)][1].pos[0]-30+x*30,self.player_sprites[self.chose_enemy_index(self.current_turn)][1].pos[1]+130)
                    self.current_turn.status[x][2].pos = (self.player_sprites[self.chose_enemy_index(self.current_turn)][1].pos[0]-790+x*30,self.player_sprites[self.chose_enemy_index(self.current_turn)][1].pos[1]-290)
                else:
                    self.current_turn.status[x][1].pos = (self.enemy_sprites[self.chose_enemy_index(self.current_turn)][1].pos[0]-30+-x*30,self.enemy_sprites[self.chose_enemy_index(self.current_turn)][1].pos[1]-40)
                    self.current_turn.status[x][2].pos = (self.enemy_sprites[self.chose_enemy_index(self.current_turn)][1].pos[0]-790-x*30,self.enemy_sprites[self.chose_enemy_index(self.current_turn)][1].pos[1]-461)
                self.current_turn.status[x][2].text = str(self.current_turn.status[x][0][2])
                self.add_widget(self.current_turn.status[x][1],-1)
                self.add_widget(self.current_turn.status[x][2],-2)

                if self.current_turn.status[x][0][4] != "one_time":
                    exec(self.current_turn.status[x][0][1])

    def start_status(self):
            if len(self.current_target.status) != 0:
                if self.current_target in enemy.player_team_alive:
                    self.current_target.status[-1][1].pos = (self.player_sprites[self.chose_enemy_index(self.current_target)][1].pos[0]-30+(len(self.current_target.status)-1)*30,self.player_sprites[self.chose_enemy_index(self.current_target)][1].pos[1]+130)
                    self.current_target.status[-1][2].pos = (self.player_sprites[self.chose_enemy_index(self.current_target)][1].pos[0]-790+(len(self.current_target.status)-1)*30,self.player_sprites[self.chose_enemy_index(self.current_target)][1].pos[1]-290)
                else:
                    self.current_target.status[-1][1].pos = (self.enemy_sprites[self.chose_enemy_index(self.current_target)][1].pos[0]-30-(len(self.current_target.status)-1)*30,self.enemy_sprites[self.chose_enemy_index(self.current_target)][1].pos[1]-40)
                    self.current_target.status[-1][2].pos = (self.enemy_sprites[self.chose_enemy_index(self.current_target)][1].pos[0]-790-(len(self.current_target.status)-1)*30,self.enemy_sprites[self.chose_enemy_index(self.current_target)][1].pos[1]-461)
                self.current_target.status[-1][2].text = str(self.current_target.status[-1][0][2])
                if self.current_target.status[-1][0][4] == "one_time":
                    exec(self.current_target.status[-1][0][1])
                
                self.add_widget(self.current_target.status[-1][1],-1)
                self.add_widget(self.current_target.status[-1][2],-2)

    def update_status(self):
        for x in range(0,len(self.player_sprites)):
            self.player_sprites[x][3].value = player.team[x].HP
            self.player_sprites[x][4].value = player.team[x].MP
            self.player_sprites[x][5].text = str(player.team[x].HP)
            self.player_sprites[x][6].text = str(player.team[x].MP)
            self.player_sprites[x][7].text = str(player.team[x].MAX_HP)
            self.player_sprites[x][8].text = str(player.team[x].MAX_MP)
        for y in range(0,len(self.enemy_sprites)):
            self.enemy_sprites[y][3].value = enemy.enemy_team[y].HP
            self.enemy_sprites[y][4].text = str(enemy.enemy_team[y].HP)


    def calculate_damage(self,target):
        self.dodge_roll = random.randint(0,100)
        self.crit_roll = random.randint(0,100)
        self.action = "self.current_target.HP -= self.final_damage"
        ### roll for critical hit
        if self.crit_roll < self.current_turn.crit_chance and self.distance != "heal" and self.distance != "status":
                self.final_damage = self.final_damage+(self.final_damage*0.5)
                self.final_damage = int(self.final_damage)
                self.action = "self.current_target.HP -= self.final_damage\nself.final_damage = 'TRAFIENIE KRYTYCZNE '+str(self.final_damage)+'!'"
        ### substract defence of the target(can't deal less than 5 points of damage)
        if (self.final_damage - self.current_target.defence) < 5  and self.distance != "heal" and self.distance != "status":    
            self.final_damage = 5
        elif self.distance != "heal" and self.distance != "status":
            self.final_damage -= self.current_target.defence
            self.final_damage = int(self.final_damage)
        ### roll for dodeging the attack
        if self.dodge_roll < self.current_target.dodge_chance  and self.distance != "heal" and self.distance != "status":
                self.action = "self.final_damage = 'PUDŁO!'"
    
        exec(self.action)
        if self.action_status != "":
            self.add_status(self.action_status)
            self.start_status()
            if self.final_damage == 0:
                self.final_damage = self.action_status.upper()
            else:
                self.final_damage = str(self.final_damage) + " " + self.action_status.upper()

        self.check_for_exceed_HP_MP()

        if self.distance == "melee":
            self.animation_type = "_attack"
            if self.current_turn in player.team:
                self.create_movement_animation(self.sprite, self.target_option[target][1][0]-250, self.target_option[target][1][1])
            else: 
                self.create_movement_animation(self.sprite, self.chose_sprite(self.current_target).pos[0]+250,self.chose_sprite(self.current_target).pos[1])
            self.create_movement_animation(self.text_pop, self.chose_sprite(self.current_target).pos[0]-635,self.chose_sprite(self.current_target).pos[1]-205)
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
        elif self.distance == "ranged":
            self.animation_type = "_magic"
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
            self.create_movement_animation(self.text_pop, self.chose_sprite(self.current_target).pos[0]-635,self.chose_sprite(self.current_target).pos[1]-205)
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
        elif self.distance == "heal":
            self.animation_type = "_magic"
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
            self.create_movement_animation(self.text_pop, self.chose_sprite(self.current_target).pos[0]-635,self.chose_sprite(self.current_target).pos[1]-205)
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
        elif self.distance == "status":
            self.animation_type = "_magic"
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
            self.create_movement_animation(self.text_pop, self.chose_sprite(self.current_target).pos[0]-635,self.chose_sprite(self.current_target).pos[1]-205)
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
        else:
            self.animation_type = "_attack"
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
            self.create_movement_animation(self.text_pop, self.chose_sprite(self.current_target).pos[0]-635,self.chose_sprite(self.current_target).pos[1]-205)
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
        
        if self.current_turn in player.team:
            self.current_turn.MP -= self.MP_cost
        self.action_status = ""

    def check_for_exceed_HP_MP(self):
        if self.current_target in player.team and self.current_target.MP > self.current_target.MAX_MP:
            self.current_target.MP = self.current_target.MAX_MP
        if self.current_target.HP > self.current_target.MAX_HP:
            self.current_target.HP = self.current_target.MAX_HP
    def add_status(self,status):
        self.current_target.status.append([se.status_effect.status_list[status].copy(),se.Status_Icon(se.status_effect.status_list[status][3],se.status_effect.status_list[status][6]),Label(font_size = 22)])
        #self.final_damage = str(self.final_damage)+' '+status

    def attack(self,target):
        self.target = target

        ### activate skills and decide targets 
        for x in self.skill_list_pop_up.children:
            x.disabled = False
        if self.target_type == "on_enemy":
            self.current_target = enemy.enemy_team[self.target]
            self.target_sprite = self.chose_sprite(self.current_target)
        else:
            self.current_target = player.team[self.target]
            self.target_sprite = self.chose_sprite(self.current_target)
        
        self.calculate_damage(target)
        
        for x in self.target_option:
            self.remove_widget(self.target_option[x][0])
        self.remove_widget(self.skill_list_pop_up)
        self.remove_widget(self.resign_button)
        self.run_animation()

    def action_attack(self):
        self.disable_control()
        self.final_damage = self.current_turn.damage
        self.MP_cost = 0
        self.distance = "melee"
        self.target_type = "on_enemy"
        self.action = "self.final_damage = self.current_turn.damage"
        self.add_widget(self.resign_button)
        self.chose_target("on_enemy")

    def resign_action(self):
        for x in self.skill_list_pop_up.children:
            x.disabled = False
        self.skill_list_pop_up.list.clear_widgets()
        self.remove_widget(self.skill_list_pop_up)
        for x in self.target_option:
            self.remove_widget(self.target_option[x][0])
        self.remove_widget(self.resign_button)
        self.restore_control()

    def chosen_skill(self,skill,MP,distance,target):

        if self.current_turn.MP < MP:
            self.resign_action()
            tp.text_pop.text = "Nie masz wystarczająco many!"
            Clock.schedule_interval(tp.clear_pop_up,2)
        else:
            for x in self.skill_list_pop_up.children:
                x.disabled = True
            exec(skill)
            self.MP_cost = MP
            self.distance = distance
            self.target_type = target
            self.chose_target(target)
    def action_spells(self):
        self.disable_control()
        self.add_widget(self.resign_button)
        self.skill_list_pop_up.list.clear_widgets()
        for x in self.current_turn.skill:
            if self.current_turn.skill[x][4] != "passive":
                self.skill_list_pop_up.list.add_widget(sk.Skill_Record(self.current_turn.skill[x][2], text=x+" "+str(self.current_turn.skill[x][1]),halign = "left", valign="middle" ,font_size = 20, color=(0,0,0,1), on_press = (lambda y, x=x:self.chosen_skill(self.current_turn.skill[x][0],self.current_turn.skill[x][1],self.current_turn.skill[x][5],self.current_turn.skill[x][6]))))
                pass
        self.add_widget(self.skill_list_pop_up)
        
    
    def enemy_action(self,e):
            enemy.current = e    
            temp = e.set_actions()
            self.current_target = temp[0]
            self.target_sprite = self.chose_sprite(self.current_target)
            #self.action = temp[1]
            exec(temp[1])
            self.distance = temp[3]
            if temp[2] != "":
                tp.text_pop.text = self.current_turn.name+" używa: "+temp[2]
            Clock.schedule_interval(tp.clear_pop_up,2)

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
        self.sprite = self.chose_sprite(e)
        self.current_turn = e 
        self.check_for_status()
        self.status_menagment()
                
        ### if player turn, set pointer ###
        if e in enemy.player_team_alive:            
            self.pointer.pos = (self.chose_sprite(self.current_turn).pos[0]-500,self.chose_sprite(self.current_turn).pos[1]-205)
            
    def next_turn(self):
        self.check_for_victory_or_defeat()
        if self.battle_end == False:
            self.turn_number -= 1
            if self.turn_number < 0:
                self.turn_number = len(self.turn_order)-1
            if self.turn_order[self.turn_number] != "dead":
                self.take_action(self.turn_order[self.turn_number])
            else:
                self.next_turn()
        else:
            return False
