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
    def __init__(self, name, lv, MAX_HP, STR, DEX, INT, damage, defence, exp_gain, gold_gain,AI, enemy_drop,enemy_sprite,source,on_death=False,on_death_status="none"):
        super().__init__()
        self.name = name
        self.lv = lv
        self.MAX_HP = MAX_HP
        self.HP = MAX_HP
        self.MP_regen_base = 0
        self.MP_regen_modifier = 0

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

        self.on_death = on_death
        self.on_death_status = on_death_status

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
        if type in ["on_enemy","on_all_enemy"]:
            targets = enemy_team_alive
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
                        if se.status_effects.status_list[value][0] == x[0][0]:
                            ok = True
                    if ok == False:
                        self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    ok = False
                    for y in x.status:
                        if se.status_effects.status_list[value][0] == y[0][0]:
                            ok = True
                    if ok == False:
                        self.actions.append([x,action,name,distance,type,effect,sound])

        if sort_by == "by_status_on":
            if type == "on_self":
                for x in targets.status:
                    if se.status_effects.status_list[value][0] == x[0][0]:
                        self.actions.clear()
                        self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    for y in x.status:
                        if se.status_effects.status_list[value][0] == y[0][0]:
                            self.actions.clear()
                            self.actions.append([x,action,name,distance,type,effect,sound])

        if sort_by == "by_status_and_HP":
            if type == "on_self":
                    for x in targets.status:
                        if se.status_effects.status_list[status][0] == x[0][0]:
                            ok = True
                    if ok == False:
                        if targets.HP <= targets.MAX_HP*value:
                            self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    ok = False
                    for y in x.status:
                        if se.status_effects.status_list[status][0] == y[0][0]:
                            ok = True
                    if ok == False:
                        if x.HP <= x.MAX_HP*value:
                            self.actions.append([x,action,name,distance,type,effect,sound])

        if sort_by == "by_status_and_HP_alter":
            if type == "on_self":
                    for x in targets.status:
                        if se.status_effects.status_list[status][0] == x[0][0]:
                            ok = True
                    if ok == False:
                        if targets.HP >= targets.MAX_HP*value:
                            self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    ok = False
                    for y in x.status:
                        if se.status_effects.status_list[status][0] == y[0][0]:
                            ok = True
                    if ok == False:
                        if x.HP >= x.MAX_HP*value:
                            self.actions.append([x,action,name,distance,type,effect,sound])

        if sort_by == "by_team_must_have": #use this ability 100% when alone
            if type == "on_self":
                    for x in targets.status:
                        if se.status_effects.status_list[value][0] == x[0][0]:
                            ok = True
                    if ok == False:
                        if len(enemy_team_alive)==1:
                            self.actions.clear()
                            self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    ok = False
                    for y in x.status:
                        if se.status_effects.status_list[value][0] == y[0][0]:
                            ok = True
                    if ok == False:
                        if len(enemy_team_alive)==1:
                            self.actions.clear()
                            self.actions.append([targets,action,name,distance,type,effect,sound])

        if sort_by == "must_have":
            if type == "on_self":
                    for x in targets.status:
                        if se.status_effects.status_list[value][0] == x[0][0]:
                            ok = True
                    if ok == False:
                        self.actions.clear()
                        self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    ok = False
                    for y in x.status:
                        if se.status_effects.status_list[value][0] == y[0][0]:
                            ok = True
                    if ok == False:
                        self.actions.clear()
                        self.actions.append([x,action,name,distance,type,effect,sound])

        if sort_by == "by_HP_must_have":
            if type == "on_self":
                    for x in targets.status:
                        if se.status_effects.status_list[status][0] == x[0][0]:
                            ok = True
                    if ok == False:
                        if targets.HP <= targets.MAX_HP*value:
                            self.actions.clear()
                            self.actions.append([targets,action,name,distance,type,effect,sound])
            else:
                for x in targets:
                    ok = False
                    for y in x.status:
                        if se.status_effects.status_list[status][0] == y[0][0]:
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
                if count == 10: # <--- ilosc kategori nadanej dla jednego przedmiotu/umiejetnosci/statusu, zmienic odpowiednio
                    enemy_skills[data[0]] = [data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]]
                    count=0
    f.close()

load_enemy_skill()
######################### 1 OBSZAR PRZECIWNICY ################################
                #nazwa #lv #MAX_HP #STR #DEX #INT #Obrażenia #Pancerz #EXP #Złoto #AI #drop #sprite #czy daje status po smierci #jesli tak to jaki (nazwa)
