import os
import sys

"""
Objective: Get programme working. Worry about time/space complexity later.

TODO
1. Learn how to run the programme and test it
    1.1 SoC computing cluster
2. Understand the programme
    2.1 Data structure that 1) swaps elts in o(1) and 2) compare with goal state in o(1)
3. Implement IDS (with O(d) space complexity)
"""
from copy import deepcopy

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
        self.state = deepcopy(init_state)
        self.k = Puzzle.get_k(init_state)
        self.blank_tile = Puzzle.get_blank_tile(init_state, self.k)

    def transition(self, action):
        """ Moves the blank tile in a direction specified by the action. Mutates node's state and blank tile position.
        """
        target_tile = deepcopy(self.blank_tile) # deep copy
        if action == Puzzle.UP:
            target_tile["row"] -= 1
        elif action == Puzzle.DOWN:
            target_tile["row"] += 1
        elif action == Puzzle.LEFT:
            target_tile["col"] -= 1
        elif action == Puzzle.RIGHT:
            target_tile["col"] += 1

        if Puzzle.is_legal_tile(target_tile, self.k):
            self.swap(target_tile)
            self.actions.append(action)

        return self

    def swap(self, target_tile):
        """ Swaps target tile with blank tile. Mutates state and blank tile position.

        """
        temp = self.state[target_tile["row"]][target_tile["col"]]
        self.state[target_tile["row"]][target_tile["col"]] = self.state[self.blank_tile["row"]][self.blank_tile["col"]]
        self.state[self.blank_tile["row"]][self.blank_tile["col"]] = temp

        # Updating position of blank_tile
        self.blank_tile = target_tile

    @staticmethod
    def is_legal_tile(target_tile, k):
        return 0 <= target_tile["row"] < k and 0 <= target_tile["col"] < k

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
    def flatten_array(unflattened_array):
        flattened_arr = []
        for array in unflattened_array:
            for i in array:
                flattened_arr.append(i)
        
        return flattened_arr

    @staticmethod
    def is_solvable(init_state):

        flattened_arr = Puzzle.flatten_array(init_state)
        no_of_rows = len(init_state)
        no_of_inversions = Puzzle.count_inversions(flattened_arr)

        isEvenRows = Puzzle.even(no_of_rows)
        isEvenInversions = Puzzle.even(no_of_inversions)
        if (not isEvenRows):
            if isEvenInversions:
                return True
            else:
                return False

        else:
            blank_tile_posi = (flattened_arr.index(0)) 
            count_frm_btm = no_of_rows - int(blank_tile_posi / no_of_rows)
            isEvenFrmBtm = Puzzle.even(count_frm_btm)
    
            if (not isEvenInversions and isEvenFrmBtm)\
                or (isEvenInversions and not isEvenFrmBtm):
                return True
            else:
                return False
        # method from https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
            

    @staticmethod
    def even(count):
        return count % 2 == 0

    @staticmethod
    def is_goal_state(current_state, goal_state):
        return current_state == goal_state

    @staticmethod
    def count_inversions(flattened_arr):
        no_of_inversions = 0
   
        for i in range(len(flattened_arr)):
            for j in range(i,len(flattened_arr),1):
                if (flattened_arr[i] > flattened_arr[j] and flattened_arr[j] != 0):
                    no_of_inversions += 1
        
        return no_of_inversions
        

    def test(self):
        """ Unit tests for basic functions. Assumes the input file is n_equals_3/input_1.txt.

        """

        # Unit test for is_legal_tile
        stubbed_illegal_target_tile = {"row": 2, "col": 2}
        stubbed_k = 3
        assert Puzzle.is_legal_tile(stubbed_illegal_target_tile, stubbed_k) == True, \
            "Unit test for is_legal_tile is failing."

        # Unit test for swap
        stubbed_self = deepcopy(self)
        stubbed_target_tile = {"row": 0, "col": 0}
        stubbed_self.swap(stubbed_target_tile)
        assert stubbed_self.state[0][0] == 0, "Unit test for swap is failing."

        # Unit test for transition
        stubbed_self = deepcopy(self)
        stubbed_state = [[1, 2, 3], [4, 5, 6], [8, 7, 0]]
        new_state = stubbed_self.transition(Puzzle.RIGHT).state
        assert new_state == stubbed_state, \
            "Unit test for transition is failing: action is illegal so state should not change"

        stubbed_self = deepcopy(self)
        new_state = stubbed_self.transition(Puzzle.LEFT).state
        assert new_state[2][2] == 7, "Unit test for transition is failing."
        assert stubbed_self.blank_tile == {"row": 2, "col": 1}, \
            "Unit test for transition is failing: Blank tile attribute is incorrect."

        #Unit test for solvable 3x3
        stubbed_state = [[8, 1, 2], [0, 4, 3], [7, 6, 5]]
        assert not Puzzle.is_solvable(stubbed_state) == True, \
            "Unit test for checking if 3x3 is unsolvable is failing"

        #Unit test for solvable 4x4
        stubbed_state = [[3, 9, 1, 15], [14, 11, 4, 6], [13, 0, 10, 12], [2, 7, 8, 5]]
        assert not Puzzle.is_solvable(stubbed_state) == True, \
            "Unit test for checking if 4x4 is unsolvable is failing"

        # Unit test for is_goal_state
        stubbed_self = deepcopy(self)
        stubbed_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        assert Puzzle.is_goal_state(stubbed_state, stubbed_self.goal_state), "Unit test for is_goal_state is failing."

    # def IDS(self):

    def solve(self):
        #TODO
        # implement your search algorithm here
        self.test()
        return self.actions # sample output

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







