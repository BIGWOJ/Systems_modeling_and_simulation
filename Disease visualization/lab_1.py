import numpy as np
import matplotlib.pyplot as plt
import random

# Miejsce narodzenia nowego może być losowe, nie musi być w tym miejscu gdzie rodzice się znaleźli
class Person:
    def __init__(self, x, y, speed, direction, state, age, immunity):
        self.x = random.randint(0, 250)
        self.y = random.randint(0, 250)
        self.speed = random.randint(1, 3)
        self.direction = random.choice(['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE'])
        self.state = 'healthy'
        self.age = 0
        self.immunity = set_immunity(self)

    def set_immunity(self):
        if self.age < 15 or self.age >= 70:
            self.immunity = 'low'
        elif 40 <= self.age < 70:
            self.immunity = 'medium'
        else:
            return 'strong'

    def move(self):
        # x cordinate
        if self.direction in ['E', 'NE', 'SE']:
            self.x += self.x * self.speed
        if self.direction in ['W', 'NW', 'SW']:
            self.x -= self.x * self.speed

        # y cordinate
        if self.direction in ['S', 'SW', 'SE']:
            self.y -= self.y * self.speed
        if self.direction in ['N', 'NW', 'NE']:
            self.y += self.y * self.speed


