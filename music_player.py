from kivy.core.audio import SoundLoader
from kivy.properties import NumericProperty
from kivy.event import EventDispatcher

class Music_Player(EventDispatcher):
    volume = NumericProperty(0.6)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.current_track = SoundLoader.load("graphics/music/stage1.wav")
        self.current_source = "graphics/music/stage1.wav" 
        self.current_track.volume = self.volume
        self.current_track.loop = True

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
            self.current_track.play()
            

music_player = Music_Player()