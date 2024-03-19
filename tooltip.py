from kivy.uix.label import Label
from kivy.graphics import Color
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.clock import Clock

def adjust_tooltip_to_screen(tooltip,pos_x,pos_y): #prewent tooltips to go over the screen where thay can't by seen by user
    #only for x axis, y is self expandable so i can't get valid size...yet
    if pos_x+tooltip.width > Window.size[0]:
        pos_x -= pos_x-Window.size[0]+tooltip.width
    if pos_x < 0:
        pos_x += -(pos_x)

    return (pos_x,pos_y)

def set_tooltip(tooltip,t,p):
    tooltip.pos = adjust_tooltip_to_screen(tooltip,p[0]+50,p[1]-50)
    tooltip.text = t
    tooltip.color = (1,1,1,1)
    tooltip.outline_width = 1
    tooltip.markup=True
    #with tooltip.canvas.before:
    #    Color(0.2,0.6,0.6,1)

def set_tooltip_status(tooltip,t,p):
    tooltip.pos = adjust_tooltip_to_screen(tooltip,p[0],p[1]+30)
    tooltip.text = t
    tooltip.color = (1,1,1,1)
    tooltip.outline_width = 1
    tooltip.markup=True
    #with tooltip.canvas.before:
    #    Color(0.2,0.6,0.6,1)

def set_tooltip_skill(tooltip,t,p):
    tooltip.text = t
    tooltip.color = (1,1,1,1)
    tooltip.outline_width = 1
    tooltip.markup=True
    tooltip.pos = adjust_tooltip_to_screen(tooltip,p[0]+50,p[1]-50)
    #with tooltip.canvas.before:
    #    Color(0.2,0.6,0.6,1)

def clear_tooltip(tooltip):
    tooltip.text = ""
    #with tooltip.canvas.before:
    #    Color(0.2,0.6,0.6,1)

class Tooltip(Label):
    pass

class Tooltip_Button(Button):
    def __init__(self, description, **kwargs):
        super().__init__(**kwargs)
        self.description = description
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.p = (0,0)
        self.t = ""
    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        Clock.unschedule(self.display_tooltip)
        self.close_tooltip()
        if self.collide_point(*self.to_widget(*pos)):
            self.t = self.description
            self.p = (self.pos[0],self.pos[1]+170)
            Clock.schedule_once(self.display_tooltip, 0.5)

    def close_tooltip(self, *args):
        clear_tooltip(self.parent.tooltip)
    def display_tooltip(self, *args):
        set_tooltip(self.parent.tooltip, self.t, self.p)

