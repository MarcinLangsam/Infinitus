import player, inventory_manager as im, fight, tooltip as tt
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.metrics import dp

def text_pop_up(t,pos_x,pos_y):
    text_pop = Label(pos=(pos_x,pos_y), text=t, font_size=25, outline_width=1)
    return text_pop

class EXPBar(ProgressBar):
    pass
class Battle_Result(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.exp_bar_player = EXPBar(pos_hint={"center_x": 0.55, "center_y": 0.7}, size_hint_x = 0.1, max=100)
        self.exp_bar_companion_one = EXPBar(pos_hint={"center_x": 0.55, "center_y": 0.5}, size_hint_x = 0.1, max=100) 
        self.exp_bar_companion_two = EXPBar(pos_hint={"center_x": 0.55, "center_y": 0.3}, size_hint_x = 0.1, max=100)
        self.exp_bar_player_text = Label(pos_hint={"center_x": 0.55, "center_y": 0.71}, font_size=25,halign="left", valign="middle", outline_width=1)
        self.exp_bar_companion_one_text = Label(pos_hint={"center_x": 0.55, "center_y": 0.51}, font_size=25,halign="left", valign="middle", outline_width=1)
        self.exp_bar_companion_two_text = Label(pos_hint={"center_x": 0.55, "center_y": 0.31}, font_size=25,halign="left", valign="middle", outline_width=1)
        self.gold_gain = Label(pos_hint={'x':-0.25,'y': -0.295}, font_size=33, halign="right", valign="middle", outline_width=1)
        self.ok1 = False
        self.ok2 = False
        self.ok3 = False
        self.tooltip = tt.Tooltip()
    def change_screen(self):
        self.check_for_lv_up()
        self.clear_widgets()
        self.manager.current = "menu"
    def setup_window(self):
        self.add_widget(Image(source="graphics/team_background.png", size_hint=(1,1), allow_stretch=True, fit_mode="fill"))
        self.add_widget(Button(pos_hint={"center_x": 0.95, "center_y": 0.95}, size=(50,50), size_hint=(None,None), background_normal="graphics/close_button.png", on_press = lambda y:self.change_screen()))
        self.add_widget(Image(source="graphics/menu_background.png", size=(550,90), pos_hint={"x": 0.069, "y": 0.16}, size_hint=(None,None), allow_stretch=True)) #gold widget
        self.add_widget(Image(source="graphics/shop_button.png", size=(60,60), pos_hint={"x": 0.14, "y": 0.18}, size_hint=(None,None), allow_stretch=True))
        Clock.schedule_once(self.progress_bar_start)
        self.add_widget(Image(source="graphics/sprites/"+player.main_player.head+"_portrait.png", pos_hint={"center_x": 0.45, "center_y": 0.7}))
        self.add_widget(Image(source="graphics/sprites/"+player.companion1.head+"_portrait.png", pos_hint={"center_x": 0.45, "center_y": 0.5}))
        self.add_widget(Image(source="graphics/sprites/"+player.companion2.head+"_portrait.png", pos_hint={"center_x": 0.45, "center_y": 0.3}))
        self.add_widget(self.exp_bar_player)
        self.add_widget(self.exp_bar_companion_one)
        self.add_widget(self.exp_bar_companion_two)
        self.add_widget(self.exp_bar_player_text)
        self.add_widget(self.exp_bar_companion_one_text)
        self.add_widget(self.exp_bar_companion_two_text)
        self.add_widget(self.gold_gain)
        im.check_whitch_screen(self.manager.current)
        
        for x in range(0,96):
            im.inventory[x] = im.ItemSlot(pos=(player.main_player.inventory[x][0],player.main_player.inventory[x][1]), sprite=(player.main_player.inventory[x][2]))
            self.add_widget(im.inventory[x])
        self.gold_gain.text = "+"+"{0:g}".format(fight.gold_gain)
        self.add_widget(self.tooltip)
            
    def progress_bar_start(self, instance): 
        self.ok1 = False
        self.ok2 = False
        self.ok3 = False
        self.exp_bar_player.value = 0
        self.exp_bar_companion_one.value = 0
        self.exp_bar_companion_two.value = 0
        self.exp_bar_player.max = player.main_player.EXP_To_Lv
        self.exp_bar_companion_one.max = player.companion1.EXP_To_Lv
        self.exp_bar_companion_two.max = player.companion2.EXP_To_Lv
        self.start_fill_animation()
    
    def check_for_lv_up(self):
        if player.main_player.EXP >= player.main_player.EXP_To_Lv:
            player.level_up(player.main_player)
        if player.companion1.EXP >= player.companion1.EXP_To_Lv:
            player.level_up(player.companion1)
        if player.companion2.EXP >= player.companion2.EXP_To_Lv:
            player.level_up(player.companion2)
  
    def next(self, dt):

        if self.ok1 == True and self.ok2 == True and self.ok3 == True:

            return False
        
        if self.exp_bar_player.value >= player.main_player.EXP or self.exp_bar_player.value == self.exp_bar_player.max:
            if self.exp_bar_player.value == self.exp_bar_player.max and self.ok1 == False:
                self.add_widget(text_pop_up("AWANS",dp(20),dp(215)))
                self.ok1 = True
        else:
            self.exp_bar_player.value += 1
            self.exp_bar_player_text.text = "{0:g}".format(self.exp_bar_player.value)+" / "+str(player.main_player.EXP_To_Lv)
        
        if self.exp_bar_companion_one.value >= player.companion1.EXP or self.exp_bar_companion_one.value == self.exp_bar_companion_one.max:
            if self.exp_bar_companion_one.value == self.exp_bar_companion_one.max and self.ok2 == False:
                self.add_widget(text_pop_up("AWANS",dp(125),dp(70)))
                self.ok2 = True
            pass    
        else:
            self.exp_bar_companion_one.value += 1
            self.exp_bar_companion_one_text.text = "{0:g}".format(self.exp_bar_companion_one.value)+" / "+str(player.companion1.EXP_To_Lv)
        
        if self.exp_bar_companion_two.value >= player.companion2.EXP or self.exp_bar_companion_two.value == self.exp_bar_companion_two.max:
            if self.exp_bar_companion_two.value == self.exp_bar_companion_two.max and self.ok3 == False:
                self.add_widget(text_pop_up("AWANS",dp(125),dp(-220)))
                self.ok3 = True
            pass
        else:
            self.exp_bar_companion_two.value += 1
            self.exp_bar_companion_two_text.text = "{0:g}".format(self.exp_bar_companion_two.value)+" / "+str(player.companion2.EXP_To_Lv)

    def start_fill_animation(self):
        Clock.schedule_interval(self.next, 1/70)
        