first_enemy = Enemy("Szkielet",1,65,5,1,1,8,1,100,200,{
                                                    "atak":enemy_skills["atak"],
                                                    "atak":enemy_skills["atak"],
                                                    "szarża":enemy_skills["szarża"],
                                                    "blok":enemy_skills["blok"]},
                                                    {"graphics/items/mała_mikstura_zdrowia.png":101},
                                                    "graphics/sprites/szkielet_sprite.png","szkielet",False)

skeleton1 = Enemy("Szkielet",2,65,5,1,5,13,1,40,15,{
                                                    "atak":enemy_skills["atak"],
                                                    "atak":enemy_skills["atak"],
                                                    "szarża":enemy_skills["szarża"],
                                                    "blok":enemy_skills["blok"]},
                                                    {"graphics/items/miedziany_sztylet.png":70,"graphics/items/pika.png":70,"graphics/items/miecz_z_brazu.png":70,"graphics/items/stalowy_miecz.png":65,"graphics/items/srebrny_pierscien.png":55},
                                                    "graphics/sprites/szkielet_sprite.png","szkielet",False)
skeleton2 = Enemy("Szkielet",2,70,5,1,5,13,1,40,15,{
                                                    "atak":enemy_skills["atak"],
                                                    "atak":enemy_skills["atak"],
                                                    "szarża":enemy_skills["szarża"],
                                                    "blok":enemy_skills["blok"]},
                                                    {"graphics/items/miedziany_sztylet.png":70,"graphics/items/pika.png":70,"graphics/items/miecz_z_brazu.png":70,"graphics/items/stalowy_miecz.png":65,"graphics/items/srebrny_pierscien.png":55},
                                                    "graphics/sprites/szkielet_sprite.png","szkielet",False)
skeleton3 = Enemy("Szkielet",2,70,5,1,5,13,1,40,15,{
                                                    "atak":enemy_skills["atak"],
                                                    "atak":enemy_skills["atak"],
                                                    "szarża":enemy_skills["szarża"],
                                                    "blok":enemy_skills["blok"]},
                                                    {"graphics/items/miedziany_sztylet.png":70,"graphics/items/pika.png":70,"graphics/items/miecz_z_brazu.png":70,"graphics/items/stalowy_miecz.png":65,"graphics/items/srebrny_pierscien.png":55},
                                                    "graphics/sprites/szkielet_sprite.png","szkielet",False)

skeleton_priest = Enemy("Upadły kapłan",3,75,10,20,13,16,0,80,25,{
                                                            "atak":enemy_skills["atak"],
                                                            "leczenie":enemy_skills["leczenie"],
                                                            "leczenie":enemy_skills["leczenie"],
                                                            "klatwa":enemy_skills["klatwa"],
                                                            "klatwa":enemy_skills["klatwa"],
                                                            "klatwa":enemy_skills["klatwa"],
                                                            "klatwa":enemy_skills["klatwa"]},
                                                            {"graphics/items/grzech_kaplana.png":25,"graphics/items/srebrny_pierscien.png":80,"graphics/items/magicza_ksiega.png":15},
                                                            "graphics/sprites/upadly_kaplan_sprite.png","upadly_kaplan",False)

skeleton_priest2 = Enemy("Upadły kapłan",3,75,10,20,15,15,0,80,25,{
                                                            "atak":enemy_skills["atak"],
                                                            "leczenie":enemy_skills["leczenie"],
                                                            "leczenie":enemy_skills["leczenie"],
                                                            "klatwa":enemy_skills["klatwa"],
                                                            "klatwa":enemy_skills["klatwa"],
                                                            "klatwa":enemy_skills["klatwa"],
                                                            "klatwa":enemy_skills["klatwa"]},
                                                            {"graphics/items/grzech_kaplana.png":25,"graphics/items/srebrny_pierscien.png":80,"graphics/items/magicza_ksiega.png":10},
                                                            "graphics/sprites/upadly_kaplan_sprite.png","upadly_kaplan",False)
skeleton_priest3 = Enemy("Upadły kapłan",3,125,10,20,15,15,0,100,25,{
                                                            "atak":enemy_skills["atak"],
                                                            "leczenie":enemy_skills["leczenie"],
                                                            "leczenie":enemy_skills["leczenie"],
                                                            "leczenie":enemy_skills["leczenie"],
                                                            "klatwa":enemy_skills["klatwa"],
                                                            "klatwa":enemy_skills["klatwa"]},
                                                            {"graphics/items/grzech_kaplana.png":25,"graphics/items/srebrny_pierscien.png":80,"graphics/items/magicza_ksiega.png":10},
                                                            "graphics/sprites/upadly_kaplan_sprite.png","upadly_kaplan",False)
                                        
