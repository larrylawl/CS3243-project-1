import os
import sys
from random import randrange

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
                        actions.append(actions)
                        self.move_by_action(new_puzzle, action)
                        print(len(actions))
                else:
                    actions.append(action)
                    self.move_by_action(new_puzzle, action)
                    print(len(actions))

        return new_puzzle
    
    # def generate_init_state(self, puzzle, actions):
    #     print("Original state:")
    #     print_puzzle(puzzle)
        
    #     for i in range(len(actions)):
    #         actions[i] = actions[i].rstrip('\n')

    #     if actions[0] == "UNSOLVABLE":
    #         print("The puzzle cannot be solved.")
    #     else:
    #         for k in range(len(actions)):
    #             self.move_by_action(puzzle, action)
    #             print_puzzle(puzzle)
        
    #     return puzzle
    
    def move_by_action(self, puzzle, action):
        if action == "DOWN":
            print("Move: DOWN")
            self.move_down(puzzle)
        elif action == "UP":
            print("Move: UP")
            self.move_up(puzzle)
        elif action == "LEFT":
            print("Move: LEFT")
            self.move_left(puzzle)
        else:
            print("Move: RIGHT")
            self.move_right(puzzle)

    def move_down(self, puzzle):
        x, y = self.get_zero(puzzle)
        puzzle[x][y] = puzzle[x - 1][y]
        puzzle[x - 1][y] = 0
        self.print_puzzle(puzzle)

    def move_up(self, puzzle):
        x, y = self.get_zero(puzzle)
        puzzle[x][y] = puzzle[x + 1][y]
        puzzle[x + 1][y] = 0
        self.print_puzzle(puzzle)

    def move_left(self, puzzle):
        x, y = self.get_zero(puzzle)
        puzzle[x][y] = puzzle[x][y + 1]
        puzzle[x][y + 1] = 0 
        self.print_puzzle(puzzle)

    def move_right(self, puzzle):
        x, y = self.get_zero(puzzle)
        puzzle[x][y] = puzzle[x][y - 1]
        puzzle[x][y - 1] = 0
        self.print_puzzle(puzzle)

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

if __name__ == "__main__":

    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    k = int(sys.argv[1])
    steps = int(sys.argv[2])

    print(k)

    print(steps)

    puzzleGenerator = KPuzzleGenerator(k, steps)
    goal_state = puzzleGenerator.generate_goal_state()
    print(goal_state)
    actions = puzzleGenerator.generate_init_state()
    print(actions)





