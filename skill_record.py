import tooltip as tt, abilities_manager as am
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.core.window import Window

class Skill_Record(Button):
    source = ObjectProperty(None)
    
    def __init__(self,source,**kwargs):
        Window.bind(mouse_pos=self.on_mouse_pos)
        super().__init__(**kwargs)
        self.source = source
        self.t = ""
        self. p = 0

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        Clock.unschedule(self.display_tooltip)
        self.close_tooltip()
        if self.collide_point(*self.to_widget(*pos)):
            for x in am.skills.skill_list.keys():
                    if self.source == am.skills.skill_list[x][3]:
                            self.t = am.skills.skill_list[x][10]
                            self.p = (235,685)
            Clock.schedule_once(self.display_tooltip, 0.5)

    def close_tooltip(self, *args):
        tt.clear_tooltip()
    def display_tooltip(self, *args):
        tt.set_tooltip(self.t, self.p)