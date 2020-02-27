import os
import sys
import math

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
        self.actions_from_root = list()

    # def expand(self):


    # def parents(self):

    @staticmethod
    def swap(node, blank_tile, target_tile, debug=True):
        """ Swaps target tile with blank tile. Returns a new node.
        """
        new_node = deepcopy(node)
        temp = new_node.state[target_tile["index"]]
        new_node.state[target_tile["index"]] = new_node.state[blank_tile["index"]]
        new_node.state[blank_tile["index"]] = temp

        return new_node

    def get_blank_tile(self, debug=True):
        i = self.state.index(0)
        result = {"index" : i}
        return result

    @staticmethod
    def state_to_string(state):
        result = "[" + ", ".join(str(x) for x in state) + "]"
        return result

    @staticmethod
    def get_k(state):
        """ Returns an integer indicating the dimension of the k x k matrix
        """
        k = int(math.sqrt(len(state)))
        return k

    @staticmethod
    def is_legal_tile(target_tile, k, debug=True):
        return 0 <= target_tile["index"] < k * k


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
    def transition(past_states, node, action):
        """ Moves the blank tile in the OPPOSITE direction specified by the action. (p4 of project1.pdf!
        Returns a new state.
        """
        blank_tile = node.get_blank_tile()
        target_tile = deepcopy(blank_tile)

        if action == Actions.DOWN:
            target_tile["index"] -= node.k
        elif action == Actions.UP:
            target_tile["index"] += node.k
        elif action == Actions.RIGHT:
            target_tile["index"] -= 1
        elif action == Actions.LEFT:
            target_tile["index"] += 1

        past_states.add(Node.state_to_string(node.state))
        new_node = Node.swap(node, blank_tile, target_tile)
        new_node.cost += 1
        new_node.depth += 1
        new_node.actions_from_root.append(action)
        return new_node

    def valid_actions(self, node):
        """ Returns an array of valid actions
        """
        result = []
        blank_tile = node.get_blank_tile()

        for action in Actions.ACTIONS:
            target_tile = deepcopy(blank_tile)
            if action == Actions.DOWN:
                target_tile["index"] -= node.k
            elif action == Actions.UP:
                target_tile["index"] += node.k
            elif action == Actions.RIGHT:
                target_tile["index"] -= 1
            elif action == Actions.LEFT:
                target_tile["index"] += 1

            if Node.is_legal_tile(target_tile, node.k):
                state_string = Node.state_to_string(Node.swap(node, blank_tile, target_tile).state)
                if not Puzzle.is_explored_state(self.past_states, state_string):
                    result.append(action)
        return result

    @staticmethod
    def is_explored_state(past_states, state_string):
        return state_string in past_states

    @staticmethod
    def is_solvable(init_state):
        k = len(init_state)
        no_of_inversions = Puzzle.count_inversions(init_state)

        isKEven = Puzzle.even(k)
        isEvenInversions = Puzzle.even(no_of_inversions)
        if (not isKEven):
            if isEvenInversions:
                print("Puzzle is solvable!")
                return True
            else:
                print("Puzzle is not solvable!")
                return False

        else:
            blank_tile_posi = (init_state.index(0))
            blank_tile_row_posi = int(blank_tile_posi / k)
            sum_of_inversions_and_blank_tile_row_posi = blank_tile_row_posi + no_of_inversions
            isSumEven = Puzzle.even(sum_of_inversions_and_blank_tile_row_posi)

            if (not isSumEven):
                print("Puzzle is solvable!")
                return True
            else:
                print("Puzzle is not solvable!")
                return False
        # method from https://www.cs.princeton.edu/courses/archive/spring18/cos226/assignments/8puzzle/index.html

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
    def is_goal_state(k, state, goal_state):
        for i in range(k):
            if state[i] != goal_state[i]:
                    return False
        
        return True

    def test(self):
        """ Unit tests for basic functions. Assumes the input file is n_equals_3/input_1.txt.

        """

        # Unit test for transition
        stubbed_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        stubbed_node = Node(state=stubbed_state)
        stubbed_past_states = set()
        new_node = Puzzle.transition(stubbed_past_states, stubbed_node, Actions.RIGHT)
        assert stubbed_node != new_node, "Unit test for transition is failing: transition should return a new node"
        assert new_node.state[7] == 0, "Unit test for transition is failing: transition incorrectly"
        assert Actions.RIGHT in new_node.actions_from_root, \
            "Unit test for transition is failing: past actions should be updated"
        assert Node.state_to_string(stubbed_state) in stubbed_past_states, \
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

        # Unit test for swap node
        stubbed_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        stubbed_target_tile = {"index": 7}
        stubbed_blank_tile = {"index": 8}
        node = Node(state=stubbed_state)
        new_node = Node.swap(node, stubbed_blank_tile, stubbed_target_tile)
        assert node != new_node, "Unit test for swap node is failing: swap should return a new node"
        assert new_node.state[7] == 0, "Unit test for swap node is failing: swapping incorrectly"

        # Unit test for state to string
        stubbed_state = [1, 2, 3, 4, 5, 6, 8, 7, 0]
        expected_state_string = "[1, 2, 3, 4, 5, 6, 8, 7, 0]"
        assert expected_state_string == Node.state_to_string(stubbed_state), \
            "Unit test for state_to_string is failing."

        # Unit test for is_legal_tile
        stubbed_illegal_target_tile = {"index" : 8}
        stubbed_k = 3
        assert Node.is_legal_tile(stubbed_illegal_target_tile, stubbed_k) == True, \
            "Unit test for is_legal_tile is failing."

    @staticmethod
    def depth_limited_search(puzzle, limit, debug=True):
        """ Depth Limited Search implementation that models the implementation in the textbook (p88).
        Set debug to True to print states.
        """
        return Puzzle.recursive_DLS(puzzle.init_node, puzzle, limit, debug)

    @staticmethod
    def recursive_DLS(node, puzzle, limit, debug=False):
        #print(Node.state_to_string(node.state))
        if Puzzle.is_goal_state(node.k, node.state, puzzle.goal_state):
            return node.actions_from_root
        elif limit == 0:
            return Puzzle.CUTOFF
        else:
            is_cutoff = False
            for action in puzzle.valid_actions(node):
                child_node = Puzzle.transition(puzzle.past_states, node, action)

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

    @staticmethod
    def iterative_deepening_search(puzzle, debug=False):
        inf = 10000000

        for depth in range(0, inf):

            puzzle.past_states = set()

            result = Puzzle.depth_limited_search(puzzle, depth, debug)
            if result != Puzzle.CUTOFF:
                return result

    def solve(self):
        # TODO
        # implement your search algorithm here

        # Remove driver test in production
        self.test()

        if not Puzzle.is_solvable(self.init_state):
            self.actions.append(Puzzle.UNSOLVABLE)

        self.actions = Puzzle.iterative_deepening_search(puzzle, debug=False)
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

    # Instantiate a 1D list of size n x n
    init_state = []
    goal_state = [0 for i in range(n ** 2)]

    for line in lines:
        line = line.strip()
        for number in line.split(" "):
            init_state.append(int(number))

    for i in range(0, max_num):
        goal_state[i] = i + 1
    goal_state[n * n - 1] = 0

    print(Node.state_to_string(init_state))
    print(Node.state_to_string(goal_state))
    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer + '\n')
