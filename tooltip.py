from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle


def set_tooltip(t,p):
    tooltip.pos = (p[0]+130,p[1]-50)
    tooltip.text = t
    with tooltip.canvas.before:
        Color(0.8, 0.8, 0.8, 1)
        Rectangle(pos=(p[0],p[1]-50), size=(430,100))

def set_tooltip_status(t,p):
    tooltip_status.pos = (p[0]+130,p[1]-10)
    tooltip_status.text = t
    with tooltip_status.canvas.before:
        Color(0.8, 0.8, 0.8, 1)
        Rectangle(pos=(p[0],p[1]), size=(350,80))


def clear_tooltip():
    tooltip.canvas.before.clear()
    tooltip_status.canvas.before.clear()
    tooltip.text = ""
    tooltip_status.text = ""

class Tooltip(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 20
        self.color = (0,0,0,1)
        self.size_hint = (None,None)
        self.valign = "middle"
        self.halign = "left"

tooltip = Tooltip()
tooltip_status = Tooltip()
        