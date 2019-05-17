from pyo import *

class Noiseur:
    def __init__(self, hp, defense, power,sound=None):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.sound=sound
        self.sound.mul = .2
    
    def add_osc(self, f):
        self.sound+=Sine(freq=f)