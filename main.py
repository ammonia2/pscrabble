# Add the implementation logic code here
from data import game_data
from graphics import defineGrid, drawGrid, t, renderCollection, printText, windowHeight, window, grid, drawRectangle
import random
import turtle as t
import time
import json
import os

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
        self.hint=[]
        self.skip=[]
        self.skipped=False
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

        self.hint_turtle = t.Turtle()
        self.hint_turtle.hideturtle()

        self.selectedLetter = None
        self.selectedLetterIndex = None

        self.gameOver=False

    def displayTime(self):
        if self.wordMade:
            self.onTimerEnd()
            return
        elif self.skipped==True:
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

    def getHints(self):
        if self.playerData[self.turn]["hints"] ==0: return
        self.playerData[self.turn]["hints"] -=1
        gridEmpty = self.gridEmpty()
        searched = {}
        hints = []
        for i in range(15):
            if gridEmpty and i!=7:
                continue

            for j in range(15):
                for k in range(2, 9):
                    if j + k<15:
                        inPlaceX= True if gridEmpty else False
                        inPlaceY= True if gridEmpty else False
                        spaces, spacesV=0,0

                        for s in range(j, j+k):
                            if grid[i][s][5]=='':
                                spaces+=1
                            if grid[s][i][5]=='':
                                spacesV+=1

                        searchWordX, searchWordY='', ''
                        miniX= min(spaces, k)
                        miniY =min(spacesV, k)

                        for s in range(j, j+miniX):
                            if grid[i][s][5]=='':
                                if not inPlaceX and self.isAdjacentToExistingLetter(i, s):
                                    inPlaceX=True
                                searchWordX+= '.'
                            else:
                                inPlaceX=True
                                searchWordX+= grid[i][s][5]

                        for s in range(j, j+miniY):
                            if grid[s][i][5]=='':
                                if not inPlaceY and self.isAdjacentToExistingLetter( s, i):
                                    inPlaceY=True
                                searchWordY+= '.'
                            else:
                                inPlaceY=True
                                searchWordY+= grid[s][i][5]

                        if not (inPlaceX and inPlaceY): continue

                        letters = self.playerData[self.turn]["collection"]
                        
                        combs= []
                        combsX = [] if not inPlaceX and spaces>=2 else self.combinations(letters,  searchWordX)
                        combsY = [] if not inPlaceY and spacesV>=2 else self.combinations(letters,  searchWordY)

                        if searchWordX not in searched:
                            searched[searchWordX] = combsX
                        if searchWordY not in searched:
                            searched[searchWordY] = combsY
                        
                        for comb in combsX:
                            comb.extend([i, j, "lateral"])
                            combs.append(comb)
                        for comb in combsY:
                            comb.extend([j, i, "vertical"])
                            combs.append(comb)

                        validCombs= self.validateCombs(combs)
                        for comb in validCombs:
                            hints.append(comb)

                    #     print(f"i: {i}, j: {j}, k: {k}, miniX: {miniX}, miniY: {miniY} condition met")
                    # else:
                    #     print(f"i: {i}, j: {j}, k: {k}, miniX: {0}, condition not met")
        
        # print(hints)
        maxm=0
        wort= ""
        pos=""
        for hint in hints:
            if hint[5] >maxm:
                maxm= hint[5]
                wort = hint[0]
                pos= hint[4]

        if wort=="":
            self.playerData[self.turn]["hints"] +=1
            return

        renderCollection(self.playerData[self.turn], self.turn)
        printText(self.hint_turtle, f"{pos} word: {wort}", 150, -windowHeight/2+150, color="red")

    def validateCombs(self, combs):
        validCombs= []
        gridEmpty = self.gridEmpty()

        for comb in combs:
            x, y, dirn= comb[2], comb[3], comb[4]

            if dirn== "lateral":
                if comb[1]=="": continue

                inPlace= False
                left= self.getTop(x, y)
                right= self.getBottom(x, y+len(comb[0])-1)

                if left!="" or right!="" or gridEmpty: inPlace=True

                if left+ comb[0]+right in words:
                    invalid=False
                    score=0
                    for i, letter in enumerate(comb[0]):
                        if not inPlace and self.isAdjacentToExistingLetter(x, y+i):
                            inPlace=True
                        top = self.getLeft(x, y+i)
                        bottom= self.getRight(x, y+i)
                        if top!=bottom and top+letter+bottom not in words:
                            invalid=True
                            break
                    
                    if not invalid and inPlace:
                        comb[0]= (left+ comb[0]+right)
                        comb[3] = comb[3] -len(left)
                        for letter in comb[1]:
                            for l in scoreDict:
                                if l["alphabet"]==letter:
                                    score+=l["score"]
                        comb.extend([score, x, y+len(comb[0]), left, right])
                        validCombs.append(comb)

            elif dirn=="vertical":
                if comb[1]=="": continue

                inPlace=False
                top= self.getLeft(x, y)
                bottom= self.getRight(x+len(comb[0])-1, y)
                if top!="" or bottom !="" or gridEmpty: inPlace=True

                if top +comb[0]+bottom in words:
                    invalid=False
                    score=0
                    for i, letter in enumerate(comb[0]):
                        if not inPlace and self.isAdjacentToExistingLetter(x+i, y):
                            inPlace=True
                        left =self.getTop(x+i, y)
                        right =self.getBottom(x+i, y)
                        if left!=right and left+letter+right not in words:
                            invalid=True
                            break
                    
                    if not invalid and inPlace:
                        comb[0] = top+ comb[0]+bottom
                        comb[2]= comb[2]- len(top)
                        for letter in comb[1]:
                            for l in scoreDict:
                                if l["alphabet"]==letter:
                                    score+=l["score"]
                        comb.extend([score, x+len(comb[0]), y, top, bottom])
                        validCombs.append(comb)

        return validCombs

    def onClick(self, x, y):
        if self.selectedLetter:
            self.gridClick(x, y)
        elif self.submit[0] <= x<=self.submit[0]+self.submit[2] and self.submit[1]-self.submit[3]<=y <=self.submit[1]:
            self.validateInsertions()
        elif self.hint[0] <= x<= self.hint[0]+self.hint[2] and self.hint[1]-self.hint[3] <= y <=self.hint[1]:
            self.getHints()
        elif self.skip[0] <= x<= self.skip[0]+self.skip[2] and self.skip[1]-self.skip[3] <= y <=self.skip[1]:
            self.skipped= True
        else:
            for k in range(self.csize):
                goti = self.playerData[self.turn]["collection"][k]["coords"]
                gotiX, gotiY, gotiW, gotiH = goti[0], goti[1], goti[2], goti[3]
                
                if (gotiX <= x <= gotiX+gotiW) and (gotiY-gotiH <= y <= gotiY) and self.playerData[self.turn]["collection"][k]["goti"]!="":
                    if self.playerData[self.turn]["collection"][k]["goti"]=='-':
                        newGoti=t.textinput("new Goti" ,"Enter goti to replace: ")
                        self.playerData[self.turn]["collection"][k]["goti"]= newGoti
                        self.playerData[self.turn]["collection"][k]['minus'] = True
                        renderCollection(self.playerData[self.turn], self.turn)
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
        self.skipped=False
        if not self.wordMade:
            self.returnCache()
        else:
            self.cache=[]
        self.wordMade=False
        
        self.turn += 1
        self.totalTurns+=1
        self.playerTurn()
        #end display timer
        #other player's turn doesn't start after submit
        #inserted letters aren't removed from cache when timer is over

    def writeScores(self, winner=False, index=None):
        if not winner:
            printText(self.hint_turtle, f"Winner: {self.playerData[self.turn]["name"]}", 150,  -windowHeight/2+150, color="red", font=("Arial", 24, "normal"))

            fileName = f"{self.playerData[self.turn]["name"]}.json"
            word = self.playerData[self.turn]["words"][-1][0]
            wordScore = self.playerData[self.turn]["words"][-1][1]

            if not os.path.exists(fileName):
                with open(fileName, 'w') as file:
                    data = {word: wordScore}
                    json.dump(data, file, indent=4)
            else:
                with open(fileName, 'r') as file:
                    data = json.load(file)
                data[word] = wordScore

                with open(fileName, 'w') as file:
                    json.dump(data, file, indent=4)
        else:
            with open("winner.txt", 'a') as file:
                file.write(f"{self.playerData[index]["name"]}\n")
                for word, score in self.playerData[index]["words"]:
                    file.write(f"{word}: {score}\n")

    def playerTurn(self):
        if self.totalTurns> self.players*5:
            maxm, n=0, 0
            for i, player in enumerate(self.playerData):
                if player["score"] > maxm:
                    maxm= player["score"]
                    n=i
            self.writeScores(winner=n, index=n)
        elif self.turn < self.players:
            self.turn_turtle.clear()
            self.hint_turtle.clear()
            printText(self.turn_turtle, f"{self.playerData[self.turn]['name']}'s turn.", 0, windowHeight/2-40, align="center")
            self.timeLeft = 90
            self.displayTime()
            
            window.onscreenclick(self.onClick)
        elif not self.gameOver:
            self.turn = 0
            self.playerTurn()
        else:
            printText(self.turn_turtle, "Game Over!", 0, windowHeight/2-40, align="center")

    def combinations(self, letters, search, k=0):
        if k==len(search):
            return [["", ""]]
        
        result = []
        if search[k]=='.':
            for i, letterDict in enumerate(letters):
                remainingLetters = letters[:i] + letters[i+1:]
                letter= letterDict["goti"]
                if letter == '-':
                    for char in 'abcdefghijklmnopqrstuvwxyz-':
                        for combo in self.combinations(remainingLetters, search, k+1):
                            result.append([char + combo[0], char + combo[1]])
                else:
                    for combo in self.combinations(remainingLetters, search, k+1):
                        result.append([letter + combo[0], letter + combo[1]])

        else:
            for combo in self.combinations(letters, search, k+1):
                result.append([search[k]+combo[0], combo[1]])
        
        return result

    def playGame(self):
        self.submit = [550, -windowHeight/2+150, 100, 50]
        drawRectangle(self.button_turtle, self.submit[0], self.submit[1], self.submit[2], self.submit[3], color="green")
        printText(self.button_turtle, "Submit",self.submit[0]+50, self.submit[1]-35, align="center")
        
        self.hint = [550, -windowHeight/2+210, 100, 50]
        drawRectangle(self.button_turtle, self.hint[0], self.hint[1], self.hint[2], self.hint[3], color="blue")
        printText(self.button_turtle, "Hint", self.hint[0]+50, self.hint[1]-35, align="center")

        self.skip = [550, -windowHeight/2+270, 100, 50]
        drawRectangle(self.button_turtle, self.skip[0], self.skip[1], self.skip[2], self.skip[3], color="DarkGrey")
        printText(self.button_turtle, "Skip", self.skip[0]+50, self.skip[1]-35, align="center")

        self.playerTurn()

    def getLeft(self, startX, startY):
        left = ""
        i = 1
        while startX - i >= 0 and grid[startX - i][startY][5] != "":
            left = grid[startX - i][startY][5] + left
            i += 1
        return left

    def getRight(self, startX, startY):
        right = ""
        i = 1
        while startX + i < len(grid) and grid[startX + i][startY][5] != "":
            right += grid[startX + i][startY][5]
            i += 1
        return right

    def getTop(self, startX, startY):
        top = ""
        i = 1
        while startY - i >= 0 and grid[startX][startY - i][5] != "":
            top = grid[startX][startY - i][5] + top
            i += 1
        return top

    def getBottom(self, startX, startY):
        bottom = ""
        i = 1
        while startY + i < len(grid[0]) and grid[startX][startY + i][5] != "":
            bottom += grid[startX][startY + i][5]
            i += 1
        return bottom

    def getWord(self, val):
        startX, startY = val[6], val[7]
        
        left= self.getLeft(startX, startY)
        right= self.getRight(startX, startY)    

        word1 = left + grid[startX][startY][5] + right

        top= self.getTop(startX, startY)
        bottom= self.getBottom(startX, startY)

        if right==left==top==bottom:
            return False, False

        word2 = top + grid[startX][startY][5] + bottom

        found1 = word1 in words if len(word1) > 1 else False
        found2 = word2 in words if len(word2) > 1 else False

        found1 = word1 if found1 else True if len(word1) == 1 else False
        found2 = word2 if found2 else True if len(word2) == 1 else False

        return found1, found2

    def returnCache(self):
        for value in self.cache:
            temp=value["grid"][5]
            value["grid"][5] =""
            value["grid"][4].clear()
            value["data"]["goti"] = temp if value["data"]["minus"]==False else '-'
            renderCollection(self.playerData[self.turn], self.turn, operation="add")
        self.cache = []

    def restoreCollection(self):
        for letter in self.playerData[self.turn]["collection"]:
            if letter["goti"]=="":
                randomGoti=random.choice(gotian)
                minus = True if randomGoti=='-' else False
                gotian.remove(randomGoti)
                letter["goti"] = randomGoti
                letter["minus"] = minus
        renderCollection(playerData[self.turn], self.turn)

    def isAdjacentToExistingLetter(self, x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        inPlace= False
        
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
        inPlace= False
        newWords = []
        # print("validating..")

        isFirstMove = self.gridEmpty()
        if isFirstMove: inPlace=True
        
        for value in self.cache:
            x, y = value["grid"][6], value["grid"][7]
            if not isFirstMove:
                if not inPlace and self.isAdjacentToExistingLetter(x, y):
                    inPlace = True

            word1, word2 = self.getWord(value["grid"])
            # print(word1, word2)
            if not (word1 and word2):
                allValid = False
                break
            if word1!=True and len(word1)>1 and word1 not in newWords:
                newWords.append(word1)
            if word2!=True and len(word2)>1 and word2 not in newWords:
                newWords.append(word2)

        if allValid and inPlace:
            for word in newWords:
                # if word not in self.playerData[self.turn]["words"]:
                score=self.getScore(word)
                self.playerData[self.turn]["words"].append([word, score])
                self.playerData[self.turn]["score"]+= score
                self.writeScores()

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
        playerData.append({"name": name, "score": 0, "collection": [], "words": [], "turtle": score_turtle, "hints": 2})

        for j in range(collectionSize):
            randomGoti = random.choice(gotian)
            gotian.remove(randomGoti)
            minus = True if randomGoti=='-' else False
            playerData[i]["collection"].append({"goti": randomGoti, "coords":[], "minus": minus})

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