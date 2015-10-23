# -*- coding: utf-8 -*-

import numpy as np

class move_missionary():
    def __init__(self):
        self.init = [3, 3, 1]
    
    def go_to(self, state, num_m, num_w):
        next_state = state
        next_state[0] -= num_m
        next_state[1] -= num_w
        next_state[2] -= 1
        return next_state
        
    def come_back(self, state, num_m, num_w):
        next_state = state
        next_state[0] += num_m
        next_state[1] += num_w
        next_state[2] += 1
        return next_state
    
    def win_or_defeat(self, next_state):
        if next_state[0] >= next_state[1] and next_state[0] != 0:
            return 2
        elif next_state[0] == 0:
            return 1
        else:
            return 0
    
    def breadth_first_search(self):
        init = self.init
        next_group = [init]
        evl = 0
        time = 0
        cost = 0
        
        while evl < 1:
            group = next_group
            next_group = []
            if cost%2 == 0:
                for i in range(len(group)): 
                    state = group[i]
                    for j in range(state[0]+1):
                        for k in range(state[1]+1):
                            place = []
                            place.append([state[0], state[1], state[2]])
                            if j + k < 3:
                                next_state = self.go_to(place[0], j, k)
                                win_or_defeat = self.win_or_defeat(next_state)
                                if win_or_defeat == 1:
                                    evl = 1
                                    return next_state, cost, time
                                elif win_or_defeat == 2:
                                    next_group.append(next_state) 
                            time += 1
            else:
                for i in range(len(group)): 
                    state = group[i]
                    for j in range(3-state[0]):
                        for k in range(3-state[1]):
                            place = []
                            place.append([state[0], state[1], state[2]])
                            if j + k <= 2:
                                next_state = self.come_back(place[0], j, k)
                                win_or_defeat = self.win_or_defeat(next_state)
                                if win_or_defeat == 2:
                                    next_group.append(next_state) 
                            time += 1
                
            cost += 1
            print next_group
    
    def cost(self, state, pre_cost):
        return pre_cost + 1 + state[0] - state[1]
    
    def minimum(self, possible_list):
        possible_list = np.array(possible_list)
        index = np.where(possible_list == possible_list.min())
        i = np.random.choice(index[0])
        return possible_list.min(), possible_list[i]
    
    def A_star(self): #ヒューリスティック関数はh=こちらの岸にいる宣教師ー狼
        init = self.init
        next_group = [init]
        possible_list = [0]
        evl = 0
        time = 0
        
        while evl < 1:
            group = next_group
            pre_cost, index = self.minimum(possible_list)
            state = next_group[index]
            next_group = []
            if state[2] == 1:
                for i in range(len(group)): 
                    state = group[i]
                    for j in range(state[0]+1):
                        for k in range(state[1]+1):
                            place = []
                            place.append([state[0], state[1], state[2]])
                            if j + k < 3 and state[0] >= state[1]:
                                next_state = self.go_to(place[0], j, k)
                                win_or_defeat = self.win_or_defeat(next_state)
                                print place[0]
                                if win_or_defeat == 1:
                                    evl = 1
                                    return next_state, pre_cost, time
                                elif win_or_defeat == 2:
                                    f = self.cost(state, pre_cost)
                                    next_group.append(next_state) 
                                    possible_list.append(f) 
                                else:
                                    next_group.append(next_state) 
                                    possible_list.append(1000) 
                                    print "Failed"
                                    
                            time += 1
            else:
                for i in range(len(group)): 
                    state = group[i]
                    for j in range(4-state[0]):
                        for k in range(4-state[1]):
                            place = []
                            place.append([state[0], state[1], state[2]])
                            if j + k < 3 and state[0] >= state[1]:
                                next_state = self.come_back(place[0], j, k)
                                win_or_defeat = self.win_or_defeat(next_state)
                                if win_or_defeat == 1:
                                    evl = 1
                                elif win_or_defeat == 2:
                                    f = self.cost(state, pre_cost)
                                    next_group.append(next_state) 
                                    possible_list.append(f) 
                                else:
                                    next_group.append(next_state) 
                                    possible_list.append(1000) 
                                    
                            time += 1