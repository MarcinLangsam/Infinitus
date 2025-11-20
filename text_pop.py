from kivy.uix.label import Label
from kivy.metrics import dp

def clear_pop_up(dt):
        text_pop_fight.text = ""
        text_pop_inventory.text = ""
        text_pop_shop.text = ""
        text_pop_abilities.text = ""
        text_pop_stat_up.text = ""
        text_pop_save_game.text = ""
        return False

text_pop_fight = Label(pos_hint={"center_x":0.5, "center_y": 0.77}, font_size=dp(24), outline_width = 1)
text_pop_inventory = Label(pos_hint={"center_x":0.5, "center_y": 0.8}, font_size=dp(24), outline_width = 1)
text_pop_shop = Label(pos_hint={"center_x":0.5, "center_y": 0.8}, font_size=dp(24), outline_width = 1)
text_pop_abilities = Label(pos_hint={"center_x":0.5, "center_y": 0.81}, font_size=dp(24), outline_width = 1)
text_pop_stat_up = Label(pos_hint={"center_x":0.5, "center_y": 0.81}, font_size=dp(24), outline_width = 1)
text_pop_save_game = Label(pos_hint={"x": 0.2, "center_y": 0.40}, font_size=dp(35), outline_width = 1)