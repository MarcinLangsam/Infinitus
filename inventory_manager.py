# -*- coding: utf-8 -*-
import player, UI_manager as UI, text_pop as tp, tooltip as tt, codecs
from itertools import islice
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.behaviors import DragBehavior
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

global screen
screen = ""

def check_whitch_screen(s):
    global screen
    screen = s

gold_on_screen = Label(pos_hint={'x':-0.34,'y':-0.378}, font_size=33,halign="left", valign="middle", text="{0:g}".format(player.gold), outline_width = 1)
def update_gold():
    gold_on_screen.text = "{0:g}".format(player.gold)

class ItemSlot(DragBehavior, Widget):
    sprite = StringProperty("")
    
    def __init__(self, **kwargs):
        Window.bind(mouse_pos=self.on_mouse_pos)
        super().__init__(**kwargs)
        self.check_collision = False
        self.check_touch = False
        self.select = 0
        self.drop = 0
        self.temp = ""
        self.t = 0
        self.p = 0
        self.pick_up_sound = SoundLoader.load("graphics/sounds/pick_up.wav")
        self.put_down_sound = SoundLoader.load("graphics/sounds/put_down.wav")
        self.error_sound = SoundLoader.load("graphics/sounds/error.wav")
        self.shop_sound = SoundLoader.load("graphics/sounds/shop.wav")

    def check_for_empty_slot(self):
        if player.current_player.inventory["main_hand"][2] == "graphics/items/empty_slot.png":
            self.parent.empty_main_hand.color = [1,1,1,1]
        else:
            self.parent.empty_main_hand.color = [0,0,0,0]
        if player.current_player.inventory["off_hand"][2] == "graphics/items/empty_slot.png":
            self.parent.empty_off_hand.color = [1,1,1,1]
        else:
            self.parent.empty_off_hand.color = [0,0,0,0]
        if player.current_player.inventory["armor"][2] == "graphics/items/empty_slot.png":
            self.parent.empty_armor.color = [1,1,1,1]
        else:
            self.parent.empty_armor.color = [0,0,0,0]
        if player.current_player.inventory["accessory"][2] == "graphics/items/empty_slot.png":
            self.parent.empty_accessory.color = [1,1,1,1]
        else:
            self.parent.empty_accessory.color = [0,0,0,0]
        if player.current_player.inventory["accessory2"][2] == "graphics/items/empty_slot.png":
            self.parent.empty_accessory2.color = [1,1,1,1]
        else:
            self.parent.empty_accessory2.color = [0,0,0,0]
        if player.current_player.inventory["accessory3"][2] == "graphics/items/empty_slot.png":
            self.parent.empty_accessory3.color = [1,1,1,1]
        else:
            self.parent.empty_accessory3.color = [0,0,0,0]

        if player.current_player.inventory["potion"][2] == "graphics/items/empty_slot.png":
            self.parent.empty_potion.color = [1,1,1,1]
        else:
            self.parent.empty_potion.color = [0,0,0,0]

    def switch_items_in_invetory(self):
        self.temp = inventory[self.select].sprite
        inventory[self.select].sprite = inventory[self.drop].sprite
        player.current_player.inventory[self.select][2] = inventory[self.drop].sprite
        inventory[self.drop].sprite = self.temp
        player.current_player.inventory[self.drop][2] = self.temp
        inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])

        if screen == "team":
            self.check_for_empty_slot()

    def on_touch_down(self, touch):
        if self.pos[0] <= touch.pos[0] <= self.pos[0]+75 and self.pos[1] <= touch.pos[1] <= self.pos[1]+75: 
            for x in player.current_player.inventory.keys():
                    if self.pos[0] == player.current_player.inventory[x][0] and self.pos[1] == player.current_player.inventory[x][1]:
                        self.select = x
                        self.check_touch = True
                        self.pick_up_sound.play()
        else:
            pass
        return super(ItemSlot, self).on_touch_down(touch)
    
    def on_touch_up(self, touch):
            for x in player.current_player.inventory.keys():
                if player.current_player.inventory[x][0] <= touch.pos[0] <= player.current_player.inventory[x][0]+75 and player.current_player.inventory[x][1] <= touch.pos[1] <= player.current_player.inventory[x][1]+75:
                    self.drop = x
                    self.check_collision = True
                else:
                    pass
            #kontrola będów i oszustwa
            if self.check_collision is False and self.check_touch is True: #powrót slotu w przypadku nie wykrycia "dokowania"
                if 440 <= touch.pos[0] <= 440+90 and 60 <= touch.pos[1] <= 60+90 and screen == "team": ### deleting item
                    player.current_player.inventory[self.select][2] = "graphics/items/empty_slot.png"
                    inventory[self.select].sprite = "graphics/items/empty_slot.png"
                    self.check_for_empty_slot()
                    inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                else:
                    inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])        
            if player.current_player.inventory[self.select][2] == "graphics/items/empty_slot.png": #zapobiega oszustwa z wykożystaniem pustego pola przy wyposażaniu
                inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
            if self.drop in range(48,95) and player.current_player.inventory[self.drop][2] != "graphics/items/empty_slot.png": #zapobiega oszustwa z wykożystaniem pustego pola przy kupowaniu
                inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
            if self.drop in range(48,95) and screen != "shop": #naprawia bug z przenoszeniem do sklepu z poziomu drużyny
                inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
            ##########################

            elif self.check_collision is True and self.check_touch is True:
                if self.select in range (0,48) or self.select in ["main_hand","off_hand","armor","accessory","accessory2","accessory3","potion"]:
                    if self.drop in range(48,95) and player.current_player.inventory[self.drop][2] == "graphics/items/empty_slot.png" and screen == "shop": #sprzedawanie przedmiotu
                        player.gold += (items.item_list[player.current_player.inventory[self.select][2]][4]/10)
                        update_gold()
                        tp.text_pop.text = "Sprzedano przedmiot"
                        self.shop_sound.play()
                        self.switch_items_in_invetory()
                    
                    elif self.drop in ["main_hand","off_hand","armor","accessory","accessory2","accessory3","potion"]: #zakładnie przedmitów
                        if self.drop == "off_hand" and items.item_list[player.current_player.inventory["main_hand"][2]][0] in ["two_hand","two_hand_sword","two_hand_spear"]:
                            inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                            tp.text_pop.text = "Używasz broni dwuręcznej!"
                            self.error_sound.play()
                        elif self.drop == "main_hand" and items.item_list[player.current_player.inventory[self.select][2]][0] in ["two_hand","two_hand_sword","two_hand_spear"] and player.current_player.inventory["off_hand"][2] != "graphics/items/empty_slot.png": 
                            inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                            tp.text_pop.text = "Potrzebujesz dwóch wolnych rąk aby używać tej broni!"
                            self.error_sound.play()
                        elif items.item_list[player.current_player.inventory[self.select][2]][0] in ["one_hand","two_hand","two_hand_sword","two_hand_spear"] and player.current_player.inventory[self.drop][3] == "main_hand":
                            items.unequip()
                            self.switch_items_in_invetory()
                            items.equip()
                            self.parent.refresh_items()
                            self.put_down_sound.play()
                        elif items.item_list[player.current_player.inventory[self.select][2]][0] == player.current_player.inventory[self.drop][3] or player.current_player.inventory[self.drop][3] == "item":
                            items.unequip()
                            self.switch_items_in_invetory()
                            items.equip()
                            self.parent.refresh_items()
                            self.put_down_sound.play()
                        else:
                            inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                            tp.text_pop.text = "Nie możesz założyć tutaj tego przedmiotu"
                            self.error_sound.play()
                    elif self.drop in range(0,48):
                        if self.select in ["main_hand","off_hand","armor","accessory","accessory2","accessory3","potion"]:
                            items.unequip()
                            self.switch_items_in_invetory()
                            items.equip()
                            self.parent.refresh_items()
                            self.put_down_sound.play()
                        else:
                            self.switch_items_in_invetory()
                            self.put_down_sound.play()
                elif self.select in range(48,95):
                    if self.drop in range(0,48):
                        if screen == "shop": #kupowanie przedmitów
                            if player.gold >= items.item_list[player.current_player.inventory[self.select][2]][4] and screen == "shop":
                                player.gold -= items.item_list[player.current_player.inventory[self.select][2]][4]
                                update_gold()
                                self.switch_items_in_invetory()
                                tp.text_pop.text = "Kupiono przedmiot"
                                self.shop_sound.play()
                            else:
                                tp.text_pop.text = "Nie masz wsytarczająco złota"
                                self.error_sound.play()
                                inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                        elif screen != "shop":
                            self.switch_items_in_invetory()
                            self.put_down_sound.play()
                    elif self.drop in range(48,95): #uniemożliwia przesuwanie przedmitów w sklepie
                        inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                 

                self.check_collision = False
                self.check_touch = False
                self.select = 0
                self.drop = 0
                self.temp = ""
                Clock.schedule_once(tp.clear_pop_up,2)
            return super(ItemSlot, self).on_touch_up(touch)
    
    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        Clock.unschedule(self.display_tooltip)
        self.close_tooltip()
        if self.collide_point(*self.to_widget(*pos)) and self.check_touch == False:
            for x in player.current_player.inventory.keys():
                    if self.pos[0] == player.current_player.inventory[x][0] and self.pos[1] == player.current_player.inventory[x][1]:
                            if player.current_player.inventory[x][2] == "graphics/items/empty_slot.png":
                                self.t = ""
                            else:
                                if x in range(0,40) or x in ["main_hand","off_hand","armor","accessory","accessory2","accessory3","potion"]:
                                    self.t = items.item_list[player.current_player.inventory[x][2]][3]+"  \nWartość sprzedarzy: "+ "{0:g}".format((items.item_list[player.current_player.inventory[x][2]][4]/10))
                                else:
                                    self.t = items.item_list[player.current_player.inventory[x][2]][3]+"  \nWartość kupna: "+ "{0:g}".format(items.item_list[player.current_player.inventory[x][2]][4])
                                self.p = (player.current_player.inventory[x][0]+40,player.current_player.inventory[x][1]+40)
                                Clock.schedule_once(self.display_tooltip, 0.5)

    def close_tooltip(self, *args):
        tt.clear_tooltip(self.parent.tooltip)
    def display_tooltip(self, *args):
        tt.set_tooltip(self.parent.tooltip,self.t, self.p)

