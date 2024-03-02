import player
from kivy.uix.label import Label

class UI():         
    def stats_setup(self,character):
        
        stats["lv_label"] = Label(pos_hint={'x':0.70,'y':0.3}, font_size=23,halign="left", valign="middle", text="Poziom postaci: ")
        stats["HP_label"]  = Label(pos_hint={'x':0.70,'y':0.25}, font_size=23,halign="left", valign="middle", text="HP: ")
        stats["MP_label"] = Label(pos_hint={'x':0.70,'y':0.20}, font_size=23,halign="left", valign="middle", text="MP: ")
        stats["STR_label"] = Label(pos_hint={'x':0.70,'y':0.15}, font_size=23,halign="left", valign="middle", text="Siła: ")
        stats["DEX_label"] = Label(pos_hint={'x':0.70,'y':0.10}, font_size=23,halign="left", valign="middle", text="Zręczność: ")
        stats["INT_label"] = Label(pos_hint={'x':0.70,'y':0.05}, font_size=23,halign="left", valign="middle", text="Inteligencja: ")
        
        stats["damage_label"] = Label(pos_hint={'x':0.70,'y':-0.1}, font_size=23,halign="left", valign="middle", text="Obrażenia: ")
        stats["defence_label"] = Label(pos_hint={'x':0.70,'y':-0.15}, font_size=23,halign="left", valign="middle", text="Pancerz: ")
        stats["crit_chance_label"] = Label(pos_hint={'x':0.70,'y':-0.2}, font_size=23,halign="left", valign="middle", text="Szansa na cios krytyczny: ")
        stats["dodge_chance_label"] = Label(pos_hint={'x':0.70,'y':-0.25}, font_size=23,halign="left", valign="middle", text="Szansa na unik: ")
        stats["exp_boost_label"] = Label(pos_hint={'x':0.70,'y':-0.3}, font_size=23,halign="left", valign="middle", text="Bonus do doświadczenia: ")
        
        #stats["exp_label"] = Label(pos_hint={'x':0.783,'y':0.45}, font_size=18,halign="left", valign="middle", text="Doświadczenie: ")
        stats["stat_points_label"] = Label(pos_hint={'x':0.70,'y':0.0}, font_size=23,halign="left", valign="middle", text="Punkty statystyk: ")
        #stats["skill_points_label"] = Label(pos_hint={'x':0.32,'y':0.45}, font_size=25,halign="left", valign="middle", text=(("Punkty umiejętności: ") + str(character.skill_points)))  

        stats["lv"] = Label(pos_hint={'x':0.83,'y':0.3}, font_size=23,halign="left", valign="middle", text=str(character.lv))
        stats["HP"]  = Label(pos_hint={'x':0.83,'y':0.25}, font_size=23,halign="left", valign="middle", text=str(character.MAX_HP))
        stats["MP"] = Label(pos_hint={'x':0.83,'y':0.20}, font_size=23,halign="left", valign="middle", text=str(character.MAX_MP))
        stats["STR"] = Label(pos_hint={'x':0.83,'y':0.15}, font_size=23,halign="left", valign="middle", text=str(character.STR))
        stats["DEX"] = Label(pos_hint={'x':0.83,'y':0.10}, font_size=23,halign="left", valign="middle", text=str(character.DEX))
        stats["INT"] = Label(pos_hint={'x':0.83,'y':0.05}, font_size=23,halign="left", valign="middle", text=str(character.INT))
        
        stats["damage"] = Label(pos_hint={'x':0.83,'y':-0.1}, font_size=23,halign="left", valign="middle", text=str(character.damage))
        stats["defence"] = Label(pos_hint={'x':0.83,'y':-0.15}, font_size=23,halign="left", valign="middle", text=str(character.defence))
        stats["crit_chance"] = Label(pos_hint={'x':0.88,'y':-0.2}, font_size=23,halign="left", valign="middle", text=str(character.crit_chance))
        stats["dodge_chance"] = Label(pos_hint={'x':0.88,'y':-0.25}, font_size=23,halign="left", valign="middle", text=str(character.dodge_chance))
        stats["exp_boost"] = Label(pos_hint={'x':0.88,'y':-0.3}, font_size=23,halign="left", valign="middle", text=str(character.EXP_boost))
        
        stats["exp"] = Label(pos_hint={'x':0.735,'y':0.35}, font_size=25,halign="left", valign="middle", text=(("Doświadczenie: ") + str(character.EXP) + ("/") + str(character.EXP_To_Lv)))
        stats["stat_points"] = Label(pos_hint={'x':0.83,'y':0.0}, font_size=23,halign="left", valign="middle", text=str(character.stat_points))
        stats["gold"] = Label(pos_hint={'x':0.13,'y':-0.378}, font_size=33,halign="left", valign="middle", text=str(player.gold))
        stats["skill_points"] = Label(pos_hint={'x':0.32,'y':0.45}, font_size=23,halign="left", valign="middle", text=(("Punkty umiejętności: ") + str(character.skill_points)))    
        
    def stats_refresh(self,character):
        character.damage = character.STR+character.weapon
        character.crit_chance = 0.1*character.DEX
        character.dodge_chance = 0.02*character.DEX
        character.EXP_boost = 0.1*character.INT

        stats["lv"].text = str(character.lv)
        stats["HP"].text = str(character.HP) + ("/") + str(character.MAX_HP)
        stats["MP"].text = str(character.MP) + ("/") + str(character.MAX_MP)
        stats["STR"].text = str(character.STR)
        stats["DEX"].text = str(character.DEX)
        stats["INT"].text = str(character.INT)
        stats["defence"].text = str(character.defence)
        stats["damage"].text = str(character.damage)
        stats["crit_chance"].text = "{:.2f}".format(character.crit_chance) + "%"
        stats["dodge_chance"].text = "{:.2f}".format(character.dodge_chance) + "%"
        stats["exp_boost"].text = "{:.2f}".format(character.EXP_boost) + "%"
        stats["exp"].text = (("Doświadczenie: ") + str(character.EXP) + ("/") + str(character.EXP_To_Lv))
        stats["gold"].text = str(player.gold)
        stats["stat_points"].text = str(character.stat_points)
        
    
    def skill_points_refresh(self,character):
        stats["skill_points"].text = (("Punkty umiejętności: ") + str(character.skill_points))

stats = {}
ui = UI()
ui.stats_setup(player.team[0])
