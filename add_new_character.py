import player, tooltip as tt, inventory_manager as im, UI_manager as UI
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from components.stats_component import stats_component
from components.character_creation_component import CreatorContainer


class Add_New_Character(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.tooltip = tt.Tooltip()
        


    def change_screen(self,screen):
        self.new_character.name = self.creation_menu.name_component.return_name()
        player.current_player = player.main_player
        self.clear_widgets()
        self.manager.current = screen
    def setup_window(self):

        if len(player.team) == 1:
            self.sprite = player.Character_Sprite(player.companion1,"one_hand",player.companion1.head,pos_hint={"center_x": 0.5, "center_y": 0.65})
            self.creation_menu = CreatorContainer(self.sprite, player.companion1, pos_hint={"center_x": 0.2, "center_y": 0.5}, size_hint=(0.25,0.95))
            self.creation_menu.classes_component.set_class(player.companion1, "warrior")
            player.team.append(player.companion1)
            player.current_player = player.companion1
            self.new_character = player.companion1
            while player.main_player.lv > player.companion1.lv:
                player.level_up(player.companion1)
        elif len(player.team) == 2:
            self.sprite = player.Character_Sprite(player.companion2,"one_hand",player.companion2.head,pos_hint={"center_x": 0.5, "center_y": 0.65})
            self.creation_menu = CreatorContainer(self.sprite, player.companion2, pos_hint={"center_x": 0.2, "center_y": 0.5}, size_hint=(0.25,0.95))
            self.creation_menu.classes_component.set_class(player.companion2, "warrior")
            player.team.append(player.companion2)
            player.current_player = player.companion2
            self.new_character = player.companion2
            while player.main_player.lv > player.companion2.lv:
                player.level_up(player.companion2)
        

        self.add_widget(Image(source="graphics/team_background.png", size_hint=(1,1), allow_stretch=True, fit_mode="fill"))
        self.add_widget(Button(pos_hint={"x": 0.9, "y": 0.92}, size=(160,60), font_size= 20, text="Wróc do menu", size_hint=(None,None), background_normal="graphics/target_button.png", on_press = lambda y:self.change_screen("main_menu")))
        self.add_widget(Button(pos_hint={"center_x": 0.5, "center_y": 0.1}, size=(500,70), font_size= 40, text="Dalej!", size_hint=(None,None), background_normal="graphics/target_button.png", on_press = lambda y:self.change_screen("menu")))
        self.add_widget(Label(text="DODAJ NOWEGO\nCZŁONKA DRUŻYNY!", pos_hint={"center_x": 0.5, "center_y": 0.9}, font_size=45))
        
        self.add_widget(self.sprite)
        self.add_widget(stats_component)
        self.add_widget(self.creation_menu)
        #self.add_widget(self.tooltip)
        
        if len(player.team) == 1:
            UI.ui.stats_refresh(player.companion1)
        elif len(player.team) == 2:
            UI.ui.stats_refresh(player.companion2)
        #self.refresh_items()

    def refresh_items(self):
        self.remove_widget(self.sprite)
        self.sprite.set_sprite(im.items.item_list[self.new_character.inventory["main_hand"][2]][0])
        self.sprite.set_sprite_weapon()
        self.add_widget(self.sprite)
        self.remove_widget(self.tooltip)
        self.add_widget(self.tooltip)

