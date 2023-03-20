import player,UI_manager as UI
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty, ListProperty

class Skill_line(Widget):
    points = ListProperty([])
class SkillSlot(Widget):

    sprite = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.pos[0] <= touch.pos[0] <= self.pos[0]+50 and self.pos[1] <= touch.pos[1] <= self.pos[1]+50: 
            for x in skills.skill_list.keys():
                    if self.pos[0] == skills.skill_list[x][4] and self.pos[1] == skills.skill_list[x][5]:
                        if skills.skill_list[x][0] in player.current_player.skill:
                            print("Już masz tę umiejętność")
                        else:
                            if player.current_player.skill_points > 0:
                                if skills.skill_list[x][2] in player.current_player.skill or skills.skill_list[x][2]=="none":
                                    player.current_player.skill[skills.skill_list[x][0]] = [skills.skill_list[x][1]]
                                    print("Dodano umiejętność")
                                    skills_objects[x].sprite=(skills.skill_list[x][7])
                                    player.current_player.skill_points-=1
                                    UI.ui.skill_points_refresh(player.current_player)
                                else:
                                    print("Potrzeba wcześniejszych umiejętności")
                            else:
                                print("Nie masz wystarczająco punktów umiejętności")
        else:
            pass

class Skills():
    skill_list={
        0:["zamach","self.enemy.HP -= self.player.STR*10","none","zamach.png",100,100,"none","zamach_ok.png"],
        1:["cios rękojeścią","self.enemy.HP -= self.player.STR*10","zamach","empty_main_hand.png",100,300,0,"zamach_ok.png"]

    }

class Stat_STR_Button(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_up(self, touch):
        if self.pos[0] <= touch.pos[0] <= self.pos[0]+25 and self.pos[1] <= touch.pos[1] <= self.pos[1]+25:
            self.increase_stat()

    def increase_stat(self):
        if player.current_player.stat_points > 0:
            player.current_player.STR += 1
            player.current_player.stat_points -=1
            UI.ui.stats_refresh(player.current_player)
        else:
            print("Nie masz punktów statystyk")

class Stat_DEX_Button(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_up(self, touch):
        if self.pos[0] <= touch.pos[0] <= self.pos[0]+25 and self.pos[1] <= touch.pos[1] <= self.pos[1]+25:
            self.increase_stat()

    def increase_stat(self):
        if player.current_player.stat_points > 0:
            player.current_player.DEX += 1
            player.current_player.stat_points -=1
            UI.ui.stats_refresh(player.current_player)
        else:
            print("Nie masz punktów statystyk")

class Stat_INT_Button(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_up(self, touch):
        if self.pos[0] <= touch.pos[0] <= self.pos[0]+25 and self.pos[1] <= touch.pos[1] <= self.pos[1]+25:
            self.increase_stat()

    def increase_stat(self):
        if player.current_player.stat_points > 0:
            player.current_player.INT += 1
            player.current_player.stat_points -=1
            UI.ui.stats_refresh(player.current_player)
        else:
            print("Nie masz punktów statystyk")


skills = Skills()
skills_objects = {}