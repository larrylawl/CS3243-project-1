import os
import sys
from random import randrange
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import CS3243_P1_49_2 as manhattan
import CS3243_P1_49_3 as euclidean
import CS3243_P1_49_4 as linear_conf_manhattan

def random_insert(lst, item):
    lst.insert(randrange(len(lst)+1), item)

class Actions:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    ACTIONS = (UP, DOWN, LEFT, RIGHT)

    @staticmethod
    def are_opposite_actions(action, latest_action):
        if action == Actions.DOWN:
            return latest_action == Actions.UP
        if action == Actions.UP:
            return latest_action == Actions.DOWN
        if action == Actions.RIGHT:
            return latest_action == Actions.LEFT
        if action == Actions.LEFT:
            return latest_action == Actions.RIGHT

    @staticmethod
    def is_legal_action(k, blank_tile, action):
        if blank_tile[0] == 0 and blank_tile[1] == 0:
            return action != Actions.DOWN and action != Actions.RIGHT
        elif blank_tile[0] == 0 and blank_tile[1] == k - 1:
            return action != Actions.DOWN and action != Actions.LEFT
        elif blank_tile[0] == k - 1 and blank_tile[1] == 0:
            return action != Actions.UP and action != Actions.RIGHT
        elif blank_tile[0] == k - 1 and blank_tile[1] == k - 1:
            return action != Actions.UP and action != Actions.LEFT
        elif blank_tile[0] == 0:
            return action != Actions.DOWN
        elif blank_tile[0] == k -1:
            return action != Actions.UP
        elif blank_tile[1] == 0:
            return action != Actions.RIGHT
        elif blank_tile[1] == k -1:
            return action != Actions.LEFT
        else:
            return True          

