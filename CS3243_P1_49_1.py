import os
import sys
import math
from random import randrange, sample


def swap(state, blank_tile_index, target_tile_index, debug=False):
        """ Swaps target tile with blank tile. Returns a new array.
        """
        new_state = state[:]
        temp = new_state[target_tile_index]
        new_state[target_tile_index] = state[blank_tile_index]
        new_state[blank_tile_index] = temp

        return new_state

def get_blank_tile(self, debug=False):
    i = self.state.index(0)
    result = {"index" : i}
    return result

def state_to_string(state):
    result = "".join(str(x) for x in state)
    return result

def is_legal_tile(target_tile_index, blank_tile_index, k, debug=False):
    
    list_right_edge = list()
    list_left_edge = list()
    for i in range(1, k + 1):
        list_right_edge.append(i * k - 1)
    for i in range(0, k):
        list_left_edge.append(i * k)
    # cannot move left
    if blank_tile_index in list_right_edge:
        return target_tile_index != blank_tile_index + 1 and 0 <= target_tile_index < k * k
    # cannot move right
    elif blank_tile_index in list_left_edge:
        return target_tile_index != blank_tile_index - 1 and 0 <= target_tile_index < k * k
    else:
        return 0 <= target_tile_index < k * k  

def opposite_actions(action, latest_action):
    if action == Actions.DOWN:
        return latest_action == Actions.UP
    if action == Actions.UP:
        return latest_action == Actions.DOWN
    if action == Actions.RIGHT:
        return latest_action == Actions.LEFT
    if action == Actions.LEFT:
        return latest_action == Actions.RIGHT

def is_goal_state(k, state, goal_state):
    for i in range(k * k):
        if state[i] != goal_state[i]:
                return False
    
    return True

def flatten_array(unflattened_array):
    flattened_arr = []
    for array in unflattened_array:
        for i in array:
            flattened_arr.append(i)

    return flattened_arr

def random_insert(lst, item):
    lst.insert(randrange(len(lst)+1), item)

def isEven(count):
        return count % 2 == 0

class Actions:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    ACTIONS = [UP, DOWN, LEFT, RIGHT]

