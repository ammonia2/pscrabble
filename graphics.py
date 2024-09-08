# Add the graphics (turtle) related code in this file
import turtle as t
import random

window = t.Screen()
window.title("Cocomo's Scrabble")
window.bgcolor("black")
windowWidth = 1600
windowHeight = 800
cellSize = 40
window.setup(width=windowWidth, height=windowHeight)

grid = []
grid_turtle = t.Turtle()
grid_turtle.speed(0)
grid_turtle.hideturtle()

def random_color():
    return (random.random(), random.random(), random.random())

def draw_rectangle(obj, x, y, width, height):
    obj.penup()
    obj.goto(x, y)
    obj.pendown()
    obj.fillcolor(random_color())
    obj.begin_fill()
    for _ in range(2):
        obj.forward(width)
        obj.right(90)
        obj.forward(height)
        obj.right(90)
    obj.end_fill()

def defineGrid(m: int = 15, n: int = 15):
    cellSpacing  =5
    grid_width = n * cellSize + (n-1)*cellSpacing
    grid_height = m * cellSize + (m-1)*cellSpacing
    startX = -windowWidth/2 +50
    startY = grid_height/2
    
    for i in range(m):
        grid.append([])
        for j in range(n):
            x = startX + j*(cellSize+cellSpacing)
            y = startY - i*(cellSize+ cellSpacing)
            grid[i].append([x, y, cellSize, cellSize])

def drawGrid(m: int = 15, n: int = 15):
    for row in grid:
        for col in row:
            draw_rectangle(grid_turtle, col[0], col[1], col[2], col[3])
    window.update()