lost_soul = Enemy("Zagubiona Dusza",4,140,17,17,17,21,5,0,0,{
                                                            "atak":enemy_skills["atak"],
                                                            "atak":enemy_skills["atak"],
                                                            "eteryczny":enemy_skills["eteryczny"],
                                                            "zimny jak lód":enemy_skills["zimny jak lód"],
                                                            "zimny jak lód":enemy_skills["zimny jak lód"],
                                                            "zimny jak lód":enemy_skills["zimny jak lód"],
                                                            "bisekcja":enemy_skills["bisekcja"],
                                                            "bisekcja":enemy_skills["bisekcja"]},
                                                            {},
                                                            "graphics/sprites/zagubiona_dusza_sprite.png","zagubiona_dusza",False)

zjawa = Enemy("Zjawa",4,140,10,30,25,24,0,70,35,{"atak":enemy_skills["atak"],
                                                "eteryczny":enemy_skills["eteryczny"],
                                                "magiczna włócznia":enemy_skills["magiczna włócznia"],
                                                "magiczna włócznia":enemy_skills["magiczna włócznia"],
                                                "magiczna włócznia":enemy_skills["magiczna włócznia"],
                                                "skowyt banshee":enemy_skills["skowyt banshee"],
                                                "skowyt banshee":enemy_skills["skowyt banshee"],},
                                                {"graphics/items/amulet_precyzji.png":40,"graphics/items/wlocznia_straznicza.png":25,"graphics/items/srebrny_pierscien.png":70,"graphics/items/mała_mikstura_zdrowia.png":45},
                                                "graphics/sprites/zjawa_sprite.png","zjawa",False)

skeleton_warrior = Enemy("Szkielet Wojownik",4,160,23,5,1,22,5,70,35,{
                                                                    "atak":enemy_skills["atak"],
                                                                    "szał wojownika":enemy_skills["szał wojownika"],
                                                                    "niezłomny":enemy_skills["niezłomny"]},
                                                                    {"graphics/items/topor_wojownika.png":30,"graphics/items/drewniana_tarcza.png":101,"graphics/items/mała_mikstura_zdrowia.png":20,"graphics/items/pierscien_zdrowia.png":15},
                                                                    "graphics/sprites/szkielet_wojownik_sprite.png","szkielet_wojownik",False)
skeleton_warrior2 = Enemy("Szkielet Wojownik",4,160,25,5,1,22,5,70,35,{
                                                                    "atak":enemy_skills["atak"],
                                                                    "szał wojownika":enemy_skills["szał wojownika"],
                                                                    "niezłomny":enemy_skills["niezłomny"]},
                                                                    {"graphics/items/topor_wojownika.png":30,"graphics/items/drewniana_tarcza.png":80,"graphics/items/mała_mikstura_zdrowia.png":20,"graphics/items/pierscien_zdrowia.png":15},
                                                                    "graphics/sprites/szkielet_wojownik_sprite.png","szkielet_wojownik",False)
skeleton_warrior3 = Enemy("Szkielet Wojownik",4,160,25,5,1,22,5,70,35,{
                                                                    "atak":enemy_skills["atak"],
                                                                    "szał wojownika":enemy_skills["szał wojownika"],
                                                                    "niezłomny":enemy_skills["niezłomny"]},
                                                                    {"graphics/items/topor_wojownika.png":30,"graphics/items/drewniana_tarcza.png":80,"graphics/items/mała_mikstura_zdrowia.png":20,"graphics/items/pierscien_zdrowia.png":15},
                                                                    "graphics/sprites/szkielet_wojownik_sprite.png","szkielet_wojownik",False)


rzeznik = Enemy("Rzeznik",5,215,30,20,10,26,120,200,200,{
                                                    "atak":enemy_skills["atak"],
                                                    "atak":enemy_skills["atak"],
                                                    "tortury":enemy_skills["tortury"],
                                                    "tortury":enemy_skills["tortury"],
                                                    "kat":enemy_skills["kat"],
                                                    "gdzie moi słudzy":enemy_skills["gdzie moi słudzy"],
                                                    "Jestem nie pokonany":enemy_skills["Jestem nie pokonany"]},
                                                    {"graphics/items/mała_mikstura_many.png":101,"graphics/items/dwureczny_topor_rzeznika.png":101,"graphics/items/pikowany_pancerz.png":101},
                                                    "graphics/sprites/rzeznik_sprite.png","rzeznik",False)

