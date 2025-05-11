# -*- coding: utf-8 -*-
import random, codecs, os, sys
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from resource_path import get_resource_path

global player_team_alive
global enemy_team_alive
from player import team
player_team_alive = team

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
        self.MP_regen = 0

        self.STR = STR
        self.DEX = DEX
        self.INT = INT

        self.STR_base = STR
        self.DEX_base = DEX
        self.INT_base = INT
        self.damage_base = damage
        self.defence_base = defence

        self.STR_modifier = 1
        self.DEX_modifier = 1
        self.INT_modifier = 1
        self.damage_modifier = 1
        self.defence_modifier = 1
        self.crit_chance_modifier = 0
        self.dodge_chance_modifier = 0
        self.damage_reduction = 1


        self.defence = defence
        self.crit_chance_base = round(0.1*self.DEX,2)
        self.dodge_chance_base = round(0.02*self.DEX,2)
        self.crit_chance = round(0.1*self.DEX,2)
        self.dodge_chance = round(0.02*self.DEX,2)
        self.damage = self.damage_base
        self.weapon = 0
        self.crit_chance_bonus = 0
        self.dodge_chance_bonus = 0
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

        self.blok = False

    def printBattleStats(self):
        print("STR "+str(self.STR))
        print("DEX "+str(self.DEX))
        print("INT "+str(self.INT))
        print("Final Damage "+str(self.damage))
        print("Defence "+str(self.defence))
        
        print("Damage modifier "+str(self.damage_modifier))
        print("STR modifier "+str(self.STR_modifier))
        print("DEX modifier "+str(self.DEX_modifier))
        print("INT modifier "+str(self.INT_modifier))
        print("Defence modifier "+str(self.defence_modifier))
        print("Damage modifier "+str(self.damage_modifier))
        print("Dodge: "+str(self.dodge_chance))

    def action(self,action,sort_by,value,type,name,distance,effect,sound,status):
        import status_effect as se
        ok = False
        if type in ["on_character","attack","on_all_character"]:
            targets = player_team_alive
            print(player_team_alive)
        if type in ["on_enemy","on_all_enemy"]:
            targets = enemy_team_alive
            print(enemy_team_alive)
        if type == "on_self":
            targets = current
        
        
        

        if sort_by == "by_HP":
            if type == "on_self":
                if targets.HP <= targets.MAX_HP*value:
                    self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    if x.HP <= x.MAX_HP*value:
                        self.actions.append([x,action,name,distance,type,effect,sound])
        if sort_by == "by_HP_alter":
            if type == "on_self":
                if targets.HP >= targets.MAX_HP*value:
                    self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    if x.HP >= x.MAX_HP*value:
                        self.actions.append([x,action,name,distance,type,effect,sound])
                        
        if sort_by == "by_MP":
            if type == "on_self":
                if targets.MP <= targets.MAX_MP*value:
                    self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    if x.MP <= x.MAX_MP*value:
                        self.actions.append([x,action,name,distance,type,effect,sound])
        if sort_by == "by_MP_alter":
            if type == "on_self":
                if targets.MP >= targets.MAX_MP*value:
                    self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    if x.MP >= x.MAX_MP*value:
                        self.actions.append([x,action,name,distance,type,effect,sound])

        if sort_by == "by_STR":
            if type == "on_self":
                self.actions.append([targets,action,name,distance,type,effect,sound])
            else: 
                max = 0
                final_target = targets[0]
                for x in targets:
                    if x.STR >= max:
                        max = x.STR
                        final_target = x
                self.actions.append([final_target,action,name,distance,type,effect,sound])
        
        if sort_by == "by_DEX":
            if type == "on_self":
                self.actions.append([targets,action,name,distance,type,effect,sound])
            else: 
                max = 0
                final_target = targets[0]
                for x in targets:
                    if x.DEX >= max:
                        max = x.DEX
                        final_target = x
                self.actions.append([final_target,action,name,distance,type,effect,sound])

        if sort_by == "by_INT":
            if type == "on_self":
                self.actions.append([targets,action,name,distance,type,effect,sound])
            else: 
                max = 0
                final_target = targets[0]
                for x in targets:
                    if x.INT >= max:
                        max = x.INT
                        final_target = x
                self.actions.append([final_target,action,name,distance,type,effect,sound])

        if sort_by == "by_defence":
            if type == "on_self":
                self.actions.append([targets,action,name,distance,type,effect,sound])
            else: 
                max = 0
                final_target = targets[0]
                for x in targets:
                    if x.defence >= max:
                        max = x.defence
                        final_target = x
                self.actions.append([final_target,action,name,distance,type,effect,sound])

        if sort_by == "by_status":
            if type == "on_self":
                    for x in targets.status:
                        if se.status_effect.status_list[value][0] == x[0][0]:
                            ok = True
                    if ok == False:
                        self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    ok = False
                    for y in x.status:
                        if se.status_effect.status_list[value][0] == y[0][0]:
                            ok = True
                    if ok == False:
                        self.actions.append([x,action,name,distance,type,effect,sound])

        if sort_by == "by_status_on":
            if type == "on_self":
                for x in targets.status:
                    if se.status_effect.status_list[value][0] == x[0][0]:
                        self.actions.clear()
                        self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    for y in x.status:
                        if se.status_effect.status_list[value][0] == y[0][0]:
                            self.actions.clear()
                            self.actions.append([x,action,name,distance,type,effect,sound])

        if sort_by == "by_stauts_and_HP":
            if type == "on_self":
                    for x in targets.status:
                        if se.status_effect.status_list[status][0] == x[0][0]:
                            ok = True
                    if ok == False:
                        if targets.HP <= targets.MAX_HP*value:
                            self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    ok = False
                    for y in x.status:
                        if se.status_effect.status_list[status][0] == y[0][0]:
                            ok = True
                    if ok == False:
                        if x.HP <= x.MAX_HP*value:
                            self.actions.append([x,action,name,distance,type,effect,sound])

        if sort_by == "by_stauts_and_HP_alter":
            if type == "on_self":
                    for x in targets.status:
                        if se.status_effect.status_list[status][0] == x[0][0]:
                            ok = True
                    if ok == False:
                        if targets.HP >= targets.MAX_HP*value:
                            self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    ok = False
                    for y in x.status:
                        if se.status_effect.status_list[status][0] == y[0][0]:
                            ok = True
                    if ok == False:
                        if x.HP >= x.MAX_HP*value:
                            self.actions.append([x,action,name,distance,type,effect,sound])

        if sort_by == "by_team_must_have": #use this ability 100% when alone
            if type == "on_self":
                    for x in targets.status:
                        if se.status_effect.status_list[value][0] == x[0][0]:
                            ok = True
                    if ok == False:
                        if len(enemy_team_alive)==1:
                            self.actions.clear()
                            self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    ok = False
                    for y in x.status:
                        if se.status_effect.status_list[value][0] == y[0][0]:
                            ok = True
                    if ok == False:
                        if len(enemy_team_alive)==1:
                            self.actions.clear()
                            self.actions.append([targets,action,name,distance,type,effect,sound])

        if sort_by == "must_have":
            if type == "on_self":
                    for x in targets.status:
                        if se.status_effect.status_list[value][0] == x[0][0]:
                            ok = True
                    if ok == False:
                        self.actions.clear()
                        self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    ok = False
                    for y in x.status:
                        if se.status_effect.status_list[value][0] == y[0][0]:
                            ok = True
                    if ok == False:
                        self.actions.clear()
                        self.actions.append([x,action,name,distance,type,effect,sound])

        if sort_by == "by_HP_must_have":
            if type == "on_self":
                    for x in targets.status:
                        if se.status_effect.status_list[status][0] == x[0][0]:
                            ok = True
                    if ok == False:
                        if targets.HP <= targets.MAX_HP*value:
                            self.actions.clear()
                            self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    ok = False
                    for y in x.status:
                        if se.status_effect.status_list[status][0] == y[0][0]:
                            ok = True
                    if ok == False:
                        if targets.HP <= targets.MAX_HP*value:
                            self.actions.clear()
                            self.actions.append([targets,action,name,distance,type,effect,sound])
 


        ###################################################################
        if type in ["attack"]:
            chanse = random.randint(0,100)
            if len(targets) == 1:
                self.actions.append([player_team_alive[0],action,name,distance,type,effect,sound])
            if len(targets) == 2:
                if chanse >=0 and chanse <= 40:
                    self.actions.append([player_team_alive[0],action,name,distance,type,effect,sound])
                elif chanse > 40 and chanse <= 100:
                    self.actions.append([player_team_alive[1],action,name,distance,type,effect,sound])
            if len(targets) == 3:
                if chanse >= 0 and chanse <= 20:
                    self.actions.append([player_team_alive[0],action,name,distance,type,effect,sound])
                elif chanse > 20 and chanse <= 70:
                    self.actions.append([player_team_alive[1],action,name,distance,type,effect,sound])
                elif chanse > 70 and chanse <= 100:
                    self.actions.append([player_team_alive[2],action,name,distance,type,effect,sound])
        elif type == "on_all_enemy":
            chanse = random.randint(0,100)
            if len(targets) == 1:
                self.actions.append([enemy_team_alive[0],action,"",distance,type,effect,sound])
            if len(targets) == 2:
                if chanse >=0 and chanse <= 40:
                    self.actions.append([enemy_team_alive[0],action,"",distance,type,effect,sound])
                elif chanse > 40 and chanse <= 100:
                    self.actions.append([enemy_team_alive[1],action,"",distance,type,effect,sound])
            if len(targets) == 3:
                if chanse >=0 and chanse <= 20:
                    self.actions.append([enemy_team_alive[0],action,"",distance,type,effect,sound])
                elif chanse > 20 and chanse <= 70:
                    self.actions.append([enemy_team_alive[1],action,"",distance,type,effect,sound])
                elif chanse > 70 and chanse <= 100:
                    self.actions.append([enemy_team_alive[2],action,"",distance,type,effect,sound])
                    
        
    def set_actions(self):
        self.actions.clear()
        for x in self.AI:
            self.action(enemy_skills[x][1],enemy_skills[x][2],enemy_skills[x][3],enemy_skills[x][4],enemy_skills[x][0],enemy_skills[x][5],enemy_skills[x][6],enemy_skills[x][7],enemy_skills[x][8])
        chose = random.randint(0,len(self.actions)-1)
        return self.actions[chose]

    def drop_mashine(self):
        drop_roll = random.randint(0,100)
        items_droped = list()
        count = 0
        for x in self.enemy_drop.keys():
            if drop_roll <= self.enemy_drop[x]:
                items_droped.append(x)
                drop_roll = random.randint(0,100)
        for x in range(48,48+len(items_droped)):
            from player import current_player
            current_player.inventory[x][2] = items_droped[count]
            count += 1

