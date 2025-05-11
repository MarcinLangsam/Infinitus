import player, tooltip as tt, inventory_manager as im, UI_manager as UI
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput

class Add_New_Character(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.new_character = player.companion1
        self.sprite = player.Character_Sprite(self.new_character,"one_hand",self.new_character.head,pos_hint={"center_x": 0.5, "center_y": 0.65})
        self.tooltip = tt.Tooltip()
        self.weapon_description = ""
        self.skill_description = ""
        self.weapon_label = Label(pos_hint={"center_x": 0.58, "center_y": 0.33}, text=self.weapon_description , size_hint=(None,None), font_size=25)
        self.skill_label = Label(pos_hint={"center_x": 0.43, "center_y": 0.33}, text=self.skill_description , size_hint=(None,None), font_size=25)
        self.class_label = Label(pos_hint={"center_x": 0.2, "center_y": 0.2}, text=self.skill_description , size_hint=(None,None), font_size=30)
        self.weapon_image = Image(pos_hint={"center_x": 0.58, "center_y": 0.2}, size=(100,100), source="", allow_stretch=True ,size_hint=(None,None))
        self.skill_image = Image(pos_hint={"center_x": 0.42, "center_y": 0.2}, size=(100,100), source="", allow_stretch=True, size_hint=(None,None))
        self.warrior_class = Button(pos_hint={"center_x": 0.12, "center_y": 0.33}, size=(100,100), size_hint=(None,None), on_press = lambda y:self.set_class(player.companion1,"warrior"), background_normal="graphics/warrior_class_disabled.png")
        self.mage_class = Button(pos_hint={"center_x": 0.2, "center_y": 0.33}, size=(100,100), size_hint=(None,None), on_press = lambda y:self.set_class(player.companion1,"mage"), background_normal="graphics/mage_class_disabled.png")
        self.thief_class = Button(pos_hint={"center_x": 0.28, "center_y": 0.33}, size=(100,100), size_hint=(None,None), on_press = lambda y:self.set_class(player.companion1,"rouge"), background_normal="graphics/thief_class_disabled.png")
        self.portarit = (Image(source="graphics/sprites/glowa1_portrait.png", pos_hint={"center_x": 0.2, "center_y": 0.55}, size_hint=(0.1,0.17), allow_stretch=True))
        self.enter_name = TextInput(text="Podaj imię...", multiline=False, pos_hint={"center_x": 0.2, "center_y": 0.8}, size_hint=(0.2,0.06), font_size=19)
        self.current_portrait = 1
        
    def previous_portrait(self):
        if self.current_portrait == 1:
            pass
        else:
            self.current_portrait-=1

        self.new_character.head = "glowa"+str(self.current_portrait)
        self.sprite.head_source = self.new_character.head
        self.sprite.set_head()
        self.portarit.source = self.sprite.portrait

    def next_portrait(self):
        if self.current_portrait == 5:
            pass
        else:
            self.current_portrait+=1

        self.new_character.head = "glowa"+str(self.current_portrait)
        self.sprite.head_source = self.new_character.head
        self.sprite.set_head()
        self.portarit.source = self.sprite.portrait
        

    def set_class(self,p,class_type):
        p.reset_player()

        self.warrior_class.background_normal = "graphics/warrior_class_disabled.png"
        self.mage_class.background_normal = "graphics/mage_class_disabled.png"
        self.thief_class.background_normal = "graphics/thief_class_disabled.png"
        
        if class_type == "warrior":
            p.HP = 60
            p.MAX_HP = 60
            p.STR_base = 15
            p.MP_regen = 10
            self.weapon_description = "Miecz z Brązu\nObrażenia +3"
            self.skill_description = "Zamach\nZadaje:\nObrażenia+50%STR\nKoszt MP: 30"
            self.weapon_image.source = "graphics/items/miecz_z_brazu.png"
            self.skill_image.source = "graphics/skills/zamach.png"
            p.inventory["main_hand"][2] = "graphics/items/miecz_z_brazu.png"
            p.skill["zamach"] = ["self.final_damage = self.current_turn.damage+self.current_turn.STR*0.5",30,"graphics/skills/zamach.png","Zamach   |   AKTYWNA\nProsta ale skuteczna technika prowadząca rozpędzoną broń prosto we wroga.\n\nZadaje: [color=#fdff80]Obrażenia[/color] + [color=#de8833]50%STR[/color]\nKoszt MP: [color=#0000ff]30[/color]","active","melee","on_enemy","zamach_effect","graphics/sounds/hit3.wav"]
            self.warrior_class.background_normal = "graphics/warrior_class.png"
            self.class_label.text = "+Bonus do siły\n+Bonus do zdrowia\nRegeneracja many na ture: 10"
        elif class_type == "mage":
            p.HP = 40
            p.MAX_HP = 40
            p.INT_base = 15
            p.MP_regen = 20
            self.weapon_description = "Pika\nObrażenia +1\nMana +10"
            self.skill_description = "Kula Ognia\nZadaje: 10+75%INT\nNakłada: Płonięcie\nKoszt MP: 40"
            self.weapon_image.source = "graphics/items/pika.png"
            self.skill_image.source = "graphics/skills/kula_ognia.png"
            p.inventory["main_hand"][2] = "graphics/items/pika.png"
            p.skill["kula ognia"] = ["self.final_damage = 10+self.current_turn.INT*0.75\nself.action_status = 'płonięcie'",40,"graphics/skills/kula_ognia.png","Kula Ognia   |   AKTYWNA\nPrzemień pokłady swojej magicznej energi w żywy ogien palący twoich wrogów.\n\nZadaje: [color=#fdff80]10[/color] + [color=#00f7ff]75%INT[/color]\nNakłada: Płonięcie 3 tury - [color=#fdff80]5 obrażeń na turę[/color]\nKoszt MP: [color=#0000ff]40[/color]","active","ranged","on_enemy","kula_ognia_effect","graphics/sounds/kula_ognia.wav"]
            self.mage_class.background_normal = "graphics/mage_class.png"
            self.class_label.text = "+Bonus do inteligencji\n-Kara do zdrowia\nRegeneracja many na ture: 20"
        elif class_type == "rouge":
            p.HP = 50
            p.MAX_HP = 50
            p.DEX_base = 15
            p.MP_regen = 15
            self.weapon_description = "Miedziany sztylet\nObrażenia +2\nZręczność +1"
            self.skill_description = "Zatrute Ostrze\nDodaje DEX do obrażeń\nKoszt MP: 20"
            self.weapon_image.source = "graphics/items/miedziany_sztylet.png"
            self.skill_image.source = "graphics/skills/zatrute_ostrze.png"
            p.inventory["main_hand"][2] = "graphics/items/miedziany_sztylet.png"
            p.skill["zatrute ostrze"] = ["self.final_damage = 0\nself.action_status = 'zatrute ostrze'",20,"graphics/skills/zatrute_ostrze.png","Zatrute Ostrze   |   AKTYWNA\nPokryj swoją broń trucizną aby wykonywała większą szkodę.\n\nNakłada: Zatrute Ostrze 3 tury - [color=#fdff80]dodaje wartość zręczności od ataku[/color] [color=#e45eff]NA SIEBIE[/color]\nKoszt MP: [color=#0000ff]20[/color]","active","status","on_self","obrazenia_buff_effect","graphics/sounds/positive_effect_1.wav"]
            self.thief_class.background_normal = "graphics/thief_class.png"
            self.class_label.text = "+Bonus do zręczności\nRegeneracja many na ture: 15"

        p.inventory["armor"][2] = "graphics/items/skorzany_pancerz.png"
        p.head = "glowa"+str(self.current_portrait)
        p.name = self.enter_name.text

        self.weapon_label.text = self.weapon_description
        self.skill_label.text = self.skill_description
    
        while player.main_player.lv > p.lv:
            player.level_up(p)
            
        p.update_player_stats()
        self.refresh_items()
        im.items.equip()

    
    def change_screen(self,screen):
        self.clear_widgets()
        self.manager.current = screen
    def setup_window(self):
        if len(player.team)==1:
            player.team.append(player.companion1)
            player.current_player = player.companion1
            self.new_character = player.companion1
        elif len(player.team)==2:
            player.team.append(player.companion2)
            player.current_player = player.companion2
            self.new_character = player.companion2
        
        self.add_widget(Image(source="graphics/team_background.png", size_hint=(1,1), allow_stretch=True, fit_mode="fill"))
        self.add_widget(Image(source="graphics/stat_background.png", size=(480,2000), pos_hint={"center_x": 0.81, "center_y": 0.5}, size_hint=(None,None), allow_stretch=True))
        self.add_widget(self.sprite)
        self.add_widget(self.portarit)
        self.add_widget(self.enter_name)

        self.add_widget(Button(pos_hint={"center_x": 0.5, "center_y": 0.1}, size=(500,70), font_size= 40, text="Rozpocznij Grę!", size_hint=(None,None), background_normal="graphics/target_button.png", on_press = lambda y:self.change_screen("menu")))
        
        self.add_widget(Label(pos_hint={"center_x": 0.2, "center_y": 0.85}, text="Imię: ", font_size=35, size_hint=(None,None)))
        self.add_widget(Label(pos_hint={"center_x": 0.2, "center_y": 0.67}, text="Portret: ", font_size=35, size_hint=(None,None)))
        self.add_widget(Button(pos_hint={"center_x": 0.1, "center_y": 0.55}, size=(100,130), size_hint=(None,None), background_normal="graphics/previous_portrait_button.png", on_press = lambda y:self.previous_portrait()))
        self.add_widget(Button(pos_hint={"center_x": 0.3, "center_y": 0.55}, size=(100,130), size_hint=(None,None), background_normal="graphics/next_portrait_button.png", on_press = lambda y:self.next_portrait()))
        self.add_widget(Label(pos_hint={"center_x": 0.2, "center_y": 0.4}, text="Klasa startowa: ", font_size=35, size_hint=(None,None)))
        self.add_widget(self.warrior_class)
        self.add_widget(self.mage_class)
        self.add_widget(self.thief_class)
        
        self.add_widget(self.weapon_image)
        self.add_widget(self.skill_image)
        self.add_widget(self.weapon_label)
        self.add_widget(self.skill_label)
        self.add_widget(self.class_label)

        for x in list(UI.stats.keys())[0:-4]:
            UI.stats[x].bind(size=UI.stats[x].setter("text_size"))
            self.add_widget(UI.stats[x])
        UI.ui.stats_refresh(self.new_character)
        self.add_widget(Label(text="DODAJ NOWEGO CZŁONKA DRUŻYNY!", pos_hint={"center_x": 0.5, "center_y": 0.9}, font_size=40))
        self.add_widget(self.tooltip)
        self.set_class(self.new_character, "warrior")
        self.refresh_items()

    def refresh_items(self):
        self.remove_widget(self.sprite)
        self.sprite.set_sprite(im.items.item_list[self.new_character.inventory["main_hand"][2]][0])
        self.sprite.set_sprite_weapon()
        self.add_widget(self.sprite)
        self.remove_widget(self.tooltip)
        self.add_widget(self.tooltip)

