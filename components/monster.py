from pyo import *


class Monster:
    def __init__(self, sound=None):
        self.sound = sound
        self.sound.mul = .1
