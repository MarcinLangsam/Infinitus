import player,inventory_manager as im, random, status_effect as se
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

global player_team_alive
global enemy_team_alive
player_team_alive = player.team

current = 0

class Enemy_Sprite(Widget):
    sprite = ObjectProperty("")
    weapon = ObjectProperty("")

    def __init__(self,enemy_sprite,**kwargs):
        super().__init__(**kwargs)
        self.time = 0.0
        self.rate= 0.03
        self.frame = 1
        self.source = "enemy_anim"
        self.frame_sum = 28
        self.weapon_source = "empty_slot"
        self.sprite = enemy_sprite
        self.set_sprite()
                
    def set_sprite(self):
        self.sprite = self.sprite
        self.anim = self.sprite[15:-4]
    def set_anim_parameters(self,time,rate,frame,frame_sum):
        self.time = time
        self.rate = rate
        self.frame = frame
        self.frame = frame_sum

class Enemy(Widget):
    def __init__(self, name, lv, MAX_HP, STR, DEX, INT, damage, defence, exp_gain, gold_gain,AI, enemy_drop,enemy_sprite):
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
        self.exp_gain = exp_gain
        self.gold_gain = gold_gain
        self.AI = AI
        self.enemy_drop = enemy_drop
        self.enemy_sprite = enemy_sprite
        self.status = list()
        self.actions = list()

    def action(self,action,sort_by,value,type,name,distance):
        print(player_team_alive)
        ok = False
        if type == "on_character" or "attack":
            targets = player_team_alive
        if type == "on_enemy":
            targets = enemy_team_alive
        if type == "on_self":
            targets = current
        
        if sort_by == "by_HP":
            if type == "on_self":
                if targets.HP <= targets.MAX_HP*value:
                    self.actions.append([targets,action,name,distance])
            else:
                for x in targets:
                    if x.HP >= x.MAX_HP*value:
                        self.actions.append([x,action,name,distance])
        if sort_by == "by_status":
            if type == "on_self":
                    for x in targets.status:
                        if se.status_effect.status_list[value][0] == x[0][0]:
                            ok = True
                    if ok == False:
                        self.actions.append([targets,action,name,distance])
            else:
                for x in targets:
                    ok = False
                    for y in x.status:
                        if se.status_effect.status_list[value][0] == y[0][0]:
                            ok = True
                    if ok == False:
                        self.actions.append([x,action,name,distance])

        ###################################################################
        if type == "attack":
            chanse = random.randint(0,100)
            if len(targets) == 1:
                self.actions.append([player_team_alive[0],action,"",distance])
            if len(targets) == 2:
                if chanse >=0 and chanse <= 40:
                    self.actions.append([player_team_alive[0],action,"",distance])
                elif chanse > 40 and chanse <= 100:
                    self.actions.append([player_team_alive[1],action,"",distance])
            if len(targets) == 3:
                if chanse >=0 and chanse <= 20:
                    self.actions.append([player_team_alive[0],action,"",distance])
                elif chanse > 20 and chanse <= 70:
                    self.actions.append([player_team_alive[1],action,"",distance])
                elif chanse > 70 and chanse <= 100:
                    self.actions.append([player_team_alive[2],action,"",distance])
                    
        
    def set_actions(self):
        self.actions.clear()
        for x in self.AI:
            self.action(enemy_skills[x][1],enemy_skills[x][2],enemy_skills[x][3],enemy_skills[x][4],enemy_skills[x][0],enemy_skills[x][5])
        chose = random.randint(0,len(self.actions)-1)
        return self.actions[chose]

    def drop_mashine(self):
        drop_roll = random.randint(0,100)
        items_droped = list()
        count = 0
        for x in self.enemy_drop.keys():
            if drop_roll < self.enemy_drop[x]:
                items_droped.append(x)
        for x in range(40,40+len(items_droped)):
            player.current_player.inventory[x][2] = items_droped[count]
            count += 1

