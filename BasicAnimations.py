####BASIC LAYOUT
#### Jessica Li (jli6) 
import random ,os, copy
import pyaudio
import wave
import _thread
import threading
from array import array
from struct import pack
from tkinter import *
from Button import *
from Note import *
from Slot import *
# from playGame import playGame
    

#using code from hw6: targetsGame
####################################
# init
####################################

#for the scoreboard
def readScoreboard(file, scoreboard):
    File = open(file, 'r') 
    for line in File: 
        nameScore = line.split(' ')
        score, name = int(nameScore[1]), nameScore[0]
        scoreboard.append((score,name))
    return scoreboard

def readText(file):
    song = []
    File = open(file, 'r') 
    for line in File:
        second = line.split(',')
        second[0] = second[0][1]
        lastElem = second[len(second)-1]
        n1 = lastElem.strip('\n')
        n2 = n1.strip(']')
        second[len(second)-1] = n2
        temp = []
        for element in second:
            if(element == "'"):
                temp.append(1)
            elif(element == ' '):
                
                temp.append(0)
            else:
                temp.append(int(element))
        song.append(temp)
    return song

#recursive method similar to lab 10
#creates the levels
def readLevels(levels,level, path):
    if (os.path.isdir(path) == False):
        # if('song' in path):
        #     level.insert(1,path)
        if('text' in path):
            level.insert(0,path)        
    else:
        #goes through all of the files in the directory
        for filename in os.listdir(path):
            newPath = path + "/" + filename
            #if the name of the file is a directory of level
            readLevels(levels,level,newPath)
            if(len(level) == 1):
                permLevel = copy.deepcopy(level)
                levels.append(permLevel)
                level[:] = []            
    return levels
    
def readSongs(path,songs):
    if (os.path.isdir(path) == False):
        songs.append(path)        
    else:
        #goes through all of the files in the directory
        for filename in os.listdir(path):
            newPath = path + "/" + filename
            readSongs(newPath, songs)    
    return songs
    
def readNotes(data,levels,notes, counter):
    if (counter == len(levels)):
        data.allSongs = notes
    else:
        #goes through all of the levels
        textFile = levels[counter][0]
        #print(readText(textFile))
        notes.append(readText(textFile))
        readNotes(data,levels,notes, counter+1)
    
