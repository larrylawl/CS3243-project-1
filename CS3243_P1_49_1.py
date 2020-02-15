import os
import sys

"""
TODO
1. Learn how to run programme. Check if it reach goal
1. Learn how to run the programme and test it
    1.1 SoC computing cluster
2. Understand the programme
    2.1 Data structure that 1) swaps elts in o(1) and 2) compare with goal state in o(1)
3. Implement IDS (with O(d) space complexity)
"""

class Puzzle(object):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.state = self.init_state
        self.k = Puzzle.get_k(init_state)
        self.blank_tile = Puzzle.get_blank_tile(init_state, self.k)

    @staticmethod
    def transition(puzzle, action):
        """ Moves the blank tile in a direction specified by the action.
        Args:
            param1 (dictionary): State of the puzzle
            param2 (int): Integer which denotes the key of the blank tile
            param3 (int): Integer which denotes the key of the target tile
        """
        target_tile = puzzle.blank_tile
        if action == UP:
            target_tile["row"] -= 1
        elif action == DOWN:
            target_tile["row"] += 1
        elif action == LEFT:
            target_tile["col"] -= 1
        elif action == RIGHT:
            target_tile["col"] += 1

        if is_illegal_tile(target):
            return puzzle

    @staticmethod
    def get_k(state):
        """ Returns an integer indicating the dimension of the k x k matrix
        """
        k = len(state)
        return k

    @staticmethod
    def get_blank_tile(state, k):
        result = {"row": -1, "col": -1}
        for i in range(0, k):
            for j in range(0, k):
                if state[i][j] == 0:
                    result["row"] = i
                    result["col"] = j
        return result


    @staticmethod
    def is_solvable(init_state):
        """ Checks if the given initial state is solvable.
        Args:
            param1 (dictionary): State of the puzzle

        Returns:
            boolean: True if state is solvable.
        """

    def is_goal_state(self):
        """ Checks if the given state is a goal state in O(1) time.
        Args:
            param1 (): State of the puzzle

        Returns:
            boolean: True if state is a goal state.
        """
        return self.state == self.goal_state

    def solve(self):
        #TODO
        # implement your search algorithm here
        print(self.init_state)
        print(self.blank_tile)
        print(self.k)
        
        return ["LEFT", "RIGHT"] # sample output 

    # you may add more functions if you think is useful

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    

    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')







