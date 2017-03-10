import numpy as np
import math
# Class Defination of Tile Coding
class TileCoding:
    def __init__(self, tiling_num, tiling_size, tile_length, space_length):
        self.tiling_num = tiling_num
        self.tiling_size = tiling_size
        self.tile_length = tile_length
        self.space_length = space_length
        self.movement = -(tiling_size * tile_length - space_length)/tiling_num
    def gen_code(self, x, y):
        tileIndices = []
        original_x = 0.0
        original_y = 0.0
        for i in range(0, self.tiling_num):
            grid_x = math.floor((x - original_x)/self.tile_length)
            grid_y = math.floor((y - original_y)/self.tile_length)
            tileIndices.append(grid_x * self.tiling_size + grid_y)
            original_x += self.movement
            original_y += self.movement
        return tileIndices
class CliffWalking:
    def __init__(self, width = 100, height = 100):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
    def resetPosition(self):
        self.x = 0
        self.y = 0
    def getReward(self):
        rew = -1
        if self.y == 0 and self.x == self.width - 1:
            rew = 100
        elif self.y == 0 and self.x > 0 and self.x < self.width - 1:
            #cliff
            self.resetPosition()
            rew = -100
        else:
            rew = -1
        return rew
    def move(self, moveType):
        if moveType == 'u':
            if self.y < self.height - 1:
                self.y += 1
        elif moveType == 'd':
            if self.y > 0:
                self.y -= 1
        elif moveType == 'r':
            if self.x < self.width - 1:
                self.x += 1
        elif moveType == 'l':
            if self.x > 0:
                self.x -= 1
        return self.getReward()
    def isEnd(self):
        return self.x > 0 and self.y == 0
    def getPosition(self):
        return [self.x, self.y]
actions = ['u', 'd', 'r', 'l']
epsilon = 0.1
#Q Learning
def qLearning_without_tileCoding(cw, width, height, avgR, iterator, max_iter):
    q = np.zeros((width, height, 4))
    G = 0.0
    i = 0
    while not cw.isEnd():
        s0 = cw.getPosition()
        a = q[s0[0], s0[1]].argmax()
        if np.random.random() < epsilon:
            a = np.random.choice(range(4))
        r = cw.move(actions[a])
        G += r
        i += 1
        if i <= max_iter:
            avgR[i] = G / i
        s1 = cw.getPosition()
        q[s0[0], s0[1], a] +=  0.1 * (r + 0.8 * q[s1[0], s1[1]].max() - q[s0[0], s0[1], a])
    iterator.append(i)
#Q Learning
def qLearning_with_tileCoding(cw, avgR, iterator, max_iter):
    q = {}
    G = 0.0
    i = 0
    tileCoder = TileCoding(4, 12, 12, 100)
    while not cw.isEnd():
        s0 = cw.getPosition()
        tc0 = tileCoder.gen_code(s0[0], s0[1])
        key = ' '.join([str(int(term)) for term in tc0])
        if not key in q:
            q[key] = np.zeros(4)
        a = q[key].argmax()
        if np.random.random() < epsilon:
            a = np.random.choice(range(4))
        r = cw.move(actions[a])
        G += r
        i += 1
        if i <= max_iter:
            avgR[i] = G / i
        s1 = cw.getPosition()
        tc1 = tileCoder.gen_code(s1[0], s1[1])
        key = ' '.join([str(int(term)) for term in tc1])
        if not key in q:
            q[key] = np.zeros(4)
        q[key][a] +=  0.1 * (r + 0.8 * q[key].max() - q[key][a])
    iterator.append(i)
import time
#initialize CliffWalking
cw = CliffWalking()
time1 = []
ite1 = []
avgR1 = [[0.0]*50] * 10
time2 = []
ite2 = []
avgR2 = [[0.0]*50] * 10

for i in range(10):
    cw.resetPosition()
    begin = time.time()
    #qLearning_without_tileCoding(cw, 100, 100, avgR1[i], ite1, 49)
    end = time.time()
    time1.append(end - begin)
    cw.resetPosition()
    begin = time.time()
    qLearning_with_tileCoding(cw, avgR2[i], ite2, 10)
    end = time.time()
    time2.append(end - begin)
    print i