# Add the implementation logic code here
from data import game_data
from graphics import defineGrid, drawGrid, t, renderCollection, printText, windowHeight, window, grid, drawRectangle
import random
import turtle as t
import time

clicked = False
cache = []
playerCount = 2
collectionSize = 8 # n
playerData = []
gotian = game_data["gotian"][:] #list with chars (copy made so original gotian isn't affected)
score_dict = game_data["alphabet_score"] #score against alphabet in nested dict
words = game_data["words"] #list with possible words

class Game:
    def __init__(self, playerData, playerCount, collectionSize):
        self.playerData = playerData
        self.csize = collectionSize
        self.players  =playerCount
        self.turn =0
        self.cache = []
        self.cellSize = 40

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

        self.clicked=False

    def displayTime(self):
        if self.timeLeft > 0:
            self.timeLeft -= 1
            self.timer_turtle.clear()
            printText(self.timer_turtle, f"Time left: {self.timeLeft} seconds", 0, windowHeight/2-70, align="center")
            window.ontimer(self.displayTime, 1000)
        else:
            self.timer_turtle.clear()
            printText(self.timer_turtle, "Time's up!", 0, windowHeight/2-70, align="center")
            self.onTimerEnd()

    def gridClick(self, x, y):
        grid_text_turtle = t.Turtle()
        grid_text_turtle.hideturtle()
        if self.selectedLetter:
            for i, row in enumerate(grid):
                for j, cell in enumerate(row):
                    if (cell[0] <= x <= cell[0] + cell[2]) and (cell[1] - cell[3] <= y <= cell[1]):
                        printText(grid_text_turtle, self.selectedLetter, cell[0] + self.cellSize/2, cell[1] - (3*self.cellSize)/4, color="black", align="center")
                        
                        self.playerData[self.turn]["collection"][self.selectedLetterIndex]["goti"] = ""
                        renderCollection(self.playerData[self.turn], self.turn)
                        self.selectedLetter = None
                        self.selectedLetterIndex = None
                        return

    def handleGotiClick(self, k):
        self.selectedLetter = self.playerData[self.turn]["collection"][k]["goti"]
        self.selectedLetterIndex = k

        x, y, w, h = self.playerData[self.turn]["collection"][k]["coords"]
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
        else:
            for k in range(self.csize):
                goti = self.playerData[self.turn]["collection"][k]["coords"]
                gotiX, gotiY, gotiW, gotiH = goti[0], goti[1], goti[2], goti[3]
                
                if (gotiX <= x <= gotiX+gotiW) and (gotiY-gotiH <= y <= gotiY):
                    self.handleGotiClick(k)
                    break

    def onTimerEnd(self):
        window.onscreenclick(None)
        self.turn += 1
        self.selectedLetter = None
        self.selectedLetterIndex = None
        self.border_turtle.clear()
        self.playerTurn()

    def playerTurn(self):
        if self.turn < self.players:
            self.turn_turtle.clear()
            printText(self.turn_turtle, f"{self.playerData[self.turn]['name']}'s turn.", 0, windowHeight/2-40, align="center")
            self.timeLeft = 90
            self.displayTime()
            
            window.onscreenclick(self.onClick)
        else:
            printText(self.turn_turtle, "Game Over!", 0, windowHeight/2-40, align="center")

    def playGame(self):
        drawRectangle(self.button_turtle, -windowHeight/2+150, 550, 200, 100)
        self.turn = 0
        self.playerTurn()

###-----
##-----
#-----
def setPlayers(playerData, playerCount, collectionSize):
    for i in range(playerCount):
        name = t.textinput("Player Name", f"Enter name for player {i + 1}:")
        playerData.append({"name": name, "score": 0, "collection": [], "words": []})

        for j in range(collectionSize):
            random_goti = random.choice(gotian)
            gotian.remove(random_goti)
            playerData[i]["collection"].append({"goti": random_goti, "coords":[]})

        renderCollection(playerData[i], i)


defineGrid()
drawGrid()

setPlayers(playerData, playerCount, collectionSize)

game = Game(playerData, playerCount, collectionSize)
# playGame(playerData, playerCount, collectionSize)
game.playGame()

t.done()

#1. words need to be made with all conecting boxes
#2. increase scrore based on number of full words completed
#3. move words inserted back to the options set if not all directions satisfy a word 
#   in the making