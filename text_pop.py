from kivy.uix.label import Label
from kivy.metrics import dp

#def text_pop_up(t,pos_x,pos_y):
#    text_pop = Label(pos=(pos_x,pos_y), text=t, font_size=dp(24)) 
#    return text_pop

def clear_pop_up(dt):
        text_pop_inventory.text = ""
        text_pop_abilities.text = ""
        text_pop_fight.text = ""
        text_pop_shop.text = ""
        return False

text_pop_fight = Label(pos_hint={"center_x":0.5, "center_y": 0.8}, font_size=dp(24), outline_width = 1)
text_pop_inventory = Label(pos_hint={"center_x":0.5, "center_y": 0.8}, font_size=dp(24), outline_width = 1)
text_pop_shop = Label(pos_hint={"center_x":0.5, "center_y": 0.8}, font_size=dp(24), outline_width = 1)
text_pop_abilities = Label(pos_hint={"center_x":0.5, "center_y": 0.8}, font_size=dp(24), outline_width = 1)