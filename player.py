from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

global current_player

def level_up(character):
        character.EXP = 0
        character.EXP_To_Lv += 100
        character.stat_points += 5
        character.skill_points += 1
        character.lv += 1

class Character_Sprite(Widget):
    sprite = ObjectProperty("graphics/sprites/empty_slot_sprite_a.png")
    weapon = ObjectProperty("graphics/sprites/empty_slot_sprite_w.png")
    head = ObjectProperty("graphics/sprites/glowa2_sprite.png")

    def __init__(self,character,type,head_source, **kwargs):
        super().__init__(**kwargs)
        self.time = 0.0
        self.rate= 0.00001
        self.frame = 1
        self.source = "character_anim"
        self.frame_sum = 46
        self.weapon_source = "empty_slot"
        self.head_source = head_source
        self.character = character
        self.portrait = ""
        self.set_sprite_weapon()
        self.set_sprite(type)
        self.set_weapon()
        self.set_head()
        
    def set_sprite(self,type):
        self.base = self.character.inventory["armor"][2]
        self.base = self.base[:-4]
        self.base = self.base[15:]
        self.source = self.base
        self.sprite = "graphics/sprites/"+self.base+"_sprite_a_"+type+".png"
        self.anim = type
    def set_sprite_weapon(self):

        self.base = self.character.inventory["main_hand"][2]
        self.base = self.base[:-4]
        self.base = self.base[15:]
        self.weapon = "graphics/sprites/"+self.base + "_sprite_w.png"
    def set_weapon(self):
        self.base = self.character.inventory["main_hand"][2]
        self.base = self.base[:-4]
        self.base = self.base[15:]
        self.weapon_source = self.base
    def set_head(self):
        self.head = "graphics/sprites/"+self.head_source+"_sprite.png"
        self.portrait = "graphics/sprites/"+self.head_source+"_portrait.png"
        print(self.portrait)
    def set_anim_parameters(self,time,rate,frame,frame_sum):
        self.time = time
        self.rate = rate
        self.frame = frame
        self.frame = frame_sum

