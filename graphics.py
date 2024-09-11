# Add the graphics (turtle) related code in this file
import turtle as t
import random

window = t.Screen()
window.title("Cocomo's Scrabble")
window.bgcolor("black")
windowWidth = 1600
windowHeight = 900
cellSize = 40
window.setup(width=windowWidth, height=windowHeight)

## all the turtles: 😴😪😭
grid = []
grid_turtle = t.Turtle()
grid_turtle.speed(0)
grid_turtle.hideturtle()

collection_turtle = t.Turtle()
collection_turtle.hideturtle()

# score_turtle = t.Turtle()
# score_turtle.hideturtle()


def random_color():
    return (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))

def drawRectangle(obj, x, y, width, height, color="none"):
    obj.penup()
    obj.goto(x, y)
    obj.pendown()
    if color=="none":
        obj.fillcolor(random_color())
    else: obj.fillcolor(color)
    obj.begin_fill()
    for _ in range(2):
        obj.forward(width)
        obj.right(90)
        obj.forward(height)
        obj.right(90)
    obj.end_fill()

def printText(turtle, text, x, y, font=("Arial", 16, "normal"), align="left", color="white"):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.color(color)
    turtle.write(text, font=font, align=align)

def renderCollection(playerData, playerNum, operation="delete", initialisation=False):
    cellSpacing = 10
    collectionSize = len(playerData["collection"])
    verticalOffset = 100

    startX= windowWidth/4 - (cellSize+cellSpacing)*collectionSize
    startY = windowHeight/2 -100 - playerNum*(cellSize + verticalOffset)

    score_turtle= playerData["turtle"]
    score_turtle.clear()
    printText(score_turtle, f"{playerData["name"]}'s score: {playerData["score"]}", startX, startY)
    startY -=40
    
    if initialisation==True: #change 5 to total players *5
        for i in range(collectionSize):
            text_turtle = t.Turtle()
            text_turtle.hideturtle()
            playerData["collection"][i]["coords"] = [startX +i*(cellSize+ cellSpacing), startY, cellSize, cellSize, text_turtle]
            drawRectangle(collection_turtle, playerData["collection"][i]["coords"][0], playerData["collection"][i]["coords"][1], playerData["collection"][i]["coords"][2], playerData["collection"][i]["coords"][3])
            printText(text_turtle, playerData["collection"][i]["goti"], playerData["collection"][i]["coords"][0]+cellSize/2, playerData["collection"][i]["coords"][1] -(3*cellSize)/4, align="center", color="black")
    else:
        for i in range(collectionSize):
            text_turtle = playerData["collection"][i]["coords"][4]
            goti = playerData["collection"][i]["goti"]
            if operation=="delete" and goti=="":
                text_turtle.clear()
            printText(text_turtle, playerData["collection"][i]["goti"], playerData["collection"][i]["coords"][0]+cellSize/2, playerData["collection"][i]["coords"][1] -(3*cellSize)/4, align="center", color="black")


def defineGrid(row:int = 15, cols:int = 15):
    cellSpacing  =4
    # grid_width = cols * cellSize + (cols-1)*cellSpacing
    grid_height = row * cellSize + (row-1)*cellSpacing
    startX = -windowWidth/2 +50
    startY = grid_height/2
    
    for i in range(row):
        grid.append([])
        for j in range(cols):
            x = startX + j*(cellSize+cellSpacing)
            y = startY - i*(cellSize+ cellSpacing)
            gridTextTurtle = t.Turtle()
            gridTextTurtle.hideturtle()
            grid[i].append([x, y, cellSize, cellSize, gridTextTurtle, "", i, j])

def drawGrid():
    for row in grid:
        for col in row:
            drawRectangle(grid_turtle, col[0], col[1], col[2], col[3])
    window.update()