def init(data):
    # There is only one init, not one-per-mode
    data.mode = "start"
    data.score = 0
    data.numPlayers = 1
    data.countdown = 5
    data.timerDelay = 10 #10000 is a second
    data.levels = readLevels([], [], 'gameFiles')
    #allSongs is a 3D list: a list with songs (that are 2D lists themselves)
    data.allSongs = []
    readNotes(data,data.levels, [], 0)
    data.scoreboard = readScoreboard('gameFiles\scoreboard.txt', [])
    
    #actual music
    data.songs = readSongs('songs',[])
    
    #aesthetics
    data.startTimer = 0
    data.startScreenNotes = []
    data.endTimer = 0

    ##BUTTONS
    #start screen buttons
    data.start = StartButton(data.width//2, data.height//2+50)
    data.help = HelpButton(data.width-50, 50)
    data.addScreen = AddScreenButton(50, 50)
    #choice screen buttons
    data.one = oneButton(250,300)
    data.two = twoButton(750,300)
    data.backChoice = BackButton(50,50)
    #help screen buttons
    data.backHelp = BackButton(50,50)
    #end screen buttons
    data.retry = RetryButton(50,50)
    if(data.numPlayers == 1):
        data.highScore = HighScoreButton(data.width//2, data.height//2+50)
    #scoreboard screen buttons
    data.backScore = BackButton(50,50)
    #add screen buttons    
    data.backAdd = BackButton(50,50)
    data.add = AddButton(data.width-50, 50)
    
    ##SLOTS
    #one player
    data.rslot = Slot(0)
    data.bslot = Slot(1)
    data.yslot = Slot(2)
    data.gslot = Slot(3)
    
    #two player
    data.r1slot = Slot(0)
    data.b1slot = Slot(1)
    data.y1slot = Slot(2)
    data.g1slot = Slot(3)
    data.r2slot = Slot(4)
    data.b2slot = Slot(5)
    data.y2slot = Slot(6)
    data.g2slot = Slot(7)
    
    ##GENERAL GAME 
    data.countdown = 5 #the game countdown til it reaches game over
                        #every five circles the a second is added back
    data.timerCounter = 0 #starts off with no seconds
    data.musicPaused = False
    data.timerCounter = 0
    data.currentLevel = 0
    data.notes = data.allSongs[data.currentLevel]
    data.currentNotes = []
    
    #two player
    data.currentNotesP1 = []
    data.currentNotesP2 = []
    data.scoreP1 = 0
    data.scoreP2 = 0

    ##ADD SCREEN OPTIONS
    data.rows = 60
    data.cols = 4
    data.selection = (-1,-1)
    
    data.createNotes = []
    for row in range(data.rows):
        notes = [0,0,0,0]
        security = copy.copy(notes)
        data.createNotes.append(security)
            
    data.marginX = data.width//4
    data.marginY = 10

###### START SCREEN
def startMousePressed(event, data):
    if(data.start.isSwitch(event.x, event.y)):
        data.mode = 'choice'
    elif(data.help.isSwitch(event.x, event.y)):
        data.mode = 'help'
    elif(data.addScreen.isSwitch(event.x, event.y)):
        data.mode = 'add'
    
def startKeyPressed(event,data):
    pass
    
def startTimerFired(data):
    for note in data.startScreenNotes:
        if(note.y > data.height):
            data.startScreenNotes.remove(note)
        else: 
            note.y += 20

    if(data.start.fill == 'white'):
        data.start.fill = 'PeachPuff2'
    else:
        data.start.fill = 'white'

    num = random.randint(0,7)
    data.startScreenNotes.append(Note(num))
    

    #threadStartSong('startsong.wav')
    
def startRedrawAll(canvas,data):
    #Background Color
    canvas.create_rectangle(0,0, data.width, data.height, fill = "black")

    #aesthetic notes
    for note in data.startScreenNotes:
        note.draw(canvas)

    #Create the intro text
    canvas.create_text(data.width//2, data.height//2 + 30, 
                        fill = 'DeepSkyBlue2', anchor='s',
                        text= 'ROLLING STONES', font = 'Franklin 80 bold')
    canvas.create_text(data.width//2+10, data.height//2 +30, 
                        fill = "salmon", anchor='s',
                        text= 'ROLLING STONES', font = 'Franklin 80 bold')
    canvas.create_text(data.width//2+20, data.height//2+30, 
                        fill = 'white', anchor='s',
                        text= 'ROLLING STONES', font = 'Franklin 80 bold')
    
    #Creates the buttons
    data.start.draw(canvas)
    data.help.draw(canvas)
    data.addScreen.draw(canvas)

###### HELP SCREEN
def helpMousePressed(event, data):
    if(data.backHelp.isSwitch(event.x,event.y)):
        data.mode = 'start'

def helpKeyPressed(event, data):
    pass
    
def helpTimerFired(data):
    pass
    
def helpRedrawAll(canvas, data):
    explanation = ('\t\t\t\tINSTRUCTIONS:\n\n'
                    'SOLO PLAYER: \n'
                    'Use the "ASDF" keys with respective slots (left to right).'
                    'When the notes (the stones) come down\n' 
                    'and hit the slots at\n'
                    'the exact moment, \npress the keys and gain points.\n'
                    'There will be one point per block\n\n'
                    'TWO-PLAYER: \n'
                    'Person 1: Use "ASDF" keys\n'
                    'Person 2: Use "HJKL" keys\n'
                    'Everything else is the same\n\n'
                    'ADD SCREEN: \n'
                    'Levels can be permantly added to the game with the add'
                    'screen. (+ button)\n'
                    'The boxes are the notes that will come down.\n'
                    'Use back button to reset and not add a level'
                    )
                
    #create background
    canvas.create_rectangle(0,0, data.width, data.height, fill = 'black')
    
    #create text
    canvas.create_text(data.width//2-2, data.height//2, font='Century 14 bold',
                        fill = 'white', text = explanation)
                        
    data.backHelp.draw(canvas)

###### CHOICE SCREEN
def choiceMousePressed(event, data):
    if(data.backChoice.isSwitch(event.x,event.y)):
        data.mode = 'start'
    elif(data.one.isSwitch(event.x,event.y)):
        data.numPlayers = 1
        data.mode = 'one'
    elif(data.two.isSwitch(event.x,event.y)):
        data.numPlayers = 2
        data.mode = 'two'
        
def choiceKeyPressed(event, data):
    pass
    
def choiceTimerFired(data):
    pass
    
def choiceRedrawAll(canvas, data):
    #create background
    canvas.create_rectangle(0,0, data.width, data.height, fill = 'black')
    
    #create text
    canvas.create_text(data.width//2-5, data.height//5,font='Franklin 60 bold',
                        fill = 'salmon', text = 'PICK A MODE')
    canvas.create_text(data.width//2+5, data.height//5, font='Franklin 60 bold',
                        fill = 'white', text = 'PICK A MODE')
    
    data.backChoice.draw(canvas)
    data.one.draw(canvas)
    data.two.draw(canvas)
    
###### END SCREEN
def endMousePressed(event,data):    
    if(data.retry.isSwitch(event.x,event.y)):
        for i in range(len(data.scoreboard)):
            person = data.scoreboard[i]
            if(person[1] == 'you'):
                newName = 'person%d' %(len(data.scoreboard))
                data.scoreboard[i] = (person[0],newName)
        
        file = open('gameFiles\scoreboard.txt', 'w')
        for person in data.scoreboard:
            text = person[1] + ' ' + str(person[0])
            file.write(text + '\n')
        file.close()
        init(data)
    elif(data.highScore.isSwitch(event.x,event.y)):
        data.mode = 'scoreboard'
                
def endKeyPressed(event, data):
    pass
        
def endTimerFired(data):
    if(data.highScore.fill == 'white'):
        data.highScore.fill = 'blue4'
    else:
        data.highScore.fill = 'white'
    
    
def endRedrawAll(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill = 'black')
    #game over text
    canvas.create_text(data.width//2, data.height//2-10, 
                        fill = "red4", anchor='s',
                        text= 'GAME OVER', font = 'Franklin 80 bold')
    canvas.create_text(data.width//2+10, data.height//2-10, 
                        fill = 'indian red', anchor='s',
                        text= 'GAME OVER', font = 'Franklin 80 bold')
    #display score
    if(data.numPlayers == 1):
        canvas.create_text(data.width//2, data.height//2+30, 
                        fill = 'indian red', anchor='s',
                        text= 'SCORE: %d' %(data.score), 
                        font = 'Franklin 30')
    else:
        winner = ''
        if(data.scoreP1 > data.scoreP2):
            winner = 'PLAYER1'
        elif(data.scoreP1 < data.scoreP2):
            winner = 'PLAYER2'
        else:
            winner = 'TIE'
            
        canvas.create_text(data.width//2, data.height//2+30, 
                        fill = 'OrangeRed2', anchor='s',
                        text= 'WINNER: %s' %(winner), 
                        font = 'Franklin 30')
                        
    data.retry.draw(canvas)
    
    if(data.numPlayers == 1):
        data.highScore = HighScoreButton(data.width//2, data.height//2+50)
        data.highScore.draw(canvas)
    
###### SCOREBOARD SCREEN 
def scoreboardMousePressed(event,data):
    if(data.backScore.isSwitch(event.x, event.y)):
        data.mode = 'end'
    
def scoreboardTimerFired(data):
    pass
    
def scoreboardKeyPressed(event,data):
    pass
    
def scoreboardRedrawAll(canvas, data):
    #background + general text
    canvas.create_rectangle(0,0, data.width, data.height, fill = 'black')
    canvas.create_text(data.width//2, data.height//8 +30, 
                        fill = "SkyBlue4", anchor='s',
                        text= 'HIGHEST SCORES', font = 'Franklin 60 bold')
    canvas.create_text(data.width//2+10, data.height//8+30, 
                        fill = 'SkyBlue2', anchor='s',
                        text= 'HIGHEST SCORES', font = 'Franklin 60 bold')
    
    #creates the scoreboard
    increment = data.height//4
    spaces = ' '*40
    if(len(data.scoreboard) < 5):
        for i in range(len(data.scoreboard)):
            person = data.scoreboard[i]
            nowText='\n\t\t\t%d. %s %s %s'%(i+1, person[1],spaces,person[0])
            canvas.create_text(data.width//4,increment, text = nowText, 
                                font = 'Arial 30 bold',fill='white')
            increment += 40
    else:
        limit = 0,5
        for c in range(5):
            person = data.scoreboard[c]
            nowText='\n\t\t\t%d. %s %s %s' %(c+1,person[1],spaces,person[0])
            canvas.create_text(data.width//4,increment, text = nowText, 
                                font = 'Arial 30 bold',fill='white')
            increment += 40
        
    data.backScore.draw(canvas)
                  
#### "ADD" SCREEN
#taken from grid demo in 15-112 examples from Event-Based Animations:
#https://www.cs.cmu.edu/~112/notes/notes-animations-examples.html
def pointInGrid(x, y, data):
    # return True if (x, y) is inside the grid defined by data.
    return ((data.marginX <= x <= data.width-data.marginX) and
            (data.marginY <= y <= data.height-data.marginY))
            
def getCell(x, y, data):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(x, y, data)):
        return (-1, -1)
    gridWidth  = data.width - 2*data.marginX
    gridHeight = data.height - 2*data.marginY
    cellWidth  = gridWidth / data.cols
    cellHeight = gridHeight / data.rows
    row = (y - data.marginY) // cellHeight
    col = (x - data.marginX) // cellWidth
    # triple-check that we are in bounds
    row = min(data.rows-1, max(0, row))
    col = min(data.cols-1, max(0, col))
    return (row, col)
    
def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.marginX
    gridHeight = data.height - 2*data.marginY
    columnWidth = gridWidth / data.cols
    rowHeight = gridHeight / data.rows
    x0 = data.marginX + col * columnWidth
    x1 = data.marginX + (col+1) * columnWidth
    y0 = data.marginY + row * rowHeight
    y1 = data.marginY + (row+1) * rowHeight
    return (x0, y0, x1, y1)
    
def addMousePressed(event, data):
    if(data.backAdd.isSwitch(event.x, event.y)):
        #switch everything back
        for row in range(data.rows): #4
            for col in range(data.cols): #60
                data.createNotes[row][col] = 0
        data.mode = 'start'
    elif(data.add.isSwitch(event.x,event.y)):
        #make the directory
        newLevelNumber = len(data.levels)+1
        directory = 'gameFiles/level%d' %(newLevelNumber)
        if(not os.path.exists(directory)):
            os.makedirs(directory)
            #make the file
            filename = 'text.txt'
            #creates the path to put the file
            realname = directory + '\\' + filename
            #put the items inside of the file
            text = copy.deepcopy(data.createNotes)
            file = open(realname,'w')
            for line in range(len(text)):
                file.write(str(text[line])+'\n')
            file.close()
        #make it a playable level
        init(data)
        data.mode = 'start' 
            
    (row, col) = getCell(event.x, event.y, data)
    # select this (row, col) unless it is selected

    if((row < data.rows and row >=0) and (col < data.cols and col >=0)):
        if(data.createNotes[int(row)][int(col)] == 1):
            data.createNotes[int(row)][int(col)] = 0
        else:
            data.createNotes[int(row)][int(col)] = 1
    
def addKeyPressed(event,data):
    pass
    
def addTimerFired(data):
    pass
    
def addRedrawAll(canvas, data):
    #background + general text
    canvas.create_rectangle(0,0, data.width, data.height, fill = 'black')
    
    #draw grid of cells
    for row in range(data.rows): #4
        for col in range(data.cols): #60
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            fill = 'white'
            if (data.createNotes[row][col] == 1):
                if(col == 0):
                    fill = 'firebrick1'
                elif(col == 1):
                    fill = 'DodgerBlue2'
                elif(col == 2):
                    fill = 'yellow2'
                elif(col == 3):
                    fill = 'green2'
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline='grey60',
                                    width = 1)
    data.add.draw(canvas)
    data.backAdd.draw(canvas)


#### ONE-PERSON PLAYER MODE
def onePersonPlayMousePressed(event,data):
    pass
            
def onePersonPlayKeyPressed(event,data):
    if(event.keysym == 'p'):
        data.musicPaused = not data.musicPaused        
    elif(event.keysym == 'a'):
        check = Slot(0)
        for note in data.currentNotes:
            if(check.overlap(note.x,note.y)):
                data.score += 1
                note.color = 'white'
                data.currentNotes.remove(note)
    elif(event.keysym == 's'):
        check = Slot(1)
        for note in data.currentNotes:
            if(check.overlap(note.x,note.y)):
                data.score += 1
                note.color = 'white'
                data.currentNotes.remove(note)
    elif(event.keysym == 'd'):
        check = Slot(2)
        for note in data.currentNotes:
            if(check.overlap(note.x,note.y)):
                data.score += 1
                note.color = 'white'
                data.currentNotes.remove(note)
    elif(event.keysym == 'f'):
        check = Slot(3)
        for note in data.currentNotes:
            if(check.overlap(note.x,note.y)):
                data.score += 1
                note.color = 'white'
                data.currentNotes.remove(note)
    elif(event.keysym == 'e'):
        data.timerCounter = 4000
        data.countdown = 5
    elif(event.keysym == 'q'):
        data.mode = 'end' 

def onePersonPlayTimerFired(data):
    #data.timerCounter == 650 is a whole song (60 seconds +5 countdown seconds)
    #so every minute+5sec it goes through a level
    #print(data.timerCounter) #10x is a hundreth of a second. 100 is a second
    if(data.timerCounter <= 2000 and data.currentLevel < len(data.levels)):
        #no more notes in the level then it moves to the next level
        #countdown
        if(data.timerCounter %30 == 0):
            if(data.timerCounter < 150): # 5 seconds
                data.countdown -= 1
            elif(data.countdown <= 1): #after the countdown
                #adds the notes into the game
                if(len(data.notes) > 0):
                    secNote = data.notes.pop(0)
                    #making the notes
                    for i in range(len(secNote)):
                        if(secNote[i] == 1):
                            data.currentNotes.append(Note(i))
        
        #movement of the fallingNotes
        for fallNote in data.currentNotes:
            fallNote.y += 5
            if(fallNote.y > data.height):
                data.currentNotes.remove(fallNote)
    else:
        #starts the next level
        #once all of the levels are done then create the space in the scoreboard
        data.currentLevel += 1
        if(data.currentLevel >= len(data.levels)):
            #insert the value
            tempScore = data.score
            if(len(data.scoreboard) == 0):
                data.scoreboard.append((data.score,'you'))
            else:
                for indexPerson in range(len(data.scoreboard)):
                    person = data.scoreboard[indexPerson]
                    if(tempScore >= person[0]):
                        data.scoreboard.insert(indexPerson,(data.score,'you'))
                        tempScore = -1
            data.mode = 'end'
        else:
            data.notes[:] = []
            #print('in here')
            data.notes = copy.deepcopy(data.allSongs[data.currentLevel])
            #print('notes',data.notes)
            data.timerCounter = 0
            data.countdown = 5   
    data.timerCounter += 1        
    
def onePersonPlayRedrawAll(canvas,data):
    #background
    canvas.create_rectangle(0,0, data.width, data.height, fill = 'black')
    #shows the score
    canvas.create_text(data.width//2, 20, font='Arial 14 bold',
                        fill = 'white', text = 'Score: %d' %(data.score))
    #countdown to level
    if(data.timerCounter < 300):
        canvas.create_text(data.width//2, data.height//2, font='Tahoma 20',
                        fill = 'white', text = data.countdown)
        canvas.create_text(data.width//2, data.height//2-30, font='Tahoma 20',
                        fill = 'white', 
                        text = 'Level %d' %(data.currentLevel+1))
    
    #shows the slots
    data.rslot.draw(canvas)
    data.bslot.draw(canvas)
    data.yslot.draw(canvas)
    data.gslot.draw(canvas)

    #shows the notes
    for note in data.currentNotes:
        note.draw(canvas)


#### TWO-PERSON PLAYER MODE 
def twoPersonPlayMousePressed(event,data):
    pass
            
def twoPersonPlayKeyPressed(event,data):
    if(event.keysym == 'p'):
        data.musicPaused = not data.musicPaused        
    elif(event.keysym == 'a'):
        check = Slot(0)
        for note in data.currentNotesP1:
            if(check.overlap(note.x,note.y)):
                data.scoreP1 += 1
                note.color = 'white'
                data.currentNotesP1.remove(note)
    elif(event.keysym == 's'):
        check = Slot(1)
        for note in data.currentNotesP1:
            if(check.overlap(note.x,note.y)):
                data.scoreP1 += 1
                note.color = 'white'
                data.currentNotesP1.remove(note)
    elif(event.keysym == 'd'):
        check = Slot(2)
        for note in data.currentNotesP1:
            if(check.overlap(note.x,note.y)):
                data.scoreP1 += 1
                note.color = 'white'
                data.currentNotesP1.remove(note)
    elif(event.keysym == 'f'):
        check = Slot(3)
        for note in data.currentNotesP1:
            if(check.overlap(note.x,note.y)):
                data.scoreP1 += 1
                note.color = 'white'
                data.currentNotesP1.remove(note)
                
    #player 2
    if(event.keysym == 'y'):
        data.musicPaused = not data.musicPaused        
    elif(event.keysym == 'h'):
        check = Slot(4)
        for note in data.currentNotesP2:
            if(check.overlap(note.x,note.y)):
                data.scoreP2 += 1
                note.color = 'white'
                data.currentNotesP2.remove(note)
    elif(event.keysym == 'j'):
        check = Slot(5)
        for note in data.currentNotesP2:
            if(check.overlap(note.x,note.y)):
                data.scoreP2 += 1
                note.color = 'white'
                data.currentNotesP2.remove(note)
    elif(event.keysym == 'k'):
        check = Slot(6)
        for note in data.currentNotesP2:
            if(check.overlap(note.x,note.y)):
                data.scoreP2 += 1
                note.color = 'white'
                data.currentNotesP2.remove(note)
    elif(event.keysym == 'l'):
        check = Slot(7)
        for note in data.currentNotesP2:
            if(check.overlap(note.x,note.y)):
                data.scoreP2 += 1
                note.color = 'white'
                data.currentNotesP2.remove(note)
    elif(event.keysym == 'e'):
        data.timerCounter = 4000
        data.countdown = 5
    elif(event.keysym == 'q'):
        data.mode = 'end' 

def twoPersonPlayTimerFired(data):
    #data.timerCounter == 650 is a whole song (60 seconds +5 countdown seconds)
    #so every minute+5sec it goes through a level
    #print(data.timerCounter) #10x is a hundreth of a second. 100 is a second
    if(data.timerCounter <= 2000 and data.currentLevel < len(data.levels)):
        #no more notes in the level then it moves to the next level
        #countdown
        if(data.timerCounter %30 == 0):
            if(data.timerCounter < 150): # 5 seconds
                data.countdown -= 1
            elif(data.countdown <= 1): #after the countdown
                #adds the notes into the game
                if(len(data.notes) > 0):
                    secNote = data.notes.pop(0)
                    #making the notes
                    for i in range(len(secNote)):
                        if(secNote[i] == 1):
                            data.currentNotesP1.append(Note(i))
                            data.currentNotesP2.append(Note(i+4))
        #movement of the fallingNotes
        for fallNote in data.currentNotesP1:
            fallNote.y += 5
            if(fallNote.y > data.height):
                if(fallNote.num < 4):
                    data.currentNotesP1.remove(fallNote)
        for fallNote2 in data.currentNotesP2:
            fallNote2.y += 5
            if(fallNote2.y > data.height):
                if(fallNote2.num < 4):
                    data.currentNotesP2.remove(fallNote2)
    else:
        #starts the next level
        #once all of the levels are done then create the space in the scoreboard
        data.currentLevel += 1
        if(data.currentLevel >= len(data.levels)):
            data.mode = 'end'
        else:
            data.notes[:] = []
            #print('in here')
            data.notes = copy.deepcopy(data.allSongs[data.currentLevel])
            print('data.notes', data.notes)
            #print('notes',data.notes)
            data.timerCounter = 0
            data.countdown = 5   
    data.timerCounter += 1        
    
def twoPersonPlayRedrawAll(canvas,data):
    #background
    canvas.create_rectangle(0,0, data.width, data.height, fill = 'black')
    
    canvas.create_rectangle(data.width//2-5,0,data.width//2+5,data.height, 
                            fill ='white')
    canvas.create_rectangle(data.width-15,0,data.width-5,data.height, 
                            fill ='white')
    canvas.create_rectangle(5,0,15,data.height, 
                            fill ='white')
    
    #shows the score:
    #player one score
    canvas.create_text(data.width//4, 20, font='Arial 14 bold',
                        fill = 'white', 
                        text = 'Player1 Score: %d' %(data.scoreP1))
    #player two score                    
    canvas.create_text(data.width-data.width//4, 20, font='Arial 14 bold',
                        fill = 'white', 
                        text = 'Player2 Score: %d' %(data.scoreP2))
    #countdown to level
    if(data.timerCounter < 150):
        #player1
        canvas.create_text(data.width//4-20, data.height//2, font='Tahoma 20',
                        fill = 'white', text = data.countdown)
        canvas.create_text(data.width//4-20, data.height//2-30, font='Tahoma 20',
                        fill = 'white', 
                        text = 'Level %d' %(data.currentLevel+1))
        #player2
        canvas.create_text(data.width-data.width//4-20, 
                        data.height//2, font='Tahoma 20',
                        fill = 'white', text = data.countdown)
        canvas.create_text(data.width-data.width//4-20, 
                        data.height//2-30, font='Tahoma 20',
                        fill = 'white', 
                        text = 'Level %d' %(data.currentLevel+1))
    
    #shows the slots
    data.r1slot.draw(canvas)
    data.b1slot.draw(canvas)
    data.y1slot.draw(canvas)
    data.g1slot.draw(canvas)
    
    data.r2slot.draw(canvas)
    data.b2slot.draw(canvas)
    data.y2slot.draw(canvas)
    data.g2slot.draw(canvas)

    #shows the notes
    for note in data.currentNotesP1:
        note.draw(canvas)
    for note2 in data.currentNotesP2:
        note2.draw(canvas)


################################################################################
#### RUN + MUSIC + THREADING
################################################################################

####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.mode == "start"): startMousePressed(event, data)
    elif(data.mode == "help"): helpMousePressed(event,data)
    elif(data.mode == "choice"): choiceMousePressed(event,data)
    elif (data.mode == "one"): onePersonPlayMousePressed(event,data)
    elif (data.mode == "two"): twoPersonPlayMousePressed(event,data)
    elif (data.mode == "end"): endMousePressed(event, data)
    elif (data.mode == "add"): addMousePressed(event, data)
    elif (data.mode == "scoreboard"): scoreboardMousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "start"): startKeyPressed(event, data)
    elif(data.mode == "help"): helpKeyPressed(event,data)
    elif(data.mode == "choice"): choiceKeyPressed(event,data)
    elif (data.mode == "one"): onePersonPlayKeyPressed(event,data)
    elif (data.mode == "two"): twoPersonPlayKeyPressed(event,data)
    elif (data.mode == "end"): endKeyPressed(event, data)
    elif (data.mode == "add"): addKeyPressed(event, data)
    elif (data.mode == "scoreboard"): scoreboardKeyPressed(event, data)

