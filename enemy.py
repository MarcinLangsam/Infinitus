import player,inventory_manager as im, random
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock

global player_team_alive
player_team_alive = player.team

class Enemy1_Sprite(Widget):
    sprite = ObjectProperty("hero_sprite.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = 0.0
        self.rate= 0.2
        self.frame = 1
        self.source = "hero_attack"
        self.frame_sum = 3

    def update(self):
        Clock.schedule_interval(self.animation, 0.3)
    def animation(self,dt):
        self.time += dt
        if (self.time > self.rate):
                self.time -= self.rate
                self.sprite = "atlas://"+self.source+"/frame" + str(self.frame)
                self.frame = self.frame + 1
                if (self.frame >= self.frame_sum):
                    self.frame = 1
                    exec("self.run_animation()")
                    

    def set_sprite(self,sprite):
        self.sprite = sprite

class Enemy2_Sprite(Widget):
    sprite = ObjectProperty("hero_sprite.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = 0.0
        self.rate= 0.2
        self.frame = 1
        self.source = "hero_attack"
        self.frame_sum = 3

    def update(self):
        Clock.schedule_interval(self.animation, 0.3)
    def animation(self,dt):
        self.time += dt
        if (self.time > self.rate):
                self.time -= self.rate
                self.sprite = "atlas://"+self.source+"/frame" + str(self.frame)
                self.frame = self.frame + 1
                if (self.frame > self.frame_sum):
                    self.frame = 1

    def set_sprite(self,sprite):
        self.sprite = sprite

class Enemy3_Sprite(Widget):
    sprite = ObjectProperty("hero_sprite.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = 0.0
        self.rate= 0.2
        self.frame = 1
        self.source = "hero_attack"
        self.frame_sum = 3

    def update(self):
        Clock.schedule_interval(self.animation, 0.3)
    def animation(self,dt):
        self.time += dt
        if (self.time > self.rate):
                self.time -= self.rate
                self.sprite = "atlas://"+self.source+"/frame" + str(self.frame)
                self.frame = self.frame + 1
                if (self.frame > self.frame_sum):
                    self.frame = 1

    def set_sprite(self,sprite):
        self.sprite = sprite

class Enemy(Widget):
    def __init__(self, name, lv, MAX_HP, MAX_MP, HP, MP, STR, DEX, INT, defence, crit_chance, damage, exp_gain,gold_gain,enemy_drop):
        super().__init__()
        self.name = name
        self.lv = lv
        self.MAX_HP = MAX_HP
        self.MAX_MP = MAX_MP
        self.HP = HP
        self.MP = MP
        self.STR = STR
        self.DEX = DEX
        self.INT = INT
        self.defence = defence
        self.crit_chance = crit_chance
        self.damage = damage
        self.exp_gain = exp_gain
        self.gold_gain = gold_gain
        self.AI = {}
        self.target = 0
        self.enemy_drop = enemy_drop
    
    def check_what_to_do(self):
        heal_target = 0
        cast_target = 0
        attack_target = 0
        actions = list()
        actions.clear()
        for x in self.AI:
            if self.AI[x][4] == "heal":
                heal_target = self.chose_to_heal(self.AI[x][3])
                if heal_target != 0:
                    actions.append([heal_target,self.AI[x]])
            elif self.AI[x][4] == "cast":
                cast_target = self.chose_to_cast(self.AI[x][3])
                if cast_target != 0:
                    actions.append([cast_target,self.AI[x]])
            elif self.AI[x][4] == "attack":
                attack_target = self.chose_to_attack()
                if attack_target != 0:    
                    actions.append([attack_target,self.AI[x]])
        chosen_target = random.randint(0,len(actions)-1)
        return actions[chosen_target]
        
    def chose_to_heal(self,value):
        self.target = 0
        for x in range(0,len(enemy_team)):
            if enemy_team[x].HP <= (enemy_team[x].MAX_HP*value):
                self.heal = True
                self.target = enemy_team[x]
        return self.target
    def chose_to_cast(self,value):
        self.target = 0
        for x in self.AI:
            if self.AI[x][0] == "atak":
                pass
            elif self.AI[x][2] == "by_HP":
                value = self.AI[x][3]
                for x in range(0,len(player_team_alive)):
                    if player_team_alive[x].HP >= (player_team_alive[x].MAX_HP*value):
                        self.cast = True
                        self.target = player_team_alive[x]                     
                return self.target
    def sort_by(self,e):
        return e.HP
    def chose_to_attack(self):
        self.target = 0
        targets = list()
        for x in range(0,len(player_team_alive)):
            targets.append(player_team_alive[x])
        targets.sort(key=self.sort_by)
        chanse = random.randint(0,100)
        self.attack = True
        if len(targets) == 1:
            self.target = targets[0]
            return self.target
        if len(targets) == 2:
            if chanse >=0 and chanse <= 40:
                self.target = targets[0]
                return self.target
            elif chanse > 40 and chanse <= 100:
                self.target = targets[1]
                return self.target
        if len(targets) == 3:
            if chanse >=0 and chanse <= 20:
                self.target = targets[0]
                return self.target
            elif chanse > 20 and chanse <= 70:
                self.target = targets[1]
                return self.target
            elif chanse > 70 and chanse <= 100:
                self.target = targets[2]
                return self.target       

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
    "atak":["atak","self.player.HP -= self.enemy.damage",0,0,"attack"],
    "szarża":["szarża","self.player.HP -= (self.enemy.damage*2)","by_HP",1,"cast"]
}

skeleton = Enemy("Szkielet",1,100,100,100,10,10,10,10,0,0,10,10,10,{"shield.png":70,"armor.png":50,"ring.png":20,"sword.png":50})
zombie = Enemy("Zombie",1,100,100,100,100,10,10,10,0,0,10,10,10,{})
spider = Enemy("Pająk",1,100,100,100,100,10,10,10,0,0,10,10,10,{})
skeleton.AI["atak"] = enemy_skills["atak"]
skeleton.AI["szarża"] = enemy_skills["szarża"]

zombie.AI["atak"] = enemy_skills["atak"]
zombie.AI["szarża"] = enemy_skills["szarża"]

spider.AI["atak"] = enemy_skills["atak"]
spider.AI["szarża"] = enemy_skills["szarża"]
enemy_team = list()
enemy_team.append(skeleton)
enemy_team.append(zombie)
enemy_team.append(spider)

story_fight = {
    1:{
        1:[skeleton],
        2:[skeleton,zombie],
        3:[spider,zombie]
    }
}