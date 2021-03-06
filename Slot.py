from tkinter import *
class Slot(object):
    def __init__(self, number=0, numPlayers=1):
        self.color = 'white'
        self.x, self.y = 0,480
        self.num = number
        self.numPlayers = numPlayers
        
        #player 1
        if(self.num == 0):
            self.color = 'firebrick1'
            self.x = 100
        elif(self.num == 1):
            self.color ='DodgerBlue2'
            self.x = 200
        elif(self.num == 2):
            self.color= 'yellow2'
            self.x = 300
        elif(self.num == 3):
            self.color = 'green2'
            self.x = 400
            
        #player 2
        if(self.num == 4):
            self.color = 'firebrick1'
            self.x = 600
        elif(self.num == 5):
            self.color ='DodgerBlue2'
            self.x = 700
        elif(self.num == 6):
            self.color= 'yellow2'
            self.x = 800
        elif(self.num == 7):
            self.color = 'green2'
            self.x = 900
        
    def draw(self, canvas):
        canvas.create_rectangle(self.x-30, self.y-10,
                                self.x+30, self.y+10,
                                fill = self.color)
                                
    def overlap(self, x,y):
        if(x== self.x and (y >= self.y-20 and y <= self.y+20)):
            return True
        return False