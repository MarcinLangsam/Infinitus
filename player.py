from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

global current_player

def level_up(character):
        print("HALOO")
        character.EXP = 0
        character.EXP_To_Lv += 100
        character.stat_points += 7
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
        self.skill_points = 3

        self.skill = {}
        self.status = list()
        self.head = "glowa1"
        self.potions = 0
        self.potion_effect = ""
        self.current_potions = 0

        self.blok = False

        self.inventory = {
            "main_hand" : [568,542,"graphics/items/empty_slot.png","main_hand"],
            "off_hand" : [568,432,"graphics/items/empty_slot.png","off_hand"],
            "armor" : [568,322,"graphics/items/empty_slot.png","armor"],
            "accessory" : [918,542,"graphics/items/empty_slot.png","accessory"],
            "accessory2" : [918,432,"graphics/items/empty_slot.png","accessory"],
            "accessory3" : [918,322,"graphics/items/empty_slot.png","accessory"],
            "potion" : [918,222,"graphics/items/empty_slot.png","potion"],
            0 : [120,650,"graphics/items/skorzany_pancerz.png","item"],
            1 : [190,650,"graphics/items/skorzany_pancerz.png","item"],
            2 : [260,650,"graphics/items/skorzany_pancerz.png","item"], 
            3 : [330,650,"graphics/items/miedziany_sztylet.png","item"],
            4 : [400,650,"graphics/items/mlot_bojowy.png","item"],
            5 : [470,650,"graphics/items/pika.png","item"],
            6 : [120,580,"graphics/items/miecz_rycerski.png","item"],
            7 : [190,580,"graphics/items/mała_mikstura_zdrowia.png","item"],
            8 : [260,580,"graphics/items/mała_mikstura_zdrowia.png","item"],
            9 : [330,580,"graphics/items/mała_mikstura_zdrowia.png","item"],
            10 : [400,580,"graphics/items/dwureczny_topor_rzeznika.png","item"],
            11 : [470,580,"graphics/items/gladius.png","item"],
            12 : [120,510,"graphics/items/grzech_kaplana.png","item"],
            13 : [190,510,"graphics/items/kostur_maga.png","item"],
            14 : [260,510,"graphics/items/maczuga_zolnierska.png","item"],
            15 : [330,510,"graphics/items/miecz_poltorareczny.png","item"],
            16 : [400,510,"graphics/items/miecz_z_brazu.png","item"],
            17 : [470,510,"graphics/items/rozczka_z_krysztalem_blyskawicy.png","item"],
            18 : [120,440,"graphics/items/rytualny_sztylet.png","item"],
            19 : [190,440,"graphics/items/siewca_smierci.png","item"],
            20 : [260,440,"graphics/items/stalowy_miecz.png","item"],
            21 : [330,440,"graphics/items/topor_wojownika.png","item"],
            22 : [400,440,"graphics/items/wlocznia_straznicza.png","item"],
            23 : [470,440,"graphics/items/kolczuga.png","item"],
            24 : [120,370,"graphics/items/pikowany_pancerz.png","item"],
            25 : [190,370,"graphics/items/szata_maga.png","item"],
            26 : [260,370,"graphics/items/przyszywanica.png","item"],
            27 : [330,370,"graphics/items/kolczuga.png","item"],
            28 : [400,370,"graphics/items/kolczuga.png","item"],
            29 : [470,370,"graphics/items/szata_maga.png","item"],
            30 : [120,300,"graphics/items/szata_maga.png","item"],
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
            48 : [1050,650,"graphics/items/empty_slot.png","item"],
            49 : [1120,650,"graphics/items/empty_slot.png","item"],
            50 : [1190,650,"graphics/items/empty_slot.png","item"], 
            51 : [1260,650,"graphics/items/empty_slot.png","item"],
            52 : [1330,650,"graphics/items/empty_slot.png","item"],
            53 : [1400,650,"graphics/items/empty_slot.png","item"],
            54 : [1050,580,"graphics/items/empty_slot.png","item"],
            55 : [1120,580,"graphics/items/empty_slot.png","item"],
            56 : [1190,580,"graphics/items/empty_slot.png","item"],
            57 : [1260,580,"graphics/items/empty_slot.png","item"],
            58 : [1330,580,"graphics/items/empty_slot.png","item"],
            59 : [1400,580,"graphics/items/empty_slot.png","item"],
            60 : [1050,510,"graphics/items/empty_slot.png","item"],
            61 : [1120,510,"graphics/items/empty_slot.png","item"],
            62 : [1190,510,"graphics/items/empty_slot.png","item"],
            63 : [1260,510,"graphics/items/empty_slot.png","item"],
            64 : [1330,510,"graphics/items/empty_slot.png","item"],
            65 : [1400,510,"graphics/items/empty_slot.png","item"],
            66 : [1050,440,"graphics/items/empty_slot.png","item"],
            67 : [1120,440,"graphics/items/empty_slot.png","item"],
            68 : [1190,440,"graphics/items/empty_slot.png","item"],
            69 : [1260,440,"graphics/items/empty_slot.png","item"],
            70 : [1330,440,"graphics/items/empty_slot.png","item"],
            71 : [1400,440,"graphics/items/empty_slot.png","item"],
            72 : [1050,370,"graphics/items/empty_slot.png","item"],
            73 : [1120,370,"graphics/items/empty_slot.png","item"],
            74 : [1190,370,"graphics/items/empty_slot.png","item"],
            75 : [1260,370,"graphics/items/empty_slot.png","item"],
            76 : [1330,370,"graphics/items/empty_slot.png","item"],
            77 : [1400,370,"graphics/items/empty_slot.png","item"],
            78 : [1050,300,"graphics/items/empty_slot.png","item"],
            79 : [1120,300,"graphics/items/empty_slot.png","item"],
            80 : [1190,300,"graphics/items/empty_slot.png","item"],
            81 : [1260,300,"graphics/items/empty_slot.png","item"],
            82 : [1330,300,"graphics/items/empty_slot.png","item"],
            83 : [1400,300,"graphics/items/empty_slot.png","item"],
            84 : [1050,230,"graphics/items/empty_slot.png","item"],
            85 : [1120,230,"graphics/items/empty_slot.png","item"],
            86 : [1190,230,"graphics/items/empty_slot.png","item"],
            87 : [1260,230,"graphics/items/empty_slot.png","item"],
            88 : [1330,230,"graphics/items/empty_slot.png","item"],
            89 : [1400,230,"graphics/items/empty_slot.png","item"],
            90 : [1050,160,"graphics/items/empty_slot.png","item"],
            91 : [1120,160,"graphics/items/empty_slot.png","item"],
            92 : [1190,160,"graphics/items/empty_slot.png","item"],
            93 : [1260,160,"graphics/items/empty_slot.png","item"],
            94 : [1330,160,"graphics/items/empty_slot.png","item"],
            95 : [1400,160,"graphics/items/empty_slot.png","item"],
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
        self.skill_points = 3
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