zombie = Enemy("Zombie",5,150,30,10,20,18,0,90,45,{
                                            "atak":enemy_skills["atak"],
                                            "grzmotnięcie":enemy_skills["grzmotnięcie"],
                                            "podcięcie":enemy_skills["podcięcie"],
                                            "walnięcie":enemy_skills["walnięcie"],
                                            "trujące opary":enemy_skills["trujące opary"],
                                            "regeneracja":enemy_skills["regeneracja"]},
                                            {"graphics/items/pikowany_pancerz.png":35,"graphics/items/maczuga_zolnierska.png":30,"graphics/items/amulet_precyzji.png":15},
                                            "graphics/sprites/zombie_sprite.png","zombie",False)
zombie2 = Enemy("Zombie",5,150,25,10,20,25,5,90,45,{
                                            "atak":enemy_skills["atak"],
                                            "grzmotnięcie":enemy_skills["grzmotnięcie"],
                                            "podcięcie":enemy_skills["podcięcie"],
                                            "walnięcie":enemy_skills["walnięcie"],
                                            "trujące opary":enemy_skills["trujące opary"],
                                            "regeneracja":enemy_skills["regeneracja"]},
                                            {"graphics/items/pikowany_pancerz.png":35,"graphics/items/maczuga_zolnierska.png":30,"graphics/items/amulet_precyzji.png":15},
                                            "graphics/sprites/zombie_sprite.png","zombie",False)

 
death_knight = Enemy("Rycerz Śmierci",6,550,30,25,20,15,13,300,150,{
                                                            "atak":enemy_skills["atak"],
                                                            "mroczne ugodzenie":enemy_skills["mroczne ugodzenie"],
                                                            "aura śmierci":enemy_skills["aura śmierci"],
                                                            "horror":enemy_skills["horror"],
                                                            "inkantacja":enemy_skills["inkantacja"],
                                                            "zagłada":enemy_skills["zagłada"],
                                                            "łaska chaosu":enemy_skills["łaska chaosu"]
                                                            },
                                                            {"graphics/items/siewca_smierci.png":101,"graphics/items/pierscien_mrocznych_mocy.png":101},
                                                            "graphics/sprites/rycerz_smierci_sprite.png","rycerz_smierci",False)


######################### 2 OBSZAR PRZECIWNICY ################################
rozdarta_dusza = Enemy("Rozdarta Dusza",6,350,30,30,29,37,15,0,0,{
                                                            "atak":enemy_skills["atak"],
                                                            "eteryczny":enemy_skills["eteryczny"],
                                                            "bisekcja":enemy_skills["bisekcja"],
                                                            "bisekcja":enemy_skills["bisekcja"],
                                                            "tchnienie śmierci":enemy_skills["tchnienie śmierci"],
                                                            "astralna wiedza":enemy_skills["astralna wiedza"],
                                                            },
                                                            {},
                                                            "graphics/sprites/rozdarta_dusza_sprite.png","rozdarta_dusza",False)

wojownik_qin = Enemy("Wojownik Qin",6,180,28,24,20,17,12,170,135,{
                                                            "atak":enemy_skills["atak"],
                                                            "wu_jian":enemy_skills["wu_jian"],
                                                            "wu_jian":enemy_skills["wu_jian"],
                                                            "manewr_kowadla":enemy_skills["manewr_kowadla"],
                                                            "manewr_mlota":enemy_skills["manewr_mlota"],
                                                            "skupienie":enemy_skills["skupienie"],
                                                            "grzmotnięcie":enemy_skills["grzmotnięcie"],                                                 
                                                            },
                                                            {"graphics/items/wiekszy_pierscien_sily.png":10,"graphics/items/zloty_pierscien.png":45,"graphics/items/pikowany_pancerz.png":25},
                                                            "graphics/sprites/wojownik_qin_sprite.png","wojownik_qin",False)
wojownik_qin2 = Enemy("Wojownik Qin",6,205,28,25,23,18,13,170,135,{
                                                            "atak":enemy_skills["atak"],
                                                            "wu_jian":enemy_skills["wu_jian"],
                                                            "wu_jian":enemy_skills["wu_jian"],
                                                            "manewr_kowadla":enemy_skills["manewr_kowadla"],
                                                            "manewr_mlota":enemy_skills["manewr_mlota"],
                                                            "skupienie":enemy_skills["skupienie"],
                                                            "grzmotnięcie":enemy_skills["grzmotnięcie"], 
                                                            },
                                                            {"graphics/items/wiekszy_pierscien_sily.png":10,"graphics/items/zloty_pierscien.png":45,"graphics/items/pikowany_pancerz.png":25},
                                                            "graphics/sprites/wojownik_qin_sprite.png","wojownik_qin",False)

