import tooltip as tt
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window

class Status():                                                                         #dmg_ot-damage over time
        #  nazwa(0)    efekt(1)     czas trawnia(w turach)(2)    ścierzka do ikony(3)   typ(4)     usunięcie efektu(5)  opis w walce(6)
    status_list={
        #statusy graczy
        "sila":["siła","self.current_target.STR *= 2\nself.current_target.damage = self.current_target.STR+self.current_target.weapon",4,"graphics/icons/gniew_status.png","one_time","self.current_turn.STR /= 2\nself.current_turn.damage = self.current_turn.STR+self.current_turn.weapon",""],
        "zrecznosc":["zręczność","self.current_target.DEX*=2",4,"graphics/icons/rozgrzewka_status.png","one_time","self.current_turn.DEX /= 2",""],
        "inteligencja":["inteligencja","self.current_target.INT*=2",4,"graphics/icons/skupienie_status.png","one_time","self.current_turn.INT /= 2","Oświecenie\nInteligencja zostaje zwiększona o 10%"],
        "zabójca idealny":["zabójca idealny","self.current_target.DEX*=50",2,"graphics/icons/zabojca_idealny_status.png","one_time","self.current_turn.DEX /= 50",""],

        #statusy wszystkich
        "ogluszenie":["ogłuszenie","",2,"graphics/icons/ogluszenie_status.png","stun","","Ogłuszenie\nCel jest ogłuszony i pomija swoją turę"],
        "obezwladnienie":["obezwladnienie","",3,"graphics/icons/ogluszenie_status.png","stun","","",""],
        "trucizna":["trucizna","self.current_turn.HP -= self.current_turn.MAX_HP*0.05",4,"graphics/icons/trucizna_status.png","dmg_ot","",""],
        "zamrożenie":["zamrożenie","self.current_turn.HP -= self.current_turn.MAX_HP*0.1",3,"graphics/icons/zamrozenie_status.png","stun_dmg_ot","",""],
        "osłabienie":["osłabienie","self.current_target.damage /= 2",4,"graphics/icons/oslabienie_status.png","one_time","self.current_turn.damage *= 2",""],

        #statusy przeciwników
        "zemsta":["zemsta","self.current_target.damage*=1.5\nself.current_target.STR*=1.5",3,"graphics/icons/zemsta_status.png","one_time","self.current_target.damage/=1.5\nself.current_target.STR/=1.5",""],
        "mroczna potega":["mroczna potega","self.current_target.damage*=2\nself.current_target.STR*=2\nself.current_target.defence -= 20",6,"graphics/icons/zemsta_status.png","one_time","self.current_target.damage/=2\nself.current_target.STR/=2\nself.current_target.defence += 20",""]
    }        

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
        tt.clear_tooltip()
    def display_tooltip(self, *args):
        tt.set_tooltip_status(self.t, self.p)


status_effect = Status()