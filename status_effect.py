# -*- coding: utf-8 -*-
import tooltip as tt, codecs
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window

class Status():
    status_list={}        

    def __init__(self):
        self.load_status()
        print(self.status_list)

    def load_status(self):
        data =["","","","","","","","",""]
        count = 0
        with codecs.open("status_list.txt",'r','utf-8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if line[0] == "_":
                    pass 
                else:
                    data[count] = line.strip().replace(r'\n','\n')
                    count+=1             
                    if count == 9: # <--- amout of separated data for one item/skill/status, change appropriately
                        self.status_list[data[0]] = [data[1],data[2],int(data[3]),data[4],data[5],data[6],data[7],data[8]]
                        count=0
        f.close()


class Status_Icon(Widget):
    source = ObjectProperty(None)
    def __init__(self,source,text,**kwargs):
        Window.bind(mouse_pos=self.on_mouse_pos)
        super().__init__(**kwargs)
        self.source = source
        self.t = text

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        Clock.unschedule(self.display_tooltip)
        self.close_tooltip()
        if self.collide_point(*self.to_widget(*pos)):
            self.p = self.pos
            Clock.schedule_once(self.display_tooltip, 0.5)

    def close_tooltip(self, *args):
        tt.clear_tooltip(self.parent.tooltip)
    def display_tooltip(self, *args):
        tt.set_tooltip_status(self.parent.tooltip,self.t, self.p)


status_effect = Status()
