from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

class DynamicStageButton(Button):
    def __init__(self, x, y, s,  **kwargs):
        super(DynamicStageButton, self).__init__(**kwargs)
        self.background_normal = s
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
            size_hint_y = None,
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
        
event_companion1 = StoryEvent(0.45,0.53,"graphics/companion1_story.png","graphics/companion1_closeup.png",1,4,"companion1","self.parent.event_add_character()","Testowy Opis", "DODAJ NOEWGO CZŁONKA DRUŻYNY!")
event_companion2 = StoryEvent(0.6,0.53,"graphics/companion2_story.png","graphics/companion2_closeup.png",2,2,"companion2","self.parent.event_add_character()","Testowy Opis nr 2", "DODAJ NOEWGO CZŁONKA DRUŻYNY!")

event_dictionary = {
    "companion1": 0,
    "companion2": 0,
    }        



        