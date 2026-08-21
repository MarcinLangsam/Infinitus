from kivy.uix.button import Button
from kivy.properties import NumericProperty, ObjectProperty
from kivy.animation import Animation
from kivy.lang import Builder

class FancyButton(Button):
    scale = NumericProperty(1.0)
    action = ObjectProperty(None, allownone=True)


    def __init__(self, **kwargs):
        self.action = kwargs.pop('action', None)
        super().__init__(**kwargs)
        self.background_down = self.background_normal
        self.border = (0,0,0,0)
        self.bind(on_press=self._on_press)
        self.bind(on_release=self._on_release)
        self.bind(on_cancel=self._on_release)

    def _on_press(self, instance):
        Animation.cancel_all(self)
        Animation(scale=0.92, opacity=0.75, duration=0.02).start(self)
        
    def _on_release(self, instance):
        Animation.cancel_all(self)
        anim = Animation(scale=1.0, opacity=1.0, duration=0.03)

        if self.action:
            anim.bind(on_complete=lambda *a: self.action(self))

        anim.start(self)
