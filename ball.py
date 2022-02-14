from fps import *

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def pos(self):
        return (self.x, self.y)
    
    def move(self, x, y):
        self.x = x
        self.y = y