from kivy.core.audio import SoundLoader
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.event import EventDispatcher

class Music_Component(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas.before.clear()
        with self.canvas.before:
            self.rect = Rectangle(
                source = 'graphics/menu_background.png',
                pos=self.pos,
                size=self.size,
            )
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.orientation = "horizontal"
        self.spacing = 5
        self.padding = 20
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class Music_Player(EventDispatcher):
    volume = NumericProperty(0.6)
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.current_track = SoundLoader.load("graphics/music/stage1.wav")
        self.current_source = "graphics/music/stage1.wav" 
        self.current_track.volume = self.volume
        self.current_track.loop = True
        self.label=Label(font_size = 25, text = str(self.volume), outline_width=1)
        self.music_component = Music_Component(pos_hint={"center_x": 0.75, "y":0}, size_hint=(0.13,0.09))
        self.music_component.add_widget(Image(source="graphics/sound_icon.png", size_hint=(1,1)))
        self.music_component.add_widget(Button(on_release = lambda y:self.change_volume(-0.05), background_normal = "graphics/sound_minus_icon.png", background_down = "graphics/sound_minus_icon_press.png", size_hint=(1,1)))
        self.music_component.add_widget(self.label)
        self.music_component.add_widget(Button(on_release = lambda y:self.change_volume(0.05), background_normal = "graphics/sound_plus_icon.png",background_down = "graphics/sound_plus_icon.png_press.png", size_hint=(1,1)))
        
    def play_music(self):
        if self.current_track.state == "stop":
            self.current_track.play()

    def stop_music(self):
        self.current_track.stop()

    def change_music(self,source):
        if self.current_source == source:
            pass
        else:
            self.current_track.stop()
            self.current_track = SoundLoader.load(source)
            self.current_source = source
            self.current_track.loop = True
            self.current_track.volume = round(self.volume,2)
            self.current_track.play()
    
    def change_volume(self,value):
        self.volume += value
        if self.volume < 0.05:
            self.volume = 0.05
        if self.volume > 1.0:
            self.volume = 1.0
        self.current_track.volume = round(self.volume,2)
        self.label.text = "{:.2f}".format(self.volume)
            

music_player = Music_Player()