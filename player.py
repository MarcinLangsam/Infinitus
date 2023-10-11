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
    sprite = ObjectProperty("graphics/items/empty_slot_sprite_a.png")
    weapon = ObjectProperty("graphics/items/empty_slot_sprite_w.png")

    def __init__(self,character,type, **kwargs):
        super().__init__(**kwargs)
        self.time = 0.0
        self.rate= 0.02
        self.frame = 1
        self.source = "character_anim"
        self.frame_sum = 46
        self.weapon_source = "empty_slot"
        self.character = character
        self.set_sprite_weapon()
        self.set_sprite(type)
        self.set_weapon()
        self.size_hint = (0.36,0.47)

    def set_sprite(self,type):
        self.sprite = self.character.inventory["armor"][2]
        self.sprite = self.sprite[:-4]
        self.anim = self.sprite[15:]
        #self.sprite = self.sprite + "_sprite_a.png"
        self.sprite = self.sprite + "_sprite_a_"+type+".png"
        self.anim = self.anim + "_"+type
        print(self.anim)
    def set_sprite_weapon(self):
        self.weapon = self.character.inventory["main_hand"][2]
        self.weapon = self.weapon[:-4]
        self.weapon = self.weapon + "_sprite_w.png"
    def set_weapon(self):
        self.weapon_source = self.character.inventory["main_hand"][2]
        self.weapon_source = self.weapon_source[:-4]
        self.weapon_source = self.weapon_source[15:]
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
        self.DEX = 10
        self.INT = 10
        self.weapon = 0
        self.damage = self.STR+self.weapon
        self.defence = 0
        self.crit_chance = 0.01*self.DEX
        self.dodge_chance = 0.02*self.DEX
        self.EXP_boost = 0.01*self.INT
        self.EXP = 0
        self.EXP_To_Lv = 100
        self.stat_points = 20
        self.skill_points = 18
        self.skill = {}
        self.status = list()

        self.inventory = {
            "main_hand" : [768-200,432,"graphics/items/empty_slot.png","main_hand"],
            "off_hand" : [768+130,432,"graphics/items/empty_slot.png","off_hand"],
            "armor" : [730,432+180,"graphics/items/empty_slot.png","armor"],
            "accessory" : [730,432-180,"graphics/items/empty_slot.png","accessory"],
            0 : [50,750,"graphics/items/miecz_poltorareczny.png","item"],
            1 : [150,750,"graphics/items/laska_maga.png","item"],
            2 : [250,750,"graphics/items/majcher_lotra.png","item"], 
            3 : [350,750,"graphics/items/zbroja_plytowa.png","item"],
            4 : [450,750,"graphics/items/kaftan_zlodzieja.png","item"],
            5 : [50,650,"graphics/items/szata_maga.png","item"],
            6 : [150,650,"graphics/items/drewniany_puklerz.png","item"],
            7 : [250,650,"graphics/items/ksiega_czarow.png","item"],
            8 : [350,650,"graphics/items/skorzany_pancerz.png","item"],
            9 : [450,650,"graphics/items/skorzany_pancerz.png","item"],
            10 : [50,550,"graphics/items/skorzany_pancerz.png","item"],
            11 : [150,550,"graphics/items/zelazny_miecz.png","item"],
            12 : [250,550,"graphics/items/zelazny_miecz.png","item"],
            13 : [350,550,"graphics/items/miecz_z_brazu.png","item"],
            14 : [450,550,"graphics/items/miecz_z_brazu.png","item"],
            15 : [50,450,"graphics/items/miecz_jednoreczny.png","item"],
            16 : [150,450,"graphics/items/miecz_dwureczny.png","item"],
            17 : [250,450,"graphics/items/test_armor.png","item"],
            18 : [350,450,"graphics/items/test_armor.png","item"],
            19 : [450,450,"graphics/items/test_armor.png","item"],
            20 : [50,350,"graphics/items/mlot.png","item"],
            21 : [150,350,"graphics/items/empty_slot.png","item"],
            22 : [250,350,"graphics/items/empty_slot.png","item"],
            23 : [350,350,"graphics/items/empty_slot.png","item"],
            24 : [450,350,"graphics/items/empty_slot.png","item"],
            25 : [50,250,"graphics/items/empty_slot.png","item"],
            26 : [150,250,"graphics/items/empty_slot.png","item"],
            27 : [250,250,"graphics/items/empty_slot.png","item"],
            28 : [350,250,"graphics/items/empty_slot.png","item"],
            29 : [450,250,"graphics/items/empty_slot.png","item"],
            30 : [50,150,"graphics/items/empty_slot.png","item"],
            31 : [150,150,"graphics/items/empty_slot.png","item"],
            32 : [250,150,"graphics/items/empty_slot.png","item"],
            33 : [350,150,"graphics/items/empty_slot.png","item"],
            34 : [450,150,"graphics/items/empty_slot.png","item"],
            35 : [50,50,"graphics/items/empty_slot.png","item"],
            36 : [150,50,"graphics/items/empty_slot.png","item"],
            37 : [250,50,"graphics/items/empty_slot.png","item"],
            38 : [350,50,"graphics/items/empty_slot.png","item"],
            39 : [450,50,"graphics/items/empty_slot.png","item"],
            #część ekwipunku przeznaczona dla sklepu oraz łupu po walce
            40 : [950,750,"graphics/items/empty_slot.png","item"],
            41 : [1050,750,"graphics/items/empty_slot.png","item"],
            42 : [1150,750,"graphics/items/empty_slot.png","item"], 
            43 : [1250,750,"graphics/items/empty_slot.png","item"],
            44 : [1350,750,"graphics/items/empty_slot.png","item"],
            45 : [950,650,"graphics/items/empty_slot.png","item"],
            46 : [1050,650,"graphics/items/empty_slot.png","item"],
            47 : [1150,650,"graphics/items/empty_slot.png","item"],
            48 : [1250,650,"graphics/items/empty_slot.png","item"],
            49 : [1350,650,"graphics/items/empty_slot.png","item"],
            50 : [950,550,"graphics/items/empty_slot.png","item"],
            51 : [1050,550,"graphics/items/empty_slot.png","item"],
            52 : [1150,550,"graphics/items/empty_slot.png","item"],
            53 : [1250,550,"graphics/items/empty_slot.png","item"],
            54 : [1350,550,"graphics/items/empty_slot.png","item"],
            55 : [950,450,"graphics/items/empty_slot.png","item"],
            56 : [1050,450,"graphics/items/empty_slot.png","item"],
            57 : [1150,450,"graphics/items/empty_slot.png","item"],
            58 : [1250,450,"graphics/items/empty_slot.png","item"],
            59 : [1350,450,"graphics/items/empty_slot.png","item"],
            60 : [950,350,"graphics/items/empty_slot.png","item"],
            61 : [1050,350,"graphics/items/empty_slot.png","item"],
            62 : [1150,350,"graphics/items/empty_slot.png","item"],
            63 : [1250,350,"graphics/items/empty_slot.png","item"],
            64 : [1350,350,"graphics/items/empty_slot.png","item"],
            65 : [950,250,"graphics/items/empty_slot.png","item"],
            66 : [1050,250,"graphics/items/empty_slot.png","item"],
            67 : [1150,250,"graphics/items/empty_slot.png","item"],
            68 : [1250,250,"graphics/items/empty_slot.png","item"],
            69 : [1350,250,"graphics/items/empty_slot.png","item"],
            70 : [950,150,"graphics/items/empty_slot.png","item"],
            71 : [1050,150,"graphics/items/empty_slot.png","item"],
            72 : [1150,150,"graphics/items/empty_slot.png","item"],
            73 : [1250,150,"graphics/items/empty_slot.png","item"],
            74 : [1350,150,"graphics/items/empty_slot.png","item"],
            75 : [950,50,"graphics/items/empty_slot.png","item"],
            76 : [1050,50,"graphics/items/empty_slot.png","item"],
            77 : [1150,50,"graphics/items/empty_slot.png","item"],
            78 : [1250,50,"graphics/items/empty_slot.png","item"],
            79 : [1350,50,"graphics/items/empty_slot.png","item"],
        }

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