class KPuzzleGenerator(object): 

    def __init__(self, k, steps):
        self.k = k
        self.steps = steps
        self.goal_state = self.generate_goal_state()

    # Generates a 2D array representing the goal state of a k x k grid
    def generate_goal_state(self):

        max_num = self.k ** 2 - 1
        goal_state = [[0 for i in range(self.k)] for j in range(self.k)]
        
        for i in range(1, max_num + 1):
            goal_state[(i - 1) // self.k][(i - 1) % self.k] = i
        goal_state[self.k - 1][self.k - 1] = 0
        
        return goal_state
    
    def generate_init_state(self):
        actions = []
        new_puzzle = self.goal_state

        # add random actions to actions list until there are k actions
        while len(actions) < self.steps:
            # take a random action
            action_choice = randrange(4)
            action = Actions.ACTIONS[action_choice]

            blank_tile = self.get_zero(new_puzzle)
            if Actions.is_legal_action(self.k, blank_tile, action):
                if actions:
                    latest_action = actions[-1]
                    if not Actions.are_opposite_actions(action, latest_action):
                        actions.append(action)
                        self.move_by_action(new_puzzle, action)
                else:
                    actions.append(action)
                    self.move_by_action(new_puzzle, action)

        return new_puzzle
        
    def move_by_action(self, puzzle, action):
        if action == "DOWN":
            self.move_down(puzzle)
        elif action == "UP":
            self.move_up(puzzle)
        elif action == "LEFT":
            self.move_left(puzzle)
        else:
            self.move_right(puzzle)

    def move_down(self, puzzle):
        x, y = self.get_zero(puzzle)
        puzzle[x][y] = puzzle[x - 1][y]
        puzzle[x - 1][y] = 0
        # self.print_puzzle(puzzle)

    def move_up(self, puzzle):
        x, y = self.get_zero(puzzle)
        puzzle[x][y] = puzzle[x + 1][y]
        puzzle[x + 1][y] = 0
        # self.print_puzzle(puzzle)

    def move_left(self, puzzle):
        x, y = self.get_zero(puzzle)
        puzzle[x][y] = puzzle[x][y + 1]
        puzzle[x][y + 1] = 0 
        # self.print_puzzle(puzzle)

    def move_right(self, puzzle):
        x, y = self.get_zero(puzzle)
        puzzle[x][y] = puzzle[x][y - 1]
        puzzle[x][y - 1] = 0
        # self.print_puzzle(puzzle)

    def print_puzzle(self, puzzle):
        size = len(puzzle)
        for i in range(size):
            print(puzzle[i])

    def get_zero(self, puzzle):
            x, y = None, None
            for i in range(len(puzzle)):
                for j in range(len(puzzle)):
                    if puzzle[i][j] == 0:
                        x, y = i, j
                        break
                if x != None:
                    break
            return x, y


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()

    def solve(self):
        #TODO
        # implement your search algorithm here
        
        return ["LEFT", "RIGHT"] # sample output 

    # you may add more functions if you think is useful

def plotRunTimes(dim_3_tuple, dim_4_tuple, dim_5_tuple):

    fig = plt.figure()

    # Add a legend
    plt.legend()
    
    # Prepare the x-axis
    x = range(30)

    ########## 3 X 3 Graph ##########
    plt.subplot(1, 3, 1)

    # Name the title
    plt.title("3 X 3 Puzzle")

    # Name the axes
    plt.xlabel("Steps to Goal State")
    plt.ylabel("Time Taken")


    # Plot the data
    plt.plot(x, dim_3_tuple[0], label='Manhattan Distance')
    plt.plot(x, dim_3_tuple[1], label='Euclidean Distance')
    plt.plot(x, dim_3_tuple[2], label='Manhattan Distance + 2(Linear Conflicts)')

    ########## 4 X 4 Graph ##########
    plt.subplot(1, 3, 2)
    
    # Name the title
    plt.title("4 x 4 Puzzle")

    # Name the axes
    plt.xlabel("Steps to Goal State")
    plt.ylabel("Time Taken")

    # Plot the data
    plt.plot(x, dim_4_tuple[0], label='Manhattan Distance')
    plt.plot(x, dim_4_tuple[1], label='Euclidean Distance')
    plt.plot(x, dim_4_tuple[2], label='Manhattan Distance + 2(Linear Conflicts)')

    ########## 5 X 5 Graph ##########
    plt.subplot(1, 3, 3)
    
    # Name the title
    plt.title("5 x 5 Puzzle")

    # Name the axes
    plt.xlabel("Steps to Goal State")
    plt.ylabel("Time Taken")

    # Plot the data
    plt.plot(x, dim_5_tuple[0], label='Manhattan Distance')
    plt.plot(x, dim_5_tuple[1], label='Euclidean Distance')
    plt.plot(x, dim_5_tuple[2], label='Manhattan Distance + 2(Linear Conflicts)')

    plt.show()


def getRunTimesForKPuzzle(k):
    m_time = []
    e_time = []
    lc_m_time = []

    for steps in range(1, 31):
        print("/////////////////////  dimension:" + str(k) + " with "+ str(steps) + "steps  ////////////////")
        m_30_times = []
        e_30_times = []
        lc_m_30_times = []

        for i in range (1, 31):
            puzzleGenerator = KPuzzleGenerator(k, steps)
            goal_state = puzzleGenerator.generate_goal_state()
            init_state = puzzleGenerator.generate_init_state()

            m_puzzle = manhattan.Puzzle(init_state, goal_state)
            e_puzzle = euclidean.Puzzle(init_state, goal_state)
            lc_m_puzzle = linear_conf_manhattan.Puzzle(init_state, goal_state)

            m_30_times.append(m_puzzle.getSolutionTime())
            e_30_times.append(e_puzzle.getSolutionTime())
            lc_m_30_times.append(lc_m_puzzle.getSolutionTime())

        m_ave_time = np.mean(m_30_times)
        e_ave_time = np.mean(e_30_times)
        lc_m_ave_time = np.mean(lc_m_30_times)

        m_time.append(m_ave_time)
        e_time.append(e_ave_time)
        lc_m_time.append(lc_m_ave_time)
    
    return (m_time, e_time, lc_m_time)


if __name__ == "__main__":
    dim_3_tuple = getRunTimesForKPuzzle(3)
    dim_4_tuple = getRunTimesForKPuzzle(4)
    dim_5_tuple = getRunTimesForKPuzzle(5)

    plotRunTimes(dim_3_tuple, dim_4_tuple, dim_5_tuple)