enemy_skills ={}

def load_enemy_skill():
    file_path = get_resource_path('enemy_skill_list.txt')
    data =["","","","","","","","","",""]
    count = 0
    with codecs.open(file_path,'r','utf-8') as f:
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
                if count == 10: # <--- amout of separated data for one item/skill/status, change appropriately
                    enemy_skills[data[0]] = [data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]]
                    count=0
    f.close()

load_enemy_skill()

                #nazwa #lv #MAX_HP #STR #DEX #INT #Obrażenia #Pancerz #EXP #Złoto #AI #drop #sprite
first_enemy = Enemy("Szkielet",1,70,5,1,1,8,1,100,100,{"atak":enemy_skills["atak"],"atak":enemy_skills["atak"],"szarża":enemy_skills["szarża"],"blok":enemy_skills["blok"]},{"graphics/items/mała_mikstura_zdrowia.png":100},"graphics/sprites/szkielet_sprite.png","szkielet")

skeleton1 = Enemy("Szkielet",2,70,5,1,5,13,1,40,10,{"atak":enemy_skills["atak"],"atak":enemy_skills["atak"],"szarża":enemy_skills["szarża"],"blok":enemy_skills["blok"]},{"graphics/items/miedziany_sztylet.png":70,"graphics/items/pika.png":70,"graphics/items/miecz_z_brazu.png":70,"graphics/items/stalowy_miecz.png":60,"graphics/items/srebrny_pierscien.png":50},"graphics/sprites/szkielet_sprite.png","szkielet")
skeleton2 = Enemy("Szkielet",2,70,5,1,5,13,1,40,10,{"atak":enemy_skills["atak"],"atak":enemy_skills["atak"],"szarża":enemy_skills["szarża"],"blok":enemy_skills["blok"]},{"graphics/items/miedziany_sztylet.png":70,"graphics/items/pika.png":70,"graphics/items/miecz_z_brazu.png":70,"graphics/items/stalowy_miecz.png":60,"graphics/items/srebrny_pierscien.png":50},"graphics/sprites/szkielet_sprite.png","szkielet")
skeleton3 = Enemy("Szkielet",2,70,5,1,5,13,1,40,10,{"atak":enemy_skills["atak"],"atak":enemy_skills["atak"],"szarża":enemy_skills["szarża"],"blok":enemy_skills["blok"]},{"graphics/items/miedziany_sztylet.png":70,"graphics/items/pika.png":70,"graphics/items/miecz_z_brazu.png":70,"graphics/items/stalowy_miecz.png":60,"graphics/items/srebrny_pierscien.png":50},"graphics/sprites/szkielet_sprite.png","szkielet")