class Items(Widget):
    def __init__(self):
        self.item_list={}

    def equip(self):
        exec(self.item_list[player.current_player.inventory["main_hand"][2]][1])
        exec(self.item_list[player.current_player.inventory["off_hand"][2]][1])
        exec(self.item_list[player.current_player.inventory["armor"][2]][1])
        exec(self.item_list[player.current_player.inventory["accessory"][2]][1])
        exec(self.item_list[player.current_player.inventory["accessory2"][2]][1])
        exec(self.item_list[player.current_player.inventory["accessory3"][2]][1])
        exec(self.item_list[player.current_player.inventory["potion"][2]][1])
        UI.ui.stats_refresh(player.current_player)

    def unequip(self):  
        exec(self.item_list[player.current_player.inventory["main_hand"][2]][2])
        exec(self.item_list[player.current_player.inventory["off_hand"][2]][2])
        exec(self.item_list[player.current_player.inventory["armor"][2]][2])
        exec(self.item_list[player.current_player.inventory["accessory"][2]][2])
        exec(self.item_list[player.current_player.inventory["accessory2"][2]][2])
        exec(self.item_list[player.current_player.inventory["accessory3"][2]][2])
        exec(self.item_list[player.current_player.inventory["potion"][2]][2])
        UI.ui.stats_refresh(player.current_player)

    def load_items(self):
        data =["","","","","",0]
        count = 0
        with codecs.open("items_list.txt",'r','utf-8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if line[0] == "_":
                    pass 
                else:
                    data[count] = line.strip().replace(r'\n','\n')
                    count+=1             
                    if count == 6: # <--- amout of separated data for one item/skill/status, change appropriately
                        self.item_list[data[0]] = [data[1],data[2],data[3],data[4],int(data[5])]
                        count=0
        f.close()
        

inventory = {}
items = Items()
items.load_items()