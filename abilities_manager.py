# -*- coding: utf-8 -*-
import player,UI_manager as UI, text_pop as tp, tooltip as tt, codecs
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivy.core.window import Window 
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.core.audio import SoundLoader
from kivy.metrics import dp
from resource_path import get_resource_path

class Skill_line(Widget):
    points = ListProperty([])
class SkillSlot(Widget):
    sprite = StringProperty("")
    def __init__(self, **kwargs):
        Window.bind(mouse_pos=self.on_mouse_pos)
        super().__init__(**kwargs)
        self.t = ""
        self.p = 0
        self.new_skill_sound = SoundLoader.load("graphics/sounds/new_skill.wav")
        self.error_sound = SoundLoader.load("graphics/sounds/error.wav")

    def on_touch_down(self, touch):
        if self.pos[0] <= touch.pos[0] <= self.pos[0]+dp(50) and self.pos[1] <= touch.pos[1] <= self.pos[1]+dp(50): 
            for x in skills.skill_list.keys():
                    if self.pos[0] == dp(skills.skill_list[x][4]) and self.pos[1] == dp(skills.skill_list[x][5]):
                        if skills.skill_list[x][0] in player.current_player.skill:
                            tp.text_pop.text = "Już masz tę umiejętność"
                            self.error_sound.play()
                        else:
                            if player.current_player.skill_points > 0:
                                if skills.skill_list[x][2] in player.current_player.skill or skills.skill_list[x][2]=="none":
                                    player.current_player.skill[skills.skill_list[x][0]] = [skills.skill_list[x][1],skills.skill_list[x][8],skills.skill_list[x][3],skills.skill_list[x][10],skills.skill_list[x][9],skills.skill_list[x][11],skills.skill_list[x][12],skills.skill_list[x][13],skills.skill_list[x][14]]
                                    if skills.skill_list[x][9] == "passive":
                                        exec(skills.skill_list[x][1])
                                    tp.text_pop.text = "Dodano umiejętność"
                                    skills_objects[x].sprite=(skills.skill_list[x][7])
                                    player.current_player.skill_points-=1
                                    UI.ui.skill_points_refresh(player.current_player)
                                    self.new_skill_sound.play()
                                else:
                                    tp.text_pop.text = "Poptrzeba wcześniejszych umiejętności"
                                    self.error_sound.play()
                            else:
                                tp.text_pop.text = "Nie masz punktów umiejętności"
                                self.error_sound.play()
                        Clock.schedule_interval(tp.clear_pop_up,3)
        else:
            pass
    
    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        Clock.unschedule(self.display_tooltip)
        self.close_tooltip()
        if self.collide_point(*self.to_widget(*pos)):
            for x in skills.skill_list.keys():
                    if self.pos[0] == dp(skills.skill_list[x][4]) and self.pos[1] == dp(skills.skill_list[x][5]):   
                            self.t = skills.skill_list[x][10]
                            self.p = (self.pos[0],self.pos[1])
            Clock.schedule_once(self.display_tooltip, 0.5)

    def close_tooltip(self, *args):
        tt.clear_tooltip(self.parent.tooltip)
    def display_tooltip(self, *args):
        tt.set_tooltip_skill(self.parent.tooltip,self.t, self.p)
    
class Skills():
    skill_list={}

    def __init__(self):
        self.load_skills()

    def load_skills(self):
        data =["","","","","","","","","","","","","","","",""]
        count = 0
        file_path = get_resource_path("skill_list.txt")
        with codecs.open(file_path,'r','utf-8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if line[0] == "_":
                    pass 
                else:
                    data[count] = line.strip().replace(r'\n','\n')
                    if count == 7 and data[count] != "none":
                        data[count] = int(data[count])
                    count+=1             
                    if count == 16: # <--- amout of separated data for one item/skill/status, change appropriately
                        self.skill_list[int(data[0])] = [data[1],data[2],data[3],data[4],int(data[5]),int(data[6]),data[7],data[8],int(data[9]),data[10],data[11],data[12],data[13],data[14],data[15]]
                        count=0
        
        f.close()

class Stat_Button(Button):
    def __init__(self,stat,description,**kwargs):
        super().__init__(**kwargs)
        self.stat = stat
        self.bind(on_release=self.on_toggle)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.description = description

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        Clock.unschedule(self.display_tooltip)
        self.close_tooltip()
        if self.collide_point(*self.to_widget(*pos)):
            self.t = self.description
            self.p = (dp(600),dp(700))
            Clock.schedule_once(self.display_tooltip, 0.5)

    def close_tooltip(self, *args):
        tt.clear_tooltip(self.parent.tooltip)
    def display_tooltip(self, *args):
        tt.set_tooltip(self.parent.tooltip, self.t, self.p)

    def on_toggle(self, touch):
        if isinstance(self.last_touch, MouseMotionEvent):
            self.increase_stat()

    def increase_stat(self):
        if player.current_player.stat_points > 0:
            if self.stat == "HP":
                player.current_player.MAX_HP += 10
                player.current_player.HP +=10
            #elif self.stat == "MP":
            #    player.current_player.MAX_MP += 5
            #    player.current_player.MP +=5
            elif self.stat == "STR":
                player.current_player.STR_base +=1
            elif self.stat == "DEX":
                player.current_player.DEX_base +=1
            elif self.stat == "INT":
                player.current_player.INT_base +=1   
            player.current_player.stat_points -=1
            UI.ui.stats_refresh(player.current_player)
        else:
            tp.text_pop.text = "Nie masz punktów statystyk"
            Clock.schedule_interval(tp.clear_pop_up,3)

skills = Skills()
skills_objects = {}