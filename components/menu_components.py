import player,fight, text_pop as tp, os
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.properties import NumericProperty, ObjectProperty
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.animation import Animation
from music_player import music_player

class Settings_Menu(BoxLayout):
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.canvas.before.clear()
        with self.canvas.before:
            self.rect = Rectangle(
                source = 'graphics/text_box.png',
                pos = self.pos,
                size = self.size,
            )
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.add_widget(Button(text="Wyjście z gry", outline_width=1, background_normal = 'graphics/text_box.png', background_down = 'graphics/text_box_dark.png', on_release=lambda y:self.exit()))
        self.add_widget(Button(text="Wyjście do menu", outline_width=1, background_normal = 'graphics/text_box.png', background_down = 'graphics/text_box_dark.png', on_release=lambda y:self.change_screeen("main_menu")))
        self.add_widget(Button(text="Zapisz grę", outline_width=1, background_normal = 'graphics/text_box.png', background_down = 'graphics/text_box_dark.png', on_release = lambda y:self.save_game()))
        self.text_pop = Label(text="ZAPISANO GRE", font_size=dp(35), outline_width = 1, opacity = 0)
        self.add_widget(self.text_pop)
        self.orientation = "vertical"
        self.spacing = 15
        self.padding = 15
        self.is_visible = False
        self.opacity = 0
        self.disabled = True

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def change_screeen(self, screen_name):
        self.parent.clear_widgets()
        self.manager.current = screen_name
    def exit(self):
        quit()
    def save_game(self):
        save_path = os.path.join(os.path.expanduser("~"), "save_game.txt")
        f = open(save_path,"w")
        characters = ["player.main_player","player.companion1","player.companion2"]
        for x in range(0,len(player.team)):
           f.write(characters[x]+'.head = "'+str(player.team[x].head)+'"\n')
           f.write(characters[x]+'.name = "'+str(player.team[x].name)+'"\n')
           f.write(characters[x]+'.lv = '+str(player.team[x].lv)+'\n')
           f.write(characters[x]+'.MAX_HP = '+str(player.team[x].MAX_HP)+'\n')
           f.write(characters[x]+'.MAX_MP = '+str(player.team[x].MAX_MP)+'\n')
           f.write(characters[x]+'.MP_regen_base = '+str(player.team[x].MP_regen_base)+'\n')
           f.write(characters[x]+'.HP = '+str(player.team[x].HP)+'\n')
           f.write(characters[x]+'.MP = '+str(player.team[x].MP)+'\n')
           f.write(characters[x]+'.STR_base = '+str(player.team[x].STR_base)+'\n')
           f.write(characters[x]+'.DEX_base = '+str(player.team[x].DEX_base)+'\n')
           f.write(characters[x]+'.INT_base = '+str(player.team[x].INT_base)+'\n')
           f.write(characters[x]+'.weapon = '+str(player.team[x].weapon)+'\n')
           f.write(characters[x]+'.damage_base = '+str(player.team[x].STR_base+player.team[x].weapon)+'\n')
           f.write(characters[x]+'.defence_base = '+str(player.team[x].defence_base)+'\n')
           f.write(characters[x]+'.crit_chance_base = '+str(player.team[x].DEX*0.01)+'\n')
           f.write(characters[x]+'.dodge_chance_base = '+str(player.team[x].DEX*0.02)+'\n')
           f.write(characters[x]+'.crit_chance_bonus = '+str(player.team[x].crit_chance_bonus)+'\n')
           f.write(characters[x]+'.dodge_chance_bonus = '+str(player.team[x].dodge_chance_bonus)+'\n')
           f.write(characters[x]+'.EXP_boost = '+str(player.team[x].INT*0.01)+'\n')
           f.write(characters[x]+'.EXP = '+str(player.team[x].EXP)+'\n')
           f.write(characters[x]+'.EXP_To_Lv = '+str(player.team[x].EXP_To_Lv)+'\n')
           f.write(characters[x]+'.stat_points = '+str(player.team[x].stat_points)+'\n')
           f.write(characters[x]+'.skill_points = '+str(player.team[x].skill_points)+'\n')
           f.write(characters[x]+'.potions = '+str(player.team[x].potions)+'\n')
           f.write(characters[x]+'.potion_effect = "'+str(player.team[x].potion_effect)+'"\n')
           f.write(characters[x]+'.current_potions = '+str(player.team[x].current_potions)+'\n')
           f.write(characters[x]+'.potion_description = "'+str(player.team[x].potion_description)+'"\n')
           for y in player.team[x].skill:
               temp = str(player.team[x].skill[y][3]).replace("\n","\\n")
               temp2 = str(player.team[x].skill[y][0]).replace("\n","\\n")
               f.write(characters[x]+'.skill["'+y+'"] = ["'+temp2+'",'+str(player.team[x].skill[y][1])+',"'+str(player.team[x].skill[y][2])+'","'+temp+'","'+str(player.team[x].skill[y][4])+'","'+str(player.team[x].skill[y][5])+'","'+str(player.team[x].skill[y][6])+'","'+str(player.team[x].skill[y][7])+'","'+str(player.team[x].skill[y][8])+'"]\n')
           f.write(characters[x]+'.inventory["main_hand"][2] = "'+str(player.team[x].inventory["main_hand"][2])+'"\n')
           f.write(characters[x]+'.inventory["off_hand"][2] = "'+str(player.team[x].inventory["off_hand"][2])+'"\n')
           f.write(characters[x]+'.inventory["armor"][2] = "'+str(player.team[x].inventory["armor"][2])+'"\n')
           f.write(characters[x]+'.inventory["accessory"][2] = "'+str(player.team[x].inventory["accessory"][2])+'"\n')
           f.write(characters[x]+'.inventory["accessory2"][2] = "'+str(player.team[x].inventory["accessory2"][2])+'"\n')
           f.write(characters[x]+'.inventory["accessory3"][2] = "'+str(player.team[x].inventory["accessory3"][2])+'"\n')
           f.write(characters[x]+'.inventory["potion"][2] = "'+str(player.team[x].inventory["potion"][2])+'"\n')
        for x in range(0,48):
            f.write('player.main_player.inventory['+str(x)+'][2] = "'+(player.current_player.inventory[x][2])+'"\n')
        f.write("fight.stage1_progress="+str(fight.stage1_progress)+"\n")
        f.write("fight.stage2_progress="+str(fight.stage2_progress)+"\n")
        f.write("fight.current_fight="+str(fight.current_fight)+"\n")
        f.write("fight.current_stage="+str(fight.current_stage)+"\n")
        if len(player.team)>=2:
            f.write("player.team.append(player.companion1)\n")
        if len(player.team)>=3:
            f.write("player.team.append(player.companion2)\n")
        f.write("player.gold = "+str(player.gold))
        for key in event_dictionary.keys():
            f.write("\nevent_dictionary['"+str(key)+"'] = "+str(event_dictionary[key]))
        for key in player.main_player.story_items.keys():
            f.write("\nplayer.main_player.story_items['"+str(key)+"'][0] = "+str(player.main_player.story_items[key][0]))
        f.close()
        self.show_message()

    def clear_pop_up(self, dt):
        self.text_pop.text = ""

    def show_message(self):
        self.text_pop.opacity = 0

        anim = (
            Animation(opacity=1, duration=0.4) +
            Animation(duration=2.0) +
            Animation(opacity=0, duration=0.5)
        )
        anim.start(self.text_pop)
    

