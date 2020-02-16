import os
import sys

"""
Objective: Get programme working. Worry about time/space complexity later.

Steps:
1. IDS
2. Time Complexity
3. Space Complexity

TODO
1. Learn how to run the programme and test it
    1.1 SoC computing cluster
2. Understand the programme
    2.1 Data structure that 1) swaps elts in o(1) and 2) compare with goal state in o(1)
3. Implement IDS (with O(d) space complexity)
4. Measure space and time complexity
4. Run on sunfire to check
"""
from copy import deepcopy


class Actions:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    ACTIONS = [UP, DOWN, LEFT, RIGHT]

class Node:
    def __init__(self, state=None, parent=None, cost=0, depth=0, children=[]):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.depth = depth
        self.children = children
        self.k = Node.get_k(state)

    # def expand(self):


    # def parents(self):

    @staticmethod
    def swap(node, blank_tile, target_tile):
        """ Swaps target tile with blank tile. Returns a new node.
        """
        new_node = deepcopy(node)
        temp = new_node.state[target_tile["row"]][target_tile["col"]]
        new_node.state[target_tile["row"]][target_tile["col"]] = new_node.state[blank_tile["row"]][blank_tile["col"]]
        new_node.state[blank_tile["row"]][blank_tile["col"]] = temp

        return new_node

    def get_blank_tile(self):
        result = {"row": -1, "col": -1}
        for i in range(0, self.k):
            for j in range(0, self.k):
                if self.state[i][j] == 0:
                    result["row"] = i
                    result["col"] = j
        return result

    @staticmethod
    def state_to_string(state):
        result = "[" + ", ".join(str(x) for x in state) + "]"
        return result

    @staticmethod
    def get_k(state):
        """ Returns an integer indicating the dimension of the k x k matrix
        """
        k = len(state)
        return k

    @staticmethod
    def is_legal_tile(target_tile, k):
        return 0 <= target_tile["row"] < k and 0 <= target_tile["col"] < k


