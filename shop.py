import inventory_manager as im, text_pop as tp, player
from fight import current_stage
import tooltip as tt
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader

class Shop(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.tooltip = tt.Tooltip()
        self.accept_sound = SoundLoader.load("graphics/sounds/accpet.wav")

    def change_screen(self):
        self.clear_on_shop_leave()
        self.accept_sound.play()
        self.clear_widgets()
        self.manager.current = "menu"
    def setup_window(self):
        self.add_widget(Image(source="graphics/plain_background.png", size=(1540,950), pos=(0,0), size_hint=(None,None), allow_stretch=True))
        self.add_widget(Image(source="graphics/menu_background.png", size=(550,90), pos=(5,60), size_hint=(None,None), allow_stretch=True)) #gold widget
        self.add_widget(Image(source="graphics/trash.png", size=(90,90), pos=(440,60), size_hint=(None,None), allow_stretch=True))
        self.add_widget(Image(source="graphics/shop_button.png", size=(60,60), pos=(130,80), size_hint=(None,None), allow_stretch=True))
        
        for x in range(0,96):
            im.inventory[x] = im.ItemSlot(pos=(player.current_player.inventory[x][0],player.current_player.inventory[x][1]), sprite=(player.current_player.inventory[x][2]))
            self.add_widget(im.inventory[x])

        self.add_widget(Button(pos=(1450,800), size=(50,50), size_hint=(None,None), background_normal="graphics/close_button.png", on_press = lambda y:self.change_screen()))
        self.add_widget(im.gold_on_screen)
        im.update_gold()
        im.check_whitch_screen(self.manager.current)
        self.add_widget(tp.text_pop)

        self.set_shop_content()
        self.add_widget(self.tooltip)

    def set_shop_content(self):
        for x in range(48,48+len(self.shop_content[current_stage])):
            im.inventory[x].sprite = str(self.shop_content[current_stage][x-48])
            player.current_player.inventory[x][2] = str(self.shop_content[current_stage][x-48])

    def clear_on_shop_leave(self):
        for x in range(48,95):
            im.inventory[x].sprite = "graphics/items/empty_slot.png"
            player.current_player.inventory[x][2] = "graphics/items/empty_slot.png"


    shop_content={
        1:["graphics/items/pierscien_many.png","graphics/items/pierscien_zdrowia.png","graphics/items/pierscien_sily.png","graphics/items/pierscien_zrecznosci.png","graphics/items/pierscien_inteligencji.png",
           "graphics/items/srebrny_pierscien.png","graphics/items/amulet_precyzji.png","graphics/items/amulet_predkosci.png","graphics/items/drewniana_tarcza.png","graphics/items/magicza_ksiega.png","graphics/items/podstepny_majcher.png",
           "graphics/items/mała_mikstura_zdrowia.png","graphics/items/mała_mikstura_many.png","graphics/items/kostur_maga.png","graphics/items/rytualny_sztylet.png","graphics/items/mlot_bojowy.png","graphics/items/pikowany_pancerz.png",
           ]
    }