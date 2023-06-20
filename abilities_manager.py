import player,UI_manager as UI, text_pop as tp, tooltip as tt, status_effect as se
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivy.core.window import Window 
from kivy.input.providers.mouse import MouseMotionEvent

class Skill_line(Widget):
    points = ListProperty([])
class SkillSlot(Widget):
    sprite = StringProperty("")
    def __init__(self, **kwargs):
        Window.bind(mouse_pos=self.on_mouse_pos)
        super().__init__(**kwargs)
        self.t = 0
        self.p = 0

    def on_touch_down(self, touch):
        if self.pos[0] <= touch.pos[0] <= self.pos[0]+50 and self.pos[1] <= touch.pos[1] <= self.pos[1]+50: 
            for x in skills.skill_list.keys():
                    if self.pos[0] == skills.skill_list[x][4] and self.pos[1] == skills.skill_list[x][5]:
                        if skills.skill_list[x][0] in player.current_player.skill:
                            tp.text_pop.text = "Już masz tę umiejętność"
                        else:
                            if player.current_player.skill_points > 0:
                                if skills.skill_list[x][2] in player.current_player.skill or skills.skill_list[x][2]=="none":
                                    player.current_player.skill[skills.skill_list[x][0]] = [skills.skill_list[x][1],skills.skill_list[x][8],skills.skill_list[x][3],skills.skill_list[x][10],skills.skill_list[x][9],skills.skill_list[x][11],skills.skill_list[x][12]]
                                    if skills.skill_list[x][9] == "passive":
                                        exec(skills.skill_list[x][1])
                                    tp.text_pop.text = "Dodano umiejętność"
                                    skills_objects[x].sprite=(skills.skill_list[x][7])
                                    player.current_player.skill_points-=1
                                    UI.ui.skill_points_refresh(player.current_player)
                                else:
                                    tp.text_pop.text = "Poptrzeba wcześniejszych umiejętności"
                            else:
                                tp.text_pop.text = "Nie masz punktów umiejętności"
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
                    if self.pos[0] == skills.skill_list[x][4] and self.pos[1] == skills.skill_list[x][5]:   
                            self.t = skills.skill_list[x][10]
                            self.p = (self.pos[0],self.pos[1])
            Clock.schedule_once(self.display_tooltip, 0.5)

    def close_tooltip(self, *args):
        tt.clear_tooltip()
    def display_tooltip(self, *args):
        tt.set_tooltip(self.t, self.p)
    