skeleton_priest = Enemy("Upadły kapłan",3,70,10,20,13,16,0,80,20,{
                                                            "atak":enemy_skills["atak"],
                                                            "leczenie":enemy_skills["leczenie"],
                                                            "leczenie":enemy_skills["leczenie"],
                                                            "klatwa":enemy_skills["klatwa"],
                                                            "klatwa":enemy_skills["klatwa"],
                                                            "klatwa":enemy_skills["klatwa"],
                                                            "klatwa":enemy_skills["klatwa"]},
                                                            {"graphics/items/grzech_kaplana.png":25,"graphics/items/srebrny_pierscien.png":80},
                                                            "graphics/sprites/upadly_kaplan_sprite.png","upadly_kaplan")

skeleton_priest2 = Enemy("Upadły kapłan",3,70,10,20,15,15,0,80,20,{
                                                            "atak":enemy_skills["atak"],
                                                            "leczenie":enemy_skills["leczenie"],
                                                            "leczenie":enemy_skills["leczenie"],
                                                            "klatwa":enemy_skills["klatwa"],
                                                            "klatwa":enemy_skills["klatwa"],
                                                            "klatwa":enemy_skills["klatwa"],
                                                            "klatwa":enemy_skills["klatwa"]},
                                                            {"graphics/items/grzech_kaplana.png":25,"graphics/items/srebrny_pierscien.png":80,"graphics/items/magicza_ksiega.png":15},
                                                            "graphics/sprites/upadly_kaplan_sprite.png","upadly_kaplan")
                                        
