import player, enemy, skill_record as sk, status_effect as se, tooltip as tt,random, text_pop as tp
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

current_stage = 1
current_fight = 1
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
        self.list.bind(minimum_height=self.list.setter('height'))

class Fight(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_turn = 0
        self.current_target = 0
        self.player_sprites = []
        self.enemy_sprites = []
        self.sprite = enemy.Enemy_Sprite(enemy.enemy_team[0].enemy_sprite,pos=(950,500))
        self.anim_queue = []
        self.turn_order = list()
        self.target_option = {}
        self.target = 0
        self.turn_number = 0
        self.action = ""
        self.resign_button = Button(size_hint=(0.09,0.113), pos=(900,0), on_press = lambda y:self.resign_action(), background_normal="graphics/back_button.png")
        #self.enemy_team_alive = list()
        self.enemy_team = list()
        self.battle_end = False
        self.if_attack = True
        self.text_pop = Label(font_size = 30)
        self.final_damage = 0
        self.MP_cost = 0
        self.distance = 0
        self.target_type = 0
        self.skill_list_pop_up = Skill_List_Pop_Up()
        self.crit_roll = 0
        self.dodge_roll = 0
        self.pointer = Image(pos=(0,0), source="graphics/pointer.png")
        self.target_pointer = Image(pos=(0,0), source="graphics/pointer.png")
        self.status_modificator = list()

    def clear_after_battle(self):
        for x in range(0,len(player.team)):
            for y in range(0,6):
                self.remove_widget(self.player_sprites[x][y])
        for x in range(0,len(enemy.enemy_team)):
            for y in range(0,4):
                self.remove_widget(self.enemy_sprites[x][y])
        self.remove_widget(tt.tooltip_status)
        self.remove_widget(self.pointer)
        self.remove_widget(tp.text_pop)
        self.remove_widget(self.text_pop)
        
        
    def prepare_battle_visuals(self):
        self.player_sprites.clear()
        self.enemy_sprites.clear()
        if len(player.team) >=1:
            self.player_sprites.append([player.Character_Sprite(player.main_player,pos=(410,380)),
                                        HPBar(pos=(30,80), max=player.team[0].MAX_HP, value=player.team[0].HP, size_hint=(0.18,0.1)),
                                        MPBar(pos=(30,60), max=player.team[0].MAX_MP, value=player.team[0].MP, size_hint=(0.18,0.1)),
                                        Label(text=(("HP: ") + str(player.team[0].HP) + ("/") + str(player.team[0].MAX_HP)),pos=(-600,-310)),
                                        Label(text=(("MP: ") + str(player.team[0].MP) + ("/") + str(player.team[0].MAX_MP)),pos=(-600,-330)),
                                        Label(text=player.team[0].name,pos=(-600,-290))
                                        ])
        if len(player.team) >=2:
            self.player_sprites.append([player.Character_Sprite(player.companion1,pos=(205,490)),
                                        HPBar(pos=(30,140), max=player.team[1].MAX_HP, value=player.team[1].HP, size_hint=(0.18,0.1)),
                                        MPBar(pos=(30,120), max=player.team[1].MAX_MP, value=player.team[1].MP, size_hint=(0.18,0.1)),
                                        Label(text=(("HP: ") + str(player.team[1].HP) + ("/") + str(player.team[1].MAX_HP)),pos=(-600,-250)),
                                        Label(text=(("MP: ") + str(player.team[1].MP) + ("/") + str(player.team[1].MAX_MP)),pos=(-600,-270)),
                                        Label(text=player.team[1].name,pos=(-600,-230))
                                        ])
        if len(player.team) >=3:
            self.player_sprites.append([player.Character_Sprite(player.companion2,pos=(260,200)),
                                        HPBar(pos=(30,20), max=player.team[2].MAX_HP, value=player.team[2].HP, size_hint=(0.18,0.1)),
                                        MPBar(pos=(30,0), max=player.team[2].MAX_MP, value=player.team[2].MP, size_hint=(0.18,0.1)),
                                        Label(text=(("HP: ") + str(player.team[2].HP) + ("/") + str(player.team[2].MAX_HP)),pos=(-600,-370)),
                                        Label(text=(("MP: ") + str(player.team[2].MP) + ("/") + str(player.team[2].MAX_MP)),pos=(-600,-390)),
                                        Label(text=player.team[2].name,pos=(-600,-350))
                                        ])
        if len(enemy.enemy_team) >=1:
            self.enemy_sprites.append([enemy.Enemy_Sprite(enemy.enemy_team[0].enemy_sprite,pos=(800,380)),
                                       EnemyHPBar(pos=(1220,80), max=enemy.enemy_team[0].MAX_HP, value=enemy.enemy_team[0].HP, size_hint=(0.18,0.1)),
                                       Label(text=(("HP: ") + str(enemy.enemy_team[0].HP) + ("/") + str(enemy.enemy_team[0].MAX_HP)),pos=(590,-310)),
                                       Label(text=enemy.enemy_team[0].name,pos=(590,-290))
                                       ])
        if len(enemy.enemy_team) >=2:
            self.enemy_sprites.append([enemy.Enemy_Sprite(enemy.enemy_team[1].enemy_sprite,pos=(985,490)),
                                       EnemyHPBar(pos=(1220,140), max=enemy.enemy_team[1].MAX_HP, value=enemy.enemy_team[1].HP, size_hint=(0.18,0.1)),
                                       Label(text=(("HP: ") + str(enemy.enemy_team[1].HP) + ("/") + str(enemy.enemy_team[1].MAX_HP)),pos=(590,-250)),
                                       Label(text=enemy.enemy_team[1].name,pos=(590,-230))
                                       ])
        if len(enemy.enemy_team) >=3:
            self.enemy_sprites.append([enemy.Enemy_Sprite(enemy.enemy_team[2].enemy_sprite,pos=(920,200)),
                                       EnemyHPBar(pos=(1220,20), max=enemy.enemy_team[2].MAX_HP, value=enemy.enemy_team[2].HP, size_hint=(0.18,0.1)),
                                       Label(text=(("HP: ") + str(enemy.enemy_team[2].HP) + ("/") + str(enemy.enemy_team[2].MAX_HP)),pos=(590,-370)),
                                       Label(text=enemy.enemy_team[2].name,pos=(590,-350))
                                       ])
        for x in range(0,len(player.team)):
            for y in range(0,6):
                self.add_widget(self.player_sprites[x][y])
        for x in range(0,len(enemy.enemy_team)):
            for y in range(0,4):
                self.add_widget(self.enemy_sprites[x][y])
        self.add_widget(tt.tooltip_status)
        self.add_widget(self.pointer)
        self.add_widget(tp.text_pop)
        self.add_widget(self.text_pop)
        

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
            #for x in range(0,len(self.target_option)-3):
            print(len(enemy.enemy_team))
            for x in range(0,len(enemy.enemy_team)):
                self.add_widget(self.target_option[x][0])
        else:
            #for x in range(3,len(self.target_option)-1):
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

    def set_pointer(self,target):
        self.target_pointer.pos = (self.chose_sprite(target).pos[0]-685,self.chose_sprite(target).pos[1]-205)
        
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
        #self.remove_widget(self.text_pop)
        return False
    def sprite_animation(self,dt):
        self.sprite.time += dt
        if (self.sprite.time > self.sprite.rate):
                self.sprite.time -= self.sprite.rate
                self.sprite.sprite = "atlas://"+self.sprite.source+"/"+self.sprite.anim + str(self.sprite.frame)
                self.sprite.weapon = "atlas://weapon_anim/"+self.sprite.weapon_source + str(self.sprite.frame)
                self.sprite.frame = self.sprite.frame + 1
                if (self.sprite.frame > self.sprite.frame_sum):
                    self.sprite.frame = 1
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
            self.anim_queue.append((widget, Animation(x=x_pos, y=y_pos, duration=0.7, t="in_out_quad")))
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
                #self.turn_order.remove(self.current_target)
                self.remove_widget(self.chose_sprite(self.current_target))
                if self.current_target in player.team:
                    enemy.player_team_alive.remove(self.current_target)
                    #self.player_sprites.remove(self.player_sprites[self.chose_enemy_index(self.current_target)])
                else:
                    self.target_option[self.chose_enemy_index(self.current_target)][0] = Button(pos=(10000,10000), size=(1,1)) 
                    enemy.enemy_team_alive.remove(self.current_target)
                    #self.enemy_sprites.remove(self.enemy_sprites[self.chose_enemy_index(self.current_target)])
                #self.turn_number -= 1
        
        
        if self.current_turn.HP <= 0:
            if self.current_turn in self.turn_order:
                self.turn_order[self.get_turn_index(self.current_turn)] = "dead"
                #self.turn_order.remove(self.current_turn)
                self.remove_widget(self.chose_sprite(self.current_turn))
                if self.current_turn in player.team:
                    enemy.player_team_alive.remove(self.current_turn)
                    #self.player_sprites.remove(self.player_sprites[self.chose_enemy_index(self.current_turn)])
                else:
                    self.target_option[self.chose_enemy_index(self.current_turn)][0] = Button(pos=(10000,10000), size=(1,1)) 
                    enemy.enemy_team_alive.remove(self.current_turn)
                    #self.enemy_sprites.remove(self.enemy_sprites[self.chose_enemy_index(self.current_turn)])
                #self.turn_number -= 1
        
        #if self.current_target.HP <= 0:
        #    if self.current_target in self.turn_order:
        #        self.turn_order.remove(self.current_target)
        #        self.remove_widget(self.chose_sprite(self.current_target))
        #        self.target_option[self.chose_enemy_index(self.current_target)][0] = Button(pos=(10000,10000), size=(1,1)) 
        #        self.current_target_team_alive.remove(self.current_target)
        #        self.turn_number -= 1
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
                    self.current_turn.status[x][1].pos = (self.player_sprites[self.chose_enemy_index(self.current_turn)][1].pos[0]+280+x*30,self.player_sprites[self.chose_enemy_index(self.current_turn)][1].pos[1]+30)
                    self.current_turn.status[x][2].pos = (self.player_sprites[self.chose_enemy_index(self.current_turn)][1].pos[0]-480+x*30,self.player_sprites[self.chose_enemy_index(self.current_turn)][1].pos[1]-390)
                else:
                    self.current_turn.status[x][1].pos = (self.enemy_sprites[self.chose_enemy_index(self.current_turn)][1].pos[0]-25+-x*30,self.enemy_sprites[self.chose_enemy_index(self.current_turn)][1].pos[1]+30)
                    self.current_turn.status[x][2].pos = (self.enemy_sprites[self.chose_enemy_index(self.current_turn)][1].pos[0]-785-x*30,self.enemy_sprites[self.chose_enemy_index(self.current_turn)][1].pos[1]-390)
                self.current_turn.status[x][2].text = str(self.current_turn.status[x][0][2])
                self.add_widget(self.current_turn.status[x][1])
                self.add_widget(self.current_turn.status[x][2])

                if self.current_turn.status[x][0][4] == "every_turn":
                    exec(self.current_turn.status[x][0][1])

    def start_status(self):
            if len(self.current_target.status) != 0:
                if self.current_target in enemy.player_team_alive:
                    self.current_target.status[-1][1].pos = (self.player_sprites[self.chose_enemy_index(self.current_target)][1].pos[0]+280+(len(self.current_target.status)-1)*30,self.player_sprites[self.chose_enemy_index(self.current_target)][1].pos[1]+30)
                    self.current_target.status[-1][2].pos = (self.player_sprites[self.chose_enemy_index(self.current_target)][1].pos[0]-480+(len(self.current_target.status)-1)*30,self.player_sprites[self.chose_enemy_index(self.current_target)][1].pos[1]-390)
                else:
                    self.current_target.status[-1][1].pos = (self.enemy_sprites[self.chose_enemy_index(self.current_target)][1].pos[0]-25-(len(self.current_target.status)-1)*30,self.enemy_sprites[self.chose_enemy_index(self.current_target)][1].pos[1]+30)
                    self.current_target.status[-1][2].pos = (self.enemy_sprites[self.chose_enemy_index(self.current_target)][1].pos[0]-785-(len(self.current_target.status)-1)*30,self.enemy_sprites[self.chose_enemy_index(self.current_target)][1].pos[1]-390)
                self.current_target.status[-1][2].text = str(self.current_target.status[-1][0][2])
                if self.current_target.status[-1][0][4] != "every_turn":
                    exec(self.current_target.status[-1][0][1])
                
                self.add_widget(self.current_target.status[-1][1])
                self.add_widget(self.current_target.status[-1][2])
    def update_status(self):
        for x in range(0,len(self.player_sprites)):
            self.player_sprites[x][1].value = player.team[x].HP
            self.player_sprites[x][2].value = player.team[x].MP
            self.player_sprites[x][3].text = "HP: " + str(player.team[x].HP) + "/" + str(player.team[x].MAX_HP)
            self.player_sprites[x][4].text = "MP: " + str(player.team[x].MP) + "/" + str(player.team[x].MAX_MP)
        for y in range(0,len(self.enemy_sprites)):
            self.enemy_sprites[y][1].value = enemy.enemy_team[y].HP
            self.enemy_sprites[y][2].text = "HP: " + str(enemy.enemy_team[y].HP) + "/" + str(enemy.enemy_team[y].MAX_HP)


    def attack(self,target):
        self.target = target

        self.dodge_roll = random.randint(0,100)
        self.crit_roll = random.randint(0,100)
        
        for x in self.skill_list_pop_up.children:
            x.disabled = False
        if self.target_type == "on_enemy":
            self.current_target = enemy.enemy_team[self.target]
        else:
            self.current_target = player.team[self.target]
        exec(self.action)
        if self.distance == "melee":
            if self.crit_roll < self.current_turn.crit_chance:
                self.final_damage = self.final_damage+(self.final_damage*0.5)
                self.action = "self.current_target.HP -= self.final_damage\nself.final_damage = 'TRAFIENIE KRYTYCZNE '+str(self.final_damage)+'!'"
            if self.dodge_roll < self.current_target.dodge_chance:
                self.action = "self.final_damage = 'PUDŁO!'"
            if (self.final_damage - self.current_target.defence) < 5:
                
                self.final_damage = 5
            else:
                self.final_damage -= self.current_target.defence 
            exec("self.current_target.HP -= self.final_damage")
            #exec(self.action)
            self.create_movement_animation(self.sprite, self.target_option[target][1][0]-100, self.target_option[target][1][1])
            self.create_movement_animation(self.text_pop, self.chose_sprite(self.current_target).pos[0]-635,self.chose_sprite(self.current_target).pos[1]-205)
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
        elif self.distance == "ranged":
            if self.crit_roll >= self.current_turn.crit_chance:
                self.final_damage = self.final_damage+(self.final_damage*0.5)
                self.action = "self.current_target.HP -= self.final_damage\nself.final_damage = 'TRAFIENIE KRYTYCZNE '+str(self.final_damage)+'!'"
            if self.dodge_roll >= self.current_target.dodge_chance:
                self.action = "self.final_damage = 'PUDŁO!'"
            if self.final_damage - self.current_target.defence < 5:
                self.final_damage == 5
            else:
                self.final_damage -= self.current_target.defence 
            exec("self.current_target.HP -= self.final_damage")
            #exec(self.action)
            if self.current_target in enemy.player_team_alive:
                if self.current_target.MP > self.current_target.MAX_MP:
                    self.current_target.MP = self.current_target.MAX_MP
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
            self.create_movement_animation(self.text_pop, self.chose_sprite(self.current_target).pos[0]-635,self.chose_sprite(self.current_target).pos[1]-205)
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
        elif self.distance == "heal":
            exec("self.current_target.HP -= self.final_damage")
            #exec(self.action)
            if self.current_target in enemy.player_team_alive:
                if self.current_target.MP > self.current_target.MAX_MP:
                    self.current_target.MP = self.current_target.MAX_MP
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
            self.create_movement_animation(self.text_pop, self.chose_sprite(self.current_target).pos[0]-635,self.chose_sprite(self.current_target).pos[1]-205)
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
        else:
            exec(self.action)
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
            self.create_movement_animation(self.text_pop, self.chose_sprite(self.current_target).pos[0]-635,self.chose_sprite(self.current_target).pos[1]-205)
            self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
            self.start_status()
        
        if self.current_target.HP > self.current_target.MAX_HP:
            self.current_target.HP = self.current_target.MAX_HP   
        self.current_turn.MP -= self.MP_cost
        
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
        else:
            #exec(skill)
            for x in self.skill_list_pop_up.children:
                x.disabled = True
            self.action = skill
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
        self.add_widget(self.skill_list_pop_up)
        
    
    def enemy_action(self,e):
            enemy.current = e    
            temp = e.set_actions()
            self.current_target = temp[0]
            self.action = temp[1]
            self.distance = temp[3]
            if temp[2] != "":
                tp.text_pop.text = self.current_turn.name+" używa: "+temp[2]
            Clock.schedule_interval(tp.clear_pop_up,2)

            if self.distance == "melee":
                exec(self.action)
                self.dodge_roll = random.randint(0,100)
                self.crit_roll = random.randint(0,100)
                if self.crit_roll < self.current_turn.crit_chance:
                    self.final_damage = self.final_damage+(self.final_damage*0.5)
                    self.action = "self.current_target.HP -= self.final_damage\nself.final_damage = 'TRAFIENIE KRYTYCZNE '+str(self.final_damage)+'!'"
                if self.dodge_roll < self.current_target.dodge_chance:
                    self.action = "self.final_damage = 'PUDŁO!'"
                if self.final_damage - self.current_target.defence < 5:
                    self.final_damage == 5
                else:
                    self.final_damage -= self.current_target.defence 
                exec("self.current_target.HP -= self.final_damage")
                self.create_movement_animation(self.sprite, self.chose_sprite(self.current_target).pos[0]+100,self.chose_sprite(self.current_target).pos[1])
                self.create_movement_animation(self.text_pop, self.chose_sprite(self.current_target).pos[0]-635,self.chose_sprite(self.current_target).pos[1]-205)
                self.create_movement_animation(self.sprite, self.sprite.pos[0],self.sprite.pos[1])    
            elif self.distance == "ranged":
                exec(self.action)
                self.dodge_roll = random.randint(0,100)
                self.crit_roll = random.randint(0,100)
                if self.crit_roll < self.current_turn.crit_chance:
                    self.final_damage = self.final_damage+(self.final_damage*0.5)
                    self.action = "self.current_target.HP -= self.final_damage\nself.final_damage = 'TRAFIENIE KRYTYCZNE '+str(self.final_damage)+'!'"
                if self.dodge_roll < self.current_target.dodge_chance:
                    self.action = "self.final_damage = 'PUDŁO!'"
                if self.final_damage - self.current_target.defence < 5:
                    self.final_damage == 5
                else:
                    self.final_damage -= self.current_target.defence 
                exec("self.current_target.HP -= self.final_damage")
                self.create_movement_animation(self.sprite, self.sprite.pos[0],self.sprite.pos[1])
                self.create_movement_animation(self.text_pop, self.chose_sprite(self.current_target).pos[0]-635,self.chose_sprite(self.current_target).pos[1]-205)
                self.create_movement_animation(self.sprite, self.sprite.pos[0],self.sprite.pos[1])
            elif self.distance == "heal":
                exec("self.current_target.HP -= self.final_damage")
                #exec(self.action)
                if self.current_target in enemy.player_team_alive:
                    if self.current_target.MP > self.current_target.MAX_MP:
                        self.current_target.MP = self.current_target.MAX_MP
                self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
                self.create_movement_animation(self.text_pop, self.chose_sprite(self.current_target).pos[0]-635,self.chose_sprite(self.current_target).pos[1]-205)
                self.create_movement_animation(self.sprite, self.sprite.pos[0], self.sprite.pos[1])
            elif self.distance == "status":
                exec(self.action)
                self.start_status()
                self.create_movement_animation(self.sprite, self.sprite.pos[0],self.sprite.pos[1])
                self.create_movement_animation(self.text_pop, self.chose_sprite(self.current_target).pos[0]-635,self.chose_sprite(self.current_target).pos[1]-205)
                self.create_movement_animation(self.sprite, self.sprite.pos[0],self.sprite.pos[1])
            
            if self.current_target.HP > self.current_target.MAX_HP:
                self.current_target.HP = self.current_target.MAX_HP
            self.run_animation()

    def take_action(self,e):
        self.if_attack = True
        self.sprite = self.chose_sprite(e)
        self.current_turn = e 
        self.check_for_status()
        self.status_modificator.clear()
        for x in self.current_turn.status:
            if se.status_effect.status_list["ogluszenie"][0] == x[0][0]:
                self.status_modificator.append("ogluszenie")
            if se.status_effect.status_list["trucizna"][0] == x[0][0]:
                self.status_modificator.append("trucizna")
            if se.status_effect.status_list["zamrożenie"][0] == x[0][0]:
                self.status_modificator.append("zamrożenie")
                
        ### jeśli tura gracza ###
        if e in enemy.player_team_alive:
            self.restore_control()
            self.pointer.pos = (self.chose_sprite(self.current_turn).pos[0]-685,self.chose_sprite(self.current_turn).pos[1]-205)
            if "ogluszenie" in self.status_modificator:
                self.next_turn()
            if "trucizna" in self.status_modificator:
                self.update_status()
                self.check_for_death()
                self.check_for_victory_or_defeat()
                if self.current_turn.HP <= 0:
                    self.next_turn()
                
        ### jeśli tura przeciwnika ###
        if e in enemy.enemy_team_alive:
            self.disable_control()
            if "ogluszenie" in self.status_modificator:
                self.next_turn()
            if "trucizna" in self.status_modificator:
                self.update_status()
                self.check_for_death()
                self.check_for_victory_or_defeat()
                if self.current_turn.HP <= 0:
                    self.next_turn()
            if "zamrożenie" in self.status_modificator:
                self.update_status()
                self.check_for_death()
                self.check_for_victory_or_defeat()
                self.next_turn()
            if len(self.status_modificator) == 0:
                self.enemy_action(e)
            
    
    def next_turn(self):
        self.check_for_victory_or_defeat()
        
        #print(self.turn_order)
        #print("\n\n\n")
        if self.battle_end == False:
            self.turn_number -= 1
            if self.turn_number < 0:
                self.turn_number = len(self.turn_order)-1
            #print(self.turn_number)
            if self.turn_order[self.turn_number] != "dead":
                self.take_action(self.turn_order[self.turn_number])
            else:
                self.next_turn()
        else:
            return False
