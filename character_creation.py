import player, tooltip as tt, inventory_manager as im, UI_manager as UI, abilities_manager as am
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image

class Character_Creation(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.sprite = player.Character_Sprite(player.main_player, im.items.item_list[player.current_player.inventory["main_hand"][2]][0], pos=(520,432-65))
        self.tooltip = tt.Tooltip()
        self.weapon_description = ""
        self.skill_description = ""
        self.weapon_label = Label(pos=(600,220), text=self.weapon_description , size_hint=(None,None), font_size=25)
        self.skill_label = Label(pos=(850,220), text=self.skill_description , size_hint=(None,None), font_size=25)
        self.weapon_image = Image(pos=(600,120), size=(100,100), source="", allow_stretch=True ,size_hint=(None,None))
        self.skill_image = Image(pos=(800,120), size=(100,100), source="", allow_stretch=True, size_hint=(None,None))

    def set_class(self,player,class_type):
        player.reset_player()
        
        if class_type == "warrior":
            player.STR = 15
            self.weapon_description = "Miecz z brązu\nObrażenia +5"
            self.skill_description = "Zamach\nZadaje: 10+STR*3\nKoszt MP: 20"
            self.weapon_image.source = ""
            self.skill_image.source = "graphics/skills/zamach.png"
            player.inventory["main_hand"][2] = "graphics/animations/mlot_bojowy.png"
        elif class_type == "mage":
            player.INT = 15
            self.weapon_description = "Pika\nObrażenia +1"
            self.skill_description = "Kula Ognia\nZadaje: 15+INT*2\nKoszt MP: 10"
            self.weapon_image.source = ""
            self.skill_image.source = "graphics/skills/kula_ognia.png"
            player.inventory["main_hand"][2] = "graphics/animations/pika.png"
        elif class_type == "rouge":
            player.DEX = 15
            self.weapon_description = "Miedziany sztylet\nObrażenia +3"
            self.skill_description = "Ciche cięcie\nZadaje: 5+DEX*4\nKoszt MP: 15"
            self.weapon_image.source = ""
            self.skill_image.source = "graphics/skills/ciche_cięcie.png"
            player.inventory["main_hand"][2] = "graphics/animations/miedziany_sztylet.png"
        self.weapon_label.text = self.weapon_description
        self.skill_label.text = self.skill_description
        UI.ui.stats_refresh(player)
        self.refresh_items()
    
    def change_screen(self,screen):
        self.clear_widgets()
        self.manager.current = screen
    def setup_window(self):
        self.add_widget(Image(source="graphics/plain_background.png", size=(1540,950), pos=(0,0), size_hint=(None,None), allow_stretch=True))
        self.add_widget(Image(source="graphics/stat_background.png", size=(300,2000), pos=(1130,-550), size_hint=(None,None), allow_stretch=True))
        self.add_widget(Image(source="graphics/animations/glowa1_sprite.png", size=(870,820), pos=(-170,220), size_hint=(None,None), allow_stretch=True))
        self.add_widget(self.sprite)

        self.add_widget(Button(pos=(50,720), size=(180,90), font_size= 25, text="Wróc do menu!", size_hint=(None,None), background_normal="graphics/target_button.png", on_press = lambda y:self.change_screen("main_menu")))
        self.add_widget(Button(pos=(500,30), size=(500,70), font_size= 40, text="Rozpocznij Grę!", size_hint=(None,None), background_normal="graphics/target_button.png", on_press = lambda y:self.change_screen("menu")))
        
        self.add_widget(Label(pos=(200,610), text="Portret: ", font_size=30, size_hint=(None,None)))
        self.add_widget(Button(pos=(100,500), size=(100,130), size_hint=(None,None)))
        self.add_widget(Button(pos=(300,500), size=(100,130), size_hint=(None,None)))
        self.add_widget(Label(pos=(200,300), text="Klasa startowa: ", font_size=30, size_hint=(None,None)))
        self.add_widget(Button(pos=(50,200), size=(100,100), size_hint=(None,None), on_press = lambda y:self.set_class(player.main_player,"warrior")))
        self.add_widget(Button(pos=(200,200), size=(100,100), size_hint=(None,None), on_press = lambda y:self.set_class(player.main_player,"mage")))
        self.add_widget(Button(pos=(350,200), size=(100,100), size_hint=(None,None), on_press = lambda y:self.set_class(player.main_player,"rouge")))

        
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

