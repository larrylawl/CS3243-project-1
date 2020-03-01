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
    
    # Generate the initial state by taking n steps from goal state
    def generate_init_state(self):
        past_states = set()
        actions = []
        new_puzzle = self.goal_state

        # Add random actions to actions list until there are k actions
        while len(actions) < self.steps:
            # Take a random action
            action_choice = randrange(4)
            action = Actions.ACTIONS[action_choice]

            blank_tile = self.get_zero(new_puzzle)

            # Check if the random action is legal and not opposite to the latest action
            if Actions.is_legal_action(self.k, blank_tile, action):
                if len(actions) > 0:
                    latest_action = actions[-1]
                    if not Actions.are_opposite_actions(action, latest_action):
                        new_puzzle = self.move_by_action(new_puzzle, action)
                        actions.append(action)

                # First move
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

def plotRunTimes(nodes, memory, times):

    # Prepare the x-axis
    x = range(1, 26)

    plt.subplot(1, 3, 1)

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
    plt.plot(x, nodes[0], label='Manhattan Distance')
    plt.plot(x, nodes[1], label='Euclidean Distance')
    plt.plot(x, nodes[2], label='Manhattan Distance + 2(Linear Conflicts)')

    # Place the legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1))

    plt.subplot(1, 3, 2)
    
    # Name the title
    plt.title("Space Complexity")

    # Name the axes
    plt.xlabel("Steps to Goal State")
    plt.ylabel("Maximum Nodes in Memory")

    # show all values on the x-axis
    plt.xticks(x)

    # show grid
    plt.grid(axis='y')

    # Plot the data
    plt.plot(x, memory[0], label='Manhattan Distance')
    plt.plot(x, memory[1], label='Euclidean Distance')
    plt.plot(x, memory[2], label='Manhattan Distance + 2(Linear Conflicts)')

    # Place the legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1))

    plt.subplot(1, 3, 3)
    
    # Name the title
    plt.title("Space Complexity")

    # Name the axes
    plt.xlabel("Steps to Goal State")
    plt.ylabel("Actual Time Taken")

    # show all values on the x-axis
    plt.xticks(x)

    # show grid
    plt.grid(axis='y')

    # Plot the data
    plt.plot(x, times[0], label='Manhattan Distance')
    plt.plot(x, times[1], label='Euclidean Distance')
    plt.plot(x, times[2], label='Manhattan Distance + 2(Linear Conflicts)')

    # Place the legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1))


    plt.show()


