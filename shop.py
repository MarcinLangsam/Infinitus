import inventory_manager as im, text_pop as tp, player, UI_manager as UI, fight, random
import tooltip as tt
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.metrics import sp
from components.inventory_component import gold_widget
from kivy.uix.label import Label

class Shop(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.tooltip = tt.Tooltip()
        self.accept_sound = SoundLoader.load("graphics/sounds/t.wav")
        self.shookeeper_welocome = SoundLoader.load("graphics/sounds/shopkeeper_start1.wav")

    def roll_shopkeeper_welcome(self):
        roll = random.randint(1,4)
        self.shookeeper_welocome = SoundLoader.load("graphics/sounds/shopkeeper_start"+str(roll)+".wav")

    def change_screen(self):
        self.clear_on_shop_leave()
        self.accept_sound.play()
        self.clear_widgets()
        self.manager.current = "menu"
    def setup_window(self):
        self.add_widget(Image(source="graphics/shop_background.png", size_hint=(1,1), allow_stretch=True, fit_mode="fill"))
        self.add_widget(Image(source="graphics/goblin_shopkeeper.png", size_hint=(0.43,0.43), allow_stretch=True, pos_hint={"center_x": 0.5, "center_y":0.5}))
        
        for x in range(0,96):
            im.inventory[x] = im.ItemSlot(pos_hint={"x": player.current_player.inventory[x][0], "y": player.current_player.inventory[x][1]}, sprite=(player.current_player.inventory[x][2]))
            
            self.add_widget(im.inventory[x])
        

        self.add_widget(Button(pos_hint={"center_x": 0.95, "center_y": 0.95}, size=(50,50), size_hint=(None,None), background_normal="graphics/close_button.png", background_down="graphics/close_button_press.png", on_release = lambda y:self.change_screen()))
        self.add_widget(gold_widget)
        UI.ui.gold_refresh()
        im.check_whitch_screen(self.manager.current)
        self.add_widget(tp.text_pop_shop)

        self.set_shop_content()
        self.add_widget(Label(text="EKWIPUNEK", font_size=(sp(50)), pos_hint={"center_x": 0.235, "center_y": 0.9}, outline_width = 1))
        self.add_widget(Label(text="SKLEP", font_size=(sp(50)), pos_hint={"center_x": 0.75, "center_y": 0.9}, outline_width = 1))
        self.add_widget(self.tooltip)
        self.shookeeper_welocome.stop()
        self.roll_shopkeeper_welcome()
        self.shookeeper_welocome.play()

    def set_shop_content(self):
        for x in range(48,48+len(self.shop_content[fight.current_stage])):
            im.inventory[x].sprite = str(self.shop_content[fight.current_stage][x-48])
            player.current_player.inventory[x][2] = str(self.shop_content[fight.current_stage][x-48])

    def clear_on_shop_leave(self):
        for x in range(48,95):
            im.inventory[x].sprite = "graphics/items/empty_slot.png"
            player.current_player.inventory[x][2] = "graphics/items/empty_slot.png"


    shop_content={
        1:["graphics/items/pierscien_many.png","graphics/items/pierscien_zdrowia.png","graphics/items/pierscien_sily.png","graphics/items/pierscien_zrecznosci.png","graphics/items/pierscien_inteligencji.png",
           "graphics/items/srebrny_pierscien.png","graphics/items/amulet_precyzji.png","graphics/items/amulet_predkosci.png","graphics/items/drewniana_tarcza.png","graphics/items/magicza_ksiega.png","graphics/items/podstepny_majcher.png",
           "graphics/items/mała_mikstura_zdrowia.png","graphics/items/mała_mikstura_many.png","graphics/items/kostur_maga.png","graphics/items/rytualny_sztylet.png","graphics/items/mlot_bojowy.png","graphics/items/miecz_poltorareczny.png",
           "graphics/items/pikowany_pancerz.png","graphics/items/szata_maga.png","graphics/items/przyszywanica.png","graphics/items/kolczuga.png",
        ],
        2:["graphics/items/wiekszy_pierscien_many.png","graphics/items/wiekszy_pierscien_zdrowia.png","graphics/items/wiekszy_pierscien_sily.png","graphics/items/wiekszy_pierscien_zrecznosci.png","graphics/items/wiekszy_pierscien_inteligencji.png",
           "graphics/items/amulet_precyzji.png","graphics/items/amulet_predkosci.png","graphics/items/zelazna_rekawica.png","graphics/items/zloty_pierscien.png","graphics/items/stalowa_tarcza.png",
           "graphics/items/srednia_mikstura_zdrowia.png","graphics/items/srednia_mikstura_many.png",
           "graphics/items/miecz_rycerski.png","graphics/items/zaklety_oskard.png","graphics/items/kostur_kaplanski.png","graphics/items/rapier.png",
           "graphics/items/pancerz_z_wzmocnionej_skory.png","graphics/items/brygantyna.png","graphics/items/ozdobna_toga.png",
        ],
        3:["graphics/items/wiekszy_pierscien_many.png","graphics/items/wiekszy_pierscien_zdrowia.png","graphics/items/wiekszy_pierscien_sily.png","graphics/items/wiekszy_pierscien_zrecznosci.png","graphics/items/wiekszy_pierscien_inteligencji.png",
                   "graphics/items/amulet_precyzji.png","graphics/items/amulet_predkosci.png","graphics/items/zelazna_rekawica.png","graphics/items/zloty_pierscien.png","graphics/items/stalowa_tarcza.png",
                   "graphics/items/srednia_mikstura_zdrowia.png","graphics/items/srednia_mikstura_many.png",
                   "graphics/items/miecz_rycerski.png","graphics/items/zaklety_oskard.png","graphics/items/kostur_kaplanski.png","graphics/items/rapier.png",
                   "graphics/items/pancerz_z_wzmocnionej_skory.png","graphics/items/brygantyna.png","graphics/items/ozdobna_toga.png",
        ]
    }