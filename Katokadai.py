# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

class Katokadai():
    def __init__(self):
        self.start = [11, 3]
        self.goal = [11, 13]
    
    def cells(self):
        cell = np.loadtxt( "cell.csv", delimiter=","  )
        cells = []
        for i in range(len(cell)):
            cells.append([])

        for i in range(len(cell)):
            for j in range(len(cell[i])):
                cells[-i].append(cell[i-1][j])
        return cells 
        
    
    def log(self):
        log = []
        for i in range(12):
            log.append([0 for i in range(17)])
        return log

    def cost_function(self, place_0, place_1, log):
        cells = self.cells()
        if log[place_1[0]][place_1[1]] == 0:
            mark = cells[place_1[0]][place_1[1]]
            if mark == 0:
                return log[place_0[0]][place_0[1]] + 1
            elif mark == 1:
                return log[place_0[0]][place_0[1]] + 3
            else:
                return 1000
        else:
            return log[place_1[0]][place_1[1]]
        
    def cost_function2(self, place_0, place_1, log):
        cells = self.cells()
        if log[place_1[0]][place_1[1]] == 0:
            mark = cells[place_1[0]][place_1[1]]
            if mark == 0:
                return 1
            elif mark == 1:
                return 3
            else:
                return 1000
        else:
            return log[place_1[0]][place_1[1]]
        
    def manhattan(self, present_place, goal):
        distance_x = math.fabs(present_place[0] - goal[0])
        distance_y = math.fabs(present_place[1] - goal[1])
        distance = distance_x + distance_y 
        return distance
    
    def minimum(self, log):
        log = np.array(log)
        log1 = log
        for i in range(len(log1)):
            for j in range(len(log1[i])):
                if log1[i][j] == 0:
                    log1[i][j] = 1000
        indexies = np.where(log1 == log1.min())
        index = [indexies[0][0], indexies[1][0]]

        return index                      
    
    def breadth_first_search(self): 
        cells = self.cells()
        log = self.log()
        depth = 0
        # 上、下、左、右の順に評価する。
        while log[11][13] == 0:
            same_depth = []
            if depth == 0:
                same_depth.append(self.start)
            else:
                for i in range(len(cells)):
                    for j in range(len(cells[i])):
                        if log[i][j] == depth:
                            same_depth.append([i, j])
            for past_place in same_depth: 
                up = [past_place[0] + 1, past_place[1]]
                down = [past_place[0] - 1, past_place[1]]
                left = [past_place[0], past_place[1]-1]
                right = [past_place[0], past_place[1]+1]
                if past_place[0] == 11 and (past_place[1] != 0 and past_place[1] != 16): #上の辺
                    log[down[0]][down[1]] = self.cost_function(past_place, down, log)
                    log[left[0]][left[1]] = self.cost_function(past_place, left, log)
                    log[right[0]][right[1]] = self.cost_function(past_place, right, log)
                elif past_place[0] == 0 and (past_place[1] != 0 and past_place[1] != 16): #下の辺
                    log[up[0]][up[1]] = self.cost_function(past_place, up, log)
                    log[left[0]][left[1]] = self.cost_function(past_place, left, log)
                    log[right[0]][right[1]] = self.cost_function(past_place, right, log)
                elif (past_place[0] != 0 and past_place[0] != 11) and past_place[1] == 0: #左の辺
                    log[up[0]][up[1]] = self.cost_function(past_place, up, log)
                    log[down[0]][down[1]] = self.cost_function(past_place, down, log)
                    log[right[0]][right[1]] = self.cost_function(past_place, right, log)
                elif (past_place[0] != 0 and past_place[0] != 11) and past_place[1] == 16: #右の辺
                    log[up[0]][up[1]] = self.cost_function(past_place, up, log)
                    log[down[0]][down[1]] = self.cost_function(past_place, down, log)
                    log[left[0]][left[1]] = self.cost_function(past_place, left, log)
                elif past_place[0] == 11 and past_place[1] == 0: #左上隅
                    log[down[0]][down[1]] = self.cost_function(past_place, down, log)
                    log[right[0]][right[1]] = self.cost_function(past_place, right, log)
                elif past_place[0] == 0 and past_place[1] == 0: #左下隅
                    log[up[0]][up[1]] = self.cost_function(past_place, up, log)
                    log[right[0]][right[1]] = self.cost_function(past_place, right, log)
                elif past_place[0] == 11 and past_place[1] == 16: #右上隅
                    log[down[0]][down[1]] = self.cost_function(past_place, down, log)
                    log[left[0]][left[1]] = self.cost_function(past_place, left, log)
                elif past_place[0] == 0 and past_place[1] == 16: #右下隅
                    log[up[0]][up[1]] = self.cost_function(past_place, up, log)
                    log[left[0]][left[1]] = self.cost_function(past_place, left, log) 
                else:
                    log[up[0]][up[1]] = self.cost_function(past_place, up, log)
                    log[down[0]][down[1]] = self.cost_function(past_place, down, log)
                    log[left[0]][left[1]] = self.cost_function(past_place, left, log)
                    log[right[0]][right[1]] = self.cost_function(past_place, right, log)
            depth += 1
        return log
    
    def A_star(self):
        cells = self.cells()
        log = self.log()
        past_place = self.start
        before_past_place = [0, 0]
        morebefore_past_place = [-1,-1]
        goal = self.goal
        k = 0
        # 上、下、左、右の順に評価する。
        while log[11][13] == 0:    
            up = [past_place[0] + 1, past_place[1]]
            down = [past_place[0] - 1, past_place[1]]
            left = [past_place[0], past_place[1]-1]
            right = [past_place[0], past_place[1]+1]
            morebefore_past_place = before_past_place
            before_past_place = past_place
            if past_place[0] == 11 and (past_place[1] != 0 and past_place[1] != 16): #上の辺
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(past_place, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(past_place, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(past_place, goal)
                past_place = down
                if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                    past_place = left
                if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                    past_place = right 
            elif past_place[0] == 0 and (past_place[1] != 0 and past_place[1] != 16): #下の辺
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(past_place, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(past_place, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(past_place, goal)
                past_place = up
                if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                    past_place = left
                if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                    past_place = right 
            elif (past_place[0] != 0 and past_place[0] != 11) and past_place[1] == 0: #左の辺
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(past_place, goal)
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(past_place, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(past_place, goal)
                past_place = up
                if log[down[0]][down[1]] < log[past_place[0]][past_place[1]]:
                    past_place = down
                if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                    past_place = right 
            elif (past_place[0] != 0 and past_place[0] != 11) and past_place[1] == 16: #右の辺
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(past_place, goal)
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(past_place, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(past_place, goal)
                past_place = up
                if log[down[0]][down[1]] < log[past_place[0]][past_place[1]]:
                    past_place = down
                if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                    past_place = left
            elif past_place[0] == 11 and past_place[1] == 0: #左上隅
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(past_place, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(past_place, goal)
                past_place = down
                if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                    past_place = right 
            elif past_place[0] == 0 and past_place[1] == 0: #左下隅
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(past_place, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(past_place, goal)
                past_place = up
                if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                    past_place = right
            elif past_place[0] == 11 and past_place[1] == 16: #右上隅
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(past_place, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(past_place, goal)
                past_place = down
                if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                    past_place = left 
            elif past_place[0] == 0 and past_place[1] == 16: #右下隅
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(past_place, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(past_place, goal) 
                past_place = up
                if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                    past_place = left 
            else:
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(past_place, goal)
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(past_place, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(past_place, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(past_place, goal)
                past_place = up
                if log[down[0]][down[1]] < log[past_place[0]][past_place[1]]:
                    past_place = down
                if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                    past_place = left
                if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                    past_place = right
            if past_place == morebefore_past_place:
                if past_place[1] != 16:
                    right = [past_place[0], past_place[1]+1]
                    if log[past_place[0]][past_place[1]] == log[right[0]][right[1]]:
                        log[past_place[0]][past_place[1]] += 100
                        past_place = right
                    else:
                        log[past_place[0]][past_place[1]] += 100
                        past_place = self.minimum(log)
                else:
                    log[past_place[0]][past_place[1]] += 100
                    past_place = self.minimum(log)
            k += 1
            if k == 200:
                break
            
        return log
    
    def LRTA_star1(self):
        cells = self.cells()
        log = self.log()
        past_place = self.start
        before_past_place = [0, 0]
        morebefore_past_place = [-1,-1]
        goal = self.goal
        k = 0
        h = self.log()
        # 上、下、左、右の順に評価する。
        while log[11][13] == 0:    
            up = [past_place[0] + 1, past_place[1]]
            down = [past_place[0] - 1, past_place[1]]
            left = [past_place[0], past_place[1]-1]
            right = [past_place[0], past_place[1]+1]
            morebefore_past_place = before_past_place
            before_past_place = past_place
            h[before_past_place[0]][before_past_place[1]] = h[past_place[0]][past_place[1]]
            if past_place[0] == 11 and (past_place[1] != 0 and past_place[1] != 16): #上の辺
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(down, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(left, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(right, goal)
                past_place = down
                if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                    past_place = left
                if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                    past_place = right 
            elif past_place[0] == 0 and (past_place[1] != 0 and past_place[1] != 16): #下の辺
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(up, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(left, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(right, goal)
                past_place = up
                if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                    past_place = left
                if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                    past_place = right 
            elif (past_place[0] != 0 and past_place[0] != 11) and past_place[1] == 0: #左の辺
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(up, goal)
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(down, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(right, goal)
                past_place = up
                if log[down[0]][down[1]] < log[past_place[0]][past_place[1]]:
                    past_place = down
                if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                    past_place = right 
            elif (past_place[0] != 0 and past_place[0] != 11) and past_place[1] == 16: #右の辺
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(up, goal)
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(down, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(left, goal)
                past_place = up
                if log[down[0]][down[1]] < log[past_place[0]][past_place[1]]:
                    past_place = down
                if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                    past_place = left
            elif past_place[0] == 11 and past_place[1] == 0: #左上隅
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(down, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(right, goal)
                past_place = down
                if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                    past_place = right 
            elif past_place[0] == 0 and past_place[1] == 0: #左下隅
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(up, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(right, goal)
                past_place = up
                if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                    past_place = right
            elif past_place[0] == 11 and past_place[1] == 16: #右上隅
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(down, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(left, goal)
                past_place = down
                if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                    past_place = left 
            elif past_place[0] == 0 and past_place[1] == 16: #右下隅
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(up, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(left, goal) 
                past_place = up
                if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                    past_place = left 
            else:
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(up, goal)
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(down, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(left, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(right, goal)
                past_place = up
                if log[down[0]][down[1]] < log[past_place[0]][past_place[1]]:
                    past_place = down
                if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                    past_place = left
                if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                    past_place = right
            if past_place == morebefore_past_place:
                if past_place[1] != 16:
                    right = [past_place[0], past_place[1]+1]
                    if log[past_place[0]][past_place[1]] == log[right[0]][right[1]]:
                        log[past_place[0]][past_place[1]] += 100
                        past_place = right
                    else:
                        log[past_place[0]][past_place[1]] += 100
                        past_place = self.minimum(log)
                else:
                    log[past_place[0]][past_place[1]] += 100
                    past_place = self.minimum(log)
            k += 1
            if k == 200:
                break
            
        return log, h
    
    def LRTA_star2(self):
        cells = self.cells()
        before_past_place = [0, 0]
        morebefore_past_place = [-1,-1]
        goal = self.goal
        k = 0
        log1, h = self.LRTA_star1()
        # 上、下、左、右の順に評価する。
        while k < 7:
            log = self.log()
            path = self.log()
            past_place = self.start
            while log[11][13] == 0:    
                up = [past_place[0] + 1, past_place[1]]
                down = [past_place[0] - 1, past_place[1]]
                left = [past_place[0], past_place[1]-1]
                right = [past_place[0], past_place[1]+1]
                morebefore_past_place = before_past_place
                before_past_place = past_place
                h[before_past_place[0]][before_past_place[1]] = h[past_place[0]][past_place[1]]
                if past_place[0] == 11 and (past_place[1] != 0 and past_place[1] != 16): #上の辺
                    log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + h[down[0]][down[1]]
                    log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + h[left[0]][left[1]]
                    log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + h[right[0]][right[1]]
                    past_place = down
                    if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                        past_place = left
                    if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                        past_place = right 
                elif past_place[0] == 0 and (past_place[1] != 0 and past_place[1] != 16): #下の辺
                    log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + h[up[0]][up[1]]
                    log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + h[left[0]][left[1]]
                    log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + h[right[0]][right[1]]
                    past_place = up
                    if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                        past_place = left
                    if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                        past_place = right 
                elif (past_place[0] != 0 and past_place[0] != 11) and past_place[1] == 0: #左の辺
                    log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + h[up[0]][up[1]]
                    log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + h[down[0]][down[1]]
                    log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + h[right[0]][right[1]]
                    past_place = up
                    if log[down[0]][down[1]] < log[past_place[0]][past_place[1]]:
                        past_place = down
                    if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                        past_place = right 
                elif (past_place[0] != 0 and past_place[0] != 11) and past_place[1] == 16: #右の辺
                    log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + h[up[0]][up[1]]
                    log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + h[down[0]][down[1]]
                    log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + h[left[0]][left[1]]
                    past_place = up
                    if log[down[0]][down[1]] < log[past_place[0]][past_place[1]]:
                        past_place = down
                    if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                        past_place = left
                elif past_place[0] == 11 and past_place[1] == 0: #左上隅
                    log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + h[down[0]][down[1]]
                    log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + h[right[0]][right[1]]
                    past_place = down
                    if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                        past_place = right 
                elif past_place[0] == 0 and past_place[1] == 0: #左下隅
                    log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + h[up[0]][up[1]]
                    log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + h[right[0]][right[1]]
                    past_place = up
                    if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                        past_place = right
                elif past_place[0] == 11 and past_place[1] == 16: #右上隅
                    log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + h[down[0]][down[1]]
                    log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + h[left[0]][left[1]]
                    past_place = down
                    if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                        past_place = left 
                elif past_place[0] == 0 and past_place[1] == 16: #右下隅
                    log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + h[up[0]][up[1]]
                    log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + h[left[0]][left[1]]
                    past_place = up
                    if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                        past_place = left 
                else:
                    log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + h[up[0]][up[1]]
                    log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + h[down[0]][down[1]]
                    log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + h[left[0]][left[1]]
                    log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + h[right[0]][right[1]]
                    past_place = up
                    if log[down[0]][down[1]] < log[past_place[0]][past_place[1]]:
                        past_place = down
                    if log[left[0]][left[1]] < log[past_place[0]][past_place[1]]:
                        past_place = left
                    if log[right[0]][right[1]] < log[past_place[0]][past_place[1]]:
                        past_place = right
                if past_place == morebefore_past_place:
                    if past_place[1] != 16:
                        right = [past_place[0], past_place[1]+1]
                        if log[past_place[0]][past_place[1]] == log[right[0]][right[1]]:
                            log[past_place[0]][past_place[1]] += 100
                            past_place = right
                        else:
                            log[past_place[0]][past_place[1]] += 100
                            past_place = self.minimum(log)
                    else:
                        log[past_place[0]][past_place[1]] += 100
                        past_place = self.minimum(log)
                h = log
                path[past_place[0]][past_place[1]] = 1
            k += 1

        return log, path 
    
    def LRTA_star3(self):
        cells = self.cells()
        log = self.log()
        past_place = self.start
        before_past_place = [0, 0]
        morebefore_past_place = [-1,-1]
        goal = self.goal
        k = 0
        h = self.log()
        # ランダムに評価する
        while log[11][13] == 0:    
            up = [past_place[0] + 1, past_place[1]]
            down = [past_place[0] - 1, past_place[1]]
            left = [past_place[0], past_place[1]-1]
            right = [past_place[0], past_place[1]+1]
            morebefore_past_place = before_past_place
            before_past_place = past_place
            h[before_past_place[0]][before_past_place[1]] = h[past_place[0]][past_place[1]]
            if past_place[0] == 11 and (past_place[1] != 0 and past_place[1] != 16): #上の辺
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(down, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(left, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(right, goal)
                past_place = np.random.choice(down, left, right)
            elif past_place[0] == 0 and (past_place[1] != 0 and past_place[1] != 16): #下の辺
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(up, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(left, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(right, goal)
                past_place = np.random.choice([up, left, right])
            elif (past_place[0] != 0 and past_place[0] != 11) and past_place[1] == 0: #左の辺
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(up, goal)
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(down, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(right, goal)
                past_place = np.random.choice([up, down,right])
            elif (past_place[0] != 0 and past_place[0] != 11) and past_place[1] == 16: #右の辺
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(up, goal)
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(down, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(left, goal)
                past_place = np.random.choice([up, down, left])
            elif past_place[0] == 11 and past_place[1] == 0: #左上隅
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(down, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(right, goal)
                past_place = np.random.choice([down, right])
            elif past_place[0] == 0 and past_place[1] == 0: #左下隅
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(up, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(right, goal)
                past_place = np.random.choice([upright])
            elif past_place[0] == 11 and past_place[1] == 16: #右上隅
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(down, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(left, goal)
                past_place = np.random.choice([down, left])
            elif past_place[0] == 0 and past_place[1] == 16: #右下隅
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(up, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(left, goal) 
                past_place = np.random.choice([up,  left])
            else:
                log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + self.manhattan(up, goal)
                log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + self.manhattan(down, goal)
                log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + self.manhattan(left, goal)
                log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + self.manhattan(right, goal)
                past_place = np.random.choice([up, down, left, right])
            k += 1
            if k == 200:
                break
            
        return log, h
    
    def LRTA_star4(self):
        cells = self.cells()
        before_past_place = [0, 0]
        morebefore_past_place = [-1,-1]
        goal = self.goal
        k = 0
        log1, h = self.LRTA_star3()
        # ランダムに評価する。
        while k < 7:
            log = self.log()
            path = self.log()
            past_place = self.start
            while log[11][13] == 0:    
                up = [past_place[0] + 1, past_place[1]]
                down = [past_place[0] - 1, past_place[1]]
                left = [past_place[0], past_place[1]-1]
                right = [past_place[0], past_place[1]+1]
                morebefore_past_place = before_past_place
                before_past_place = past_place
                h[before_past_place[0]][before_past_place[1]] = h[past_place[0]][past_place[1]]
                if past_place[0] == 11 and (past_place[1] != 0 and past_place[1] != 16): #上の辺
                    log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + h[down[0]][down[1]]
                    log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + h[left[0]][left[1]]
                    log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + h[right[0]][right[1]]
                    past_place = np.random.choice([down, left, right])

                elif past_place[0] == 0 and (past_place[1] != 0 and past_place[1] != 16): #下の辺
                    log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + h[up[0]][up[1]]
                    log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + h[left[0]][left[1]]
                    log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + h[right[0]][right[1]]
                    past_place = np.random.choice([up, left, right])

                elif (past_place[0] != 0 and past_place[0] != 11) and past_place[1] == 0: #左の辺
                    log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + h[up[0]][up[1]]
                    log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + h[down[0]][down[1]]
                    log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + h[right[0]][right[1]]
                    past_place = np.random.choice([up, down, right])
                elif (past_place[0] != 0 and past_place[0] != 11) and past_place[1] == 16: #右の辺
                    log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + h[up[0]][up[1]]
                    log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + h[down[0]][down[1]]
                    log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + h[left[0]][left[1]]
                    past_place = np.random.choice([up, down, left])
                elif past_place[0] == 11 and past_place[1] == 0: #左上隅
                    log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + h[down[0]][down[1]]
                    log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + h[right[0]][right[1]]
                    past_place = np.random.choice([down, right])
                elif past_place[0] == 0 and past_place[1] == 0: #左下隅
                    log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + h[up[0]][up[1]]
                    log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + h[right[0]][right[1]]
                    past_place = np.random.choice([up, right])
                elif past_place[0] == 11 and past_place[1] == 16: #右上隅
                    log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + h[down[0]][down[1]]
                    log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + h[left[0]][left[1]]
                    past_place = np.random.choice([down, left])
                elif past_place[0] == 0 and past_place[1] == 16: #右下隅
                    log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + h[up[0]][up[1]]
                    log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + h[left[0]][left[1]]
                    past_place = np.random.choice([up, left])
                else:
                    log[up[0]][up[1]] = self.cost_function2(past_place, up, log) + h[up[0]][up[1]]
                    log[down[0]][down[1]] = self.cost_function2(past_place, down, log) + h[down[0]][down[1]]
                    log[left[0]][left[1]] = self.cost_function2(past_place, left, log) + h[left[0]][left[1]]
                    log[right[0]][right[1]] = self.cost_function2(past_place, right, log) + h[right[0]][right[1]]
                    past_place = np.random.choice([up, down, left, right])
            k += 1

        return log, path 