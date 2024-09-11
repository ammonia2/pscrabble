# Add the implementation logic code here
from data import game_data
from graphics import defineGrid, drawGrid, t, renderCollection, printText, windowHeight, window, grid, drawRectangle
import random
import turtle as t
import time

playerCount = 2
collectionSize = 8 # n
playerData = []
gotian = game_data["gotian"][:] #list with chars (copy made so original gotian isn't affected)
scoreDict = game_data["alphabet_score"] #score against alphabet in nested dict
words = game_data["words"] #list with possible words

class Game:
    def __init__(self, playerData, playerCount, collectionSize):
        self.playerData = playerData
        self.csize = collectionSize
        self.players  =playerCount
        self.turn =0
        self.totalTurns =0
        self.cache = []
        self.submit = []
        self.cellSize = 40
        self.wordMade=False

        self.timer_turtle = t.Turtle()
        self.timer_turtle.hideturtle()

        self.turn_turtle = t.Turtle()
        self.turn_turtle.hideturtle()

        self.border_turtle = t.Turtle()
        self.border_turtle.hideturtle()

        self.button_turtle = t.Turtle()
        self.button_turtle.hideturtle()

        self.selectedLetter = None
        self.selectedLetterIndex = None

        self.gameOver=False

    def displayTime(self):
        if self.wordMade:
            self.onTimerEnd()
            return
        elif self.timeLeft > 0:
            self.timeLeft -= 1
            self.timer_turtle.clear()
            printText(self.timer_turtle, f"Time left: {self.timeLeft} seconds", 0, windowHeight/2-70, align="center")
            window.ontimer(self.displayTime, 1000)
        else:
            self.timer_turtle.clear()
            printText(self.timer_turtle, "Time's up!", 0, windowHeight/2-70, align="center")
            self.onTimerEnd()

    def gridClick(self, x, y):
        if self.selectedLetter:
            for i, row in enumerate(grid):
                for j, cell in enumerate(row):
                    if (cell[0] <= x <= cell[0] + cell[2]) and (cell[1] - cell[3] <= y <= cell[1]) and (cell[5]=="" or self.selectedLetter=='-'):
                        cell[5] = self.selectedLetter
                        printText(cell[4], cell[5], cell[0] + self.cellSize/2, cell[1] - (3*self.cellSize)/4, color="black", align="center")
                        
                        self.playerData[self.turn]["collection"][self.selectedLetterIndex]["goti"] = ""
                        renderCollection(self.playerData[self.turn], self.turn)

                        self.cache.append({"grid": cell, "data": self.playerData[self.turn]["collection"][self.selectedLetterIndex]})
                        
                        self.border_turtle.clear()
                        self.selectedLetter = None
                        self.selectedLetterIndex = None
                        return

    def handleGotiClick(self, k):
        self.selectedLetter = self.playerData[self.turn]["collection"][k]["goti"]
        self.selectedLetterIndex = k

        x, y, w, h, turtle = self.playerData[self.turn]["collection"][k]["coords"]
        self.border_turtle.clear()
        self.border_turtle.penup()
        self.border_turtle.goto(x, y)
        self.border_turtle.pendown()
        self.border_turtle.color("red")
        for _ in range(2):
            self.border_turtle.forward(w)
            self.border_turtle.right(90)
            self.border_turtle.forward(h)
            self.border_turtle.right(90)

    def onClick(self, x, y):
        if self.selectedLetter:
            self.gridClick(x, y)
        elif self.submit[0] <= x<=self.submit[0]+self.submit[2] and self.submit[1]-self.submit[3]<=y <=self.submit[1]:
            self.validateInsertions()
        else:
            for k in range(self.csize):
                goti = self.playerData[self.turn]["collection"][k]["coords"]
                gotiX, gotiY, gotiW, gotiH = goti[0], goti[1], goti[2], goti[3]
                
                if (gotiX <= x <= gotiX+gotiW) and (gotiY-gotiH <= y <= gotiY) and self.playerData[self.turn]["collection"][k]["goti"]!="":
                    self.handleGotiClick(k)
                    break

    def getScore(self, word):
        score=0
        for letter in word:
            inCache=False
            for value in self.cache:
                if value["grid"][5]==letter:
                    for x in scoreDict:
                        if x["alphabet"] ==value["grid"][5]:
                            score+=x["score"]
                            break

        return score

    def onTimerEnd(self):
        window.onscreenclick(None)
        self.selectedLetter = None
        self.selectedLetterIndex = None
        self.border_turtle.clear()
        if not self.wordMade:
            self.returnCache()
        else:
            self.cache=[]
        self.wordMade=False
        
        self.turn += 1
        self.playerTurn()
        #end display timer
        #other player's turn doesn't start after submit
        #inserted letters aren't removed from cache when timer is over

    def playerTurn(self):
        if self.turn < self.players:
            self.turn_turtle.clear()
            printText(self.turn_turtle, f"{self.playerData[self.turn]['name']}'s turn.", 0, windowHeight/2-40, align="center")
            self.timeLeft = 90
            self.displayTime()
            
            window.onscreenclick(self.onClick)
        elif not self.gameOver:
            self.turn = 0
            self.playerTurn()
        else:
            printText(self.turn_turtle, "Game Over!", 0, windowHeight/2-40, align="center")

    def playGame(self):
        self.submit = [550, -windowHeight/2+150, 100, 50]
        drawRectangle(self.button_turtle, self.submit[0], self.submit[1], self.submit[2], self.submit[3], color="green")
        printText(self.button_turtle, "Submit",self.submit[0]+50, self.submit[1]-35, align="center")
        self.playerTurn()

    def getWord(self, val):
        startX, startY = val[6], val[7]
        foundL, foundR = False, False
        i, left, right=1, "", ""
        while not foundL or not foundR:
            if not foundL and startX-i>=0 and grid[startX-i][startY][5]=="":
                foundL=True
            else:
                left+=grid[startX-i][startY][5]
            if not foundR and startX+i<len(grid[0]) and grid[startX+i][startY][5]=="":
                foundR=True
            else:
                right+=grid[startX+i][startY][5]
            i+=1
        i=1
        top, bottom="", ""
        foundL, foundR=False, False
        while not foundL or not foundR:
            if not foundL and startY-i>=0 and grid[startX][startY-i][5]=="":
                foundL=True
            else:
                top+=grid[startX][startY-i][5]
            if not foundR and startY+i<len(grid[0]) and grid[startX][startY+i][5]=="":
                foundR=True
            else:
                bottom+=grid[startX][startY+i][5]
            i+=1

        if top==bottom==left==right:
            return False, False

        left = left[::-1]
        top= top[::-1]
        word1 = left+grid[startX][startY][5] + right
        word2 = top+ grid[startX][startY][5] + bottom

        found1= word1 in words if len(word1)!=1 else False
        found2= word2 in words if len(word2)!=1 else False

        found1 =word1 if found1 else False
        found1 =word2 if found2 else False

        return found1, found2

    def returnCache(self):
        for value in self.cache:
            temp=value["grid"][5]
            value["grid"][5] =""
            value["grid"][4].clear()
            value["data"]["goti"] = temp
            renderCollection(self.playerData[self.turn], self.turn, operation="add")
        self.cache = []

    def restoreCollection(self):
        for letter in self.playerData[self.turn]["collection"]:
            if letter["goti"]=="":
                randomGoti=random.choice(gotian)
                gotian.remove(randomGoti)
                letter["goti"] = randomGoti
        renderCollection(playerData[self.turn], self.turn)

    def isAdjacentToExistingLetter(self, x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dx, dy in directions:
            adjacentX = x + dx
            adjacentY = y + dy
            
            if 0 <= adjacentX < len(grid[0]) and 0 <= adjacentY<len(grid[0]):
                if grid[adjacentX][adjacentY][5] != "":
                    isFromCurrentMove = False
                    for value in self.cache:
                        if value["grid"][6] == adjacentX and value["grid"][7] == adjacentY:
                            isFromCurrentMove =True
                            break
                    
                    if not isFromCurrentMove:
                        return True
        
        return False

    def gridEmpty(self):
        for row in grid:
            for cell in row:
                inCache = False
                for value in self.cache:
                    if cell ==value["grid"]:
                        inCache=True
                
                if cell[5] != "" and not inCache:
                    return False
        return True

    def validateInsertions(self):
        allValid = True
        newWords = []

        isFirstMove = self.gridEmpty()
        
        for value in self.cache:
            x, y = value["grid"][6], value["grid"][7]
            if not isFirstMove:
                if not self.isAdjacentToExistingLetter(x, y):
                    allValid = False
                    break

            word1, word2 = self.getWord(value["grid"])
            if not (word1 and word2):
                allValid = False
                break
            if word1!=True and len(word1)>1 and word1 not in newWords:
                newWords.append(word1)
            if word2!=True and len(word2)>1 and word2 not in newWords:
                newWords.append(word2)

        if allValid:
            # print(newWords)
            for word in newWords:
                if word not in self.playerData[self.turn]["words"]:
                    score=self.getScore(word)
                    self.playerData[self.turn]["words"].append([word, score])
                    self.playerData[self.turn]["score"]+= score

            self.wordMade=True
            self.cache=[]
            self.restoreCollection()
        else:
            self.returnCache()

###-----
##-----
#-----
def setPlayers(playerData, playerCount, collectionSize):
    for i in range(playerCount):
        name = t.textinput("Player Name", f"Enter name for player {i + 1}:")
        score_turtle = t.Turtle()
        score_turtle.hideturtle()
        playerData.append({"name": name, "score": 0, "collection": [], "words": [], "turtle": score_turtle})

        for j in range(collectionSize):
            randomGoti = random.choice(gotian)
            gotian.remove(randomGoti)
            playerData[i]["collection"].append({"goti": randomGoti, "coords":[]})

        renderCollection(playerData[i], i, initialisation=True)

# button_turtle = t.Turtle()
# button_turtle.hideturtle()
defineGrid()
drawGrid()

setPlayers(playerData, playerCount, collectionSize)

game = Game(playerData, playerCount, collectionSize)
game.playGame()

t.done()

#1. words need to be made with all conecting boxes
#2. increase scrore based on number of full words completed
#3. move words inserted back to the options set if not all directions satisfy a word 
#   in the making