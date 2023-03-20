import player, UI_manager as UI
from itertools import islice
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.behaviors import DragBehavior
from kivy.properties import StringProperty
from kivy.clock import Clock

global screen
screen = ""

def check_whitch_screen(s):
    global screen
    screen = s

gold_on_screen = Label(pos=(300,-300), text=(str(player.gold)))
def update_gold():
    gold_on_screen.text = str(player.gold)

class Tooltip(Label):
    pass
class ItemSlot(DragBehavior, Widget):
    tooltip = Tooltip()
    sprite = StringProperty("")
    
    def __init__(self, **kwargs):
        Window.bind(mouse_pos=self.on_mouse_pos)
        super().__init__(**kwargs)
        self.check_collision = False
        self.check_touch = False
        self.select = 0
        self.drop = 0
        self.temp = ""
        
    def on_touch_down(self, touch):
        if self.pos[0] <= touch.pos[0] <= self.pos[0]+75 and self.pos[1] <= touch.pos[1] <= self.pos[1]+75: 
            for x in player.current_player.inventory.keys():
                    if self.pos[0] == player.current_player.inventory[x][0] and self.pos[1] == player.current_player.inventory[x][1]:
                        self.select = x
                        self.check_touch = True
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
            if self.check_collision is False and self.check_touch is True:
                inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])        
            elif self.check_collision is True and self.check_touch is True:
                if self.select in range (0,40) or self.select in ["main_hand","off_hand","armor","accessory"]:
                    if player.current_player.inventory[self.select][2] == "empty_slot.png": #zapobiega oszustwa z wykożystaniem pustego pola przy wysosarzaniu
                        inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                    elif self.drop in range(39,80) and player.current_player.inventory[self.drop][2] == "empty_slot.png" and screen == "shop":
                        player.gold += (items.item_list[player.current_player.inventory[self.select][2]][4]/10)
                        update_gold()
                        self.temp = inventory[self.select].sprite
                        inventory[self.select].sprite = inventory[self.drop].sprite
                        player.current_player.inventory[self.select][2] = inventory[self.drop].sprite
                        inventory[self.drop].sprite = self.temp
                        player.current_player.inventory[self.drop][2] = self.temp
                        inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                    elif self.drop in range(39,80) and player.current_player.inventory[self.drop][2] != "empty_slot.png": #zapobiega oszustwa z wykożystaniem pustego pola przy kupowaniu
                        inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                    elif self.drop in range(39,80) and screen != "shop": #naprawia bug z przenoszeniem do sklepu z poziomu drużyny
                        inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                    elif self.drop in ["main_hand","off_hand","armor","accessory"]:
                        if items.item_list[player.current_player.inventory[self.select][2]][0] == player.current_player.inventory[self.drop][3] or player.current_player.inventory[self.drop][3] == "item":
                            items.unequip()
                            self.temp = inventory[self.select].sprite
                            inventory[self.select].sprite = inventory[self.drop].sprite
                            player.current_player.inventory[self.select][2] = inventory[self.drop].sprite
                            inventory[self.drop].sprite = self.temp
                            player.current_player.inventory[self.drop][2] = self.temp
                            inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                            items.equip()
                        else:
                            inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                    elif self.drop in range(0,40):
                        if self.select in ["main_hand","off_hand","armor","accessory"]:
                            items.unequip()
                        self.temp = inventory[self.select].sprite
                        inventory[self.select].sprite = inventory[self.drop].sprite
                        player.current_player.inventory[self.select][2] = inventory[self.drop].sprite
                        inventory[self.drop].sprite = self.temp
                        player.current_player.inventory[self.drop][2] = self.temp
                        inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])   
                elif self.select in range(39,80):
                    if player.current_player.inventory[self.select][2] == "epmty_slot.png":
                        inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                    elif self.drop in range(0,40) and player.current_player.inventory[self.drop][2] != "empty_slot.png": #zapobiega oszustwa z wykożystaniem pustego pola przy kupowaniu
                        inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                    elif self.drop in range(0,40):
                        if screen == "shop":
                            print("AAAA")
                            if player.gold >= items.item_list[player.current_player.inventory[self.select][2]][4] and screen == "shop":
                                player.gold -= items.item_list[player.current_player.inventory[self.select][2]][4]
                                update_gold()
                                self.temp = inventory[self.select].sprite
                                inventory[self.select].sprite = inventory[self.drop].sprite
                                player.current_player.inventory[self.select][2] = inventory[self.drop].sprite
                                inventory[self.drop].sprite = self.temp
                                player.current_player.inventory[self.drop][2] = self.temp
                                inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                            else:
                                print("Nie masz wystarczająco złota")
                                inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                        elif screen != "shop":
                            self.temp = inventory[self.select].sprite
                            inventory[self.select].sprite = inventory[self.drop].sprite
                            player.current_player.inventory[self.select][2] = inventory[self.drop].sprite
                            inventory[self.drop].sprite = self.temp
                            player.current_player.inventory[self.drop][2] = self.temp
                            inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                            
                        
                    elif self.drop in range(39,80):
                        inventory[self.select].pos=(player.current_player.inventory[self.select][0],player.current_player.inventory[self.select][1])
                 
                self.check_collision = False
                self.check_touch = False
                self.select = 0
                self.drop = 0
                self.temp = ""
            return super(ItemSlot, self).on_touch_up(touch)
    
    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        Clock.unschedule(self.display_tooltip)
        self.close_tooltip()
        if self.collide_point(*self.to_widget(*pos)) and self.check_touch==False:
            for x in player.current_player.inventory.keys():
                    if self.pos[0] == player.current_player.inventory[x][0] and self.pos[1] == player.current_player.inventory[x][1]:
                        if x in range(0,40):
                            if player.current_player.inventory[x][2] == "empty_slot.png":
                                self.tooltip.text = ""
                            else:
                                self.tooltip.text = items.item_list[player.current_player.inventory[x][2]][3]+"  Wartość sprzedarzy: "+ str((items.item_list[player.current_player.inventory[x][2]][4]/10))
                                self.tooltip.pos = (player.current_player.inventory[x][0]+40,player.current_player.inventory[x][1]+40)
                        elif x in range(39,80):
                            if player.current_player.inventory[x][2] == "empty_slot.png":
                                self.tooltip.text = ""
                            else:
                                self.tooltip.text = items.item_list[player.current_player.inventory[x][2]][3]+"  Wartość kupna: "+ str(items.item_list[player.current_player.inventory[x][2]][4])
                                self.tooltip.pos = (player.current_player.inventory[x][0]+40,player.current_player.inventory[x][1]+40)
            Clock.schedule_once(self.display_tooltip, 0.5)

    def close_tooltip(self, *args):
        self.remove_widget(self.tooltip)
    def display_tooltip(self, *args):
        self.add_widget(self.tooltip)

