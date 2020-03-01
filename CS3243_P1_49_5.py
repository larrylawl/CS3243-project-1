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
        past_states = set()
        actions = []
        new_puzzle = self.goal_state

        # add random actions to actions list until there are k actions
        while len(actions) < self.steps:
            # take a random action
            action_choice = randrange(4)
            action = Actions.ACTIONS[action_choice]

            blank_tile = self.get_zero(new_puzzle)
            if Actions.is_legal_action(self.k, blank_tile, action):
                if len(actions) > 0:
                    latest_action = actions[-1]
                    if not Actions.are_opposite_actions(action, latest_action):
                        new_puzzle = self.move_by_action(new_puzzle, action)
                        actions.append(action)

                # first move
                else:
                    actions.append(action)
                    new_puzzle = self.move_by_action(new_puzzle, action)
                    past_states.add(self.puzzle_to_string(new_puzzle))

        print(actions)
        return new_puzzle
    
    def puzzle_to_string(self, puzzle):
        result = "[" + ", ".join(str(x) for x in puzzle) + "]"
        result = "".join(str(x) for x in puzzle)
        return result
        
        
    def move_by_action(self, puzzle, action):
        new_puzzle = [row[:] for row in puzzle]
        if action == "DOWN":
            self.move_down(new_puzzle)
        elif action == "UP":
            self.move_up(new_puzzle)
        elif action == "LEFT":
            self.move_left(new_puzzle)
        else:
            self.move_right(new_puzzle)
        return new_puzzle

    def move_down(self, puzzle):
        x, y = self.get_zero(puzzle)
        puzzle[x][y] = puzzle[x - 1][y]
        puzzle[x - 1][y] = 0

    def move_up(self, puzzle):
        x, y = self.get_zero(puzzle)
        puzzle[x][y] = puzzle[x + 1][y]
        puzzle[x + 1][y] = 0

    def move_left(self, puzzle):
        x, y = self.get_zero(puzzle)
        puzzle[x][y] = puzzle[x][y + 1]
        puzzle[x][y + 1] = 0 

    def move_right(self, puzzle):
        x, y = self.get_zero(puzzle)
        puzzle[x][y] = puzzle[x][y - 1]
        puzzle[x][y - 1] = 0

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

def plotRunTimes(dim_3_nodes, dim_3_frontier):

    fig = plt.figure()

    # Prepare the x-axis
    x = range(1, 28)

    plt.subplot(1, 2, 1)

    # Name the title
    plt.title("Time Complexity")

    # Name the axes
    plt.xlabel("Steps to Goal State")
    plt.ylabel("Nodes Explored")

    # show all values on the x-axis
    plt.xticks(x)

    # show grid
    plt.grid(axis='y')


    # Plot the data
    plt.plot(x, dim_3_nodes[0], label='Manhattan Distance')
    plt.plot(x, dim_3_nodes[1], label='Euclidean Distance')
    plt.plot(x, dim_3_nodes[2], label='Manhattan Distance + 2(Linear Conflicts)')

    # Place the legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1))

    plt.subplot(1, 2, 2)
    
    # Name the title
    plt.title("Space Complexity")

    # Name the axes
    plt.xlabel("Steps to Goal State")
    plt.ylabel("Maximum Frontier Size")

    # show all values on the x-axis
    plt.xticks(x)

    # show grid
    plt.grid(axis='y')

    # Plot the data
    plt.plot(x, dim_3_frontier[0], label='Manhattan Distance')
    plt.plot(x, dim_3_frontier[1], label='Euclidean Distance')
    plt.plot(x, dim_3_frontier[2], label='Manhattan Distance + 2(Linear Conflicts)')
    
    plt.show()


def getNodesExploredAndMaxFrontierSizeForKPuzzle(k):
    m_nodes = []
    e_nodes = []
    lc_m_nodes = []

    m_max_frontier = []
    e_max_frontier = []
    lc_m_max_frontier = []

    for steps in range(1, 28):
        m_30_nodes = []
        e_30_nodes = []
        lc_m_30_nodes = []

        m_30_max_frontier = []
        e_30_max_frontier = []
        lc_m_30_max_frontier = []

        for i in range(10):

            incorrectNumberOfSteps = True
            while incorrectNumberOfSteps:
                print("\n/////////////////////  dimension:" + str(k) + " with "+ str(steps) + "steps" + str(i) + " times  ////////////////")
                puzzleGenerator = KPuzzleGenerator(k, steps)
                goal_state = puzzleGenerator.generate_goal_state()
                init_state = puzzleGenerator.generate_init_state()

                m_puzzle = manhattan.Puzzle(init_state, goal_state)
                e_puzzle = euclidean.Puzzle(init_state, goal_state)
                lc_m_puzzle = linear_conf_manhattan.Puzzle(init_state, goal_state)

                m_puzzle.solve()
                e_puzzle.solve()
                lc_m_puzzle.solve()

                m_steps = len(m_puzzle.actions)
                e_steps = len(e_puzzle.actions)
                lc_m_steps = len(lc_m_puzzle.actions)
            
                if (m_steps == steps and e_steps == steps and lc_m_steps == steps):

                    incorrectNumberOfSteps = False

                    m_30_nodes.append(len(m_puzzle.past_states))
                    e_30_nodes.append(len(e_puzzle.past_states))
                    lc_m_30_nodes.append(len(lc_m_puzzle.past_states))

                    m_30_max_frontier.append(m_puzzle.frontier_size)
                    e_30_max_frontier.append(e_puzzle.frontier_size)
                    lc_m_30_max_frontier.append(lc_m_puzzle.frontier_size)
                else:
                    print("!!!!!!!!!!!!!!!!!!REDO!!!!!!!!!!!!!!!!!!!\n")

        m_ave_nodes = np.mean(m_30_nodes)
        e_ave_nodes = np.mean(e_30_nodes)
        lc_m_ave_nodes = np.mean(lc_m_30_nodes)

        m_ave_max_frontier = np.mean(m_30_max_frontier)
        e_ave_max_frontier = np.mean(e_30_max_frontier)
        lc_m_ave_max_frontier = np.mean(lc_m_30_max_frontier)

        m_nodes.append(m_ave_nodes)
        e_nodes.append(e_ave_nodes)
        lc_m_nodes.append(lc_m_ave_nodes)

        m_max_frontier.append(m_ave_max_frontier)
        e_max_frontier.append(e_ave_max_frontier)
        lc_m_max_frontier.append(lc_m_ave_max_frontier)
    
    nodes_tuple = (m_nodes, e_nodes, lc_m_nodes)
    max_frontier_tuple = (m_max_frontier, e_max_frontier, lc_m_max_frontier)

    return (nodes_tuple, max_frontier_tuple)


if __name__ == "__main__":
    dim_3_tuples = getNodesExploredAndMaxFrontierSizeForKPuzzle(3)

    plotRunTimes(dim_3_tuples[0], dim_3_tuples[1])
