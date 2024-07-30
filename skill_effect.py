from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

class Skill_Effect(Widget):
    effect = ObjectProperty("")

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.time = 0.0
        self.rate= 0.00001
        self.frame = 1
        self.frame_sum = 46
        self.source = "test_effect"
        
    def set_effect(self):
        pass
    
    def set_anim_parameters(self,time,rate,frame,frame_sum):
        self.time = time
        self.rate = rate
        self.frame = frame
        self.frame = frame_sum
