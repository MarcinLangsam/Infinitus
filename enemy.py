# -*- coding: utf-8 -*-
import player,inventory_manager as im, random, status_effect as se, codecs
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

global player_team_alive
global enemy_team_alive
player_team_alive = player.team

current = 0

class Enemy_Sprite(Widget):
    sprite = ObjectProperty("")
    weapon = ObjectProperty("")
    head = ""
    effect = ObjectProperty("graphics/effects/no_effect.png")

    def __init__(self,enemy_sprite,source,**kwargs):
        super().__init__(**kwargs)
        self.time = 0.0
        self.rate= 0.0001
        self.frame = 1
        self.source = source
        self.frame_sum = 46
        self.weapon_source = "empty_slot"
        self.effect_source = ""
        self.head_source = ""
        self.sprite = enemy_sprite
        self.set_sprite()
                
    def set_sprite(self):
        self.sprite = self.sprite
        self.anim = self.source
        
    def set_anim_parameters(self,time,rate,frame,frame_sum):
        self.time = time
        self.rate = rate
        self.frame = frame
        self.frame = frame_sum

class Enemy(Widget):
    def __init__(self, name, lv, MAX_HP, STR, DEX, INT, damage, defence, exp_gain, gold_gain,AI, enemy_drop,enemy_sprite,source):
        super().__init__()
        self.name = name
        self.lv = lv
        self.MAX_HP = MAX_HP
        self.HP = MAX_HP
        self.STR = STR
        self.DEX = DEX
        self.INT = INT
        self.defence = defence
        self.crit_chance = DEX*0.1
        self.dodge_chance = DEX*0.1
        self.damage = damage
        self.damage_bonus = 0
        self.damage_special_effect = ""
        self.exp_gain = exp_gain
        self.gold_gain = gold_gain
        self.AI = AI
        self.enemy_drop = enemy_drop
        self.enemy_sprite = enemy_sprite
        self.status = list()
        self.actions = list()
        self.source = source

    def action(self,action,sort_by,value,type,name,distance,effect):
        ok = False
        if type in ["on_character","attack","on_all_character"]:
            targets = player_team_alive
        if type == "on_enemy" or "on_all_enemy":
            targets = enemy_team_alive
        if type == "on_self":
            targets = current
        

        if sort_by == "by_HP":
            if type == "on_self":
                if targets.HP <= targets.MAX_HP*value:
                    self.actions.append([targets,action,name,distance,type,effect])
            else:
                for x in targets:
                    if x.HP <= x.MAX_HP*value:
                        self.actions.append([x,action,name,distance,type,effect])
        if sort_by == "by_HP_alter":
            if type == "on_self":
                if targets.HP >= targets.MAX_HP*value:
                    self.actions.append([targets,action,name,distance,type,effect])
            else:
                for x in targets:
                    if x.HP >= x.MAX_HP*value:
                        self.actions.append([x,action,name,distance,type,effect])
                        
        if sort_by == "by_MP":
            if type == "on_self":
                if targets.MP <= targets.MAX_MP*value:
                    self.actions.append([targets,action,name,distance,type,effect])
            else:
                for x in targets:
                    if x.MP <= x.MAX_MP*value:
                        self.actions.append([x,action,name,distance,type,effect])
        if sort_by == "by_MP_alter":
            if type == "on_self":
                if targets.MP >= targets.MAX_MP*value:
                    self.actions.append([targets,action,name,distance,type,effect])
            else:
                for x in targets:
                    if x.MP >= x.MAX_MP*value:
                        self.actions.append([x,action,name,distance,type,effect])

        if sort_by == "by_STR":
            if type == "on_self":
                self.actions.append([targets,action,name,distance,type,effect])
            else: 
                max = 0
                final_target = targets[0]
                for x in targets:
                    if x.STR >= max:
                        max = x.STR
                        final_target = x
                self.actions.append([final_target,action,name,distance,type,effect])
        
        if sort_by == "by_DEX":
            if type == "on_self":
                self.actions.append([targets,action,name,distance,type,effect])
            else: 
                max = 0
                final_target = targets[0]
                for x in targets:
                    if x.DEX >= max:
                        max = x.DEX
                        final_target = x
                self.actions.append([final_target,action,name,distance,type,effect])

        if sort_by == "by_INT":
            if type == "on_self":
                self.actions.append([targets,action,name,distance,type,effect])
            else: 
                max = 0
                final_target = targets[0]
                for x in targets:
                    if x.INT >= max:
                        max = x.INT
                        final_target = x
                self.actions.append([final_target,action,name,distance,type,effect])

        if sort_by == "by_defence":
            if type == "on_self":
                self.actions.append([targets,action,name,distance,type,effect])
            else: 
                max = 0
                final_target = targets[0]
                for x in targets:
                    if x.defence >= max:
                        max = x.defence
                        final_target = x
                self.actions.append([final_target,action,name,distance,type,effect])

        if sort_by == "by_status":
            if type == "on_self":
                    for x in targets.status:
                        if se.status_effect.status_list[value][0] == x[0][0]:
                            ok = True
                    if ok == False:
                        self.actions.append([targets,action,name,distance,type,effect])
            else:
                for x in targets:
                    ok = False
                    for y in x.status:
                        if se.status_effect.status_list[value][0] == y[0][0]:
                            ok = True
                    if ok == False:
                        self.actions.append([x,action,name,distance,type,effect])

        ###################################################################
        if type in ["attack","on_all_character","on_character"]:
            chanse = random.randint(0,100)
            if len(targets) == 1:
                self.actions.append([player_team_alive[0],action,name,distance,type,effect])
            if len(targets) == 2:
                if chanse >=0 and chanse <= 40:
                    self.actions.append([player_team_alive[0],action,name,distance,type,effect])
                elif chanse > 40 and chanse <= 100:
                    self.actions.append([player_team_alive[1],action,name,distance,type,effect])
            if len(targets) == 3:
                if chanse >=0 and chanse <= 20:
                    self.actions.append([player_team_alive[0],action,name,distance,type,effect])
                elif chanse > 20 and chanse <= 70:
                    self.actions.append([player_team_alive[1],action,name,distance,type,effect])
                elif chanse > 70 and chanse <= 100:
                    self.actions.append([player_team_alive[2],action,name,distance,type,effect])
        elif type == "on_all_enemy":
            chanse = random.randint(0,100)
            if len(targets) == 1:
                self.actions.append([enemy_team_alive[0],action,"",distance,type,effect])
            if len(targets) == 2:
                if chanse >=0 and chanse <= 40:
                    self.actions.append([enemy_team_alive[0],action,"",distance,type,effect])
                elif chanse > 40 and chanse <= 100:
                    self.actions.append([enemy_team_alive[1],action,"",distance,type,effect])
            if len(targets) == 3:
                if chanse >=0 and chanse <= 20:
                    self.actions.append([enemy_team_alive[0],action,"",distance,type,effect])
                elif chanse > 20 and chanse <= 70:
                    self.actions.append([enemy_team_alive[1],action,"",distance,type,effect])
                elif chanse > 70 and chanse <= 100:
                    self.actions.append([enemy_team_alive[2],action,"",distance,type,effect])
                    
        
    def set_actions(self):
        self.actions.clear()
        for x in self.AI:
            self.action(enemy_skills[x][1],enemy_skills[x][2],enemy_skills[x][3],enemy_skills[x][4],enemy_skills[x][0],enemy_skills[x][5],enemy_skills[x][6])
        chose = random.randint(0,len(self.actions)-1)
        return self.actions[chose]

    def drop_mashine(self):
        drop_roll = random.randint(0,100)
        items_droped = list()
        count = 0
        for x in self.enemy_drop.keys():
            if drop_roll < self.enemy_drop[x]:
                items_droped.append(x)
        for x in range(48,48+len(items_droped)):
            player.current_player.inventory[x][2] = items_droped[count]
            count += 1

