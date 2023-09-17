from kivy.uix.label import Label
from kivy.graphics import Color

def set_tooltip(tooltip,t,p):
    tooltip.pos = (p[0]+50,p[1]-50)
    tooltip.text = t
    with tooltip.canvas.before:
        Color(0.8,0.8,0.8,1)

def clear_tooltip(tooltip):
    tooltip.text = ""
    with tooltip.canvas.before:
        Color(0,0,0,0)

class Tooltip(Label):
    pass
