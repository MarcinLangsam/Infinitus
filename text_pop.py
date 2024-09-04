from kivy.uix.label import Label

def text_pop_up(t,pos_x,pos_y):
    text_pop = Label(pos=(pos_x,pos_y), text=t, font_size=24) 
    return text_pop

def clear_pop_up(dt):
        text_pop.text = ""
        return False

text_pop = Label(pos=(0,250), font_size=24, outline_width = 1)