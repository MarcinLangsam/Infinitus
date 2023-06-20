import inventory_manager as im, text_pop as tp, player
import tooltip as tt
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image

class Shop(Screen):
    def change_screen(self):
        self.clear_widgets()
        self.manager.current = "menu"
    def setup_window(self):
        self.add_widget(Image(source="graphics/plain_background.png", size=(1540,950), pos=(0,0), size_hint=(None,None), allow_stretch=True))
        for x in range(0,80):
            im.inventory[x] = im.ItemSlot(pos=(player.current_player.inventory[x][0],player.current_player.inventory[x][1]), sprite=(player.current_player.inventory[x][2]))
            self.add_widget(im.inventory[x])

        self.add_widget(Button(pos=(1450,800), size=(50,50), size_hint=(None,None), background_normal="graphics/close_button.png", on_press = lambda y:self.change_screen()))
        self.add_widget(im.gold_on_screen)
        im.update_gold()
        im.check_whitch_screen(self.manager.current)
        self.add_widget(tp.text_pop)

        self.add_widget(Label(text="EKWPUNEK", pos=(-490,415), font_size=40))
        self.add_widget(Label(text="SKLEP", pos=(440,415), font_size=40))
        self.set_shop_content()
        self.add_widget(tt.tooltip)

    def set_shop_content(self):
        for x in range(40,40+len(self.shop_content[1])):
            im.inventory[x].sprite = str(self.shop_content[1][x-40])
            player.current_player.inventory[x][2] = str(self.shop_content[1][x-40])

    shop_content={
        1:["graphics/items/pierscien_many.png","graphics/items/pierscien_zdrowia.png","graphics/items/pierscien_sily.png","graphics/items/pierscien_zrecznosci.png","graphics/items/pierscien_inteligencji.png"]
    }