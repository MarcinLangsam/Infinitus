import player, inventory_manager as im, UI_manager as UI, abilities_manager as am, text_pop as tp, tooltip as tt
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader


class EXPBar(ProgressBar):
    pass
class Switch_Character_Button(Button):
    pass
class Team(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.accept_sound = SoundLoader.load("graphics/sounds/accpet.wav")
        self.main_player_sprite = player.Character_Sprite(player.main_player, im.items.item_list[player.main_player.inventory["main_hand"][2]][0], player.main_player.head, pos=(590,432-65))
        self.companion1_sprite = player.Character_Sprite(player.companion1, im.items.item_list[player.companion1.inventory["main_hand"][2]][0], player.companion1.head, pos=(590,432-65))
        self.companion2_sprite = player.Character_Sprite(player.companion2, im.items.item_list[player.companion2.inventory["main_hand"][2]][0], player.companion2.head, pos=(590,432-65))

        self.current_sprite = self.main_player_sprite
        self.main_player_button = Button(pos=(140,730), size_hint=(0.065,0.13), background_normal="graphics/sprites/"+player.main_player.head+"_portrait.png", on_press = lambda y:self.change_character_menu(player.main_player))
        self.companion1_button = Button(pos=(280,730), size_hint=(0.065,0.13), background_normal="graphics/sprites/"+player.companion1.head+"_portrait.png", on_press = lambda y:self.change_character_menu(player.companion1))
        self.companion2_button = Button(pos=(410,730), size_hint=(0.065,0.13), background_normal="graphics/sprites/"+player.companion2.head+"_portrait.png", on_press = lambda y:self.change_character_menu(player.companion2))
        self.current_button = self.main_player_button
        self.exp_bar = EXPBar()
        self.tooltip = tt.Tooltip()

        self.empty_main_hand = Image(source="graphics/items/empty_slot_main_hand.png", size=(65,65), pos=(568,542), size_hint=(None,None))
        self.empty_off_hand = Image(source="graphics/items/empty_slot_off_hand.png", size=(65,65), pos=(568,432), size_hint=(None,None))
        self.empty_armor = Image(source="graphics/items/empty_slot_armor.png", size=(65,65), pos=(568,322), size_hint=(None,None))
        self.empty_accessory = Image(source="graphics/items/empty_slot_accessory.png", size=(65,65), pos=(918,542), size_hint=(None,None))
        self.empty_accessory2 = Image(source="graphics/items/empty_slot_accessory.png", size=(65,65), pos=(918,432), size_hint=(None,None))
        self.empty_accessory3 = Image(source="graphics/items/empty_slot_accessory.png", size=(65,65), pos=(918,322), size_hint=(None,None))
        #self.empty_potion = Image(source="graphics/items/empty_slot_potion.png", size=(65,65), pos=(918,222), size_hint=(None,None))
        
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
        
        #if player.current_player.inventory["potion"][2] == "graphics/items/empty_slot.png":
        #    self.empty_potion.color = [1,1,1,1]
        #else:
        #    self.empty_potion.color = [0,0,0,0]
        
    def change_screen(self):
        self.accept_sound.play()
        self.change_character_menu(player.main_player)
        self.clear_widgets()
        self.manager.current = "menu"
    def change_window(self,window_name): #TYMCZASOWE OGARNĄĆ TO
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

        self.add_widget(Image(source="graphics/team_background.png", size=(1540,950), pos=(0,0), size_hint=(None,None), allow_stretch=True))
        self.add_widget(Image(source="graphics/stat_background.png", size=(430,2000), pos=(1040,-590), size_hint=(None,None), allow_stretch=True))
        self.add_widget(Image(source="graphics/menu_background.png", size=(400,100), pos=(600,0), size_hint=(None,None), allow_stretch=True)) #botton menu
        self.add_widget(Image(source="graphics/menu_background.png", size=(550,90), pos=(5,60), size_hint=(None,None), allow_stretch=True)) #gold widget
        self.add_widget(Image(source="graphics/trash.png", size=(90,90), pos=(440,60), size_hint=(None,None), allow_stretch=True))
        self.add_widget(Image(source="graphics/shop_button.png", size=(60,60), pos=(130,80), size_hint=(None,None), allow_stretch=True))
        
        self.add_widget(Button(pos=(660,10), size_hint=(0.05,0.09), background_normal="graphics/team_button.png", on_press = lambda y:self.change_window("team")))
        self.add_widget(Button(pos=(760,10), size_hint=(0.05,0.09), background_normal="graphics/skills_button.png", on_press = lambda y:self.change_window("skills")))
        self.add_widget(Button(pos=(860,10), size_hint=(0.05,0.09), background_normal="graphics/map_button.png", on_press = lambda y:self.change_window("map")))
    
        
        im.inventory["main_hand"] = im.ItemSlot(pos=(player.current_player.inventory["main_hand"][0],player.current_player.inventory["main_hand"][1]), sprite=(player.current_player.inventory["main_hand"][2]))
        im.inventory["off_hand"] = im.ItemSlot(pos=(player.current_player.inventory["off_hand"][0],player.current_player.inventory["off_hand"][1]), sprite=(player.current_player.inventory["off_hand"][2]))
        im.inventory["armor"] = im.ItemSlot(pos=(player.current_player.inventory["armor"][0],player.current_player.inventory["armor"][1]), sprite=(player.current_player.inventory["armor"][2]))
        im.inventory["accessory"] = im.ItemSlot(pos=(player.current_player.inventory["accessory"][0],player.current_player.inventory["accessory"][1]), sprite=(player.current_player.inventory["accessory"][2]))
        im.inventory["accessory2"] = im.ItemSlot(pos=(player.current_player.inventory["accessory2"][0],player.current_player.inventory["accessory2"][1]), sprite=(player.current_player.inventory["accessory2"][2]))
        im.inventory["accessory3"] = im.ItemSlot(pos=(player.current_player.inventory["accessory3"][0],player.current_player.inventory["accessory3"][1]), sprite=(player.current_player.inventory["accessory3"][2]))
        im.inventory["potion"] = im.ItemSlot(pos=(player.current_player.inventory["potion"][0],player.current_player.inventory["potion"][1]), sprite=(player.current_player.inventory["potion"][2]))
        self.add_widget(im.inventory["main_hand"])
        self.add_widget(im.inventory["off_hand"])
        self.add_widget(im.inventory["armor"])
        self.add_widget(im.inventory["accessory"])
        self.add_widget(im.inventory["accessory2"])
        self.add_widget(im.inventory["accessory3"])
        self.add_widget(im.inventory["potion"])
        for x in range(0,48):
            im.inventory[x] = im.ItemSlot(pos=(player.current_player.inventory[x][0],player.current_player.inventory[x][1]), sprite=(player.current_player.inventory[x][2]))
            self.add_widget(im.inventory[x])

        self.add_widget(Button(pos=(1450,800), size=(50,50), size_hint=(None,None), background_normal="graphics/close_button.png", on_press = lambda y:self.change_screen()))
        
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
        self.exp_bar.pos_hint = {'x':0.705,'y':0.34}
        self.exp_bar.size_hint_x = 0.22
        self.add_widget(self.exp_bar)
        for x in list(UI.stats.keys())[0:-1]:
            UI.stats[x].bind(size=UI.stats[x].setter("text_size"))
            self.add_widget(UI.stats[x])
        self.add_widget(am.Stat_Button("HP","Zwiększa zdrowię o 10",pos=(1380,635)))
        self.add_widget(am.Stat_Button("MP","Zwiększa manę o 5",pos=(1380,590)))
        self.add_widget(am.Stat_Button("STR","Zwiększa obrażenia o 1\nWpływa na umiejętności wojownika",pos=(1380,545)))
        self.add_widget(am.Stat_Button("DEX","Decyduje o kolejce w walce\nZwiększa szansę na unik i cios krytyczny\nWpływa na umięjętności łotra",pos=(1380,505)))
        self.add_widget(am.Stat_Button("INT","Zwiększa bonus do doświadczenia\nWływa na umiejętności maga",pos=(1380,460)))
        
        UI.ui.stats_refresh(player.current_player)
        im.check_whitch_screen(self.manager.current)
        
        self.add_widget(self.current_sprite)
        self.add_widget(tp.text_pop)
        
        self.add_widget(self.empty_main_hand)
        self.add_widget(self.empty_off_hand)
        self.add_widget(self.empty_armor)
        self.add_widget(self.empty_accessory)
        self.add_widget(self.empty_accessory2) 
        self.add_widget(self.empty_accessory3)
        #self.add_widget(self.empty_potion)
        
        self.refresh_items()
            
    def change_character_menu(self,character):
        self.clear_widgets()
        UI.ui.stats_refresh(character)
        player.current_player = character
        for x in range(0,47):
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
        self.add_widget(self.current_sprite)
        print(self.current_sprite.base)
        self.remove_widget(self.tooltip)
        self.add_widget(self.tooltip)
 