class Puzzle(object):
    UNSOLVABLE = "UNSOLVABLE"
    CUTOFF = "CUTOFF"
    FAILURE = "FAILURE"

    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.flat_state = flatten_array(init_state)
        self.flat_goal_state = flatten_array(goal_state)
        self.init_state = self.flat_state
        self.init_node = {"state" : self.flat_state, "cost" : 0, "depth": 0, "actions_history": list()}
        self.goal_state = self.flat_goal_state
        self.actions = list()
        self.past_states = set()
        self.k = len(init_state)

    def transition(self, node, action):
        """ Moves the blank tile in the OPPOSITE direction specified by the action. (p4 of project1.pdf!
        Returns a new state.
        """
        blank_tile_index = node["state"].index(0)
        target_tile_index = blank_tile_index

        if action == Actions.DOWN:
            target_tile_index -= self.k
        elif action == Actions.UP:
            target_tile_index += self.k
        elif action == Actions.RIGHT:
            target_tile_index -= 1
        elif action == Actions.LEFT:
            target_tile_index += 1

        self.past_states.add(state_to_string(node["state"]))
        new_state = swap(node["state"], blank_tile_index, target_tile_index)
        new_cost = node["cost"] + 1
        new_depth = node["depth"] + 1
        actions_history = node["actions_history"]
        new_actions_history = actions_history[:]
        new_actions_history.append(action)

        new_node = {"state" : new_state, "cost" : new_cost, "depth": new_depth, "actions_history" : new_actions_history}
        return new_node

    def valid_actions(self, node):
        """ Returns an array of valid actions
        """
        result = []
        blank_tile_index = node["state"].index(0)

        for action in Actions.ACTIONS:
            actions_count = len(node["actions_history"])
            if actions_count > 0:
                latest_action = node["actions_history"][actions_count - 1]
                if opposite_actions(action, latest_action):
                    continue

            target_tile_index = blank_tile_index

            if action == Actions.DOWN:
                target_tile_index -= self.k
            elif action == Actions.UP:
                target_tile_index += self.k
            elif action == Actions.RIGHT:
                target_tile_index -= 1
            elif action == Actions.LEFT:
                target_tile_index += 1

            if is_legal_tile(target_tile_index, blank_tile_index, self.k):
                state_string = state_to_string(swap(node["state"], blank_tile_index, target_tile_index))
                if not self.is_explored_state(state_string):
                    result.append(action)

        return result

    def is_explored_state(self, state_string):
        return state_string in self.past_states

    @staticmethod
    def is_solvable(state):
        k = len(state)
        no_of_inversions = Puzzle.count_inversions(state)

        isKEven = isEven(k)
        isEvenInversions = isEven(no_of_inversions)
        if (not isKEven):
            if isEvenInversions:
                return True
            else:
                return False

        else:
            blank_tile_posi = (state.index(0))
            blank_tile_row_posi = int(blank_tile_posi / k)
            sum_of_inversions_and_blank_tile_row_posi = blank_tile_row_posi + no_of_inversions
            isSumEven = isEven(sum_of_inversions_and_blank_tile_row_posi)

            if (not isSumEven):
                print("Puzzle is solvable!")
                return True
            else:
                print("Puzzle is not solvable!")
                return False
        # method from https://www.cs.princeton.edu/courses/archive/spring18/cos226/assignments/8puzzle/index.html


    @staticmethod
    def count_inversions(flattened_arr):
        no_of_inversions = 0

        for i in range(len(flattened_arr)):
            for j in range(i, len(flattened_arr), 1):
                if flattened_arr[i] > flattened_arr[j] != 0:
                    no_of_inversions += 1

        return no_of_inversions



    def test(self):
        """ Unit tests for basic functions. Assumes the input file is n_equals_3/input_1.txt.

        """
        # Stubbed puzzle
        stubbed_init_state = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
        stubbed_goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        puzzle = Puzzle(stubbed_init_state, stubbed_goal_state)
        # Unit test for transition
        stubbed_state = [1, 2, 3, 4, 5, 6, 7, 0, 8]
        stubbed_node = {"state" : stubbed_state, "cost" : 0, "depth": 0, "actions_history": list()}
        stubbed_past_states = set()
        new_node = puzzle.transition(stubbed_node, Actions.LEFT)
        assert stubbed_node != new_node, "Unit test for transition is failing: transition should return a new node"
        assert new_node["state"][8] == 0, "Unit test for transition is failing: transition incorrectly"
        assert Actions.LEFT in new_node["actions_history"], \
            "Unit test for transition is failing: past actions should be updated"
        assert state_to_string(stubbed_state) in puzzle.past_states, \
            "Unit test for transition is failing: past states should be updated"

        # Unit test for solvable 3x3
        stubbed_state = [8, 1, 2, 0, 4, 3, 7, 6, 5]
        assert not Puzzle.is_solvable(stubbed_state) == True, \
            "Unit test for checking if 3x3 is unsolvable is failing"

        # Unit test for solvable 4x4
        stubbed_state = [3, 9, 1, 15, 14, 11, 4, 6, 13, 0, 10, 12, 2, 7, 8, 5]
        assert not Puzzle.is_solvable(stubbed_state) == True, \
            "Unit test for checking if 4x4 is unsolvable is failing"

        ### Node Tests

        # Unit test for swap
        stubbed_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        stubbed_target_tile_index = 7
        stubbed_blank_tile_index = 8
        new_state = swap(stubbed_state, stubbed_blank_tile_index, stubbed_target_tile_index)
        assert stubbed_state != new_state, "Unit test for swap node is failing: swap should return a new node"
        assert new_state[7] == 0, "Unit test for swap node is failing: swapping incorrectly"

        # Unit test for state to string
        stubbed_state = [1, 2, 3, 4, 5, 6, 8, 7, 0]
        # expected_state_string = "[1, 2, 3, 4, 5, 6, 8, 7, 0]"
        expected_state_string = "123456870"
        assert expected_state_string == state_to_string(stubbed_state), \
            "Unit test for state_to_string is failing."

        # Unit test for is_legal_tile
        stubbed_illegal_target_tile_index = 8
        stubbed_k = 3
        assert is_legal_tile(stubbed_illegal_target_tile_index, stubbed_blank_tile_index, stubbed_k) == True, \
            "Unit test for is_legal_tile is failing."

    def depth_limited_search(self, limit, debug=False):
        """ Depth Limited Search implementation that models the implementation in the textbook (p88).
        Set debug to True to print states.
        """
        return puzzle.recursive_DLS(self.init_node, limit, debug)

    def recursive_DLS(self, node, limit, debug=False):
        if debug:
            print(state_to_string(node["state"]))

        if is_goal_state(self.k, node["state"], self.goal_state):
            return node["actions_history"]
        elif limit == 0:
            return Puzzle.CUTOFF
        else:
            is_cutoff = False
            for action in self.valid_actions(node):
                child_node = puzzle.transition(node, action)

                result = puzzle.recursive_DLS(child_node, limit - 1, debug)
                if result == Puzzle.CUTOFF:
                    is_cutoff = True
                elif result != Puzzle.FAILURE:
                    return result
            if is_cutoff:
                return Puzzle.CUTOFF
            else:
                return Puzzle.FAILURE

    def iterative_deepening_search(self, debug=False):
        inf = 10000000

        for depth in range(0, inf):

            self.past_states = set()

            result = self.depth_limited_search(depth, debug)
            if result != Puzzle.CUTOFF:
                return result

    def solve(self):
        # TODO
        # implement your search algorithm here

        # Remove driver test in production
        
        # self.test()

        if not Puzzle.is_solvable(self.flat_state):
            self.actions.append(Puzzle.UNSOLVABLE)

        else:
            self.actions = self.iterative_deepening_search(debug=False)
            print("Space Complexity for IDS (size of explored set): " + str(len(self.past_states)))

        return self.actions  # sample output

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