enemy_skills ={}

def load_enemy_skill():
    data =["","","","","","","",""]
    count = 0
    with codecs.open("enemy_skill_list.txt",'r','utf-8') as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line[0] == "_":
                pass 
            else:
                data[count] = line.strip().replace(r'\n','\n')
                if count == 3 and len(data[count]) <= 4:
                        data[count] = int(data[count])
                if count == 4 and len(data[count]) <= 4:
                        data[count] = float(data[count])
                count+=1             
                if count == 8: # <--- amout of separated data for one item/skill/status, change appropriately
                    enemy_skills[data[0]] = [data[1],data[2],data[3],data[4],data[5],data[6],data[7]]
                    count=0
    f.close()

load_enemy_skill()

                #nazwa #lv #MAX_HP #STR #DEX #INT #Obrażenia #Pancerz #EXP #Złoto #AI #drop #sprite
first_enemy = Enemy("Szkielet",1,60,10,1,1,10,0,100,50,{"atak":enemy_skills["atak"],"atak":enemy_skills["atak"],"szarża":enemy_skills["szarża"],"blok":enemy_skills["blok"]},{"graphics/items/mała_mikstura_zdrowia.png":100},"graphics/sprites/szkielet_sprite.png","szkielet")
                
skeleton1 = Enemy("Szkielet",2,40,10,1,5,10,0,20,5,{"atak":enemy_skills["atak"],"szarża":enemy_skills["szarża"],"blok":enemy_skills["blok"]},{},"graphics/sprites/szkielet_sprite.png","szkielet")
skeleton2 = Enemy("Szkielet",2,40,10,1,5,10,0,20,5,{"atak":enemy_skills["atak"],"szarża":enemy_skills["szarża"],"blok":enemy_skills["blok"]},{},"graphics/sprites/szkielet_sprite.png","szkielet")
skeleton3 = Enemy("Szkielet",2,40,10,1,5,10,0,20,5,{"atak":enemy_skills["atak"],"szarża":enemy_skills["szarża"],"blok":enemy_skills["blok"]},{},"graphics/sprites/szkielet_sprite.png","szkielet")

