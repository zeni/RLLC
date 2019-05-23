from pyo import *


class Plant:
    def __init__(self, sound=None):
        self.sound = sound
        self.sound.mul = .1
        self.mute = False
