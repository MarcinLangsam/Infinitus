from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from tooltip import set_tooltip_status, clear_tooltip
from kivy.core.window import Window
from kivy.graphics import Line, Color, Rectangle

class HPBar(ProgressBar):
    pass
class MPBar(ProgressBar):
    pass
class EnemyHPBar(ProgressBar):
    pass
class Skill_List_Pop_Up(BoxLayout):
    list = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class StatusIcon(Image):
    def __init__(self, text, source, description, **kwargs):
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(StatusIcon, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(35), dp(35))
        self.source = source
        self.t = text
        self.description = description

        self.label = Label(
            text=self.t,
            size_hint=(None, None),
            size=(dp(35), dp(35)),
            pos=(self.x + (self.width - dp(35)) / 2, self.y + (self.height - dp(35)) / 2),
            font_size=20,
            halign='center',
            valign='middle',
            text_size=(dp(35), dp(35))
        )
        self.add_widget(self.label)

        self.bind(pos=self.update_label_pos, size=self.update_label_pos)

    def update_label_pos(self, *args):
        self.label.pos = (
            self.x + (self.width - self.label.width) / 2,
            self.y + (self.height - self.label.height) / 2
        )

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        Clock.unschedule(self.display_tooltip)
        self.close_tooltip()
        if self.collide_point(*self.to_widget(*pos)):
            self.p = self.pos
            Clock.schedule_once(self.display_tooltip, 0.5)

    def close_tooltip(self, *args):
        clear_tooltip(self.parent.tooltip)
    def display_tooltip(self, *args):
        set_tooltip_status(self.parent.tooltip, self.description, self.p)

class StatusIconContainer(BoxLayout):
    def __init__(self, tooltip, **kwargs):
        super(StatusIconContainer, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.padding = 0
        self.spacing = 0
        self.icons_list = list()
        self.tooltip = tooltip

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def draw_all_icons(self, status_list):
        self.clear_widgets()
        for status in status_list:
            self.add_widget(StatusIcon( str(status[0][2]),
                                        status[0][3],
                                        status[0][6]
                                    )
                            )
            
class NameContainer(Label):
    def __init__(self, name, **kwargs):
        super(NameContainer, self).__init__(**kwargs)
        self.canvas.before.clear()
        with self.canvas.before:
            self.rect = Rectangle(
                source='graphics/name_holder.png',
                pos=self.pos,
                size=self.size,
            )
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.text = name

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class PlayerStatusContainer(BoxLayout):
    def __init__(self, player, tooltip, **kwargs):
        super(PlayerStatusContainer, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint = (0.18, 0.178)
        self.height = self.minimum_height
        self.padding = 0
        self.spacing = 0
        self.tooltip = tooltip
        self.player = player
        
        self.hp_portrait_mp_container = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 6/10),
            padding=0,
            spacing=0
        )

        self.portrait = Image(
            source=f'graphics/sprites/{self.player.head}_portrait.png',
            size_hint=(1/3, 1),
            allow_stretch=True,
            keep_ratio=False
        )
        self.hp_portrait_mp_container.add_widget(self.portrait)

        self.hp_bar = HPBar(
            max=self.player.MAX_HP,
            value=self.player.HP,
            size_hint=(1/3, 1),
        )
        self.hp_portrait_mp_container.add_widget(self.hp_bar)

        self.mp_bar = MPBar(
            max=self.player.MAX_MP,
            value=self.player.MP,
            size_hint=(1/3, 1),
        )
        self.hp_portrait_mp_container.add_widget(self.mp_bar)

        self.add_widget(self.hp_portrait_mp_container)

        self.name_container = NameContainer(
            self.player.name,
            size_hint=(1, 2/10),
        )
        self.add_widget(self.name_container)
        self.status_icons = StatusIconContainer(
            self.tooltip,
            size_hint=(1, 2/10),
        )
        self.add_widget(self.status_icons)

        self.bind(minimum_height=self.setter('height'))

    def show_border(self):
        with self.hp_portrait_mp_container.canvas.before:
            Color(0.8,0,0,0.75)
            self.border = Line(
                rectangle=(self.hp_portrait_mp_container.x, self.hp_portrait_mp_container.y, self.hp_portrait_mp_container.width, self.hp_portrait_mp_container.height),
                width=6
            )
    def hide_border(self):
        self.hp_portrait_mp_container.canvas.before.clear()

    def update_bars(self):
        self.hp_bar.max = self.player.MAX_HP
        self.hp_bar.value = self.player.HP

        self.mp_bar.max = self.player.MAX_MP
        self.mp_bar.value = self.player.MP

class EnemyStatusContainer(BoxLayout):
    def __init__(self, enemy, tooltip, **kwargs):
        super(EnemyStatusContainer, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint = (0.115, 0.17)
        self.height = self.minimum_height
        self.padding = 0
        self.spacing = 0
        self.tooltip = tooltip
    
        self.enemy = enemy

        self.hp_portrait_mp_container = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 6/10),
            height=dp(100),
            padding=0,
            spacing=0
        )

        self.portrait = Image(
            source=f'graphics/sprites/{self.enemy.source}_portrait.png',
            size_hint=(1/3, 1),
            allow_stretch=True,
            keep_ratio=False
        )
        self.hp_portrait_mp_container.add_widget(self.portrait)

        self.hp_bar = HPBar(
            max=self.enemy.MAX_HP,
            value=self.enemy.HP,
            size_hint=(1/3, 1),
        )
        self.hp_portrait_mp_container.add_widget(self.hp_bar)

        self.add_widget(self.hp_portrait_mp_container)

        self.name_container = NameContainer(
            self.enemy.name,
            size_hint=(1, 2/10),
        )
        self.add_widget(self.name_container)

        self.status_icons = StatusIconContainer(
            self.tooltip,
            size_hint=(1, 2/10),
        )
        self.add_widget(self.status_icons)

        self.bind(minimum_height=self.setter('height'))

    def show_border(self):
        with self.hp_portrait_mp_container.canvas.before:
            Color(0.8,0,0,0.75)
            self.border = Line(
                rectangle=(self.hp_portrait_mp_container.x, self.hp_portrait_mp_container.y, self.hp_portrait_mp_container.width, self.hp_portrait_mp_container.height),
                width=6
            )
    def hide_border(self):
        self.hp_portrait_mp_container.canvas.before.clear()

    def update_bars(self):
        self.hp_bar.max = self.enemy.MAX_HP
        self.hp_bar.value = self.enemy.HP

