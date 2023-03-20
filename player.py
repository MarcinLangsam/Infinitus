from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock

global current_player

class Companion2_Sprite(Widget):
    sprite = ObjectProperty("hero_sprite.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = 0.0
        self.rate= 0.2
        self.frame = 1
        self.source = "hero_attack"
        self.frame_sum = 3
        self.anim = Clock.schedule_interval(self.animation, 0.3)
    def update(self):
        self.anim()
    def animation(self,dt):
        self.time += dt
        if (self.time > self.rate):
                self.time -= self.rate
                self.sprite = "atlas://"+self.source+"/frame" + str(self.frame)
                self.frame = self.frame + 1
                if (self.frame > self.frame_sum):
                    return False

    def set_sprite(self,sprite):
        self.sprite = sprite
class Companion1_Sprite(Widget):
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
        global animation_fin
        self.time += dt
        if (self.time > self.rate):
                self.time -= self.rate
                self.sprite = "atlas://"+self.source+"/frame" + str(self.frame)
                self.frame = self.frame + 1
                if (self.frame > self.frame_sum):
                    self.frame = 1
                    return False

    def set_sprite(self,sprite):
        self.sprite = sprite
class Main_Player_Sprite(Widget):
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

class Player():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Player"
        self.lv = 1
        self.MAX_HP = 100
        self.MAX_MP = 100
        self.HP = 100
        self.MP = 100
        self.STR = 30
        self.DEX = 10
        self.INT = 10
        self.weapon = 0
        self.damage = self.STR+self.weapon
        self.defence = 0
        self.crit_chance = 0.1*self.DEX
        self.dodge_chance = 0.02*self.DEX
        self.EXP_boost = 0.1*self.INT
        self.EXP = 0
        self.EXP_To_Lv = 100
        self.stat_points = 3
        self.skill_points = 2
        self.skill = {}

        self.inventory = {
            "main_hand" : [768-200,432,"empty_slot.png","main_hand"],
            "off_hand" : [768+200,432,"empty_slot.png","off_hand"],
            "armor" : [768,432+200,"empty_slot.png","armor"],
            "accessory" : [768,432-200,"empty_slot.png","accessory"],
            0 : [50,750,"sword.png","item"],
            1 : [150,750,"sword.png","item"],
            2 : [250,750,"empty_slot.png","item"], 
            3 : [350,750,"empty_slot.png","item"],
            4 : [450,750,"empty_slot.png","item"],
            5 : [50,650,"empty_slot.png","item"],
            6 : [150,650,"empty_slot.png","item"],
            7 : [250,650,"empty_slot.png","item"],
            8 : [350,650,"empty_slot.png","item"],
            9 : [450,650,"empty_slot.png","item"],
            10 : [50,550,"empty_slot.png","item"],
            11 : [150,550,"empty_slot.png","item"],
            12 : [250,550,"empty_slot.png","item"],
            13 : [350,550,"empty_slot.png","item"],
            14 : [450,550,"empty_slot.png","item"],
            15 : [50,450,"empty_slot.png","item"],
            16 : [150,450,"empty_slot.png","item"],
            17 : [250,450,"empty_slot.png","item"],
            18 : [350,450,"empty_slot.png","item"],
            19 : [450,450,"empty_slot.png","item"],
            20 : [50,350,"empty_slot.png","item"],
            21 : [150,350,"empty_slot.png","item"],
            22 : [250,350,"empty_slot.png","item"],
            23 : [350,350,"empty_slot.png","item"],
            24 : [450,350,"empty_slot.png","item"],
            25 : [50,250,"empty_slot.png","item"],
            26 : [150,250,"empty_slot.png","item"],
            27 : [250,250,"empty_slot.png","item"],
            28 : [350,250,"empty_slot.png","item"],
            29 : [450,250,"empty_slot.png","item"],
            30 : [50,150,"empty_slot.png","item"],
            31 : [150,150,"empty_slot.png","item"],
            32 : [250,150,"empty_slot.png","item"],
            33 : [350,150,"empty_slot.png","item"],
            34 : [450,150,"empty_slot.png","item"],
            35 : [50,50,"empty_slot.png","item"],
            36 : [150,50,"empty_slot.png","item"],
            37 : [250,50,"empty_slot.png","item"],
            38 : [350,50,"empty_slot.png","item"],
            39 : [450,50,"empty_slot.png","item"],
            #część ekwipunku przeznaczona dla sklepu oraz łupu po walce
            40 : [650,750,"empty_slot.png","item"],
            41 : [750,750,"empty_slot.png","item"],
            42 : [850,750,"empty_slot.png","item"], 
            43 : [950,750,"empty_slot.png","item"],
            44 : [1050,750,"empty_slot.png","item"],
            45 : [650,650,"empty_slot.png","item"],
            46 : [750,650,"empty_slot.png","item"],
            47 : [850,650,"empty_slot.png","item"],
            48 : [950,650,"empty_slot.png","item"],
            49 : [1050,650,"empty_slot.png","item"],
            50 : [650,550,"empty_slot.png","item"],
            51 : [750,550,"empty_slot.png","item"],
            52 : [850,550,"empty_slot.png","item"],
            53 : [950,550,"empty_slot.png","item"],
            54 : [1050,550,"empty_slot.png","item"],
            55 : [650,450,"empty_slot.png","item"],
            56 : [750,450,"empty_slot.png","item"],
            57 : [850,450,"empty_slot.png","item"],
            58 : [950,450,"empty_slot.png","item"],
            59 : [1050,450,"empty_slot.png","item"],
            60 : [650,350,"empty_slot.png","item"],
            61 : [750,350,"empty_slot.png","item"],
            62 : [850,350,"empty_slot.png","item"],
            63 : [950,350,"empty_slot.png","item"],
            64 : [1050,350,"empty_slot.png","item"],
            65 : [650,250,"empty_slot.png","item"],
            66 : [750,250,"empty_slot.png","item"],
            67 : [850,250,"empty_slot.png","item"],
            68 : [950,250,"empty_slot.png","item"],
            69 : [1050,250,"empty_slot.png","item"],
            70 : [650,150,"empty_slot.png","item"],
            71 : [750,150,"empty_slot.png","item"],
            72 : [850,150,"empty_slot.png","item"],
            73 : [950,150,"empty_slot.png","item"],
            74 : [1050,150,"empty_slot.png","item"],
            75 : [650,50,"empty_slot.png","item"],
            76 : [750,50,"empty_slot.png","item"],
            77 : [850,50,"empty_slot.png","item"],
            78 : [950,50,"empty_slot.png","item"],
            79 : [1050,50,"empty_slot.png","item"],
        }

class Companion():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Companion"
        self.lv = 1
        self.MAX_HP = 100
        self.MAX_MP = 100
        self.HP = 100
        self.MP = 100
        self.STR = 40
        self.DEX = 20
        self.INT = 20
        self.weapon = 0
        self.damage = self.STR+self.weapon
        self.defence = 0
        self.crit_chance = 0.1*self.DEX
        self.dodge_chance = 0.02*self.DEX
        self.EXP_boost = 0.1*self.INT
        self.EXP = 0
        self.EXP_To_Lv = 100
        self.stat_points = 5
        self.skill_points = 2
        self.skill = {}

        self.inventory = {
            "main_hand" : [768-200,432,"empty_slot.png","main_hand"],
            "off_hand" : [768+200,432,"empty_slot.png","off_hand"],
            "armor" : [768,432+200,"empty_slot.png","armor"],
            "accessory" : [768,432-200,"empty_slot.png","accessory"],
            0 : [50,750,"sword.png","item"],
            1 : [150,750,"sword.png","item"],
            2 : [250,750,"empty_slot.png","item"], 
            3 : [350,750,"empty_slot.png","item"],
            4 : [450,750,"empty_slot.png","item"],
            5 : [50,650,"empty_slot.png","item"],
            6 : [150,650,"empty_slot.png","item"],
            7 : [250,650,"empty_slot.png","item"],
            8 : [350,650,"empty_slot.png","item"],
            9 : [450,650,"empty_slot.png","item"],
            10 : [50,550,"empty_slot.png","item"],
            11 : [150,550,"empty_slot.png","item"],
            12 : [250,550,"empty_slot.png","item"],
            13 : [350,550,"empty_slot.png","item"],
            14 : [450,550,"empty_slot.png","item"],
            15 : [50,450,"empty_slot.png","item"],
            16 : [150,450,"empty_slot.png","item"],
            17 : [250,450,"empty_slot.png","item"],
            18 : [350,450,"empty_slot.png","item"],
            19 : [450,450,"empty_slot.png","item"],
            20 : [50,350,"empty_slot.png","item"],
            21 : [150,350,"empty_slot.png","item"],
            22 : [250,350,"empty_slot.png","item"],
            23 : [350,350,"empty_slot.png","item"],
            24 : [450,350,"empty_slot.png","item"],
            25 : [50,250,"empty_slot.png","item"],
            26 : [150,250,"empty_slot.png","item"],
            27 : [250,250,"empty_slot.png","item"],
            28 : [350,250,"empty_slot.png","item"],
            29 : [450,250,"empty_slot.png","item"],
            30 : [50,150,"empty_slot.png","item"],
            31 : [150,150,"empty_slot.png","item"],
            32 : [250,150,"empty_slot.png","item"],
            33 : [350,150,"empty_slot.png","item"],
            34 : [450,150,"empty_slot.png","item"],
            35 : [50,50,"empty_slot.png","item"],
            36 : [150,50,"empty_slot.png","item"],
            37 : [250,50,"empty_slot.png","item"],
            38 : [350,50,"empty_slot.png","item"],
            39 : [450,50,"empty_slot.png","item"],
            #część ekwipunku przeznaczona dla sklepu oraz łupu po walce
            40 : [650,750,"empty_slot.png","item"],
            41 : [750,750,"empty_slot.png","item"],
            42 : [850,750,"empty_slot.png","item"], 
            43 : [950,750,"empty_slot.png","item"],
            44 : [1050,750,"empty_slot.png","item"],
            45 : [650,650,"empty_slot.png","item"],
            46 : [750,650,"empty_slot.png","item"],
            47 : [850,650,"empty_slot.png","item"],
            48 : [950,650,"empty_slot.png","item"],
            49 : [1050,650,"empty_slot.png","item"],
            50 : [650,550,"empty_slot.png","item"],
            51 : [750,550,"empty_slot.png","item"],
            52 : [850,550,"empty_slot.png","item"],
            53 : [950,550,"empty_slot.png","item"],
            54 : [1050,550,"empty_slot.png","item"],
            55 : [650,450,"empty_slot.png","item"],
            56 : [750,450,"empty_slot.png","item"],
            57 : [850,450,"empty_slot.png","item"],
            58 : [950,450,"empty_slot.png","item"],
            59 : [1050,450,"empty_slot.png","item"],
            60 : [650,350,"empty_slot.png","item"],
            61 : [750,350,"empty_slot.png","item"],
            62 : [850,350,"empty_slot.png","item"],
            63 : [950,350,"empty_slot.png","item"],
            64 : [1050,350,"empty_slot.png","item"],
            65 : [650,250,"empty_slot.png","item"],
            66 : [750,250,"empty_slot.png","item"],
            67 : [850,250,"empty_slot.png","item"],
            68 : [950,250,"empty_slot.png","item"],
            69 : [1050,250,"empty_slot.png","item"],
            70 : [650,150,"empty_slot.png","item"],
            71 : [750,150,"empty_slot.png","item"],
            72 : [850,150,"empty_slot.png","item"],
            73 : [950,150,"empty_slot.png","item"],
            74 : [1050,150,"empty_slot.png","item"],
            75 : [650,50,"empty_slot.png","item"],
            76 : [750,50,"empty_slot.png","item"],
            77 : [850,50,"empty_slot.png","item"],
            78 : [950,50,"empty_slot.png","item"],
            79 : [1050,50,"empty_slot.png","item"],
        }

main_player = Player()
current_player = main_player
companion1 = Companion()
companion2 = Companion() 

team = list()
team.append(main_player)
team.append(companion1)
gold = 0