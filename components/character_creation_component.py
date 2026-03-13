import player, inventory_manager as im
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
        
class NameInputComponent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enter_name = TextInput(text="Podaj imię...", multiline=False, font_size=19)
        self.orientation = "vertical"
        self.spacing = 15

        self.add_widget(Label(text="Imię: ", font_size=35))
        self.add_widget(self.enter_name)
    
    def return_name(self):
        return self.enter_name.text

class PortraitComponent(BoxLayout):
    def __init__(self, sprite, current_character,  **kwargs):
        super(PortraitComponent, self).__init__(**kwargs)
        self.current_portrait = 1
        self.sprite = sprite
        self.current_character = current_character
        self.orientation = "vertical"
        self.padding = [45,0,45,0]

        self.container = (BoxLayout(orientation = "horizontal", spacing = 15))
        self.portarit = (Image(source="graphics/sprites/glowa1_portrait.png"))
        self.container.add_widget(Button(background_normal="graphics/previous_portrait_button.png", on_press = lambda y:self.previous_portrait()))
        self.container.add_widget(self.portarit)
        self.container.add_widget(Button(background_normal="graphics/next_portrait_button.png", on_press = lambda y:self.next_portrait()))
        
        self.add_widget(Label(text="Portret: ", font_size=35))
        self.add_widget(self.container)
        
    def previous_portrait(self):
        if self.current_portrait == 1:
            pass
        else:
            self.current_portrait-=1
        self.current_character.head = "glowa"+str(self.current_portrait)
        self.sprite.head_source = self.current_character.head
        self.sprite.set_head()
        self.portarit.source = self.sprite.portrait

    def next_portrait(self):
        if self.current_portrait == 5:
            pass
        else:
            self.current_portrait+=1

        self.current_character.head = "glowa"+str(self.current_portrait)
        self.sprite.head_source = self.current_character.head
        self.sprite.set_head()
        self.portarit.source = self.sprite.portrait

