import player
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

class UI():         
    def stats_setup(self,character):
        stats["lv"] = Label(pos_hint={'x':0.35,'y':0.4}, font_size=20, text=(("Poziom postaci: ") + str(character.lv)))
        stats["HP"]  = Label(pos_hint={'x':0.35,'y':0.35}, font_size=20, text=(("HP: ") + str(character.HP) + ("/") + str(character.MAX_HP)))
        stats["MP"] = Label(pos_hint={'x':0.35,'y':0.30}, font_size=20, text=(("MP: ") + str(character.MP) + ("/") + str(character.MAX_MP)))
        stats["STR"] = Label(pos_hint={'x':0.35,'y':0.25}, font_size=20, text=(("Siła: ") + str(character.STR)))
        stats["DEX"] = Label(pos_hint={'x':0.35,'y':0.20}, font_size=20, text=(("Zręczność: ") + str(character.DEX)))
        stats["INT"] = Label(pos_hint={'x':0.35,'y':0.15}, font_size=20, text=(("Inteligencja: ") + str(character.INT)))
        stats["defence"] = Label(pos_hint={'x':0.35,'y':0.10}, font_size=20, text=(("Pancerz: ") + str(character.defence)))
        stats["damage"] = Label(pos_hint={'x':0.35,'y':0.05}, font_size=20, text=(("Obrażenia: ") + str(character.damage)))
        stats["crit_chance"] = Label(pos_hint={'x':0.35,'y':0.0}, font_size=20, text=(("Szansa na cios krytyczny: ") + str(character.crit_chance)))
        stats["dodge_chance"] = Label(pos_hint={'x':0.35,'y':-0.05}, font_size=20, text=(("Szansa na unik: ") + str(character.dodge_chance)))
        stats["exp_boost"] = Label(pos_hint={'x':0.35,'y':-0.1}, font_size=20, text=(("Bonus do doświadczenia: ") + str(character.EXP_boost)))
        stats["exp"] = Label(pos_hint={'x':0.35,'y':-0.25}, font_size=20, text=(("Doświadczenie: ") + str(character.EXP) + ("/") + str(character.EXP_To_Lv)))
        stats["gold"] = Label(pos_hint={'x':0.35,'y':-0.3}, font_size=20, text=(("Złoto: ") + str(player.gold)))
        stats["stat_points"] = Label(pos_hint={'x':0.35,'y':-0.15}, font_size=20, text=(("Punkty statystyk: ") + str(character.stat_points)))
        stats["skill_points"] = Label(pos_hint={'x':0.35,'y':0.4}, font_size=20, text=(("Punkty umiejętności: ") + str(character.skill_points)))    
        
    def stats_refresh(self,character):
        character.damage = character.STR+character.weapon
        character.crit_chance = 0.1*character.DEX
        character.dodge_chance = 0.02*character.DEX
        character.EXP_boost = 0.1*character.INT
        stats["lv"].text = (("Poziom postaci: ") + str(character.lv))
        stats["HP"].text = ("HP: ") + str(character.HP) + ("/") + str(character.MAX_HP)
        stats["MP"].text = ("MP: ") + str(character.MP) + ("/") + str(character.MAX_MP)
        stats["STR"].text = (("Siła: ") + str(character.STR))
        stats["DEX"].text = (("Zręczność: ") + str(character.DEX))
        stats["INT"].text = (("Inteligencja: ") + str(character.INT))
        stats["defence"].text = (("Pancerz: ") + str(character.defence))
        stats["damage"].text = (("Obrażenia: ") + str(character.damage))
        stats["crit_chance"].text = (("Szansa na cios krytyczny: ") + str(character.crit_chance))
        stats["dodge_chance"].text = (("Szansa na unik: ") + str(character.dodge_chance))
        stats["exp_boost"].text = (("Bonus do doświadczenia: ") + str(character.EXP_boost))
        stats["exp"].text = (("Doświadczenie: ") + str(character.EXP) + ("/") + str(character.EXP_To_Lv))
        stats["gold"].text = (("Złoto: ") + str(player.gold))
        stats["stat_points"].text = (("Punkty statystyk: ") + str(character.stat_points))
        
    
    def skill_points_refresh(self,character):
        stats["skill_points"].text = (("Punkty umiejętności: ") + str(character.skill_points))

stats = {}
ui = UI()
ui.stats_setup(player.team[0])
