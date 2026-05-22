import player, inventory_manager as im, UI_manager as UI, abilities_manager as am, text_pop as tp, tooltip as tt
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.metrics import dp
from components.stats_component import stats_component
from components.inventory_component import gold_widget, Trash
from components.bottom_menu import BottomMenu
from kivy.uix.label import Label


class EXPBar(ProgressBar):
    pass
class Switch_Character_Button(Button):
    pass
class Team(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.accept_sound = SoundLoader.load("graphics/sounds/accept.wav")
        self.main_player_sprite = player.Character_Sprite(player.main_player, im.items.item_list[player.main_player.inventory["main_hand"][2]][0], player.main_player.head, pos_hint={"center_x": 0.5, "center_y": 0.65})
        self.companion1_sprite = player.Character_Sprite(player.companion1, im.items.item_list[player.companion1.inventory["main_hand"][2]][0], player.companion1.head, pos_hint={"center_x": 0.5, "center_y": 0.65})
        self.companion2_sprite = player.Character_Sprite(player.companion2, im.items.item_list[player.companion2.inventory["main_hand"][2]][0], player.companion2.head, pos_hint={"center_x": 0.5, "center_y": 0.65})
        self.current_sprite = self.main_player_sprite

        self.main_player_button = Button(pos_hint={"center_x": 0.1, "y": 0.8}, size_hint=(0.05,0.10), background_normal="graphics/sprites/"+player.main_player.head+"_portrait.png", on_press = lambda y:self.change_character_menu(player.main_player))
        self.companion1_button = Button(pos_hint={"center_x": 0.17, "y": 0.8}, size_hint=(0.05,0.10), background_normal="graphics/sprites/"+player.companion1.head+"_portrait.png", on_press = lambda y:self.change_character_menu(player.companion1))
        self.companion2_button = Button(pos_hint={"center_x": 0.24, "y": 0.8}, size_hint=(0.05,0.10), background_normal="graphics/sprites/"+player.companion2.head+"_portrait.png", on_press = lambda y:self.change_character_menu(player.companion2))
        self.current_button = self.main_player_button
        self.exp_bar = EXPBar()
        self.tooltip = tt.Tooltip()

        self.empty_main_hand = Image(source="graphics/items/empty_slot_main_hand.png", size_hint=(0.031,0.055), pos_hint={"x": player.current_player.inventory["main_hand"][0], "y": player.current_player.inventory["main_hand"][1]})
        self.empty_off_hand = Image(source="graphics/items/empty_slot_off_hand.png", size_hint=(0.031,0.055), pos_hint={"x": player.current_player.inventory["off_hand"][0], "y": player.current_player.inventory["off_hand"][1]})
        self.empty_armor = Image(source="graphics/items/empty_slot_armor.png", size_hint=(0.031,0.055), pos_hint={"x": player.current_player.inventory["armor"][0], "y": player.current_player.inventory["armor"][1]})
        self.empty_accessory = Image(source="graphics/items/empty_slot_accessory.png", size_hint=(0.031,0.055), pos_hint={"x": player.current_player.inventory["accessory"][0], "y": player.current_player.inventory["accessory"][1]})
        self.empty_accessory2 = Image(source="graphics/items/empty_slot_accessory.png", size_hint=(0.031,0.055), pos_hint={"x": player.current_player.inventory["accessory2"][0], "y": player.current_player.inventory["accessory2"][1]})
        self.empty_accessory3 = Image(source="graphics/items/empty_slot_accessory.png", size_hint=(0.031,0.055), pos_hint={"x": player.current_player.inventory["accessory3"][0], "y": player.current_player.inventory["accessory3"][1]})
        self.empty_potion = Image(source="graphics/items/empty_slot_potion.png", size_hint=(0.031,0.055), pos_hint={"x": player.current_player.inventory["potion"][0], "y": player.current_player.inventory["potion"][1]}, allow_stretch=True) 
        self.trash = Trash()
        

    def check_for_empty_slot(self):
        if player.current_player.inventory["main_hand"][2] == "graphics/items/empty_slot.png":
            self.empty_main_hand.color = [1,1,1,1]
        else:
            self.empty_main_hand.color = [0,0,0,0]
        if player.current_player.inventory["off_hand"][2] == "graphics/items/empty_slot.png":
            self.empty_off_hand.color = [1,1,1,1]
        else:
            self.empty_off_hand.color = [0,0,0,0]
        if player.current_player.inventory["armor"][2] == "graphics/items/empty_slot.png":
            self.empty_armor.color = [1,1,1,1]
        else:
            self.empty_armor.color = [0,0,0,0]
        
        if player.current_player.inventory["accessory"][2] == "graphics/items/empty_slot.png":
            self.empty_accessory.color = [1,1,1,1]
        else:
            self.empty_accessory.color = [0,0,0,0]
        if player.current_player.inventory["accessory2"][2] == "graphics/items/empty_slot.png":
            self.empty_accessory2.color = [1,1,1,1]
        else:
            self.empty_accessory2.color = [0,0,0,0]
        if player.current_player.inventory["accessory3"][2] == "graphics/items/empty_slot.png":
            self.empty_accessory3.color = [1,1,1,1]
        else:
            self.empty_accessory3.color = [0,0,0,0]
        
        if player.current_player.inventory["potion"][2] == "graphics/items/empty_slot.png":
            self.empty_potion.color = [1,1,1,1]
        else:
            self.empty_potion.color = [0,0,0,0]
        
    def change_window(self,window_name):
        self.accept_sound.play()
        self.change_character_menu(player.main_player)
        self.clear_widgets()
        self.manager.current = window_name

    def setup_window(self):
        self.check_for_empty_slot()
        self.add_widget(self.tooltip)
        self.main_player_sprite.head_source = player.main_player.head
        self.main_player_sprite.set_head()
        self.companion1_sprite.set_head()
        self.companion1_sprite.head_source = player.companion1.head
        self.companion2_sprite.set_head()
        self.companion2_sprite.head_source = player.companion2.head
        self.main_player_button.background_normal ="graphics/sprites/"+player.main_player.head+"_portrait.png"
        self.companion1_button.background_normal ="graphics/sprites/"+player.companion1.head+"_portrait.png"
        self.companion2_button.background_normal ="graphics/sprites/"+player.companion2.head+"_portrait.png"

        self.add_widget(Image(source="graphics/team_background.png", size_hint=(1,1), allow_stretch=True, fit_mode="fill"))   
        self.add_widget(Label(text="Trzymaj kursor na przedmiocie aby zobaczyć jego opis", pos_hint={"center_x": 0.5,"center_y": 0.05}, font_size=18))     
        #self.add_widget(BottomMenu(self.manager, pos_hint={"center_x": 0.5, "y": 0}))
        
        im.inventory["main_hand"] = im.ItemSlot(pos_hint={"x": player.current_player.inventory["main_hand"][0], "y": player.current_player.inventory["main_hand"][1]}, sprite=(player.current_player.inventory["main_hand"][2]))
        im.inventory["off_hand"] = im.ItemSlot(pos_hint={"x": player.current_player.inventory["off_hand"][0], "y": player.current_player.inventory["off_hand"][1]}, sprite=(player.current_player.inventory["off_hand"][2]))
        im.inventory["armor"] = im.ItemSlot(pos_hint={"x": player.current_player.inventory["armor"][0], "y": player.current_player.inventory["armor"][1]}, sprite=(player.current_player.inventory["armor"][2]))
        im.inventory["accessory"] = im.ItemSlot(pos_hint={"x": player.current_player.inventory["accessory"][0], "y": player.current_player.inventory["accessory"][1]}, sprite=(player.current_player.inventory["accessory"][2]))
        im.inventory["accessory2"] = im.ItemSlot(pos_hint={"x": player.current_player.inventory["accessory2"][0], "y": player.current_player.inventory["accessory2"][1]}, sprite=(player.current_player.inventory["accessory2"][2]))
        im.inventory["accessory3"] = im.ItemSlot(pos_hint={"x": player.current_player.inventory["accessory3"][0], "y": player.current_player.inventory["accessory3"][1]}, sprite=(player.current_player.inventory["accessory3"][2]))
        im.inventory["potion"] = im.ItemSlot(pos_hint={"x": player.current_player.inventory["potion"][0], "y": player.current_player.inventory["potion"][1]}, sprite=(player.current_player.inventory["potion"][2]))
        self.add_widget(im.inventory["main_hand"])
        self.add_widget(im.inventory["off_hand"])
        self.add_widget(im.inventory["armor"])
        self.add_widget(im.inventory["accessory"])
        self.add_widget(im.inventory["accessory2"])
        self.add_widget(im.inventory["accessory3"])
        self.add_widget(im.inventory["potion"])

        self.add_widget(Button(pos_hint={"center_x": 0.95, "center_y": 0.95}, size=(50,50), size_hint=(None,None), background_normal="graphics/close_button.png", on_press = lambda y:self.change_window("menu")))
        
        if len(player.team) >= 1:
            self.main_player_button.background_color = (0.4,0.4,0.4,1)
            self.add_widget(self.main_player_button)
        if len(player.team) >= 2:
            self.companion1_button.background_color = (0.4,0.4,0.4,1)
            self.add_widget(self.companion1_button)
        if len(player.team) >= 3:
            self.companion2_button.background_color = (0.4,0.4,0.4,1)
            self.add_widget(self.companion2_button)
        
        self.current_button.background_color = (1,1,1,1)

        self.exp_bar.value = player.current_player.EXP
        self.exp_bar.max = player.current_player.EXP_To_Lv
        self.exp_bar.pos_hint = {'center_x':0.5,'center_y':0.9}
        self.exp_bar.size_hint_x = 0.20
        self.add_widget(self.exp_bar)
        stats_component.visible()
        self.add_widget(stats_component)
        self.add_widget(gold_widget)
        self.add_widget(self.trash)

        UI.ui.stats_refresh(player.current_player)
        im.check_whitch_screen(self.manager.current)
        
        self.add_widget(self.current_sprite,10)
        self.add_widget(tp.text_pop_inventory)
        self.add_widget(tp.text_pop_stat_up)
        
        self.add_widget(self.empty_main_hand)
        self.add_widget(self.empty_off_hand)
        self.add_widget(self.empty_armor)
        self.add_widget(self.empty_accessory)
        self.add_widget(self.empty_accessory2) 
        self.add_widget(self.empty_accessory3)
        self.add_widget(self.empty_potion)
        
        
        for x in range(0,48):
            im.inventory[x] = im.ItemSlot(pos_hint={"x": player.current_player.inventory[x][0], "y": player.current_player.inventory[x][1]}, sprite=(player.current_player.inventory[x][2]))
            self.add_widget(im.inventory[x])
        
        self.refresh_items()
            
    def change_character_menu(self,character):
        self.clear_widgets()
        UI.ui.stats_refresh(character)
        player.current_player = character
        for x in range(0,48):
            character.inventory[x][2] = im.inventory[x].sprite
        
        if character == player.main_player:
            self.current_sprite = self.main_player_sprite
            self.current_button = self.main_player_button
        if character == player.companion1:
            self.current_sprite = self.companion1_sprite
            self.current_button = self.companion1_button
        if character == player.companion2:
            self.current_sprite = self.companion2_sprite
            self.current_button = self.companion2_button
        
        self.setup_window()
    
    def refresh_items(self):
        self.remove_widget(self.current_sprite)
        self.current_sprite.set_sprite(im.items.item_list[player.current_player.inventory["main_hand"][2]][0])
        self.current_sprite.set_sprite_weapon()
        self.current_sprite.set_weapon()
        self.add_widget(self.current_sprite,10)
        self.remove_widget(self.tooltip)
        self.add_widget(self.tooltip)
 