class Puzzle(object):
    UNSOLVABLE = "UNSOLVABLE"
    CUTOFF = "CUTOFF"
    FAILURE = "FAILURE"

    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.init_node = Node(state=init_state)
        self.goal_state = goal_state
        self.goal_node = Node(state=goal_state)
        self.actions = list()
        self.past_states = set()

    @staticmethod
    def transition(past_states, actions, node, action):
        """ Moves the blank tile in a direction specified by the action. Returns a new state.
        """
        # print(node)
        blank_tile = node.get_blank_tile()
        target_tile = deepcopy(blank_tile)
        if action == Actions.UP:
            target_tile["row"] -= 1
        elif action == Actions.DOWN:
            target_tile["row"] += 1
        elif action == Actions.LEFT:
            target_tile["col"] -= 1
        elif action == Actions.RIGHT:
            target_tile["col"] += 1

        past_states.add(Node.state_to_string(node.state))
        new_node = Node.swap(node, blank_tile, target_tile)
        new_node.cost += 1
        new_node.depth += 1
        actions.append(action)
        return new_node

    @staticmethod
    def valid_actions(node):
        """ Returns an array of valid actions
        """
        result = []
        blank_tile = node.get_blank_tile()

        for action in Actions.ACTIONS:
            target_tile = deepcopy(blank_tile)
            if action == Actions.UP:
                target_tile["row"] -= 1
            elif action == Actions.DOWN:
                target_tile["row"] += 1
            elif action == Actions.LEFT:
                target_tile["col"] -= 1
            elif action == Actions.RIGHT:
                target_tile["col"] += 1

            if Node.is_legal_tile(target_tile, node.k):
                result.append(action)
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

            if (not isEvenInversions and isEvenFrmBtm) \
                    or (isEvenInversions and not isEvenFrmBtm):
                return True
            else:
                return False
        # method from https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/

    @staticmethod
    def even(count):
        return count % 2 == 0

    @staticmethod
    def count_inversions(flattened_arr):
        no_of_inversions = 0

        for i in range(len(flattened_arr)):
            for j in range(i, len(flattened_arr), 1):
                if flattened_arr[i] > flattened_arr[j] != 0:
                    no_of_inversions += 1

        return no_of_inversions

    @staticmethod
    def is_goal_state(state, goal_state):
        return state == goal_state

    def test(self):
        """ Unit tests for basic functions. Assumes the input file is n_equals_3/input_1.txt.

        """

        # Unit test for swap
        # stubbed_self = deepcopy(self)
        # stubbed_target_tile = {"row": 0, "col": 0}
        # stubbed_self.swap(stubbed_target_tile)
        # assert stubbed_self.state[0][0] == 0, "Unit test for swap is failing."

        # Unit test for transition
        stubbed_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        stubbed_node = Node(state=stubbed_state)
        stubbed_past_states = set()
        stubbed_past_actions = []
        new_node = Puzzle.transition(stubbed_past_states, stubbed_past_actions, stubbed_node, Actions.LEFT)
        assert stubbed_node != new_node, "Unit test for transition is failing: transition should return a new node"
        assert new_node.state[2][1] == 0, "Unit test for transition is failing: transition incorrectly"
        assert Actions.LEFT in stubbed_past_actions, \
            "Unit test for transition is failing: past actions should be updated"
        assert Node.state_to_string(stubbed_state) in stubbed_past_states, \
            "Unit test for transition is failing: past states should be updated"

        # Unit test for solvable 3x3
        stubbed_state = [[8, 1, 2], [0, 4, 3], [7, 6, 5]]
        assert not Puzzle.is_solvable(stubbed_state) == True, \
            "Unit test for checking if 3x3 is unsolvable is failing"

        # Unit test for solvable 4x4
        stubbed_state = [[3, 9, 1, 15], [14, 11, 4, 6], [13, 0, 10, 12], [2, 7, 8, 5]]
        assert not Puzzle.is_solvable(stubbed_state) == True, \
            "Unit test for checking if 4x4 is unsolvable is failing"

        ### Node Tests

        # Unit test for swap node
        stubbed_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        stubbed_target_tile = {"row": 2, "col": 1}
        stubbed_blank_tile = {"row": 2, "col": 2}
        node = Node(state=stubbed_state)
        new_node = Node.swap(node, stubbed_blank_tile, stubbed_target_tile)
        assert node != new_node, "Unit test for swap node is failing: swap should return a new node"
        assert new_node.state[2][1] == 0, "Unit test for swap node is failing: swapping incorrectly"

        # Unit test for state to string
        stubbed_state = [[1, 2, 3], [4, 5, 6], [8, 7, 0]]
        expected_state_string = "[[1, 2, 3], [4, 5, 6], [8, 7, 0]]"
        assert expected_state_string == Node.state_to_string(stubbed_state), \
            "Unit test for state_to_string is failing."

        # Unit test for is_legal_tile
        stubbed_illegal_target_tile = {"row": 2, "col": 2}
        stubbed_k = 3
        assert Node.is_legal_tile(stubbed_illegal_target_tile, stubbed_k) == True, \
            "Unit test for is_legal_tile is failing."

    @staticmethod
    def depth_limited_search(puzzle, limit, debug=False):
        """ Depth Limited Search implementation that models the implementation in the textbook (p88).
        """
        return Puzzle.recursive_DLS(puzzle.init_node, puzzle, limit, debug)

    # TODO: Add graph search
    # TODO: Way to print states to check
    # TODO: Run on sunfire to check
    @staticmethod
    def recursive_DLS(node, puzzle, limit, debug=False):
        if Puzzle.is_goal_state(node.state, puzzle.goal_state):
            return puzzle.actions
        elif limit == 0:
            return Puzzle.CUTOFF
        else:
            is_cutoff = False
            for action in Puzzle.valid_actions(node):
                child_node = Puzzle.transition(puzzle.past_states, puzzle.actions, node, action)

                if debug:
                    print(child_node.state)

                result = Puzzle.recursive_DLS(child_node, puzzle, limit - 1, debug)
                if result == Puzzle.CUTOFF:
                    is_cutoff = True
                elif result != Puzzle.FAILURE:
                    return result
            if is_cutoff:
                return Puzzle.CUTOFF
            else:
                return Puzzle.FAILURE


    # def IDS(self):
    #     inf = sys.maxint
    #
    #     for depth in range(0, inf):
    #         result = DLS(self, depth)
    #         if result

    def solve(self):
        # TODO
        # implement your search algorithm here
        self.test()

        if not Puzzle.is_solvable(self.init_state):
            self.actions.append(Puzzle.UNSOLVABLE)

        Puzzle.depth_limited_search(self, 5, debug=True)
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

    i, j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number, base=10)
            if 0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i - 1) // n][(i - 1) % n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer + '\n')
