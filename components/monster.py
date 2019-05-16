from pyo import *

class Monster:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        #self.sound=sound
        #self.sound.mul=.1