def timerFired(data):
    if (data.mode == "start"): startTimerFired(data)
    elif(data.mode == "help"): helpTimerFired(data)
    elif(data.mode == "add"): addTimerFired(data)
    elif(data.mode == "choice"): choiceTimerFired(data)
    elif (data.mode == "one"): onePersonPlayTimerFired(data)
    elif (data.mode == "two"): twoPersonPlayTimerFired(data)
    elif (data.mode == "end"): endTimerFired(data)
    elif (data.mode == "scoreboard"): scoreboardTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "start"): startRedrawAll(canvas, data)
    elif (data.mode == "help"): helpRedrawAll(canvas, data)
    elif (data.mode == "add"): addRedrawAll(canvas, data)
    elif (data.mode == "choice"): choiceRedrawAll(canvas, data)
    elif (data.mode == "one"): onePersonPlayRedrawAll(canvas,data)
    elif (data.mode == "two"): twoPersonPlayRedrawAll(canvas,data)
    elif (data.mode == "end"): endRedrawAll(canvas, data)
    elif (data.mode == "scoreboard"): scoreboardRedrawAll(canvas, data)

#cite: demo code in pyaudio manual: 
#https://abhgog.gitbooks.io/pyaudio-manual/content/sample-project.html
def playMusic(file):
    CHUNK = 1024 #measured in bytes
    SECONDS = 60 #original number of seconds will be 60
    wf = wave.open(file, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    for t in range(0, int(CHUNK*SECONDS)):
            if(len(data) > 0):
                stream.write(data)
                data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()
    

def run(width = 1000, height=500):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds (1000 is a second)
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    #theThreading(data)
    root.mainloop()  # blocks until window is closed
    print("bye!")

def stageMusic(data):
    if(data.mode == 'one' or data.mode == 'two'):
        if(data.timerCounter > 150):
            playMusic(data.songs[data.currentLevel])
    elif(data.mode == 'start'):
        playMusic('universalfunk.wav')

def theThreading(data):
    animation = threading.Thread(target = timerFired, args=data)
    music = threading.Thread(target = stageMusic, args = data)
    animation.start()
    music.start()


def main():
    run()

if __name__== "__main__":
  main()
  

#extraneous code
# print(data.musicPaused)
# for t in range(0, int(CHUNK*SECONDS)):
#     if(data.musicPaused):
#         stream.stop_stream()
#     else:
#         if(not stream.is_stopped()):
#             stream.start_stream()
#         else:
#             if(len(data) > 0):
#                 stream.write(data)
#                 data = wf.readframes(CHUNK)