lost_soul = Enemy("Zagubiona Dusza",4,150,17,17,17,21,5,0,0,{
                                                            "atak":enemy_skills["atak"]
                                                            ,"atak":enemy_skills["atak"]
                                                            ,"eteryczny":enemy_skills["eteryczny"]
                                                            ,"zimny jak lód":enemy_skills["zimny jak lód"]
                                                            ,"zimny jak lód":enemy_skills["zimny jak lód"]
                                                            ,"zimny jak lód":enemy_skills["zimny jak lód"]
                                                            ,"bisekcja":enemy_skills["bisekcja"]
                                                            ,"bisekcja":enemy_skills["bisekcja"]},
                                                            {},
                                                            "graphics/sprites/zagubiona_dusza_sprite.png","zagubiona_dusza")

zjawa = Enemy("Zjawa",4,140,10,30,25,22,0,50,30,{"atak":enemy_skills["atak"],
                                                "eteryczny":enemy_skills["eteryczny"],
                                                "magiczna włócznia":enemy_skills["magiczna włócznia"],
                                                "magiczna włócznia":enemy_skills["magiczna włócznia"],
                                                "magiczna włócznia":enemy_skills["magiczna włócznia"],
                                                "skowyt banshee":enemy_skills["skowyt banshee"],
                                                "skowyt banshee":enemy_skills["skowyt banshee"],},
                                                {"graphics/items/amulet_precyzji.png":40,"graphics/items/wlocznia_straznicza.png":20,"graphics/items/srebrny_pierscien.png":60,"graphics/items/mała_mikstura_zdrowia.png":40},
                                                "graphics/sprites/zjawa_sprite.png","zjawa")

skeleton_warrior = Enemy("Szkielet Wojownik",4,170,23,5,1,24,5,50,35,{
                                                                    "atak":enemy_skills["atak"],
                                                                    "szał wojownika":enemy_skills["szał wojownika"],
                                                                    "niezłomny":enemy_skills["niezłomny"]},
                                                                    {"graphics/items/topor_wojownika.png":30,"graphics/items/drewniana_tarcza.png":100,"graphics/items/mała_mikstura_zdrowia.png":20,"graphics/items/pierscien_zdrowia.png":15},
                                                                    "graphics/sprites/szkielet_wojownik_sprite.png","szkielet_wojownik")
skeleton_warrior2 = Enemy("Szkielet Wojownik",4,170,25,5,1,24,5,50,35,{
                                                                    "atak":enemy_skills["atak"],
                                                                    "szał wojownika":enemy_skills["szał wojownika"],
                                                                    "niezłomny":enemy_skills["niezłomny"]},
                                                                    {"graphics/items/topor_wojownika.png":30,"graphics/items/drewniana_tarcza.png":80,"graphics/items/mała_mikstura_zdrowia.png":20,"graphics/items/pierscien_zdrowia.png":15},
                                                                    "graphics/sprites/szkielet_wojownik_sprite.png","szkielet_wojownik")
