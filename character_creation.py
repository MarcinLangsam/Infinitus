import player, tooltip as tt, inventory_manager as im, UI_manager as UI, abilities_manager as am
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput

class Character_Creation(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.sprite = player.Character_Sprite(player.main_player,"one_hand",player.main_player.head,pos=(520,432-65))
        self.tooltip = tt.Tooltip()
        self.weapon_description = ""
        self.skill_description = ""
        self.weapon_label = Label(pos=(600,220), text=self.weapon_description , size_hint=(None,None), font_size=25)
        self.skill_label = Label(pos=(850,220), text=self.skill_description , size_hint=(None,None), font_size=25)
        self.weapon_image = Image(pos=(600,120), size=(100,100), source="", allow_stretch=True ,size_hint=(None,None))
        self.skill_image = Image(pos=(800,120), size=(100,100), source="", allow_stretch=True, size_hint=(None,None))
        self.warrior_class = Button(pos=(50,150), size=(100,100), size_hint=(None,None), on_press = lambda y:self.set_class(player.main_player,"warrior"), background_normal="graphics/warrior_class_disabled.png")
        self.mage_class = Button(pos=(200,150), size=(100,100), size_hint=(None,None), on_press = lambda y:self.set_class(player.main_player,"mage"), background_normal="graphics/mage_class_disabled.png")
        self.thief_class = Button(pos=(350,150), size=(100,100), size_hint=(None,None), on_press = lambda y:self.set_class(player.main_player,"rouge"), background_normal="graphics/thief_class_disabled.png")
        self.portarit = (Image(source="graphics/sprites/glowa1_portrait.png", pos=(170,390), size_hint=(0.1,0.17), allow_stretch=True))
        self.enter_name = TextInput(text="Podaj imię...", multiline=False, pos=(120,690), size_hint=(0.18,0.04))
        self.current_portrait = 1
        
    def previous_portrait(self):
        if self.current_portrait == 1:
            pass
        else:
            self.current_portrait-=1

        player.main_player.head = "glowa"+str(self.current_portrait)
        self.sprite.head_source = player.main_player.head
        self.sprite.set_head()
        self.portarit.source = self.sprite.portrait

    def next_portrait(self):
        if self.current_portrait == 5:
            pass
        else:
            self.current_portrait+=1

        player.main_player.head = "glowa"+str(self.current_portrait)
        self.sprite.head_source = player.main_player.head
        self.sprite.set_head()
        self.portarit.source = self.sprite.portrait
        

    def set_class(self,p,class_type):
        p.reset_player()

        self.warrior_class.background_normal = "graphics/warrior_class_disabled.png"
        self.mage_class.background_normal = "graphics/mage_class_disabled.png"
        self.thief_class.background_normal = "graphics/thief_class_disabled.png"
        
        if class_type == "warrior":
            p.STR = 15
            self.weapon_description = "Młot Bojowy\nObrażenia +10"
            self.skill_description = "Zamach\nZadaje: 10+STR*3\nKoszt MP: 20"
            self.weapon_image.source = "graphics/items/mlot_bojowy.png"
            self.skill_image.source = "graphics/skills/zamach.png"
            p.inventory["main_hand"][2] = "graphics/items/mlot_bojowy.png"
            self.warrior_class.background_normal = "graphics/warrior_class.png"
        elif class_type == "mage":
            p.INT = 15
            self.weapon_description = "Pika\nObrażenia +1"
            self.skill_description = "Kula Ognia\nZadaje: 15+INT*2\nKoszt MP: 10"
            self.weapon_image.source = "graphics/items/pika.png"
            self.skill_image.source = "graphics/skills/kula_ognia.png"
            p.inventory["main_hand"][2] = "graphics/items/pika.png"
            self.mage_class.background_normal = "graphics/mage_class.png"
        elif class_type == "rouge":
            p.DEX = 15
            self.weapon_description = "Miedziany sztylet\nObrażenia +3"
            self.skill_description = "Ciche cięcie\nZadaje: 5+DEX*4\nKoszt MP: 15"
            self.weapon_image.source = "graphics/items/miedziany_sztylet.png"
            self.skill_image.source = "graphics/skills/ciche_cięcie.png"
            p.inventory["main_hand"][2] = "graphics/items/miedziany_sztylet.png"
            self.thief_class.background_normal = "graphics/thief_class_disabled.png"

        p.inventory["armor"][2] = "graphics/items/skorzany_pancerz.png"
        p.head = "glowa"+str(self.current_portrait)
        p.name = self.enter_name.text

        self.weapon_label.text = self.weapon_description
        self.skill_label.text = self.skill_description
    
        self.refresh_items()
        im.items.equip()

    
    def change_screen(self,screen):
        self.clear_widgets()
        self.manager.current = screen
    def setup_window(self):
        self.add_widget(Image(source="graphics/team_background.png", size=(1540,950), pos=(0,0), size_hint=(None,None), allow_stretch=True))
        self.add_widget(Image(source="graphics/stat_background.png", size=(430,2000), pos=(1040,-590), size_hint=(None,None), allow_stretch=True))
        self.add_widget(self.sprite)
        self.add_widget(self.portarit)
        self.add_widget(self.enter_name)

        #self.add_widget(Button(pos=(50,720), size=(180,90), font_size= 25, text="Wróc do menu!", size_hint=(None,None), background_normal="graphics/target_button.png", on_press = lambda y:self.change_screen("main_menu")))
        self.add_widget(Button(pos=(500,30), size=(500,70), font_size= 40, text="Rozpocznij Grę!", size_hint=(None,None), background_normal="graphics/target_button.png", on_press = lambda y:self.change_screen("menu")))
        
        self.add_widget(Label(pos=(210,710), text="Imię: ", font_size=35, size_hint=(None,None)))
        self.add_widget(Label(pos=(210,520), text="Portret: ", font_size=35, size_hint=(None,None)))
        self.add_widget(Button(pos=(50,400), size=(100,130), size_hint=(None,None), background_normal="graphics/previous_portrait_button.png", on_press = lambda y:self.previous_portrait()))
        self.add_widget(Button(pos=(350,400), size=(100,130), size_hint=(None,None), background_normal="graphics/next_portrait_button.png", on_press = lambda y:self.next_portrait()))
        self.add_widget(Label(pos=(200,230), text="Klasa startowa: ", font_size=35, size_hint=(None,None)))
        self.add_widget(self.warrior_class)
        self.add_widget(self.mage_class)
        self.add_widget(self.thief_class)
        
        self.add_widget(self.weapon_image)
        self.add_widget(self.skill_image)
        self.add_widget(self.weapon_label)
        self.add_widget(self.skill_label)

        for x in list(UI.stats.keys())[0:-4]:
            UI.stats[x].bind(size=UI.stats[x].setter("text_size"))
            self.add_widget(UI.stats[x])
        UI.ui.stats_refresh(player.main_player)
        self.add_widget(Label(text="KIM JESTEŚ?", pos=(720,750), font_size=40))
        self.add_widget(self.tooltip)
        self.set_class(player.main_player, "warrior")
        self.refresh_items()

    def refresh_items(self):
        self.remove_widget(self.sprite)
        self.sprite.set_sprite(im.items.item_list[player.current_player.inventory["main_hand"][2]][0])
        #self.current_sprite.set_sprite()
        self.sprite.set_sprite_weapon()
        self.add_widget(self.sprite)
        self.remove_widget(self.tooltip)
        self.add_widget(self.tooltip)