class Character(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Player"
        self.lv = 1
        self.MAX_HP = 100
        self.MAX_MP = 100
        self.HP = 100
        self.MP = 100
        self.STR = 10
        self.DEX = 30
        self.INT = 10
        self.weapon = 0
        self.damage = self.STR+self.weapon
        self.defence = 0
        self.crit_chance = round(0.01*self.DEX,2)
        self.dodge_chance = round(0.02*self.DEX,2)
        self.EXP_boost = round(0.01*self.INT,2)
        self.EXP = 0
        self.EXP_To_Lv = 100
        self.stat_points = 20
        self.skill_points = 18
        self.skill = {}
        self.status = list()
        self.head = "glowa1"

        self.inventory = {
            "main_hand" : [568,542,"graphics/items/empty_slot.png","main_hand"],
            "off_hand" : [568,432,"graphics/items/empty_slot.png","off_hand"],
            "armor" : [568,322,"graphics/items/empty_slot.png","armor"],
            "accessory" : [918,542,"graphics/items/empty_slot.png","accessory"],
            "accessory2" : [918,432,"graphics/items/empty_slot.png","accessory"],
            "accessory3" : [918,322,"graphics/items/empty_slot.png","accessory"],
            0 : [120,650,"graphics/items/skorzany_pancerz.png","item"],
            1 : [190,650,"graphics/items/skorzany_pancerz.png","item"],
            2 : [260,650,"graphics/items/skorzany_pancerz.png","item"], 
            3 : [330,650,"graphics/items/miedziany_sztylet.png","item"],
            4 : [400,650,"graphics/items/mlot_bojowy.png","item"],
            5 : [470,650,"graphics/items/pika.png","item"],
            6 : [120,580,"graphics/items/miecz_rycerski.png","item"],
            7 : [190,580,"graphics/items/empty_slot.png","item"],
            8 : [260,580,"graphics/items/empty_slot.png","item"],
            9 : [330,580,"graphics/items/empty_slot.png","item"],
            10 : [400,580,"graphics/items/empty_slot.png","item"],
            11 : [470,580,"graphics/items/empty_slot.png","item"],
            12 : [120,510,"graphics/items/empty_slot.png","item"],
            13 : [190,510,"graphics/items/empty_slot.png","item"],
            14 : [260,510,"graphics/items/empty_slot.png","item"],
            15 : [330,510,"graphics/items/empty_slot.png","item"],
            16 : [400,510,"graphics/items/empty_slot.png","item"],
            17 : [470,510,"graphics/items/empty_slot.png","item"],
            18 : [120,440,"graphics/items/empty_slot.png","item"],
            19 : [190,440,"graphics/items/empty_slot.png","item"],
            20 : [260,440,"graphics/items/empty_slot.png","item"],
            21 : [330,440,"graphics/items/empty_slot.png","item"],
            22 : [400,440,"graphics/items/empty_slot.png","item"],
            23 : [470,440,"graphics/items/empty_slot.png","item"],
            24 : [120,370,"graphics/items/empty_slot.png","item"],
            25 : [190,370,"graphics/items/empty_slot.png","item"],
            26 : [260,370,"graphics/items/empty_slot.png","item"],
            27 : [330,370,"graphics/items/empty_slot.png","item"],
            28 : [400,370,"graphics/items/empty_slot.png","item"],
            29 : [470,370,"graphics/items/empty_slot.png","item"],
            30 : [120,300,"graphics/items/empty_slot.png","item"],
            31 : [190,300,"graphics/items/empty_slot.png","item"],
            32 : [260,300,"graphics/items/empty_slot.png","item"],
            33 : [330,300,"graphics/items/empty_slot.png","item"],
            34 : [400,300,"graphics/items/empty_slot.png","item"],
            35 : [470,300,"graphics/items/empty_slot.png","item"],
            36 : [120,230,"graphics/items/empty_slot.png","item"],
            37 : [190,230,"graphics/items/empty_slot.png","item"],
            38 : [260,230,"graphics/items/empty_slot.png","item"],
            39 : [330,230,"graphics/items/empty_slot.png","item"],
            40 : [400,230,"graphics/items/empty_slot.png","item"],
            41 : [470,230,"graphics/items/empty_slot.png","item"],
            42 : [120,160,"graphics/items/empty_slot.png","item"],
            43 : [190,160,"graphics/items/empty_slot.png","item"],
            44 : [260,160,"graphics/items/empty_slot.png","item"],
            45 : [330,160,"graphics/items/empty_slot.png","item"],
            46 : [400,160,"graphics/items/empty_slot.png","item"],
            47 : [470,160,"graphics/items/empty_slot.png","item"],
            #część ekwipunku przeznaczona dla sklepu oraz łupu po walce
            48 : [1050,750,"graphics/items/empty_slot.png","item"],
            49 : [1120,750,"graphics/items/empty_slot.png","item"],
            50 : [1190,750,"graphics/items/empty_slot.png","item"], 
            51 : [1260,750,"graphics/items/empty_slot.png","item"],
            52 : [1330,750,"graphics/items/empty_slot.png","item"],
            53 : [1400,750,"graphics/items/empty_slot.png","item"],
            54 : [1050,680,"graphics/items/empty_slot.png","item"],
            55 : [1120,680,"graphics/items/empty_slot.png","item"],
            56 : [1190,680,"graphics/items/empty_slot.png","item"],
            57 : [1260,680,"graphics/items/empty_slot.png","item"],
            58 : [1330,680,"graphics/items/empty_slot.png","item"],
            59 : [1400,680,"graphics/items/empty_slot.png","item"],
            60 : [1050,610,"graphics/items/empty_slot.png","item"],
            61 : [1120,610,"graphics/items/empty_slot.png","item"],
            62 : [1190,610,"graphics/items/empty_slot.png","item"],
            63 : [1260,610,"graphics/items/empty_slot.png","item"],
            64 : [1330,610,"graphics/items/empty_slot.png","item"],
            65 : [1400,610,"graphics/items/empty_slot.png","item"],
            66 : [1050,540,"graphics/items/empty_slot.png","item"],
            67 : [1120,540,"graphics/items/empty_slot.png","item"],
            68 : [1190,540,"graphics/items/empty_slot.png","item"],
            69 : [1260,540,"graphics/items/empty_slot.png","item"],
            70 : [1330,540,"graphics/items/empty_slot.png","item"],
            71 : [1400,540,"graphics/items/empty_slot.png","item"],
            72 : [1050,470,"graphics/items/empty_slot.png","item"],
            73 : [1120,470,"graphics/items/empty_slot.png","item"],
            74 : [1190,470,"graphics/items/empty_slot.png","item"],
            75 : [1260,470,"graphics/items/empty_slot.png","item"],
            76 : [1330,470,"graphics/items/empty_slot.png","item"],
            77 : [1400,470,"graphics/items/empty_slot.png","item"],
            78 : [1050,400,"graphics/items/empty_slot.png","item"],
            79 : [1120,400,"graphics/items/empty_slot.png","item"],
            80 : [1190,400,"graphics/items/empty_slot.png","item"],
            81 : [1260,400,"graphics/items/empty_slot.png","item"],
            82 : [1330,400,"graphics/items/empty_slot.png","item"],
            83 : [1400,400,"graphics/items/empty_slot.png","item"],
            84 : [1050,330,"graphics/items/empty_slot.png","item"],
            85 : [1120,330,"graphics/items/empty_slot.png","item"],
            86 : [1190,330,"graphics/items/empty_slot.png","item"],
            87 : [1260,330,"graphics/items/empty_slot.png","item"],
            88 : [1330,330,"graphics/items/empty_slot.png","item"],
            89 : [1400,330,"graphics/items/empty_slot.png","item"],
            90 : [1050,260,"graphics/items/empty_slot.png","item"],
            91 : [1120,260,"graphics/items/empty_slot.png","item"],
            92 : [1190,260,"graphics/items/empty_slot.png","item"],
            93 : [1260,260,"graphics/items/empty_slot.png","item"],
            94 : [1330,260,"graphics/items/empty_slot.png","item"],
            95 : [1400,260,"graphics/items/empty_slot.png","item"],
        }
    def reset_player(self):
        self.name = "Player"
        self.lv = 1
        self.MAX_HP = 100
        self.MAX_MP = 100
        self.HP = 100
        self.MP = 100
        self.STR = 10
        self.DEX = 10
        self.INT = 10
        self.weapon = 0
        self.damage = self.STR+self.weapon
        self.defence = 0
        self.crit_chance = round(0.01*self.DEX,2)
        self.dodge_chance = round(0.02*self.DEX,2)
        self.EXP_boost = round(0.01*self.INT,2)
        self.EXP = 0
        self.EXP_To_Lv = 100
        self.stat_points = 20
        self.skill_points = 18
        self.skill = {}
        self.status = list()

main_player = Character()
main_player.name = "Gracz Pierwszy"
current_player = main_player
companion1 = Character()
companion1.name = "Gracz Drugi"
companion2 = Character()
companion2.name = "Gracz Trzeci"
       
team = list()
team.append(main_player)
team.append(companion1)
team.append(companion2)
gold = 1000