skeleton_priest = Enemy("Upadły kapłan",3,60,10,15,15,10,0,40,15,{"atak":enemy_skills["atak"],"leczenie":enemy_skills["leczenie"],"klatwa":enemy_skills["klatwa"],"klatwa":enemy_skills["klatwa"]},{},"upadly_kaplan_sprite.png","upadly_kaplan")

lost_soul = Enemy("Zagubiona Dusza",4,130,20,20,20,20,5,100,0,{"atak":enemy_skills["atak"],"atak":enemy_skills["atak"],"duch":enemy_skills["duch"],"zimny jak lód":enemy_skills["zimny jak lód"],"zimny jak lód":enemy_skills["zimny jak lód"],"zimny jak lód":enemy_skills["bisekcja"],"zimny jak lód":enemy_skills["bisekcja"]},{"graphics/items/pierscien_sily.png":50},"zagubiona_dusza_sprite.png","zagubiona_dusza")

zjawa = Enemy("Zjawa",3,100,10,20,25,15,0,40,15,{"atak":enemy_skills["atak"],"duch":enemy_skills["duch"],"duch":enemy_skills["duch"],},{},"graphics/sprites/zjawa_sprite.png","zjawa")

skeleton_warrior = Enemy("Szkielet Wojownik",3,150,25,5,1,25,10,40,15,{"atak":enemy_skills["atak"],"szal wojownika":["szal wojownika"],"szal wojownika":["szal wojownika"],"szal wojownika":["szal wojownika"],"szal wojownika":["szal wojownika"]},{},"graphics/sprites/szkielet_wojownik.png","szkielet_wojownik")

rzeznik = Enemy("Rzeznik",5,350,30,20,10,30,10,100,40,{"atak":enemy_skills["atak"],"tortury":["tortury"],"kat":["kat"],"kat":["kat"],"swad_smierci":["swad_smierci"]},{},"graphics/sprites/szkielet_wojownik.png","szkielet_wojownik")

zombie = Enemy("Zombie",5,250,30,10,30,30,0,70,20,{"atak":enemy_skills["atak"],"zarodniki":["zarodniki"],"zarodniki":["zarodniki"],"zarodniki":["zarodniki"],"trujace_opary":["trujace_opary"],"trujace_opary":["trujace_opary"],"trujace_opary":["trujace_opary"],"trujace_opary":["trujace_opary"]},{},"graphics/sprites/szkielet_wojownik.png","szkielet_wojownik")

 
death_knight = Enemy("Rycerz Śmierci",3,500,50,20,35,30,0,500,1000,{"atak":enemy_skills["atak"],"fala_śmierci":enemy_skills["fala_śmierci"],"kojące_dźwięki":enemy_skills["kojące_dźwięki"]},{},"graphics/sprites/rycerz_smierci_sprite.png","rycerz_smierci")
death_knight2 = Enemy("Rycerz Śmierci",3,500,50,20,35,30,20,500,1000,{"atak":enemy_skills["atak"],"fala_śmierci":enemy_skills["fala_śmierci"],"kojące_dźwięki":enemy_skills["kojące_dźwięki"]},{},"graphics/sprites/rycerz_smierci_sprite.png","rycerz_smierci")
death_knight3 = Enemy("Rycerz Śmierci",3,500,50,20,35,30,20,500,1000,{"atak":enemy_skills["atak"],"fala_śmierci":enemy_skills["fala_śmierci"],"kojące_dźwięki":enemy_skills["kojące_dźwięki"]},{},"graphics/sprites/rycerz_smierci_sprite.png","rycerz_smierci")

enemy_team = list()
enemy_team.append(skeleton1)
enemy_team.append(skeleton2)
enemy_team.append(skeleton3)
enemy_team_alive = list()

#character - after this fight you gey new companion(max 2 at playthrough), one-time - this fight dont count to random fight, normal - well..it's normal XD
story_fight = {
    1:{
        1:[[first_enemy],"one-time"],
        2:[[skeleton1,skeleton2],"normal"],
        3:[[skeleton_priest,skeleton1],"normal"],
        4:[[lost_soul],"character"],
        5:[[zjawa,skeleton_warrior],"normal"],
        6:[[rzeznik,skeleton_priest,skeleton_priest],"normal"],
        7:[[zombie,zombie],"normal"],
        8:[[skeleton_warrior,skeleton_warrior,skeleton_warrior],"normal"],
        9:[[skeleton_warrior,zombie,skeleton_priest],"normal"],
        10:[[death_knight],"one_time"]
        #1:[[death_knight,death_knight2,death_knight3],"normal"],
        #2:[[death_knight],"normal"],
        #3:[[death_knight,death_knight2,death_knight3],"normal"]
    }
}