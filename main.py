# Add the implementation logic code here
from data import game_data
from graphics import defineGrid, drawGrid, t, renderCollection
import random

# class playerData:
#     def __init__(self):
#         self.data = []
#         self.size = 0

playerCount = 2
collectionSize = 8 # n
playerData = []
gotian = game_data["gotian"][:] #list with chars (copy made so original gotian isn't affected)
score_dict = game_data["alphabet_score"] #score against alphabet in nested dict
words = game_data["words"] #list with possible words

defineGrid()
drawGrid()

def setPlayers(playerData, playerCount, collectionSize):
    for i in range(playerCount):
        name = t.textinput("Player Name", f"Enter name for player {i + 1}:")
        playerData.append({"name": name, "score": 0, "collection": [], "words": []})

        for j in range(collectionSize):
            random_goti = random.choice(gotian)
            gotian.remove(random_goti)
            playerData[i]["collection"].append({"goti": random_goti, "coords":[]})

        renderCollection(playerData[i], i)

setPlayers(playerData, playerCount, collectionSize)

t.done()

#1. words need to be made with all conecting boxes
#2. increase scrore based on number of full words completed
#3. move words inserted back to the options set if not all directions satisfy a word 
#   in the making