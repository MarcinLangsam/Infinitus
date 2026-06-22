import player, tooltip as tt, inventory_manager as im, UI_manager as UI, fight, text_pop as tp
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from components.stats_component import stats_component
from components.character_creation_component import CreatorContainer

class Character_Creation(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.sprite = player.Character_Sprite(player.main_player,"one_hand",player.main_player.head,pos_hint={"center_x": 0.5, "center_y": 0.65})
        self.tooltip = tt.Tooltip()
        self.creation_menu = CreatorContainer(self.sprite, player.main_player, pos_hint={"center_x": 0.2, "center_y": 0.5}, size_hint=(0.25,0.95))
        
    def change_screen(self,screen):
        player.main_player.name = self.creation_menu.name_component.return_name()
        player.gold = 5000
        self.clear_widgets()
        self.manager.current = screen
    def setup_window(self):
        player.main_player.hard_reset_player()
        player.companion1.hard_reset_player()
        player.companion2.hard_reset_player()
        player.team.clear()
        player.team.append(player.main_player)
        player.current_player = player.main_player

        fight.current_fight = 1
        fight.current_stage = 1


        self.add_widget(Image(source="graphics/team_background.png", size_hint=(1,1), allow_stretch=True, fit_mode="fill"))
        self.add_widget(Button(pos_hint={"x": 0.9, "y": 0.92}, size=(160,60), font_size= 20, text="Wróc do menu", size_hint=(None,None), background_normal="graphics/target_button.png", on_press = lambda y:self.change_screen("main_menu")))
        self.add_widget(Button(pos_hint={"center_x": 0.5, "center_y": 0.1}, size=(500,70), font_size= 40, text="Rozpocznij Grę!", size_hint=(None,None), background_normal="graphics/target_button.png", on_press = lambda y:self.change_screen("menu")))
        self.add_widget(Label(text="KIM JESTEŚ?", pos_hint={"center_x": 0.5, "center_y": 0.9}, font_size=45))
        
        self.add_widget(self.sprite)
        stats_component.hidden()
        self.add_widget(stats_component)
        self.add_widget(self.creation_menu)
        self.creation_menu.classes_component.set_class(player.main_player, "warrior")
        self.add_widget(tp.text_pop_stat_up)
        #self.add_widget(self.tooltip)
        
        UI.ui.stats_refresh(player.main_player)
        #self.refresh_items()


    def refresh_items(self):
        self.remove_widget(self.sprite)
        self.sprite.set_sprite(im.items.item_list[player.current_player.inventory["main_hand"][2]][0])
        self.sprite.set_sprite_weapon()
        self.add_widget(self.sprite)
        self.remove_widget(self.tooltip)
        self.add_widget(self.tooltip)