class DynamicStageButton(Button):
    scale = NumericProperty(1.0)
    action = ObjectProperty(None, allownone=True)

    def __init__(self, x, y, s, s_d,  **kwargs):
        self.action = kwargs.pop('action', None)
        super(DynamicStageButton, self).__init__(**kwargs)
        self.background_normal = s
        self.background_down = s_d
        self.border = (0,0,0,0)
        self.pos_hint = {"center_x": x, "center_y": y}
        self.size = (dp(150),dp(150))
        self.size_hint = (None, None)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class StoryEvent(Button):
    def __init__(self, x, y, s, s_closeup, stage, fight, name, action, description, button_description, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = s
        self.background_closeup = s_closeup
        self.border = (0,0,0,0)
        self.size = (dp(180),dp(250))
        self.pos_hint = {"center_x": x, "center_y": y}
        self.size_hint = (None, None)
        self.is_happend = False
        self.which_stage = stage
        self.which_fight = fight
        self.story_event_name = name
        self.action = action
        self.description = description
        self.button_description = button_description

        content = BoxLayout(orientation='horizontal', padding=30, spacing=5)
        text_box = BoxLayout(orientation='vertical', padding=20, spacing=25)

        image = Image(
            source = self.background_closeup,
            size = (dp(25),dp(25)),
            allow_stretch = True,
        )

        label = Label(
            text = self.description,
            size_hint_y = None,
            height = dp(200),
            text_size = (dp(400), None),
            font_size = 23,
            halign = 'center',
            valign = 'middle',
        )

        close_button = Button(
            text = self.button_description or "OK",
            size_hint_y = 0.8,
            height= dp(60),
            background_normal="graphics/target_button.png",
        )

        self.popup = Popup(
            title = '',
            content=content,
            size_hint = (None, None),
            size = (dp(500), dp(400)),
            auto_dismiss = True,
            separator_color = (0,0,0,0),
            background = 'graphics/text_box.png',
        )

        text_box.add_widget(label)
        text_box.add_widget(close_button)

        content.add_widget(image)
        content.add_widget(text_box)

        close_button.bind(on_press=self.execute_action)

        self.bind(on_press=self.show_popup)

    def show_popup(self, instance):
        self.popup.open()

    def execute_action(self, instance):
        self.is_happend = True
        event_dictionary[self.story_event_name] = 1
        self.popup.dismiss()
        exec(self.action)

    def is_event_expired(self):
        if self.is_happend == True:
            return True
        else:
            return False
        
event_companion1 = StoryEvent(0.45,0.53,"graphics/companion1_story.png","graphics/companion1_closeup.png",1,4,"companion1","self.parent.event_add_character()","Ah! Jak dobrze ujrzeć jakąś przyjazną twarz w tym zapomnianym przez boga miejscu. Może przyłączę się do ciebie i razem odnajdziemy wyjście z tego przeklętego lochu?", "DODAJ NOEWGO CZŁONKA DRUŻYNY!")
event_companion2 = StoryEvent(0.6,0.53,"graphics/companion2_story.png","graphics/companion2_closeup.png",2,2,"companion2","self.parent.event_add_character()","Witajcie dzielni wojownicy! Spotkanie tutaj innego człowieka, który nie jest stertą kości graniczy z cudem. Co wy na to abym się do was przyłączył i we trzech będziemy stawiać czoła przeciwnością tego lochu?", "DODAJ NOEWGO CZŁONKA DRUŻYNY!")

event_dictionary = {
    "companion1": 0,
    "companion2": 0,
    }        


        