def getNodesExploredMaxMemorySizeAndTimeForKPuzzle(k):

    # The arrays will store the number of nodes generated for puzzles of steps n
    # where arr[i - 1] contains the number of nodes for step n
    m_nodes = []
    e_nodes = []
    lc_m_nodes = []

    # The arrays will store the max nodes in memory generated for puzzles of steps n
    # where arr[i - 1] contains the max nodes in memory for step n
    m_max_memory_used = []
    e_max_memory_used = []
    lc_m_max_memory_used = []

    # The arrays will store the times generated for puzzles of steps n
    # where arr[i - 1] contains the times for step n
    m_times = []
    e_times = []
    lc_m_times = []

    # Generate puzzles from steps 1 to 25
    for steps in range(1, 26):
        m_30_nodes = []
        e_30_nodes = []
        lc_m_30_nodes = []

        m_30_max_memory_used = []
        e_30_max_memory_used = []
        lc_m_30_max_memory_used = []

        m_30_times = []
        e_30_times = []
        lc_m_30_times = []

        # Generate each puzzle 30 times and take the average of each metric
        for i in range(30):

            # Some puzzles are generated with n number of steps, but the heuristiscs can sometimes take less than n steps to achieve goal state
            # Thus a new puzzle will generate until the solution REALLY takes n steps to goal state
            incorrectNumberOfSteps = True

            while incorrectNumberOfSteps:
                print("\n/////////////////////  dimension:" + str(k) + " with "+ str(steps) + "steps" + str(i) + " times  ////////////////")
                # Generate a goal state and initial state of dimension k x k that should take 'steps' steps to solve
                puzzleGenerator = KPuzzleGenerator(k, steps)
                goal_state = puzzleGenerator.generate_goal_state()
                init_state = puzzleGenerator.generate_init_state()

                # Creates the puzzles for each of the heuristics scripts
                m_puzzle = manhattan.Puzzle(init_state, goal_state)
                e_puzzle = euclidean.Puzzle(init_state, goal_state)
                lc_m_puzzle = linear_conf_manhattan.Puzzle(init_state, goal_state)

                # Solve the puzzles for each of the heuristics scripts
                m_time = m_puzzle.getSolutionTime()
                e_time = e_puzzle.getSolutionTime()
                lc_m_time = lc_m_puzzle.getSolutionTime()

                # Get the number of steps taken to reach goal state
                m_steps = len(m_puzzle.actions)
                e_steps = len(e_puzzle.actions)
                lc_m_steps = len(lc_m_puzzle.actions)
            
                # If the number of steps is truly as what was intended:
                if (m_steps == steps and e_steps == steps and lc_m_steps == steps):

                    incorrectNumberOfSteps = False

                    # Get the number of nodes explored
                    m_30_nodes.append(len(m_puzzle.past_states))
                    e_30_nodes.append(len(e_puzzle.past_states))
                    lc_m_30_nodes.append(len(lc_m_puzzle.past_states))

                    # Get the maximum number of nodes in memory
                    m_30_max_memory_used.append(m_puzzle.nodes_in_memory)
                    e_30_max_memory_used.append(e_puzzle.nodes_in_memory)
                    lc_m_30_max_memory_used.append(lc_m_puzzle.nodes_in_memory)

                    # Get the actual time taken
                    m_30_times.append(m_time)
                    e_30_times.append(e_time)
                    lc_m_30_times.append(lc_m_time)

                else:
                    print("!!!!!!!!!!!!!!!!!!REDO!!!!!!!!!!!!!!!!!!!\n")

        # Get averages of 30 puzzles
        m_ave_nodes = np.mean(m_30_nodes)
        e_ave_nodes = np.mean(e_30_nodes)
        lc_m_ave_nodes = np.mean(lc_m_30_nodes)

        m_ave_max_memory_used = np.mean(m_30_max_memory_used)
        e_ave_max_memory_used = np.mean(e_30_max_memory_used)
        lc_m_ave_max_memory_used = np.mean(lc_m_30_max_memory_used)

        m_ave_times = np.mean(m_30_times)
        e_ave_times = np.mean(e_30_times)
        lc_m_ave_times = np.mean(lc_m_30_times) 
        
        # Append to the arrays
        m_nodes.append(m_ave_nodes)
        e_nodes.append(e_ave_nodes)
        lc_m_nodes.append(lc_m_ave_nodes)

        m_max_memory_used.append(m_ave_max_memory_used)
        e_max_memory_used.append(e_ave_max_memory_used)
        lc_m_max_memory_used.append(lc_m_ave_max_memory_used)

        m_times.append(m_ave_times)
        e_times.append(e_ave_times)
        lc_m_times.append(lc_m_ave_times)
    
    nodes_tuple = (m_nodes, e_nodes, lc_m_nodes)
    max_memory_used_tuple = (m_max_memory_used, e_max_memory_used, lc_m_max_memory_used)
    time_tuple = (m_times, e_times, lc_m_times)

    return (nodes_tuple, max_memory_used_tuple, time_tuple)


if __name__ == "__main__":
    # dim_3_tuples return a tuple which contains:
    # tuple[0]: the nodes generated for the puzzles for each heuristic
    # tuple[1]: the max nodes in memory for the puzzles for each heuristics 
    dim_3_tuples = getNodesExploredMaxMemorySizeAndTimeForKPuzzle(3)

    plotRunTimes(dim_3_tuples[0], dim_3_tuples[1], dim_3_tuples[2])