class ClassesComponent(BoxLayout):
    def __init__(self, current_character, **kwargs):
        super(ClassesComponent, self).__init__(**kwargs)
        self.current_character = current_character
        self.orientation = "vertical"
        self.current_class = "warrior"
        self.spacing = 5

        self.container = (BoxLayout(orientation = "horizontal", spacing = 15, padding=[45,0,45,0]))
        self.warrior_class = Button(on_press = lambda y:self.set_class(self.current_character,"warrior"), background_normal="graphics/warrior_class_disabled.png")
        self.mage_class = Button(on_press = lambda y:self.set_class(self.current_character,"mage"), background_normal="graphics/mage_class_disabled.png")
        self.thief_class = Button(on_press = lambda y:self.set_class(self.current_character,"rouge"), background_normal="graphics/thief_class_disabled.png")
        self.container.add_widget(self.warrior_class)
        self.container.add_widget(self.mage_class)
        self.container.add_widget(self.thief_class)

        self.class_label = Label(text="", font_size=27)

        self.weapon_label = Label(text="", font_size=27)
        self.weapon_image = Image(source="", size_hint = (0.9,0.9), allow_stretch = True)
        self.skill_label = Label(text="", font_size=27)
        self.skill_image = Image(source="", size_hint = (0.9,0.9), allow_stretch = True)


        self.icons_container = BoxLayout(spacing = 5)
        self.icons_container.add_widget(self.skill_image)
        self.icons_container.add_widget(self.weapon_image)
       

        self.labels_container = BoxLayout(spacing = 20)
        self.labels_container.add_widget(self.weapon_label)
        self.labels_container.add_widget(self.skill_label)


        self.add_widget(Label(text="Klasa startowa: ", font_size=35))
        self.add_widget(self.container)
        self.add_widget(self.class_label)

        self.add_widget(self.icons_container)
        self.add_widget(self.labels_container)
        #self.set_class(self.current_character, "warrior")
        

    def set_class(self,current_character,class_type):
        current_character.soft_reset_player()

        self.warrior_class.background_normal = "graphics/warrior_class_disabled.png"
        self.mage_class.background_normal = "graphics/mage_class_disabled.png"
        self.thief_class.background_normal = "graphics/thief_class_disabled.png"
        
        if class_type == "warrior":
            self.current_class = "warrior"
            current_character.HP = 60
            current_character.MAX_HP = 60
            current_character.STR_base = 15
            current_character.MP_regen = 10
            current_character.inventory["main_hand"][2] = "graphics/items/miecz_z_brazu.png"
            current_character.skill["zamach"] = ["self.final_damage = self.current_turn.damage+self.current_turn.STR*0.5",30,"graphics/skills/zamach.png","Zamach   |   AKTYWNA\nProsta ale skuteczna technika prowadząca rozpędzoną broń prosto we wroga.\n\nZadaje: [color=#fdff80]Obrażenia[/color] + [color=#de8833]50%STR[/color]\nKoszt MP: [color=#0000ff]30[/color]","active","melee","on_enemy","zamach_effect","graphics/sounds/hit3.wav"]
            self.warrior_class.background_normal = "graphics/warrior_class.png"
            self.class_label.text = "+Bonus do siły\n+Bonus do zdrowia\nRegeneracja many na ture: 10"
            self.weapon_label.text = "Miecz z Brązu\nObrażenia +3"
            self.weapon_image.source = "graphics/items/miecz_z_brazu.png"
            self.skill_label.text = "Zamach\nZadaje:\nObrażenia+50%STR\nKoszt MP: 30"
            self.skill_image.source = "graphics/skills/zamach.png"
        elif class_type == "mage":
            self.current_class = "mage"
            current_character.HP = 40
            current_character.MAX_HP = 40
            current_character.INT_base = 15
            current_character.MP_regen = 20
            current_character.inventory["main_hand"][2] = "graphics/items/pika.png"
            current_character.skill["kula ognia"] = ["self.final_damage = 10+self.current_turn.INT*0.75\nself.action_status = 'płonięcie'",40,"graphics/skills/kula_ognia.png","Kula Ognia   |   AKTYWNA\nPrzemień pokłady swojej magicznej energi w żywy ogien palący twoich wrogów.\n\nZadaje: [color=#fdff80]10[/color] + [color=#00f7ff]75%INT[/color]\nNakłada: Płonięcie 3 tury - [color=#fdff80]5 obrażeń na turę[/color]\nKoszt MP: [color=#0000ff]40[/color]","active","ranged","on_enemy","kula_ognia_effect","graphics/sounds/kula_ognia.wav"]
            self.mage_class.background_normal = "graphics/mage_class.png"
            self.class_label.text = "+Bonus do inteligencji\n-Kara do zdrowia\nRegeneracja many na ture: 20"
            self.weapon_label.text = "Pika\nObrażenia +1\nMana +10"
            self.weapon_image.source = "graphics/items/pika.png"
            self.skill_label.text = "Kula Ognia\nZadaje: 10+75%INT\nNakłada: Płonięcie\nKoszt MP: 40"
            self.skill_image.source = "graphics/skills/kula_ognia.png"
        elif class_type == "rouge":
            self.current_class = "rouge"
            current_character.HP = 50
            current_character.MAX_HP = 50
            current_character.DEX_base = 15
            current_character.MP_regen = 15
            current_character.inventory["main_hand"][2] = "graphics/items/miedziany_sztylet.png"
            current_character.skill["zatrute ostrze"] = ["self.final_damage = 0\nself.action_status = 'zatrute ostrze'",20,"graphics/skills/zatrute_ostrze.png","Zatrute Ostrze   |   AKTYWNA\nPokryj swoją broń trucizną aby wykonywała większą szkodę.\n\nNakłada: Zatrute Ostrze 3 tury - [color=#fdff80]dodaje wartość zręczności od ataku[/color] [color=#e45eff]NA SIEBIE[/color]\nKoszt MP: [color=#0000ff]20[/color]","active","status","on_self","obrazenia_buff_effect","graphics/sounds/positive_effect_1.wav"]
            self.thief_class.background_normal = "graphics/thief_class.png"
            self.class_label.text = "+Bonus do zręczności\nRegeneracja many na ture: 15"
            self.weapon_label.text = "Miedziany sztylet\nObrażenia +2\nZręczność +1"
            self.weapon_image.source = "graphics/items/miedziany_sztylet.png"
            self.skill_label.text = "Zatrute Ostrze\nDodaje DEX do obrażeń\nKoszt MP: 20"
            self.skill_image.source = "graphics/skills/zatrute_ostrze.png"
  
        current_character.update_player_stats()
        im.items.equip()

    def return_current_class(self):
        return self.current_class

class CreatorContainer(BoxLayout):
    def __init__(self, sprite, current_character, **kwargs):
        super(CreatorContainer, self).__init__(**kwargs)
        self.spacing = dp(15)
        self.sprite = sprite
        self.current_character = current_character
        self.orientation = "vertical"

        self.name_component = NameInputComponent(size_hint_y = 0.15)
        self.portrait_component = PortraitComponent(self.sprite, self.current_character, size_hint_y=0.4)
        self.classes_component = ClassesComponent(self.current_character)
        self.add_widget(self.name_component)
        self.add_widget(self.portrait_component)
        self.add_widget(self.classes_component)