enemy_skills ={
            #nazwa(0)  efekt(1)     po czym wybrać cel(2)       mnożnik statystyki(3)   typ(4)  dystans(5)
    "atak":["atak","self.final_damage = self.current_turn.damage",0,0,"attack","melee"],
    "szarża":["Szarża","self.final_damage = (self.current_turn.damage*2)","by_HP",1,"on_character","melee"],
    "leczenie":["Leczenie","self.final_damage = -(self.current_turn.INT*3)","by_HP",0.5,"on_enemy","ranged"],
    "zemsta":["Zemsta","self.current_target.status.append([se.status_effect.status_list['zemsta'].copy(),se.Status_Icon('graphics/icons/zemsta_status.png','Zemsta\\nCel zadaje półtora razy więcej obrażeń'),Label(font_size = 22)])\nself.final_damage = 'ZEMSTA!'","by_HP",1,"on_self", "status"],
    "zatrucie":["Zatrucie","self.current_target.status.append([se.status_effect.status_list['trucizna'].copy(),se.Status_Icon('graphics/icons/trucizna_status.png','Trucizna\\nCel traci 5% zdrowia co turę'),Label(font_size = 22)])\nself.final_damage = 'ZATRUCIE!'","by_status","trucizna","on_charcter","status"],
    "mroczny_pocisk":["Mroczny Pocisk","self.final_damage = self.current_turn.INT",0,0,"attack","ranged"],
    "mroczna_potega":["Mroczna Potęga","self.current_target.status.append([se.status_effect.status_list['mroczna potega'].copy(),se.Status_Icon('graphics/icons/mroczna_potega_status.png','Mroczna Potęga\\nCel zadaje 100% więcej obrażeń\\nale traci cały pancerz'),Label(font_size = 22)])\nself.final_damage = 'MROCZNA POTĘGA!'","by_status","mroczna potega","on_enemy","status"],
    "uderzenie_smierci":["Uderzenie Śmierci","self.final_damage = (self.current_turn.STR)","by_HP",0.2,"on_character","melee"],
    "obezwladnienie":["Obezwładnienie","self.current_target.status.append([se.status_effect.status_list['obezwladnienie'].copy(),se.Status_Icon('graphics/icons/ogluszenie_status.png','Obezwładnienie\\nCel pomija swoją turę'),Label(font_size = 22)])\nself.final_damage = 'OBEZWŁADNIENIE!'","by_status","obezwladnienie","on_character","status"],
    "niemoc":["Niemoc","self.current_target.status.append([se.status_effect.status_list['osłabienie'].copy(),se.Status_Icon('graphics/icons/niemoc_status.png','Niemoc\\nCel zadaje tylko połowę obrażeń'),Label(font_size = 22)])\nself.final_damage = 'NIEMOC!'","by_status","osłabienie","on_character","status"]
}
                #nazwa #lv #MAX_HP #STR #DEX #INT #Obrażenia #Pancerz #EXP #Złoto #AI #drop #sprite
skeleton = Enemy("Szkielet",1,50,20,10,10,20,0,50,10,{"atak":enemy_skills["atak"]},{"graphics/items/pierscien_sily.png":50},"graphics/items/skeleton.png")
skeleton2 = Enemy("Szkielet",1,50,10,10,10,20,0,50,10,{"atak":enemy_skills["atak"]},{"graphics/items/pierscien_sily.png":50},"graphics/items/skeleton.png")
skeleton3 = Enemy("Szkielet",1,50,10,10,10,20,0,50,10,{"atak":enemy_skills["atak"]},{"graphics/items/pierscien_sily.png":50},"graphics/items/skeleton.png")
death_knight = Enemy("Rycerz Śmierci",3,500,50,20,35,30,20,500,1000,{"atak":enemy_skills["atak"],"mroczna_potega":enemy_skills["mroczna_potega"],"atak":enemy_skills["atak"],"mroczna_potega":enemy_skills["mroczna_potega"],"uderzenie_smierci":enemy_skills["uderzenie_smierci"],"obezwladnienie":enemy_skills["obezwladnienie"]},{},"graphics/items/death_knight.png")
death_knight2 = Enemy("Rycerz Śmierci",3,500,50,20,35,30,20,500,1000,{"atak":enemy_skills["atak"],"mroczna_potega":enemy_skills["mroczna_potega"],"atak":enemy_skills["atak"],"mroczna_potega":enemy_skills["mroczna_potega"],"uderzenie_smierci":enemy_skills["uderzenie_smierci"],"obezwladnienie":enemy_skills["obezwladnienie"]},{},"graphics/items/death_knight.png")
death_knight3 = Enemy("Rycerz Śmierci",3,500,50,20,35,30,20,500,1000,{"atak":enemy_skills["atak"],"mroczna_potega":enemy_skills["mroczna_potega"],"atak":enemy_skills["atak"],"mroczna_potega":enemy_skills["mroczna_potega"],"uderzenie_smierci":enemy_skills["uderzenie_smierci"],"obezwladnienie":enemy_skills["obezwladnienie"]},{},"graphics/items/death_knight.png")

#skeleton_priest = Enemy("Duch Wojownika",2,150,20,5,10,20,10,50,100,{"atak":enemy_skills["atak"],"leczenie":enemy_skills["leczenie"],"szarża":enemy_skills["szarża"]},{"graphics/items/pierscien_sily.png":50},"graphics/items/skeleton.png")
#skeleton_warrior = Enemy("Upadły kapłan",3,70,5,20,30,5,5,50,100,{"atak":enemy_skills["atak"],"leczenie":enemy_skills["leczenie"],"szarża":enemy_skills["szarża"]},{"graphics/items/pierscien_sily.png":50},"graphics/items/skeleton.png")

enemy_team = list()
enemy_team.append(skeleton)
enemy_team.append(skeleton2)
enemy_team.append(skeleton3)
enemy_team_alive = list()

story_fight = {
    1:{
        1:[skeleton,skeleton2,skeleton3],
        2:[death_knight],
        3:[death_knight,death_knight2,death_knight3]
    }
}