wlocznik_qin = Enemy("Włócznik Qin",6,230,20,20,35,14,7,170,145,{
                                                            "atak":enemy_skills["atak"],
                                                            "remedium":enemy_skills["remedium"],
                                                            "remedium":enemy_skills["remedium"],
                                                            "cios_rewersem":enemy_skills["cios_rewersem"],
                                                            "shi_mao":enemy_skills["shi_mao"],
                                                            "walnięcie":enemy_skills["walnięcie"],                                                         
                                                            },
                                                            {"graphics/items/pierscien_zrecznosci.png":40,"graphics/items/wiekszy_pierscien_zrecznosci.png":15,"graphics/items/pikowany_pancerz.png":20},
                                                            "graphics/sprites/wlocznik_qin_sprite.png","wlocznik_qin",False)

halabardnik_qin = Enemy("Halabardnik Qin",6,185,30,20,10,19,10,170,175,{
                                                            "atak":enemy_skills["atak"],
                                                            "tun_ji":enemy_skills["tun_ji"],
                                                            "wojenny_gong_gu":enemy_skills["wojenny_gong_gu"],
                                                            "wojenny_gong_gu":enemy_skills["wojenny_gong_gu"],
                                                            "wojenny_gong_gu":enemy_skills["wojenny_gong_gu"],
                                                            "manewr_kowadla":enemy_skills["manewr_kowadla"],
                                                            "manewr_mlota":enemy_skills["manewr_mlota"],
                                                            "podcięcie":enemy_skills["podcięcie"],
                                                            },
                                                            {"graphics/items/halbarda_ji.png":101,"graphics/items/amulet_predkosci.png":35,"graphics/items/pierscien_inteligencji.png":25,"graphics/items/pikowany_pancerz.png":13},
                                                            "graphics/sprites/halabardnik_qin_sprite.png","halabardnik_qin",False)

zhihui_guan = Enemy("Zhihui Guan",6,600,30,25,20,15,13,100,200,{
                                                            "atak":enemy_skills["atak"],
                                                            "sepuku":enemy_skills["sepuku"],
                                                            "polksiezyc":enemy_skills["polksiezyc"],
                                                            "polksiezyc":enemy_skills["polksiezyc"],
                                                            "pelnia":enemy_skills["pelnia"],
                                                            "taktyka_oskrzydlajaca":enemy_skills["taktyka_oskrzydlajaca"],
                                                            "taktyka_oskrzydlajaca":enemy_skills["taktyka_oskrzydlajaca"],
                                                            "taktyka_frontalna":enemy_skills["taktyka_frontalna"],
                                                            "taktyka_frontalna":enemy_skills["taktyka_frontalna"],
                                                            "taktyka_frontalna":enemy_skills["taktyka_frontalna"],
                                                            },
                                                            {"graphics/items/berdysz_mao.png":101,"graphics/items/srednia_mikstura_zdrowia.png":50,"graphics/items/srednia_mikstura_many.png":50},
                                                            "graphics/sprites/zhihui_guan_sprite.png","zhihui_guan",False)

jaszczurzy_wojownik = Enemy("Jaszczurzy Wojownik",6,300,30,30,18,24,11,190,185,{
                                                            "atak":enemy_skills["atak"],
                                                            "ognisty_oddech":enemy_skills["ognisty_oddech"],
                                                            "zemsta":enemy_skills["zemsta"],
                                                            "zemsta":enemy_skills["zemsta"],
                                                            "mocny_cios":enemy_skills["mocny_cios"],
                                                            "instynkt_przetrwania":enemy_skills["instynkt_przetrwania"],
                                                            },
                                                            {"graphics/items/jaszczurzy_kord.png":35,"graphics/items/wiekszy_pierscien_sily.png":10,"graphics/items/zelazna_rekawica.png":15},
                                                            "graphics/sprites/jaszczurzy_wojownik_sprite.png","jaszczurzy_wojownik",True,"zwiększone obrażenia")

