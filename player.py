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
        self.MP_regen_base = 10
        self.MP_regen_modifier = 0

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
        self.potion_description = ""

        self.blok = False
        #skok o 0.062!!! -------------------------------------------
        self.inventory = {
            "main_hand" : [0.38,0.7,"graphics/items/empty_slot.png","main_hand"],
            "off_hand" : [0.38,0.6,"graphics/items/empty_slot.png","off_hand"],
            "armor" : [0.38,0.5,"graphics/items/skorzany_pancerz.png","armor"],
            "accessory" : [0.6,0.7,"graphics/items/empty_slot.png","accessory"],
            "accessory2" : [0.6,0.6,"graphics/items/empty_slot.png","accessory"],
            "accessory3" : [0.6,0.5,"graphics/items/empty_slot.png","accessory"],
            "potion" : [0.6,0.4,"graphics/items/empty_slot.png","potion"],
            0 : [0.14,0.72,"graphics/items/skorzany_pancerz.png","item"],
            1 : [0.175,0.72,"graphics/items/skorzany_pancerz.png","item"],
            2 : [0.21,0.72,"graphics/items/skorzany_pancerz.png","item"], 
            3 : [0.245,0.72,"graphics/items/miedziany_sztylet.png","item"],
            4 : [0.28,0.72,"graphics/items/mlot_bojowy.png","item"],
            5 : [0.315,0.72,"graphics/items/pika.png","item"],
            6 : [0.14,0.658,"graphics/items/miecz_rycerski.png","item"],
            7 : [0.175,0.658,"graphics/items/mała_mikstura_zdrowia.png","item"],
            8 : [0.21,0.658,"graphics/items/mała_mikstura_zdrowia.png","item"],
            9 : [0.245,0.658,"graphics/items/mała_mikstura_zdrowia.png","item"],
            10 : [0.28,0.658,"graphics/items/dwureczny_topor_rzeznika.png","item"],
            11 : [0.315,0.658,"graphics/items/gladius.png","item"],
            12 : [0.14,0.596,"graphics/items/grzech_kaplana.png","item"],
            13 : [0.175,0.596,"graphics/items/kostur_maga.png","item"],
            14 : [0.21,0.596,"graphics/items/maczuga_zolnierska.png","item"],
            15 : [0.245,0.596,"graphics/items/miecz_poltorareczny.png","item"],
            16 : [0.28,0.596,"graphics/items/miecz_z_brazu.png","item"],
            17 : [0.315,0.596,"graphics/items/rozczka_z_krysztalem_blyskawicy.png","item"],
            18 : [0.14,0.534,"graphics/items/rytualny_sztylet.png","item"],
            19 : [0.175,0.534,"graphics/items/siewca_smierci.png","item"],
            20 : [0.21,0.534,"graphics/items/stalowy_miecz.png","item"],
            21 : [0.245,0.534,"graphics/items/topor_wojownika.png","item"],
            22 : [0.28,0.534,"graphics/items/wlocznia_straznicza.png","item"],
            23 : [0.315,0.534,"graphics/items/kolczuga.png","item"],
            24 : [0.14,0.472,"graphics/items/pikowany_pancerz.png","item"],
            25 : [0.175,0.472,"graphics/items/szata_maga.png","item"],
            26 : [0.21,0.472,"graphics/items/przyszywanica.png","item"],
            27 : [0.245,0.472,"graphics/items/kolczuga.png","item"],
            28 : [0.28,0.472,"graphics/items/kolczuga.png","item"],
            29 : [0.315,0.472,"graphics/items/szata_maga.png","item"],
            30 : [0.14,0.41,"graphics/items/szata_maga.png","item"],
            31 : [0.175,0.41,"graphics/items/empty_slot.png","item"],
            32 : [0.21,0.41,"graphics/items/empty_slot.png","item"],
            33 : [0.245,0.41,"graphics/items/empty_slot.png","item"],
            34 : [0.28,0.41,"graphics/items/pancerz_z_wzmocnionej_skory.png","item"],
            35 : [0.315,0.41,"graphics/items/gladius.png","item"],
            36 : [0.14,0.348,"graphics/items/gladius.png","item"],
            37 : [0.175,0.348,"graphics/items/empty_slot.png","item"],
            38 : [0.21,0.348,"graphics/items/empty_slot.png","item"],
            39 : [0.245,0.348,"graphics/items/empty_slot.png","item"],
            40 : [0.28,0.348,"graphics/items/empty_slot.png","item"],
            41 : [0.315,0.348,"graphics/items/empty_slot.png","item"],
            42 : [0.14,0.286,"graphics/items/empty_slot.png","item"],
            43 : [0.175,0.286,"graphics/items/empty_slot.png","item"],
            44 : [0.21,0.286,"graphics/items/empty_slot.png","item"],
            45 : [0.245,0.286,"graphics/items/empty_slot.png","item"],
            46 : [0.28,0.286,"graphics/items/empty_slot.png","item"],
            47 : [0.315,0.286,"graphics/items/empty_slot.png","item"],
            #część ekwipunku przeznaczona dla sklepu oraz łupu po walce
            48 : [0.65,0.72,"graphics/items/empty_slot.png","item"],
            49 : [0.685,0.72,"graphics/items/empty_slot.png","item"],
            50 : [0.72,0.72,"graphics/items/empty_slot.png","item"], 
            51 : [0.755,0.72,"graphics/items/empty_slot.png","item"],
            52 : [0.79,0.72,"graphics/items/empty_slot.png","item"],
            53 : [0.825,0.72,"graphics/items/empty_slot.png","item"],
            54 : [0.65,0.658,"graphics/items/empty_slot.png","item"],
            55 : [0.685,0.658,"graphics/items/empty_slot.png","item"],
            56 : [0.72,0.658,"graphics/items/empty_slot.png","item"],
            57 : [0.755,0.658,"graphics/items/empty_slot.png","item"],
            58 : [0.79,0.658,"graphics/items/empty_slot.png","item"],
            59 : [0.825,0.658,"graphics/items/empty_slot.png","item"],
            60 : [0.65,0.596,"graphics/items/empty_slot.png","item"],
            61 : [0.685,0.596,"graphics/items/empty_slot.png","item"],
            62 : [0.72,0.596,"graphics/items/empty_slot.png","item"],
            63 : [0.755,0.596,"graphics/items/empty_slot.png","item"],
            64 : [0.79,0.596,"graphics/items/empty_slot.png","item"],
            65 : [0.825,0.596,"graphics/items/empty_slot.png","item"],
            66 : [0.65,0.534,"graphics/items/empty_slot.png","item"],
            67 : [0.685,0.534,"graphics/items/empty_slot.png","item"],
            68 : [0.72,0.534,"graphics/items/empty_slot.png","item"],
            69 : [0.755,0.534,"graphics/items/empty_slot.png","item"],
            70 : [0.79,0.534,"graphics/items/empty_slot.png","item"],
            71 : [0.825,0.534,"graphics/items/empty_slot.png","item"],
            72 : [0.65,0.472,"graphics/items/empty_slot.png","item"],
            73 : [0.685,0.472,"graphics/items/empty_slot.png","item"],
            74 : [0.72,0.472,"graphics/items/empty_slot.png","item"],
            75 : [0.755,0.472,"graphics/items/empty_slot.png","item"],
            76 : [0.79,0.472,"graphics/items/empty_slot.png","item"],
            77 : [0.825,0.472,"graphics/items/empty_slot.png","item"],
            78 : [0.65,0.41,"graphics/items/empty_slot.png","item"],
            79 : [0.685,0.41,"graphics/items/empty_slot.png","item"],
            80 : [0.72,0.41,"graphics/items/empty_slot.png","item"],
            81 : [0.755,0.41,"graphics/items/empty_slot.png","item"],
            82 : [0.79,0.41,"graphics/items/empty_slot.png","item"],
            83 : [0.825,0.41,"graphics/items/empty_slot.png","item"],
            84 : [0.65,0.348,"graphics/items/empty_slot.png","item"],
            85 : [0.685,0.348,"graphics/items/empty_slot.png","item"],
            86 : [0.72,0.348,"graphics/items/empty_slot.png","item"],
            87 : [0.755,0.348,"graphics/items/empty_slot.png","item"],
            88 : [0.79,0.348,"graphics/items/empty_slot.png","item"],
            89 : [0.825,0.348,"graphics/items/empty_slot.png","item"],
            90 : [0.65,0.286,"graphics/items/empty_slot.png","item"],
            91 : [0.685,0.286,"graphics/items/empty_slot.png","item"],
            92 : [0.72,0.286,"graphics/items/empty_slot.png","item"],
            93 : [0.755,0.286,"graphics/items/empty_slot.png","item"],
            94 : [0.79,0.286,"graphics/items/empty_slot.png","item"],
            95 : [0.825,0.286,"graphics/items/empty_slot.png","item"],
        }

    def hard_reset_player(self):
        self.lv = 1
        self.MAX_HP = 100
        self.MAX_MP = 100
        self.HP = 100
        self.MP = 100
        self.MP_regen_base = 10
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
        self.potion_description = ""
        self.inventory["main_hand"][2] = "graphics/items/empty_slot.png"
        self.inventory["off_hand"][2] = "graphics/items/empty_slot.png"
        self.inventory["armor"][2] = "graphics/items/skorzany_pancerz.png"
        self.inventory["accessory"][2] = "graphics/items/empty_slot.png"
        self.inventory["accessory2"][2] = "graphics/items/empty_slot.png"
        self.inventory["accessory3"][2] = "graphics/items/empty_slot.png"
        self.inventory["potion"][2] = "graphics/items/empty_slot.png"
        self.blok = False

    def soft_reset_player(self):
        #self.lv = 1
        self.MAX_HP = 100
        self.MAX_MP = 100
        self.HP = 100
        self.MP = 100
        self.MP_regen_base = 10
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
        self.EXP_To_Lv = 100*self.lv
        #self.stat_points = 0
        #self.skill_points = 0
        self.skill = {}
        self.status = list()
        #self.head = "glowa1"
        self.potions = 0
        self.potion_effect = ""
        self.current_potions = 0
        self.potion_description = ""
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
        self.EXP_boost = round(0.1*self.INT,2) + self.EXP_boost_bonus
        
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
current_player = main_player
companion1 = Character()
companion2 = Character()
       
team = list()
team.append(main_player)
gold = 0