skeleton_warrior3 = Enemy("Szkielet Wojownik",4,170,25,5,1,24,5,50,35,{
                                                                    "atak":enemy_skills["atak"],
                                                                    "szał wojownika":enemy_skills["szał wojownika"],
                                                                    "niezłomny":enemy_skills["niezłomny"]},
                                                                    {"graphics/items/topor_wojownika.png":30,"graphics/items/drewniana_tarcza.png":80,"graphics/items/mała_mikstura_zdrowia.png":20,"graphics/items/pierscien_zdrowia.png":15},
                                                                    "graphics/sprites/szkielet_wojownik_sprite.png","szkielet_wojownik")


rzeznik = Enemy("Rzeznik",5,185,30,20,10,30,120,200,100,{
                                                    "atak":enemy_skills["atak"],
                                                    "atak":enemy_skills["atak"],
                                                    "tortury":enemy_skills["tortury"],
                                                    "tortury":enemy_skills["tortury"],
                                                    "kat":enemy_skills["kat"],
                                                    "gdzie moi słudzy":enemy_skills["gdzie moi słudzy"],
                                                    "Jestem nie pokonany":enemy_skills["Jestem nie pokonany"]},
                                                    {"graphics/items/mała_mikstura_many.png":100,"graphics/items/dwureczny_topor_rzeznika.png":100,"graphics/items/pikowany_pancerz.png":100},
                                                    "graphics/sprites/rzeznik_sprite.png","rzeznik")

zombie = Enemy("Zombie",5,150,30,10,20,30,0,60,40,{
                                            "atak":enemy_skills["atak"],
                                            "grzmotnięcie":enemy_skills["grzmotnięcie"],
                                            "podcięcie":enemy_skills["podcięcie"],
                                            "walnięcie":enemy_skills["walnięcie"],
                                            "zarodniki":enemy_skills["zarodniki"],
                                            "trujące opary":enemy_skills["trujące opary"]},
                                            {"graphics/items/pikowany_pancerz.png":35,"graphics/items/maczuga_zolnierska.png":30,"graphics/items/amulet_precyzji.png":15},
                                            "graphics/sprites/zombie_sprite.png","zombie")
zombie2 = Enemy("Zombie",5,150,25,10,20,25,5,60,40,{
                                            "atak":enemy_skills["atak"],
                                            "grzmotnięcie":enemy_skills["grzmotnięcie"],
                                            "podcięcie":enemy_skills["podcięcie"],
                                            "walnięcie":enemy_skills["walnięcie"],
                                            "zarodniki":enemy_skills["zarodniki"],
                                            "trujące opary":enemy_skills["trujące opary"]},
                                            {"graphics/items/pikowany_pancerz.png":35,"graphics/items/maczuga_zolnierska.png":30,"graphics/items/amulet_precyzji.png":15},
                                            "graphics/sprites/zombie_sprite.png","zombie")

 
death_knight = Enemy("Rycerz Śmierci",6,600,30,25,20,15,13,100,200,{
                                                            "atak":enemy_skills["atak"],
                                                            "mroczne ugodzenie":enemy_skills["mroczne ugodzenie"],
                                                            "aura śmierci":enemy_skills["aura śmierci"],
                                                            "horror":enemy_skills["horror"],
                                                            "inkantacja":enemy_skills["inkantacja"],
                                                            "zagłada":enemy_skills["zagłada"],
                                                            "łaska chaosu":enemy_skills["łaska chaosu"]
                                                            },
                                                            {"graphics/items/siewca_smierci.png":100,"graphics/items/pierscien_mrocznych_mocy.png":100},
                                                            "graphics/sprites/rycerz_smierci_sprite.png","rycerz_smierci")

enemy_team = list()
enemy_team.append(skeleton1)
enemy_team.append(skeleton2)
enemy_team.append(skeleton3)
enemy_team_alive = list()

#character - after this fight you get new companion(max 2 at playthrough), one-time - this fight dont count to random fight, normal - well..it's normal XD
story_fight = {
    1:{
        1:[[first_enemy],"one-time"],
        2:[[skeleton1,skeleton2],"normal"],
        3:[[skeleton_priest,skeleton1],"normal"],
        4:[[lost_soul],"character"],
        5:[[zjawa,skeleton_warrior],"normal"],
        6:[[rzeznik,skeleton_priest,skeleton_priest2],"normal"],
        7:[[zombie,zombie2],"normal"],
        8:[[skeleton_warrior,skeleton_warrior2,skeleton_warrior3],"normal"],
        9:[[skeleton_warrior,zombie,skeleton_priest],"normal"],
        10:[[death_knight],"one_time"]
    }
}