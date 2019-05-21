from pyo import *


class Noiseur:
    def __init__(self, sound=None):
        self.sound = []
        if sound is not None:
            self.sound.append(sound)
            self.sound[-1].mul = 0

    def add_osc(self, f):
        self.sound.append(Sine(freq=f))
        self.sound[-1].mul = .2
        self.sound[-1].out()

    def sound_out(self):
        for s in self.sound:
            s.out()