class Items():
    def __init__(self):
        self.item_list={
            "empty_slot.png" : ["none","","","",0],
            "sword.png" : ["main_hand","player.current_player.weapon += 10","player.current_player.weapon -= 10","Miecz\nObrażenia +10",10],
            "shield.png" : ["off_hand","player.current_player.defence += 10","player.current_player.defence -= 10","Tarcza\nPancerz +10",10],
            "armor.png" : ["armor","player.current_player.MAX_HP += 50","player.current_player.MAX_HP -= 50","Zbroja\nZdrowie +50",10],
            "ring.png" : ["accessory","player.current_player.INT += 5","player.current_player.INT -= 5","Pierśceiń\nInteligencja +5",10] 
        }

    def equip(self):
        exec(self.item_list[player.current_player.inventory["main_hand"][2]][1])
        exec(self.item_list[player.current_player.inventory["off_hand"][2]][1])
        exec(self.item_list[player.current_player.inventory["armor"][2]][1])
        exec(self.item_list[player.current_player.inventory["accessory"][2]][1])
        UI.ui.stats_refresh(player.current_player)

    def unequip(self):  
        exec(self.item_list[player.current_player.inventory["main_hand"][2]][2])
        exec(self.item_list[player.current_player.inventory["off_hand"][2]][2])
        exec(self.item_list[player.current_player.inventory["armor"][2]][2])
        exec(self.item_list[player.current_player.inventory["accessory"][2]][2])
        UI.ui.stats_refresh(player.current_player)

inventory = {}
items = Items()