class Skills():
    skill_list={
        #nazwa(0)   efekt(1)   czego wymaga(2)    ścierzka do pliku(3)   pozycja x(4)   pozycja y(5)   od którego ma być linia(6)    ścierzka po nauczeniu(7)    koszt MP(8)    aktywa/pasywna(9)      opis(10)    zasieg(11)      cel(12)
        #umiejętności wojownika
        0:["zamach","self.final_damage = 10+self.current_turn.STR*3","none","graphics/skills/zamach.png",300,70,"none","graphics/skills/zamach_ok.png",20,"active","Zamach\nObszerny zamach zadający:\n10+STR*3 obrażeń\nKoszt MP: 20","melee","on_enemy"],
        1:["rozpłatanie","self.final_damage = self.current_target.HP*0.2","zamach","graphics/skills/rozplatanie.png",250,270,0,"graphics/skills/rozplatanie_ok.png",30,"active","Rozpłatanie\nPotężny cios zadający:\naktualne 20% zrowia przeciwnika\nKoszt MP: 30","melee","on_enemy"],
        2:["cios rękojeścią","self.current_target.status.append([se.status_effect.status_list['ogluszenie'].copy(),se.Status_Icon('graphics/icons/ogluszenie_status.png','Ogłuszenie\\nCel jest ogłuszony i pomija swoją turę'),Label(font_size = 22)])\nself.final_damage = 'OGŁUSZENIE!'","zamach","graphics/skills/cios_rekojescia.png",350,270,0,"graphics/skills/cios_rekojescia_ok.png",30,"active","Ogłuszenie\nAtak obuchowy powodujący ogłuszenie\nCzas trwania: 1 tura, Pominięcie tury\nKoszt MP: 30","status","on_enemy"],
        3:["siła byka","player.current_player.STR += 5","rozpłatanie","graphics/skills/sila_byka.png",250,470,1,"graphics/skills/sila_byka_ok.png",0,"passive","Siła byka\nUMIEJĘTNOŚĆ PASYWNA\nZwiększa na stałe siłę o 5","",""],
        4:["gniew","self.current_target.status.append([se.status_effect.status_list['sila'].copy(),se.Status_Icon('graphics/icons/gniew_status.png','Gniew\\nSiła zostaje zwiększona o 10%'),Label(font_size = 22)])\nself.final_damage = 'GNIEW!'","cios rękojeścią","graphics/skills/gniew.png",350,470,2,"graphics/skills/gniew_ok.png",20,"active","Gniew\nZwiększasz na chwilę swoją siłę\nCzas trawania: 3 tury, STR+20%\nKoszt MP: 20","status","on_characters"],
        5:["ostateczny osoąd","self.final_damage = self.current_turn.STR*10","gniew","graphics/skills/ostateczny_osad.png",350,670,4,"graphics/skills/ostateczny_osad_ok.png",50,"active","Ostateczny osoąd\nCios kładący każdego na kolana zadaje:\nSTR*10\nKoszt MP: 50","melee","on_enemy"],
        
        #umiejętności maga
        6:["kula ognia","self.final_damage = 15+self.current_turn.INT*2","none","graphics/skills/kula_ognia.png",700,70,"none","graphics/skills/kula_ognia_ok.png",10,"active","Kula Ognia\nPrzemiana magi w ogień zadaje:\n15+INT*2\nKoszt MP: 10","ranged","on_enemy"],
        7:["uzdrowienie","self.final_damage = -(self.current_turn.INT*10)","kula ognia","graphics/skills/leczenie.png",700,270,6,"graphics/skills/leczenie_ok.png",15,"active","Uzdrowienie\nZaklęcie kojące rany leczy:\nINT*10\nKoszt MP: 15","heal","on_characters"],
        8:["skupienie","self.current_target.status.append([se.status_effect.status_list['inteligencja'].copy(),se.Status_Icon('graphics/icons/skupienie_status.png','Oświecenie\\nInteligencja zostaje zwiększona o 10%'),Label(font_size = 22)])\nself.final_damage = 'OŚWIECENIE!'","uzdrowienie","graphics/skills/skupienie.png",700,470,7,"graphics/skills/skupienie_ok.png",20,"active","Skupienie\nZwiększa na chwilę twoją inteligencje\nCzas trwania: 3 tury, INT+20%\nKoszt MP: 20","status","on_characters"],  
        9:["oświecenie","player.current_player.INT += 5","uzdrowienie","graphics/skills/oswiecenie.png",600,270,7,"graphics/skills/oswiecenie_ok.png",0,"passive","Oświecenie\nUMIEJĘTNOŚĆ PASYWNA\nZwiększa na stałe inteligencje o 5","",""],
        10:["zamrożenie","self.current_target.status.append([se.status_effect.status_list['zamrożenie'].copy(),se.Status_Icon('graphics/icons/zamrozenie_status.png','Zamrożenie\\nCel pomija turę i tracir 10% zdrowia'),Label(font_size = 22)])\nself.final_damage = 'ZAMROŻENIE!'","skupienie","graphics/skills/zamrozenie.png",800,470,8,"graphics/skills/zamrozenie_ok.png",60,"active","Zamrożenie\nMrążące zakęcie,powduje zamrożenie\nCzas trwania: 2 tury Pomija turę, \ni zabiera 10% zdrowia Koszt MP: 60","status","on_enemy"],
        11:["medytacja","self.current_target.MP += 50","skupienie","graphics/skills/medytacja.png",700,670,8,"graphics/skills/medytacja_ok.png",0,"active","Medytacja\nStan pozwalający odzyskać część sił\nOdnawia 50 MP\nKoszt MP: 0","ranged","on_character"],
        
        #umiejętności łotrzyka
        12:["ciche cięcie","self.final_damage = 5+self.current_turn.DEX*4","none","graphics/skills/ciche_cięcie.png",1100,70,"none","graphics/skills/ciche_cięcie_ok.png",15,"active","Ciche Cięcie\nAtak z zaskoczenia zadaje:\n5+DEX*4\nKoszt MP: 15","melee","on_enemy"],
        13:["piorun","self.final_damage = self.current_turn.INT*3 + self.current_turn.DEX*4","ciche cięcie","graphics/skills/piorun.png",1100,270,12,"graphics/skills/piorun_ok.png",20,"active","Piorun\nPołączenie magi i techniki zadaje:\nINT*3 + DEX*4\nKoszt MP: 20","ranged","on_enemy"],
        14:["akrobatyka","player.current_player.DEX += 5","piorun","graphics/skills/akrobatyka.png",1050,470,13,"graphics/skills/akrobatyka_ok.png",0,"passive","Akrobatyka\nUMIEJĘTNOŚĆ PASYWNA\nZwiększa na stałe zręczność o 5","",""],
        15:["rozgrzewka","self.current_target.status.append([se.status_effect.status_list['zrecznosc'].copy(),se.Status_Icon('graphics/icons/rozgrzewka_status.png','Rozgrzewka\\nZręczność zostaje zwiększona o 10%'),Label(font_size = 22)])\nself.final_damage = 'ROZGRZEWKA!'","piorun","graphics/skills/rozgrzewka.png",1150,470,13,"graphics/skills/rozgrzewka_ok.png",30,"active","Rozgrzewka\nNa chwilę zwiększa zręczność\nCzas trwania: 3 tury, DEX+20%\nKoszt MP: 30","status","on_characters"],
        16:["osłabienie","self.current_target.status.append([se.status_effect.status_list['osłabienie'].copy(),se.Status_Icon('graphics/icons/oslabienie_status.png','Osłabienie\\nCel zadaje połowę obrażeń'),Label(font_size = 22)])\nself.final_damage = 'OSŁABIENIE!'","akrobatyka","graphics/skills/oslabienie.png",1050,670,14,"graphics/skills/oslabienie_ok.png",40,"active","Osłabienie\nOsłabiający cios w czuły punkt\nCzas trwania: 3 tury, Przeciwnik zadaje,\npołowę obrażeń Koszt MP: 40","status","on_enemy"],
        17:["zabójca idealny","self.current_target.status.append([se.status_effect.status_list['zabójca idealny'].copy(),se.Status_Icon('graphics/icons/zabojca_idealny_status.png','Zabójca idealny\\nCel ma zwiększoną zręczność razy 20'),Label(font_size = 22)])\nself.final_damage = 'ZABÓJCA IDEALNY!'","akrobatyka","graphics/skills/zabojca_idealny.png",1150,670,14,"graphics/skills/zabojca_idealny_ok.png",50,"active","ZABÓJCA IDEALNY\nJeden cios jeden trup\nNa 1 turę mnoży zręczność razy 20\nKoszt MP: 50","status","on_character"]
        
    }

class Stat_Button(Button):
    def __init__(self,stat,**kwargs):
        super().__init__(**kwargs)
        self.stat = stat
        self.bind(on_release=self.on_toggle)

    def on_toggle(self, touch):
        if isinstance(self.last_touch, MouseMotionEvent):
            self.increase_stat()

    def increase_stat(self):
        if player.current_player.stat_points > 0:
            if self.stat == "HP":
                player.current_player.MAX_HP += 15
                player.current_player.HP +=15
            elif self.stat == "MP":
                player.current_player.MAX_MP += 10
                player.current_player.MP +=10
            elif self.stat == "STR":
                player.current_player.STR +=1
            elif self.stat == "DEX":
                player.current_player.DEX +=1
            elif self.stat == "INT":
                player.current_player.INT +=1   
            player.current_player.stat_points -=1
            UI.ui.stats_refresh(player.current_player)
        else:
            tp.text_pop.text = "Nie masz punktów statystyk"
            Clock.schedule_interval(tp.clear_pop_up,3)

skills = Skills()
skills_objects = {}