jaszczurzy_wojownik2 = Enemy("Jaszczurzy Wojownik",6,300,30,30,18,24,11,190,185,{
                                                            "atak":enemy_skills["atak"],
                                                            "ognisty_oddech":enemy_skills["ognisty_oddech"],
                                                            "zemsta":enemy_skills["zemsta"],
                                                            "zemsta":enemy_skills["zemsta"],
                                                            "mocny_cios":enemy_skills["mocny_cios"],
                                                            "instynkt_przetrwania":enemy_skills["instynkt_przetrwania"],
                                                            },
                                                            {"graphics/items/jaszczurzy_kord.png":35,"graphics/items/wiekszy_pierscien_sily.png":10,"graphics/items/zelazna_rekawica.png":15},
                                                            "graphics/sprites/jaszczurzy_wojownik_sprite.png","jaszczurzy_wojownik",True,"zwiększone obrażenia")


jaszczurzy_zabojca = Enemy("Jaszczurzy Zabójca",6,270,20,50,23,34,6,210,185,{
                                                            "atak":enemy_skills["atak"],
                                                            "jadowity_oddech":enemy_skills["jadowity_oddech"],
                                                            "jadowity_oddech":enemy_skills["jadowity_oddech"],
                                                            "bomba_dymna":enemy_skills["bomba_dymna"],
                                                            "ofiara":enemy_skills["ofiara"],
                                                            "ofiara":enemy_skills["ofiara"],
                                                            "cios_z_ukrycia":enemy_skills["cios_z_ukrycia"],
                                                            "instynkt_przetrwania":enemy_skills["instynkt_przetrwania"],
                                                            },
                                                            {"graphics/items/kiel_weza.png":30,"graphics/items/pierscien_many.png":20,"graphics/items/amulet_precyzji.png":15,"graphics/items/podstepny_majcher.png":50},
                                                            "graphics/sprites/jaszczurzy_zabojca_sprite.png","jaszczurzy_zabojca",True,"zwiększona szansa na unik")


jaszczurzy_czempion = Enemy("Jaszczurzy Czempion",6,380,40,30,27,43,15,260,220,{
                                                            "atak":enemy_skills["atak"],
                                                            "smoczy_oddech":enemy_skills["smoczy_oddech"],
                                                            "bebny_strachu":enemy_skills["bebny_strachu"],
                                                            "mocny_cios":enemy_skills["mocny_cios"],
                                                            "czempion":enemy_skills["czempion"],
                                                            },
                                                            {"graphics/items/sejmitar.png":25,"graphics/items/srednia_mikstura_zdrowia.png":30,"graphics/items/zloty_pierscien.png":80,"graphics/items/wiekszy_pierscien_zdrowia.png":5},
                                                            "graphics/sprites/jaszczurzy_czempion_sprite.png","jaszczurzy_czempion",True,"zwiększony pancerz")

nosiciel_swiatla = Enemy("Nosiciel Światła",6,600,35,30,50,50,0,600,300,{
                                                            "atak":enemy_skills["atak"],
                                                            "oslepienie":enemy_skills["oslepienie"],
                                                            "oslepienie":enemy_skills["oslepienie"],
                                                            "korozja":enemy_skills["korozja"],
                                                            "kuracja":enemy_skills["kuracja"],
                                                            "kuracja":enemy_skills["kuracja"],
                                                            "kuracja":enemy_skills["kuracja"],
                                                            "natchnienie":enemy_skills["natchnienie"],
                                                            "natchnienie":enemy_skills["natchnienie"],
                                                            "uzdrowienie":enemy_skills["uzdrowienie"],
                                                            "uzdrowienie":enemy_skills["uzdrowienie"],
                                                            "grupowe uzdrowienie":enemy_skills["grupowe uzdrowienie"],
                                                            "blysk":enemy_skills["blysk"],
                                                            "blask":enemy_skills["blask"],
                                                            "ostatni bastion":enemy_skills["ostatni bastion"],
                                                            },
                                                            {"graphics/items/ostatni_bastion.png":101,"graphics/items/magicza_ksiega.png":101},
                                                            "graphics/sprites/nosiciel_swiatla_sprite.png","nosiciel_swiatla",False)

chory_jaszczur = Enemy("Chory Jaszczur",6,380,40,25,30,60,0,280,200,{
                                                            "atak":enemy_skills["atak"],
                                                            "tchnienie śmierci":enemy_skills["tchnienie śmierci"],
                                                            "zemsta":enemy_skills["zemsta"],
                                                            "mocny_cios":enemy_skills["mocny_cios"],
                                                            "mocny_cios":enemy_skills["mocny_cios"],
                                                            "trujące opary":enemy_skills["trujące opary"],
                                                            },
                                                            {"graphics/items/pierscien_zdrowia.png":75,"graphics/items/pierscien_many.png":60},
                                                            "graphics/sprites/chory_jaszczur_sprite.png","chory_jaszczur",False)
