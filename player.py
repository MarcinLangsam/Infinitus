from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.metrics import dp

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
    effect = ObjectProperty("graphics/effects/no_effect.png")

    def __init__(self,character,type,head_source, **kwargs):
        super().__init__(**kwargs)
        self.time = 0.0
        self.rate= 0.00001
        self.frame = 1
        self.source = "character_anim"
        self.frame_sum = 46
        self.weapon_source = "empty_slot"
        self.effect_source = ""
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
        #print(self.sprite)
        #print(self.anim)
        #print(self.source)

    def set_sprite_weapon(self):
        self.base = self.character.inventory["main_hand"][2]
        self.base = self.base[:-4]
        self.base = self.base[15:]
        self.weapon = "graphics/sprites/"+self.base + "_sprite_w.png"
        #print(self.weapon)
    def set_weapon(self):
        self.base = self.character.inventory["main_hand"][2]
        self.base = self.base[:-4]
        self.base = self.base[15:]
        self.weapon_source = self.base
        #print(self.weapon_source)
        #print("TUTAJ JEDNO SIĘ KOŃCZY\n")
    def set_head(self):
        self.head = "graphics/sprites/"+self.head_source+"_sprite.png"
        self.portrait = "graphics/sprites/"+self.head_source+"_portrait.png"
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
        self.MP_regen = 10

        self.STR = 10
        self.DEX = 10
        self.INT = 10


        self.STR_base = 10
        self.DEX_base = 10
        self.INT_base = 10

        self.weapon = 0
        self.damage = self.STR+self.weapon
        self.damage_bonus = 0
        self.damage_special_effect = ""
        self.damage_base = self.STR_base+self.weapon
        self.defence_base = 0

        
        self.defence = self.defence_base
        self.crit_chance_base = round(0.1*self.DEX,2)
        self.dodge_chance_base = round(0.02*self.DEX,2)
        self.crit_chance = round(0.1*self.DEX_base,2)
        self.dodge_chance = round(0.02*self.DEX_base,2)
        self.EXP_boost = round(0.1*self.INT_base,2)

        self.STR_modifier = 1
        self.DEX_modifier = 1
        self.INT_modifier = 1
        self.damage_modifier = 1
        self.defence_modifier = 1
        self.crit_chance_modifier = 0
        self.dodge_chance_modifier = 0
        self.damage_reduction = 1

        self.crit_chance_bonus = 0
        self.dodge_chance_bonus = 0
        self.EXP_boost_bonus = 0
        self.EXP = 0
        self.EXP_To_Lv = 100
        self.stat_points = 0
        self.skill_points = 30

        self.skill = {}
        self.status = list()
        self.head = "glowa1"
        self.potions = 0
        self.potion_effect = ""
        self.current_potions = 0

        self.blok = False

        self.inventory = {
            "main_hand" : [dp(600),dp(550),"graphics/items/empty_slot.png","main_hand"],
            "off_hand" : [dp(600),dp(450),"graphics/items/empty_slot.png","off_hand"],
            "armor" : [dp(600),dp(350),"graphics/items/empty_slot.png","armor"],
            "accessory" : [dp(880),dp(550),"graphics/items/empty_slot.png","accessory"],
            "accessory2" : [dp(880),dp(450),"graphics/items/empty_slot.png","accessory"],
            "accessory3" : [dp(880),dp(350),"graphics/items/empty_slot.png","accessory"],
            "potion" : [dp(880),dp(250),"graphics/items/empty_slot.png","potion"],
            0 : [dp(200),dp(600),"graphics/items/skorzany_pancerz.png","item"],
            1 : [dp(255),dp(600),"graphics/items/skorzany_pancerz.png","item"],
            2 : [dp(310),dp(600),"graphics/items/skorzany_pancerz.png","item"], 
            3 : [dp(365),dp(600),"graphics/items/miedziany_sztylet.png","item"],
            4 : [dp(420),dp(600),"graphics/items/mlot_bojowy.png","item"],
            5 : [dp(475),dp(600),"graphics/items/pika.png","item"],
            6 : [dp(200),dp(545),"graphics/items/miecz_rycerski.png","item"],
            7 : [dp(255),dp(545),"graphics/items/mała_mikstura_zdrowia.png","item"],
            8 : [dp(310),dp(545),"graphics/items/mała_mikstura_zdrowia.png","item"],
            9 : [dp(365),dp(545),"graphics/items/mała_mikstura_zdrowia.png","item"],
            10 : [dp(420),dp(545),"graphics/items/dwureczny_topor_rzeznika.png","item"],
            11 : [dp(475),dp(545),"graphics/items/gladius.png","item"],
            12 : [dp(200),dp(490),"graphics/items/grzech_kaplana.png","item"],
            13 : [dp(255),dp(490),"graphics/items/kostur_maga.png","item"],
            14 : [dp(310),dp(490),"graphics/items/maczuga_zolnierska.png","item"],
            15 : [dp(365),dp(490),"graphics/items/miecz_poltorareczny.png","item"],
            16 : [dp(420),dp(490),"graphics/items/miecz_z_brazu.png","item"],
            17 : [dp(475),dp(490),"graphics/items/rozczka_z_krysztalem_blyskawicy.png","item"],
            18 : [dp(200),dp(435),"graphics/items/rytualny_sztylet.png","item"],
            19 : [dp(255),dp(435),"graphics/items/siewca_smierci.png","item"],
            20 : [dp(310),dp(435),"graphics/items/stalowy_miecz.png","item"],
            21 : [dp(365),dp(435),"graphics/items/topor_wojownika.png","item"],
            22 : [dp(420),dp(435),"graphics/items/wlocznia_straznicza.png","item"],
            23 : [dp(475),dp(435),"graphics/items/kolczuga.png","item"],
            24 : [dp(200),dp(380),"graphics/items/pikowany_pancerz.png","item"],
            25 : [dp(255),dp(380),"graphics/items/szata_maga.png","item"],
            26 : [dp(310),dp(380),"graphics/items/przyszywanica.png","item"],
            27 : [dp(365),dp(380),"graphics/items/kolczuga.png","item"],
            28 : [dp(420),dp(380),"graphics/items/kolczuga.png","item"],
            29 : [dp(475),dp(380),"graphics/items/szata_maga.png","item"],
            30 : [dp(200),dp(325),"graphics/items/szata_maga.png","item"],
            31 : [dp(255),dp(325),"graphics/items/empty_slot.png","item"],
            32 : [dp(310),dp(325),"graphics/items/empty_slot.png","item"],
            33 : [dp(365),dp(325),"graphics/items/empty_slot.png","item"],
            34 : [dp(420),dp(325),"graphics/items/empty_slot.png","item"],
            35 : [dp(475),dp(325),"graphics/items/empty_slot.png","item"],
            36 : [dp(200),dp(270),"graphics/items/empty_slot.png","item"],
            37 : [dp(255),dp(270),"graphics/items/empty_slot.png","item"],
            38 : [dp(310),dp(270),"graphics/items/empty_slot.png","item"],
            39 : [dp(365),dp(270),"graphics/items/empty_slot.png","item"],
            40 : [dp(420),dp(270),"graphics/items/empty_slot.png","item"],
            41 : [dp(475),dp(270),"graphics/items/empty_slot.png","item"],
            42 : [dp(200),dp(215),"graphics/items/empty_slot.png","item"],
            43 : [dp(255),dp(215),"graphics/items/empty_slot.png","item"],
            44 : [dp(310),dp(215),"graphics/items/empty_slot.png","item"],
            45 : [dp(365),dp(215),"graphics/items/empty_slot.png","item"],
            46 : [dp(420),dp(215),"graphics/items/empty_slot.png","item"],
            47 : [dp(475),dp(215),"graphics/items/empty_slot.png","item"],
            #część ekwipunku przeznaczona dla sklepu oraz łupu po walce
            48 : [dp(900),dp(600),"graphics/items/empty_slot.png","item"],
            49 : [dp(955),dp(600),"graphics/items/empty_slot.png","item"],
            50 : [dp(1010),dp(600),"graphics/items/empty_slot.png","item"], 
            51 : [dp(1065),dp(600),"graphics/items/empty_slot.png","item"],
            52 : [dp(1120),dp(600),"graphics/items/empty_slot.png","item"],
            53 : [dp(1175),dp(600),"graphics/items/empty_slot.png","item"],
            54 : [dp(900),dp(545),"graphics/items/empty_slot.png","item"],
            55 : [dp(955),dp(545),"graphics/items/empty_slot.png","item"],
            56 : [dp(1010),dp(545),"graphics/items/empty_slot.png","item"],
            57 : [dp(1065),dp(545),"graphics/items/empty_slot.png","item"],
            58 : [dp(1120),dp(545),"graphics/items/empty_slot.png","item"],
            59 : [dp(1175),dp(545),"graphics/items/empty_slot.png","item"],
            60 : [dp(900),dp(490),"graphics/items/empty_slot.png","item"],
            61 : [dp(955),dp(490),"graphics/items/empty_slot.png","item"],
            62 : [dp(1010),dp(490),"graphics/items/empty_slot.png","item"],
            63 : [dp(1065),dp(490),"graphics/items/empty_slot.png","item"],
            64 : [dp(1120),dp(490),"graphics/items/empty_slot.png","item"],
            65 : [dp(1175),dp(490),"graphics/items/empty_slot.png","item"],
            66 : [dp(900),dp(435),"graphics/items/empty_slot.png","item"],
            67 : [dp(955),dp(435),"graphics/items/empty_slot.png","item"],
            68 : [dp(1010),dp(435),"graphics/items/empty_slot.png","item"],
            69 : [dp(1065),dp(435),"graphics/items/empty_slot.png","item"],
            70 : [dp(1120),dp(435),"graphics/items/empty_slot.png","item"],
            71 : [dp(1175),dp(435),"graphics/items/empty_slot.png","item"],
            72 : [dp(900),dp(380),"graphics/items/empty_slot.png","item"],
            73 : [dp(955),dp(380),"graphics/items/empty_slot.png","item"],
            74 : [dp(1010),dp(380),"graphics/items/empty_slot.png","item"],
            75 : [dp(1065),dp(380),"graphics/items/empty_slot.png","item"],
            76 : [dp(1120),dp(380),"graphics/items/empty_slot.png","item"],
            77 : [dp(1175),dp(380),"graphics/items/empty_slot.png","item"],
            78 : [dp(900),dp(325),"graphics/items/empty_slot.png","item"],
            79 : [dp(955),dp(325),"graphics/items/empty_slot.png","item"],
            80 : [dp(1010),dp(325),"graphics/items/empty_slot.png","item"],
            81 : [dp(1065),dp(325),"graphics/items/empty_slot.png","item"],
            82 : [dp(1120),dp(325),"graphics/items/empty_slot.png","item"],
            83 : [dp(1175),dp(325),"graphics/items/empty_slot.png","item"],
            84 : [dp(900),dp(270),"graphics/items/empty_slot.png","item"],
            85 : [dp(955),dp(270),"graphics/items/empty_slot.png","item"],
            86 : [dp(1010),dp(270),"graphics/items/empty_slot.png","item"],
            87 : [dp(1065),dp(270),"graphics/items/empty_slot.png","item"],
            88 : [dp(1120),dp(270),"graphics/items/empty_slot.png","item"],
            89 : [dp(1175),dp(270),"graphics/items/empty_slot.png","item"],
            90 : [dp(900),dp(215),"graphics/items/empty_slot.png","item"],
            91 : [dp(955),dp(215),"graphics/items/empty_slot.png","item"],
            92 : [dp(1010),dp(215),"graphics/items/empty_slot.png","item"],
            93 : [dp(1065),dp(215),"graphics/items/empty_slot.png","item"],
            94 : [dp(1120),dp(215),"graphics/items/empty_slot.png","item"],
            95 : [dp(1175),dp(215),"graphics/items/empty_slot.png","item"],
        }
    def reset_player(self):
        self.name = "Player"
        self.lv = 1
        self.MAX_HP = 100
        self.MAX_MP = 100
        self.HP = 100
        self.MP = 100
        self.MP_regen = 10
        self.STR = 10
        self.DEX = 10
        self.INT = 10

        self.STR_base = 10
        self.DEX_base = 10
        self.INT_base = 10
        self.damage_base = self.STR_base+self.weapon
        self.defence_base = 0

        self.STR_modifier = 1
        self.DEX_modifier = 1
        self.INT_modifier = 1
        self.damage_modifier = 1
        self.defence_modifier = 1
        self.crit_chance_modifier = 0
        self.dodge_chance_modifier = 0

        self.weapon = 0
        self.damage = self.STR+self.weapon
        self.damage_bonus = 0
        self.damage_special_effect = ""
        self.defence = 0
        self.crit_chance_base = round(0.1*self.DEX,2)
        self.dodge_chance_base = round(0.02*self.DEX,2)
        self.crit_chance = round(0.1*self.DEX,2)
        self.dodge_chance = round(0.02*self.DEX,2)
        self.EXP_boost = round(0.1*self.INT,2)
        self.crit_chance_bonus = 0
        self.dodge_chance_bonus = 0
        self.EXP_boost_bonus = 0
        self.EXP = 0
        self.EXP_To_Lv = 100
        self.stat_points = 0
        self.skill_points = 30
        self.skill = {}
        self.status = list()
        self.head = "glowa1"
        self.potions = 0
        self.potion_effect = ""
        self.current_potions = 0
        self.inventory["main_hand"][2] = "graphics/items/empty_slot.png"
        self.inventory["off_hand"][2] = "graphics/items/empty_slot.png"
        self.inventory["armor"][2] = "graphics/items/empty_slot.png"
        self.inventory["accessory"][2] = "graphics/items/empty_slot.png"
        self.inventory["accessory2"][2] = "graphics/items/empty_slot.png"
        self.inventory["accessory3"][2] = "graphics/items/empty_slot.png"
        self.inventory["potion"][2] = "graphics/items/empty_slot.png"

        self.blok = False

    def update_player_stats(self):
        self.STR = self.STR_base
        self.INT = self.INT_base
        self.DEX = self.DEX_base
        self.damage_base = self.STR_base+self.weapon
        self.damage = self.STR+self.weapon
        self.crit_chance_base = round(0.1*self.DEX,2)
        self.dodge_chance_base = round(0.02*self.DEX,2)
        self.crit_chance = round(0.1*self.DEX,2)
        self.dodge_chance = round(0.02*self.DEX,2)
        self.EXP_boost = round(0.1*self.INT,2)
        
    def printBattleStats(self):
        print("STR "+str(self.STR))
        print("DEX "+str(self.DEX))
        print("INT "+str(self.INT))
        print("Weapon Damage "+str(self.weapon))
        print("Final Damage "+str(self.damage))
        print("Defence "+str(self.defence))
        
        print("Damage modifier "+str(self.damage_modifier))
        print("STR modifier "+str(self.STR_modifier))
        print("DEX modifier "+str(self.DEX_modifier))
        print("INT modifier "+str(self.INT_modifier))
        print("Defence modifier "+str(self.defence_modifier))
        print("Damage modifier "+str(self.damage_modifier))
        

main_player = Character()
main_player.name = "Gracz Pierwszy"
current_player = main_player
companion1 = Character()
companion1.name = "Gracz Drugi"
companion2 = Character()
companion2.name = "Gracz Trzeci"
       
team = list()
team.append(main_player)
gold = 1000
