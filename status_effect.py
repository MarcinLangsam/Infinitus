import tooltip as tt
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window

class Status():                                                                         #dmg_ot-damage over time
        #  nazwa(0)    efekt(1)     czas trawnia(w turach)(2)    ścierzka do ikony(3)   typ(4)     usunięcie efektu(5)  opis w walce(6)
    status_list={
        #statusy graczy
        "gniew":["gniew","self.current_target.STR *= 2\nself.current_target.damage = self.current_target.STR+self.current_target.weapon",4,"graphics/icons/gniew_status.png","one_time","self.current_turn.STR /= 2\nself.current_turn.damage = self.current_turn.STR+self.current_turn.weapon","Gniew\nSiła zwiększona o 20%"],
        "rozgrzewka":["rozgrzewka","self.current_target.DEX*=2",4,"graphics/icons/rozgrzewka_status.png","one_time","self.current_turn.DEX /= 2","Rozgrzewka\nZręczność zwiększona o 20%"],
        "skupienie":["skupienie","self.current_target.INT*=2",4,"graphics/icons/skupienie_status.png","one_time","self.current_turn.INT /= 2","Skupienie\nInteligencja zostaje zwiększona o 20%"],
        "zabójca idealny":["zabójca idealny","self.current_target.DEX*=50",2,"graphics/icons/zabojca_idealny_status.png","one_time","self.current_turn.DEX /= 50","Zabójca Idealny\nZręczność zwiększona 50-cio krotnie"],

        #statusy wszystkich
        "ogłuszenie":["ogłuszenie","",2,"graphics/icons/ogluszenie_status.png","stun","","Ogłuszenie\nCel pomija swoją turę"],
        "obezwładnienie":["obezwładnienie","",3,"graphics/icons/ogluszenie_status.png","stun","","Obezwładnienie\nCel pomija swoją turę"],
        "trucizna":["trucizna","self.current_turn.HP -= self.current_turn.MAX_HP*0.05",4,"graphics/icons/trucizna_status.png","dmg_ot","","Trucizna\nCel traci 5% HP co turę"],
        "zamrożenie":["zamrożenie","self.current_turn.HP -= self.current_turn.MAX_HP*0.1",3,"graphics/icons/zamrozenie_status.png","stun_dmg_ot","","Zamrożenie\nCel traci 10% HP i pomiją swoją turę "],
        "osłabienie":["osłabienie","self.current_target.damage /= 2",4,"graphics/icons/oslabienie_status.png","one_time","self.current_turn.damage *= 2","Osłabienie\nObrażenie od ataków zmniejszone o połowę"],

        #statusy przeciwników
        "zemsta":["zemsta","self.current_target.damage*=1.5\nself.current_target.STR*=1.5",3,"graphics/icons/zemsta_status.png","one_time","self.current_target.damage/=1.5\nself.current_target.STR/=1.5","Zemsta\nObrażenia od ataków zwiększone 1.5-ra"],
        "mroczna potega":["mroczna potega","self.current_target.damage*=2\nself.current_target.STR*=2\nself.current_target.defence -= 20",6,"graphics/icons/zemsta_status.png","one_time","self.current_target.damage/=2\nself.current_target.STR/=2\nself.current_target.defence += 20","Mroczna Potęga\nZadaje podwójne obrażenia ale traci cały pancerz"]
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
        tt.clear_tooltip(self.parent.tooltip)
    def display_tooltip(self, *args):
        tt.set_tooltip(self.parent.tooltip,self.t, self.p)


status_effect = Status()