chory_jaszczur2 = Enemy("Chory Jaszczur",6,380,40,25,30,60,0,280,200,{
                                                            "atak":enemy_skills["atak"],
                                                            "tchnienie śmierci":enemy_skills["tchnienie śmierci"],
                                                            "zemsta":enemy_skills["zemsta"],
                                                            "mocny_cios":enemy_skills["mocny_cios"],
                                                            "mocny_cios":enemy_skills["mocny_cios"],
                                                            "trujące opary":enemy_skills["trujące opary"],
                                                            },
                                                            {"graphics/items/pierscien_zdrowia.png":101,"graphics/items/pierscien_many.png":60},
                                                            "graphics/sprites/chory_jaszczur_sprite.png","chory_jaszczur",False)
chory_jaszczur3 = Enemy("Chory Jaszczur",6,380,40,25,30,60,0,280,200,{
                                                            "atak":enemy_skills["atak"],
                                                            "tchnienie śmierci":enemy_skills["tchnienie śmierci"],
                                                            "zemsta":enemy_skills["zemsta"],
                                                            "mocny_cios":enemy_skills["mocny_cios"],
                                                            "mocny_cios":enemy_skills["mocny_cios"],
                                                            "trujące opary":enemy_skills["trujące opary"],
                                                            },
                                                            {"graphics/items/pierscien_zdrowia.png":101,"graphics/items/pierscien_many.png":60},
                                                            "graphics/sprites/chory_jaszczur_sprite.png","chory_jaszczur",False)

przeklety_wojownik = Enemy("Przeklęty Wojownik",6,400,55,15,40,56,20,295,205,{
                                                            "atak":enemy_skills["atak"],
                                                            "atak":enemy_skills["atak"],
                                                            "przeklety_oddech":enemy_skills["przeklety_oddech"],
                                                            "zemsta":enemy_skills["zemsta"],
                                                            "zemsta":enemy_skills["zemsta"],
                                                            "mocny_cios":enemy_skills["mocny_cios"],
                                                            "klatwa":enemy_skills["klatwa"],
                                                            },
                                                            {"graphics/items/pierscien_sily.png":101,"graphics/items/pierscien_inteligencji.png":40,"graphics/items/pierscien_zrecznosci.png":60},
                                                            "graphics/sprites/przeklety_wojownik_sprite.png","przeklety_wojownik",False)
przeklety_wojownik2 = Enemy("Przeklęty Wojownik",6,400,55,15,40,56,20,295,205,{
                                                            "atak":enemy_skills["atak"],
                                                            "atak":enemy_skills["atak"],
                                                            "przeklety_oddech":enemy_skills["przeklety_oddech"],
                                                            "zemsta":enemy_skills["zemsta"],
                                                            "zemsta":enemy_skills["zemsta"],
                                                            "mocny_cios":enemy_skills["mocny_cios"],
                                                            "klatwa":enemy_skills["klatwa"],
                                                            },
                                                            {"graphics/items/pierscien_sily.png":101,"graphics/items/pierscien_inteligencji.png":40,"graphics/items/pierscien_zrecznosci.png":60},
                                                            "graphics/sprites/przeklety_wojownik_sprite.png","przeklety_wojownik",False)

przeklety_czempion = Enemy("Przeklęty Czempion",6,500,60,25,30,65,20,350,230,{
                                                            "atak":enemy_skills["atak"],
                                                            "smoczy_oddech":enemy_skills["smoczy_oddech"],
                                                            "bebny_strachu":enemy_skills["bebny_strachu"],
                                                            "morderczy_cios":enemy_skills["morderczy_cios"],
                                                            "morderczy_cios":enemy_skills["morderczy_cios"],
                                                            "zgnilizna":enemy_skills["zgnilizna"]
                                                            },
                                                            {"graphics/items/srednia_mikstura_zdrowia.png":50,"graphics/items/srednia_mikstura_many.png":50},
                                                            "graphics/sprites/przeklety_czempion_sprite.png","przeklety_czempion",False)
przeklety_czempion2 = Enemy("Przeklęty Czempion",6,500,60,25,30,65,20,350,230,{
                                                            "atak":enemy_skills["atak"],
                                                            "smoczy_oddech":enemy_skills["smoczy_oddech"],
                                                            "bebny_strachu":enemy_skills["bebny_strachu"],
                                                            "morderczy_cios":enemy_skills["morderczy_cios"],
                                                            "morderczy_cios":enemy_skills["morderczy_cios"],
                                                            "zgnilizna":enemy_skills["zgnilizna"]
                                                            },
                                                            {"graphics/items/srednia_mikstura_zdrowia.png":50,"graphics/items/srednia_mikstura_many.png":50},
                                                            "graphics/sprites/przeklety_czempion_sprite.png","przeklety_czempion",False)

