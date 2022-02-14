class Player:
    def __init__(self, x, y, shirt_number):
        self.x = x
        self.y = y
        self.shirt_number = shirt_number
        
    def move(self, x, y):
        self.x = x
        self.y = y
        
    def pos(self):
        return (self.x, self.y)
    
    def shirt_num(self):
        return self.shirt_number