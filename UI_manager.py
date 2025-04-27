from kivy.uix.label import Label
from player import gold
from player import team

class UI():         
    def stats_setup(self,character):
        
        stats["lv_label"] = Label(pos_hint={'x':0.70,'y':0.29}, font_size=33,halign="left", valign="middle", text="Poziom: ", outline_width = 1)
        stats["HP_label"]  = Label(pos_hint={'x':0.70,'y':0.24}, font_size=23,halign="left", valign="middle", text="HP: ", outline_width = 1, color=(1,0,0,1))
        stats["MP_label"] = Label(pos_hint={'x':0.70,'y':0.19}, font_size=23,halign="left", valign="middle", text="MP: ", outline_width = 1, color=(0,0,1,1))
        stats["STR_label"] = Label(pos_hint={'x':0.70,'y':0.14}, font_size=23,halign="left", valign="middle", text="Siła: ", outline_width = 1, color=(1,0.5,0,1))
        stats["DEX_label"] = Label(pos_hint={'x':0.70,'y':0.09}, font_size=23,halign="left", valign="middle", text="Zręczność: ", outline_width = 1, color=(0,1,0,1))
        stats["INT_label"] = Label(pos_hint={'x':0.70,'y':0.04}, font_size=23,halign="left", valign="middle", text="Inteligencja: ", outline_width = 1, color=(0.2,0.8,0.8,1))
        
        stats["damage_label"] = Label(pos_hint={'x':0.70,'y':-0.1}, font_size=23,halign="left", valign="middle", text="Obrażenia: ", outline_width = 1)
        stats["defence_label"] = Label(pos_hint={'x':0.70,'y':-0.15}, font_size=23,halign="left", valign="middle", text="Pancerz: ", outline_width = 1)
        stats["crit_chance_label"] = Label(pos_hint={'x':0.70,'y':-0.20}, font_size=23,halign="left", valign="middle", text="Szansa na cios krytyczny: ", outline_width = 1)
        stats["dodge_chance_label"] = Label(pos_hint={'x':0.70,'y':-0.25}, font_size=23,halign="left", valign="middle", text="Szansa na unik: ", outline_width = 1)
        stats["exp_boost_label"] = Label(pos_hint={'x':0.70,'y':-0.3}, font_size=23,halign="left", valign="middle", text="Bonus do doświadczenia: ", outline_width = 1)
        
        stats["stat_points_label"] = Label(pos_hint={'x':0.70,'y':-0.01}, font_size=27,halign="left", valign="middle", text="Punkty statystyk: ", outline_width = 1)
        
        stats["lv"] = Label(pos_hint={'x':0.83,'y':0.29}, font_size=33,halign="left", valign="middle", text=str(character.lv), outline_width = 1)
        stats["HP"]  = Label(pos_hint={'x':0.83,'y':0.24}, font_size=23,halign="left", valign="middle", text=str(character.MAX_HP), outline_width = 1, color=(1,0,0,1))
        stats["MP"] = Label(pos_hint={'x':0.83,'y':0.19}, font_size=23,halign="left", valign="middle", text=str(character.MAX_MP), outline_width = 1, color=(0,0,1,1))
        stats["STR"] = Label(pos_hint={'x':0.83,'y':0.14}, font_size=23,halign="left", valign="middle", text=str(character.STR), outline_width = 1, color=(1,0.5,0,1))
        stats["DEX"] = Label(pos_hint={'x':0.83,'y':0.09}, font_size=23,halign="left", valign="middle", text=str(character.DEX), outline_width = 1, color=(0,1,0,1))
        stats["INT"] = Label(pos_hint={'x':0.83,'y':0.04}, font_size=23,halign="left", valign="middle", text=str(character.INT), outline_width = 1, color=(0.2,0.8,0.8,1))
        
        stats["damage"] = Label(pos_hint={'x':0.83,'y':-0.1}, font_size=23,halign="left", valign="middle", text=str(character.damage), outline_width = 1)
        stats["defence"] = Label(pos_hint={'x':0.83,'y':-0.15}, font_size=23,halign="left", valign="middle", text=str(character.defence), outline_width = 1)
        stats["crit_chance"] = Label(pos_hint={'x':0.88,'y':-0.2}, font_size=23,halign="left", valign="middle", text=str(character.crit_chance), outline_width = 1)
        stats["dodge_chance"] = Label(pos_hint={'x':0.88,'y':-0.25}, font_size=23,halign="left", valign="middle", text=str(character.dodge_chance), outline_width = 1)
        stats["exp_boost"] = Label(pos_hint={'x':0.88,'y':-0.3}, font_size=23,halign="left", valign="middle", text=str(character.EXP_boost), outline_width = 1)
        
        stats["exp"] = Label(pos_hint={'x':0.745,'y':0.34}, font_size=25,halign="left", valign="middle", text=(("Doświadczenie: ") + str(character.EXP) + ("/") + str(character.EXP_To_Lv)), outline_width = 1)
        stats["stat_points"] = Label(pos_hint={'x':0.883,'y':-0.01}, font_size=27,halign="left", valign="middle", text="+"+str(character.stat_points), outline_width = 1)
        stats["gold"] = Label(pos_hint={'x':0.23,'y': -0.30}, font_size=33,halign="left", valign="middle", text=str(gold), outline_width = 1)
        stats["skill_points"] = Label(pos_hint={'x':0.315,'y':-0.437}, font_size=40,halign="left", valign="middle", text=(str(character.skill_points)), outline_width = 1)    
        
    def stats_refresh(self,character):
        character.damage = character.STR_base+character.weapon
        character.damage_base = character.STR_base+character.weapon
        character.crit_chance = 0.1*character.DEX_base+character.crit_chance_bonus
        character.dodge_chance = 0.02*character.DEX_base+character.dodge_chance_bonus
        character.EXP_boost = 0.1*character.INT_base+character.EXP_boost_bonus
        character.defence = character.defence_base

        stats["lv"].text = str(character.lv)
        stats["HP"].text = str(character.HP) + ("/") + str(character.MAX_HP)
        stats["MP"].text = str(character.MP) + ("/") + str(character.MAX_MP)
        stats["STR"].text = "{:.0f}".format(character.STR_base)
        stats["DEX"].text = "{:.0f}".format(character.DEX_base)
        stats["INT"].text = "{:.0f}".format(character.INT_base)
        stats["defence"].text = "{:.0f}".format(character.defence_base)
        stats["damage"].text = "{:.0f}".format(character.damage_base)
        stats["crit_chance"].text = "{:.2f}".format(character.crit_chance) + "%"
        stats["dodge_chance"].text = "{:.2f}".format(character.dodge_chance) + "%"
        stats["exp_boost"].text = "{:.2f}".format(character.EXP_boost) + "%"
        stats["exp"].text = (("Doświadczenie: ") + "{:.0f}".format(character.EXP) + ("/") + str(character.EXP_To_Lv))
        stats["gold"].text = "{0:g}".format(gold)
        if character.stat_points <= 0 :
            stats["stat_points_label"].font_size = 20
            stats["stat_points"].text = "brak"
            stats["stat_points"].font_size = 20
        else:
            stats["stat_points_label"].font_size = 27
            stats["stat_points"].text = "+"+str(character.stat_points)
            stats["stat_points"].font_size = 27

    
    def skill_points_refresh(self,character):
        stats["skill_points"].text = (str(character.skill_points))

stats = {}
ui = UI()
ui.stats_setup(team[0])