golem = Enemy("Golem",6,500,30,25,20,35,37,400,200,{
                                                    "atak":enemy_skills["atak"],
                                                    "serce_natury":enemy_skills["serce_natury"],
                                                    "serce_natury":enemy_skills["serce_natury"],
                                                    "wstrzas":enemy_skills["wstrzas"],
                                                    "wstrzas":enemy_skills["wstrzas"],
                                                    "lawina głazów":enemy_skills["lawina głazów"],
                                                    "lubudu_i_bec":enemy_skills["lubudu_i_bec"],
                                                    "lubudu_i_bec":enemy_skills["lubudu_i_bec"],
                                                    "roztrzaskanie":enemy_skills["roztrzaskanie"],
                                                    "roztrzaskanie":enemy_skills["roztrzaskanie"],
                                                    "rzut głazem":enemy_skills["rzut głazem"],
                                                    "rzut głazem":enemy_skills["rzut głazem"],
                                                    "dzicz":enemy_skills["dzicz"],
                                                    "miazga":enemy_skills["miazga"],
                                                    },
                                                    {"graphics/items/serce_golema.png":101},
                                                    "graphics/sprites/golem_sprite.png","golem",False)

layt = Enemy("Wiedzma Layt",6,2000,66,66,66,66,0,500,400,{
                                                    "atak":enemy_skills["atak"],
                                                    "ciemnosc":enemy_skills["ciemnosc"],
                                                    "ciemnosc":enemy_skills["ciemnosc"],
                                                    "ciemnosc":enemy_skills["ciemnosc"],
                                                    "rozdarcie":enemy_skills["rozdarcie"],
                                                    "rozdarcie":enemy_skills["rozdarcie"],
                                                    "mroczna eksplozja":enemy_skills["mroczna eksplozja"],
                                                    "horror":enemy_skills["horror"],
                                                    "pycha":enemy_skills["pycha"],
                                                    "pycha":enemy_skills["pycha"],
                                                    "pycha":enemy_skills["pycha"],
                                                    "pycha":enemy_skills["pycha"],
                                                    "gniew":enemy_skills["gniew"],
                                                    "gniew":enemy_skills["gniew"],
                                                    "gniew":enemy_skills["gniew"],
                                                    "lenistwo":enemy_skills["lenistwo"],
                                                    "lenistwo":enemy_skills["lenistwo"],
                                                    "lenistwo":enemy_skills["lenistwo"],
                                                    },
                                                    {},
                                                    "graphics/sprites/layt_sprite.png","layt",False)





enemy_team = list()
enemy_team.append(skeleton1)
enemy_team.append(skeleton2)
enemy_team.append(skeleton3)
enemy_team_alive = list()

#character - after this fight you get new companion(max 2 at playthrough), one-time - this fight dont count to random fight, normal - well..it's normal XD
story_fight = {
    1:{
        1:[[first_enemy],"normal"],
        2:[[skeleton1,skeleton2],"normal"],
        3:[[skeleton_priest,skeleton1],"normal"],
        4:[[lost_soul],"character"],
        5:[[zjawa,skeleton_warrior],"normal"],
        6:[[rzeznik,skeleton_priest,skeleton_priest2],"normal"],
        7:[[zombie,zombie2],"normal"],
        8:[[skeleton_warrior,skeleton_warrior2,skeleton_warrior3],"normal"],
        9:[[skeleton_warrior,zombie,skeleton_priest3],"normal"],
        10:[[death_knight],"one_time"]
    },
    2:{
        1:[[wojownik_qin,wojownik_qin2],"normal"],
        2:[[rozdarta_dusza],"character"],
        3:[[wojownik_qin,wlocznik_qin, halabardnik_qin],"normal"],
        4:[[golem],"normal"],
        5:[[jaszczurzy_wojownik,jaszczurzy_zabojca],"normal"],
        6:[[jaszczurzy_czempion,jaszczurzy_wojownik,jaszczurzy_wojownik2],"normal"],
        7:[[nosiciel_swiatla,jaszczurzy_wojownik, jaszczurzy_wojownik2],"normal"],
        8:[[chory_jaszczur,chory_jaszczur2],"normal"],
        9:[[przeklety_wojownik,przeklety_czempion,],"normal"],
        10:[[layt],"one_time"]
    }
}