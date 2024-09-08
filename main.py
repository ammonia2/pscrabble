# Add the implementation logic code here
from data import game_data
from graphics import defineGrid, drawGrid, t

gotian = game_data["gotian"] #list with chars
score_dict = game_data["alphabet_score"] #score against alphabet in nested dict
words = game_data["words"] #list with possible words

defineGrid()
drawGrid()

t.done()