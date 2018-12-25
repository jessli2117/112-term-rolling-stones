
from tkinter import *
class Button(object):
    def __init__(self,x,y, currentMode=''):
        self.x = x
        self.y = y
        self.height = 30
        self.width = 30
        self.mode = currentMode
        self.color = 'blue'
        
    def draw(self, canvas):
        canvas.create_rectangle(self.x-self.width, self.y-self.height,
                                self.x+self.width, self.y+self.height,
                                fill = self.color, width = 5, 
                                outline = 'white')
        canvas.create_text(self.x, self.y, fill = 'white', text = self.mode)
        
    def isSwitch(self,x,y):
        if(x <= self.x+self.width and x >= self.x-self.width):
            if(y <= self.y+self.height and y >= self.y-self.height):
                return True                
        return False
        
class StartButton(Button):
    def __init__(self,x,y, fill = 'white'):
        super().__init__(x,y,'START')
        self.fill = fill
    
    def draw(self, canvas):       
        self.width = 100
        self.height = 25                         
        canvas.create_text(self.x, self.y, 
                        fill = self.fill, text = self.mode,
                        font = 'Franklin 30')

class BackButton(Button):
    def __init__(self,x,y):
        super().__init__(x,y,'Back')
        
    def draw(self, canvas):
        self.height = 20
        self.width = 20
        canvas.create_rectangle(self.x-self.width, self.y-self.height,
                                self.x+self.width, self.y+self.height,
                                fill = 'PaleVioletRed1')
        canvas.create_text(self.x, self.y, 
                        fill = "white", text = '←',
                        font = 'Franklin 35 bold')

class RetryButton(Button): 
    def __init__(self,x,y):
        super().__init__(x,y,'Retry')
        
    def draw(self, canvas):
        self.height = 20
        self.width = 20
        canvas.create_rectangle(self.x-self.width, self.y-self.height,
                                self.x+self.width, self.y+self.height,
                                fill = 'NavajoWhite2')
        canvas.create_text(self.x, self.y, 
                        fill = "white", text = '∞',
                        font = 'Franklin 35 bold')

class HelpButton(Button):
    def __init__(self,x,y):
        super().__init__(x,y,'Help')
    
    def draw(self, canvas):
        self.height = 20
        self.width = 20
        canvas.create_rectangle(self.x-self.width, self.y-self.height,
                                self.x+self.width, self.y+self.height,
                                fill = 'sienna1')
        canvas.create_text(self.x, self.y, 
                        fill = "white", text = '?',
                        font = 'Franklin 30 bold')

class AddScreenButton(Button):
    def __init__(self,x,y):
        super().__init__(x,y,'AddScreen')
    
    def draw(self, canvas):
        self.height = 20
        self.width = 20
        canvas.create_rectangle(self.x-self.width, self.y-self.height,
                                self.x+self.width, self.y+self.height,
                                fill = 'palegreen3')
        canvas.create_text(self.x, self.y, 
                        fill = "white", text = '+',
                        font = 'Franklin 40 bold')
        
class AddButton(Button):
    def __init__(self,x,y):
        super().__init__(x,y,'Add')
        
    def draw(self, canvas):
        self.height = 20
        self.width = 20
        canvas.create_rectangle(self.x-self.width, self.y-self.height,
                                self.x+self.width, self.y+self.height,
                                fill = 'palegreen3')
        canvas.create_text(self.x, self.y, 
                        fill = "white", text = '+',
                        font = 'Franklin 40 bold')
                        
class oneButton(Button):
    def __init__(self,x=500,y=150):
        super().__init__(x,y,'ONE')
        
    def draw(self, canvas):
        self.height = 100
        self.width = 200
        canvas.create_rectangle(self.x-self.width, self.y-self.height,
                                self.x+self.width, self.y+self.height,
                                fill = 'LightSkyBlue1', outline = 'white',
                                width = 10)
        canvas.create_text(self.x-5, self.y, 
                        fill = "grey60", text = 'ONE',
                        font = 'Franklin 70 bold')
        canvas.create_text(self.x+5, self.y, 
                        fill = "black", text = 'ONE',
                        font = 'Franklin 70 bold')
                        
class twoButton(Button):
    def __init__(self,x=750,y=150):
        super().__init__(x,y,'TWO')
        
    def draw(self, canvas):
        self.height = 100
        self.width = 200
        canvas.create_rectangle(self.x-self.width, self.y-self.height,
                                self.x+self.width, self.y+self.height,
                                fill = 'lavender', outline = 'white',
                                width = 10)
        canvas.create_text(self.x-5, self.y, 
                        fill = "grey60", text = 'TWO',
                        font = 'Franklin 70 bold')
        canvas.create_text(self.x+5, self.y, 
                        fill = "black", text = 'TWO',
                        font = 'Franklin 70 bold')
        
class HighScoreButton(Button):
    def __init__(self,x,y,fill = 'white'):
        super().__init__(x,y,'Scoreboard')
        self.fill = fill
    def draw(self, canvas):
        self.height = 25
        self.width = 150
        canvas.create_text(self.x, self.y, 
                        fill = self.fill, text = 'SCOREBOARD',
                        font = 'Franklin 30')

    
class SoundButton(Button):
    def __init__(self,x,y):
        super()._init_(x,y,'Sound')
    